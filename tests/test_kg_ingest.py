"""Epistemic-graph typed-node ingestion via agent_connector_sdk — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_items`` / ``ingest_artists`` /
``ingest_documents`` seam against a fake transport one level below the SDK's own
``KnowledgeIngest`` facade, so these tests still run the SDK's real request-building
contract. Asserts the Jellyfin item -> :MediaItem/:Book/:Genre/:Artist mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from jellyfin_mcp.kg_ingest import (
    ingest_artists,
    ingest_documents,
    ingest_entities,
    ingest_items,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector, stream):
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request):
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data):
        raise AssertionError("jellyfin-mcp structural ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


def _node_type(record: Any) -> str:
    """A real generated ``SourceRecord`` has no bare ``node_type`` field — it's the
    last segment of ``mapping_reference``
    (``manifest:<connector>#schema_mappings/<NodeType>``)."""
    return record.mapping_reference.rsplit("/", 1)[-1]


def _rel_name(relationship: Any) -> str:
    """Likewise, a ``SourceRelationship``'s kind is the last segment of
    ``relation_reference`` (``manifest:<connector>#resources/<NodeType>/relations/<kind>``)."""
    return relationship.relation_reference.rsplit("/", 1)[-1]


async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "MediaItem", "name": "m"},
            {"id": "g", "node_type": "Genre", "name": "Drama"},
        ],
        [{"source": "a", "target": "g", "relationship": "hasGenre"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    records = {r.record_id: r for r in transport.requests[0].records}
    assert set(records) == {"a", "g"}
    rel = transport.requests[0].relationships[0]
    assert (rel.source.record_id, rel.target.record_id, _rel_name(rel)) == (
        "a",
        "g",
        "hasGenre",
    )


async def test_ingest_items_maps_movie_genre_and_documents(ingest):
    service, transport = ingest
    res = await ingest_items(
        {
            "Items": [
                {
                    "Id": "abc",
                    "Type": "Movie",
                    "Name": "Blade Runner",
                    "Overview": "A blade runner hunts replicants.",
                    "ProductionYear": 1982,
                    "Genres": ["Science Fiction", "Drama"],
                }
            ]
        },
        ingest=service,
    )
    assert res is not None
    records = {r.record_id: r for r in transport.requests[0].records}
    node = records["media:MediaItem:abc"]
    assert _node_type(node) == "MediaItem"
    assert node.payload["itemKind"] == "Movie"
    assert node.payload["externalToolId"] == "abc"
    assert node.payload["productionYear"] == 1982
    # genre nodes + hasGenre edges
    assert "media:Genre:science-fiction" in records
    rels = {
        (r.source.record_id, r.target.record_id, _rel_name(r))
        for r in transport.requests[0].relationships
    }
    assert ("media:MediaItem:abc", "media:Genre:drama", "hasGenre") in rels
    # overview became a :Document (second submit call — documents go through
    # ingest_documents, a separate request)
    assert res["documents"] == 1
    doc_records = {r.record_id: r for r in transport.requests[1].records}
    assert _node_type(doc_records["media:Document:abc"]) == "Document"


async def test_ingest_items_maps_audio_artist_and_book_author(ingest):
    service, transport = ingest
    await ingest_items(
        [
            {"Id": "s1", "Type": "Audio", "Name": "Song", "Artists": ["Miles Davis"]},
            {"Id": "b1", "Type": "Book", "Name": "Dune", "Artists": ["Frank Herbert"]},
        ],
        ingest=service,
        with_documents=False,
    )
    records = {r.record_id: r for r in transport.requests[0].records}
    assert _node_type(records["media:Book:b1"]) == "Book"
    assert "media:Artist:miles-davis" in records
    assert "media:Author:frank-herbert" in records
    rels = {
        (r.source.record_id, r.target.record_id, _rel_name(r))
        for r in transport.requests[0].relationships
    }
    assert ("media:MediaItem:s1", "media:Artist:miles-davis", "performedBy") in rels
    assert ("media:Book:b1", "media:Author:frank-herbert", "authoredBy") in rels


async def test_ingest_artists_maps_artist_nodes(ingest):
    service, transport = ingest
    res = await ingest_artists(
        {"Items": [{"Id": "art1", "Name": "Radiohead"}]}, ingest=service
    )
    assert res == {"nodes": 1, "edges": 0}
    records = {r.record_id: r for r in transport.requests[0].records}
    assert _node_type(records["media:Artist:art1"]) == "Artist"
    assert records["media:Artist:art1"].payload["name"] == "Radiohead"


async def test_ingest_documents_writes_document_nodes(ingest):
    service, transport = ingest
    res = await ingest_documents(
        [{"id": "media:Document:x", "text": "hello", "title": "X"}], ingest=service
    )
    assert res == {"nodes": 1, "edges": 0}
    records = {r.record_id: r for r in transport.requests[0].records}
    assert _node_type(records["media:Document:x"]) == "Document"


async def test_retired_structural_alias_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError):
        await ingest_entities([{"id": "a", "type": "MediaItem"}], ingest=service)


async def test_empty_native_ingest_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)


async def test_ingest_items_empty_is_a_noop(ingest):
    service, transport = ingest
    assert await ingest_items([], ingest=service) is None
    assert await ingest_artists([], ingest=service) is None
    assert transport.requests == []
