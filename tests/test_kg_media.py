"""Native epistemic-graph blob ingestion — Wire-First coverage.

Exercises the real ``ingest_image_bytes`` seam with a fake ``MediaStore`` (no engine
required), asserting the poster bytes + metadata reach ``store_media``.
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from dataclasses import dataclass

from jellyfin_mcp.kg_media import ingest_image_bytes


@dataclass
class _Stored:
    asset_id: str
    digest: str


class _FakeMediaStore:
    def __init__(self):
        self.calls = []

    def store_media(self, data, **kw):
        self.calls.append((data, kw))
        return _Stored(asset_id="media:cafebabe", digest="cafebabe")


def test_ingest_image_bytes_stores_bytes_and_metadata():
    store = _FakeMediaStore()
    res = ingest_image_bytes(
        b"\x89PNG\r\n\x1a\nfake",
        item_id="item-1",
        name="Poster",
        image_format="png",
        image_type="Primary",
        store=store,
    )
    assert res is not None
    assert res["asset_id"] == "media:cafebabe"
    assert res["media_type"] == "image"
    assert res["size_bytes"] == len(b"\x89PNG\r\n\x1a\nfake")

    assert len(store.calls) == 1
    data, kw = store.calls[0]
    assert data == b"\x89PNG\r\n\x1a\nfake"
    assert kw["source"] == "jellyfin-mcp"
    assert kw["media_type"] == "image"
    assert kw["mime_type"] == "image/png"
    assert kw["name"] == "Poster"
    assert kw["extra"]["jellyfin_item_id"] == "item-1"
    assert kw["extra"]["image_type"] == "Primary"


def test_ingest_image_bytes_defaults_mime_and_name():
    store = _FakeMediaStore()
    ingest_image_bytes(b"bytes", item_id="i2", store=store)
    _, kw = store.calls[0]
    assert kw["mime_type"] == "image/jpeg"  # default
    assert kw["name"] == "i2-Primary"


def test_ingest_image_bytes_noops_without_engine():
    # No injected store + no reachable engine -> clean no-op (never raises).
    assert ingest_image_bytes(b"bytes", item_id="i3") is None


def test_ingest_image_bytes_noops_on_empty():
    assert ingest_image_bytes(b"", item_id="i4", store=_FakeMediaStore()) is None
    assert ingest_image_bytes(None, item_id="i5", store=_FakeMediaStore()) is None
