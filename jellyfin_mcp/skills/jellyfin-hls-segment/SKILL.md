---
name: jellyfin-hls-segment
description: "Generated skill for HlsSegment operations. Contains 5 tools."
---

### Overview
This skill handles operations related to HlsSegment.

### Available Tools
- `get_hls_audio_segment_legacy_aac_tool`: Gets the specified audio segment for an audio item.
  - **Parameters**:
    - `item_id` (str)
    - `segment_id` (str)
- `get_hls_audio_segment_legacy_mp3_tool`: Gets the specified audio segment for an audio item.
  - **Parameters**:
    - `item_id` (str)
    - `segment_id` (str)
- `get_hls_video_segment_legacy_tool`: Gets a hls video segment.
  - **Parameters**:
    - `item_id` (str)
    - `playlist_id` (str)
    - `segment_id` (str)
    - `segment_container` (str)
- `get_hls_playlist_legacy_tool`: Gets a hls video playlist.
  - **Parameters**:
    - `item_id` (str)
    - `playlist_id` (str)
- `stop_encoding_process_tool`: Stops an active encoding.
  - **Parameters**:
    - `device_id` (Optional[str])
    - `play_session_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
