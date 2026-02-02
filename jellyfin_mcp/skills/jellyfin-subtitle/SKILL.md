---
name: jellyfin-subtitle
description: "Generated skill for Subtitle operations. Contains 10 tools."
---

### Overview
This skill handles operations related to Subtitle.

### Available Tools
- `get_fallback_font_list_tool`: Gets a list of available fallback font files.
- `get_fallback_font_tool`: Gets a fallback font file.
  - **Parameters**:
    - `name` (str)
- `search_remote_subtitles_tool`: Search remote subtitles.
  - **Parameters**:
    - `item_id` (str)
    - `language` (str)
    - `is_perfect_match` (Optional[bool])
- `download_remote_subtitles_tool`: Downloads a remote subtitle.
  - **Parameters**:
    - `item_id` (str)
    - `subtitle_id` (str)
- `get_remote_subtitles_tool`: Gets the remote subtitles.
  - **Parameters**:
    - `subtitle_id` (str)
- `get_subtitle_playlist_tool`: Gets an HLS subtitle playlist.
  - **Parameters**:
    - `item_id` (str)
    - `index` (int)
    - `media_source_id` (str)
    - `segment_length` (Optional[int])
- `upload_subtitle_tool`: Upload an external subtitle file.
  - **Parameters**:
    - `item_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `delete_subtitle_tool`: Deletes an external subtitle file.
  - **Parameters**:
    - `item_id` (str)
    - `index` (int)
- `get_subtitle_with_ticks_tool`: Gets subtitles in a specified format.
  - **Parameters**:
    - `route_item_id` (str)
    - `route_media_source_id` (str)
    - `route_index` (int)
    - `route_start_position_ticks` (int)
    - `route_format` (str)
    - `item_id` (Optional[str])
    - `media_source_id` (Optional[str])
    - `index` (Optional[int])
    - `start_position_ticks` (Optional[int])
    - `format` (Optional[str])
    - `end_position_ticks` (Optional[int])
    - `copy_timestamps` (Optional[bool])
    - `add_vtt_time_map` (Optional[bool])
- `get_subtitle_tool`: Gets subtitles in a specified format.
  - **Parameters**:
    - `route_item_id` (str)
    - `route_media_source_id` (str)
    - `route_index` (int)
    - `route_format` (str)
    - `item_id` (Optional[str])
    - `media_source_id` (Optional[str])
    - `index` (Optional[int])
    - `format` (Optional[str])
    - `end_position_ticks` (Optional[int])
    - `copy_timestamps` (Optional[bool])
    - `add_vtt_time_map` (Optional[bool])
    - `start_position_ticks` (Optional[int])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
