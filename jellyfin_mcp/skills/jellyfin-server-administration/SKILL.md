---
name: jellyfin-server-administration
skill_type: skill
description: >-
  Administer a Jellyfin server via the jellyfin-mcp MCP server - health, scheduled tasks, backups, plugins, users, API keys, Quick Connect, branding and configuration. Use when the agent must check or change the server itself. Do NOT use for browsing media (use `jellyfin-library-catalog`), playback (use `jellyfin-media-playback`) or live TV (use `jellyfin-live-tv`).
license: MIT
tags: [jellyfin, media, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Jellyfin Server Administration

Operate the server through typed `jellyfin_*` tools. Read first; every delete, revoke, uninstall, restart and restore needs the operator's approval.

## Workflows

### jellyfin-server-health-check
Read server identity, storage, task state and recent log entries.

1. `jellyfin_get_system_info` (no parameters)
2. `jellyfin_get_system_storage` (no parameters)
3. `jellyfin_get_tasks` (is_enabled, is_hidden)
4. `jellyfin_get_log_entries` (limit, min_date)

### jellyfin-backup-server
List backups, create one, and confirm it appears.

1. `jellyfin_list_backups` (no parameters)
2. `jellyfin_create_backup` (body) - needs the operator's approval.
3. `jellyfin_list_backups` (no parameters)

### jellyfin-quick-connect-sign-in
Approve a Quick Connect sign-in code for a user.

1. `jellyfin_get_quick_connect_enabled` (no parameters)
2. `jellyfin_authorize_quick_connect` (code, user_id) - needs the operator's approval.

### jellyfin-create-user
Create a user and set the policy the household role needs.

1. `jellyfin_get_users` (is_disabled, is_hidden)
2. `jellyfin_create_user_by_name` (body) - needs the operator's approval.
3. `jellyfin_update_user_policy` (user_id, body) - needs the operator's approval.

### jellyfin-install-plugin
Pick a catalog package, install it, and confirm the plugin list.

1. `jellyfin_get_packages` (no parameters)
2. `jellyfin_install_package` (name, assembly_guid, version, repository_url) - needs the operator's approval.
3. `jellyfin_get_plugins` (no parameters)


## When NOT to use
- Media browsing, playlists and watch state: `jellyfin-library-catalog`, `jellyfin-media-playback`.
- Tuners and recordings: `jellyfin-live-tv`.

## Environment
`JELLYFIN_URL` is the server base URL and `JELLYFIN_API_KEY` an administrator API key; read both from the credential store.

## Tools

`jellyfin_authenticate_user_by_name`, `jellyfin_authenticate_with_quick_connect`, `jellyfin_authorize_quick_connect`, `jellyfin_cancel_package_installation`, `jellyfin_complete_wizard`, `jellyfin_create_backup`, `jellyfin_create_key`, `jellyfin_create_user_by_name`, `jellyfin_delete_user`, `jellyfin_delete_user_item_rating`, `jellyfin_disable_plugin`, `jellyfin_enable_plugin`, `jellyfin_forgot_password`, `jellyfin_forgot_password_pin`, `jellyfin_get_auth_providers`, `jellyfin_get_backup`, `jellyfin_get_branding_css`, `jellyfin_get_branding_css_2`, `jellyfin_get_branding_options`, `jellyfin_get_configuration`, `jellyfin_get_configuration_pages`, `jellyfin_get_countries`, `jellyfin_get_cultures`, `jellyfin_get_current_user`, `jellyfin_get_dashboard_configuration_page`, `jellyfin_get_default_directory_browser`, `jellyfin_get_default_metadata_options`, `jellyfin_get_directory_contents`, `jellyfin_get_drives`, `jellyfin_get_endpoint_info`, `jellyfin_get_fallback_font`, `jellyfin_get_fallback_font_list`, `jellyfin_get_first_user`, `jellyfin_get_first_user_2`, `jellyfin_get_grouping_options`, `jellyfin_get_item_user_data`, `jellyfin_get_keys`, `jellyfin_get_localization_options`, `jellyfin_get_log_entries`, `jellyfin_get_log_file`, `jellyfin_get_named_configuration`, `jellyfin_get_network_shares`, `jellyfin_get_package_info`, `jellyfin_get_packages`, `jellyfin_get_parent_path`, `jellyfin_get_parental_ratings`, `jellyfin_get_password_reset_providers`, `jellyfin_get_ping_system`, `jellyfin_get_plugin_configuration`, `jellyfin_get_plugin_manifest`, `jellyfin_get_plugins`, `jellyfin_get_public_system_info`, `jellyfin_get_public_users`, `jellyfin_get_quick_connect_enabled`, `jellyfin_get_quick_connect_state`, `jellyfin_get_repositories`, `jellyfin_get_server_logs`, `jellyfin_get_startup_configuration`, `jellyfin_get_system_info`, `jellyfin_get_system_storage`, `jellyfin_get_task`, `jellyfin_get_tasks`, `jellyfin_get_user_by_id`, `jellyfin_get_user_views`, `jellyfin_get_users`, `jellyfin_get_utc_time`, `jellyfin_initiate_quick_connect`, `jellyfin_install_package`, `jellyfin_list_backups`, `jellyfin_log_file`, `jellyfin_post_ping_system`, `jellyfin_restart_application`, `jellyfin_revoke_key`, `jellyfin_send_system_command`, `jellyfin_set_remote_access`, `jellyfin_set_repositories`, `jellyfin_shutdown_application`, `jellyfin_start_restore_backup`, `jellyfin_start_task`, `jellyfin_stop_task`, `jellyfin_tmdb_client_configuration`, `jellyfin_uninstall_plugin`, `jellyfin_uninstall_plugin_by_version`, `jellyfin_update_branding_configuration`, `jellyfin_update_configuration`, `jellyfin_update_initial_configuration`, `jellyfin_update_item_user_data`, `jellyfin_update_named_configuration`, `jellyfin_update_plugin_configuration`, `jellyfin_update_startup_user`, `jellyfin_update_task`, `jellyfin_update_user`, `jellyfin_update_user_configuration`, `jellyfin_update_user_item_rating`, `jellyfin_update_user_password`, `jellyfin_update_user_policy`, `jellyfin_validate_path`
