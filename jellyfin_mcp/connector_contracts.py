"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "jellyfin-find-item",
        (
            ToolStep(
                "jellyfin_get_search_hints",
                params=("search_term", "include_item_types", "limit"),
                result=("SearchHints",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_items",
                params=(
                    "search_term",
                    "include_item_types",
                    "recursive",
                    "limit",
                    "fields",
                ),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_item",
                params=("item_id",),
                result=("Id", "Name", "Type"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Resolve a title to an item id and read the item.",
    ),
    ToolUseContract(
        "jellyfin-add-media-and-scan",
        (
            ToolStep(
                "jellyfin_get_virtual_folders",
                params=(),
                result=("Name", "ItemId", "Locations"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_add_media_path",
                params=("body", "refresh_library"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_refresh_library",
                params=(),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_items",
                params=("parent_id", "recursive", "sort_by", "sort_order", "limit"),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Add a media folder path to a library, rescan, and confirm the new items.",
    ),
    ToolUseContract(
        "jellyfin-mark-watched",
        (
            ToolStep(
                "jellyfin_get_search_hints",
                params=("search_term", "include_item_types", "limit"),
                result=("SearchHints",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_item",
                params=("item_id", "user_id"),
                result=("Id", "UserData"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_mark_played_item",
                params=("item_id", "user_id", "date_played"),
                result=("Played", "PlayCount"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Find an item and mark it played for a user.",
    ),
    ToolUseContract(
        "jellyfin-build-playlist",
        (
            ToolStep(
                "jellyfin_create_playlist",
                params=("name", "ids", "media_type", "user_id"),
                result=("Id",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_add_item_to_playlist",
                params=("playlist_id", "ids", "user_id"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_playlist_items",
                params=("playlist_id", "user_id", "limit"),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Create a playlist, add items and read it back.",
    ),
    ToolUseContract(
        "jellyfin-build-collection",
        (
            ToolStep(
                "jellyfin_get_items",
                params=("search_term", "include_item_types", "recursive", "limit"),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_create_collection",
                params=("name", "ids", "parent_id", "is_locked"),
                result=("Id",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_add_to_collection",
                params=("collection_id", "ids"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_item",
                params=("item_id",),
                result=("Id", "Name"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Create a collection (box set) from items and read it back.",
    ),
    ToolUseContract(
        "jellyfin-fetch-subtitles",
        (
            ToolStep(
                "jellyfin_get_item",
                params=("item_id",),
                result=("Id", "MediaStreams"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_search_remote_subtitles",
                params=("item_id", "language", "is_perfect_match"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_download_remote_subtitles",
                params=("item_id", "subtitle_id"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_item",
                params=("item_id",),
                result=("Id", "MediaStreams"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Search remote subtitle providers for an item and download the best match.",
    ),
    ToolUseContract(
        "jellyfin-refresh-item-metadata",
        (
            ToolStep(
                "jellyfin_get_item",
                params=("item_id",),
                result=("Id", "Name", "ProviderIds"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_refresh_item",
                params=(
                    "item_id",
                    "metadata_refresh_mode",
                    "image_refresh_mode",
                    "replace_all_metadata",
                    "replace_all_images",
                ),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_item",
                params=("item_id",),
                result=("Id", "Name", "ProviderIds"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Re-read the metadata of one item and confirm it.",
    ),
    ToolUseContract(
        "jellyfin-schedule-recording",
        (
            ToolStep(
                "jellyfin_get_live_tv_info",
                params=(),
                result=("Services", "IsEnabled"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_programs",
                params=("body",),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_default_timer",
                params=("program_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_create_timer",
                params=("body",),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_timers",
                params=("is_active", "is_scheduled"),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Find a guide program and record it with a timer.",
    ),
    ToolUseContract(
        "jellyfin-server-health-check",
        (
            ToolStep(
                "jellyfin_get_system_info",
                params=(),
                result=("Version", "ServerName", "OperatingSystem"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_system_storage",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_tasks",
                params=("is_enabled", "is_hidden"),
                result=("Name", "State", "LastExecutionResult"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_log_entries",
                params=("limit", "min_date"),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read server identity, storage, task state and recent log entries.",
    ),
    ToolUseContract(
        "jellyfin-backup-server",
        (
            ToolStep(
                "jellyfin_list_backups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_create_backup",
                params=("body",),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_list_backups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="List backups, create one, and confirm it appears.",
    ),
    ToolUseContract(
        "jellyfin-quick-connect-sign-in",
        (
            ToolStep(
                "jellyfin_get_quick_connect_enabled",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_authorize_quick_connect",
                params=("code", "user_id"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Approve a Quick Connect sign-in code for a user.",
    ),
    ToolUseContract(
        "jellyfin-create-user",
        (
            ToolStep(
                "jellyfin_get_users",
                params=("is_disabled", "is_hidden"),
                result=("Id", "Name"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_create_user_by_name",
                params=("body",),
                result=("Id", "Name"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_user_policy",
                params=("user_id", "body"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Create a user and set the policy the household role needs.",
    ),
    ToolUseContract(
        "jellyfin-install-plugin",
        (
            ToolStep(
                "jellyfin_get_packages",
                params=(),
                result=("name", "guid", "versions"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_install_package",
                params=("name", "assembly_guid", "version", "repository_url"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_plugins",
                params=(),
                result=("Name", "Version", "Status"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Pick a catalog package, install it, and confirm the plugin list.",
    ),
    ToolUseContract(
        "jellyfin-message-session",
        (
            ToolStep(
                "jellyfin_get_sessions",
                params=("active_within_seconds", "device_id"),
                result=("Id", "DeviceName", "UserName"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_send_message_command",
                params=("session_id", "body"),
                result=("status",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Show a message on a client that is signed in.",
    ),
    ToolUseContract(
        "jellyfin-ingest-posters",
        (
            ToolStep(
                "jellyfin_get_items",
                params=("include_item_types", "recursive", "limit"),
                result=("Items",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_ingest_posters",
                params=("item_ids", "image_type"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Push poster images of chosen items into the knowledge graph.",
    ),
    ToolUseContract(
        "jellyfin-manage-backup-restore",
        (
            ToolStep(
                "jellyfin_get_backup",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_list_backups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_create_backup",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_start_restore_backup",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the backup restore tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-collections",
        (
            ToolStep(
                "jellyfin_add_to_collection",
                params=("collection_id", "ids"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_create_collection",
                params=("ids", "is_locked", "name", "parent_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_remove_from_collection",
                params=("collection_id", "confirm", "ids"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the collections tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-favorites-ratings",
        (
            ToolStep(
                "jellyfin_mark_favorite_item",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_unmark_favorite_item",
                params=("confirm", "item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read, then change, the favorites ratings tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-images",
        (
            ToolStep(
                "jellyfin_get_artist_image",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_genre_image",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_genre_image_by_index",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_item_image",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "item_id",
                    "max_height",
                    "max_width",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_item_image2",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "item_id",
                    "max_height",
                    "max_width",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_item_image_by_index",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "item_id",
                    "max_height",
                    "max_width",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_item_image_infos",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_music_genre_image",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_music_genre_image_by_index",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_person_image",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_person_image_by_index",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_plugin_image",
                params=("plugin_id", "version"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_remote_image_providers",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_remote_images",
                params=(
                    "include_all_languages",
                    "item_id",
                    "limit",
                    "provider_name",
                    "start_index",
                    "type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_splashscreen",
                params=("format", "tag"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_studio_image",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_studio_image_by_index",
                params=(
                    "background_color",
                    "blur",
                    "fill_height",
                    "fill_width",
                    "foreground_layer",
                    "format",
                    "height",
                    "image_index",
                    "image_type",
                    "max_height",
                    "max_width",
                    "name",
                    "percent_played",
                    "quality",
                    "tag",
                    "unplayed_count",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_trickplay_tile_image",
                params=("index", "item_id", "media_source_id", "width"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_user_image",
                params=("format", "tag", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_download_remote_image",
                params=("image_url", "item_id", "type"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_post_user_image",
                params=("body", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_set_item_image",
                params=("body", "image_type", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_set_item_image_by_index",
                params=("body", "image_index", "image_type", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_item_image_index",
                params=("image_index", "image_type", "item_id", "new_index"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_upload_custom_splashscreen",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_custom_splashscreen",
                params=("confirm",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_item_image",
                params=("confirm", "image_index", "image_type", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_item_image_by_index",
                params=("confirm", "image_index", "image_type", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_user_image",
                params=("confirm", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the images tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-items",
        (
            ToolStep(
                "jellyfin_get_ancestors",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_item",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_item_counts",
                params=("is_favorite", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_items",
                params=(
                    "adjacent_to",
                    "album_artist_ids",
                    "album_ids",
                    "albums",
                    "artist_ids",
                    "artists",
                    "collapse_box_set_items",
                    "contributing_artist_ids",
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "exclude_artist_ids",
                    "exclude_item_ids",
                    "exclude_item_types",
                    "exclude_location_types",
                    "fields",
                    "filters",
                    "genre_ids",
                    "genres",
                    "has_imdb_id",
                    "has_official_rating",
                    "has_overview",
                    "has_parental_rating",
                    "has_special_feature",
                    "has_subtitles",
                    "has_theme_song",
                    "has_theme_video",
                    "has_tmdb_id",
                    "has_trailer",
                    "has_tvdb_id",
                    "ids",
                    "image_type_limit",
                    "image_types",
                    "include_item_types",
                    "index_number",
                    "is3_d",
                    "is4_k",
                    "is_favorite",
                    "is_hd",
                    "is_kids",
                    "is_locked",
                    "is_missing",
                    "is_movie",
                    "is_news",
                    "is_place_holder",
                    "is_played",
                    "is_series",
                    "is_sports",
                    "is_unaired",
                    "limit",
                    "location_types",
                    "max_height",
                    "max_official_rating",
                    "max_premiere_date",
                    "max_width",
                    "media_types",
                    "min_community_rating",
                    "min_critic_rating",
                    "min_date_last_saved",
                    "min_date_last_saved_for_user",
                    "min_height",
                    "min_official_rating",
                    "min_premiere_date",
                    "min_width",
                    "name_less_than",
                    "name_starts_with",
                    "name_starts_with_or_greater",
                    "official_ratings",
                    "parent_id",
                    "parent_index_number",
                    "person",
                    "person_ids",
                    "person_types",
                    "recursive",
                    "search_term",
                    "series_status",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "studio_ids",
                    "studios",
                    "tags",
                    "user_id",
                    "video_types",
                    "years",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_query_filters",
                params=(
                    "include_item_types",
                    "is_airing",
                    "is_kids",
                    "is_movie",
                    "is_news",
                    "is_series",
                    "is_sports",
                    "parent_id",
                    "recursive",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_query_filters_legacy",
                params=("include_item_types", "media_types", "parent_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_item",
                params=("body", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_delete_item",
                params=("confirm", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_items",
                params=("confirm", "ids"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the items tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-library-admin",
        (
            ToolStep(
                "jellyfin_get_library_options_info",
                params=("is_new_library", "library_content_type"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_media_folders",
                params=("is_hidden",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_physical_paths",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_root_folder",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_virtual_folders",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_add_media_path",
                params=("body", "refresh_library"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_add_virtual_folder",
                params=("body", "collection_type", "name", "paths", "refresh_library"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_ingest_library",
                params=("include_item_types", "limit", "parent_id", "recursive"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_post_added_movies",
                params=("imdb_id", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_post_added_series",
                params=("tvdb_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_post_updated_media",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_post_updated_movies",
                params=("imdb_id", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_post_updated_series",
                params=("tvdb_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_refresh_library",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_library_options",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_media_path",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_remove_media_path",
                params=("confirm", "name", "path", "refresh_library"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_remove_virtual_folder",
                params=("confirm", "name", "refresh_library"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_rename_virtual_folder",
                params=("name", "new_name", "refresh_library"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read, then change, the library admin tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-livetv-recordings",
        (
            ToolStep(
                "jellyfin_get_default_timer",
                params=("program_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_live_recording_file",
                params=("recording_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_recording",
                params=("recording_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_recording_folders",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_recording_group",
                params=("group_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_recording_groups",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_recordings",
                params=(
                    "channel_id",
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "is_in_progress",
                    "is_kids",
                    "is_library_item",
                    "is_movie",
                    "is_news",
                    "is_series",
                    "is_sports",
                    "limit",
                    "series_timer_id",
                    "start_index",
                    "status",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_recordings_series",
                params=(
                    "channel_id",
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "fields",
                    "group_id",
                    "image_type_limit",
                    "is_in_progress",
                    "limit",
                    "series_timer_id",
                    "start_index",
                    "status",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_series_timer",
                params=("timer_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_series_timers",
                params=("sort_by", "sort_order"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_timer",
                params=("timer_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_timers",
                params=("channel_id", "is_active", "is_scheduled", "series_timer_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_create_series_timer",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_create_timer",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_series_timer",
                params=("body", "timer_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_timer",
                params=("body", "timer_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_cancel_series_timer",
                params=("confirm", "timer_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_cancel_timer",
                params=("confirm", "timer_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_recording",
                params=("confirm", "recording_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the livetv recordings tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-livetv-setup",
        (
            ToolStep(
                "jellyfin_discover_tuners",
                params=("new_devices_only",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_all_channel_features",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_channel",
                params=("channel_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_channel_features",
                params=("channel_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_channel_items",
                params=(
                    "channel_id",
                    "fields",
                    "filters",
                    "folder_id",
                    "limit",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_channel_mapping_options",
                params=("provider_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_channels",
                params=(
                    "is_favorite",
                    "limit",
                    "start_index",
                    "supports_latest_items",
                    "supports_media_deletion",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_default_listing_provider",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_guide_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_latest_channel_items",
                params=(
                    "channel_ids",
                    "fields",
                    "filters",
                    "limit",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_lineups",
                params=("country", "id", "location", "type"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_live_stream_file",
                params=("container", "stream_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_live_tv_channels",
                params=(
                    "add_current_program",
                    "enable_favorite_sorting",
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "is_disliked",
                    "is_favorite",
                    "is_kids",
                    "is_liked",
                    "is_movie",
                    "is_news",
                    "is_series",
                    "is_sports",
                    "limit",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "type",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_live_tv_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_live_tv_programs",
                params=(
                    "channel_ids",
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "fields",
                    "genre_ids",
                    "genres",
                    "has_aired",
                    "image_type_limit",
                    "is_airing",
                    "is_kids",
                    "is_movie",
                    "is_news",
                    "is_series",
                    "is_sports",
                    "library_series_id",
                    "limit",
                    "max_end_date",
                    "max_start_date",
                    "min_end_date",
                    "min_start_date",
                    "series_timer_id",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_program",
                params=("program_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_programs",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_recommended_programs",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "fields",
                    "genre_ids",
                    "has_aired",
                    "image_type_limit",
                    "is_airing",
                    "is_kids",
                    "is_movie",
                    "is_news",
                    "is_series",
                    "is_sports",
                    "limit",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_schedules_direct_countries",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_tuner_host_types",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_add_listing_provider",
                params=("body", "pw", "validate_listings", "validate_login"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_add_tuner_host",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_close_live_stream",
                params=("live_stream_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_open_live_stream",
                params=(
                    "always_burn_in_subtitle_when_transcoding",
                    "audio_stream_index",
                    "body",
                    "enable_direct_play",
                    "enable_direct_stream",
                    "item_id",
                    "max_audio_channels",
                    "max_streaming_bitrate",
                    "open_token",
                    "play_session_id",
                    "start_time_ticks",
                    "subtitle_stream_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_set_channel_mapping",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_listing_provider",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_tuner_host",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_discvover_tuners",
                params=("new_devices_only",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_reset_tuner",
                params=("tuner_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the livetv setup tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-lyrics",
        (
            ToolStep(
                "jellyfin_get_lyrics",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_remote_lyrics",
                params=("lyric_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_search_remote_lyrics",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_download_remote_lyrics",
                params=("item_id", "lyric_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_upload_lyrics",
                params=("body", "file_name", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_delete_lyrics",
                params=("confirm", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the lyrics tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-misc",
        (
            ToolStep(
                "jellyfin_get_display_preferences",
                params=("client", "display_preferences_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_ingest_posters",
                params=("image_type", "item_ids"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_display_preferences",
                params=("body", "client", "display_preferences_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read, then change, the misc tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-people-genres-studios",
        (
            ToolStep(
                "jellyfin_get_album_artists",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "exclude_item_types",
                    "fields",
                    "filters",
                    "genre_ids",
                    "genres",
                    "image_type_limit",
                    "include_item_types",
                    "is_favorite",
                    "limit",
                    "media_types",
                    "min_community_rating",
                    "name_less_than",
                    "name_starts_with",
                    "name_starts_with_or_greater",
                    "official_ratings",
                    "parent_id",
                    "person",
                    "person_ids",
                    "person_types",
                    "search_term",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "studio_ids",
                    "studios",
                    "tags",
                    "user_id",
                    "years",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_artist_by_name",
                params=("name", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_artists",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "exclude_item_types",
                    "fields",
                    "filters",
                    "genre_ids",
                    "genres",
                    "image_type_limit",
                    "include_item_types",
                    "is_favorite",
                    "limit",
                    "media_types",
                    "min_community_rating",
                    "name_less_than",
                    "name_starts_with",
                    "name_starts_with_or_greater",
                    "official_ratings",
                    "parent_id",
                    "person",
                    "person_ids",
                    "person_types",
                    "search_term",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "studio_ids",
                    "studios",
                    "tags",
                    "user_id",
                    "years",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_genre",
                params=("genre_name", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_genres",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "exclude_item_types",
                    "fields",
                    "image_type_limit",
                    "include_item_types",
                    "is_favorite",
                    "limit",
                    "name_less_than",
                    "name_starts_with",
                    "name_starts_with_or_greater",
                    "parent_id",
                    "search_term",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_artists",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "item_id",
                    "limit",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_artists2",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "id",
                    "image_type_limit",
                    "limit",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_music_genre_by_id",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "id",
                    "image_type_limit",
                    "limit",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_music_genre_by_name",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "limit",
                    "name",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_music_genre",
                params=("genre_name", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_music_genres",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "exclude_item_types",
                    "fields",
                    "image_type_limit",
                    "include_item_types",
                    "is_favorite",
                    "limit",
                    "name_less_than",
                    "name_starts_with",
                    "name_starts_with_or_greater",
                    "parent_id",
                    "search_term",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_person",
                params=("name", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_persons",
                params=(
                    "appears_in_item_id",
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "exclude_person_types",
                    "fields",
                    "filters",
                    "image_type_limit",
                    "is_favorite",
                    "limit",
                    "person_types",
                    "search_term",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_similar_artists",
                params=("exclude_artist_ids", "fields", "item_id", "limit", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_studio",
                params=("name", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_studios",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "exclude_item_types",
                    "fields",
                    "image_type_limit",
                    "include_item_types",
                    "is_favorite",
                    "limit",
                    "name_less_than",
                    "name_starts_with",
                    "name_starts_with_or_greater",
                    "parent_id",
                    "search_term",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_year",
                params=("user_id", "year"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_years",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "exclude_item_types",
                    "fields",
                    "image_type_limit",
                    "include_item_types",
                    "limit",
                    "media_types",
                    "parent_id",
                    "recursive",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read, then change, the people genres studios tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-playback-reporting",
        (
            ToolStep(
                "jellyfin_ping_playback_session",
                params=("play_session_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_display_content",
                params=("item_id", "item_name", "item_type", "session_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_mark_played_item",
                params=("date_played", "item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_mark_unplayed_item",
                params=("confirm", "item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_on_playback_progress",
                params=(
                    "audio_stream_index",
                    "is_muted",
                    "is_paused",
                    "item_id",
                    "live_stream_id",
                    "media_source_id",
                    "play_method",
                    "play_session_id",
                    "position_ticks",
                    "repeat_mode",
                    "subtitle_stream_index",
                    "volume_level",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_on_playback_start",
                params=(
                    "audio_stream_index",
                    "can_seek",
                    "item_id",
                    "live_stream_id",
                    "media_source_id",
                    "play_method",
                    "play_session_id",
                    "subtitle_stream_index",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_on_playback_stopped",
                params=(
                    "confirm",
                    "item_id",
                    "live_stream_id",
                    "media_source_id",
                    "next_media_type",
                    "play_session_id",
                    "position_ticks",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_play",
                params=(
                    "audio_stream_index",
                    "item_ids",
                    "media_source_id",
                    "play_command",
                    "session_id",
                    "start_index",
                    "start_position_ticks",
                    "subtitle_stream_index",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_report_playback_progress",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_report_playback_start",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_report_playback_stopped",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_report_session_ended",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_report_viewing",
                params=("item_id", "session_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_send_playstate_command",
                params=(
                    "command",
                    "controlling_user_id",
                    "seek_position_ticks",
                    "session_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read, then change, the playback reporting tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-playlists",
        (
            ToolStep(
                "jellyfin_get_hls_playlist_legacy",
                params=("item_id", "playlist_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_playlist",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "item_id",
                    "limit",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_master_hls_audio_playlist",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_adaptive_bitrate_streaming",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_ref_frames",
                    "max_streaming_bitrate",
                    "max_video_bit_depth",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_master_hls_video_playlist",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "always_burn_in_subtitle_when_transcoding",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_adaptive_bitrate_streaming",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "enable_trickplay",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_height",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "max_width",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_playlist",
                params=("playlist_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_playlist_items",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "limit",
                    "playlist_id",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_playlist_user",
                params=("playlist_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_playlist_users",
                params=("playlist_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_subtitle_playlist",
                params=("index", "item_id", "media_source_id", "segment_length"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_trickplay_hls_playlist",
                params=("item_id", "media_source_id", "width"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_variant_hls_audio_playlist",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_ref_frames",
                    "max_streaming_bitrate",
                    "max_video_bit_depth",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_variant_hls_video_playlist",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "always_burn_in_subtitle_when_transcoding",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_height",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "max_width",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_add_item_to_playlist",
                params=("ids", "playlist_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_create_playlist",
                params=("body", "ids", "media_type", "name", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_move_item",
                params=("item_id", "new_index", "playlist_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_playlist",
                params=("body", "playlist_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_playlist_user",
                params=("body", "playlist_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_remove_item_from_playlist",
                params=("confirm", "entry_ids", "playlist_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_remove_user_from_playlist",
                params=("confirm", "playlist_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the playlists tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-plugins-packages",
        (
            ToolStep(
                "jellyfin_get_package_info",
                params=("assembly_guid", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_packages",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_plugin_configuration",
                params=("plugin_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_plugin_manifest",
                params=("plugin_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_plugins",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_repositories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_enable_plugin",
                params=("plugin_id", "version"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_install_package",
                params=("assembly_guid", "name", "repository_url", "version"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_set_repositories",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_plugin_configuration",
                params=("plugin_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_cancel_package_installation",
                params=("confirm", "package_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_disable_plugin",
                params=("plugin_id", "version"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_uninstall_plugin",
                params=("confirm", "plugin_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_uninstall_plugin_by_version",
                params=("confirm", "plugin_id", "version"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the plugins packages tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-quick-connect-auth",
        (
            ToolStep(
                "jellyfin_get_auth_providers",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_first_user",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_first_user_2",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_keys",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_password_reset_providers",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_quick_connect_enabled",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_quick_connect_state",
                params=("secret",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_authenticate_user_by_name",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_authenticate_with_quick_connect",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_authorize_quick_connect",
                params=("code", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_create_key",
                params=("app",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_forgot_password",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_forgot_password_pin",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_initiate_quick_connect",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_startup_user",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_user_password",
                params=("body", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_revoke_key",
                params=("confirm", "key"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the quick connect auth tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-remote-metadata",
        (
            ToolStep(
                "jellyfin_get_book_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_box_set_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_external_id_infos",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_metadata_editor_info",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_movie_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_music_album_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_music_artist_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_music_video_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_person_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_search_hints",
                params=(
                    "exclude_item_types",
                    "include_artists",
                    "include_genres",
                    "include_item_types",
                    "include_media",
                    "include_people",
                    "include_studios",
                    "is_kids",
                    "is_movie",
                    "is_news",
                    "is_series",
                    "is_sports",
                    "limit",
                    "media_types",
                    "parent_id",
                    "search_term",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_series_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_trailer_remote_search_results",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_apply_search_criteria",
                params=("body", "item_id", "replace_all_images"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_refresh_item",
                params=(
                    "image_refresh_mode",
                    "item_id",
                    "metadata_refresh_mode",
                    "regenerate_trickplay",
                    "replace_all_images",
                    "replace_all_metadata",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_item_content_type",
                params=("content_type", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read, then change, the remote metadata tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-scheduled-tasks",
        (
            ToolStep(
                "jellyfin_get_task",
                params=("task_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_tasks",
                params=("is_enabled", "is_hidden"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_start_task",
                params=("task_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_task",
                params=("body", "task_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_stop_task",
                params=("confirm", "task_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the scheduled tasks tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-server-config",
        (
            ToolStep(
                "jellyfin_get_branding_css",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_branding_css_2",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_branding_options",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_configuration",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_configuration_pages",
                params=("enable_in_main_menu",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_countries",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_cultures",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_dashboard_configuration_page",
                params=("name",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_default_directory_browser",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_default_metadata_options",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_directory_contents",
                params=("include_directories", "include_files", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_drives",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_endpoint_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_fallback_font",
                params=("name",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_fallback_font_list",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_grouping_options",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_localization_options",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_named_configuration",
                params=("key",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_network_shares",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_parent_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_parental_ratings",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_ping_system",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_public_system_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_startup_configuration",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_system_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_system_storage",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_utc_time",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_complete_wizard",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_post_ping_system",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_send_system_command",
                params=("command", "session_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_set_remote_access",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_tmdb_client_configuration",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_branding_configuration",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_configuration",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_initial_configuration",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_named_configuration",
                params=("body", "key"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_restart_application",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_shutdown_application",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_validate_path",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read, then change, the server config tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-server-logs",
        (
            ToolStep(
                "jellyfin_get_log_entries",
                params=("has_user_id", "limit", "min_date", "start_index"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_log_file",
                params=("name",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_server_logs",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_log_file",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read, then change, the server logs tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-sessions-devices",
        (
            ToolStep(
                "jellyfin_get_device_info",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_device_options",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_devices",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_sessions",
                params=(
                    "active_within_seconds",
                    "controllable_by_user_id",
                    "device_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_add_user_to_session",
                params=("session_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_post_capabilities",
                params=(
                    "id",
                    "playable_media_types",
                    "supported_commands",
                    "supports_media_control",
                    "supports_persistent_identifier",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_post_full_capabilities",
                params=("body", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_send_full_general_command",
                params=("body", "session_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_send_general_command",
                params=("command", "session_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_send_message_command",
                params=("body", "session_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_device_options",
                params=("body", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_device",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_remove_user_from_session",
                params=("confirm", "session_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the sessions devices tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-shows-and-recommendations",
        (
            ToolStep(
                "jellyfin_get_critic_reviews",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_episodes",
                params=(
                    "adjacent_to",
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "is_missing",
                    "limit",
                    "season",
                    "season_id",
                    "series_id",
                    "sort_by",
                    "start_index",
                    "start_item_id",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_album",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "item_id",
                    "limit",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_item",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "item_id",
                    "limit",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_instant_mix_from_song",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "item_id",
                    "limit",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_intros",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_item_segments",
                params=("include_segment_types", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_latest_media",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "group_items",
                    "image_type_limit",
                    "include_item_types",
                    "is_played",
                    "limit",
                    "parent_id",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_local_trailers",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_movie_recommendations",
                params=(
                    "category_limit",
                    "fields",
                    "item_limit",
                    "parent_id",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_next_up",
                params=(
                    "disable_first_episode",
                    "enable_image_types",
                    "enable_images",
                    "enable_resumable",
                    "enable_rewatching",
                    "enable_total_record_count",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "limit",
                    "next_up_date_cutoff",
                    "parent_id",
                    "series_id",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_resume_items",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "exclude_active_sessions",
                    "exclude_item_types",
                    "fields",
                    "image_type_limit",
                    "include_item_types",
                    "limit",
                    "media_types",
                    "parent_id",
                    "search_term",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_seasons",
                params=(
                    "adjacent_to",
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "is_missing",
                    "is_special_season",
                    "series_id",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_similar_albums",
                params=("exclude_artist_ids", "fields", "item_id", "limit", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_similar_items",
                params=("exclude_artist_ids", "fields", "item_id", "limit", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_similar_movies",
                params=("exclude_artist_ids", "fields", "item_id", "limit", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_similar_shows",
                params=("exclude_artist_ids", "fields", "item_id", "limit", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_similar_trailers",
                params=("exclude_artist_ids", "fields", "item_id", "limit", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_special_features",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_suggestions",
                params=(
                    "enable_total_record_count",
                    "limit",
                    "media_type",
                    "start_index",
                    "type",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_theme_media",
                params=(
                    "inherit_from_parent",
                    "item_id",
                    "sort_by",
                    "sort_order",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_theme_songs",
                params=(
                    "inherit_from_parent",
                    "item_id",
                    "sort_by",
                    "sort_order",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_theme_videos",
                params=(
                    "inherit_from_parent",
                    "item_id",
                    "sort_by",
                    "sort_order",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_trailers",
                params=(
                    "adjacent_to",
                    "album_artist_ids",
                    "album_ids",
                    "albums",
                    "artist_ids",
                    "artists",
                    "collapse_box_set_items",
                    "contributing_artist_ids",
                    "enable_image_types",
                    "enable_images",
                    "enable_total_record_count",
                    "enable_user_data",
                    "exclude_artist_ids",
                    "exclude_item_ids",
                    "exclude_item_types",
                    "exclude_location_types",
                    "fields",
                    "filters",
                    "genre_ids",
                    "genres",
                    "has_imdb_id",
                    "has_official_rating",
                    "has_overview",
                    "has_parental_rating",
                    "has_special_feature",
                    "has_subtitles",
                    "has_theme_song",
                    "has_theme_video",
                    "has_tmdb_id",
                    "has_trailer",
                    "has_tvdb_id",
                    "ids",
                    "image_type_limit",
                    "image_types",
                    "is3_d",
                    "is4_k",
                    "is_favorite",
                    "is_hd",
                    "is_kids",
                    "is_locked",
                    "is_missing",
                    "is_movie",
                    "is_news",
                    "is_place_holder",
                    "is_played",
                    "is_series",
                    "is_sports",
                    "is_unaired",
                    "limit",
                    "location_types",
                    "max_height",
                    "max_official_rating",
                    "max_premiere_date",
                    "max_width",
                    "media_types",
                    "min_community_rating",
                    "min_critic_rating",
                    "min_date_last_saved",
                    "min_date_last_saved_for_user",
                    "min_height",
                    "min_official_rating",
                    "min_premiere_date",
                    "min_width",
                    "name_less_than",
                    "name_starts_with",
                    "name_starts_with_or_greater",
                    "official_ratings",
                    "parent_id",
                    "parent_index_number",
                    "person",
                    "person_ids",
                    "person_types",
                    "recursive",
                    "search_term",
                    "series_status",
                    "sort_by",
                    "sort_order",
                    "start_index",
                    "studio_ids",
                    "studios",
                    "tags",
                    "user_id",
                    "video_types",
                    "years",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_upcoming_episodes",
                params=(
                    "enable_image_types",
                    "enable_images",
                    "enable_user_data",
                    "fields",
                    "image_type_limit",
                    "limit",
                    "parent_id",
                    "start_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read, then change, the shows and recommendations tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-streaming",
        (
            ToolStep(
                "jellyfin_get_additional_part",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_attachment",
                params=("index", "media_source_id", "video_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_audio_stream",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "container",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_audio_stream_by_container",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "container",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_bitrate_test_bytes",
                params=("size",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_download",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_file",
                params=("item_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_hls_audio_segment",
                params=(
                    "actual_segment_length_ticks",
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "container",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_ref_frames",
                    "max_streaming_bitrate",
                    "max_video_bit_depth",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "playlist_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "runtime_ticks",
                    "segment_container",
                    "segment_id",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_hls_audio_segment_legacy_aac",
                params=("item_id", "segment_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_hls_audio_segment_legacy_mp3",
                params=("item_id", "segment_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_hls_video_segment",
                params=(
                    "actual_segment_length_ticks",
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "always_burn_in_subtitle_when_transcoding",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "container",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_height",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "max_width",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "playlist_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "runtime_ticks",
                    "segment_container",
                    "segment_id",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_hls_video_segment_legacy",
                params=("item_id", "playlist_id", "segment_container", "segment_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_live_hls_stream",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "always_burn_in_subtitle_when_transcoding",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "container",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "enable_subtitles_in_manifest",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_height",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "max_width",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_playback_info",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_posted_playback_info",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_stream_index",
                    "auto_open_live_stream",
                    "body",
                    "enable_direct_play",
                    "enable_direct_stream",
                    "enable_transcoding",
                    "item_id",
                    "live_stream_id",
                    "max_audio_channels",
                    "max_streaming_bitrate",
                    "media_source_id",
                    "start_time_ticks",
                    "subtitle_stream_index",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_universal_audio_stream",
                params=(
                    "audio_bit_rate",
                    "audio_codec",
                    "break_on_non_key_frames",
                    "container",
                    "device_id",
                    "enable_audio_vbr_encoding",
                    "enable_redirection",
                    "enable_remote_media",
                    "item_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_audio_sample_rate",
                    "max_streaming_bitrate",
                    "media_source_id",
                    "start_time_ticks",
                    "transcoding_audio_channels",
                    "transcoding_container",
                    "transcoding_protocol",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_video_stream",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "container",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_height",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "max_width",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_video_stream_by_container",
                params=(
                    "allow_audio_stream_copy",
                    "allow_video_stream_copy",
                    "audio_bit_rate",
                    "audio_channels",
                    "audio_codec",
                    "audio_sample_rate",
                    "audio_stream_index",
                    "break_on_non_key_frames",
                    "container",
                    "context",
                    "copy_timestamps",
                    "cpu_core_limit",
                    "de_interlace",
                    "device_id",
                    "device_profile_id",
                    "enable_audio_vbr_encoding",
                    "enable_auto_stream_copy",
                    "enable_mpegts_m2_ts_mode",
                    "framerate",
                    "height",
                    "item_id",
                    "level",
                    "live_stream_id",
                    "max_audio_bit_depth",
                    "max_audio_channels",
                    "max_framerate",
                    "max_height",
                    "max_ref_frames",
                    "max_video_bit_depth",
                    "max_width",
                    "media_source_id",
                    "min_segments",
                    "play_session_id",
                    "profile",
                    "require_avc",
                    "require_non_anamorphic",
                    "segment_container",
                    "segment_length",
                    "start_time_ticks",
                    "static",
                    "stream_options",
                    "stream_params",
                    "subtitle_codec",
                    "subtitle_method",
                    "subtitle_stream_index",
                    "tag",
                    "transcode_reasons",
                    "transcoding_max_audio_channels",
                    "video_bit_rate",
                    "video_codec",
                    "video_stream_index",
                    "width",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_merge_versions",
                params=("ids",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_alternate_sources",
                params=("confirm", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_stop_encoding_process",
                params=("confirm", "device_id", "play_session_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the streaming tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-subtitles",
        (
            ToolStep(
                "jellyfin_get_remote_subtitles",
                params=("subtitle_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_subtitle",
                params=(
                    "add_vtt_time_map",
                    "copy_timestamps",
                    "end_position_ticks",
                    "format",
                    "index",
                    "item_id",
                    "media_source_id",
                    "route_format",
                    "route_index",
                    "route_item_id",
                    "route_media_source_id",
                    "start_position_ticks",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_subtitle_with_ticks",
                params=(
                    "add_vtt_time_map",
                    "copy_timestamps",
                    "end_position_ticks",
                    "format",
                    "index",
                    "item_id",
                    "media_source_id",
                    "route_format",
                    "route_index",
                    "route_item_id",
                    "route_media_source_id",
                    "route_start_position_ticks",
                    "start_position_ticks",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_search_remote_subtitles",
                params=("is_perfect_match", "item_id", "language"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_download_remote_subtitles",
                params=("item_id", "subtitle_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_upload_subtitle",
                params=("body", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_delete_subtitle",
                params=("confirm", "index", "item_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the subtitles tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-syncplay",
        (
            ToolStep(
                "jellyfin_sync_play_buffering",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_create_group",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_get_group",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_get_groups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_join_group",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_leave_group",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_move_playlist_item",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_next_item",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_pause",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_ping",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_previous_item",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_queue",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_ready",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_remove_from_playlist",
                params=("body", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_seek",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_set_ignore_wait",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_set_new_queue",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_set_playlist_item",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_set_repeat_mode",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_set_shuffle_mode",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_stop",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_sync_play_unpause",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read, then change, the syncplay tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
    ToolUseContract(
        "jellyfin-manage-users",
        (
            ToolStep(
                "jellyfin_get_current_user",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_item_user_data",
                params=("item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_public_users",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_get_user_by_id",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_user_views",
                params=(
                    "include_external_content",
                    "include_hidden",
                    "preset_views",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_get_users",
                params=("is_disabled", "is_hidden"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_create_user_by_name",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_update_item_user_data",
                params=("body", "item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_user",
                params=("body", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_user_configuration",
                params=("body", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_user_item_rating",
                params=("item_id", "likes", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_update_user_policy",
                params=("body", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "jellyfin_delete_user",
                params=("confirm", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "jellyfin_delete_user_item_rating",
                params=("confirm", "item_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read, then change, the users tools of the Jellyfin server; reads first, destructive calls need confirmation.",
    ),
)

LINKS = (
    SurfaceLink(
        "jellyfin-find-item",
        tools=(
            "jellyfin_get_item",
            "jellyfin_get_items",
            "jellyfin_get_search_hints",
        ),
        prompts=(
            "jellyfin-operator",
            "jellyfin-media-librarian",
            "jellyfin-playback-coordinator",
        ),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-add-media-and-scan",
        tools=(
            "jellyfin_add_media_path",
            "jellyfin_get_items",
            "jellyfin_get_virtual_folders",
            "jellyfin_refresh_library",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-mark-watched",
        tools=(
            "jellyfin_get_item",
            "jellyfin_get_search_hints",
            "jellyfin_mark_played_item",
        ),
        prompts=("jellyfin-operator", "jellyfin-playback-coordinator"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-build-playlist",
        tools=(
            "jellyfin_add_item_to_playlist",
            "jellyfin_create_playlist",
            "jellyfin_get_playlist_items",
        ),
        prompts=("jellyfin-operator", "jellyfin-playback-coordinator"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-build-collection",
        tools=(
            "jellyfin_add_to_collection",
            "jellyfin_create_collection",
            "jellyfin_get_item",
            "jellyfin_get_items",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-fetch-subtitles",
        tools=(
            "jellyfin_download_remote_subtitles",
            "jellyfin_get_item",
            "jellyfin_search_remote_subtitles",
        ),
        prompts=(
            "jellyfin-operator",
            "jellyfin-media-librarian",
            "jellyfin-playback-coordinator",
        ),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-refresh-item-metadata",
        tools=(
            "jellyfin_get_item",
            "jellyfin_refresh_item",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-schedule-recording",
        tools=(
            "jellyfin_create_timer",
            "jellyfin_get_default_timer",
            "jellyfin_get_live_tv_info",
            "jellyfin_get_programs",
            "jellyfin_get_timers",
        ),
        prompts=("jellyfin-operator", "jellyfin-live-tv-manager"),
        skills=("jellyfin-live-tv",),
    ),
    SurfaceLink(
        "jellyfin-server-health-check",
        tools=(
            "jellyfin_get_log_entries",
            "jellyfin_get_system_info",
            "jellyfin_get_system_storage",
            "jellyfin_get_tasks",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration", "jellyfin-mcp-operations"),
    ),
    SurfaceLink(
        "jellyfin-backup-server",
        tools=(
            "jellyfin_create_backup",
            "jellyfin_list_backups",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-quick-connect-sign-in",
        tools=(
            "jellyfin_authorize_quick_connect",
            "jellyfin_get_quick_connect_enabled",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-create-user",
        tools=(
            "jellyfin_create_user_by_name",
            "jellyfin_get_users",
            "jellyfin_update_user_policy",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-install-plugin",
        tools=(
            "jellyfin_get_packages",
            "jellyfin_get_plugins",
            "jellyfin_install_package",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-message-session",
        tools=(
            "jellyfin_get_sessions",
            "jellyfin_send_message_command",
        ),
        prompts=("jellyfin-operator", "jellyfin-playback-coordinator"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-ingest-posters",
        tools=(
            "jellyfin_get_items",
            "jellyfin_ingest_posters",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-kg-ingestion",),
    ),
    SurfaceLink(
        "jellyfin-manage-backup-restore",
        tools=(
            "jellyfin_create_backup",
            "jellyfin_get_backup",
            "jellyfin_list_backups",
            "jellyfin_start_restore_backup",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-manage-collections",
        tools=(
            "jellyfin_add_to_collection",
            "jellyfin_create_collection",
            "jellyfin_remove_from_collection",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-favorites-ratings",
        tools=(
            "jellyfin_mark_favorite_item",
            "jellyfin_unmark_favorite_item",
        ),
        prompts=(
            "jellyfin-operator",
            "jellyfin-media-librarian",
            "jellyfin-playback-coordinator",
        ),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-images",
        tools=(
            "jellyfin_delete_custom_splashscreen",
            "jellyfin_delete_item_image",
            "jellyfin_delete_item_image_by_index",
            "jellyfin_delete_user_image",
            "jellyfin_download_remote_image",
            "jellyfin_get_artist_image",
            "jellyfin_get_genre_image",
            "jellyfin_get_genre_image_by_index",
            "jellyfin_get_item_image",
            "jellyfin_get_item_image2",
            "jellyfin_get_item_image_by_index",
            "jellyfin_get_item_image_infos",
            "jellyfin_get_music_genre_image",
            "jellyfin_get_music_genre_image_by_index",
            "jellyfin_get_person_image",
            "jellyfin_get_person_image_by_index",
            "jellyfin_get_plugin_image",
            "jellyfin_get_remote_image_providers",
            "jellyfin_get_remote_images",
            "jellyfin_get_splashscreen",
            "jellyfin_get_studio_image",
            "jellyfin_get_studio_image_by_index",
            "jellyfin_get_trickplay_tile_image",
            "jellyfin_get_user_image",
            "jellyfin_post_user_image",
            "jellyfin_set_item_image",
            "jellyfin_set_item_image_by_index",
            "jellyfin_update_item_image_index",
            "jellyfin_upload_custom_splashscreen",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-items",
        tools=(
            "jellyfin_delete_item",
            "jellyfin_delete_items",
            "jellyfin_get_ancestors",
            "jellyfin_get_item",
            "jellyfin_get_item_counts",
            "jellyfin_get_items",
            "jellyfin_get_query_filters",
            "jellyfin_get_query_filters_legacy",
            "jellyfin_update_item",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-library-admin",
        tools=(
            "jellyfin_add_media_path",
            "jellyfin_add_virtual_folder",
            "jellyfin_get_library_options_info",
            "jellyfin_get_media_folders",
            "jellyfin_get_physical_paths",
            "jellyfin_get_root_folder",
            "jellyfin_get_virtual_folders",
            "jellyfin_ingest_library",
            "jellyfin_post_added_movies",
            "jellyfin_post_added_series",
            "jellyfin_post_updated_media",
            "jellyfin_post_updated_movies",
            "jellyfin_post_updated_series",
            "jellyfin_refresh_library",
            "jellyfin_remove_media_path",
            "jellyfin_remove_virtual_folder",
            "jellyfin_rename_virtual_folder",
            "jellyfin_update_library_options",
            "jellyfin_update_media_path",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-livetv-recordings",
        tools=(
            "jellyfin_cancel_series_timer",
            "jellyfin_cancel_timer",
            "jellyfin_create_series_timer",
            "jellyfin_create_timer",
            "jellyfin_delete_recording",
            "jellyfin_get_default_timer",
            "jellyfin_get_live_recording_file",
            "jellyfin_get_recording",
            "jellyfin_get_recording_folders",
            "jellyfin_get_recording_group",
            "jellyfin_get_recording_groups",
            "jellyfin_get_recordings",
            "jellyfin_get_recordings_series",
            "jellyfin_get_series_timer",
            "jellyfin_get_series_timers",
            "jellyfin_get_timer",
            "jellyfin_get_timers",
            "jellyfin_update_series_timer",
            "jellyfin_update_timer",
        ),
        prompts=("jellyfin-operator", "jellyfin-live-tv-manager"),
        skills=("jellyfin-live-tv",),
    ),
    SurfaceLink(
        "jellyfin-manage-livetv-setup",
        tools=(
            "jellyfin_add_listing_provider",
            "jellyfin_add_tuner_host",
            "jellyfin_close_live_stream",
            "jellyfin_delete_listing_provider",
            "jellyfin_delete_tuner_host",
            "jellyfin_discover_tuners",
            "jellyfin_discvover_tuners",
            "jellyfin_get_all_channel_features",
            "jellyfin_get_channel",
            "jellyfin_get_channel_features",
            "jellyfin_get_channel_items",
            "jellyfin_get_channel_mapping_options",
            "jellyfin_get_channels",
            "jellyfin_get_default_listing_provider",
            "jellyfin_get_guide_info",
            "jellyfin_get_latest_channel_items",
            "jellyfin_get_lineups",
            "jellyfin_get_live_stream_file",
            "jellyfin_get_live_tv_channels",
            "jellyfin_get_live_tv_info",
            "jellyfin_get_live_tv_programs",
            "jellyfin_get_program",
            "jellyfin_get_programs",
            "jellyfin_get_recommended_programs",
            "jellyfin_get_schedules_direct_countries",
            "jellyfin_get_tuner_host_types",
            "jellyfin_open_live_stream",
            "jellyfin_reset_tuner",
            "jellyfin_set_channel_mapping",
        ),
        prompts=("jellyfin-operator", "jellyfin-live-tv-manager"),
        skills=("jellyfin-live-tv",),
    ),
    SurfaceLink(
        "jellyfin-manage-lyrics",
        tools=(
            "jellyfin_delete_lyrics",
            "jellyfin_download_remote_lyrics",
            "jellyfin_get_lyrics",
            "jellyfin_get_remote_lyrics",
            "jellyfin_search_remote_lyrics",
            "jellyfin_upload_lyrics",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-manage-misc",
        tools=(
            "jellyfin_get_display_preferences",
            "jellyfin_ingest_posters",
            "jellyfin_update_display_preferences",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-people-genres-studios",
        tools=(
            "jellyfin_get_album_artists",
            "jellyfin_get_artist_by_name",
            "jellyfin_get_artists",
            "jellyfin_get_genre",
            "jellyfin_get_genres",
            "jellyfin_get_instant_mix_from_artists",
            "jellyfin_get_instant_mix_from_artists2",
            "jellyfin_get_instant_mix_from_music_genre_by_id",
            "jellyfin_get_instant_mix_from_music_genre_by_name",
            "jellyfin_get_music_genre",
            "jellyfin_get_music_genres",
            "jellyfin_get_person",
            "jellyfin_get_persons",
            "jellyfin_get_similar_artists",
            "jellyfin_get_studio",
            "jellyfin_get_studios",
            "jellyfin_get_year",
            "jellyfin_get_years",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-playback-reporting",
        tools=(
            "jellyfin_display_content",
            "jellyfin_mark_played_item",
            "jellyfin_mark_unplayed_item",
            "jellyfin_on_playback_progress",
            "jellyfin_on_playback_start",
            "jellyfin_on_playback_stopped",
            "jellyfin_ping_playback_session",
            "jellyfin_play",
            "jellyfin_report_playback_progress",
            "jellyfin_report_playback_start",
            "jellyfin_report_playback_stopped",
            "jellyfin_report_session_ended",
            "jellyfin_report_viewing",
            "jellyfin_send_playstate_command",
        ),
        prompts=("jellyfin-operator", "jellyfin-playback-coordinator"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-manage-playlists",
        tools=(
            "jellyfin_add_item_to_playlist",
            "jellyfin_create_playlist",
            "jellyfin_get_hls_playlist_legacy",
            "jellyfin_get_instant_mix_from_playlist",
            "jellyfin_get_master_hls_audio_playlist",
            "jellyfin_get_master_hls_video_playlist",
            "jellyfin_get_playlist",
            "jellyfin_get_playlist_items",
            "jellyfin_get_playlist_user",
            "jellyfin_get_playlist_users",
            "jellyfin_get_subtitle_playlist",
            "jellyfin_get_trickplay_hls_playlist",
            "jellyfin_get_variant_hls_audio_playlist",
            "jellyfin_get_variant_hls_video_playlist",
            "jellyfin_move_item",
            "jellyfin_remove_item_from_playlist",
            "jellyfin_remove_user_from_playlist",
            "jellyfin_update_playlist",
            "jellyfin_update_playlist_user",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-manage-plugins-packages",
        tools=(
            "jellyfin_cancel_package_installation",
            "jellyfin_disable_plugin",
            "jellyfin_enable_plugin",
            "jellyfin_get_package_info",
            "jellyfin_get_packages",
            "jellyfin_get_plugin_configuration",
            "jellyfin_get_plugin_manifest",
            "jellyfin_get_plugins",
            "jellyfin_get_repositories",
            "jellyfin_install_package",
            "jellyfin_set_repositories",
            "jellyfin_uninstall_plugin",
            "jellyfin_uninstall_plugin_by_version",
            "jellyfin_update_plugin_configuration",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-manage-quick-connect-auth",
        tools=(
            "jellyfin_authenticate_user_by_name",
            "jellyfin_authenticate_with_quick_connect",
            "jellyfin_authorize_quick_connect",
            "jellyfin_create_key",
            "jellyfin_forgot_password",
            "jellyfin_forgot_password_pin",
            "jellyfin_get_auth_providers",
            "jellyfin_get_first_user",
            "jellyfin_get_first_user_2",
            "jellyfin_get_keys",
            "jellyfin_get_password_reset_providers",
            "jellyfin_get_quick_connect_enabled",
            "jellyfin_get_quick_connect_state",
            "jellyfin_initiate_quick_connect",
            "jellyfin_revoke_key",
            "jellyfin_update_startup_user",
            "jellyfin_update_user_password",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-manage-remote-metadata",
        tools=(
            "jellyfin_apply_search_criteria",
            "jellyfin_get_book_remote_search_results",
            "jellyfin_get_box_set_remote_search_results",
            "jellyfin_get_external_id_infos",
            "jellyfin_get_metadata_editor_info",
            "jellyfin_get_movie_remote_search_results",
            "jellyfin_get_music_album_remote_search_results",
            "jellyfin_get_music_artist_remote_search_results",
            "jellyfin_get_music_video_remote_search_results",
            "jellyfin_get_person_remote_search_results",
            "jellyfin_get_search_hints",
            "jellyfin_get_series_remote_search_results",
            "jellyfin_get_trailer_remote_search_results",
            "jellyfin_refresh_item",
            "jellyfin_update_item_content_type",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-scheduled-tasks",
        tools=(
            "jellyfin_get_task",
            "jellyfin_get_tasks",
            "jellyfin_start_task",
            "jellyfin_stop_task",
            "jellyfin_update_task",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-manage-server-config",
        tools=(
            "jellyfin_complete_wizard",
            "jellyfin_get_branding_css",
            "jellyfin_get_branding_css_2",
            "jellyfin_get_branding_options",
            "jellyfin_get_configuration",
            "jellyfin_get_configuration_pages",
            "jellyfin_get_countries",
            "jellyfin_get_cultures",
            "jellyfin_get_dashboard_configuration_page",
            "jellyfin_get_default_directory_browser",
            "jellyfin_get_default_metadata_options",
            "jellyfin_get_directory_contents",
            "jellyfin_get_drives",
            "jellyfin_get_endpoint_info",
            "jellyfin_get_fallback_font",
            "jellyfin_get_fallback_font_list",
            "jellyfin_get_grouping_options",
            "jellyfin_get_localization_options",
            "jellyfin_get_named_configuration",
            "jellyfin_get_network_shares",
            "jellyfin_get_parent_path",
            "jellyfin_get_parental_ratings",
            "jellyfin_get_ping_system",
            "jellyfin_get_public_system_info",
            "jellyfin_get_startup_configuration",
            "jellyfin_get_system_info",
            "jellyfin_get_system_storage",
            "jellyfin_get_utc_time",
            "jellyfin_post_ping_system",
            "jellyfin_restart_application",
            "jellyfin_send_system_command",
            "jellyfin_set_remote_access",
            "jellyfin_shutdown_application",
            "jellyfin_tmdb_client_configuration",
            "jellyfin_update_branding_configuration",
            "jellyfin_update_configuration",
            "jellyfin_update_initial_configuration",
            "jellyfin_update_named_configuration",
            "jellyfin_validate_path",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-manage-server-logs",
        tools=(
            "jellyfin_get_log_entries",
            "jellyfin_get_log_file",
            "jellyfin_get_server_logs",
            "jellyfin_log_file",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
    SurfaceLink(
        "jellyfin-manage-sessions-devices",
        tools=(
            "jellyfin_add_user_to_session",
            "jellyfin_delete_device",
            "jellyfin_get_device_info",
            "jellyfin_get_device_options",
            "jellyfin_get_devices",
            "jellyfin_get_sessions",
            "jellyfin_post_capabilities",
            "jellyfin_post_full_capabilities",
            "jellyfin_remove_user_from_session",
            "jellyfin_send_full_general_command",
            "jellyfin_send_general_command",
            "jellyfin_send_message_command",
            "jellyfin_update_device_options",
        ),
        prompts=(
            "jellyfin-operator",
            "jellyfin-server-administrator",
            "jellyfin-playback-coordinator",
        ),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-manage-shows-and-recommendations",
        tools=(
            "jellyfin_get_critic_reviews",
            "jellyfin_get_episodes",
            "jellyfin_get_instant_mix_from_album",
            "jellyfin_get_instant_mix_from_item",
            "jellyfin_get_instant_mix_from_song",
            "jellyfin_get_intros",
            "jellyfin_get_item_segments",
            "jellyfin_get_latest_media",
            "jellyfin_get_local_trailers",
            "jellyfin_get_movie_recommendations",
            "jellyfin_get_next_up",
            "jellyfin_get_resume_items",
            "jellyfin_get_seasons",
            "jellyfin_get_similar_albums",
            "jellyfin_get_similar_items",
            "jellyfin_get_similar_movies",
            "jellyfin_get_similar_shows",
            "jellyfin_get_similar_trailers",
            "jellyfin_get_special_features",
            "jellyfin_get_suggestions",
            "jellyfin_get_theme_media",
            "jellyfin_get_theme_songs",
            "jellyfin_get_theme_videos",
            "jellyfin_get_trailers",
            "jellyfin_get_upcoming_episodes",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-library-catalog",),
    ),
    SurfaceLink(
        "jellyfin-manage-streaming",
        tools=(
            "jellyfin_delete_alternate_sources",
            "jellyfin_get_additional_part",
            "jellyfin_get_attachment",
            "jellyfin_get_audio_stream",
            "jellyfin_get_audio_stream_by_container",
            "jellyfin_get_bitrate_test_bytes",
            "jellyfin_get_download",
            "jellyfin_get_file",
            "jellyfin_get_hls_audio_segment",
            "jellyfin_get_hls_audio_segment_legacy_aac",
            "jellyfin_get_hls_audio_segment_legacy_mp3",
            "jellyfin_get_hls_video_segment",
            "jellyfin_get_hls_video_segment_legacy",
            "jellyfin_get_live_hls_stream",
            "jellyfin_get_playback_info",
            "jellyfin_get_posted_playback_info",
            "jellyfin_get_universal_audio_stream",
            "jellyfin_get_video_stream",
            "jellyfin_get_video_stream_by_container",
            "jellyfin_merge_versions",
            "jellyfin_stop_encoding_process",
        ),
        prompts=("jellyfin-operator", "jellyfin-playback-coordinator"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-manage-subtitles",
        tools=(
            "jellyfin_delete_subtitle",
            "jellyfin_download_remote_subtitles",
            "jellyfin_get_remote_subtitles",
            "jellyfin_get_subtitle",
            "jellyfin_get_subtitle_with_ticks",
            "jellyfin_search_remote_subtitles",
            "jellyfin_upload_subtitle",
        ),
        prompts=("jellyfin-operator", "jellyfin-media-librarian"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-manage-syncplay",
        tools=(
            "jellyfin_sync_play_buffering",
            "jellyfin_sync_play_create_group",
            "jellyfin_sync_play_get_group",
            "jellyfin_sync_play_get_groups",
            "jellyfin_sync_play_join_group",
            "jellyfin_sync_play_leave_group",
            "jellyfin_sync_play_move_playlist_item",
            "jellyfin_sync_play_next_item",
            "jellyfin_sync_play_pause",
            "jellyfin_sync_play_ping",
            "jellyfin_sync_play_previous_item",
            "jellyfin_sync_play_queue",
            "jellyfin_sync_play_ready",
            "jellyfin_sync_play_remove_from_playlist",
            "jellyfin_sync_play_seek",
            "jellyfin_sync_play_set_ignore_wait",
            "jellyfin_sync_play_set_new_queue",
            "jellyfin_sync_play_set_playlist_item",
            "jellyfin_sync_play_set_repeat_mode",
            "jellyfin_sync_play_set_shuffle_mode",
            "jellyfin_sync_play_stop",
            "jellyfin_sync_play_unpause",
        ),
        prompts=("jellyfin-operator", "jellyfin-playback-coordinator"),
        skills=("jellyfin-media-playback",),
    ),
    SurfaceLink(
        "jellyfin-manage-users",
        tools=(
            "jellyfin_create_user_by_name",
            "jellyfin_delete_user",
            "jellyfin_delete_user_item_rating",
            "jellyfin_get_current_user",
            "jellyfin_get_item_user_data",
            "jellyfin_get_public_users",
            "jellyfin_get_user_by_id",
            "jellyfin_get_user_views",
            "jellyfin_get_users",
            "jellyfin_update_item_user_data",
            "jellyfin_update_user",
            "jellyfin_update_user_configuration",
            "jellyfin_update_user_item_rating",
            "jellyfin_update_user_policy",
        ),
        prompts=("jellyfin-operator", "jellyfin-server-administrator"),
        skills=("jellyfin-server-administration",),
    ),
)

LOCATIONS = (
    DataLocation(
        "jellyfin-library", ("MediaLibrary",), "JELLYFIN_URL", "jellyfin_get_items"
    ),
    DataLocation("jellyfin-users", ("Person",), "JELLYFIN_URL", "jellyfin_get_users"),
    DataLocation(
        "jellyfin-sessions", ("System",), "JELLYFIN_URL", "jellyfin_get_sessions"
    ),
    DataLocation(
        "jellyfin-livetv", ("MediaCollection",), "JELLYFIN_URL", "jellyfin_get_timers"
    ),
    DataLocation(
        "jellyfin-server", ("System",), "JELLYFIN_URL", "jellyfin_get_system_info"
    ),
)

ROLES = (
    BusinessRole(
        "media librarian",
        tasks=(
            "jellyfin-add-media-and-scan",
            "jellyfin-build-collection",
            "jellyfin-fetch-subtitles",
            "jellyfin-find-item",
            "jellyfin-ingest-posters",
            "jellyfin-manage-collections",
            "jellyfin-manage-favorites-ratings",
            "jellyfin-manage-images",
            "jellyfin-manage-items",
            "jellyfin-manage-library-admin",
            "jellyfin-manage-lyrics",
            "jellyfin-manage-misc",
            "jellyfin-manage-people-genres-studios",
            "jellyfin-manage-playlists",
            "jellyfin-manage-remote-metadata",
            "jellyfin-manage-shows-and-recommendations",
            "jellyfin-manage-subtitles",
            "jellyfin-refresh-item-metadata",
        ),
    ),
    BusinessRole(
        "server administrator",
        tasks=(
            "jellyfin-backup-server",
            "jellyfin-create-user",
            "jellyfin-install-plugin",
            "jellyfin-manage-backup-restore",
            "jellyfin-manage-plugins-packages",
            "jellyfin-manage-quick-connect-auth",
            "jellyfin-manage-scheduled-tasks",
            "jellyfin-manage-server-config",
            "jellyfin-manage-server-logs",
            "jellyfin-manage-sessions-devices",
            "jellyfin-manage-users",
            "jellyfin-quick-connect-sign-in",
            "jellyfin-server-health-check",
        ),
    ),
    BusinessRole(
        "playback coordinator",
        tasks=(
            "jellyfin-build-playlist",
            "jellyfin-fetch-subtitles",
            "jellyfin-find-item",
            "jellyfin-manage-favorites-ratings",
            "jellyfin-manage-playback-reporting",
            "jellyfin-manage-sessions-devices",
            "jellyfin-manage-streaming",
            "jellyfin-manage-syncplay",
            "jellyfin-mark-watched",
            "jellyfin-message-session",
        ),
    ),
    BusinessRole(
        "live tv manager",
        tasks=(
            "jellyfin-manage-livetv-recordings",
            "jellyfin-manage-livetv-setup",
            "jellyfin-schedule-recording",
        ),
    ),
)
