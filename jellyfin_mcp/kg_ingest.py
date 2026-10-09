"""Native epistemic-graph ingestion for Jellyfin media (typed graph nodes + docs).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The jellyfin-mcp connector pushes its
library into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:MediaItem``, ``:Book``, ``:Artist``, ``:Genre``) + links (``:hasGenre`` /
``:performedBy`` / ``:authoredBy``), and item overviews as searchable ``:Document`` nodes,
through ``agent_connector_sdk.ingest`` -- the generated ``SourceIngest`` client, not a
local ingestion helper. Node ids follow ``media:<class>:<externalId>`` and each
``node_type`` matches a class the package's ``jellyfin_mcp.ontology`` ``.ttl`` federates.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Document,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

logger = logging.getLogger("jellyfin_mcp.kg")

_BINDING = IngestBinding(connector="jellyfin-mcp", stream="media")
# Jellyfin item Type values that are book/audiobook items -> :Book (else :MediaItem).
_BOOK_KINDS = {"Book", "AudioBook"}

_ENTITY_RESERVED_KEYS = frozenset({"id", "node_type"})
_RELATIONSHIP_RESERVED_KEYS = frozenset({"source", "target", "relationship"})


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={
            key: value
            for key, value in record.items()
            if key not in _ENTITY_RESERVED_KEYS
        },
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    properties = {
        key: value
        for key, value in record.items()
        if key not in _RELATIONSHIP_RESERVED_KEYS
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=properties or None,
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write typed OWL nodes (+ edges) into epistemic-graph via the SDK ingest facade.

    Nodes use ``node_type`` and relationships use ``relationship``.
    """
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(entity) for entity in entities),
        relationships=tuple(
            _to_relationship(relationship) for relationship in relationships or ()
        ),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write text records as ``:Document`` nodes (semantic-search fodder)."""
    if not documents:
        raise IngestError("ingest_documents needs at least one document")
    change_set = ChangeSet(
        documents=tuple(
            Document(
                id=doc["id"],
                text=doc["text"],
                title=doc.get("title"),
                source_uri=doc.get("source_uri"),
            )
            for doc in documents
        ),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


# --------------------------------------------------------------------------- #
# Record -> entity mappers (Jellyfin item / artist shapes)
# --------------------------------------------------------------------------- #
def _norm(name: str) -> str:
    """Stable slug for name-keyed nodes (genres, artists)."""
    return name.strip().lower().replace(" ", "-")


def _map_item(
    item: dict[str, Any],
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    seen: set[str],
    docs: list[dict[str, Any]],
) -> None:
    """Map ONE Jellyfin item dict onto entity/relationship/doc lists."""
    iid = item.get("Id") or item.get("id")
    if not iid:
        return
    kind = item.get("Type") or item.get("type") or "MediaItem"
    cls = "Book" if kind in _BOOK_KINDS else "MediaItem"
    node_id = f"media:{cls}:{iid}"
    entities.append(
        {
            "id": node_id,
            "node_type": cls,
            "name": item.get("Name") or item.get("name"),
            "itemKind": kind,
            "overview": item.get("Overview"),
            "productionYear": item.get("ProductionYear"),
            "communityRating": item.get("CommunityRating"),
            "officialRating": item.get("OfficialRating"),
            "runTimeTicks": item.get("RunTimeTicks"),
            "album": item.get("Album"),
            "seriesName": item.get("SeriesName"),
            "externalToolId": str(iid),
        }
    )

    overview = item.get("Overview")
    if overview:
        docs.append(
            {
                "id": f"media:Document:{iid}",
                "title": item.get("Name") or item.get("name"),
                "text": overview,
                "source_uri": f"jellyfin://item/{iid}",
                "itemKind": kind,
            }
        )

    # Genres -> :Genre + :hasGenre
    for genre in item.get("Genres") or []:
        if not genre:
            continue
        gid = f"media:Genre:{_norm(str(genre))}"
        if gid not in seen:
            entities.append({"id": gid, "node_type": "Genre", "name": str(genre)})
            seen.add(gid)
        relationships.append(
            {"source": node_id, "target": gid, "relationship": "hasGenre"}
        )

    # Artists (audio) / authors (books) -> :Artist|:Author + link
    for artist in item.get("Artists") or []:
        if not artist:
            continue
        if cls == "Book":
            aid = f"media:Author:{_norm(str(artist))}"
            atype, link = "Author", "authoredBy"
        else:
            aid = f"media:Artist:{_norm(str(artist))}"
            atype, link = "Artist", "performedBy"
        if aid not in seen:
            entities.append({"id": aid, "node_type": atype, "name": str(artist)})
            seen.add(aid)
        relationships.append({"source": node_id, "target": aid, "relationship": link})


async def ingest_items(
    items: list[dict[str, Any]] | dict[str, Any],
    *,
    ingest: KnowledgeIngest | None = None,
    with_documents: bool = True,
) -> dict[str, int] | None:
    """Map Jellyfin library items -> ``:MediaItem``/``:Book`` (+ genre/artist) nodes.

    Accepts either a raw list of item dicts or the Jellyfin ``{"Items": [...]}`` envelope.
    Returns ``{"nodes":n, "edges":m, "documents":d}`` or ``None``.
    """
    if isinstance(items, dict):
        items = items.get("Items") or items.get("items") or []
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    docs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items or []:
        if isinstance(item, dict):
            _map_item(item, entities, relationships, seen, docs)
    if not entities:
        return None
    result = await ingest_entities(entities, relationships, ingest=ingest)
    if with_documents and docs:
        doc_res = await ingest_documents(docs, ingest=ingest)
        result["documents"] = doc_res.get("nodes", 0)
    else:
        result["documents"] = 0
    return result


async def ingest_artists(
    artists: list[dict[str, Any]] | dict[str, Any],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int] | None:
    """Map Jellyfin artist items -> ``:Artist`` nodes."""
    if isinstance(artists, dict):
        artists = artists.get("Items") or artists.get("items") or []
    entities: list[dict[str, Any]] = []
    for artist in artists or []:
        if not isinstance(artist, dict):
            continue
        aid = artist.get("Id") or artist.get("id")
        if not aid:
            continue
        entities.append(
            {
                "id": f"media:Artist:{aid}",
                "node_type": "Artist",
                "name": artist.get("Name") or artist.get("name"),
                "overview": artist.get("Overview"),
                "externalToolId": str(aid),
            }
        )
    if not entities:
        return None
    return await ingest_entities(entities, None, ingest=ingest)
