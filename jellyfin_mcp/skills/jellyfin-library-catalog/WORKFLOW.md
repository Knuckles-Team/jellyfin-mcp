# Jellyfin Library Catalog

Browse and search a Jellyfin media library via the jellyfin-mcp MCP server — list library items (movies, series, episodes, audio, books), fetch one item by id, walk collections and user views, and run search hints with the typed `jellyfin_*` tools. Use when the agent must find or enumerate catalog items, resolve an item id, inspect a collection, or query library structure. Do NOT use for playback/streaming or artists/playlists (use `jellyfin-media-playback`), for server administration, users, or backups (use the typed system/user/backup `jellyfin_*` tools), or for pushing the catalog into the knowledge graph (use `jellyfin-kg-ingestion`).

# Jellyfin Library Catalog

Domain-typed browse/search over a **Jellyfin** library through the
typed per-operation tools (`jellyfin_get_items`, `jellyfin_get_item`,
`jellyfin_get_search_hints`, ...). Prefer them over raw HTTP; they return Jellyfin item-shaped records.

## When to use
- List / filter library items (`get_items`) by type, parent folder, genre, year.
- Fetch a single item by id (`get_item`) or resume list (`get_resume_items`).
- Inspect collections (`jellyfin_get_items` with `include_item_types=["BoxSet"]`) and user views (`get_user_views`).
- Resolve a title to an item id via search hints (`get_search_hints`).

## When NOT to use
- Streaming, playback control, artists, playlists → `jellyfin-media-playback`.
- Users, API keys, backups, server config → the typed system/user/backup `jellyfin_*` tools.
- Ingesting the catalog into the KG → `jellyfin-kg-ingestion`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`jellyfin-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `JELLYFIN_URL` | ✅ | Base server URL (e.g. `[configured-endpoint]`) |
| `JELLYFIN_API_KEY` / `JELLYFIN_TOKEN` | ✅ | `X-Emby-Token` API key |
| `JELLYFIN_USER_ID` | optional | Default `user_id` for user-scoped reads |
| `JELLYFIN_TLS_PROFILE[_REF]` | optional | Runtime TLS profile for private PKI, mTLS, or proxy policy |

## Tools
Each operation is its own tool named `jellyfin_<operation>`; arguments are typed tool
parameters named after the Jellyfin query/body fields.

| Tools |
|-------|
| `jellyfin_get_items`, `jellyfin_get_item`, `jellyfin_get_resume_items`, `jellyfin_create_collection`, `jellyfin_add_to_collection`, `jellyfin_remove_from_collection`, `jellyfin_get_user_views`, `jellyfin_get_search_hints`, `jellyfin_get_latest_media`, `jellyfin_get_genres`, `jellyfin_get_studios`, `jellyfin_get_persons` |

### Key parameters
- `include_item_types` — e.g. `["Movie","Series","Audio","Book"]`.
- `parent_id` — scope to one library/folder; `recursive: true` to walk children.
- `user_id` — user-scoped reads (playstate, favorites); defaults to env.
- `search_term` / `fields` / `limit` / `start_index` — filtering + pagination.
- `item_id` — required for `get_item`.

## Recipes (tool arguments)
List the 25 most-recent movies with a few fields:
```json
{"include_item_types":["Movie"],"recursive":true,"sort_by":["DateCreated"],"sort_order":["Descending"],"limit":25,"fields":["Overview","Genres","ProductionYear"]}
```
Get one item by id:
```json
{"item_id":"<itemId>","user_id":"<userId>"}
```
Search hints for a title:
```json
{"search_term":"blade runner","limit":10}
```

## Gotchas
- `get_items` is unbounded without `recursive`/`parent_id`; always set `limit`
  and prefer `fields` to keep payloads small.
- Item ids are opaque GUIDs; resolve titles with `get_search_hints` first.
- `include_item_types` values are Jellyfin type names (`Audio`, not `Music`).

## Related
- `jellyfin-media-playback` — streaming, artists, playlists, playstate.
- `jellyfin-kg-ingestion` — push these items into the knowledge graph.
