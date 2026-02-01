---
name: jellyfin-library-structure
description: "Generated skill for LibraryStructure operations. Contains 8 tools."
---

### Overview
This skill handles operations related to LibraryStructure.

### Available Tools
- `get_virtual_folders_tool`: Gets all virtual folders.
- `add_virtual_folder_tool`: Adds a virtual folder.
  - **Parameters**:
    - `name` (Optional[str])
    - `collection_type` (Optional[str])
    - `paths` (Optional[List[Any]])
    - `refresh_library` (Optional[bool])
    - `body` (Optional[Dict[str, Any]])
- `remove_virtual_folder_tool`: Removes a virtual folder.
  - **Parameters**:
    - `name` (Optional[str])
    - `refresh_library` (Optional[bool])
- `update_library_options_tool`: Update library options.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `rename_virtual_folder_tool`: Renames a virtual folder.
  - **Parameters**:
    - `name` (Optional[str])
    - `new_name` (Optional[str])
    - `refresh_library` (Optional[bool])
- `add_media_path_tool`: Add a media path to a library.
  - **Parameters**:
    - `refresh_library` (Optional[bool])
    - `body` (Optional[Dict[str, Any]])
- `remove_media_path_tool`: Remove a media path.
  - **Parameters**:
    - `name` (Optional[str])
    - `path` (Optional[str])
    - `refresh_library` (Optional[bool])
- `update_media_path_tool`: Updates a media path.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
