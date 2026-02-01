---
name: jellyfin-system
description: "Generated skill for System operations. Contains 10 tools."
---

### Overview
This skill handles operations related to System.

### Available Tools
- `get_endpoint_info_tool`: Gets information about the request endpoint.
- `get_system_info_tool`: Gets information about the server.
- `get_public_system_info_tool`: Gets public information about the server.
- `get_system_storage_tool`: Gets information about the server.
- `get_server_logs_tool`: Gets a list of available server log files.
- `get_log_file_tool`: Gets a log file.
  - **Parameters**:
    - `name` (Optional[str])
- `get_ping_system_tool`: Pings the system.
- `post_ping_system_tool`: Pings the system.
- `restart_application_tool`: Restarts the application.
- `shutdown_application_tool`: Shuts down the application.

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
