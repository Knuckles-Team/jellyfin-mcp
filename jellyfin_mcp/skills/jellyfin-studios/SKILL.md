---
name: jellyfin-studios
description: "Generated skill for Studios operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Studios.

### Available Tools
- `get_studios_tool`: Gets all studios from a given item, folder, or the entire library.
  - **Parameters**:
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `search_term` (Optional[str])
    - `parent_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `exclude_item_types` (Optional[List[Any]])
    - `include_item_types` (Optional[List[Any]])
    - `is_favorite` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `name_starts_with_or_greater` (Optional[str])
    - `name_starts_with` (Optional[str])
    - `name_less_than` (Optional[str])
    - `enable_images` (Optional[bool])
    - `enable_total_record_count` (Optional[bool])
- `get_studio_tool`: Gets a studio by name.
  - **Parameters**:
    - `name` (str)
    - `user_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
