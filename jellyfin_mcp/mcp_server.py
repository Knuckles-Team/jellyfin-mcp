#!/usr/bin/python
"""Jellyfin MCP Server module.

Dynamic Tool Routing
"""

import logging
import sys
from typing import Any, Literal

from agent_utilities.core.config import load_config
from agent_utilities.mcp.action_dispatch import dispatch_async, parse_json_object
from agent_utilities.mcp.concurrency import run_blocking
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from jellyfin_mcp.api_client import Api
from jellyfin_mcp.auth import get_client

# The real, closed action set every jellyfin_* condensed tool dispatches
# to: all three share one combined Api client (Media+Library+System+User
# mixins, jellyfin_mcp/api_client.py), so the true dispatchable set is the
# same union for all of them regardless of the tool own domain label.
_JELLYFIN_ACTIONS = Literal[
    "add_item_to_playlist",
    "add_listing_provider",
    "add_media_path",
    "add_to_collection",
    "add_tuner_host",
    "add_user_to_session",
    "add_virtual_folder",
    "apply_search_criteria",
    "authenticate_user_by_name",
    "authenticate_with_quick_connect",
    "authorize_quick_connect",
    "cancel_package_installation",
    "cancel_series_timer",
    "cancel_timer",
    "close_live_stream",
    "complete_wizard",
    "create_backup",
    "create_collection",
    "create_key",
    "create_playlist",
    "create_series_timer",
    "create_timer",
    "create_user_by_name",
    "delete_alternate_sources",
    "delete_custom_splashscreen",
    "delete_device",
    "delete_item",
    "delete_item_image",
    "delete_item_image_by_index",
    "delete_items",
    "delete_listing_provider",
    "delete_lyrics",
    "delete_recording",
    "delete_subtitle",
    "delete_tuner_host",
    "delete_user",
    "delete_user_image",
    "delete_user_item_rating",
    "disable_plugin",
    "discover_tuners",
    "discvover_tuners",
    "display_content",
    "download_remote_image",
    "download_remote_lyrics",
    "download_remote_subtitles",
    "enable_plugin",
    "forgot_password",
    "forgot_password_pin",
    "get_additional_part",
    "get_album_artists",
    "get_all_channel_features",
    "get_ancestors",
    "get_artist_by_name",
    "get_artist_image",
    "get_artists",
    "get_attachment",
    "get_audio_stream",
    "get_audio_stream_by_container",
    "get_auth_providers",
    "get_backup",
    "get_bitrate_test_bytes",
    "get_book_remote_search_results",
    "get_box_set_remote_search_results",
    "get_branding_css",
    "get_branding_css_2",
    "get_branding_options",
    "get_channel",
    "get_channel_features",
    "get_channel_items",
    "get_channel_mapping_options",
    "get_channels",
    "get_configuration",
    "get_configuration_pages",
    "get_countries",
    "get_critic_reviews",
    "get_cultures",
    "get_current_user",
    "get_dashboard_configuration_page",
    "get_default_directory_browser",
    "get_default_listing_provider",
    "get_default_metadata_options",
    "get_default_timer",
    "get_device_info",
    "get_device_options",
    "get_devices",
    "get_directory_contents",
    "get_display_preferences",
    "get_download",
    "get_drives",
    "get_endpoint_info",
    "get_episodes",
    "get_external_id_infos",
    "get_fallback_font",
    "get_fallback_font_list",
    "get_file",
    "get_first_user",
    "get_first_user_2",
    "get_genre",
    "get_genre_image",
    "get_genre_image_by_index",
    "get_genres",
    "get_grouping_options",
    "get_guide_info",
    "get_hls_audio_segment",
    "get_hls_audio_segment_legacy_aac",
    "get_hls_audio_segment_legacy_mp3",
    "get_hls_playlist_legacy",
    "get_hls_video_segment",
    "get_hls_video_segment_legacy",
    "get_instant_mix_from_album",
    "get_instant_mix_from_artists",
    "get_instant_mix_from_artists2",
    "get_instant_mix_from_item",
    "get_instant_mix_from_music_genre_by_id",
    "get_instant_mix_from_music_genre_by_name",
    "get_instant_mix_from_playlist",
    "get_instant_mix_from_song",
    "get_intros",
    "get_item",
    "get_item_counts",
    "get_item_image",
    "get_item_image2",
    "get_item_image_by_index",
    "get_item_image_infos",
    "get_item_segments",
    "get_item_user_data",
    "get_items",
    "get_keys",
    "get_latest_channel_items",
    "get_latest_media",
    "get_library_options_info",
    "get_lineups",
    "get_live_hls_stream",
    "get_live_recording_file",
    "get_live_stream_file",
    "get_live_tv_channels",
    "get_live_tv_info",
    "get_live_tv_programs",
    "get_local_trailers",
    "get_localization_options",
    "get_log_entries",
    "get_log_file",
    "get_lyrics",
    "get_master_hls_audio_playlist",
    "get_master_hls_video_playlist",
    "get_media_folders",
    "get_metadata_editor_info",
    "get_movie_recommendations",
    "get_movie_remote_search_results",
    "get_music_album_remote_search_results",
    "get_music_artist_remote_search_results",
    "get_music_genre",
    "get_music_genre_image",
    "get_music_genre_image_by_index",
    "get_music_genres",
    "get_music_video_remote_search_results",
    "get_named_configuration",
    "get_network_shares",
    "get_next_up",
    "get_package_info",
    "get_packages",
    "get_parent_path",
    "get_parental_ratings",
    "get_password_reset_providers",
    "get_person",
    "get_person_image",
    "get_person_image_by_index",
    "get_person_remote_search_results",
    "get_persons",
    "get_physical_paths",
    "get_ping_system",
    "get_playback_info",
    "get_playlist",
    "get_playlist_items",
    "get_playlist_user",
    "get_playlist_users",
    "get_plugin_configuration",
    "get_plugin_image",
    "get_plugin_manifest",
    "get_plugins",
    "get_posted_playback_info",
    "get_program",
    "get_programs",
    "get_public_system_info",
    "get_public_users",
    "get_query_filters",
    "get_query_filters_legacy",
    "get_quick_connect_enabled",
    "get_quick_connect_state",
    "get_recommended_programs",
    "get_recording",
    "get_recording_folders",
    "get_recording_group",
    "get_recording_groups",
    "get_recordings",
    "get_recordings_series",
    "get_remote_image_providers",
    "get_remote_images",
    "get_remote_lyrics",
    "get_remote_subtitles",
    "get_repositories",
    "get_resume_items",
    "get_root_folder",
    "get_schedules_direct_countries",
    "get_search_hints",
    "get_seasons",
    "get_series_remote_search_results",
    "get_series_timer",
    "get_series_timers",
    "get_server_logs",
    "get_sessions",
    "get_similar_albums",
    "get_similar_artists",
    "get_similar_items",
    "get_similar_movies",
    "get_similar_shows",
    "get_similar_trailers",
    "get_special_features",
    "get_splashscreen",
    "get_startup_configuration",
    "get_studio",
    "get_studio_image",
    "get_studio_image_by_index",
    "get_studios",
    "get_subtitle",
    "get_subtitle_playlist",
    "get_subtitle_with_ticks",
    "get_suggestions",
    "get_system_info",
    "get_system_storage",
    "get_task",
    "get_tasks",
    "get_theme_media",
    "get_theme_songs",
    "get_theme_videos",
    "get_timer",
    "get_timers",
    "get_trailer_remote_search_results",
    "get_trailers",
    "get_trickplay_hls_playlist",
    "get_trickplay_tile_image",
    "get_tuner_host_types",
    "get_universal_audio_stream",
    "get_upcoming_episodes",
    "get_user_by_id",
    "get_user_image",
    "get_user_views",
    "get_users",
    "get_utc_time",
    "get_variant_hls_audio_playlist",
    "get_variant_hls_video_playlist",
    "get_video_stream",
    "get_video_stream_by_container",
    "get_virtual_folders",
    "get_year",
    "get_years",
    "initiate_quick_connect",
    "install_package",
    "list_backups",
    "log_file",
    "mark_favorite_item",
    "mark_played_item",
    "mark_unplayed_item",
    "merge_versions",
    "move_item",
    "on_playback_progress",
    "on_playback_start",
    "on_playback_stopped",
    "open_live_stream",
    "ping_playback_session",
    "play",
    "post_added_movies",
    "post_added_series",
    "post_capabilities",
    "post_full_capabilities",
    "post_ping_system",
    "post_updated_media",
    "post_updated_movies",
    "post_updated_series",
    "post_user_image",
    "refresh_item",
    "refresh_library",
    "remove_from_collection",
    "remove_item_from_playlist",
    "remove_media_path",
    "remove_user_from_playlist",
    "remove_user_from_session",
    "remove_virtual_folder",
    "rename_virtual_folder",
    "report_playback_progress",
    "report_playback_start",
    "report_playback_stopped",
    "report_session_ended",
    "report_viewing",
    "reset_tuner",
    "restart_application",
    "revoke_key",
    "search_remote_lyrics",
    "search_remote_subtitles",
    "send_full_general_command",
    "send_general_command",
    "send_message_command",
    "send_playstate_command",
    "send_system_command",
    "set_channel_mapping",
    "set_item_image",
    "set_item_image_by_index",
    "set_remote_access",
    "set_repositories",
    "shutdown_application",
    "start_restore_backup",
    "start_task",
    "stop_encoding_process",
    "stop_task",
    "sync_play_buffering",
    "sync_play_create_group",
    "sync_play_get_group",
    "sync_play_get_groups",
    "sync_play_join_group",
    "sync_play_leave_group",
    "sync_play_move_playlist_item",
    "sync_play_next_item",
    "sync_play_pause",
    "sync_play_ping",
    "sync_play_previous_item",
    "sync_play_queue",
    "sync_play_ready",
    "sync_play_remove_from_playlist",
    "sync_play_seek",
    "sync_play_set_ignore_wait",
    "sync_play_set_new_queue",
    "sync_play_set_playlist_item",
    "sync_play_set_repeat_mode",
    "sync_play_set_shuffle_mode",
    "sync_play_stop",
    "sync_play_unpause",
    "tmdb_client_configuration",
    "uninstall_plugin",
    "uninstall_plugin_by_version",
    "unmark_favorite_item",
    "update_branding_configuration",
    "update_configuration",
    "update_device_options",
    "update_display_preferences",
    "update_initial_configuration",
    "update_item",
    "update_item_content_type",
    "update_item_image_index",
    "update_item_user_data",
    "update_library_options",
    "update_media_path",
    "update_named_configuration",
    "update_playlist",
    "update_playlist_user",
    "update_plugin_configuration",
    "update_series_timer",
    "update_startup_user",
    "update_task",
    "update_timer",
    "update_user",
    "update_user_configuration",
    "update_user_item_rating",
    "update_user_password",
    "update_user_policy",
    "upload_custom_splashscreen",
    "upload_lyrics",
    "upload_subtitle",
    "validate_path",
]

