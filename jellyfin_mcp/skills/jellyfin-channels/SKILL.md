---
name: jellyfin-channels
description: "Generated skill for Channels operations. Contains 5 tools."
---

### Overview
This skill handles operations related to Channels.

### Available Tools
- `get_channels_tool`: Gets available channels.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `supports_latest_items` (Optional[bool])
    - `supports_media_deletion` (Optional[bool])
    - `is_favorite` (Optional[bool])
- `get_channel_features_tool`: Get channel features.
  - **Parameters**:
    - `channel_id` (str)
- `get_channel_items_tool`: Get channel items.
  - **Parameters**:
    - `channel_id` (str)
    - `folder_id` (Optional[str])
    - `user_id` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `sort_order` (Optional[List[Any]])
    - `filters` (Optional[List[Any]])
    - `sort_by` (Optional[List[Any]])
    - `fields` (Optional[List[Any]])
- `get_all_channel_features_tool`: Get all channel features.
- `get_latest_channel_items_tool`: Gets latest channel items.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `filters` (Optional[List[Any]])
    - `fields` (Optional[List[Any]])
    - `channel_ids` (Optional[List[Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
