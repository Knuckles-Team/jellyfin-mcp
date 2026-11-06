---
name: jellyfin-live-tv
skill_type: skill
description: >-
  Manage Jellyfin live TV via the jellyfin-mcp MCP server - tuners, listing providers, the guide, recording timers and finished recordings. Use when the agent must set up live TV, schedule or cancel a recording, or read the guide. Do NOT use for library media (use `jellyfin-library-catalog`) or server settings (use `jellyfin-server-administration`).
license: MIT
tags: [jellyfin, media, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Jellyfin Live Tv

Live TV through typed `jellyfin_*` tools: read the guide, record with timers, clear finished recordings only with approval.

## Workflows

### jellyfin-schedule-recording
Find a guide program and record it with a timer.

1. `jellyfin_get_live_tv_info` (no parameters)
2. `jellyfin_get_programs` (body)
3. `jellyfin_get_default_timer` (program_id)
4. `jellyfin_create_timer` (body) - needs the operator's approval.
5. `jellyfin_get_timers` (is_active, is_scheduled)


## When NOT to use
- Library items and metadata: `jellyfin-library-catalog`.
- Server settings: `jellyfin-server-administration`.

## Environment
`JELLYFIN_URL` is the server base URL and `JELLYFIN_API_KEY` an administrator API key; read both from the credential store.

## Tools

`jellyfin_add_listing_provider`, `jellyfin_add_tuner_host`, `jellyfin_cancel_series_timer`, `jellyfin_cancel_timer`, `jellyfin_close_live_stream`, `jellyfin_create_series_timer`, `jellyfin_create_timer`, `jellyfin_delete_listing_provider`, `jellyfin_delete_recording`, `jellyfin_delete_tuner_host`, `jellyfin_discover_tuners`, `jellyfin_discvover_tuners`, `jellyfin_get_all_channel_features`, `jellyfin_get_channel`, `jellyfin_get_channel_features`, `jellyfin_get_channel_items`, `jellyfin_get_channel_mapping_options`, `jellyfin_get_channels`, `jellyfin_get_default_listing_provider`, `jellyfin_get_default_timer`, `jellyfin_get_guide_info`, `jellyfin_get_latest_channel_items`, `jellyfin_get_lineups`, `jellyfin_get_live_recording_file`, `jellyfin_get_live_stream_file`, `jellyfin_get_live_tv_channels`, `jellyfin_get_live_tv_info`, `jellyfin_get_live_tv_programs`, `jellyfin_get_program`, `jellyfin_get_programs`, `jellyfin_get_recommended_programs`, `jellyfin_get_recording`, `jellyfin_get_recording_folders`, `jellyfin_get_recording_group`, `jellyfin_get_recording_groups`, `jellyfin_get_recordings`, `jellyfin_get_recordings_series`, `jellyfin_get_schedules_direct_countries`, `jellyfin_get_series_timer`, `jellyfin_get_series_timers`, `jellyfin_get_timer`, `jellyfin_get_timers`, `jellyfin_get_tuner_host_types`, `jellyfin_open_live_stream`, `jellyfin_reset_tuner`, `jellyfin_set_channel_mapping`, `jellyfin_update_series_timer`, `jellyfin_update_timer`
