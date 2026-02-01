---
name: jellyfin-persons
description: "Generated skill for Persons operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Persons.

### Available Tools
- `get_persons_tool`: Gets all persons.
  - **Parameters**:
    - `limit` (Optional[int])
    - `search_term` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `filters` (Optional[List[Any]])
    - `is_favorite` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
    - `exclude_person_types` (Optional[List[Any]])
    - `person_types` (Optional[List[Any]])
    - `appears_in_item_id` (Optional[str])
    - `user_id` (Optional[str])
    - `enable_images` (Optional[bool])
- `get_person_tool`: Get person by name.
  - **Parameters**:
    - `name` (str)
    - `user_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
