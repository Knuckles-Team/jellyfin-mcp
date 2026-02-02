---
name: jellyfin-filter
description: "Generated skill for Filter operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Filter.

### Available Tools
- `get_query_filters_legacy_tool`: Gets legacy query filters.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `parent_id` (Optional[str])
    - `include_item_types` (Optional[List[Any]])
    - `media_types` (Optional[List[Any]])
- `get_query_filters_tool`: Gets query filters.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `parent_id` (Optional[str])
    - `include_item_types` (Optional[List[Any]])
    - `is_airing` (Optional[bool])
    - `is_movie` (Optional[bool])
    - `is_sports` (Optional[bool])
    - `is_kids` (Optional[bool])
    - `is_news` (Optional[bool])
    - `is_series` (Optional[bool])
    - `recursive` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
