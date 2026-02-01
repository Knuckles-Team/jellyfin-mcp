---
name: jellyfin-remote-image
description: "Generated skill for RemoteImage operations. Contains 3 tools."
---

### Overview
This skill handles operations related to RemoteImage.

### Available Tools
- `get_remote_images_tool`: Gets available remote images for an item.
  - **Parameters**:
    - `item_id` (str)
    - `type` (Optional[str])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `provider_name` (Optional[str])
    - `include_all_languages` (Optional[bool])
- `download_remote_image_tool`: Downloads a remote image for an item.
  - **Parameters**:
    - `item_id` (str)
    - `type` (Optional[str])
    - `image_url` (Optional[str])
- `get_remote_image_providers_tool`: Gets available remote image providers for an item.
  - **Parameters**:
    - `item_id` (str)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
