"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_items`` / ``ingest_artists`` seam with
a fake engine client (no engine required), asserting the single-transaction node/edge staging and commit
and the Jellyfin item -> :MediaItem/:Book/:Genre/:Artist mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from jellyfin_mcp.kg_ingest import (
    ingest_artists,
    ingest_documents,
    ingest_entities,
    ingest_items,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, source, target, props):
        self.edges.append((source, target, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "MediaItem", "name": "m"},
            {"id": "g", "node_type": "Genre", "name": "Drama"},
        ],
        [{"source": "a", "target": "g", "relationship": "hasGenre"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "g"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "jellyfin-mcp"
    assert c.txn.nodes["a"]["domain"] == "media"
    assert c.txn.edges == [("a", "g", {"relationship": "hasGenre"})]


def test_ingest_items_maps_movie_genre_and_documents():
    c = _FakeClient()
    res = ingest_items(
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
        client=c,
    )
    assert res is not None
    node = c.txn.nodes["media:MediaItem:abc"]
    assert node["node_type"] == "MediaItem"
    assert node["itemKind"] == "Movie"
    assert node["externalToolId"] == "abc"
    assert node["productionYear"] == 1982
    # genre nodes + hasGenre edges
    assert "media:Genre:science-fiction" in c.txn.nodes
    assert (
        "media:MediaItem:abc",
        "media:Genre:drama",
        {"relationship": "hasGenre"},
    ) in c.txn.edges
    # overview became a :Document
    assert res["documents"] == 1
    assert c.txn.nodes["media:Document:abc"]["node_type"] == "Document"


def test_ingest_items_maps_audio_artist_and_book_author():
    c = _FakeClient()
    ingest_items(
        [
            {"Id": "s1", "Type": "Audio", "Name": "Song", "Artists": ["Miles Davis"]},
            {"Id": "b1", "Type": "Book", "Name": "Dune", "Artists": ["Frank Herbert"]},
        ],
        client=c,
        with_documents=False,
    )
    assert c.txn.nodes["media:Book:b1"]["node_type"] == "Book"
    assert "media:Artist:miles-davis" in c.txn.nodes
    assert "media:Author:frank-herbert" in c.txn.nodes
    assert (
        "media:MediaItem:s1",
        "media:Artist:miles-davis",
        {"relationship": "performedBy"},
    ) in c.txn.edges
    assert (
        "media:Book:b1",
        "media:Author:frank-herbert",
        {"relationship": "authoredBy"},
    ) in c.txn.edges


def test_ingest_artists_maps_artist_nodes():
    c = _FakeClient()
    res = ingest_artists({"Items": [{"Id": "art1", "Name": "Radiohead"}]}, client=c)
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["media:Artist:art1"]["node_type"] == "Artist"
    assert c.txn.nodes["media:Artist:art1"]["name"] == "Radiohead"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "media:Document:x", "text": "hello", "title": "X"}], client=c
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["media:Document:x"]["node_type"] == "Document"


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "MediaItem"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
