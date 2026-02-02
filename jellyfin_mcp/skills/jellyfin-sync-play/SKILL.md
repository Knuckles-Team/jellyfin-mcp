---
name: jellyfin-sync-play
description: "Generated skill for SyncPlay operations. Contains 22 tools."
---

### Overview
This skill handles operations related to SyncPlay.

### Available Tools
- `sync_play_get_group_tool`: Gets a SyncPlay group by id.
  - **Parameters**:
    - `id` (str)
- `sync_play_buffering_tool`: Notify SyncPlay group that member is buffering.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_join_group_tool`: Join an existing SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_leave_group_tool`: Leave the joined SyncPlay group.
- `sync_play_get_groups_tool`: Gets all SyncPlay groups.
- `sync_play_move_playlist_item_tool`: Request to move an item in the playlist in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_create_group_tool`: Create a new SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_next_item_tool`: Request next item in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_pause_tool`: Request pause in SyncPlay group.
- `sync_play_ping_tool`: Update session ping.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_previous_item_tool`: Request previous item in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_queue_tool`: Request to queue items to the playlist of a SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_ready_tool`: Notify SyncPlay group that member is ready for playback.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_remove_from_playlist_tool`: Request to remove items from the playlist in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_seek_tool`: Request seek in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_set_ignore_wait_tool`: Request SyncPlay group to ignore member during group-wait.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_set_new_queue_tool`: Request to set new playlist in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_set_playlist_item_tool`: Request to change playlist item in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_set_repeat_mode_tool`: Request to set repeat mode in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_set_shuffle_mode_tool`: Request to set shuffle mode in SyncPlay group.
  - **Parameters**:
    - `body` (Optional[Dict[str, Any]])
- `sync_play_stop_tool`: Request stop in SyncPlay group.
- `sync_play_unpause_tool`: Request unpause in SyncPlay group.

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
