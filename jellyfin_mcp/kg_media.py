"""Native epistemic-graph blob ingestion for Jellyfin artwork / media bytes.

CONCEPT:AU-KG.ingest.list-durable-media. A Jellyfin item's **poster / primary image**
(or any downloaded bytes) is stored as a content-addressed :Blob with a linked
:MediaAsset graph node in ONE cross-modal ACID commit, via the agent-utilities
``MediaStore``. This makes the raw artwork bytes — not just an image URL — durable,
deduped, and queryable inside the knowledge graph beside the typed library nodes that
``jellyfin_mcp.kg_ingest`` writes.

Best-effort and dependency-/engine-guarded: with no KG stack or no reachable engine every
entry point **no-ops** (returns ``None``), so the connector runs with zero KG infrastructure.
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
    """Build a ``MediaStore`` over a live engine, or ``None`` when unavailable.

    Prefers the shared ``native_ingest.media_store`` primitive; falls back to
    constructing one directly. Never raises.
    """
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest.media_store()
    except Exception as e:  # noqa: BLE001 — shared primitive absent
        logger.debug("shared media_store unavailable: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG media ingest unavailable (import): %s", e)
        return None
    try:
        engine = GraphComputeEngine()
        if getattr(engine, "_client", None) is None:
            return None
        return MediaStore(engine)
    except Exception as e:  # noqa: BLE001 — no reachable engine
        logger.debug("KG media ingest: engine unreachable: %s", e)
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
    """Store Jellyfin item artwork as a :Blob + :MediaAsset in the knowledge graph.

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
        logger.warning("KG media ingest: store_media failed: %s", e)
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
