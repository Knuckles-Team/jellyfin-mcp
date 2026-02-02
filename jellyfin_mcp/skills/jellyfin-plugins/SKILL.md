---
name: jellyfin-plugins
description: "Generated skill for Plugins operations. Contains 9 tools."
---

### Overview
This skill handles operations related to Plugins.

### Available Tools
- `get_plugins_tool`: Gets a list of currently installed plugins.
- `uninstall_plugin_tool`: Uninstalls a plugin.
  - **Parameters**:
    - `plugin_id` (str)
- `uninstall_plugin_by_version_tool`: Uninstalls a plugin by version.
  - **Parameters**:
    - `plugin_id` (str)
    - `version` (str)
- `disable_plugin_tool`: Disable a plugin.
  - **Parameters**:
    - `plugin_id` (str)
    - `version` (str)
- `enable_plugin_tool`: Enables a disabled plugin.
  - **Parameters**:
    - `plugin_id` (str)
    - `version` (str)
- `get_plugin_image_tool`: Gets a plugin's image.
  - **Parameters**:
    - `plugin_id` (str)
    - `version` (str)
- `get_plugin_configuration_tool`: Gets plugin configuration.
  - **Parameters**:
    - `plugin_id` (str)
- `update_plugin_configuration_tool`: Updates plugin configuration.
  - **Parameters**:
    - `plugin_id` (str)
- `get_plugin_manifest_tool`: Gets a plugin's manifest.
  - **Parameters**:
    - `plugin_id` (str)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
