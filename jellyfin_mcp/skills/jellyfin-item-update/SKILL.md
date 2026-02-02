---
name: jellyfin-item-update
description: "Generated skill for ItemUpdate operations. Contains 3 tools."
---

### Overview
This skill handles operations related to ItemUpdate.

### Available Tools
- `update_item_tool`: Updates an item.
  - **Parameters**:
    - `item_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `update_item_content_type_tool`: Updates an item's content type.
  - **Parameters**:
    - `item_id` (str)
    - `content_type` (Optional[str])
- `get_metadata_editor_info_tool`: Gets metadata editor info for an item.
  - **Parameters**:
    - `item_id` (str)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
