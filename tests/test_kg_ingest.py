"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_items`` / ``ingest_artists`` seam with
a fake engine client (no engine required), asserting the single-transaction node/edge staging and commit
and the Jellyfin item -> :MediaItem/:Book/:Genre/:Artist mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.models.company_brain import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session

from jellyfin_mcp.kg_ingest import (
    ingest_artists,
    ingest_documents,
    ingest_entities,
    ingest_items,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "MediaItem", "name": "m"},
            {"id": "g", "node_type": "Genre", "name": "Drama"},
        ],
        [{"source": "a", "target": "g", "relationship": "hasGenre"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "g"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "jellyfin-mcp"
    assert c.nodes.values["a"]["domain"] == "media"
    assert c.changes.edges == [("a", "g", {"relationship": "hasGenre"})]


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
    node = c.nodes.values["media:MediaItem:abc"]
    assert node["node_type"] == "MediaItem"
    assert node["itemKind"] == "Movie"
    assert node["externalToolId"] == "abc"
    assert node["productionYear"] == 1982
    # genre nodes + hasGenre edges
    assert "media:Genre:science-fiction" in c.nodes.values
    assert (
        "media:MediaItem:abc",
        "media:Genre:drama",
        {"relationship": "hasGenre"},
    ) in c.changes.edges
    # overview became a :Document
    assert res["documents"] == 1
    assert c.nodes.values["media:Document:abc"]["node_type"] == "Document"


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
    assert c.nodes.values["media:Book:b1"]["node_type"] == "Book"
    assert "media:Artist:miles-davis" in c.nodes.values
    assert "media:Author:frank-herbert" in c.nodes.values
    assert (
        "media:MediaItem:s1",
        "media:Artist:miles-davis",
        {"relationship": "performedBy"},
    ) in c.changes.edges
    assert (
        "media:Book:b1",
        "media:Author:frank-herbert",
        {"relationship": "authoredBy"},
    ) in c.changes.edges


def test_ingest_artists_maps_artist_nodes():
    c = _FakeClient()
    res = ingest_artists({"Items": [{"Id": "art1", "Name": "Radiohead"}]}, client=c)
    assert res == {"nodes": 1, "edges": 0}
    assert c.nodes.values["media:Artist:art1"]["node_type"] == "Artist"
    assert c.nodes.values["media:Artist:art1"]["name"] == "Radiohead"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "media:Document:x", "text": "hello", "title": "X"}], client=c
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.nodes.values["media:Document:x"]["node_type"] == "Document"


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "MediaItem"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
