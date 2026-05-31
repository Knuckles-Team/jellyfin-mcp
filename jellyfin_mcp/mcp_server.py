#!/usr/bin/python
"""Jellyfin MCP Server module.

Dynamic Tool Routing
"""

import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import sys
from typing import Any

from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from jellyfin_mcp.auth import get_client

__version__ = "0.34.0"

logger = get_logger(name="jellyfin-mcp")
logger.setLevel(logging.INFO)


def register_condensed_jellyfin_tools(mcp: FastMCP):
    """Register highly optimized, condensed tools mapping dynamically to Jellyfin client methods.

    Dynamic Tool Routing
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

        Dynamic Tool Routing
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

        Dynamic Tool Routing
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

        Dynamic Tool Routing
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


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance.

    Dynamic Tool Routing
    """
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="jellyfin-mcp MCP",
        version=__version__,
        instructions="jellyfin-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    # Always register optimized condensed tools
    register_condensed_jellyfin_tools(mcp)

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
