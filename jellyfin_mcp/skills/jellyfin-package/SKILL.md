---
name: jellyfin-package
description: "Generated skill for Package operations. Contains 6 tools."
---

### Overview
This skill handles operations related to Package.

### Available Tools
- `get_packages_tool`: Gets available packages.
- `get_package_info_tool`: Gets a package by name or assembly GUID.
  - **Parameters**:
    - `name` (str)
    - `assembly_guid` (Optional[str])
- `install_package_tool`: Installs a package.
  - **Parameters**:
    - `name` (str)
    - `assembly_guid` (Optional[str])
    - `version` (Optional[str])
    - `repository_url` (Optional[str])
- `cancel_package_installation_tool`: Cancels a package installation.
  - **Parameters**:
    - `package_id` (str)
- `get_repositories_tool`: Gets all package repositories.
- `set_repositories_tool`: Sets the enabled and existing package repositories.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
