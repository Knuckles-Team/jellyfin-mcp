"""Native epistemic-graph blob ingestion for Jellyfin artwork / media bytes.

CONCEPT:AU-KG.ingest.list-durable-media. A Jellyfin item's **poster / primary image**
(or any downloaded bytes) is stored as a content-addressed :Blob with a linked
:AssetOccurrence graph node in ONE cross-modal ACID commit, via a ``MediaStore``.
This makes the raw artwork bytes — not just an image URL — durable, deduped, and
queryable inside the knowledge graph beside the typed library nodes that
``jellyfin_mcp.kg_ingest`` writes.

Best-effort and dependency-/engine-guarded: with no KG stack or no reachable engine every
entry point **no-ops** (returns ``None``), so the connector runs with zero KG infrastructure.

SDK GAP (EH-481/SDK-GAPS.md): this used to build a ``MediaStore`` over
``agent_utilities.knowledge_graph.memory.native_ingest.media_store`` (or, as a fallback,
``agent_utilities.knowledge_graph.core.graph_compute.GraphComputeEngine`` +
``agent_utilities.knowledge_graph.memory.media_store.MediaStore`` directly). The SDK has no
equivalent blob/media store primitive yet. Until the gap is filled, ``media_store()`` always
returns ``None``; every call site above keeps working as a documented no-op.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("jellyfin_mcp.kg.media")

_SOURCE = "jellyfin-mcp"

# Jellyfin image-format -> mime.
_MIME_BY_EXT = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
}


def media_store() -> Any | None:
    """No native ``MediaStore`` authority is wired yet; see the SDK-GAPS note above."""
    return None


def ingest_image_bytes(
    data: bytes | None,
    *,
    item_id: str,
    name: str = "",
    image_format: str = "jpg",
    image_type: str = "Primary",
    store: Any | None = None,
) -> dict[str, Any] | None:
    """Store Jellyfin item artwork as a :Blob + :AssetOccurrence in the knowledge graph.

    Returns ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None``
    when there is no engine, no bytes, or the store failed (never raises).
    ``store`` may be injected (tests); otherwise one is built on demand.
    """
    if not data:
        return None
    store = store if store is not None else media_store()
    if store is None:
        return None

    mime = _MIME_BY_EXT.get(str(image_format).lower().lstrip("."), "image/jpeg")
    extra = {
        "jellyfin_item_id": str(item_id),
        "image_type": image_type,
        "source_uri": f"jellyfin://item/{item_id}/images/{image_type}",
    }
    try:
        stored = store.store_media(
            data,
            media_type="image",
            mime_type=mime,
            source=_SOURCE,
            name=name or f"{item_id}-{image_type}",
            extra=extra,
        )
    except Exception as e:  # noqa: BLE001 — engine/store failure is non-fatal
        logger.warning("Operation failed: error_type=%s", type(e).__name__)
        return None
    if stored is None:
        return None

    logger.info(
        "KG media ingest: stored %s poster (%d bytes) as asset %s",
        item_id,
        len(data),
        getattr(stored, "asset_id", "?"),
    )
    return {
        "asset_id": getattr(stored, "asset_id", None),
        "digest": getattr(stored, "digest", None),
        "size_bytes": len(data),
        "media_type": "image",
    }
