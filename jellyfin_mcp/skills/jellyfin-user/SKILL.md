---
name: jellyfin-user
description: "Generated skill for User operations. Contains 14 tools."
---

### Overview
This skill handles operations related to User.

### Available Tools
- `get_users_tool`: Gets a list of users.
  - **Parameters**:
    - `is_hidden` (Optional[bool])
    - `is_disabled` (Optional[bool])
- `update_user_tool`: Updates a user.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `body` (Optional[Dict[str, Any]])
- `get_user_by_id_tool`: Gets a user by Id.
  - **Parameters**:
    - `user_id` (str)
- `delete_user_tool`: Deletes a user.
  - **Parameters**:
    - `user_id` (str)
- `update_user_policy_tool`: Updates a user policy.
  - **Parameters**:
    - `user_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `authenticate_user_by_name_tool`: Authenticates a user by name.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `authenticate_with_quick_connect_tool`: Authenticates a user with quick connect.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `update_user_configuration_tool`: Updates a user configuration.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `body` (Optional[Dict[str, Any]])
- `forgot_password_tool`: Initiates the forgot password process for a local user.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `forgot_password_pin_tool`: Redeems a forgot password pin.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_current_user_tool`: Gets the user based on auth token.
- `create_user_by_name_tool`: Creates a user.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `update_user_password_tool`: Updates a user's password.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `body` (Optional[Dict[str, Any]])
- `get_public_users_tool`: Gets a list of publicly visible users for display on a login screen.

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
