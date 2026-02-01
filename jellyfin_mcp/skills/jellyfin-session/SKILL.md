---
name: jellyfin-session
description: "Generated skill for Session operations. Contains 16 tools."
---

### Overview
This skill handles operations related to Session.

### Available Tools
- `get_password_reset_providers_tool`: Get all password reset providers.
- `get_auth_providers_tool`: Get all auth providers.
- `get_sessions_tool`: Gets a list of sessions.
  - **Parameters**:
    - `controllable_by_user_id` (Optional[str])
    - `device_id` (Optional[str])
    - `active_within_seconds` (Optional[int])
- `send_full_general_command_tool`: Issues a full general command to a client.
  - **Parameters**:
    - `session_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `send_general_command_tool`: Issues a general command to a client.
  - **Parameters**:
    - `session_id` (str)
    - `command` (str)
- `send_message_command_tool`: Issues a command to a client to display a message to the user.
  - **Parameters**:
    - `session_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `play_tool`: Instructs a session to play an item.
  - **Parameters**:
    - `session_id` (str)
    - `play_command` (Optional[str])
    - `item_ids` (Optional[List[Any]])
    - `start_position_ticks` (Optional[int])
    - `media_source_id` (Optional[str])
    - `audio_stream_index` (Optional[int])
    - `subtitle_stream_index` (Optional[int])
    - `start_index` (Optional[int])
- `send_playstate_command_tool`: Issues a playstate command to a client.
  - **Parameters**:
    - `session_id` (str)
    - `command` (str)
    - `seek_position_ticks` (Optional[int])
    - `controlling_user_id` (Optional[str])
- `send_system_command_tool`: Issues a system command to a client.
  - **Parameters**:
    - `session_id` (str)
    - `command` (str)
- `add_user_to_session_tool`: Adds an additional user to a session.
  - **Parameters**:
    - `session_id` (str)
    - `user_id` (str)
- `remove_user_from_session_tool`: Removes an additional user from a session.
  - **Parameters**:
    - `session_id` (str)
    - `user_id` (str)
- `display_content_tool`: Instructs a session to browse to an item or view.
  - **Parameters**:
    - `session_id` (str)
    - `item_type` (Optional[str])
    - `item_id` (Optional[str])
    - `item_name` (Optional[str])
- `post_capabilities_tool`: Updates capabilities for a device.
  - **Parameters**:
    - `id` (Optional[str])
    - `playable_media_types` (Optional[List[Any]])
    - `supported_commands` (Optional[List[Any]])
    - `supports_media_control` (Optional[bool])
    - `supports_persistent_identifier` (Optional[bool])
- `post_full_capabilities_tool`: Updates capabilities for a device.
  - **Parameters**:
    - `id` (Optional[str])
    - `body` (Optional[Dict[str, Any]])
- `report_session_ended_tool`: Reports that a session has ended.
- `report_viewing_tool`: Reports that a session is viewing an item.
  - **Parameters**:
    - `session_id` (Optional[str])
    - `item_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
