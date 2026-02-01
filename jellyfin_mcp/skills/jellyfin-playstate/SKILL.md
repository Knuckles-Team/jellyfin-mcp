---
name: jellyfin-playstate
description: "Generated skill for Playstate operations. Contains 9 tools."
---

### Overview
This skill handles operations related to Playstate.

### Available Tools
- `on_playback_start_tool`: Reports that a session has begun playing an item.
  - **Parameters**:
    - `item_id` (str)
    - `media_source_id` (Optional[str])
    - `audio_stream_index` (Optional[int])
    - `subtitle_stream_index` (Optional[int])
    - `play_method` (Optional[str])
    - `live_stream_id` (Optional[str])
    - `play_session_id` (Optional[str])
    - `can_seek` (Optional[bool])
- `on_playback_stopped_tool`: Reports that a session has stopped playing an item.
  - **Parameters**:
    - `item_id` (str)
    - `media_source_id` (Optional[str])
    - `next_media_type` (Optional[str])
    - `position_ticks` (Optional[int])
    - `live_stream_id` (Optional[str])
    - `play_session_id` (Optional[str])
- `on_playback_progress_tool`: Reports a session's playback progress.
  - **Parameters**:
    - `item_id` (str)
    - `media_source_id` (Optional[str])
    - `position_ticks` (Optional[int])
    - `audio_stream_index` (Optional[int])
    - `subtitle_stream_index` (Optional[int])
    - `volume_level` (Optional[int])
    - `play_method` (Optional[str])
    - `live_stream_id` (Optional[str])
    - `play_session_id` (Optional[str])
    - `repeat_mode` (Optional[str])
    - `is_paused` (Optional[bool])
    - `is_muted` (Optional[bool])
- `report_playback_start_tool`: Reports playback has started within a session.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `ping_playback_session_tool`: Pings a playback session.
  - **Parameters**:
    - `play_session_id` (Optional[str])
- `report_playback_progress_tool`: Reports playback progress within a session.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `report_playback_stopped_tool`: Reports playback has stopped within a session.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `mark_played_item_tool`: Marks an item as played for user.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `date_played` (Optional[str])
- `mark_unplayed_item_tool`: Marks an item as unplayed for user.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
