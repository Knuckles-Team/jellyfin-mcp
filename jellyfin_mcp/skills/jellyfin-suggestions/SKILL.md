---
name: jellyfin-suggestions
description: "Generated skill for Suggestions operations. Contains 1 tools."
---

### Overview
This skill handles operations related to Suggestions.

### Available Tools
- `get_suggestions_tool`: Gets suggestions.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `media_type` (Optional[List[Any]])
    - `type` (Optional[List[Any]])
    - `start_index` (Optional[int])
    - `limit` (Optional[int])
    - `enable_total_record_count` (Optional[bool])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
