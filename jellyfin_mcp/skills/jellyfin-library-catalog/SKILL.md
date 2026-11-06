---
name: jellyfin-library-catalog
skill_type: skill
description: >-
  Browse and search a Jellyfin media library via the jellyfin-mcp MCP server —
  list library items (movies, series, episodes, audio, books), fetch one item by
  id, walk collections and user views, and run search hints with the
  typed `jellyfin_*` tools. Use when the agent must find or enumerate
  catalog items, resolve an item id, inspect a collection, or query library
  structure. Do NOT use for playback/streaming or artists/playlists (use
  `jellyfin-media-playback`), for server administration, users, or backups (use
  the typed `jellyfin_get_system_info` / `jellyfin_get_users` / `jellyfin_create_backup` tools), or for pushing the catalog into the knowledge
  graph (use `jellyfin-kg-ingestion`).
license: MIT
tags: [jellyfin, media, library, catalog, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

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
| `JELLYFIN_URL` | ✅ | Base server URL (e.g. `https://jelly.host`) |
| `JELLYFIN_API_KEY` / `JELLYFIN_TOKEN` | ✅ | `X-Emby-Token` API key |
| `JELLYFIN_USER_ID` | optional | Default `user_id` for user-scoped reads |
| `JELLYFIN_VERIFY_SSL` | optional | TLS verification toggle |

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

## Workflows

### jellyfin-find-item
Resolve a title to an item id and read the item.

1. `jellyfin_get_search_hints` (search_term, include_item_types, limit)
2. `jellyfin_get_items` (search_term, include_item_types, recursive, limit, fields)
3. `jellyfin_get_item` (item_id)

### jellyfin-add-media-and-scan
Add a media folder path to a library, rescan, and confirm the new items.

1. `jellyfin_get_virtual_folders` (no parameters)
2. `jellyfin_add_media_path` (body, refresh_library) - needs the operator's approval.
3. `jellyfin_refresh_library` (no parameters)
4. `jellyfin_get_items` (parent_id, recursive, sort_by, sort_order, limit)

### jellyfin-build-collection
Create a collection (box set) from items and read it back.

1. `jellyfin_get_items` (search_term, include_item_types, recursive, limit)
2. `jellyfin_create_collection` (name, ids, parent_id, is_locked)
3. `jellyfin_add_to_collection` (collection_id, ids)
4. `jellyfin_get_item` (item_id)

### jellyfin-refresh-item-metadata
Re-read the metadata of one item and confirm it.

1. `jellyfin_get_item` (item_id)
2. `jellyfin_refresh_item` (item_id, metadata_refresh_mode, image_refresh_mode, replace_all_metadata, replace_all_images) - needs the operator's approval.
3. `jellyfin_get_item` (item_id)

## All tools of this skill

`jellyfin_add_media_path`, `jellyfin_add_to_collection`, `jellyfin_add_virtual_folder`, `jellyfin_apply_search_criteria`, `jellyfin_create_collection`, `jellyfin_delete_custom_splashscreen`, `jellyfin_delete_item`, `jellyfin_delete_item_image`, `jellyfin_delete_item_image_by_index`, `jellyfin_delete_items`, `jellyfin_delete_user_image`, `jellyfin_download_remote_image`, `jellyfin_get_album_artists`, `jellyfin_get_ancestors`, `jellyfin_get_artist_by_name`, `jellyfin_get_artist_image`, `jellyfin_get_artists`, `jellyfin_get_book_remote_search_results`, `jellyfin_get_box_set_remote_search_results`, `jellyfin_get_critic_reviews`, `jellyfin_get_display_preferences`, `jellyfin_get_episodes`, `jellyfin_get_external_id_infos`, `jellyfin_get_genre`, `jellyfin_get_genre_image`, `jellyfin_get_genre_image_by_index`, `jellyfin_get_genres`, `jellyfin_get_instant_mix_from_album`, `jellyfin_get_instant_mix_from_artists`, `jellyfin_get_instant_mix_from_artists2`, `jellyfin_get_instant_mix_from_item`, `jellyfin_get_instant_mix_from_music_genre_by_id`, `jellyfin_get_instant_mix_from_music_genre_by_name`, `jellyfin_get_instant_mix_from_song`, `jellyfin_get_intros`, `jellyfin_get_item`, `jellyfin_get_item_counts`, `jellyfin_get_item_image`, `jellyfin_get_item_image2`, `jellyfin_get_item_image_by_index`, `jellyfin_get_item_image_infos`, `jellyfin_get_item_segments`, `jellyfin_get_items`, `jellyfin_get_latest_media`, `jellyfin_get_library_options_info`, `jellyfin_get_local_trailers`, `jellyfin_get_media_folders`, `jellyfin_get_metadata_editor_info`, `jellyfin_get_movie_recommendations`, `jellyfin_get_movie_remote_search_results`, `jellyfin_get_music_album_remote_search_results`, `jellyfin_get_music_artist_remote_search_results`, `jellyfin_get_music_genre`, `jellyfin_get_music_genre_image`, `jellyfin_get_music_genre_image_by_index`, `jellyfin_get_music_genres`, `jellyfin_get_music_video_remote_search_results`, `jellyfin_get_next_up`, `jellyfin_get_person`, `jellyfin_get_person_image`, `jellyfin_get_person_image_by_index`, `jellyfin_get_person_remote_search_results`, `jellyfin_get_persons`, `jellyfin_get_physical_paths`, `jellyfin_get_plugin_image`, `jellyfin_get_query_filters`, `jellyfin_get_query_filters_legacy`, `jellyfin_get_remote_image_providers`, `jellyfin_get_remote_images`, `jellyfin_get_resume_items`, `jellyfin_get_root_folder`, `jellyfin_get_search_hints`, `jellyfin_get_seasons`, `jellyfin_get_series_remote_search_results`, `jellyfin_get_similar_albums`, `jellyfin_get_similar_artists`, `jellyfin_get_similar_items`, `jellyfin_get_similar_movies`, `jellyfin_get_similar_shows`, `jellyfin_get_similar_trailers`, `jellyfin_get_special_features`, `jellyfin_get_splashscreen`, `jellyfin_get_studio`, `jellyfin_get_studio_image`, `jellyfin_get_studio_image_by_index`, `jellyfin_get_studios`, `jellyfin_get_suggestions`, `jellyfin_get_theme_media`, `jellyfin_get_theme_songs`, `jellyfin_get_theme_videos`, `jellyfin_get_trailer_remote_search_results`, `jellyfin_get_trailers`, `jellyfin_get_trickplay_tile_image`, `jellyfin_get_upcoming_episodes`, `jellyfin_get_user_image`, `jellyfin_get_virtual_folders`, `jellyfin_get_year`, `jellyfin_get_years`, `jellyfin_ingest_library`, `jellyfin_ingest_posters`, `jellyfin_mark_favorite_item`, `jellyfin_post_added_movies`, `jellyfin_post_added_series`, `jellyfin_post_updated_media`, `jellyfin_post_updated_movies`, `jellyfin_post_updated_series`, `jellyfin_post_user_image`, `jellyfin_refresh_item`, `jellyfin_refresh_library`, `jellyfin_remove_from_collection`, `jellyfin_remove_media_path`, `jellyfin_remove_virtual_folder`, `jellyfin_rename_virtual_folder`, `jellyfin_set_item_image`, `jellyfin_set_item_image_by_index`, `jellyfin_unmark_favorite_item`, `jellyfin_update_display_preferences`, `jellyfin_update_item`, `jellyfin_update_item_content_type`, `jellyfin_update_item_image_index`, `jellyfin_update_library_options`, `jellyfin_update_media_path`, `jellyfin_upload_custom_splashscreen`
