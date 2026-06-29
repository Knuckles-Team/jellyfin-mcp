# Jellyfin Mcp
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/jellyfin-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/jellyfin-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/jellyfin-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/jellyfin-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/jellyfin-mcp)
![PyPI - License](https://img.shields.io/pypi/l/jellyfin-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/jellyfin-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/jellyfin-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/jellyfin-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/jellyfin-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/jellyfin-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/jellyfin-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/jellyfin-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/jellyfin-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/jellyfin-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/jellyfin-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/jellyfin-mcp)

*Version: 1.0.0*

> **Documentation** — Installation, deployment, usage across the MCP, API, and A2A
> agent interfaces, and guidance for provisioning the Jellyfin media server are
> maintained in the [official documentation](https://knuckles-team.github.io/jellyfin-mcp/).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI or API](#cli-or-api)
- [MCP Integration](#mcp)
  - [Available MCP Tools](#available-mcp-tools)
  - [MCP Configuration Examples](#mcp-configuration-examples)
- [Agent Capabilities](#agent)
  - [Running the Agent CLI](#running-the-agent-cli)
  - [Docker Compose Orchestration](#docker-compose-orchestration)
- [Security & Governance](#security--governance)
- [Documentation](#documentation)
- [Contribute](#contribute)

---

## Overview

**Jellyfin Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Jellyfin MCP Server for Agentic AI!.

---

## Quick Start

### 1. Installation
Install the package directly from PyPI:
```bash
uv pip install jellyfin-mcp[all]
```

### 2. Configure Environment
Set up your connection keys and Jellyfin host details (see `.env.example` for comprehensive list):
```bash
export JELLYFIN_URL="http://localhost:8096"
export JELLYFIN_API_KEY="your_api_key_here"
```

### 3. Run the MCP Server
Launch the server over standard standard I/O (stdio) transport:
```bash
jellyfin-mcp
```

### 4. Run the Agent CLI
To launch the interactive Graph Agent terminal interface:
```bash
jellyfin-agent --provider openai --model-id gpt-4o
```

---

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Jellyfin MCP Server for Agentic AI! API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

_Auto-generated from the live MCP server — do not edit by hand._

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `jellyfin_library` | `CONDENSED_JELLYFINTOOL` | Execute library searches, items, collection updates, and catalog queries dynamically. |
| `jellyfin_media` | `CONDENSED_JELLYFINTOOL` | Execute media playback, stream, artist, playlist, and audio/video queries dynamically. |
| `jellyfin_system` | `CONDENSED_JELLYFINTOOL` | Execute administrative actions, system status, configurations, backups, and user management. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>368 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `jellyfin_add_item_to_playlist` | `MEDIA_CLIENTTOOL` | Adds items to a playlist. |
| `jellyfin_add_listing_provider` | `MEDIA_CLIENTTOOL` | Adds a listings provider. |
| `jellyfin_add_media_path` | `LIBRARY_CLIENTTOOL` | Add a media path to a library. |
| `jellyfin_add_to_collection` | `LIBRARY_CLIENTTOOL` | Adds items to a collection. |
| `jellyfin_add_tuner_host` | `MEDIA_CLIENTTOOL` | Adds a tuner host. |
| `jellyfin_add_user_to_session` | `USER_CLIENTTOOL` | Adds an additional user to a session. |
| `jellyfin_add_virtual_folder` | `LIBRARY_CLIENTTOOL` | Adds a virtual folder. |
| `jellyfin_apply_search_criteria` | `LIBRARY_CLIENTTOOL` | Applies search criteria to an item and refreshes metadata. |
| `jellyfin_authenticate_user_by_name` | `USER_CLIENTTOOL` | Authenticates a user by name. |
| `jellyfin_authenticate_with_quick_connect` | `USER_CLIENTTOOL` | Authenticates a user with quick connect. |
| `jellyfin_authorize_quick_connect` | `USER_CLIENTTOOL` | Authorizes a pending quick connect request. |
| `jellyfin_cancel_package_installation` | `LIBRARY_CLIENTTOOL` | Cancels a package installation. |
| `jellyfin_cancel_series_timer` | `MEDIA_CLIENTTOOL` | Cancels a live tv series timer. |
| `jellyfin_cancel_timer` | `MEDIA_CLIENTTOOL` | Cancels a live tv timer. |
| `jellyfin_close_live_stream` | `MEDIA_CLIENTTOOL` | Closes a media source. |
| `jellyfin_complete_wizard` | `LIBRARY_CLIENTTOOL` | Completes the startup wizard. |
| `jellyfin_create_backup` | `SYSTEM_CLIENTTOOL` | Creates a new Backup. |
| `jellyfin_create_collection` | `LIBRARY_CLIENTTOOL` | Creates a new collection. |
| `jellyfin_create_key` | `SYSTEM_CLIENTTOOL` | Create a new api key. |
| `jellyfin_create_playlist` | `MEDIA_CLIENTTOOL` | Creates a new playlist. |
| `jellyfin_create_series_timer` | `MEDIA_CLIENTTOOL` | Creates a live tv series timer. |
| `jellyfin_create_timer` | `MEDIA_CLIENTTOOL` | Creates a live tv timer. |
| `jellyfin_create_user_by_name` | `USER_CLIENTTOOL` | Creates a user. |
| `jellyfin_delete_alternate_sources` | `MEDIA_CLIENTTOOL` | Removes alternate video sources. |
| `jellyfin_delete_custom_splashscreen` | `SYSTEM_CLIENTTOOL` | Delete a custom splashscreen. |
| `jellyfin_delete_device` | `USER_CLIENTTOOL` | Deletes a device. |
| `jellyfin_delete_item` | `LIBRARY_CLIENTTOOL` | Deletes an item from the library and filesystem. |
| `jellyfin_delete_item_image` | `LIBRARY_CLIENTTOOL` | Delete an item's image. |
| `jellyfin_delete_item_image_by_index` | `LIBRARY_CLIENTTOOL` | Delete an item's image. |
| `jellyfin_delete_items` | `LIBRARY_CLIENTTOOL` | Deletes items from the library and filesystem. |
| `jellyfin_delete_listing_provider` | `MEDIA_CLIENTTOOL` | Delete listing provider. |
| `jellyfin_delete_lyrics` | `MEDIA_CLIENTTOOL` | Deletes an external lyric file. |
| `jellyfin_delete_recording` | `MEDIA_CLIENTTOOL` | Deletes a live tv recording. |
| `jellyfin_delete_subtitle` | `MEDIA_CLIENTTOOL` | Deletes an external subtitle file. |
| `jellyfin_delete_tuner_host` | `MEDIA_CLIENTTOOL` | Deletes a tuner host. |
| `jellyfin_delete_user` | `USER_CLIENTTOOL` | Deletes a user. |
| `jellyfin_delete_user_image` | `USER_CLIENTTOOL` | Delete the user's image. |
| `jellyfin_delete_user_item_rating` | `USER_CLIENTTOOL` | Deletes a user's saved personal rating for an item. |
| `jellyfin_disable_plugin` | `SYSTEM_CLIENTTOOL` | Disable a plugin. |
| `jellyfin_discover_tuners` | `MEDIA_CLIENTTOOL` | Discover tuners. |
| `jellyfin_discvover_tuners` | `MEDIA_CLIENTTOOL` | Discover tuners. |
| `jellyfin_display_content` | `MEDIA_CLIENTTOOL` | Instructs a session to browse to an item or view. |
| `jellyfin_download_remote_image` | `LIBRARY_CLIENTTOOL` | Downloads a remote image for an item. |
| `jellyfin_download_remote_lyrics` | `MEDIA_CLIENTTOOL` | Downloads a remote lyric. |
| `jellyfin_download_remote_subtitles` | `MEDIA_CLIENTTOOL` | Downloads a remote subtitle. |
| `jellyfin_enable_plugin` | `SYSTEM_CLIENTTOOL` | Enables a disabled plugin. |
| `jellyfin_forgot_password` | `USER_CLIENTTOOL` | Initiates the forgot password process for a local user. |
| `jellyfin_forgot_password_pin` | `USER_CLIENTTOOL` | Redeems a forgot password pin. |
| `jellyfin_get_additional_part` | `MEDIA_CLIENTTOOL` | Gets additional parts for a video. |
| `jellyfin_get_album_artists` | `MEDIA_CLIENTTOOL` | Gets all album artists from a given item, folder, or the entire library. |
| `jellyfin_get_all_channel_features` | `MEDIA_CLIENTTOOL` | Get all channel features. |
| `jellyfin_get_ancestors` | `LIBRARY_CLIENTTOOL` | Gets all parents of an item. |
| `jellyfin_get_artist_by_name` | `MEDIA_CLIENTTOOL` | Gets an artist by name. |
| `jellyfin_get_artist_image` | `MEDIA_CLIENTTOOL` | Get artist image by name. |
| `jellyfin_get_artists` | `MEDIA_CLIENTTOOL` | Gets all artists from a given item, folder, or the entire library. |
| `jellyfin_get_attachment` | `MEDIA_CLIENTTOOL` | Get video attachment. |
| `jellyfin_get_audio_stream` | `MEDIA_CLIENTTOOL` | Gets an audio stream. |
| `jellyfin_get_audio_stream_by_container` | `MEDIA_CLIENTTOOL` | Gets an audio stream. |
| `jellyfin_get_auth_providers` | `USER_CLIENTTOOL` | Get all auth providers. |
| `jellyfin_get_backup` | `SYSTEM_CLIENTTOOL` | Gets the descriptor from an existing archive is present. |
| `jellyfin_get_bitrate_test_bytes` | `LIBRARY_CLIENTTOOL` | Tests the network with a request with the size of the bitrate. |
| `jellyfin_get_book_remote_search_results` | `LIBRARY_CLIENTTOOL` | Get book remote search. |
| `jellyfin_get_box_set_remote_search_results` | `LIBRARY_CLIENTTOOL` | Get box set remote search. |
| `jellyfin_get_branding_css` | `SYSTEM_CLIENTTOOL` | Gets branding css. |
| `jellyfin_get_branding_css_2` | `SYSTEM_CLIENTTOOL` | Gets branding css. |
| `jellyfin_get_branding_options` | `SYSTEM_CLIENTTOOL` | Gets branding configuration. |
| `jellyfin_get_channel` | `MEDIA_CLIENTTOOL` | Gets a live tv channel. |
| `jellyfin_get_channel_features` | `MEDIA_CLIENTTOOL` | Get channel features. |
| `jellyfin_get_channel_items` | `MEDIA_CLIENTTOOL` | Get channel items. |
| `jellyfin_get_channel_mapping_options` | `SYSTEM_CLIENTTOOL` | Get channel mapping options. |
| `jellyfin_get_channels` | `MEDIA_CLIENTTOOL` | Gets available channels. |
| `jellyfin_get_configuration` | `SYSTEM_CLIENTTOOL` | Gets application configuration. |
| `jellyfin_get_configuration_pages` | `SYSTEM_CLIENTTOOL` | Gets the configuration pages. |
| `jellyfin_get_countries` | `LIBRARY_CLIENTTOOL` | Gets known countries. |
| `jellyfin_get_critic_reviews` | `LIBRARY_CLIENTTOOL` | Gets critic review for an item. |
| `jellyfin_get_cultures` | `LIBRARY_CLIENTTOOL` | Gets known cultures. |
| `jellyfin_get_current_user` | `USER_CLIENTTOOL` | Gets the user based on auth token. |
| `jellyfin_get_dashboard_configuration_page` | `SYSTEM_CLIENTTOOL` | Gets a dashboard configuration page. |
| `jellyfin_get_default_directory_browser` | `SYSTEM_CLIENTTOOL` | Get Default directory browser. |
| `jellyfin_get_default_listing_provider` | `MEDIA_CLIENTTOOL` | Gets default listings provider info. |
| `jellyfin_get_default_metadata_options` | `SYSTEM_CLIENTTOOL` | Gets a default MetadataOptions object. |
| `jellyfin_get_default_timer` | `MEDIA_CLIENTTOOL` | Gets the default values for a new timer. |
| `jellyfin_get_device_info` | `USER_CLIENTTOOL` | Get info for a device. |
| `jellyfin_get_device_options` | `USER_CLIENTTOOL` | Get options for a device. |
| `jellyfin_get_devices` | `USER_CLIENTTOOL` | Get Devices. |
| `jellyfin_get_directory_contents` | `SYSTEM_CLIENTTOOL` | Gets the contents of a given directory in the file system. |
| `jellyfin_get_display_preferences` | `MEDIA_CLIENTTOOL` | Get Display Preferences. |
| `jellyfin_get_download` | `LIBRARY_CLIENTTOOL` | Downloads item media. |
| `jellyfin_get_drives` | `SYSTEM_CLIENTTOOL` | Gets available drives from the server's file system. |
| `jellyfin_get_endpoint_info` | `SYSTEM_CLIENTTOOL` | Gets information about the request endpoint. |
| `jellyfin_get_episodes` | `LIBRARY_CLIENTTOOL` | Gets episodes for a tv season. |
| `jellyfin_get_external_id_infos` | `LIBRARY_CLIENTTOOL` | Get the item's external id info. |
| `jellyfin_get_fallback_font` | `LIBRARY_CLIENTTOOL` | Gets a fallback font file. |
| `jellyfin_get_fallback_font_list` | `LIBRARY_CLIENTTOOL` | Gets a list of available fallback font files. |
| `jellyfin_get_file` | `LIBRARY_CLIENTTOOL` | Get the original file of an item. |
| `jellyfin_get_first_user` | `USER_CLIENTTOOL` | Gets the first user. |
| `jellyfin_get_first_user_2` | `USER_CLIENTTOOL` | Gets the first user. |
| `jellyfin_get_genre` | `LIBRARY_CLIENTTOOL` | Gets a genre, by name. |
| `jellyfin_get_genre_image` | `LIBRARY_CLIENTTOOL` | Get genre image by name. |
| `jellyfin_get_genre_image_by_index` | `LIBRARY_CLIENTTOOL` | Get genre image by name. |
| `jellyfin_get_genres` | `LIBRARY_CLIENTTOOL` | Gets all genres from a given item, folder, or the entire library. |
| `jellyfin_get_grouping_options` | `SYSTEM_CLIENTTOOL` | Get user view grouping options. |
| `jellyfin_get_guide_info` | `MEDIA_CLIENTTOOL` | Get guide info. |
| `jellyfin_get_hls_audio_segment` | `MEDIA_CLIENTTOOL` | Gets a video stream using HTTP live streaming. |
| `jellyfin_get_hls_audio_segment_legacy_aac` | `MEDIA_CLIENTTOOL` | Gets the specified audio segment for an audio item. |
| `jellyfin_get_hls_audio_segment_legacy_mp3` | `MEDIA_CLIENTTOOL` | Gets the specified audio segment for an audio item. |
| `jellyfin_get_hls_playlist_legacy` | `MEDIA_CLIENTTOOL` | Gets a hls video playlist. |
| `jellyfin_get_hls_video_segment` | `MEDIA_CLIENTTOOL` | Gets a video stream using HTTP live streaming. |
| `jellyfin_get_hls_video_segment_legacy` | `MEDIA_CLIENTTOOL` | Gets a hls video segment. |
| `jellyfin_get_instant_mix_from_album` | `LIBRARY_CLIENTTOOL` | Creates an instant playlist based on a given album. |
| `jellyfin_get_instant_mix_from_artists` | `MEDIA_CLIENTTOOL` | Creates an instant playlist based on a given artist. |
| `jellyfin_get_instant_mix_from_artists2` | `MEDIA_CLIENTTOOL` | Creates an instant playlist based on a given artist. |
| `jellyfin_get_instant_mix_from_item` | `LIBRARY_CLIENTTOOL` | Creates an instant playlist based on a given item. |
| `jellyfin_get_instant_mix_from_music_genre_by_id` | `MEDIA_CLIENTTOOL` | Creates an instant playlist based on a given genre. |
| `jellyfin_get_instant_mix_from_music_genre_by_name` | `MEDIA_CLIENTTOOL` | Creates an instant playlist based on a given genre. |
| `jellyfin_get_instant_mix_from_playlist` | `MEDIA_CLIENTTOOL` | Creates an instant playlist based on a given playlist. |
| `jellyfin_get_instant_mix_from_song` | `MEDIA_CLIENTTOOL` | Creates an instant playlist based on a given song. |
| `jellyfin_get_intros` | `LIBRARY_CLIENTTOOL` | Gets intros to play before the main media item plays. |
| `jellyfin_get_item` | `LIBRARY_CLIENTTOOL` | Gets an item from a user's library. |
| `jellyfin_get_item_counts` | `LIBRARY_CLIENTTOOL` | Get item counts. |
| `jellyfin_get_item_image` | `LIBRARY_CLIENTTOOL` | Gets the item's image. |
| `jellyfin_get_item_image2` | `LIBRARY_CLIENTTOOL` | Gets the item's image. |
| `jellyfin_get_item_image_by_index` | `LIBRARY_CLIENTTOOL` | Gets the item's image. |
| `jellyfin_get_item_image_infos` | `LIBRARY_CLIENTTOOL` | Get item image infos. |
| `jellyfin_get_item_segments` | `MEDIA_CLIENTTOOL` | Gets all media segments based on an itemId. |
| `jellyfin_get_item_user_data` | `USER_CLIENTTOOL` | Get Item User Data. |
| `jellyfin_get_items` | `LIBRARY_CLIENTTOOL` | Gets items based on a query. |
| `jellyfin_get_keys` | `SYSTEM_CLIENTTOOL` | Get all keys. |
| `jellyfin_get_latest_channel_items` | `MEDIA_CLIENTTOOL` | Gets latest channel items. |
| `jellyfin_get_latest_media` | `LIBRARY_CLIENTTOOL` | Gets latest media. |
| `jellyfin_get_library_options_info` | `LIBRARY_CLIENTTOOL` | Gets the library options info. |
| `jellyfin_get_lineups` | `MEDIA_CLIENTTOOL` | Gets available lineups. |
| `jellyfin_get_live_hls_stream` | `MEDIA_CLIENTTOOL` | Gets a hls live stream. |
| `jellyfin_get_live_recording_file` | `MEDIA_CLIENTTOOL` | Gets a live tv recording stream. |
| `jellyfin_get_live_stream_file` | `MEDIA_CLIENTTOOL` | Gets a live tv channel stream. |
| `jellyfin_get_live_tv_channels` | `MEDIA_CLIENTTOOL` | Gets available live tv channels. |
| `jellyfin_get_live_tv_info` | `MEDIA_CLIENTTOOL` | Gets available live tv services. |
| `jellyfin_get_live_tv_programs` | `MEDIA_CLIENTTOOL` | Gets available live tv epgs. |
| `jellyfin_get_local_trailers` | `MEDIA_CLIENTTOOL` | Gets local trailers for an item. |
| `jellyfin_get_localization_options` | `LIBRARY_CLIENTTOOL` | Gets localization options. |
| `jellyfin_get_log_entries` | `SYSTEM_CLIENTTOOL` | Gets activity log entries. |
| `jellyfin_get_log_file` | `SYSTEM_CLIENTTOOL` | Gets a log file. |
| `jellyfin_get_lyrics` | `MEDIA_CLIENTTOOL` | Gets an item's lyrics. |
| `jellyfin_get_master_hls_audio_playlist` | `MEDIA_CLIENTTOOL` | Gets an audio hls playlist stream. |
| `jellyfin_get_master_hls_video_playlist` | `MEDIA_CLIENTTOOL` | Gets a video hls playlist stream. |
| `jellyfin_get_media_folders` | `MEDIA_CLIENTTOOL` | Gets all user media folders. |
| `jellyfin_get_metadata_editor_info` | `LIBRARY_CLIENTTOOL` | Gets metadata editor info for an item. |
| `jellyfin_get_movie_recommendations` | `MEDIA_CLIENTTOOL` | Gets movie recommendations. |
| `jellyfin_get_movie_remote_search_results` | `MEDIA_CLIENTTOOL` | Get movie remote search. |
| `jellyfin_get_music_album_remote_search_results` | `MEDIA_CLIENTTOOL` | Get music album remote search. |
| `jellyfin_get_music_artist_remote_search_results` | `MEDIA_CLIENTTOOL` | Get music artist remote search. |
| `jellyfin_get_music_genre` | `MEDIA_CLIENTTOOL` | Gets a music genre, by name. |
| `jellyfin_get_music_genre_image` | `MEDIA_CLIENTTOOL` | Get music genre image by name. |
| `jellyfin_get_music_genre_image_by_index` | `MEDIA_CLIENTTOOL` | Get music genre image by name. |
| `jellyfin_get_music_genres` | `MEDIA_CLIENTTOOL` | Gets all music genres from a given item, folder, or the entire library. |
| `jellyfin_get_music_video_remote_search_results` | `MEDIA_CLIENTTOOL` | Get music video remote search. |
| `jellyfin_get_named_configuration` | `SYSTEM_CLIENTTOOL` | Gets a named configuration. |
| `jellyfin_get_network_shares` | `SYSTEM_CLIENTTOOL` | Gets network paths. |
| `jellyfin_get_next_up` | `LIBRARY_CLIENTTOOL` | Gets a list of next up episodes. |
| `jellyfin_get_package_info` | `LIBRARY_CLIENTTOOL` | Gets a package by name or assembly GUID. |
| `jellyfin_get_packages` | `LIBRARY_CLIENTTOOL` | Gets available packages. |
| `jellyfin_get_parent_path` | `SYSTEM_CLIENTTOOL` | Gets the parent path of a given path. |
| `jellyfin_get_parental_ratings` | `LIBRARY_CLIENTTOOL` | Gets known parental ratings. |
| `jellyfin_get_password_reset_providers` | `USER_CLIENTTOOL` | Get all password reset providers. |
| `jellyfin_get_person` | `LIBRARY_CLIENTTOOL` | Get person by name. |
| `jellyfin_get_person_image` | `LIBRARY_CLIENTTOOL` | Get person image by name. |
| `jellyfin_get_person_image_by_index` | `LIBRARY_CLIENTTOOL` | Get person image by name. |
| `jellyfin_get_person_remote_search_results` | `LIBRARY_CLIENTTOOL` | Get person remote search. |
| `jellyfin_get_persons` | `LIBRARY_CLIENTTOOL` | Gets all persons. |
| `jellyfin_get_physical_paths` | `LIBRARY_CLIENTTOOL` | Gets a list of physical paths from virtual folders. |
| `jellyfin_get_ping_system` | `SYSTEM_CLIENTTOOL` | Pings the system. |
| `jellyfin_get_playback_info` | `MEDIA_CLIENTTOOL` | Gets live playback media info for an item. |
| `jellyfin_get_playlist` | `MEDIA_CLIENTTOOL` | Get a playlist. |
| `jellyfin_get_playlist_items` | `MEDIA_CLIENTTOOL` | Gets the original items of a playlist. |
| `jellyfin_get_playlist_user` | `MEDIA_CLIENTTOOL` | Get a playlist user. |
| `jellyfin_get_playlist_users` | `MEDIA_CLIENTTOOL` | Get a playlist's users. |
| `jellyfin_get_plugin_configuration` | `SYSTEM_CLIENTTOOL` | Gets plugin configuration. |
| `jellyfin_get_plugin_image` | `SYSTEM_CLIENTTOOL` | Gets a plugin's image. |
| `jellyfin_get_plugin_manifest` | `SYSTEM_CLIENTTOOL` | Gets a plugin's manifest. |
| `jellyfin_get_plugins` | `SYSTEM_CLIENTTOOL` | Gets a list of currently installed plugins. |
| `jellyfin_get_posted_playback_info` | `MEDIA_CLIENTTOOL` | Gets live playback media info for an item. |
| `jellyfin_get_program` | `MEDIA_CLIENTTOOL` | Gets a live tv program. |
| `jellyfin_get_programs` | `MEDIA_CLIENTTOOL` | Gets available live tv epgs. |
| `jellyfin_get_public_system_info` | `SYSTEM_CLIENTTOOL` | Gets public information about the server. |
| `jellyfin_get_public_users` | `USER_CLIENTTOOL` | Gets a list of publicly visible users for display on a login screen. |
| `jellyfin_get_query_filters` | `LIBRARY_CLIENTTOOL` | Gets query filters. |
| `jellyfin_get_query_filters_legacy` | `LIBRARY_CLIENTTOOL` | Gets legacy query filters. |
| `jellyfin_get_quick_connect_enabled` | `USER_CLIENTTOOL` | Gets the current quick connect state. |
| `jellyfin_get_quick_connect_state` | `USER_CLIENTTOOL` | Attempts to retrieve authentication information. |
| `jellyfin_get_recommended_programs` | `MEDIA_CLIENTTOOL` | Gets recommended live tv epgs. |
| `jellyfin_get_recording` | `MEDIA_CLIENTTOOL` | Gets a live tv recording. |
| `jellyfin_get_recording_folders` | `MEDIA_CLIENTTOOL` | Gets recording folders. |
| `jellyfin_get_recording_group` | `MEDIA_CLIENTTOOL` | Get recording group. |
| `jellyfin_get_recording_groups` | `MEDIA_CLIENTTOOL` | Gets live tv recording groups. |
| `jellyfin_get_recordings` | `MEDIA_CLIENTTOOL` | Gets live tv recordings. |
| `jellyfin_get_recordings_series` | `MEDIA_CLIENTTOOL` | Gets live tv recording series. |
| `jellyfin_get_remote_image_providers` | `LIBRARY_CLIENTTOOL` | Gets available remote image providers for an item. |
| `jellyfin_get_remote_images` | `LIBRARY_CLIENTTOOL` | Gets available remote images for an item. |
| `jellyfin_get_remote_lyrics` | `MEDIA_CLIENTTOOL` | Gets the remote lyrics. |
| `jellyfin_get_remote_subtitles` | `MEDIA_CLIENTTOOL` | Gets the remote subtitles. |
| `jellyfin_get_repositories` | `LIBRARY_CLIENTTOOL` | Gets all package repositories. |
| `jellyfin_get_resume_items` | `LIBRARY_CLIENTTOOL` | Gets items based on a query. |
| `jellyfin_get_root_folder` | `LIBRARY_CLIENTTOOL` | Gets the root folder from a user's library. |
| `jellyfin_get_schedules_direct_countries` | `MEDIA_CLIENTTOOL` | Gets available countries. |
| `jellyfin_get_search_hints` | `LIBRARY_CLIENTTOOL` | Gets the search hint result. |
| `jellyfin_get_seasons` | `LIBRARY_CLIENTTOOL` | Gets seasons for a tv series. |
| `jellyfin_get_series_remote_search_results` | `LIBRARY_CLIENTTOOL` | Get series remote search. |
| `jellyfin_get_series_timer` | `MEDIA_CLIENTTOOL` | Gets a live tv series timer. |
| `jellyfin_get_series_timers` | `MEDIA_CLIENTTOOL` | Gets live tv series timers. |
| `jellyfin_get_server_logs` | `SYSTEM_CLIENTTOOL` | Gets a list of available server log files. |
| `jellyfin_get_sessions` | `USER_CLIENTTOOL` | Gets a list of sessions. |
| `jellyfin_get_similar_albums` | `LIBRARY_CLIENTTOOL` | Gets similar items. |
| `jellyfin_get_similar_artists` | `MEDIA_CLIENTTOOL` | Gets similar items. |
| `jellyfin_get_similar_items` | `LIBRARY_CLIENTTOOL` | Gets similar items. |
| `jellyfin_get_similar_movies` | `MEDIA_CLIENTTOOL` | Gets similar items. |
| `jellyfin_get_similar_shows` | `LIBRARY_CLIENTTOOL` | Gets similar items. |
| `jellyfin_get_similar_trailers` | `MEDIA_CLIENTTOOL` | Gets similar items. |
| `jellyfin_get_special_features` | `LIBRARY_CLIENTTOOL` | Gets special features for an item. |
| `jellyfin_get_splashscreen` | `SYSTEM_CLIENTTOOL` | Generates or gets the splashscreen. |
| `jellyfin_get_startup_configuration` | `SYSTEM_CLIENTTOOL` | Gets the initial startup wizard configuration. |
| `jellyfin_get_studio` | `LIBRARY_CLIENTTOOL` | Gets a studio by name. |
| `jellyfin_get_studio_image` | `LIBRARY_CLIENTTOOL` | Get studio image by name. |
| `jellyfin_get_studio_image_by_index` | `LIBRARY_CLIENTTOOL` | Get studio image by name. |
| `jellyfin_get_studios` | `LIBRARY_CLIENTTOOL` | Gets all studios from a given item, folder, or the entire library. |
| `jellyfin_get_subtitle` | `MEDIA_CLIENTTOOL` | Gets subtitles in a specified format. |
| `jellyfin_get_subtitle_playlist` | `MEDIA_CLIENTTOOL` | Gets an HLS subtitle playlist. |
| `jellyfin_get_subtitle_with_ticks` | `MEDIA_CLIENTTOOL` | Gets subtitles in a specified format. |
| `jellyfin_get_suggestions` | `LIBRARY_CLIENTTOOL` | Gets suggestions. |
| `jellyfin_get_system_info` | `SYSTEM_CLIENTTOOL` | Gets information about the server. |
| `jellyfin_get_system_storage` | `SYSTEM_CLIENTTOOL` | Gets information about the server. |
| `jellyfin_get_task` | `SYSTEM_CLIENTTOOL` | Get task by id. |
| `jellyfin_get_tasks` | `SYSTEM_CLIENTTOOL` | Get tasks. |
| `jellyfin_get_theme_media` | `LIBRARY_CLIENTTOOL` | Get theme songs and videos for an item. |
| `jellyfin_get_theme_songs` | `MEDIA_CLIENTTOOL` | Get theme songs for an item. |
| `jellyfin_get_theme_videos` | `MEDIA_CLIENTTOOL` | Get theme videos for an item. |
| `jellyfin_get_timer` | `MEDIA_CLIENTTOOL` | Gets a timer. |
| `jellyfin_get_timers` | `MEDIA_CLIENTTOOL` | Gets the live tv timers. |
| `jellyfin_get_trailer_remote_search_results` | `MEDIA_CLIENTTOOL` | Get trailer remote search. |
| `jellyfin_get_trailers` | `MEDIA_CLIENTTOOL` | Finds movies and trailers similar to a given trailer. |
| `jellyfin_get_trickplay_hls_playlist` | `MEDIA_CLIENTTOOL` | Gets an image tiles playlist for trickplay. |
| `jellyfin_get_trickplay_tile_image` | `MEDIA_CLIENTTOOL` | Gets a trickplay tile image. |
| `jellyfin_get_tuner_host_types` | `MEDIA_CLIENTTOOL` | Get tuner host types. |
| `jellyfin_get_universal_audio_stream` | `MEDIA_CLIENTTOOL` | Gets an audio stream. |
| `jellyfin_get_upcoming_episodes` | `LIBRARY_CLIENTTOOL` | Gets a list of upcoming episodes. |
| `jellyfin_get_user_by_id` | `USER_CLIENTTOOL` | Gets a user by Id. |
| `jellyfin_get_user_image` | `USER_CLIENTTOOL` | Get user profile image. |
| `jellyfin_get_user_views` | `USER_CLIENTTOOL` | Get user views. |
| `jellyfin_get_users` | `USER_CLIENTTOOL` | Gets a list of users. |
| `jellyfin_get_utc_time` | `LIBRARY_CLIENTTOOL` | Gets the current UTC time. |
| `jellyfin_get_variant_hls_audio_playlist` | `MEDIA_CLIENTTOOL` | Gets an audio stream using HTTP live streaming. |
| `jellyfin_get_variant_hls_video_playlist` | `MEDIA_CLIENTTOOL` | Gets a video stream using HTTP live streaming. |
| `jellyfin_get_video_stream` | `MEDIA_CLIENTTOOL` | Gets a video stream. |
| `jellyfin_get_video_stream_by_container` | `MEDIA_CLIENTTOOL` | Gets a video stream. |
| `jellyfin_get_virtual_folders` | `LIBRARY_CLIENTTOOL` | Gets all virtual folders. |
| `jellyfin_get_year` | `LIBRARY_CLIENTTOOL` | Gets a year. |
| `jellyfin_get_years` | `LIBRARY_CLIENTTOOL` | Get years. |
| `jellyfin_initiate_quick_connect` | `USER_CLIENTTOOL` | Initiate a new quick connect request. |
| `jellyfin_install_package` | `LIBRARY_CLIENTTOOL` | Installs a package. |
| `jellyfin_list_backups` | `SYSTEM_CLIENTTOOL` | Gets a list of all currently present backups in the backup directory. |
| `jellyfin_log_file` | `SYSTEM_CLIENTTOOL` | Upload a document. |
| `jellyfin_mark_favorite_item` | `LIBRARY_CLIENTTOOL` | Marks an item as a favorite. |
| `jellyfin_mark_played_item` | `MEDIA_CLIENTTOOL` | Marks an item as played for user. |
| `jellyfin_mark_unplayed_item` | `MEDIA_CLIENTTOOL` | Marks an item as unplayed for user. |
| `jellyfin_merge_versions` | `MEDIA_CLIENTTOOL` | Merges videos into a single record. |
| `jellyfin_move_item` | `MEDIA_CLIENTTOOL` | Moves a playlist item. |
| `jellyfin_on_playback_progress` | `MEDIA_CLIENTTOOL` | Reports a session's playback progress. |
| `jellyfin_on_playback_start` | `MEDIA_CLIENTTOOL` | Reports that a session has begun playing an item. |
| `jellyfin_on_playback_stopped` | `MEDIA_CLIENTTOOL` | Reports that a session has stopped playing an item. |
| `jellyfin_open_live_stream` | `MEDIA_CLIENTTOOL` | Opens a media source. |
| `jellyfin_ping_playback_session` | `SYSTEM_CLIENTTOOL` | Pings a playback session. |
| `jellyfin_play` | `MEDIA_CLIENTTOOL` | Instructs a session to play an item. |
| `jellyfin_post_added_movies` | `MEDIA_CLIENTTOOL` | Reports that new movies have been added by an external source. |
| `jellyfin_post_added_series` | `LIBRARY_CLIENTTOOL` | Reports that new episodes of a series have been added by an external source. |
| `jellyfin_post_capabilities` | `USER_CLIENTTOOL` | Updates capabilities for a device. |
| `jellyfin_post_full_capabilities` | `USER_CLIENTTOOL` | Updates capabilities for a device. |
| `jellyfin_post_ping_system` | `SYSTEM_CLIENTTOOL` | Pings the system. |
| `jellyfin_post_updated_media` | `MEDIA_CLIENTTOOL` | Reports that new movies have been added by an external source. |
| `jellyfin_post_updated_movies` | `MEDIA_CLIENTTOOL` | Reports that new movies have been added by an external source. |
| `jellyfin_post_updated_series` | `LIBRARY_CLIENTTOOL` | Reports that new episodes of a series have been added by an external source. |
| `jellyfin_post_user_image` | `USER_CLIENTTOOL` | Sets the user image. |
| `jellyfin_refresh_item` | `LIBRARY_CLIENTTOOL` | Refreshes metadata for an item. |
| `jellyfin_refresh_library` | `LIBRARY_CLIENTTOOL` | Starts a library scan. |
| `jellyfin_remove_from_collection` | `LIBRARY_CLIENTTOOL` | Removes items from a collection. |
| `jellyfin_remove_item_from_playlist` | `MEDIA_CLIENTTOOL` | Removes items from a playlist. |
| `jellyfin_remove_media_path` | `LIBRARY_CLIENTTOOL` | Remove a media path. |
| `jellyfin_remove_user_from_playlist` | `MEDIA_CLIENTTOOL` | Remove a user from a playlist's users. |
| `jellyfin_remove_user_from_session` | `USER_CLIENTTOOL` | Removes an additional user from a session. |
| `jellyfin_remove_virtual_folder` | `LIBRARY_CLIENTTOOL` | Removes a virtual folder. |
| `jellyfin_rename_virtual_folder` | `LIBRARY_CLIENTTOOL` | Renames a virtual folder. |
| `jellyfin_report_playback_progress` | `MEDIA_CLIENTTOOL` | Reports playback progress within a session. |
| `jellyfin_report_playback_start` | `MEDIA_CLIENTTOOL` | Reports playback has started within a session. |
| `jellyfin_report_playback_stopped` | `MEDIA_CLIENTTOOL` | Reports playback has stopped within a session. |
| `jellyfin_report_session_ended` | `USER_CLIENTTOOL` | Reports that a session has ended. |
| `jellyfin_report_viewing` | `USER_CLIENTTOOL` | Reports that a session is viewing an item. |
| `jellyfin_reset_tuner` | `MEDIA_CLIENTTOOL` | Resets a tv tuner. |
| `jellyfin_restart_application` | `SYSTEM_CLIENTTOOL` | Restarts the application. |
| `jellyfin_revoke_key` | `SYSTEM_CLIENTTOOL` | Remove an api key. |
| `jellyfin_search_remote_lyrics` | `MEDIA_CLIENTTOOL` | Search remote lyrics. |
| `jellyfin_search_remote_subtitles` | `MEDIA_CLIENTTOOL` | Search remote subtitles. |
| `jellyfin_send_full_general_command` | `USER_CLIENTTOOL` | Issues a full general command to a client. |
| `jellyfin_send_general_command` | `USER_CLIENTTOOL` | Issues a general command to a client. |
| `jellyfin_send_message_command` | `USER_CLIENTTOOL` | Issues a command to a client to display a message to the user. |
| `jellyfin_send_playstate_command` | `MEDIA_CLIENTTOOL` | Issues a playstate command to a client. |
| `jellyfin_send_system_command` | `SYSTEM_CLIENTTOOL` | Issues a system command to a client. |
| `jellyfin_set_channel_mapping` | `SYSTEM_CLIENTTOOL` | Set channel mappings. |
| `jellyfin_set_item_image` | `LIBRARY_CLIENTTOOL` | Set item image. |
| `jellyfin_set_item_image_by_index` | `LIBRARY_CLIENTTOOL` | Set item image. |
| `jellyfin_set_remote_access` | `LIBRARY_CLIENTTOOL` | Sets remote access and UPnP. |
| `jellyfin_set_repositories` | `LIBRARY_CLIENTTOOL` | Sets the enabled and existing package repositories. |
| `jellyfin_shutdown_application` | `SYSTEM_CLIENTTOOL` | Shuts down the application. |
| `jellyfin_start_restore_backup` | `SYSTEM_CLIENTTOOL` | Restores to a backup by restarting the server and applying the backup. |
| `jellyfin_start_task` | `SYSTEM_CLIENTTOOL` | Start specified task. |
| `jellyfin_stop_encoding_process` | `MEDIA_CLIENTTOOL` | Stops an active encoding. |
| `jellyfin_stop_task` | `SYSTEM_CLIENTTOOL` | Stop specified task. |
| `jellyfin_sync_play_buffering` | `MEDIA_CLIENTTOOL` | Notify SyncPlay group that member is buffering. |
| `jellyfin_sync_play_create_group` | `MEDIA_CLIENTTOOL` | Create a new SyncPlay group. |
| `jellyfin_sync_play_get_group` | `MEDIA_CLIENTTOOL` | Gets a SyncPlay group by id. |
| `jellyfin_sync_play_get_groups` | `MEDIA_CLIENTTOOL` | Gets all SyncPlay groups. |
| `jellyfin_sync_play_join_group` | `MEDIA_CLIENTTOOL` | Join an existing SyncPlay group. |
| `jellyfin_sync_play_leave_group` | `MEDIA_CLIENTTOOL` | Leave the joined SyncPlay group. |
| `jellyfin_sync_play_move_playlist_item` | `MEDIA_CLIENTTOOL` | Request to move an item in the playlist in SyncPlay group. |
| `jellyfin_sync_play_next_item` | `MEDIA_CLIENTTOOL` | Request next item in SyncPlay group. |
| `jellyfin_sync_play_pause` | `MEDIA_CLIENTTOOL` | Request pause in SyncPlay group. |
| `jellyfin_sync_play_ping` | `SYSTEM_CLIENTTOOL` | Update session ping. |
| `jellyfin_sync_play_previous_item` | `MEDIA_CLIENTTOOL` | Request previous item in SyncPlay group. |
| `jellyfin_sync_play_queue` | `MEDIA_CLIENTTOOL` | Request to queue items to the playlist of a SyncPlay group. |
| `jellyfin_sync_play_ready` | `MEDIA_CLIENTTOOL` | Notify SyncPlay group that member is ready for playback. |
| `jellyfin_sync_play_remove_from_playlist` | `MEDIA_CLIENTTOOL` | Request to remove items from the playlist in SyncPlay group. |
| `jellyfin_sync_play_seek` | `MEDIA_CLIENTTOOL` | Request seek in SyncPlay group. |
| `jellyfin_sync_play_set_ignore_wait` | `MEDIA_CLIENTTOOL` | Request SyncPlay group to ignore member during group-wait. |
| `jellyfin_sync_play_set_new_queue` | `MEDIA_CLIENTTOOL` | Request to set new playlist in SyncPlay group. |
| `jellyfin_sync_play_set_playlist_item` | `MEDIA_CLIENTTOOL` | Request to change playlist item in SyncPlay group. |
| `jellyfin_sync_play_set_repeat_mode` | `MEDIA_CLIENTTOOL` | Request to set repeat mode in SyncPlay group. |
| `jellyfin_sync_play_set_shuffle_mode` | `MEDIA_CLIENTTOOL` | Request to set shuffle mode in SyncPlay group. |
| `jellyfin_sync_play_stop` | `MEDIA_CLIENTTOOL` | Request stop in SyncPlay group. |
| `jellyfin_sync_play_unpause` | `MEDIA_CLIENTTOOL` | Request unpause in SyncPlay group. |
| `jellyfin_tmdb_client_configuration` | `SYSTEM_CLIENTTOOL` | Gets the TMDb image configuration options. |
| `jellyfin_uninstall_plugin` | `SYSTEM_CLIENTTOOL` | Uninstalls a plugin. |
| `jellyfin_uninstall_plugin_by_version` | `SYSTEM_CLIENTTOOL` | Uninstalls a plugin by version. |
| `jellyfin_unmark_favorite_item` | `LIBRARY_CLIENTTOOL` | Unmarks item as a favorite. |
| `jellyfin_update_branding_configuration` | `SYSTEM_CLIENTTOOL` | Updates branding configuration. |
| `jellyfin_update_configuration` | `SYSTEM_CLIENTTOOL` | Updates application configuration. |
| `jellyfin_update_device_options` | `USER_CLIENTTOOL` | Update device options. |
| `jellyfin_update_display_preferences` | `MEDIA_CLIENTTOOL` | Update Display Preferences. |
| `jellyfin_update_initial_configuration` | `SYSTEM_CLIENTTOOL` | Sets the initial startup wizard configuration. |
| `jellyfin_update_item` | `LIBRARY_CLIENTTOOL` | Updates an item. |
| `jellyfin_update_item_content_type` | `LIBRARY_CLIENTTOOL` | Updates an item's content type. |
| `jellyfin_update_item_image_index` | `LIBRARY_CLIENTTOOL` | Updates the index for an item image. |
| `jellyfin_update_item_user_data` | `USER_CLIENTTOOL` | Update Item User Data. |
| `jellyfin_update_library_options` | `LIBRARY_CLIENTTOOL` | Update library options. |
| `jellyfin_update_media_path` | `LIBRARY_CLIENTTOOL` | Updates a media path. |
| `jellyfin_update_named_configuration` | `SYSTEM_CLIENTTOOL` | Updates named configuration. |
| `jellyfin_update_playlist` | `MEDIA_CLIENTTOOL` | Updates a playlist. |
| `jellyfin_update_playlist_user` | `MEDIA_CLIENTTOOL` | Modify a user of a playlist's users. |
| `jellyfin_update_plugin_configuration` | `SYSTEM_CLIENTTOOL` | Updates plugin configuration. |
| `jellyfin_update_series_timer` | `MEDIA_CLIENTTOOL` | Updates a live tv series timer. |
| `jellyfin_update_startup_user` | `USER_CLIENTTOOL` | Sets the user name and password. |
| `jellyfin_update_task` | `SYSTEM_CLIENTTOOL` | Update specified task triggers. |
| `jellyfin_update_timer` | `MEDIA_CLIENTTOOL` | Updates a live tv timer. |
| `jellyfin_update_user` | `USER_CLIENTTOOL` | Updates a user. |
| `jellyfin_update_user_configuration` | `SYSTEM_CLIENTTOOL` | Updates a user configuration. |
| `jellyfin_update_user_item_rating` | `USER_CLIENTTOOL` | Updates a user's rating for an item. |
| `jellyfin_update_user_password` | `USER_CLIENTTOOL` | Updates a user's password. |
| `jellyfin_update_user_policy` | `USER_CLIENTTOOL` | Updates a user policy. |
| `jellyfin_upload_custom_splashscreen` | `SYSTEM_CLIENTTOOL` | Uploads a custom splashscreen. |
| `jellyfin_upload_lyrics` | `MEDIA_CLIENTTOOL` | Upload an external lyric file. |
| `jellyfin_upload_subtitle` | `MEDIA_CLIENTTOOL` | Upload an external subtitle file. |
| `jellyfin_validate_path` | `SYSTEM_CLIENTTOOL` | Validates path. |

</details>

_3 action-routed tool(s) (default) · 368 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/index.md#mcp](docs/index.md#mcp).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

> **Install the slim `[mcp]` extra.** All examples below install
> `jellyfin-mcp[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "jellyfin-mcp[mcp]",
        "jellyfin-mcp"
      ],
      "env": {
        "JELLYFIN_URL": "your_jellyfin_url_here",
        "JELLYFIN_USERNAME": "your_jellyfin_username_here",
        "JELLYFIN_PASSWORD": "your_jellyfin_password_here",
        "JELLYFIN_API_KEY": "your_jellyfin_api_key_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "jellyfin-mcp[mcp]",
        "jellyfin-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "JELLYFIN_URL": "your_jellyfin_url_here",
        "JELLYFIN_USERNAME": "your_jellyfin_username_here",
        "JELLYFIN_PASSWORD": "your_jellyfin_password_here",
        "JELLYFIN_API_KEY": "your_jellyfin_api_key_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "url": "http://localhost:8000/jellyfin-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name jellyfin-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e JELLYFIN_URL="your_value" \
  -e JELLYFIN_USERNAME="your_value" \
  -e JELLYFIN_PASSWORD="your_value" \
  -e JELLYFIN_API_KEY="your_value" \
  knucklessg1/jellyfin-mcp:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `jellyfin-mcp[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `jellyfin-mcp[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `jellyfin-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`jellyfin-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/jellyfin-mcp/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://jellyfin-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export JELLYFIN_URL="your_value"
export JELLYFIN_USERNAME="your_value"
export JELLYFIN_PASSWORD="your_value"
export JELLYFIN_API_KEY="your_value"

# Run the agent server
jellyfin-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  jellyfin-mcp-mcp:
    image: knucklessg1/jellyfin-mcp:mcp
    container_name: jellyfin-mcp-mcp
    hostname: jellyfin-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  jellyfin-mcp-agent:
    image: knucklessg1/jellyfin-mcp:latest
    container_name: jellyfin-mcp-agent
    hostname: jellyfin-mcp-agent
    restart: always
    depends_on:
      - jellyfin-mcp-mcp
    env_file:
      - ../.env
    command: [ "jellyfin-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9056
      - MCP_URL=http://jellyfin-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9056:9056"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9056/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/index.md#a2a-agent](docs/index.md#a2a-agent).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/jellyfin-mcp/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/jellyfin-mcp/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/jellyfin-mcp/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/jellyfin-mcp/usage/) | the MCP tools, the `Api` client, the agent CLI |
| [Backing Platform](https://knuckles-team.github.io/jellyfin-mcp/platform/) | deploy a Jellyfin media server with Docker |
| [Overview](https://knuckles-team.github.io/jellyfin-mcp/overview/) | the agent-package pattern and MCP configuration |
| [Concepts](https://knuckles-team.github.io/jellyfin-mcp/concepts/) | concept registry (`CONCEPT:JELLYFIN-*`) |

---

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `jellyfin-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `jellyfin-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `jellyfin-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "jellyfin-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "jellyfin-mcp[agent]"

# Everything (development)
uv pip install "jellyfin-mcp[all]"      # or: python -m pip install "jellyfin-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/jellyfin-mcp:mcp` | `--target mcp` | `jellyfin-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `jellyfin-mcp` |
| `knucklessg1/jellyfin-mcp:latest` | `--target agent` (default) | `jellyfin-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `jellyfin-agent` |

```bash
docker build --target mcp   -t knucklessg1/jellyfin-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/jellyfin-mcp:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

---

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `DEFAULT_AGENT_NAME` | `"Jellyfin MCP Agent"` | Displayed name of the integrated Graph Agent |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `AUTH_TYPE` | `apiKey` | AUTH_TYPE defines the authorization flow: 'apiKey', 'credentials', or 'delegated' (OIDC) |
| `JELLYFIN_URL` | `http://localhost:8096` | Base Jellyfin server URL |
| `JELLYFIN_API_KEY` | `your_jellyfin_api_key_here` | API key standard input: |
| `JELLYFIN_USERNAME` | `admin` | Credential-based login (used if API key is not provided): |
| `JELLYFIN_PASSWORD` | `your_jellyfin_password_here` |  |
| `JELLYFIN_SSL_VERIFY` | `True` | SSL connection validation (True by default, set to False to bypass local certificate checks) |
| `ENABLE_DELEGATION` | `False` |  |
| `DELEGATED_SCOPES` | `api` |  |
| `JELLYFIN_AUDIENCE` | `https://jellyfin.example.com` |  |
| `OIDC_TOKEN_ENDPOINT` | `https://identity.example.com/oauth2/token` |  |
| `OIDC_CLIENT_ID` | `your-oidc-client-id` |  |
| `OIDC_CLIENT_SECRET` | `your-oidc-client-secret` |  |
| `CONDENSED_JELLYFINTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_25 package + 12 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


Every variable the server reads, grouped by purpose.

### Connection & Credentials (Jellyfin)
| Variable | Description | Default |
|----------|-------------|---------|
| `JELLYFIN_URL` | Base Jellyfin server URL | `http://localhost:8096` |
| `JELLYFIN_API_KEY` | Jellyfin API key | — |
| `JELLYFIN_USERNAME` | Username for the credential login flow | — |
| `JELLYFIN_PASSWORD` | Password for the credential login flow | — |
| `JELLYFIN_SSL_VERIFY` | TLS verification | `True` |
| `AUTH_TYPE` | Auth flow: `apiKey`, `credentials`, or `delegated` (OIDC) | `apiKey` |

### OIDC / token delegation (RFC 8693)
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_DELEGATION` | Flow the caller's IdP token through to Jellyfin | `False` |
| `DELEGATED_SCOPES` | OIDC delegation scopes | `api` |
| `JELLYFIN_AUDIENCE` | OIDC delegation token audience | — |
| `OIDC_TOKEN_ENDPOINT` / `OIDC_CLIENT_ID` / `OIDC_CLIENT_SECRET` | OIDC delegation IdP config | — |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |

### Agent runtime (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_AGENT_NAME` | Display name of the integrated Graph Agent | `Jellyfin MCP Agent` |
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Tool toggles
The action-routed tools share one toggle env var, `CONDENSED_JELLYFINTOOL` (set to `false`
to disable). See the [Available MCP Tools](#available-mcp-tools) table above.

See [`.env.example`](.env.example) for a copy-paste starting point.

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `jellyfin-mcp` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx jellyfin-mcp` · or `uv tool install jellyfin-mcp` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/jellyfin-mcp:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
