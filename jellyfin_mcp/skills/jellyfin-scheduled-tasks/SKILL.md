---
name: jellyfin-scheduled-tasks
description: "Generated skill for ScheduledTasks operations. Contains 5 tools."
---

### Overview
This skill handles operations related to ScheduledTasks.

### Available Tools
- `get_tasks_tool`: Get tasks.
  - **Parameters**:
    - `is_hidden` (Optional[bool])
    - `is_enabled` (Optional[bool])
- `get_task_tool`: Get task by id.
  - **Parameters**:
    - `task_id` (str)
- `update_task_tool`: Update specified task triggers.
  - **Parameters**:
    - `task_id` (str)
    - `body` (Optional[Dict[str, Any]])
- `start_task_tool`: Start specified task.
  - **Parameters**:
    - `task_id` (str)
- `stop_task_tool`: Stop specified task.
  - **Parameters**:
    - `task_id` (str)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
