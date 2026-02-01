---
name: jellyfin-movies
description: "Generated skill for Movies operations. Contains 1 tools."
---

### Overview
This skill handles operations related to Movies.

### Available Tools
- `get_movie_recommendations_tool`: Gets movie recommendations.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `parent_id` (Optional[str])
    - `fields` (Optional[List[Any]])
    - `category_limit` (Optional[int])
    - `item_limit` (Optional[int])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
