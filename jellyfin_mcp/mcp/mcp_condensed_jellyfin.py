"""MCP tools for condensed jellyfin operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from jellyfin_mcp.auth import get_client


def register_condensed_jellyfin_tools(mcp: FastMCP):
    """Register highly optimized, condensed tools mapping dynamically to Jellyfin client methods.

    CONCEPT:JELLYFIN-2.0 — Dynamic Tool Routing
    """

    @mcp.tool(tags={"Media"})
    async def jellyfin_media(
        action: str = Field(
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

        CONCEPT:JELLYFIN-2.0 — Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing media action: {action}...")
        import json

        try:
            kwargs = json.loads(params_json) if params_json else {}
        except Exception as e:
            return {"error": f"Invalid params_json JSON: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        method = getattr(client, action, None)
        if not method or not callable(method):
            return {"error": f"Unknown or invalid media action: {action}"}

        try:
            return method(**kwargs)
        except Exception as e:
            return {"error": f"Media action failed: {str(e)}"}

    @mcp.tool(tags={"Library"})
    async def jellyfin_library(
        action: str = Field(
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

        CONCEPT:JELLYFIN-2.0 — Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing library action: {action}...")
        import json

        try:
            kwargs = json.loads(params_json) if params_json else {}
        except Exception as e:
            return {"error": f"Invalid params_json JSON: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        method = getattr(client, action, None)
        if not method or not callable(method):
            return {"error": f"Unknown or invalid library action: {action}"}

        try:
            return method(**kwargs)
        except Exception as e:
            return {"error": f"Library action failed: {str(e)}"}

    @mcp.tool(tags={"System"})
    async def jellyfin_system(
        action: str = Field(
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

        CONCEPT:JELLYFIN-2.0 — Dynamic Tool Routing
        """
        if ctx and hasattr(ctx, "info"):
            await ctx.info(f"Executing system action: {action}...")
        import json

        try:
            kwargs = json.loads(params_json) if params_json else {}
        except Exception as e:
            return {"error": f"Invalid params_json JSON: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        method = getattr(client, action, None)
        if not method or not callable(method):
            return {"error": f"Unknown or invalid system action: {action}"}

        try:
            return method(**kwargs)
        except Exception as e:
            return {"error": f"System action failed: {str(e)}"}
