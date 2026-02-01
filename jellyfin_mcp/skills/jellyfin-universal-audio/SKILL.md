---
name: jellyfin-universal-audio
description: "Generated skill for UniversalAudio operations. Contains 1 tools."
---

### Overview
This skill handles operations related to UniversalAudio.

### Available Tools
- `get_universal_audio_stream_tool`: Gets an audio stream.
  - **Parameters**:
    - `item_id` (str)
    - `container` (Optional[List[Any]])
    - `media_source_id` (Optional[str])
    - `device_id` (Optional[str])
    - `user_id` (Optional[str])
    - `audio_codec` (Optional[str])
    - `max_audio_channels` (Optional[int])
    - `transcoding_audio_channels` (Optional[int])
    - `max_streaming_bitrate` (Optional[int])
    - `audio_bit_rate` (Optional[int])
    - `start_time_ticks` (Optional[int])
    - `transcoding_container` (Optional[str])
    - `transcoding_protocol` (Optional[str])
    - `max_audio_sample_rate` (Optional[int])
    - `max_audio_bit_depth` (Optional[int])
    - `enable_remote_media` (Optional[bool])
    - `enable_audio_vbr_encoding` (Optional[bool])
    - `break_on_non_key_frames` (Optional[bool])
    - `enable_redirection` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
