---
name: jellyfin-years
description: "Generated skill for Years operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Years.

### Available Tools
- `get_years_tool`: Get years.
  - **Parameters**:
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `sort_order` (Optional[List[Any]])
    - `parent_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `exclude_item_types` (Optional[List[Any]])
    - `include_item_types` (Optional[List[Any]])
    - `media_types` (Optional[List[Any]])
    - `sort_by` (Optional[List[Any]])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `recursive` (Optional[bool])
    - `enable_images` (Optional[bool])
- `get_year_tool`: Gets a year.
  - **Parameters**:
    - `year` (int)
    - `user_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
