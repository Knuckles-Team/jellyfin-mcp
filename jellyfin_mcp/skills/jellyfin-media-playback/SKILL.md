---
name: jellyfin-media-playback
description: >-
  Stream and control Jellyfin playback and browse music via the jellyfin-mcp MCP
  server — list artists, albums, and music genres, resolve audio/video streams,
  manage playlists, and drive playstate (play, mark played, report progress) with
  the domain-typed `jellyfin_media` tool. Use when the agent must start or control
  playback, enumerate artists/playlists, build an instant mix, or fetch stream
  URLs. Do NOT use for browsing/searching the catalog or collections (use
  `jellyfin-library-catalog`), server administration (use the `jellyfin_system`
  tool), or KG ingestion (use `jellyfin-kg-ingestion`).
license: MIT
tags: [jellyfin, media, playback, streaming, music, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---

# Jellyfin Media Playback

Domain-typed streaming, music browsing, and playback control through the
`jellyfin_media` condensed tool. Prefer it over raw HTTP — it action-routes to the
media client methods (artists, streams, playlists, playstate).

## When to use
- List artists / album artists (`get_artists`, `get_album_artists`) and music
  genres (`get_music_genres`).
- Manage playlists (`create_playlist`, `add_item_to_playlist`,
  `get_playlist_items`) and build instant mixes (`get_instant_mix_from_song`).
- Resolve streams (`get_audio_stream`, `get_video_stream`,
  `get_universal_audio_stream`) and playback info (`get_playback_info`).
- Drive playstate (`play`, `mark_played_item`, `report_playback_progress`).

## When NOT to use
- Browsing/searching items, collections, user views → `jellyfin-library-catalog`.
- Users, keys, backups, config → the `jellyfin_system` tool.
- Ingesting artists/media into the KG → `jellyfin-kg-ingestion`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`jellyfin-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `JELLYFIN_URL` | ✅ | Base server URL |
| `JELLYFIN_API_KEY` / `JELLYFIN_TOKEN` | ✅ | `X-Emby-Token` API key |
| `JELLYFIN_USER_ID` | optional | Default `user_id` for playstate/favorites |
| `JELLYFIN_VERIFY_SSL` | optional | TLS verification toggle |

`MCP_TOOL_MODE` selects the condensed surface below vs. the verbose 1:1 tools.

## Tools & actions
Prefer the **condensed** tool with `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `jellyfin_media` | `get_artists`, `get_album_artists`, `get_artist_by_name`, `get_music_genres`, `create_playlist`, `add_item_to_playlist`, `get_playlist_items`, `get_instant_mix_from_song`, `get_audio_stream`, `get_video_stream`, `get_universal_audio_stream`, `get_playback_info`, `play`, `mark_played_item`, `report_playback_progress`, `get_lyrics` |

### Key parameters
- `item_id` — required for stream/playstate/lyrics/instant-mix actions.
- `user_id` — required for playstate + favorites (defaults to env).
- `body` — object payload for `create_playlist` / `report_playback_*`.
- `search_term` / `limit` / `start_index` — filter + paginate artist lists.

## Recipes (`params_json`)
List the first 50 artists:
```json
{"limit":50,"start_index":0}
```
Create a playlist and add a track:
```json
{"body":{"Name":"Focus","Ids":["<itemId>"],"MediaType":"Audio","UserId":"<userId>"}}
```
Mark an item played for a user:
```json
{"item_id":"<itemId>","user_id":"<userId>"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- Stream actions return a URL/handle, not raw bytes — hand the URL to a player.
- Playstate + favorite actions require a `user_id`; a server API key alone is not
  a user context.
- Playlist creation takes a `body` object (`Name`, `Ids`, `MediaType`), not flat
  kwargs.

## Related
- `jellyfin-library-catalog` — find item ids to stream / add to playlists.
- `jellyfin-kg-ingestion` — persist artists + media into the knowledge graph.
