---
name: jellyfin-artists
description: "Generated skill for Artists operations. Contains 3 tools."
---

### Overview
This skill handles operations related to Artists.

### Available Tools
- `get_artists_tool`: Gets all artists from a given item, folder, or the entire library.
  - **Parameters**:
    - `min_community_rating` (Optional[float])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `search_term` (Optional[str])
    - `parent_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `exclude_item_types` (Optional[List[Any]])
    - `include_item_types` (Optional[List[Any]])
    - `filters` (Optional[List[Any]])
    - `is_favorite` (Optional[bool])
    - `media_types` (Optional[List[Any]])
    - `genres` (Optional[List[Any]])
    - `genre_ids` (Optional[List[Any]])
    - `official_ratings` (Optional[List[Any]])
    - `tags` (Optional[List[Any]])
    - `years` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `person` (Optional[str])
    - `person_ids` (Optional[List[Any]])
    - `person_types` (Optional[List[Any]])
    - `studios` (Optional[List[Any]])
    - `studio_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `name_starts_with_or_greater` (Optional[str])
    - `name_starts_with` (Optional[str])
    - `name_less_than` (Optional[str])
    - `sort_by` (Optional[List[Any]])
    - `sort_order` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_total_record_count` (Optional[bool])
- `get_artist_by_name_tool`: Gets an artist by name.
  - **Parameters**:
    - `name` (str)
    - `user_id` (Optional[str])
- `get_album_artists_tool`: Gets all album artists from a given item, folder, or the entire library.
  - **Parameters**:
    - `min_community_rating` (Optional[float])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `search_term` (Optional[str])
    - `parent_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `exclude_item_types` (Optional[List[Any]])
    - `include_item_types` (Optional[List[Any]])
    - `filters` (Optional[List[Any]])
    - `is_favorite` (Optional[bool])
    - `media_types` (Optional[List[Any]])
    - `genres` (Optional[List[Any]])
    - `genre_ids` (Optional[List[Any]])
    - `official_ratings` (Optional[List[Any]])
    - `tags` (Optional[List[Any]])
    - `years` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `person` (Optional[str])
    - `person_ids` (Optional[List[Any]])
    - `person_types` (Optional[List[Any]])
    - `studios` (Optional[List[Any]])
    - `studio_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `name_starts_with_or_greater` (Optional[str])
    - `name_starts_with` (Optional[str])
    - `name_less_than` (Optional[str])
    - `sort_by` (Optional[List[Any]])
    - `sort_order` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_total_record_count` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
