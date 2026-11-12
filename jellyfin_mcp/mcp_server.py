#!/usr/bin/python
"""Jellyfin MCP Server module.

Dynamic Tool Routing
"""

import logging
from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from scion_sdk.mcp.concurrency import run_blocking

from jellyfin_mcp.auth import get_client

logger = get_logger(name="jellyfin-mcp")
logger.setLevel(logging.INFO)


def register_kg_ingest_tools(mcp: FastMCP):
    """Register native medulla ingestion tools (Wire-First).

    CONCEPT:AU-KG.ingest.enterprise-source-extractor. Lists the real Jellyfin library
    via the client and pushes it into the knowledge graph as typed :MediaItem/:Book/
    :Artist/:Genre nodes (+ item overviews as :Document, + posters as :Blob).
    """

    @mcp.tool(tags={"misc", "kg"})
    async def jellyfin_ingest_library(
        include_item_types: list[str] | None = Field(
            default=None,
            description="Jellyfin item types to ingest (e.g. Movie, Series, Audio).",
        ),
        parent_id: str | None = Field(
            default=None, description="Only ingest items under this parent Id."
        ),
        limit: int | None = Field(
            default=None, description="Maximum number of items to list."
        ),
        recursive: bool | None = Field(
            default=True, description="Recurse into child folders."
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Natively ingest the Jellyfin library into medulla as typed nodes.

        Lists items via ``get_items`` and pushes them (with :hasGenre/:performedBy/
        :authoredBy links + item overviews as :Document) into the knowledge graph.
        Best-effort: ``ingested`` is ``None`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from jellyfin_mcp.kg_ingest import ingest_items

        kwargs = {
            "include_item_types": include_item_types,
            "parent_id": parent_id,
            "limit": limit,
            "recursive": recursive,
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            resp = await run_blocking(client.get_items, **kwargs)
        except Exception:
            return {"error": "get_items failed"}
        data = getattr(resp, "data", resp)
        items = data.get("Items", []) if isinstance(data, dict) else data
        items = items if isinstance(items, list) else [items]
        result = await ingest_items(items)
        return {"listed": len(items), "ingested": result}

    @mcp.tool(tags={"misc", "kg"})
    async def jellyfin_ingest_posters(
        item_ids: list[str] = Field(
            default_factory=list,
            description="Jellyfin item Ids whose primary poster image to ingest as blobs.",
        ),
        image_type: str = Field(default="Primary", description="Jellyfin image type."),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest item posters as content-addressed :Blob + :AssetOccurrence (best-effort).

        CONCEPT:AU-KG.ingest.list-durable-media.
        """
        from jellyfin_mcp.kg_media import ingest_image_bytes

        stored: list[dict[str, Any]] = []
        for iid in item_ids or []:
            try:
                raw = await run_blocking(
                    client.get_item_image, item_id=iid, image_type=image_type
                )
            except Exception as e:
                logger.debug("Poster fetch failed: error_type=%s", type(e).__name__)
                continue
            data = raw if isinstance(raw, bytes) else None
            if data is None and isinstance(raw, str):
                data = raw.encode("latin-1", "ignore")
            res = await ingest_image_bytes(data, item_id=iid, image_type=image_type)
            if res:
                stored.append(res)
        return {"requested": len(item_ids or []), "stored": stored}

    return None
