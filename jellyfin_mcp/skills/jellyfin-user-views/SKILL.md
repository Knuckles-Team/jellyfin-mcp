---
name: jellyfin-user-views
description: "Generated skill for UserViews operations. Contains 2 tools."
---

### Overview
This skill handles operations related to UserViews.

### Available Tools
- `get_user_views_tool`: Get user views.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `include_external_content` (Optional[bool])
    - `preset_views` (Optional[List[Any]])
    - `include_hidden` (Optional[bool])
- `get_grouping_options_tool`: Get user view grouping options.
  - **Parameters**:
    - `user_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
