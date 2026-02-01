---
name: jellyfin-startup
description: "Generated skill for Startup operations. Contains 7 tools."
---

### Overview
This skill handles operations related to Startup.

### Available Tools
- `complete_wizard_tool`: Completes the startup wizard.
- `get_startup_configuration_tool`: Gets the initial startup wizard configuration.
- `update_initial_configuration_tool`: Sets the initial startup wizard configuration.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_first_user_2_tool`: Gets the first user.
- `set_remote_access_tool`: Sets remote access and UPnP.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_first_user_tool`: Gets the first user.
- `update_startup_user_tool`: Sets the user name and password.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
