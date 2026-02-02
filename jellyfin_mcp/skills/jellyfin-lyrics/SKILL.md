---
name: jellyfin-lyrics
description: "Generated skill for Lyrics operations. Contains 6 tools."
---

### Overview
This skill handles operations related to Lyrics.

### Available Tools
- `get_lyrics_tool`: Gets an item's lyrics.
  - **Parameters**:
    - `item_id` (str)
- `upload_lyrics_tool`: Upload an external lyric file.
  - **Parameters**:
    - `item_id` (str)
    - `file_name` (Optional[str])
    - `body` (Optional[Dict[str, Any]])
- `delete_lyrics_tool`: Deletes an external lyric file.
  - **Parameters**:
    - `item_id` (str)
- `search_remote_lyrics_tool`: Search remote lyrics.
  - **Parameters**:
    - `item_id` (str)
- `download_remote_lyrics_tool`: Downloads a remote lyric.
  - **Parameters**:
    - `item_id` (str)
    - `lyric_id` (str)
- `get_remote_lyrics_tool`: Gets the remote lyrics.
  - **Parameters**:
    - `lyric_id` (str)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
