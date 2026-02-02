---
name: jellyfin-item-lookup
description: "Generated skill for ItemLookup operations. Contains 11 tools."
---

### Overview
This skill handles operations related to ItemLookup.

### Available Tools
- `get_external_id_infos_tool`: Get the item's external id info.
  - **Parameters**:
    - `item_id` (str)
- `apply_search_criteria_tool`: Applies search criteria to an item and refreshes metadata.
  - **Parameters**:
    - `item_id` (str)
    - `replace_all_images` (Optional[bool])
    - `body` (Optional[Dict[str, Any]])
- `get_book_remote_search_results_tool`: Get book remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_box_set_remote_search_results_tool`: Get box set remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_movie_remote_search_results_tool`: Get movie remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_music_album_remote_search_results_tool`: Get music album remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_music_artist_remote_search_results_tool`: Get music artist remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_music_video_remote_search_results_tool`: Get music video remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_person_remote_search_results_tool`: Get person remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_series_remote_search_results_tool`: Get series remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_trailer_remote_search_results_tool`: Get trailer remote search.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
