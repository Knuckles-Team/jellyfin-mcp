---
name: jellyfin-backup
description: "Generated skill for Backup operations. Contains 4 tools."
---

### Overview
This skill handles operations related to Backup.

### Available Tools
- `list_backups_tool`: Gets a list of all currently present backups in the backup directory.
- `create_backup_tool`: Creates a new Backup.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_backup_tool`: Gets the descriptor from an existing archive is present.
  - **Parameters**:
    - `path` (Optional[str])
- `start_restore_backup_tool`: Restores to a backup by restarting the server and applying the backup.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
