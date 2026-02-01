---
name: jellyfin-api-key
description: "Generated skill for ApiKey operations. Contains 3 tools."
---

### Overview
This skill handles operations related to ApiKey.

### Available Tools
- `get_keys_tool`: Get all keys.
- `create_key_tool`: Create a new api key.
  - **Parameters**:
    - `app` (Optional[str])
- `revoke_key_tool`: Remove an api key.
  - **Parameters**:
    - `key` (str)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
