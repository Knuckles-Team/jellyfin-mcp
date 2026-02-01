---
name: jellyfin-search
description: "Generated skill for Search operations. Contains 1 tools."
---

### Overview
This skill handles operations related to Search.

### Available Tools
- `get_search_hints_tool`: Gets the search hint result.
  - **Parameters**:
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `user_id` (Optional[str])
    - `search_term` (Optional[str])
    - `include_item_types` (Optional[List[Any]])
    - `exclude_item_types` (Optional[List[Any]])
    - `media_types` (Optional[List[Any]])
    - `parent_id` (Optional[str])
    - `is_movie` (Optional[bool])
    - `is_series` (Optional[bool])
    - `is_news` (Optional[bool])
    - `is_kids` (Optional[bool])
    - `is_sports` (Optional[bool])
    - `include_people` (Optional[bool])
    - `include_media` (Optional[bool])
    - `include_genres` (Optional[bool])
    - `include_studios` (Optional[bool])
    - `include_artists` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
