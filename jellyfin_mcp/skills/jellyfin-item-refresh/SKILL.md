---
name: jellyfin-item-refresh
description: "Generated skill for ItemRefresh operations. Contains 1 tools."
---

### Overview
This skill handles operations related to ItemRefresh.

### Available Tools
- `refresh_item_tool`: Refreshes metadata for an item.
  - **Parameters**:
    - `item_id` (str)
    - `metadata_refresh_mode` (Optional[str])
    - `image_refresh_mode` (Optional[str])
    - `replace_all_metadata` (Optional[bool])
    - `replace_all_images` (Optional[bool])
    - `regenerate_trickplay` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
