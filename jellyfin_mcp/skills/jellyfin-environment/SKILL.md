---
name: jellyfin-environment
description: "Generated skill for Environment operations. Contains 6 tools."
---

### Overview
This skill handles operations related to Environment.

### Available Tools
- `get_default_directory_browser_tool`: Get Default directory browser.
- `get_directory_contents_tool`: Gets the contents of a given directory in the file system.
  - **Parameters**:
    - `path` (Optional[str])
    - `include_files` (Optional[bool])
    - `include_directories` (Optional[bool])
- `get_drives_tool`: Gets available drives from the server's file system.
- `get_network_shares_tool`: Gets network paths.
- `get_parent_path_tool`: Gets the parent path of a given path.
  - **Parameters**:
    - `path` (Optional[str])
- `validate_path_tool`: Validates path.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
