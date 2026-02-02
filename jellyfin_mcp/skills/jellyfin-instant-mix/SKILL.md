---
name: jellyfin-instant-mix
description: "Generated skill for InstantMix operations. Contains 8 tools."
---

### Overview
This skill handles operations related to InstantMix.

### Available Tools
- `get_instant_mix_from_album_tool`: Creates an instant playlist based on a given album.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `get_instant_mix_from_artists_tool`: Creates an instant playlist based on a given artist.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `get_instant_mix_from_artists2_tool`: Creates an instant playlist based on a given artist.
  - **Parameters**:
    - `id` (Optional[str])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `get_instant_mix_from_item_tool`: Creates an instant playlist based on a given item.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `get_instant_mix_from_music_genre_by_name_tool`: Creates an instant playlist based on a given genre.
  - **Parameters**:
    - `name` (str)
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `get_instant_mix_from_music_genre_by_id_tool`: Creates an instant playlist based on a given genre.
  - **Parameters**:
    - `id` (Optional[str])
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `get_instant_mix_from_playlist_tool`: Creates an instant playlist based on a given playlist.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])
- `get_instant_mix_from_song_tool`: Creates an instant playlist based on a given song.
  - **Parameters**:
    - `item_id` (str)
    - `user_id` (Optional[str])
    - `limit` (Optional[int])
    - `fields` (Optional[List[Any]])
    - `enable_images` (Optional[bool])
    - `enable_user_data` (Optional[bool])
    - `image_type_limit` (Optional[int])
    - `enable_image_types` (Optional[List[Any]])

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
