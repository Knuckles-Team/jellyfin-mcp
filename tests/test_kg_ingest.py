"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_items`` / ``ingest_artists`` seam with
a fake engine client (no engine required), asserting the txn add_node/commit + edge calls
and the Jellyfin item -> :MediaAsset/:Book/:Genre/:Artist mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from jellyfin_mcp.kg_ingest import (
    ingest_artists,
    ingest_documents,
    ingest_entities,
    ingest_items,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "MediaAsset", "name": "m"},
            {"id": "g", "type": "Genre", "name": "Drama"},
        ],
        [{"source": "a", "target": "g", "type": "hasGenre"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "g"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "jellyfin-mcp"
    assert c.txn.nodes["a"]["domain"] == "media"
    assert c.edges.edges == [("a", "g", {"type": "hasGenre"})]


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
    node = c.txn.nodes["media:MediaAsset:abc"]
    assert node["type"] == "MediaAsset"
    assert node["itemKind"] == "Movie"
    assert node["externalToolId"] == "abc"
    assert node["productionYear"] == 1982
    # genre nodes + hasGenre edges
    assert "media:Genre:science-fiction" in c.txn.nodes
    assert (
        "media:MediaAsset:abc",
        "media:Genre:drama",
        {"type": "hasGenre"},
    ) in c.edges.edges
    # overview became a :Document
    assert res["documents"] == 1
    assert c.txn.nodes["media:Document:abc"]["type"] == "Document"


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
    assert c.txn.nodes["media:Book:b1"]["type"] == "Book"
    assert "media:Artist:miles-davis" in c.txn.nodes
    assert "media:Author:frank-herbert" in c.txn.nodes
    assert (
        "media:MediaAsset:s1",
        "media:Artist:miles-davis",
        {"type": "performedBy"},
    ) in c.edges.edges
    assert (
        "media:Book:b1",
        "media:Author:frank-herbert",
        {"type": "authoredBy"},
    ) in c.edges.edges


def test_ingest_artists_maps_artist_nodes():
    c = _FakeClient()
    res = ingest_artists({"Items": [{"Id": "art1", "Name": "Radiohead"}]}, client=c)
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["media:Artist:art1"]["type"] == "Artist"
    assert c.txn.nodes["media:Artist:art1"]["name"] == "Radiohead"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "media:Document:x", "text": "hello", "title": "X"}], client=c
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["media:Document:x"]["type"] == "Document"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "MediaAsset"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_items([], client=_FakeClient()) is None
    assert ingest_artists([], client=_FakeClient()) is None
