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

## Workflows

### jellyfin-mark-watched
Find an item and mark it played for a user.

1. `jellyfin_get_search_hints` (search_term, include_item_types, limit)
2. `jellyfin_get_item` (item_id, user_id)
3. `jellyfin_mark_played_item` (item_id, user_id, date_played)

### jellyfin-build-playlist
Create a playlist, add items and read it back.

1. `jellyfin_create_playlist` (name, ids, media_type, user_id)
2. `jellyfin_add_item_to_playlist` (playlist_id, ids, user_id)
3. `jellyfin_get_playlist_items` (playlist_id, user_id, limit)

### jellyfin-fetch-subtitles
Search remote subtitle providers for an item and download the best match.

1. `jellyfin_get_item` (item_id)
2. `jellyfin_search_remote_subtitles` (item_id, language, is_perfect_match)
3. `jellyfin_download_remote_subtitles` (item_id, subtitle_id)
4. `jellyfin_get_item` (item_id)

### jellyfin-message-session
Show a message on a client that is signed in.

1. `jellyfin_get_sessions` (active_within_seconds, device_id)
2. `jellyfin_send_message_command` (session_id, body)

## All tools of this skill

`jellyfin_add_item_to_playlist`, `jellyfin_add_user_to_session`, `jellyfin_create_playlist`, `jellyfin_delete_alternate_sources`, `jellyfin_delete_device`, `jellyfin_delete_lyrics`, `jellyfin_delete_subtitle`, `jellyfin_display_content`, `jellyfin_download_remote_lyrics`, `jellyfin_download_remote_subtitles`, `jellyfin_get_additional_part`, `jellyfin_get_attachment`, `jellyfin_get_audio_stream`, `jellyfin_get_audio_stream_by_container`, `jellyfin_get_bitrate_test_bytes`, `jellyfin_get_device_info`, `jellyfin_get_device_options`, `jellyfin_get_devices`, `jellyfin_get_download`, `jellyfin_get_file`, `jellyfin_get_hls_audio_segment`, `jellyfin_get_hls_audio_segment_legacy_aac`, `jellyfin_get_hls_audio_segment_legacy_mp3`, `jellyfin_get_hls_playlist_legacy`, `jellyfin_get_hls_video_segment`, `jellyfin_get_hls_video_segment_legacy`, `jellyfin_get_instant_mix_from_playlist`, `jellyfin_get_item`, `jellyfin_get_live_hls_stream`, `jellyfin_get_lyrics`, `jellyfin_get_master_hls_audio_playlist`, `jellyfin_get_master_hls_video_playlist`, `jellyfin_get_playback_info`, `jellyfin_get_playlist`, `jellyfin_get_playlist_items`, `jellyfin_get_playlist_user`, `jellyfin_get_playlist_users`, `jellyfin_get_posted_playback_info`, `jellyfin_get_remote_lyrics`, `jellyfin_get_remote_subtitles`, `jellyfin_get_search_hints`, `jellyfin_get_sessions`, `jellyfin_get_subtitle`, `jellyfin_get_subtitle_playlist`, `jellyfin_get_subtitle_with_ticks`, `jellyfin_get_trickplay_hls_playlist`, `jellyfin_get_universal_audio_stream`, `jellyfin_get_variant_hls_audio_playlist`, `jellyfin_get_variant_hls_video_playlist`, `jellyfin_get_video_stream`, `jellyfin_get_video_stream_by_container`, `jellyfin_mark_played_item`, `jellyfin_mark_unplayed_item`, `jellyfin_merge_versions`, `jellyfin_move_item`, `jellyfin_on_playback_progress`, `jellyfin_on_playback_start`, `jellyfin_on_playback_stopped`, `jellyfin_ping_playback_session`, `jellyfin_play`, `jellyfin_post_capabilities`, `jellyfin_post_full_capabilities`, `jellyfin_remove_item_from_playlist`, `jellyfin_remove_user_from_playlist`, `jellyfin_remove_user_from_session`, `jellyfin_report_playback_progress`, `jellyfin_report_playback_start`, `jellyfin_report_playback_stopped`, `jellyfin_report_session_ended`, `jellyfin_report_viewing`, `jellyfin_search_remote_lyrics`, `jellyfin_search_remote_subtitles`, `jellyfin_send_full_general_command`, `jellyfin_send_general_command`, `jellyfin_send_message_command`, `jellyfin_send_playstate_command`, `jellyfin_stop_encoding_process`, `jellyfin_sync_play_buffering`, `jellyfin_sync_play_create_group`, `jellyfin_sync_play_get_group`, `jellyfin_sync_play_get_groups`, `jellyfin_sync_play_join_group`, `jellyfin_sync_play_leave_group`, `jellyfin_sync_play_move_playlist_item`, `jellyfin_sync_play_next_item`, `jellyfin_sync_play_pause`, `jellyfin_sync_play_ping`, `jellyfin_sync_play_previous_item`, `jellyfin_sync_play_queue`, `jellyfin_sync_play_ready`, `jellyfin_sync_play_remove_from_playlist`, `jellyfin_sync_play_seek`, `jellyfin_sync_play_set_ignore_wait`, `jellyfin_sync_play_set_new_queue`, `jellyfin_sync_play_set_playlist_item`, `jellyfin_sync_play_set_repeat_mode`, `jellyfin_sync_play_set_shuffle_mode`, `jellyfin_sync_play_stop`, `jellyfin_sync_play_unpause`, `jellyfin_update_device_options`, `jellyfin_update_playlist`, `jellyfin_update_playlist_user`, `jellyfin_upload_lyrics`, `jellyfin_upload_subtitle`
