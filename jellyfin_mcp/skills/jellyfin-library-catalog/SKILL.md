---
name: jellyfin-library-catalog
description: >-
  Browse and search a Jellyfin media library via the jellyfin-mcp MCP server —
  list library items (movies, series, episodes, audio, books), fetch one item by
  id, walk collections and user views, and run search hints with the
  domain-typed `jellyfin_library` tool. Use when the agent must find or enumerate
  catalog items, resolve an item id, inspect a collection, or query library
  structure. Do NOT use for playback/streaming or artists/playlists (use
  `jellyfin-media-playback`), for server administration, users, or backups (use
  the `jellyfin_system` tool), or for pushing the catalog into the knowledge
  graph (use `jellyfin-kg-ingestion`).
license: MIT
tags: [jellyfin, media, library, catalog, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---

# Jellyfin Library Catalog

Domain-typed browse/search over a **Jellyfin** library through the
`jellyfin_library` condensed tool. Prefer it over raw HTTP — it action-routes
directly to the library client methods and returns Jellyfin item-shaped records.

## When to use
- List / filter library items (`get_items`) by type, parent folder, genre, year.
- Fetch a single item by id (`get_item`) or resume list (`get_resume_items`).
- Inspect collections (`get_collections`) and user views (`get_user_views`).
- Resolve a title to an item id via search hints (`get_search_hints`).

## When NOT to use
- Streaming, playback control, artists, playlists → `jellyfin-media-playback`.
- Users, API keys, backups, server config → the `jellyfin_system` tool.
- Ingesting the catalog into the KG → `jellyfin-kg-ingestion`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`jellyfin-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `JELLYFIN_URL` | ✅ | Base server URL (e.g. `https://jelly.host`) |
| `JELLYFIN_API_KEY` / `JELLYFIN_TOKEN` | ✅ | `X-Emby-Token` API key |
| `JELLYFIN_USER_ID` | optional | Default `user_id` for user-scoped reads |
| `JELLYFIN_VERIFY_SSL` | optional | TLS verification toggle |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface used
below vs. the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys map straight to the client method kwargs.

| Condensed tool | Actions |
|----------------|---------|
| `jellyfin_library` | `get_items`, `get_item`, `get_resume_items`, `get_collections`, `create_collection`, `add_to_collection`, `remove_from_collection`, `get_user_views`, `get_search_hints`, `get_latest_media`, `get_genres`, `get_studios`, `get_persons` |

### Key parameters
- `include_item_types` — e.g. `["Movie","Series","Audio","Book"]`.
- `parent_id` — scope to one library/folder; `recursive: true` to walk children.
- `user_id` — user-scoped reads (playstate, favorites); defaults to env.
- `search_term` / `fields` / `limit` / `start_index` — filtering + pagination.
- `item_id` — required for `get_item`.

## Recipes (`params_json`)
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
- `params_json` is a **string** of JSON, not an object — serialize it.
- `get_items` is unbounded without `recursive`/`parent_id`; always set `limit`
  and prefer `fields` to keep payloads small.
- Item ids are opaque GUIDs; resolve titles with `get_search_hints` first.
- `include_item_types` values are Jellyfin type names (`Audio`, not `Music`).

## Related
- `jellyfin-media-playback` — streaming, artists, playlists, playstate.
- `jellyfin-kg-ingestion` — push these items into the knowledge graph.
