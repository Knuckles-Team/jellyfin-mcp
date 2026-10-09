"""Native epistemic-graph blob ingestion — Wire-First coverage.

Exercises the real ``ingest_image_bytes`` seam with a fake ``KnowledgeIngest``
transport (no engine required), asserting the poster bytes + metadata reach the
SDK's own request builder. CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from jellyfin_mcp.kg_media import ingest_image_bytes


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []
        self.stored: list[bytes] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        self.stored.append(data)
        return hashlib.sha256(data).hexdigest()


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_image_bytes_stores_bytes_and_metadata(ingest):
    service, transport = ingest
    data = b"\x89PNG\r\n\x1a\nfake"
    res = await ingest_image_bytes(
        data,
        item_id="item-1",
        name="Poster",
        image_format="png",
        image_type="Primary",
        ingest=service,
    )
    assert res is not None
    assert res["digest"] == hashlib.sha256(data).hexdigest()
    assert res["asset_id"] == f"blob:{res['digest']}"
    assert res["media_type"] == "image"
    assert res["size_bytes"] == len(data)
    assert transport.stored == [data]

    record = transport.requests[0].records[0]
    assert record.payload["mime_type"] == "image/png"
    assert record.payload["name"] == "Poster"
    assert record.payload["jellyfin_item_id"] == "item-1"
    assert record.payload["image_type"] == "Primary"


@pytest.mark.asyncio
async def test_ingest_image_bytes_defaults_mime_and_name(ingest):
    service, transport = ingest
    await ingest_image_bytes(b"bytes", item_id="i2", ingest=service)
    record = transport.requests[0].records[0]
    assert record.payload["mime_type"] == "image/jpeg"  # default
    assert record.payload["name"] == "i2-Primary"


@pytest.mark.asyncio
async def test_ingest_image_bytes_noops_on_empty(ingest):
    service, _transport = ingest
    assert await ingest_image_bytes(b"", item_id="i4", ingest=service) is None
    assert await ingest_image_bytes(None, item_id="i5", ingest=service) is None
