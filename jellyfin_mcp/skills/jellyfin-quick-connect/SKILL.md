---
name: jellyfin-quick-connect
description: "Generated skill for QuickConnect operations. Contains 4 tools."
---

### Overview
This skill handles operations related to QuickConnect.

### Available Tools
- `authorize_quick_connect_tool`: Authorizes a pending quick connect request.
  - **Parameters**:
    - `code` (Optional[str])
    - `user_id` (Optional[str])
- `get_quick_connect_state_tool`: Attempts to retrieve authentication information.
  - **Parameters**:
    - `secret` (Optional[str])
- `get_quick_connect_enabled_tool`: Gets the current quick connect state.
- `initiate_quick_connect_tool`: Initiate a new quick connect request.

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
