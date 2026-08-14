"""Native epistemic-graph ingestion for Jellyfin media (typed graph nodes + docs).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The jellyfin-mcp connector natively
pushes its library into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:MediaItem``, ``:Book``, ``:Artist``, ``:Genre``) + links (``:hasGenre`` /
``:performedBy`` / ``:authoredBy``), and item overviews as searchable ``:Document`` nodes.

This is a thin mapper: the transaction path lives once in the required
``agent_utilities.knowledge_graph.memory.native_ingest`` primitive. Engine failures are
explicit and partial writes are never acknowledged. Node ids follow
``media:<class>:<externalId>`` and each ``node_type`` matches a class the package's
``jellyfin_mcp.ontology`` ``.ttl`` federates.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("jellyfin_mcp.kg")

_SOURCE = "jellyfin-mcp"
_DOMAIN = "media"
# Jellyfin item Type values that are book/audiobook items -> :Book (else :MediaItem).
_BOOK_KINDS = {"Book", "AudioBook"}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    Nodes use ``node_type`` and relationships use ``relationship``.
    """
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write text records as ``:Document`` nodes (semantic-search fodder)."""
    return _native_ingest_documents(
        documents,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


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


def ingest_items(
    items: list[dict[str, Any]] | dict[str, Any],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    result = ingest_entities(entities, relationships, client=client, graph=graph)
    if result is None:
        return None
    if with_documents and docs:
        doc_res = ingest_documents(docs, client=client, graph=graph)
        result["documents"] = (doc_res or {}).get("nodes", 0)
    else:
        result["documents"] = 0
    return result


def ingest_artists(
    artists: list[dict[str, Any]] | dict[str, Any],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, None, client=client, graph=graph)
