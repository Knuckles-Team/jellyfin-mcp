---
name: jellyfin-trickplay
description: "Generated skill for Trickplay operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Trickplay.

### Available Tools
- `get_trickplay_tile_image_tool`: Gets a trickplay tile image.
  - **Parameters**:
    - `item_id` (str)
    - `width` (int)
    - `index` (int)
    - `media_source_id` (Optional[str])
- `get_trickplay_hls_playlist_tool`: Gets an image tiles playlist for trickplay.
  - **Parameters**:
    - `item_id` (str)
    - `width` (int)
    - `media_source_id` (Optional[str])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
