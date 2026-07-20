# Jellyfin Kg Ingestion

Natively ingest a Jellyfin library into the epistemic-graph knowledge graph via the jellyfin-mcp MCP server — push library items as typed :MediaItem/:Book nodes with :hasGenre/:performedBy/:authoredBy links and item overviews as searchable :Document nodes (`jellyfin_ingest_library`), and item posters as content-addressed :Blob assets (`jellyfin_ingest_posters`). Use when the agent must make a Jellyfin catalog queryable in the KG or refresh its media nodes. Do NOT use for interactive browse/search (use `jellyfin-library-catalog`) or playback/streaming (use `jellyfin-media-playback`); this skill is the ingestion seam, not the operational surface.

# Jellyfin Knowledge-Graph Ingestion

Native "maximum ingestion" of a **Jellyfin** library into the ONE epistemic-graph
knowledge graph. Library items become typed OWL nodes; overviews become
semantic-search documents; posters become deduped blobs — all best-effort and
engine-guarded (no engine reachable ⇒ clean no-op).

## When to use
- Make a Jellyfin catalog queryable in the KG (`jellyfin_ingest_library`).
- Refresh media nodes after library changes (re-run; ids are stable).
- Persist item artwork as durable blobs (`jellyfin_ingest_posters`).

## When NOT to use
- Interactive catalog browse/search → `jellyfin-library-catalog`.
- Streaming / playback control → `jellyfin-media-playback`.
- Server administration → the `jellyfin_system` tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`jellyfin-mcp`** MCP server.
Ingestion additionally requires a reachable epistemic-graph engine (an
`agent_utilities` KG stack); with none present the tools return
`{"ingested": null}` and do nothing else.

| Variable | Required | Notes |
|----------|----------|-------|
| `JELLYFIN_URL` | ✅ | Base server URL |
| `JELLYFIN_API_KEY` / `JELLYFIN_TOKEN` | ✅ | `X-Emby-Token` API key |
| `JELLYFIN_USER_ID` | optional | Default `user_id` for item reads |

## Tools & actions
| Tool | Purpose |
|------|---------|
| `jellyfin_ingest_library` | List items (`get_items` filters via `params_json`) → typed nodes + documents |
| `jellyfin_ingest_posters` | For given `item_ids`, fetch the primary image → `:Blob` + `:AssetOccurrence` |

### KG mapping
- Item → `media:MediaItem:<Id>` (`:Book` when the item Type is a book/audiobook),
  carrying `itemKind`, `overview`, `productionYear`, `communityRating`, …
- `Genres[]` → `media:Genre:<slug>` + `:hasGenre` edge.
- `Artists[]` → `media:Artist:<slug>` + `:performedBy` (or `:Author` + `:authoredBy`
  for books).
- Item `Overview` → `media:Document:<Id>` (`:Document`, embedded hub-side).
- Node ids follow `media:<class>:<externalId>`; provenance `source=jellyfin-mcp`,
  `domain=media`.

## Recipes
Ingest all movies + series (bounded, recursive):
```json
{"include_item_types":["Movie","Series"],"recursive":true,"limit":500,"fields":["Overview","Genres","ProductionYear","CommunityRating"]}
```
Then ingest posters for a handful of ids (tool args, not `params_json`):
```json
{"item_ids":["<id1>","<id2>"],"image_type":"Primary"}
```

## Gotchas
- Ingestion is **best-effort**: no engine ⇒ `ingested: null`, never an error.
- Always pass `fields` including `Overview`/`Genres` — items fetched without them
  produce nodes with no documents or genre links.
- Re-running is idempotent on node id (`media:<class>:<Id>`); it MERGEs, not
  duplicates.
- `jellyfin_ingest_posters` depends on the server returning image bytes; large
  batches are slow — pass a small `item_ids` list.

## Related
- `jellyfin-library-catalog` — find the item ids / filters to feed ingestion.
- Backed by `jellyfin_mcp.kg_ingest` (typed nodes + documents) and
  `jellyfin_mcp.kg_media` (poster blobs) over the shared `native_ingest` primitive.
