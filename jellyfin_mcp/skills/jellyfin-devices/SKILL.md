---
name: jellyfin-devices
description: "Generated skill for Devices operations. Contains 5 tools."
---

### Overview
This skill handles operations related to Devices.

### Available Tools
- `get_devices_tool`: Get Devices.
  - **Parameters**:
    - `user_id` (Optional[str])
- `delete_device_tool`: Deletes a device.
  - **Parameters**:
    - `id` (Optional[str])
- `get_device_info_tool`: Get info for a device.
  - **Parameters**:
    - `id` (Optional[str])
- `get_device_options_tool`: Get options for a device.
  - **Parameters**:
    - `id` (Optional[str])
- `update_device_options_tool`: Update device options.
  - **Parameters**:
    - `id` (Optional[str])
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
