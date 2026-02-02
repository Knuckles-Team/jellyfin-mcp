---
name: jellyfin-user-library
description: "Generated skill for UserLibrary operations. Contains 10 tools."
---

### Overview
This skill handles operations related to UserLibrary.

### Available Tools
- `get_item_tool`: Gets an item from a user's library.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `get_intros_tool`: Gets intros to play before the main media item plays.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `get_local_trailers_tool`: Gets local trailers for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `get_special_features_tool`: Gets special features for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `get_latest_media_tool`: Gets latest media.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `parent_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `include_item_types` (Optional[List[Any]])
    - `is_played` (Optional[bool])
    - `enable_images` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])
    - `limit` (Optional[int])
    - `group_items` (Optional[bool])
- `get_root_folder_tool`: Gets the root folder from a user's library.
  - **Parameters**:
    - `user_id` (Optional[str])
- `mark_favorite_item_tool`: Marks an item as a favorite.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `unmark_favorite_item_tool`: Unmarks item as a favorite.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `delete_user_item_rating_tool`: Deletes a user's saved personal rating for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `update_user_item_rating_tool`: Updates a user's rating for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `likes` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
