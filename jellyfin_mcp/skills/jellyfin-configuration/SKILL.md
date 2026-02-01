---
name: jellyfin-configuration
description: "Generated skill for Configuration operations. Contains 6 tools."
---

### Overview
This skill handles operations related to Configuration.

### Available Tools
- `get_configuration_tool`: Gets application configuration.
- `update_configuration_tool`: Updates application configuration.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_named_configuration_tool`: Gets a named configuration.
  - **Parameters**:
    - `key` (str)
- `update_named_configuration_tool`: Updates named configuration.
  - **Parameters**:
    - `key` (str)
    - `body` (Optional[Dict[str, Any]])
- `update_branding_configuration_tool`: Updates branding configuration.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_default_metadata_options_tool`: Gets a default MetadataOptions object.

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
