"""Native epistemic-graph ingestion for Jellyfin media (typed graph nodes + docs).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The jellyfin-mcp connector natively
pushes its library into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:MediaAsset``, ``:Book``, ``:Artist``, ``:Genre``) + links (``:hasGenre`` /
``:performedBy`` / ``:authoredBy``), and item overviews as searchable ``:Document`` nodes.

This is a thin mapper: the txn write path lives once in the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``. When that primitive is present it
is used directly; otherwise a self-contained, engine-guarded txn fallback runs (the shared
module is not yet in every installed agent_utilities). Everything is best-effort — with no
KG stack or no reachable engine every entry point **no-ops** (returns ``None``), so the
connector runs with zero KG infrastructure. Node ids follow ``media:<class>:<externalId>``
and each ``type`` matches a class the package's ``jellyfin_mcp.ontology`` ``.ttl`` federates.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("jellyfin_mcp.kg")

_SOURCE = "jellyfin-mcp"
_DOMAIN = "media"
_DEFAULT_GRAPH = "__commons__"

# Jellyfin item Type values that are book/audiobook items -> :Book (else :MediaAsset).
_BOOK_KINDS = {"Book", "AudioBook"}


# --------------------------------------------------------------------------- #
# Shared-primitive-first, guarded fallback write path
# --------------------------------------------------------------------------- #
def _shared():
    """Return the shared native_ingest module, or ``None`` when absent."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest
    except Exception as e:  # noqa: BLE001 — shared primitive not installed yet
        logger.debug("shared native_ingest unavailable: %s", e)
        return None


def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    shared = _shared()
    if shared is not None:
        return shared.native_client()
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None

    shared = _shared()
    if shared is not None:
        return shared.ingest_entities(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )

    # Self-contained fallback txn path (mirrors the shared primitive).
    if client is None:
        client, graph = _client()
    if client is None:
        return None
    graph = graph or _DEFAULT_GRAPH
    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder)."""
    documents = [d for d in (documents or []) if d.get("id") and d.get("text")]
    if not documents:
        return None

    shared = _shared()
    if shared is not None:
        return shared.ingest_documents(
            documents, source=source, domain=domain, client=client, graph=graph
        )

    # Fallback: :Document nodes are just typed nodes carrying ``text``.
    nodes = [{**d, "type": "Document"} for d in documents]
    return ingest_entities(
        nodes, None, source=source, domain=domain, client=client, graph=graph
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
    kind = item.get("Type") or item.get("type") or "MediaAsset"
    cls = "Book" if kind in _BOOK_KINDS else "MediaAsset"
    node_id = f"media:{cls}:{iid}"
    entities.append(
        {
            "id": node_id,
            "type": cls,
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
            entities.append({"id": gid, "type": "Genre", "name": str(genre)})
            seen.add(gid)
        relationships.append({"source": node_id, "target": gid, "type": "hasGenre"})

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
            entities.append({"id": aid, "type": atype, "name": str(artist)})
            seen.add(aid)
        relationships.append({"source": node_id, "target": aid, "type": link})


def ingest_items(
    items: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
    with_documents: bool = True,
) -> dict[str, int] | None:
    """Map Jellyfin library items -> ``:MediaAsset``/``:Book`` (+ genre/artist) nodes.

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
    artists: list[dict[str, Any]],
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
                "type": "Artist",
                "name": artist.get("Name") or artist.get("name"),
                "overview": artist.get("Overview"),
                "externalToolId": str(aid),
            }
        )
    return ingest_entities(entities, None, client=client, graph=graph)
