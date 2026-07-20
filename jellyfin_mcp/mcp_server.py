#!/usr/bin/python
"""Jellyfin MCP Server module.

Dynamic Tool Routing
"""

import logging
import sys
from typing import Any

from agent_utilities.core.config import load_config
from agent_utilities.mcp.action_dispatch import dispatch_async, parse_json_object
from agent_utilities.mcp.concurrency import run_blocking
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from jellyfin_mcp.api_client import Api
from jellyfin_mcp.auth import get_client

__version__ = "1.0.1"

logger = get_logger(name="jellyfin-mcp")
logger.setLevel(logging.INFO)


def register_condensed_jellyfin_tools(mcp: FastMCP):
    """Register highly optimized, condensed tools mapping dynamically to Jellyfin client methods.

    Dynamic Tool Routing
    """

    @mcp.tool(tags={"Media"})
    async def jellyfin_media(
        action: str = Field(
            description="The media-related client method to execute. Examples: get_artists, get_artist_by_name, get_album_artists, get_audio_stream, get_audio_stream_by_container, get_genres, get_musicgenres, get_movies, get_playlists, get_playstate, get_subtitle, get_lyrics, get_trickplay, get_videos."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of keyword parameters to pass to the method.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute media playback, stream, artist, playlist, and audio/video queries dynamically.

        Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing media action: {action}...")
        try:
            kwargs = parse_json_object(params_json)
        except ValueError:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await dispatch_async(
                client, action, kwargs, service="jellyfin-mcp", ctx=ctx
            )
        except ValueError:
            return {"error": "Operation failed"}
        except Exception as e:
            return {"error": f"Media action failed: {type(e).__name__}"}

    @mcp.tool(tags={"Library"})
    async def jellyfin_library(
        action: str = Field(
            description="The library or search-related client method to execute. Examples: get_items, get_item_by_id, search_items, get_collections, create_collection, add_to_collection, remove_from_collection, get_library_info, get_user_views, get_user_library, get_library_structure, get_channels, get_channel_items, get_latest_channel_items."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of keyword parameters to pass to the method.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute library searches, items, collection updates, and catalog queries dynamically.

        Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing library action: {action}...")
        try:
            kwargs = parse_json_object(params_json)
        except ValueError:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await dispatch_async(
                client, action, kwargs, service="jellyfin-mcp", ctx=ctx
            )
        except ValueError:
            return {"error": "Operation failed"}
        except Exception as e:
            return {"error": f"Library action failed: {type(e).__name__}"}

    @mcp.tool(tags={"System"})
    async def jellyfin_system(
        action: str = Field(
            description="The administrative, system, or configuration-related client method to execute. Examples: get_log_entries, get_keys, create_key, revoke_key, get_system_info, get_users, get_devices, list_backups, create_backup, get_backup, start_restore_backup, get_branding_options, get_configuration, update_configuration, log_file."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of keyword parameters to pass to the method.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute administrative actions, system status, configurations, backups, and user management.

        Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing system action: {action}...")
        try:
            kwargs = parse_json_object(params_json)
        except ValueError:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await dispatch_async(
                client, action, kwargs, service="jellyfin-mcp", ctx=ctx
            )
        except ValueError:
            return {"error": "Operation failed"}
        except Exception as e:
            return {"error": f"System action failed: {type(e).__name__}"}


def register_kg_ingest_tools(mcp: FastMCP):
    """Register native epistemic-graph ingestion tools (Wire-First).

    CONCEPT:AU-KG.ingest.enterprise-source-extractor. Lists the real Jellyfin library
    via the client and pushes it into the knowledge graph as typed :MediaItem/:Book/
    :Artist/:Genre nodes (+ item overviews as :Document, + posters as :Blob).
    """

    @mcp.tool(tags={"misc", "kg"})
    async def jellyfin_ingest_library(
        params_json: str = Field(
            default="{}",
            description="JSON string of get_items filters (e.g. include_item_types, "
            "parent_id, limit, recursive).",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Natively ingest the Jellyfin library into epistemic-graph as typed nodes.

        Lists items via ``get_items`` and pushes them (with :hasGenre/:performedBy/
        :authoredBy links + item overviews as :Document) into the knowledge graph.
        Best-effort: ``ingested`` is ``None`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from jellyfin_mcp.kg_ingest import ingest_items

        try:
            kwargs = _json.loads(params_json) if params_json else {}
        except Exception:
            return {"error": "Operation failed"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            resp = await run_blocking(client.get_items, **kwargs)
        except Exception:
            return {"error": "get_items failed"}
        data = getattr(resp, "data", resp)
        items = data.get("Items", []) if isinstance(data, dict) else data
        items = items if isinstance(items, list) else [items]
        result = ingest_items(items)
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
        from jellyfin_mcp.kg_media import ingest_image_bytes, media_store

        store = media_store()
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
            res = ingest_image_bytes(
                data, item_id=iid, image_type=image_type, store=store
            )
            if res:
                stored.append(res)
        return {"requested": len(item_ids or []), "stored": stored}

    return None


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance.

    Dynamic Tool Routing
    """
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="jellyfin-mcp MCP",
        version=__version__,
        instructions="jellyfin-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="jellyfin-mcp",
        tools_module=sys.modules[__name__],
    )

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    """Run the MCP server.

    Dynamic Tool Routing
    """
    mcp, args, middlewares = get_mcp_instance()
    print(f"jellyfin-mcp MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
