---
name: jellyfin-collection
description: "Generated skill for Collection operations. Contains 3 tools."
---

### Overview
This skill handles operations related to Collection.

### Available Tools
- `create_collection_tool`: Creates a new collection.
  - **Parameters**:
    - `name` (Optional[str])
    - `ids` (Optional[List[Any]])
    - `parent_id` (Optional[str])
    - `is_locked` (Optional[bool])
- `add_to_collection_tool`: Adds items to a collection.
  - **Parameters**:
    - `collection_id` (str)
    - `ids` (Optional[List[Any]])
- `remove_from_collection_tool`: Removes items from a collection.
  - **Parameters**:
    - `collection_id` (str)
    - `ids` (Optional[List[Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
