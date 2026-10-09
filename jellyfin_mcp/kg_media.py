"""Native epistemic-graph blob ingestion for Jellyfin artwork / media bytes.

CONCEPT:AU-KG.ingest.list-durable-media. A Jellyfin item's **poster / primary image**
(or any downloaded bytes) is stored as a content-addressed blob with a linked
``:MediaAsset`` graph node in ONE cross-modal ACID commit, via the
``agent_connector_sdk.ingest`` facade. This makes the raw artwork bytes — not just an
image URL — durable, deduped, and queryable inside the knowledge graph beside the typed
library nodes that ``jellyfin_mcp.kg_ingest`` writes.

The knowledge-ingest service is obtained through ``agent_connector_sdk.ingest
.current_ingest()`` (process-installed, or connected from settings on first use).
Best-effort and engine-guarded: with no reachable engine every entry point **no-ops**
(returns ``None``, never raises), so the connector runs with zero KG infrastructure.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    IngestBinding,
    IngestError,
    IngestUnavailableError,
    KnowledgeIngest,
    MediaAsset,
    current_ingest,
)

logger = logging.getLogger("jellyfin_mcp.kg.media")

_BINDING = IngestBinding(connector="jellyfin-mcp", stream="media")

# Jellyfin image-format -> mime.
_MIME_BY_EXT = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
}


async def ingest_image_bytes(
    data: bytes | None,
    *,
    item_id: str,
    name: str = "",
    image_format: str = "jpg",
    image_type: str = "Primary",
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Store Jellyfin item artwork as a blob + ``:MediaAsset`` node. Never raises.

    Returns ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None``
    when there is no engine, no bytes, or the store failed. ``ingest`` may be
    injected (tests); otherwise the process-owned service is resolved on demand.

    ``digest`` is computed client-side (SHA-256 of ``data``) for the caller's
    immediate use; it matches the asset id the engine derives when no explicit id
    is set.
    """
    if not data:
        return None

    mime = _MIME_BY_EXT.get(str(image_format).lower().lstrip("."), "image/jpeg")
    extra = {
        "jellyfin_item_id": str(item_id),
        "image_type": image_type,
        "source_uri": f"jellyfin://item/{item_id}/images/{image_type}",
    }
    digest = hashlib.sha256(data).hexdigest()

    asset = MediaAsset(
        data=data,
        mime_type=mime,
        name=name or f"{item_id}-{image_type}",
        properties=extra,
    )
    change_set = ChangeSet(media=(asset,))
    try:
        service = ingest if ingest is not None else current_ingest()
        await service.submit(_BINDING, change_set)
    except (IngestError, IngestUnavailableError) as exc:
        logger.debug("KG media ingest unavailable/failed: %s", exc)
        return None

    logger.info(
        "KG media ingest: stored %s poster (%d bytes) digest=%s",
        item_id,
        len(data),
        digest,
    )
    return {
        "asset_id": f"blob:{digest}",
        "digest": digest,
        "size_bytes": len(data),
        "media_type": "image",
    }