__version__ = "2.1.0"

logger = get_logger(name="jellyfin-mcp")
logger.setLevel(logging.INFO)


def register_condensed_jellyfin_tools(mcp: FastMCP):
    """Register highly optimized, condensed tools mapping dynamically to Jellyfin client methods.

    Dynamic Tool Routing
    """

    @mcp.tool(tags={"Media"})
    async def jellyfin_media(
        action: _JELLYFIN_ACTIONS = Field(
            description="The media-related client method to execute. Examples: get_artists, get_artist_by_name, get_album_artists, get_audio_stream, get_audio_stream_by_container, get_genres, get_musicgenres, get_movies, get_playlists, get_playstate, get_subtitle, get_lyrics, get_trickplay, get_videos."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of keyword parameters to pass to the method.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute media playback, stream, artist, playlist, and audio/video queries dynamically.

        Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing media action: {action}...")
        try:
            kwargs = parse_json_object(params_json)
        except ValueError:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await dispatch_async(
                client, action, kwargs, service="jellyfin-mcp", ctx=ctx
            )
        except ValueError:
            return {"error": "Operation failed"}
        except Exception as e:
            return {"error": f"Media action failed: {type(e).__name__}"}

    @mcp.tool(tags={"Library"})
    async def jellyfin_library(
        action: _JELLYFIN_ACTIONS = Field(
            description="The library or search-related client method to execute. Examples: get_items, get_item_by_id, search_items, get_collections, create_collection, add_to_collection, remove_from_collection, get_library_info, get_user_views, get_user_library, get_library_structure, get_channels, get_channel_items, get_latest_channel_items."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of keyword parameters to pass to the method.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute library searches, items, collection updates, and catalog queries dynamically.

        Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing library action: {action}...")
        try:
            kwargs = parse_json_object(params_json)
        except ValueError:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await dispatch_async(
                client, action, kwargs, service="jellyfin-mcp", ctx=ctx
            )
        except ValueError:
            return {"error": "Operation failed"}
        except Exception as e:
            return {"error": f"Library action failed: {type(e).__name__}"}

    @mcp.tool(tags={"System"})
    async def jellyfin_system(
        action: _JELLYFIN_ACTIONS = Field(
            description="The administrative, system, or configuration-related client method to execute. Examples: get_log_entries, get_keys, create_key, revoke_key, get_system_info, get_users, get_devices, list_backups, create_backup, get_backup, start_restore_backup, get_branding_options, get_configuration, update_configuration, log_file."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of keyword parameters to pass to the method.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute administrative actions, system status, configurations, backups, and user management.

        Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing system action: {action}...")
        try:
            kwargs = parse_json_object(params_json)
        except ValueError:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await dispatch_async(
                client, action, kwargs, service="jellyfin-mcp", ctx=ctx
            )
        except ValueError:
            return {"error": "Operation failed"}
        except Exception as e:
            return {"error": f"System action failed: {type(e).__name__}"}


def register_kg_ingest_tools(mcp: FastMCP):
    """Register native epistemic-graph ingestion tools (Wire-First).

    CONCEPT:AU-KG.ingest.enterprise-source-extractor. Lists the real Jellyfin library
    via the client and pushes it into the knowledge graph as typed :MediaItem/:Book/
    :Artist/:Genre nodes (+ item overviews as :Document, + posters as :Blob).
    """

    @mcp.tool(tags={"misc", "kg"})
    async def jellyfin_ingest_library(
        params_json: str = Field(
            default="{}",
            description="JSON string of get_items filters (e.g. include_item_types, "
            "parent_id, limit, recursive).",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Natively ingest the Jellyfin library into epistemic-graph as typed nodes.

        Lists items via ``get_items`` and pushes them (with :hasGenre/:performedBy/
        :authoredBy links + item overviews as :Document) into the knowledge graph.
        Best-effort: ``ingested`` is ``None`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from jellyfin_mcp.kg_ingest import ingest_items

        try:
            kwargs = _json.loads(params_json) if params_json else {}
        except Exception:
            return {"error": "Operation failed"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            resp = await run_blocking(client.get_items, **kwargs)
        except Exception:
            return {"error": "get_items failed"}
        data = getattr(resp, "data", resp)
        items = data.get("Items", []) if isinstance(data, dict) else data
        items = items if isinstance(items, list) else [items]
        result = ingest_items(items)
        return {"listed": len(items), "ingested": result}

    @mcp.tool(tags={"misc", "kg"})
    async def jellyfin_ingest_posters(
        item_ids: list[str] = Field(
            default_factory=list,
            description="Jellyfin item Ids whose primary poster image to ingest as blobs.",
        ),
        image_type: str = Field(default="Primary", description="Jellyfin image type."),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest item posters as content-addressed :Blob + :AssetOccurrence (best-effort).

        CONCEPT:AU-KG.ingest.list-durable-media.
        """
        from jellyfin_mcp.kg_media import ingest_image_bytes, media_store

        store = media_store()
        stored: list[dict[str, Any]] = []
        for iid in item_ids or []:
            try:
                raw = await run_blocking(
                    client.get_item_image, item_id=iid, image_type=image_type
                )
            except Exception as e:
                logger.debug("Poster fetch failed: error_type=%s", type(e).__name__)
                continue
            data = raw if isinstance(raw, bytes) else None
            if data is None and isinstance(raw, str):
                data = raw.encode("latin-1", "ignore")
            res = ingest_image_bytes(
                data, item_id=iid, image_type=image_type, store=store
            )
            if res:
                stored.append(res)
        return {"requested": len(item_ids or []), "stored": stored}

    return None


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance.

    Dynamic Tool Routing
    """
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="jellyfin-mcp MCP",
        version=__version__,
        instructions="jellyfin-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="jellyfin-mcp",
        tools_module=sys.modules[__name__],
    )

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    """Run the MCP server.

    Dynamic Tool Routing
    """
    mcp, args, middlewares = get_mcp_instance()
    print(f"jellyfin-mcp MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
