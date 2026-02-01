---
name: jellyfin-display-preferences
description: "Generated skill for DisplayPreferences operations. Contains 2 tools."
---

### Overview
This skill handles operations related to DisplayPreferences.

### Available Tools
- `get_display_preferences_tool`: Get Display Preferences.
  - **Parameters**:
    - `display_preferences_id` (str)
    - `user_id` (Optional[str])
    - `client` (Optional[str])
- `update_display_preferences_tool`: Update Display Preferences.
  - **Parameters**:
    - `display_preferences_id` (str)
    - `user_id` (Optional[str])
    - `client` (Optional[str])
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
