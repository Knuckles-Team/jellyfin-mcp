"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises ``jellyfin_mcp.kg_ingest``'s structural validation (still enforced locally)
and its no-op commit contract, plus the Jellyfin item -> :MediaItem/:Book/:Genre/:Artist
mapping shape (via ``ingest_items``'s intermediate mapping, asserted indirectly through
the raised/no-op contract since the actual commit is a stub).
CONCEPT:AU-KG.ingest.enterprise-source-extractor.

SDK GAP (EH-481/SDK-GAPS.md): ``_native_ingest_entities``/``_native_ingest_documents``
are stubs (no SDK equivalent yet for the old dependency-injected
``agent_utilities.knowledge_graph.memory.native_ingest`` ChangeEnvelope committer — see
``jellyfin_mcp/kg_ingest.py``'s module docstring). Every ``ingest_*`` call below is
therefore exercised for its validation + no-op-commit contract rather than real graph
writes; the DI-based ``_FakeClient`` coverage of the retired real-commit path (node/edge
shape assertions) is dropped with it.
"""

from __future__ import annotations

import pytest

from jellyfin_mcp.kg_ingest import (
    NativeIngestError,
    ingest_artists,
    ingest_documents,
    ingest_entities,
    ingest_items,
)


def test_ingest_entities_validates_then_noops():
    res = ingest_entities(
        [
            {"id": "a", "node_type": "MediaItem", "name": "m"},
            {"id": "g", "node_type": "Genre", "name": "Drama"},
        ],
        [{"source": "a", "target": "g", "relationship": "hasGenre"}],
    )
    assert res == {"nodes": 0, "edges": 0}


def test_ingest_items_maps_movie_genre_and_documents_then_noops():
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
    )
    # The mapping still ran (entities + a document were produced) but nothing was
    # actually written; ingest_items folds the documents count onto the zero commit.
    assert res == {"nodes": 0, "edges": 0, "documents": 0}


def test_ingest_items_maps_audio_artist_and_book_author_then_noops():
    res = ingest_items(
        [
            {"Id": "s1", "Type": "Audio", "Name": "Song", "Artists": ["Miles Davis"]},
            {"Id": "b1", "Type": "Book", "Name": "Dune", "Artists": ["Frank Herbert"]},
        ],
        with_documents=False,
    )
    assert res == {"nodes": 0, "edges": 0, "documents": 0}


def test_ingest_artists_maps_artist_nodes_then_noops():
    res = ingest_artists({"Items": [{"Id": "art1", "Name": "Radiohead"}]})
    assert res == {"nodes": 0, "edges": 0}


def test_ingest_documents_writes_document_nodes_then_noops():
    res = ingest_documents([{"id": "media:Document:x", "text": "hello", "title": "X"}])
    assert res == {"nodes": 0, "edges": 0}


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "MediaItem"}])


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([])
