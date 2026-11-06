# Provider workflow catalog

Load only the workflow relevant to the current request.

- `jellyfin-library-catalog`: find items, add media and rescan, build collections, refresh item metadata (typed `jellyfin_get_items`, `jellyfin_get_item`, `jellyfin_add_media_path`, `jellyfin_refresh_library`, `jellyfin_create_collection`, `jellyfin_refresh_item`).
- `jellyfin-media-playback`: watch state, playlists, subtitles, lyrics, streams, shared playback and client messages (`jellyfin_mark_played_item`, `jellyfin_create_playlist`, `jellyfin_search_remote_subtitles`, `jellyfin_send_message_command`).
- `jellyfin-server-administration`: health, tasks, backups, plugins, users and Quick Connect (`jellyfin_get_system_info`, `jellyfin_create_backup`, `jellyfin_install_package`, `jellyfin_create_user_by_name`, `jellyfin_authorize_quick_connect`).
- `jellyfin-live-tv`: guide, tuners and recording timers (`jellyfin_get_programs`, `jellyfin_create_timer`, `jellyfin_get_timers`).
- `jellyfin-kg-ingestion`: mirror the library and posters into the knowledge graph (`jellyfin_ingest_library`, `jellyfin_ingest_posters`).
