---
name: jellyfin-tv-shows
description: "Generated skill for TvShows operations. Contains 4 tools."
---

### Overview
This skill handles operations related to TvShows.

### Available Tools
- `get_episodes_tool`: Gets episodes for a tv season.
  - **Parameters**:
    - `series_id` (str)
    - `user_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `season` (Optional[int])
    - `season_id` (Optional[str])
    - `is_missing` (Optional[bool])
    - `adjacent_to` (Optional[str])
    - `start_item_id` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `enable_images` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])
    - `sort_by` (Optional[str])
- `get_seasons_tool`: Gets seasons for a tv series.
  - **Parameters**:
    - `series_id` (str)
    - `user_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `is_special_season` (Optional[bool])
    - `is_missing` (Optional[bool])
    - `adjacent_to` (Optional[str])
    - `enable_images` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])
- `get_next_up_tool`: Gets a list of next up episodes.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `series_id` (Optional[str])
    - `parent_id` (Optional[str])
    - `enable_images` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])
    - `next_up_date_cutoff` (Optional[str])
    - `enable_total_record_count` (Optional[bool])
    - `disable_first_episode` (Optional[bool])
    - `enable_resumable` (Optional[bool])
    - `enable_rewatching` (Optional[bool])
- `get_upcoming_episodes_tool`: Gets a list of upcoming episodes.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `parent_id` (Optional[str])
    - `enable_images` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
