---
name: jellyfin-media-info
description: "Generated skill for MediaInfo operations. Contains 5 tools."
---

### Overview
This skill handles operations related to MediaInfo.

### Available Tools
- `get_playback_info_tool`: Gets live playback media info for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `get_posted_playback_info_tool`: Gets live playback media info for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `max_streaming_bitrate` (Optional[int])
    - `start_time_ticks` (Optional[int])
    - `audio_stream_index` (Optional[int])
    - `subtitle_stream_index` (Optional[int])
    - `max_audio_channels` (Optional[int])
    - `media_source_id` (Optional[str])
    - `live_stream_id` (Optional[str])
    - `auto_open_live_stream` (Optional[bool])
    - `enable_direct_play` (Optional[bool])
    - `enable_direct_stream` (Optional[bool])
    - `enable_transcoding` (Optional[bool])
    - `allow_video_stream_copy` (Optional[bool])
    - `allow_audio_stream_copy` (Optional[bool])
    - `body` (Optional[Dict[str, Any]])
- `close_live_stream_tool`: Closes a media source.
  - **Parameters**:
    - `live_stream_id` (Optional[str])
- `open_live_stream_tool`: Opens a media source.
  - **Parameters**:
    - `open_token` (Optional[str])
    - `user_id` (Optional[str])
    - `play_session_id` (Optional[str])
    - `max_streaming_bitrate` (Optional[int])
    - `start_time_ticks` (Optional[int])
    - `audio_stream_index` (Optional[int])
    - `subtitle_stream_index` (Optional[int])
    - `max_audio_channels` (Optional[int])
    - `item_id` (Optional[str])
    - `enable_direct_play` (Optional[bool])
    - `enable_direct_stream` (Optional[bool])
    - `always_burn_in_subtitle_when_transcoding` (Optional[bool])
    - `body` (Optional[Dict[str, Any]])
- `get_bitrate_test_bytes_tool`: Tests the network with a request with the size of the bitrate.
  - **Parameters**:
    - `size` (Optional[int])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
