---
name: jellyfin-activity-log
description: "Generated skill for ActivityLog operations. Contains 1 tools."
---

### Overview
This skill handles operations related to ActivityLog.

### Available Tools
- `get_log_entries_tool`: Gets activity log entries.
  - **Parameters**:
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `min_date` (Optional[str])
    - `has_user_id` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
