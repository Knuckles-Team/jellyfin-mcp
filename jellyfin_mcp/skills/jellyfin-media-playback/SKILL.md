---
name: jellyfin-media-playback
skill_type: skill
description: >-
  Stream and control Jellyfin playback and browse music via the jellyfin-mcp MCP
  server — list artists, albums, and music genres, resolve audio/video streams,
  manage playlists, and drive playstate (play, mark played, report progress) with
  the typed `jellyfin_*` tools. Use when the agent must start or control
  playback, enumerate artists/playlists, build an instant mix, or fetch stream
  URLs. Do NOT use for browsing/searching the catalog or collections (use
  `jellyfin-library-catalog`), server administration (use the typed system tools), or KG ingestion (use `jellyfin-kg-ingestion`).
license: MIT
tags: [jellyfin, media, playback, streaming, music, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Jellyfin Media Playback

Domain-typed streaming, music browsing, and playback control through the
typed per-operation tools (`jellyfin_get_artists`, `jellyfin_create_playlist`,
`jellyfin_get_audio_stream`, ...). Prefer them over raw HTTP.

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
- Users, keys, backups, config → the typed system/user/backup `jellyfin_*` tools.
- Ingesting artists/media into the KG → `jellyfin-kg-ingestion`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`jellyfin-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `JELLYFIN_URL` | ✅ | Base server URL |
| `JELLYFIN_API_KEY` / `JELLYFIN_TOKEN` | ✅ | `X-Emby-Token` API key |
| `JELLYFIN_USER_ID` | optional | Default `user_id` for playstate/favorites |
| `JELLYFIN_VERIFY_SSL` | optional | TLS verification toggle |

## Tools
Each operation is its own tool named `jellyfin_<operation>`; arguments are typed tool
parameters named after the Jellyfin query/body fields.

| Tools |
|-------|
| `jellyfin_get_artists`, `jellyfin_get_album_artists`, `jellyfin_get_artist_by_name`, `jellyfin_get_music_genres`, `jellyfin_create_playlist`, `jellyfin_add_item_to_playlist`, `jellyfin_get_playlist_items`, `jellyfin_get_instant_mix_from_song`, `jellyfin_get_audio_stream`, `jellyfin_get_video_stream`, `jellyfin_get_universal_audio_stream`, `jellyfin_get_playback_info`, `jellyfin_play`, `jellyfin_mark_played_item`, `jellyfin_report_playback_progress`, `jellyfin_get_lyrics` |

### Key parameters
- `item_id` — required for stream/playstate/lyrics/instant-mix actions.
- `user_id` — required for playstate + favorites (defaults to env).
- `body` — object payload for `create_playlist` / `report_playback_*`.
- `search_term` / `limit` / `start_index` — filter + paginate artist lists.

## Recipes (tool arguments)
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
- Stream actions return a URL/handle, not raw bytes — hand the URL to a player.
- Playstate + favorite actions require a `user_id`; a server API key alone is not
  a user context.
- Playlist creation takes a `body` object (`Name`, `Ids`, `MediaType`), not flat
  kwargs.

## Related
- `jellyfin-library-catalog` — find item ids to stream / add to playlists.
- `jellyfin-kg-ingestion` — persist artists + media into the knowledge graph.
