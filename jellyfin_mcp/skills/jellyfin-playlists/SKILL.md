---
name: jellyfin-playlists
description: "Generated skill for Playlists operations. Contains 11 tools."
---

### Overview
This skill handles operations related to Playlists.

### Available Tools
- `create_playlist_tool`: Creates a new playlist.
  - **Parameters**:
    - `name` (Optional[str])
    - `ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `media_type` (Optional[str])
    - `body` (Optional[Dict[str, Any]])
- `update_playlist_tool`: Updates a playlist.
  - **Parameters**:
    - `playlist_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `get_playlist_tool`: Get a playlist.
  - **Parameters**:
    - `playlist_id` (str)
- `add_item_to_playlist_tool`: Adds items to a playlist.
  - **Parameters**:
    - `playlist_id` (str)
    - `ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
- `remove_item_from_playlist_tool`: Removes items from a playlist.
  - **Parameters**:
    - `playlist_id` (str)
    - `entry_ids` (Optional[List[Any]])
- `get_playlist_items_tool`: Gets the original items of a playlist.
  - **Parameters**:
    - `playlist_id` (str)
    - `user_id` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `move_item_tool`: Moves a playlist item.
  - **Parameters**:
    - `playlist_id` (str)
    - `item_id` (str)
    - `new_index` (int)
- `get_playlist_users_tool`: Get a playlist's users.
  - **Parameters**:
    - `playlist_id` (str)
- `get_playlist_user_tool`: Get a playlist user.
  - **Parameters**:
    - `playlist_id` (str)
    - `user_id` (str)
- `update_playlist_user_tool`: Modify a user of a playlist's users.
  - **Parameters**:
    - `playlist_id` (str)
    - `user_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `remove_user_from_playlist_tool`: Remove a user from a playlist's users.
  - **Parameters**:
    - `playlist_id` (str)
    - `user_id` (str)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
