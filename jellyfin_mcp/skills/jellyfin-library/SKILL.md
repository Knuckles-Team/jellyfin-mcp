---
name: jellyfin-library
description: "Generated skill for Library operations. Contains 25 tools."
---

### Overview
This skill handles operations related to Library.

### Available Tools
- `delete_items_tool`: Deletes items from the library and filesystem.
  - **Parameters**:
    - `ids` (Optional[List[Any]])
- `delete_item_tool`: Deletes an item from the library and filesystem.
  - **Parameters**:
    - `item_id` (str)
- `get_similar_albums_tool`: Gets similar items.
  - **Parameters**:
    - `item_id` (str)
    - `exclude_artist_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
- `get_similar_artists_tool`: Gets similar items.
  - **Parameters**:
    - `item_id` (str)
    - `exclude_artist_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
- `get_ancestors_tool`: Gets all parents of an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
- `get_critic_reviews_tool`: Gets critic review for an item.
  - **Parameters**:
    - `item_id` (str)
- `get_download_tool`: Downloads item media.
  - **Parameters**:
    - `item_id` (str)
- `get_file_tool`: Get the original file of an item.
  - **Parameters**:
    - `item_id` (str)
- `get_similar_items_tool`: Gets similar items.
  - **Parameters**:
    - `item_id` (str)
    - `exclude_artist_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
- `get_theme_media_tool`: Get theme songs and videos for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `inherit_from_parent` (Optional[bool])
    - `sort_by` (Optional[List[Any]])
    - `sort_order` (Optional[List[Any]])
- `get_theme_songs_tool`: Get theme songs for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `inherit_from_parent` (Optional[bool])
    - `sort_by` (Optional[List[Any]])
    - `sort_order` (Optional[List[Any]])
- `get_theme_videos_tool`: Get theme videos for an item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `inherit_from_parent` (Optional[bool])
    - `sort_by` (Optional[List[Any]])
    - `sort_order` (Optional[List[Any]])
- `get_item_counts_tool`: Get item counts.
  - **Parameters**:
    - `user_id` (Optional[str])
    - `is_favorite` (Optional[bool])
- `get_library_options_info_tool`: Gets the library options info.
  - **Parameters**:
    - `library_content_type` (Optional[str])
    - `is_new_library` (Optional[bool])
- `post_updated_media_tool`: Reports that new movies have been added by an external source.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `get_media_folders_tool`: Gets all user media folders.
  - **Parameters**:
    - `is_hidden` (Optional[bool])
- `post_added_movies_tool`: Reports that new movies have been added by an external source.
  - **Parameters**:
    - `tmdb_id` (Optional[str])
    - `imdb_id` (Optional[str])
- `post_updated_movies_tool`: Reports that new movies have been added by an external source.
  - **Parameters**:
    - `tmdb_id` (Optional[str])
    - `imdb_id` (Optional[str])
- `get_physical_paths_tool`: Gets a list of physical paths from virtual folders.
- `refresh_library_tool`: Starts a library scan.
- `post_added_series_tool`: Reports that new episodes of a series have been added by an external source.
  - **Parameters**:
    - `tvdb_id` (Optional[str])
- `post_updated_series_tool`: Reports that new episodes of a series have been added by an external source.
  - **Parameters**:
    - `tvdb_id` (Optional[str])
- `get_similar_movies_tool`: Gets similar items.
  - **Parameters**:
    - `item_id` (str)
    - `exclude_artist_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
- `get_similar_shows_tool`: Gets similar items.
  - **Parameters**:
    - `item_id` (str)
    - `exclude_artist_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
- `get_similar_trailers_tool`: Gets similar items.
  - **Parameters**:
    - `item_id` (str)
    - `exclude_artist_ids` (Optional[List[Any]])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
