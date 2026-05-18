#!/usr/bin/python
import warnings

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
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from jellyfin_mcp.auth import get_client

__version__ = "0.12.0"

logger = get_logger(name="jellyfin-mcp")
logger.setLevel(logging.INFO)


def register_activitylog_tools(mcp: FastMCP):
    @mcp.tool(tags={"ActivityLog"})
    async def jellyfin_activitylog(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_log_entries'"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        min_date: str | None = Field(default=None, description="min date"),
        has_user_id: bool | None = Field(default=None, description="has user id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage activitylog operations.

        Actions:
          - 'get_log_entries': Gets activity log entries.
        """
        kwargs: dict[str, Any]
        if action == "get_log_entries":
            kwargs = {
                "start_index": start_index,
                "limit": limit,
                "min_date": min_date,
                "has_user_id": has_user_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_log_entries(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_log_entries")


def register_apikey_tools(mcp: FastMCP):
    @mcp.tool(tags={"ApiKey"})
    async def jellyfin_apikey(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_keys', 'create_key'"
        ),
        app: str | None = Field(default=None, description="app"),
        client=Depends(get_client),
    ) -> dict:
        """Manage apikey operations.

        Actions:
          - 'get_keys': Get all keys.
          - 'create_key': Create a new api key.
        """
        kwargs: dict[str, Any]
        if action == "get_keys":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_keys(**kwargs)
        if action == "create_key":
            kwargs = {"app": app}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_key(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_keys', 'create_key"
        )


def register_artists_tools(mcp: FastMCP):
    @mcp.tool(tags={"Artists"})
    async def jellyfin_artists(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_artists', 'get_artist_by_name', 'get_album_artists'"
        ),
        min_community_rating: float | None = Field(
            default=None, description="min community rating"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        search_term: str | None = Field(default=None, description="search term"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        filters: list[Any] | None = Field(default=None, description="filters"),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        media_types: list[Any] | None = Field(default=None, description="media types"),
        genres: list[Any] | None = Field(default=None, description="genres"),
        genre_ids: list[Any] | None = Field(default=None, description="genre ids"),
        official_ratings: list[Any] | None = Field(
            default=None, description="official ratings"
        ),
        tags: list[Any] | None = Field(default=None, description="tags"),
        years: list[Any] | None = Field(default=None, description="years"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        person: str | None = Field(default=None, description="person"),
        person_ids: list[Any] | None = Field(default=None, description="person ids"),
        person_types: list[Any] | None = Field(
            default=None, description="person types"
        ),
        studios: list[Any] | None = Field(default=None, description="studios"),
        studio_ids: list[Any] | None = Field(default=None, description="studio ids"),
        user_id: str | None = Field(default=None, description="user id"),
        name_starts_with_or_greater: str | None = Field(
            default=None, description="name starts with or greater"
        ),
        name_starts_with: str | None = Field(
            default=None, description="name starts with"
        ),
        name_less_than: str | None = Field(default=None, description="name less than"),
        sort_by: list[Any] | None = Field(default=None, description="sort by"),
        sort_order: list[Any] | None = Field(default=None, description="sort order"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        name: str | None = Field(default=None, description="name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage artists operations.

        Actions:
          - 'get_artists': Gets all artists from a given item, folder, or the entire library.
          - 'get_artist_by_name': Gets an artist by name.
          - 'get_album_artists': Gets all album artists from a given item, folder, or the entire library.
        """
        kwargs: dict[str, Any]
        if action == "get_artists":
            kwargs = {
                "min_community_rating": min_community_rating,
                "start_index": start_index,
                "limit": limit,
                "search_term": search_term,
                "parent_id": parent_id,
                "fields": fields,
                "exclude_item_types": exclude_item_types,
                "include_item_types": include_item_types,
                "filters": filters,
                "is_favorite": is_favorite,
                "media_types": media_types,
                "genres": genres,
                "genre_ids": genre_ids,
                "official_ratings": official_ratings,
                "tags": tags,
                "years": years,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "person": person,
                "person_ids": person_ids,
                "person_types": person_types,
                "studios": studios,
                "studio_ids": studio_ids,
                "user_id": user_id,
                "name_starts_with_or_greater": name_starts_with_or_greater,
                "name_starts_with": name_starts_with,
                "name_less_than": name_less_than,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "enable_images": enable_images,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_artists(**kwargs)
        if action == "get_artist_by_name":
            kwargs = {"name": name, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_artist_by_name(**kwargs)
        if action == "get_album_artists":
            kwargs = {
                "min_community_rating": min_community_rating,
                "start_index": start_index,
                "limit": limit,
                "search_term": search_term,
                "parent_id": parent_id,
                "fields": fields,
                "exclude_item_types": exclude_item_types,
                "include_item_types": include_item_types,
                "filters": filters,
                "is_favorite": is_favorite,
                "media_types": media_types,
                "genres": genres,
                "genre_ids": genre_ids,
                "official_ratings": official_ratings,
                "tags": tags,
                "years": years,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "person": person,
                "person_ids": person_ids,
                "person_types": person_types,
                "studios": studios,
                "studio_ids": studio_ids,
                "user_id": user_id,
                "name_starts_with_or_greater": name_starts_with_or_greater,
                "name_starts_with": name_starts_with,
                "name_less_than": name_less_than,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "enable_images": enable_images,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_album_artists(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_artists', 'get_artist_by_name', 'get_album_artists"
        )


def register_audio_tools(mcp: FastMCP):
    @mcp.tool(tags={"Audio"})
    async def jellyfin_audio(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_audio_stream', 'get_audio_stream_by_container'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        container: Any | None = Field(default=None, description="container"),
        static: bool | None = Field(default=None, description="static"),
        stream_params: str | None = Field(default=None, description="stream params"),
        tag: str | None = Field(default=None, description="tag"),
        device_profile_id: str | None = Field(
            default=None, description="device profile id"
        ),
        play_session_id: str | None = Field(
            default=None, description="play session id"
        ),
        segment_container: str | None = Field(
            default=None, description="segment container"
        ),
        segment_length: int | None = Field(default=None, description="segment length"),
        min_segments: int | None = Field(default=None, description="min segments"),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        device_id: str | None = Field(default=None, description="device id"),
        audio_codec: str | None = Field(default=None, description="audio codec"),
        enable_auto_stream_copy: bool | None = Field(
            default=None, description="enable auto stream copy"
        ),
        allow_video_stream_copy: bool | None = Field(
            default=None, description="allow video stream copy"
        ),
        allow_audio_stream_copy: bool | None = Field(
            default=None, description="allow audio stream copy"
        ),
        break_on_non_key_frames: bool | None = Field(
            default=None, description="break on non key frames"
        ),
        audio_sample_rate: int | None = Field(
            default=None, description="audio sample rate"
        ),
        max_audio_bit_depth: int | None = Field(
            default=None, description="max audio bit depth"
        ),
        audio_bit_rate: int | None = Field(default=None, description="audio bit rate"),
        audio_channels: int | None = Field(default=None, description="audio channels"),
        max_audio_channels: int | None = Field(
            default=None, description="max audio channels"
        ),
        profile: str | None = Field(default=None, description="profile"),
        level: str | None = Field(default=None, description="level"),
        framerate: float | None = Field(default=None, description="framerate"),
        max_framerate: float | None = Field(default=None, description="max framerate"),
        copy_timestamps: bool | None = Field(
            default=None, description="copy timestamps"
        ),
        start_time_ticks: int | None = Field(
            default=None, description="start time ticks"
        ),
        width: int | None = Field(default=None, description="width"),
        height: int | None = Field(default=None, description="height"),
        video_bit_rate: int | None = Field(default=None, description="video bit rate"),
        subtitle_stream_index: int | None = Field(
            default=None, description="subtitle stream index"
        ),
        subtitle_method: str | None = Field(
            default=None, description="subtitle method"
        ),
        max_ref_frames: int | None = Field(default=None, description="max ref frames"),
        max_video_bit_depth: int | None = Field(
            default=None, description="max video bit depth"
        ),
        require_avc: bool | None = Field(default=None, description="require avc"),
        de_interlace: bool | None = Field(default=None, description="de interlace"),
        require_non_anamorphic: bool | None = Field(
            default=None, description="require non anamorphic"
        ),
        transcoding_max_audio_channels: int | None = Field(
            default=None, description="transcoding max audio channels"
        ),
        cpu_core_limit: int | None = Field(default=None, description="cpu core limit"),
        live_stream_id: str | None = Field(default=None, description="live stream id"),
        enable_mpegts_m2_ts_mode: bool | None = Field(
            default=None, description="enable mpegts m2 ts mode"
        ),
        video_codec: str | None = Field(default=None, description="video codec"),
        subtitle_codec: str | None = Field(default=None, description="subtitle codec"),
        transcode_reasons: str | None = Field(
            default=None, description="transcode reasons"
        ),
        audio_stream_index: int | None = Field(
            default=None, description="audio stream index"
        ),
        video_stream_index: int | None = Field(
            default=None, description="video stream index"
        ),
        context: str | None = Field(default=None, description="context"),
        stream_options: dict[str, Any] | None = Field(
            default=None, description="stream options"
        ),
        enable_audio_vbr_encoding: bool | None = Field(
            default=None, description="enable audio vbr encoding"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage audio operations.

        Actions:
          - 'get_audio_stream': Gets an audio stream.
          - 'get_audio_stream_by_container': Gets an audio stream.
        """
        kwargs: dict[str, Any]
        if action == "get_audio_stream":
            kwargs = {
                "item_id": item_id,
                "container": container,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_audio_stream(**kwargs)
        if action == "get_audio_stream_by_container":
            kwargs = {
                "item_id": item_id,
                "container": container,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_audio_stream_by_container(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_audio_stream', 'get_audio_stream_by_container"
        )


def register_backup_tools(mcp: FastMCP):
    @mcp.tool(tags={"Backup"})
    async def jellyfin_backup(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_backups', 'create_backup', 'get_backup', 'start_restore_backup'"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        path: str | None = Field(default=None, description="path"),
        client=Depends(get_client),
    ) -> dict:
        """Manage backup operations.

        Actions:
          - 'list_backups': Gets a list of all currently present backups in the backup directory.
          - 'create_backup': Creates a new Backup.
          - 'get_backup': Gets the descriptor from an existing archive is present.
          - 'start_restore_backup': Restores to a backup by restarting the server and applying the backup.
        """
        kwargs: dict[str, Any]
        if action == "list_backups":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_backups(**kwargs)
        if action == "create_backup":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_backup(**kwargs)
        if action == "get_backup":
            kwargs = {"path": path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_backup(**kwargs)
        if action == "start_restore_backup":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.start_restore_backup(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_backups', 'create_backup', 'get_backup', 'start_restore_backup"
        )


def register_branding_tools(mcp: FastMCP):
    @mcp.tool(tags={"Branding"})
    async def jellyfin_branding(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_branding_options', 'get_branding_css', 'get_branding_css_2'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage branding operations.

        Actions:
          - 'get_branding_options': Gets branding configuration.
          - 'get_branding_css': Gets branding css.
          - 'get_branding_css_2': Gets branding css.
        """
        kwargs: dict[str, Any]
        if action == "get_branding_options":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_branding_options(**kwargs)
        if action == "get_branding_css":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_branding_css(**kwargs)
        if action == "get_branding_css_2":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_branding_css_2(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_branding_options', 'get_branding_css', 'get_branding_css_2"
        )


def register_channels_tools(mcp: FastMCP):
    @mcp.tool(tags={"Channels"})
    async def jellyfin_channels(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_channels', 'get_channel_features', 'get_channel_items', 'get_all_channel_features', 'get_latest_channel_items'"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        supports_latest_items: bool | None = Field(
            default=None, description="supports latest items"
        ),
        supports_media_deletion: bool | None = Field(
            default=None, description="supports media deletion"
        ),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        channel_id: str | None = Field(default=None, description="channel id"),
        folder_id: str | None = Field(default=None, description="folder id"),
        sort_order: list[Any] | None = Field(default=None, description="sort order"),
        filters: list[Any] | None = Field(default=None, description="filters"),
        sort_by: list[Any] | None = Field(default=None, description="sort by"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        channel_ids: list[Any] | None = Field(default=None, description="channel ids"),
        client=Depends(get_client),
    ) -> dict:
        """Manage channels operations.

        Actions:
          - 'get_channels': Gets available channels.
          - 'get_channel_features': Get channel features.
          - 'get_channel_items': Get channel items.
          - 'get_all_channel_features': Get all channel features.
          - 'get_latest_channel_items': Gets latest channel items.
        """
        kwargs: dict[str, Any]
        if action == "get_channels":
            kwargs = {
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "supports_latest_items": supports_latest_items,
                "supports_media_deletion": supports_media_deletion,
                "is_favorite": is_favorite,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_channels(**kwargs)
        if action == "get_channel_features":
            kwargs = {"channel_id": channel_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_channel_features(**kwargs)
        if action == "get_channel_items":
            kwargs = {
                "channel_id": channel_id,
                "folder_id": folder_id,
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "sort_order": sort_order,
                "filters": filters,
                "sort_by": sort_by,
                "fields": fields,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_channel_items(**kwargs)
        if action == "get_all_channel_features":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_channel_features(**kwargs)
        if action == "get_latest_channel_items":
            kwargs = {
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "filters": filters,
                "fields": fields,
                "channel_ids": channel_ids,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_latest_channel_items(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_channels', 'get_channel_features', 'get_channel_items', 'get_all_channel_features', 'get_latest_channel_items"
        )


def register_clientlog_tools(mcp: FastMCP):
    @mcp.tool(tags={"ClientLog"})
    async def jellyfin_clientlog(
        action: str = Field(
            description="Action to perform. Must be one of: 'log_file'"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage clientlog operations.

        Actions:
          - 'log_file': Upload a document.
        """
        kwargs: dict[str, Any]
        if action == "log_file":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.log_file(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: log_file")


def register_collection_tools(mcp: FastMCP):
    @mcp.tool(tags={"Collection"})
    async def jellyfin_collection(
        action: str = Field(
            description="Action to perform. Must be one of: 'create_collection', 'add_to_collection'"
        ),
        name: str | None = Field(default=None, description="name"),
        ids: list[Any] | None = Field(default=None, description="ids"),
        parent_id: str | None = Field(default=None, description="parent id"),
        is_locked: bool | None = Field(default=None, description="is locked"),
        collection_id: str | None = Field(default=None, description="collection id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage collection operations.

        Actions:
          - 'create_collection': Creates a new collection.
          - 'add_to_collection': Adds items to a collection.
        """
        kwargs: dict[str, Any]
        if action == "create_collection":
            kwargs = {
                "name": name,
                "ids": ids,
                "parent_id": parent_id,
                "is_locked": is_locked,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_collection(**kwargs)
        if action == "add_to_collection":
            kwargs = {"collection_id": collection_id, "ids": ids}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_to_collection(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: create_collection', 'add_to_collection"
        )


def register_configuration_tools(mcp: FastMCP):
    @mcp.tool(tags={"Configuration"})
    async def jellyfin_configuration(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_configuration', 'update_configuration', 'get_named_configuration', 'update_named_configuration', 'update_branding_configuration', 'get_default_metadata_options'"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        key: str | None = Field(default=None, description="key"),
        client=Depends(get_client),
    ) -> dict:
        """Manage configuration operations.

        Actions:
          - 'get_configuration': Gets application configuration.
          - 'update_configuration': Updates application configuration.
          - 'get_named_configuration': Gets a named configuration.
          - 'update_named_configuration': Updates named configuration.
          - 'update_branding_configuration': Updates branding configuration.
          - 'get_default_metadata_options': Gets a default MetadataOptions object.
        """
        kwargs: dict[str, Any]
        if action == "get_configuration":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_configuration(**kwargs)
        if action == "update_configuration":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_configuration(**kwargs)
        if action == "get_named_configuration":
            kwargs = {"key": key}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_named_configuration(**kwargs)
        if action == "update_named_configuration":
            kwargs = {"key": key, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_named_configuration(**kwargs)
        if action == "update_branding_configuration":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_branding_configuration(**kwargs)
        if action == "get_default_metadata_options":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_default_metadata_options(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_configuration', 'update_configuration', 'get_named_configuration', 'update_named_configuration', 'update_branding_configuration', 'get_default_metadata_options"
        )


def register_dashboard_tools(mcp: FastMCP):
    @mcp.tool(tags={"Dashboard"})
    async def jellyfin_dashboard(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_dashboard_configuration_page', 'get_configuration_pages'"
        ),
        name: str | None = Field(default=None, description="name"),
        enable_in_main_menu: bool | None = Field(
            default=None, description="enable in main menu"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage dashboard operations.

        Actions:
          - 'get_dashboard_configuration_page': Gets a dashboard configuration page.
          - 'get_configuration_pages': Gets the configuration pages.
        """
        kwargs: dict[str, Any]
        if action == "get_dashboard_configuration_page":
            kwargs = {"name": name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_dashboard_configuration_page(**kwargs)
        if action == "get_configuration_pages":
            kwargs = {"enable_in_main_menu": enable_in_main_menu}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_configuration_pages(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_dashboard_configuration_page', 'get_configuration_pages"
        )


def register_devices_tools(mcp: FastMCP):
    @mcp.tool(tags={"Devices"})
    async def jellyfin_devices(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_devices', 'get_device_info', 'get_device_options', 'update_device_options'"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        id: str | None = Field(default=None, description="id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage devices operations.

        Actions:
          - 'get_devices': Get Devices.
          - 'get_device_info': Get info for a device.
          - 'get_device_options': Get options for a device.
          - 'update_device_options': Update device options.
        """
        kwargs: dict[str, Any]
        if action == "get_devices":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_devices(**kwargs)
        if action == "get_device_info":
            kwargs = {"id": id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_device_info(**kwargs)
        if action == "get_device_options":
            kwargs = {"id": id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_device_options(**kwargs)
        if action == "update_device_options":
            kwargs = {"id": id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_device_options(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_devices', 'get_device_info', 'get_device_options', 'update_device_options"
        )


def register_displaypreferences_tools(mcp: FastMCP):
    @mcp.tool(tags={"DisplayPreferences"})
    async def jellyfin_displaypreferences(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_display_preferences', 'update_display_preferences'"
        ),
        display_preferences_id: str | None = Field(
            default=None, description="display preferences id"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        client_app: str | None = Field(default=None, description="client"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage displaypreferences operations.

        Actions:
          - 'get_display_preferences': Get Display Preferences.
          - 'update_display_preferences': Update Display Preferences.
        """
        kwargs: dict[str, Any]
        if action == "get_display_preferences":
            kwargs = {
                "display_preferences_id": display_preferences_id,
                "user_id": user_id,
                "client": client_app,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_display_preferences(**kwargs)
        if action == "update_display_preferences":
            kwargs = {
                "display_preferences_id": display_preferences_id,
                "user_id": user_id,
                "client": client_app,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_display_preferences(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_display_preferences', 'update_display_preferences"
        )


def register_dynamichls_tools(mcp: FastMCP):
    @mcp.tool(tags={"DynamicHls"})
    async def jellyfin_dynamichls(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_hls_audio_segment', 'get_variant_hls_audio_playlist', 'get_master_hls_audio_playlist', 'get_hls_video_segment', 'get_live_hls_stream', 'get_variant_hls_video_playlist', 'get_master_hls_video_playlist'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        playlist_id: str | None = Field(default=None, description="playlist id"),
        segment_id: int | None = Field(default=None, description="segment id"),
        container: Any | None = Field(default=None, description="container"),
        runtime_ticks: int | None = Field(default=None, description="runtime ticks"),
        actual_segment_length_ticks: int | None = Field(
            default=None, description="actual segment length ticks"
        ),
        static: bool | None = Field(default=None, description="static"),
        stream_params: str | None = Field(default=None, description="stream params"),
        tag: str | None = Field(default=None, description="tag"),
        device_profile_id: str | None = Field(
            default=None, description="device profile id"
        ),
        play_session_id: str | None = Field(
            default=None, description="play session id"
        ),
        segment_container: str | None = Field(
            default=None, description="segment container"
        ),
        segment_length: int | None = Field(default=None, description="segment length"),
        min_segments: int | None = Field(default=None, description="min segments"),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        device_id: str | None = Field(default=None, description="device id"),
        audio_codec: str | None = Field(default=None, description="audio codec"),
        enable_auto_stream_copy: bool | None = Field(
            default=None, description="enable auto stream copy"
        ),
        allow_video_stream_copy: bool | None = Field(
            default=None, description="allow video stream copy"
        ),
        allow_audio_stream_copy: bool | None = Field(
            default=None, description="allow audio stream copy"
        ),
        break_on_non_key_frames: bool | None = Field(
            default=None, description="break on non key frames"
        ),
        audio_sample_rate: int | None = Field(
            default=None, description="audio sample rate"
        ),
        max_audio_bit_depth: int | None = Field(
            default=None, description="max audio bit depth"
        ),
        max_streaming_bitrate: int | None = Field(
            default=None, description="max streaming bitrate"
        ),
        audio_bit_rate: int | None = Field(default=None, description="audio bit rate"),
        audio_channels: int | None = Field(default=None, description="audio channels"),
        max_audio_channels: int | None = Field(
            default=None, description="max audio channels"
        ),
        profile: str | None = Field(default=None, description="profile"),
        level: str | None = Field(default=None, description="level"),
        framerate: float | None = Field(default=None, description="framerate"),
        max_framerate: float | None = Field(default=None, description="max framerate"),
        copy_timestamps: bool | None = Field(
            default=None, description="copy timestamps"
        ),
        start_time_ticks: int | None = Field(
            default=None, description="start time ticks"
        ),
        width: int | None = Field(default=None, description="width"),
        height: int | None = Field(default=None, description="height"),
        video_bit_rate: int | None = Field(default=None, description="video bit rate"),
        subtitle_stream_index: int | None = Field(
            default=None, description="subtitle stream index"
        ),
        subtitle_method: str | None = Field(
            default=None, description="subtitle method"
        ),
        max_ref_frames: int | None = Field(default=None, description="max ref frames"),
        max_video_bit_depth: int | None = Field(
            default=None, description="max video bit depth"
        ),
        require_avc: bool | None = Field(default=None, description="require avc"),
        de_interlace: bool | None = Field(default=None, description="de interlace"),
        require_non_anamorphic: bool | None = Field(
            default=None, description="require non anamorphic"
        ),
        transcoding_max_audio_channels: int | None = Field(
            default=None, description="transcoding max audio channels"
        ),
        cpu_core_limit: int | None = Field(default=None, description="cpu core limit"),
        live_stream_id: str | None = Field(default=None, description="live stream id"),
        enable_mpegts_m2_ts_mode: bool | None = Field(
            default=None, description="enable mpegts m2 ts mode"
        ),
        video_codec: str | None = Field(default=None, description="video codec"),
        subtitle_codec: str | None = Field(default=None, description="subtitle codec"),
        transcode_reasons: str | None = Field(
            default=None, description="transcode reasons"
        ),
        audio_stream_index: int | None = Field(
            default=None, description="audio stream index"
        ),
        video_stream_index: int | None = Field(
            default=None, description="video stream index"
        ),
        context: str | None = Field(default=None, description="context"),
        stream_options: dict[str, Any] | None = Field(
            default=None, description="stream options"
        ),
        enable_audio_vbr_encoding: bool | None = Field(
            default=None, description="enable audio vbr encoding"
        ),
        enable_adaptive_bitrate_streaming: bool | None = Field(
            default=None, description="enable adaptive bitrate streaming"
        ),
        max_width: int | None = Field(default=None, description="max width"),
        max_height: int | None = Field(default=None, description="max height"),
        always_burn_in_subtitle_when_transcoding: bool | None = Field(
            default=None, description="always burn in subtitle when transcoding"
        ),
        enable_subtitles_in_manifest: bool | None = Field(
            default=None, description="enable subtitles in manifest"
        ),
        enable_trickplay: bool | None = Field(
            default=None, description="enable trickplay"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage dynamichls operations.

        Actions:
          - 'get_hls_audio_segment': Gets a video stream using HTTP live streaming.
          - 'get_variant_hls_audio_playlist': Gets an audio stream using HTTP live streaming.
          - 'get_master_hls_audio_playlist': Gets an audio hls playlist stream.
          - 'get_hls_video_segment': Gets a video stream using HTTP live streaming.
          - 'get_live_hls_stream': Gets a hls live stream.
          - 'get_variant_hls_video_playlist': Gets a video stream using HTTP live streaming.
          - 'get_master_hls_video_playlist': Gets a video hls playlist stream.
        """
        kwargs: dict[str, Any]
        if action == "get_hls_audio_segment":
            kwargs = {
                "item_id": item_id,
                "playlist_id": playlist_id,
                "segment_id": segment_id,
                "container": container,
                "runtime_ticks": runtime_ticks,
                "actual_segment_length_ticks": actual_segment_length_ticks,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "max_streaming_bitrate": max_streaming_bitrate,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_hls_audio_segment(**kwargs)
        if action == "get_variant_hls_audio_playlist":
            kwargs = {
                "item_id": item_id,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "max_streaming_bitrate": max_streaming_bitrate,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_variant_hls_audio_playlist(**kwargs)
        if action == "get_master_hls_audio_playlist":
            kwargs = {
                "item_id": item_id,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "max_streaming_bitrate": max_streaming_bitrate,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_adaptive_bitrate_streaming": enable_adaptive_bitrate_streaming,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_master_hls_audio_playlist(**kwargs)
        if action == "get_hls_video_segment":
            kwargs = {
                "item_id": item_id,
                "playlist_id": playlist_id,
                "segment_id": segment_id,
                "container": container,
                "runtime_ticks": runtime_ticks,
                "actual_segment_length_ticks": actual_segment_length_ticks,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "max_width": max_width,
                "max_height": max_height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
                "always_burn_in_subtitle_when_transcoding": always_burn_in_subtitle_when_transcoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_hls_video_segment(**kwargs)
        if action == "get_live_hls_stream":
            kwargs = {
                "item_id": item_id,
                "container": container,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "max_width": max_width,
                "max_height": max_height,
                "enable_subtitles_in_manifest": enable_subtitles_in_manifest,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
                "always_burn_in_subtitle_when_transcoding": always_burn_in_subtitle_when_transcoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_live_hls_stream(**kwargs)
        if action == "get_variant_hls_video_playlist":
            kwargs = {
                "item_id": item_id,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "max_width": max_width,
                "max_height": max_height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
                "always_burn_in_subtitle_when_transcoding": always_burn_in_subtitle_when_transcoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_variant_hls_video_playlist(**kwargs)
        if action == "get_master_hls_video_playlist":
            kwargs = {
                "item_id": item_id,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "max_width": max_width,
                "max_height": max_height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_adaptive_bitrate_streaming": enable_adaptive_bitrate_streaming,
                "enable_trickplay": enable_trickplay,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
                "always_burn_in_subtitle_when_transcoding": always_burn_in_subtitle_when_transcoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_master_hls_video_playlist(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_hls_audio_segment', 'get_variant_hls_audio_playlist', 'get_master_hls_audio_playlist', 'get_hls_video_segment', 'get_live_hls_stream', 'get_variant_hls_video_playlist', 'get_master_hls_video_playlist"
        )


def register_environment_tools(mcp: FastMCP):
    @mcp.tool(tags={"Environment"})
    async def jellyfin_environment(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_default_directory_browser', 'get_directory_contents', 'get_drives', 'get_network_shares', 'get_parent_path', 'validate_path'"
        ),
        path: str | None = Field(default=None, description="path"),
        include_files: bool | None = Field(default=None, description="include files"),
        include_directories: bool | None = Field(
            default=None, description="include directories"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage environment operations.

        Actions:
          - 'get_default_directory_browser': Get Default directory browser.
          - 'get_directory_contents': Gets the contents of a given directory in the file system.
          - 'get_drives': Gets available drives from the server's file system.
          - 'get_network_shares': Gets network paths.
          - 'get_parent_path': Gets the parent path of a given path.
          - 'validate_path': Validates path.
        """
        kwargs: dict[str, Any]
        if action == "get_default_directory_browser":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_default_directory_browser(**kwargs)
        if action == "get_directory_contents":
            kwargs = {
                "path": path,
                "include_files": include_files,
                "include_directories": include_directories,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_directory_contents(**kwargs)
        if action == "get_drives":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_drives(**kwargs)
        if action == "get_network_shares":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_network_shares(**kwargs)
        if action == "get_parent_path":
            kwargs = {"path": path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_parent_path(**kwargs)
        if action == "validate_path":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.validate_path(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_default_directory_browser', 'get_directory_contents', 'get_drives', 'get_network_shares', 'get_parent_path', 'validate_path"
        )


def register_filter_tools(mcp: FastMCP):
    @mcp.tool(tags={"Filter"})
    async def jellyfin_filter(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_query_filters_legacy', 'get_query_filters'"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        parent_id: str | None = Field(default=None, description="parent id"),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        media_types: list[Any] | None = Field(default=None, description="media types"),
        is_airing: bool | None = Field(default=None, description="is airing"),
        is_movie: bool | None = Field(default=None, description="is movie"),
        is_sports: bool | None = Field(default=None, description="is sports"),
        is_kids: bool | None = Field(default=None, description="is kids"),
        is_news: bool | None = Field(default=None, description="is news"),
        is_series: bool | None = Field(default=None, description="is series"),
        recursive: bool | None = Field(default=None, description="recursive"),
        client=Depends(get_client),
    ) -> dict:
        """Manage filter operations.

        Actions:
          - 'get_query_filters_legacy': Gets legacy query filters.
          - 'get_query_filters': Gets query filters.
        """
        kwargs: dict[str, Any]
        if action == "get_query_filters_legacy":
            kwargs = {
                "user_id": user_id,
                "parent_id": parent_id,
                "include_item_types": include_item_types,
                "media_types": media_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_query_filters_legacy(**kwargs)
        if action == "get_query_filters":
            kwargs = {
                "user_id": user_id,
                "parent_id": parent_id,
                "include_item_types": include_item_types,
                "is_airing": is_airing,
                "is_movie": is_movie,
                "is_sports": is_sports,
                "is_kids": is_kids,
                "is_news": is_news,
                "is_series": is_series,
                "recursive": recursive,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_query_filters(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_query_filters_legacy', 'get_query_filters"
        )


def register_genres_tools(mcp: FastMCP):
    @mcp.tool(tags={"Genres"})
    async def jellyfin_genres(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_genres', 'get_genre'"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        search_term: str | None = Field(default=None, description="search term"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        name_starts_with_or_greater: str | None = Field(
            default=None, description="name starts with or greater"
        ),
        name_starts_with: str | None = Field(
            default=None, description="name starts with"
        ),
        name_less_than: str | None = Field(default=None, description="name less than"),
        sort_by: list[Any] | None = Field(default=None, description="sort by"),
        sort_order: list[Any] | None = Field(default=None, description="sort order"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        genre_name: str | None = Field(default=None, description="genre name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage genres operations.

        Actions:
          - 'get_genres': Gets all genres from a given item, folder, or the entire library.
          - 'get_genre': Gets a genre, by name.
        """
        kwargs: dict[str, Any]
        if action == "get_genres":
            kwargs = {
                "start_index": start_index,
                "limit": limit,
                "search_term": search_term,
                "parent_id": parent_id,
                "fields": fields,
                "exclude_item_types": exclude_item_types,
                "include_item_types": include_item_types,
                "is_favorite": is_favorite,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "user_id": user_id,
                "name_starts_with_or_greater": name_starts_with_or_greater,
                "name_starts_with": name_starts_with,
                "name_less_than": name_less_than,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "enable_images": enable_images,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_genres(**kwargs)
        if action == "get_genre":
            kwargs = {"genre_name": genre_name, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_genre(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_genres', 'get_genre"
        )


def register_hlssegment_tools(mcp: FastMCP):
    @mcp.tool(tags={"HlsSegment"})
    async def jellyfin_hlssegment(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_hls_audio_segment_legacy_aac', 'get_hls_audio_segment_legacy_mp3', 'get_hls_video_segment_legacy', 'get_hls_playlist_legacy'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        segment_id: str | None = Field(default=None, description="segment id"),
        playlist_id: str | None = Field(default=None, description="playlist id"),
        segment_container: str | None = Field(
            default=None, description="segment container"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage hlssegment operations.

        Actions:
          - 'get_hls_audio_segment_legacy_aac': Gets the specified audio segment for an audio item.
          - 'get_hls_audio_segment_legacy_mp3': Gets the specified audio segment for an audio item.
          - 'get_hls_video_segment_legacy': Gets a hls video segment.
          - 'get_hls_playlist_legacy': Gets a hls video playlist.
        """
        kwargs: dict[str, Any]
        if action == "get_hls_audio_segment_legacy_aac":
            kwargs = {"item_id": item_id, "segment_id": segment_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_hls_audio_segment_legacy_aac(**kwargs)
        if action == "get_hls_audio_segment_legacy_mp3":
            kwargs = {"item_id": item_id, "segment_id": segment_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_hls_audio_segment_legacy_mp3(**kwargs)
        if action == "get_hls_video_segment_legacy":
            kwargs = {
                "item_id": item_id,
                "playlist_id": playlist_id,
                "segment_id": segment_id,
                "segment_container": segment_container,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_hls_video_segment_legacy(**kwargs)
        if action == "get_hls_playlist_legacy":
            kwargs = {"item_id": item_id, "playlist_id": playlist_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_hls_playlist_legacy(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_hls_audio_segment_legacy_aac', 'get_hls_audio_segment_legacy_mp3', 'get_hls_video_segment_legacy', 'get_hls_playlist_legacy"
        )


def register_image_tools(mcp: FastMCP):
    @mcp.tool(tags={"Image"})
    async def jellyfin_image(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_artist_image', 'get_splashscreen', 'get_genre_image', 'get_genre_image_by_index', 'get_item_image_infos', 'set_item_image', 'get_item_image', 'set_item_image_by_index', 'get_item_image_by_index', 'get_item_image2', 'update_item_image_index', 'get_music_genre_image', 'get_music_genre_image_by_index', 'get_person_image', 'get_person_image_by_index', 'get_studio_image', 'get_studio_image_by_index', 'post_user_image', 'get_user_image'"
        ),
        name: str | None = Field(default=None, description="name"),
        image_type: str | None = Field(default=None, description="image type"),
        image_index: Any | None = Field(default=None, description="image index"),
        tag: Any | None = Field(default=None, description="tag"),
        format: Any | None = Field(default=None, description="format"),
        max_width: Any | None = Field(default=None, description="max width"),
        max_height: Any | None = Field(default=None, description="max height"),
        percent_played: Any | None = Field(default=None, description="percent played"),
        unplayed_count: Any | None = Field(default=None, description="unplayed count"),
        width: int | None = Field(default=None, description="width"),
        height: int | None = Field(default=None, description="height"),
        quality: int | None = Field(default=None, description="quality"),
        fill_width: int | None = Field(default=None, description="fill width"),
        fill_height: int | None = Field(default=None, description="fill height"),
        blur: int | None = Field(default=None, description="blur"),
        background_color: str | None = Field(
            default=None, description="background color"
        ),
        foreground_layer: str | None = Field(
            default=None, description="foreground layer"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        new_index: int | None = Field(default=None, description="new index"),
        user_id: str | None = Field(default=None, description="user id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage image operations.

        Actions:
          - 'get_artist_image': Get artist image by name.
          - 'get_splashscreen': Generates or gets the splashscreen.
          - 'get_genre_image': Get genre image by name.
          - 'get_genre_image_by_index': Get genre image by name.
          - 'get_item_image_infos': Get item image infos.
          - 'set_item_image': Set item image.
          - 'get_item_image': Gets the item's image.
          - 'set_item_image_by_index': Set item image.
          - 'get_item_image_by_index': Gets the item's image.
          - 'get_item_image2': Gets the item's image.
          - 'update_item_image_index': Updates the index for an item image.
          - 'get_music_genre_image': Get music genre image by name.
          - 'get_music_genre_image_by_index': Get music genre image by name.
          - 'get_person_image': Get person image by name.
          - 'get_person_image_by_index': Get person image by name.
          - 'get_studio_image': Get studio image by name.
          - 'get_studio_image_by_index': Get studio image by name.
          - 'post_user_image': Sets the user image.
          - 'get_user_image': Get user profile image.
        """
        kwargs: dict[str, Any]
        if action == "get_artist_image":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "image_index": image_index,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_artist_image(**kwargs)
        if action == "get_splashscreen":
            kwargs = {"tag": tag, "format": format}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_splashscreen(**kwargs)
        if action == "get_genre_image":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
                "image_index": image_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_genre_image(**kwargs)
        if action == "get_genre_image_by_index":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "image_index": image_index,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_genre_image_by_index(**kwargs)
        if action == "get_item_image_infos":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item_image_infos(**kwargs)
        if action == "set_item_image":
            kwargs = {
                "item_id": item_id,
                "image_type": image_type,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_item_image(**kwargs)
        if action == "get_item_image":
            kwargs = {
                "item_id": item_id,
                "image_type": image_type,
                "max_width": max_width,
                "max_height": max_height,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "tag": tag,
                "format": format,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
                "image_index": image_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item_image(**kwargs)
        if action == "set_item_image_by_index":
            kwargs = {
                "item_id": item_id,
                "image_type": image_type,
                "image_index": image_index,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_item_image_by_index(**kwargs)
        if action == "get_item_image_by_index":
            kwargs = {
                "item_id": item_id,
                "image_type": image_type,
                "image_index": image_index,
                "max_width": max_width,
                "max_height": max_height,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "tag": tag,
                "format": format,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item_image_by_index(**kwargs)
        if action == "get_item_image2":
            kwargs = {
                "item_id": item_id,
                "image_type": image_type,
                "max_width": max_width,
                "max_height": max_height,
                "tag": tag,
                "format": format,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "image_index": image_index,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item_image2(**kwargs)
        if action == "update_item_image_index":
            kwargs = {
                "item_id": item_id,
                "image_type": image_type,
                "image_index": image_index,
                "new_index": new_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_item_image_index(**kwargs)
        if action == "get_music_genre_image":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
                "image_index": image_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_music_genre_image(**kwargs)
        if action == "get_music_genre_image_by_index":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "image_index": image_index,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_music_genre_image_by_index(**kwargs)
        if action == "get_person_image":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
                "image_index": image_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_person_image(**kwargs)
        if action == "get_person_image_by_index":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "image_index": image_index,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_person_image_by_index(**kwargs)
        if action == "get_studio_image":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
                "image_index": image_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_studio_image(**kwargs)
        if action == "get_studio_image_by_index":
            kwargs = {
                "name": name,
                "image_type": image_type,
                "image_index": image_index,
                "tag": tag,
                "format": format,
                "max_width": max_width,
                "max_height": max_height,
                "percent_played": percent_played,
                "unplayed_count": unplayed_count,
                "width": width,
                "height": height,
                "quality": quality,
                "fill_width": fill_width,
                "fill_height": fill_height,
                "blur": blur,
                "background_color": background_color,
                "foreground_layer": foreground_layer,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_studio_image_by_index(**kwargs)
        if action == "post_user_image":
            kwargs = {"user_id": user_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_user_image(**kwargs)
        if action == "get_user_image":
            kwargs = {"user_id": user_id, "tag": tag, "format": format}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_user_image(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_artist_image', 'get_splashscreen', 'get_genre_image', 'get_genre_image_by_index', 'get_item_image_infos', 'set_item_image', 'get_item_image', 'set_item_image_by_index', 'get_item_image_by_index', 'get_item_image2', 'update_item_image_index', 'get_music_genre_image', 'get_music_genre_image_by_index', 'get_person_image', 'get_person_image_by_index', 'get_studio_image', 'get_studio_image_by_index', 'post_user_image', 'get_user_image"
        )


def register_instantmix_tools(mcp: FastMCP):
    @mcp.tool(tags={"InstantMix"})
    async def jellyfin_instantmix(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_instant_mix_from_album', 'get_instant_mix_from_artists', 'get_instant_mix_from_artists2', 'get_instant_mix_from_item', 'get_instant_mix_from_music_genre_by_name', 'get_instant_mix_from_music_genre_by_id', 'get_instant_mix_from_playlist', 'get_instant_mix_from_song'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        user_id: str | None = Field(default=None, description="user id"),
        limit: int | None = Field(default=None, description="limit"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        id: str | None = Field(default=None, description="id"),
        name: str | None = Field(default=None, description="name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage instantmix operations.

        Actions:
          - 'get_instant_mix_from_album': Creates an instant playlist based on a given album.
          - 'get_instant_mix_from_artists': Creates an instant playlist based on a given artist.
          - 'get_instant_mix_from_artists2': Creates an instant playlist based on a given artist.
          - 'get_instant_mix_from_item': Creates an instant playlist based on a given item.
          - 'get_instant_mix_from_music_genre_by_name': Creates an instant playlist based on a given genre.
          - 'get_instant_mix_from_music_genre_by_id': Creates an instant playlist based on a given genre.
          - 'get_instant_mix_from_playlist': Creates an instant playlist based on a given playlist.
          - 'get_instant_mix_from_song': Creates an instant playlist based on a given song.
        """
        kwargs: dict[str, Any]
        if action == "get_instant_mix_from_album":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_album(**kwargs)
        if action == "get_instant_mix_from_artists":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_artists(**kwargs)
        if action == "get_instant_mix_from_artists2":
            kwargs = {
                "id": id,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_artists2(**kwargs)
        if action == "get_instant_mix_from_item":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_item(**kwargs)
        if action == "get_instant_mix_from_music_genre_by_name":
            kwargs = {
                "name": name,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_music_genre_by_name(**kwargs)
        if action == "get_instant_mix_from_music_genre_by_id":
            kwargs = {
                "id": id,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_music_genre_by_id(**kwargs)
        if action == "get_instant_mix_from_playlist":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_playlist(**kwargs)
        if action == "get_instant_mix_from_song":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_instant_mix_from_song(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_instant_mix_from_album', 'get_instant_mix_from_artists', 'get_instant_mix_from_artists2', 'get_instant_mix_from_item', 'get_instant_mix_from_music_genre_by_name', 'get_instant_mix_from_music_genre_by_id', 'get_instant_mix_from_playlist', 'get_instant_mix_from_song"
        )


def register_itemlookup_tools(mcp: FastMCP):
    @mcp.tool(tags={"ItemLookup"})
    async def jellyfin_itemlookup(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_external_id_infos', 'apply_search_criteria', 'get_book_remote_search_results', 'get_box_set_remote_search_results', 'get_movie_remote_search_results', 'get_music_album_remote_search_results', 'get_music_artist_remote_search_results', 'get_music_video_remote_search_results', 'get_person_remote_search_results', 'get_series_remote_search_results', 'get_trailer_remote_search_results'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        replace_all_images: bool | None = Field(
            default=None, description="replace all images"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage itemlookup operations.

        Actions:
          - 'get_external_id_infos': Get the item's external id info.
          - 'apply_search_criteria': Applies search criteria to an item and refreshes metadata.
          - 'get_book_remote_search_results': Get book remote search.
          - 'get_box_set_remote_search_results': Get box set remote search.
          - 'get_movie_remote_search_results': Get movie remote search.
          - 'get_music_album_remote_search_results': Get music album remote search.
          - 'get_music_artist_remote_search_results': Get music artist remote search.
          - 'get_music_video_remote_search_results': Get music video remote search.
          - 'get_person_remote_search_results': Get person remote search.
          - 'get_series_remote_search_results': Get series remote search.
          - 'get_trailer_remote_search_results': Get trailer remote search.
        """
        kwargs: dict[str, Any]
        if action == "get_external_id_infos":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_external_id_infos(**kwargs)
        if action == "apply_search_criteria":
            kwargs = {
                "item_id": item_id,
                "replace_all_images": replace_all_images,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.apply_search_criteria(**kwargs)
        if action == "get_book_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_book_remote_search_results(**kwargs)
        if action == "get_box_set_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_box_set_remote_search_results(**kwargs)
        if action == "get_movie_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_movie_remote_search_results(**kwargs)
        if action == "get_music_album_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_music_album_remote_search_results(**kwargs)
        if action == "get_music_artist_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_music_artist_remote_search_results(**kwargs)
        if action == "get_music_video_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_music_video_remote_search_results(**kwargs)
        if action == "get_person_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_person_remote_search_results(**kwargs)
        if action == "get_series_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_series_remote_search_results(**kwargs)
        if action == "get_trailer_remote_search_results":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_trailer_remote_search_results(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_external_id_infos', 'apply_search_criteria', 'get_book_remote_search_results', 'get_box_set_remote_search_results', 'get_movie_remote_search_results', 'get_music_album_remote_search_results', 'get_music_artist_remote_search_results', 'get_music_video_remote_search_results', 'get_person_remote_search_results', 'get_series_remote_search_results', 'get_trailer_remote_search_results"
        )


def register_itemrefresh_tools(mcp: FastMCP):
    @mcp.tool(tags={"ItemRefresh"})
    async def jellyfin_itemrefresh(
        action: str = Field(
            description="Action to perform. Must be one of: 'refresh_item'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        metadata_refresh_mode: str | None = Field(
            default=None, description="metadata refresh mode"
        ),
        image_refresh_mode: str | None = Field(
            default=None, description="image refresh mode"
        ),
        replace_all_metadata: bool | None = Field(
            default=None, description="replace all metadata"
        ),
        replace_all_images: bool | None = Field(
            default=None, description="replace all images"
        ),
        regenerate_trickplay: bool | None = Field(
            default=None, description="regenerate trickplay"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage itemrefresh operations.

        Actions:
          - 'refresh_item': Refreshes metadata for an item.
        """
        kwargs: dict[str, Any]
        if action == "refresh_item":
            kwargs = {
                "item_id": item_id,
                "metadata_refresh_mode": metadata_refresh_mode,
                "image_refresh_mode": image_refresh_mode,
                "replace_all_metadata": replace_all_metadata,
                "replace_all_images": replace_all_images,
                "regenerate_trickplay": regenerate_trickplay,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.refresh_item(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: refresh_item")


def register_items_tools(mcp: FastMCP):
    @mcp.tool(tags={"Items"})
    async def jellyfin_items(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_item_user_data', 'update_item_user_data', 'get_resume_items'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        user_id: str | None = Field(default=None, description="user id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        search_term: str | None = Field(default=None, description="search term"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        media_types: list[Any] | None = Field(default=None, description="media types"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        enable_images: bool | None = Field(default=None, description="enable images"),
        exclude_active_sessions: bool | None = Field(
            default=None, description="exclude active sessions"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage items operations.

        Actions:
          - 'get_item_user_data': Get Item User Data.
          - 'update_item_user_data': Update Item User Data.
          - 'get_resume_items': Gets items based on a query.
        """
        kwargs: dict[str, Any]
        if action == "get_item_user_data":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item_user_data(**kwargs)
        if action == "update_item_user_data":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_item_user_data(**kwargs)
        if action == "get_resume_items":
            kwargs = {
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "search_term": search_term,
                "parent_id": parent_id,
                "fields": fields,
                "media_types": media_types,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "exclude_item_types": exclude_item_types,
                "include_item_types": include_item_types,
                "enable_total_record_count": enable_total_record_count,
                "enable_images": enable_images,
                "exclude_active_sessions": exclude_active_sessions,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_resume_items(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_item_user_data', 'update_item_user_data', 'get_resume_items"
        )


def register_library_tools(mcp: FastMCP):
    @mcp.tool(tags={"Library"})
    async def jellyfin_library(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_similar_albums', 'get_similar_artists', 'get_ancestors', 'get_critic_reviews', 'get_file', 'get_similar_items', 'get_theme_media', 'get_theme_songs', 'get_theme_videos', 'get_item_counts', 'get_library_options_info', 'post_updated_media', 'get_media_folders', 'post_added_movies', 'post_updated_movies', 'get_physical_paths', 'refresh_library', 'post_added_series', 'post_updated_series', 'get_similar_movies', 'get_similar_shows', 'get_similar_trailers'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        exclude_artist_ids: list[Any] | None = Field(
            default=None, description="exclude artist ids"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        limit: int | None = Field(default=None, description="limit"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        inherit_from_parent: bool | None = Field(
            default=None, description="inherit from parent"
        ),
        sort_by: list[Any] | None = Field(default=None, description="sort by"),
        sort_order: list[Any] | None = Field(default=None, description="sort order"),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        library_content_type: str | None = Field(
            default=None, description="library content type"
        ),
        is_new_library: bool | None = Field(default=None, description="is new library"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        is_hidden: bool | None = Field(default=None, description="is hidden"),
        tmdb_id: str | None = Field(default=None, description="tmdb id"),
        imdb_id: str | None = Field(default=None, description="imdb id"),
        tvdb_id: str | None = Field(default=None, description="tvdb id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage library operations.

        Actions:
          - 'get_similar_albums': Gets similar items.
          - 'get_similar_artists': Gets similar items.
          - 'get_ancestors': Gets all parents of an item.
          - 'get_critic_reviews': Gets critic review for an item.
          - 'get_file': Get the original file of an item.
          - 'get_similar_items': Gets similar items.
          - 'get_theme_media': Get theme songs and videos for an item.
          - 'get_theme_songs': Get theme songs for an item.
          - 'get_theme_videos': Get theme videos for an item.
          - 'get_item_counts': Get item counts.
          - 'get_library_options_info': Gets the library options info.
          - 'post_updated_media': Reports that new movies have been added by an external source.
          - 'get_media_folders': Gets all user media folders.
          - 'post_added_movies': Reports that new movies have been added by an external source.
          - 'post_updated_movies': Reports that new movies have been added by an external source.
          - 'get_physical_paths': Gets a list of physical paths from virtual folders.
          - 'refresh_library': Starts a library scan.
          - 'post_added_series': Reports that new episodes of a series have been added by an external source.
          - 'post_updated_series': Reports that new episodes of a series have been added by an external source.
          - 'get_similar_movies': Gets similar items.
          - 'get_similar_shows': Gets similar items.
          - 'get_similar_trailers': Gets similar items.
        """
        kwargs: dict[str, Any]
        if action == "get_similar_albums":
            kwargs = {
                "item_id": item_id,
                "exclude_artist_ids": exclude_artist_ids,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_similar_albums(**kwargs)
        if action == "get_similar_artists":
            kwargs = {
                "item_id": item_id,
                "exclude_artist_ids": exclude_artist_ids,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_similar_artists(**kwargs)
        if action == "get_ancestors":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_ancestors(**kwargs)
        if action == "get_critic_reviews":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_critic_reviews(**kwargs)
        if action == "get_file":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_file(**kwargs)
        if action == "get_similar_items":
            kwargs = {
                "item_id": item_id,
                "exclude_artist_ids": exclude_artist_ids,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_similar_items(**kwargs)
        if action == "get_theme_media":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "inherit_from_parent": inherit_from_parent,
                "sort_by": sort_by,
                "sort_order": sort_order,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_theme_media(**kwargs)
        if action == "get_theme_songs":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "inherit_from_parent": inherit_from_parent,
                "sort_by": sort_by,
                "sort_order": sort_order,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_theme_songs(**kwargs)
        if action == "get_theme_videos":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "inherit_from_parent": inherit_from_parent,
                "sort_by": sort_by,
                "sort_order": sort_order,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_theme_videos(**kwargs)
        if action == "get_item_counts":
            kwargs = {"user_id": user_id, "is_favorite": is_favorite}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item_counts(**kwargs)
        if action == "get_library_options_info":
            kwargs = {
                "library_content_type": library_content_type,
                "is_new_library": is_new_library,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_library_options_info(**kwargs)
        if action == "post_updated_media":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_updated_media(**kwargs)
        if action == "get_media_folders":
            kwargs = {"is_hidden": is_hidden}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_media_folders(**kwargs)
        if action == "post_added_movies":
            kwargs = {"tmdb_id": tmdb_id, "imdb_id": imdb_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_added_movies(**kwargs)
        if action == "post_updated_movies":
            kwargs = {"tmdb_id": tmdb_id, "imdb_id": imdb_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_updated_movies(**kwargs)
        if action == "get_physical_paths":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_physical_paths(**kwargs)
        if action == "refresh_library":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.refresh_library(**kwargs)
        if action == "post_added_series":
            kwargs = {"tvdb_id": tvdb_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_added_series(**kwargs)
        if action == "post_updated_series":
            kwargs = {"tvdb_id": tvdb_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_updated_series(**kwargs)
        if action == "get_similar_movies":
            kwargs = {
                "item_id": item_id,
                "exclude_artist_ids": exclude_artist_ids,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_similar_movies(**kwargs)
        if action == "get_similar_shows":
            kwargs = {
                "item_id": item_id,
                "exclude_artist_ids": exclude_artist_ids,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_similar_shows(**kwargs)
        if action == "get_similar_trailers":
            kwargs = {
                "item_id": item_id,
                "exclude_artist_ids": exclude_artist_ids,
                "user_id": user_id,
                "limit": limit,
                "fields": fields,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_similar_trailers(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_similar_albums', 'get_similar_artists', 'get_ancestors', 'get_critic_reviews', 'get_file', 'get_similar_items', 'get_theme_media', 'get_theme_songs', 'get_theme_videos', 'get_item_counts', 'get_library_options_info', 'post_updated_media', 'get_media_folders', 'post_added_movies', 'post_updated_movies', 'get_physical_paths', 'refresh_library', 'post_added_series', 'post_updated_series', 'get_similar_movies', 'get_similar_shows', 'get_similar_trailers"
        )


def register_itemupdate_tools(mcp: FastMCP):
    @mcp.tool(tags={"ItemUpdate"})
    async def jellyfin_itemupdate(
        action: str = Field(
            description="Action to perform. Must be one of: 'update_item', 'update_item_content_type', 'get_metadata_editor_info'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        content_type: str | None = Field(default=None, description="content type"),
        client=Depends(get_client),
    ) -> dict:
        """Manage itemupdate operations.

        Actions:
          - 'update_item': Updates an item.
          - 'update_item_content_type': Updates an item's content type.
          - 'get_metadata_editor_info': Gets metadata editor info for an item.
        """
        kwargs: dict[str, Any]
        if action == "update_item":
            kwargs = {"item_id": item_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_item(**kwargs)
        if action == "update_item_content_type":
            kwargs = {"item_id": item_id, "content_type": content_type}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_item_content_type(**kwargs)
        if action == "get_metadata_editor_info":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_metadata_editor_info(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: update_item', 'update_item_content_type', 'get_metadata_editor_info"
        )


def register_userlibrary_tools(mcp: FastMCP):
    @mcp.tool(tags={"UserLibrary"})
    async def jellyfin_userlibrary(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_item', 'get_intros', 'get_local_trailers', 'get_special_features', 'get_latest_media', 'get_root_folder', 'mark_favorite_item', 'unmark_favorite_item', 'update_user_item_rating'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        user_id: str | None = Field(default=None, description="user id"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        is_played: bool | None = Field(default=None, description="is played"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        limit: int | None = Field(default=None, description="limit"),
        group_items: bool | None = Field(default=None, description="group items"),
        likes: bool | None = Field(default=None, description="likes"),
        client=Depends(get_client),
    ) -> dict:
        """Manage userlibrary operations.

        Actions:
          - 'get_item': Gets an item from a user's library.
          - 'get_intros': Gets intros to play before the main media item plays.
          - 'get_local_trailers': Gets local trailers for an item.
          - 'get_special_features': Gets special features for an item.
          - 'get_latest_media': Gets latest media.
          - 'get_root_folder': Gets the root folder from a user's library.
          - 'mark_favorite_item': Marks an item as a favorite.
          - 'unmark_favorite_item': Unmarks item as a favorite.
          - 'update_user_item_rating': Updates a user's rating for an item.
        """
        kwargs: dict[str, Any]
        if action == "get_item":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item(**kwargs)
        if action == "get_intros":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_intros(**kwargs)
        if action == "get_local_trailers":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_local_trailers(**kwargs)
        if action == "get_special_features":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_special_features(**kwargs)
        if action == "get_latest_media":
            kwargs = {
                "user_id": user_id,
                "parent_id": parent_id,
                "fields": fields,
                "include_item_types": include_item_types,
                "is_played": is_played,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "enable_user_data": enable_user_data,
                "limit": limit,
                "group_items": group_items,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_latest_media(**kwargs)
        if action == "get_root_folder":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_root_folder(**kwargs)
        if action == "mark_favorite_item":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.mark_favorite_item(**kwargs)
        if action == "unmark_favorite_item":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.unmark_favorite_item(**kwargs)
        if action == "update_user_item_rating":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "likes": likes,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user_item_rating(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_item', 'get_intros', 'get_local_trailers', 'get_special_features', 'get_latest_media', 'get_root_folder', 'mark_favorite_item', 'unmark_favorite_item', 'update_user_item_rating"
        )


def register_librarystructure_tools(mcp: FastMCP):
    @mcp.tool(tags={"LibraryStructure"})
    async def jellyfin_librarystructure(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_virtual_folders', 'add_virtual_folder', 'update_library_options', 'rename_virtual_folder', 'add_media_path', 'update_media_path'"
        ),
        name: str | None = Field(default=None, description="name"),
        collection_type: str | None = Field(
            default=None, description="collection type"
        ),
        paths: list[Any] | None = Field(default=None, description="paths"),
        refresh_library: bool | None = Field(
            default=None, description="refresh library"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        new_name: str | None = Field(default=None, description="new name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage librarystructure operations.

        Actions:
          - 'get_virtual_folders': Gets all virtual folders.
          - 'add_virtual_folder': Adds a virtual folder.
          - 'update_library_options': Update library options.
          - 'rename_virtual_folder': Renames a virtual folder.
          - 'add_media_path': Add a media path to a library.
          - 'update_media_path': Updates a media path.
        """
        kwargs: dict[str, Any]
        if action == "get_virtual_folders":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_virtual_folders(**kwargs)
        if action == "add_virtual_folder":
            kwargs = {
                "name": name,
                "collection_type": collection_type,
                "paths": paths,
                "refresh_library": refresh_library,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_virtual_folder(**kwargs)
        if action == "update_library_options":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_library_options(**kwargs)
        if action == "rename_virtual_folder":
            kwargs = {
                "name": name,
                "new_name": new_name,
                "refresh_library": refresh_library,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.rename_virtual_folder(**kwargs)
        if action == "add_media_path":
            kwargs = {"refresh_library": refresh_library, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_media_path(**kwargs)
        if action == "update_media_path":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_media_path(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_virtual_folders', 'add_virtual_folder', 'update_library_options', 'rename_virtual_folder', 'add_media_path', 'update_media_path"
        )


def register_livetv_tools(mcp: FastMCP):
    @mcp.tool(tags={"LiveTv"})
    async def jellyfin_livetv(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_channel_mapping_options', 'set_channel_mapping', 'get_live_tv_channels', 'get_channel', 'get_guide_info', 'get_live_tv_info', 'add_listing_provider', 'get_default_listing_provider', 'get_lineups', 'get_schedules_direct_countries', 'get_live_recording_file', 'get_live_stream_file', 'get_live_tv_programs', 'get_programs', 'get_program', 'get_recommended_programs', 'get_recordings', 'get_recording', 'get_recording_folders', 'get_recording_groups', 'get_recording_group', 'get_recordings_series', 'get_series_timers', 'create_series_timer', 'get_series_timer', 'update_series_timer', 'get_timers', 'create_timer', 'get_timer', 'update_timer', 'get_default_timer', 'add_tuner_host', 'get_tuner_host_types', 'discover_tuners', 'discvover_tuners'"
        ),
        provider_id: str | None = Field(default=None, description="provider id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        type: str | None = Field(default=None, description="type"),
        user_id: str | None = Field(default=None, description="user id"),
        start_index: int | None = Field(default=None, description="start index"),
        is_movie: bool | None = Field(default=None, description="is movie"),
        is_series: bool | None = Field(default=None, description="is series"),
        is_news: bool | None = Field(default=None, description="is news"),
        is_kids: bool | None = Field(default=None, description="is kids"),
        is_sports: bool | None = Field(default=None, description="is sports"),
        limit: int | None = Field(default=None, description="limit"),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        is_liked: bool | None = Field(default=None, description="is liked"),
        is_disliked: bool | None = Field(default=None, description="is disliked"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        fields: list[Any] | None = Field(default=None, description="fields"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        sort_by: Any | None = Field(default=None, description="sort by"),
        sort_order: Any | None = Field(default=None, description="sort order"),
        enable_favorite_sorting: bool | None = Field(
            default=None, description="enable favorite sorting"
        ),
        add_current_program: bool | None = Field(
            default=None, description="add current program"
        ),
        channel_id: Any | None = Field(default=None, description="channel id"),
        pw: str | None = Field(default=None, description="pw"),
        validate_listings: bool | None = Field(
            default=None, description="validate listings"
        ),
        validate_login: bool | None = Field(default=None, description="validate login"),
        id: str | None = Field(default=None, description="id"),
        location: str | None = Field(default=None, description="location"),
        country: str | None = Field(default=None, description="country"),
        recording_id: str | None = Field(default=None, description="recording id"),
        stream_id: str | None = Field(default=None, description="stream id"),
        container: str | None = Field(default=None, description="container"),
        channel_ids: list[Any] | None = Field(default=None, description="channel ids"),
        min_start_date: str | None = Field(default=None, description="min start date"),
        has_aired: bool | None = Field(default=None, description="has aired"),
        is_airing: bool | None = Field(default=None, description="is airing"),
        max_start_date: str | None = Field(default=None, description="max start date"),
        min_end_date: str | None = Field(default=None, description="min end date"),
        max_end_date: str | None = Field(default=None, description="max end date"),
        genres: list[Any] | None = Field(default=None, description="genres"),
        genre_ids: list[Any] | None = Field(default=None, description="genre ids"),
        series_timer_id: str | None = Field(
            default=None, description="series timer id"
        ),
        library_series_id: str | None = Field(
            default=None, description="library series id"
        ),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        program_id: Any | None = Field(default=None, description="program id"),
        status: str | None = Field(default=None, description="status"),
        is_in_progress: bool | None = Field(default=None, description="is in progress"),
        is_library_item: bool | None = Field(
            default=None, description="is library item"
        ),
        group_id: Any | None = Field(default=None, description="group id"),
        timer_id: str | None = Field(default=None, description="timer id"),
        is_active: bool | None = Field(default=None, description="is active"),
        is_scheduled: bool | None = Field(default=None, description="is scheduled"),
        new_devices_only: bool | None = Field(
            default=None, description="new devices only"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage livetv operations.

        Actions:
          - 'get_channel_mapping_options': Get channel mapping options.
          - 'set_channel_mapping': Set channel mappings.
          - 'get_live_tv_channels': Gets available live tv channels.
          - 'get_channel': Gets a live tv channel.
          - 'get_guide_info': Get guide info.
          - 'get_live_tv_info': Gets available live tv services.
          - 'add_listing_provider': Adds a listings provider.
          - 'get_default_listing_provider': Gets default listings provider info.
          - 'get_lineups': Gets available lineups.
          - 'get_schedules_direct_countries': Gets available countries.
          - 'get_live_recording_file': Gets a live tv recording stream.
          - 'get_live_stream_file': Gets a live tv channel stream.
          - 'get_live_tv_programs': Gets available live tv epgs.
          - 'get_programs': Gets available live tv epgs.
          - 'get_program': Gets a live tv program.
          - 'get_recommended_programs': Gets recommended live tv epgs.
          - 'get_recordings': Gets live tv recordings.
          - 'get_recording': Gets a live tv recording.
          - 'get_recording_folders': Gets recording folders.
          - 'get_recording_groups': Gets live tv recording groups.
          - 'get_recording_group': Get recording group.
          - 'get_recordings_series': Gets live tv recording series.
          - 'get_series_timers': Gets live tv series timers.
          - 'create_series_timer': Creates a live tv series timer.
          - 'get_series_timer': Gets a live tv series timer.
          - 'update_series_timer': Updates a live tv series timer.
          - 'get_timers': Gets the live tv timers.
          - 'create_timer': Creates a live tv timer.
          - 'get_timer': Gets a timer.
          - 'update_timer': Updates a live tv timer.
          - 'get_default_timer': Gets the default values for a new timer.
          - 'add_tuner_host': Adds a tuner host.
          - 'get_tuner_host_types': Get tuner host types.
          - 'discover_tuners': Discover tuners.
          - 'discvover_tuners': Discover tuners.
        """
        kwargs: dict[str, Any]
        if action == "get_channel_mapping_options":
            kwargs = {"provider_id": provider_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_channel_mapping_options(**kwargs)
        if action == "set_channel_mapping":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_channel_mapping(**kwargs)
        if action == "get_live_tv_channels":
            kwargs = {
                "type": type,
                "user_id": user_id,
                "start_index": start_index,
                "is_movie": is_movie,
                "is_series": is_series,
                "is_news": is_news,
                "is_kids": is_kids,
                "is_sports": is_sports,
                "limit": limit,
                "is_favorite": is_favorite,
                "is_liked": is_liked,
                "is_disliked": is_disliked,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "fields": fields,
                "enable_user_data": enable_user_data,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "enable_favorite_sorting": enable_favorite_sorting,
                "add_current_program": add_current_program,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_live_tv_channels(**kwargs)
        if action == "get_channel":
            kwargs = {"channel_id": channel_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_channel(**kwargs)
        if action == "get_guide_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_guide_info(**kwargs)
        if action == "get_live_tv_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_live_tv_info(**kwargs)
        if action == "add_listing_provider":
            kwargs = {
                "pw": pw,
                "validate_listings": validate_listings,
                "validate_login": validate_login,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_listing_provider(**kwargs)
        if action == "get_default_listing_provider":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_default_listing_provider(**kwargs)
        if action == "get_lineups":
            kwargs = {
                "id": id,
                "type": type,
                "location": location,
                "country": country,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_lineups(**kwargs)
        if action == "get_schedules_direct_countries":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_schedules_direct_countries(**kwargs)
        if action == "get_live_recording_file":
            kwargs = {"recording_id": recording_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_live_recording_file(**kwargs)
        if action == "get_live_stream_file":
            kwargs = {"stream_id": stream_id, "container": container}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_live_stream_file(**kwargs)
        if action == "get_live_tv_programs":
            kwargs = {
                "channel_ids": channel_ids,
                "user_id": user_id,
                "min_start_date": min_start_date,
                "has_aired": has_aired,
                "is_airing": is_airing,
                "max_start_date": max_start_date,
                "min_end_date": min_end_date,
                "max_end_date": max_end_date,
                "is_movie": is_movie,
                "is_series": is_series,
                "is_news": is_news,
                "is_kids": is_kids,
                "is_sports": is_sports,
                "start_index": start_index,
                "limit": limit,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "genres": genres,
                "genre_ids": genre_ids,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "enable_user_data": enable_user_data,
                "series_timer_id": series_timer_id,
                "library_series_id": library_series_id,
                "fields": fields,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_live_tv_programs(**kwargs)
        if action == "get_programs":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_programs(**kwargs)
        if action == "get_program":
            kwargs = {"program_id": program_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_program(**kwargs)
        if action == "get_recommended_programs":
            kwargs = {
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "is_airing": is_airing,
                "has_aired": has_aired,
                "is_series": is_series,
                "is_movie": is_movie,
                "is_news": is_news,
                "is_kids": is_kids,
                "is_sports": is_sports,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "genre_ids": genre_ids,
                "fields": fields,
                "enable_user_data": enable_user_data,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recommended_programs(**kwargs)
        if action == "get_recordings":
            kwargs = {
                "channel_id": channel_id,
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "status": status,
                "is_in_progress": is_in_progress,
                "series_timer_id": series_timer_id,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "fields": fields,
                "enable_user_data": enable_user_data,
                "is_movie": is_movie,
                "is_series": is_series,
                "is_kids": is_kids,
                "is_sports": is_sports,
                "is_news": is_news,
                "is_library_item": is_library_item,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recordings(**kwargs)
        if action == "get_recording":
            kwargs = {"recording_id": recording_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recording(**kwargs)
        if action == "get_recording_folders":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recording_folders(**kwargs)
        if action == "get_recording_groups":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recording_groups(**kwargs)
        if action == "get_recording_group":
            kwargs = {"group_id": group_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recording_group(**kwargs)
        if action == "get_recordings_series":
            kwargs = {
                "channel_id": channel_id,
                "user_id": user_id,
                "group_id": group_id,
                "start_index": start_index,
                "limit": limit,
                "status": status,
                "is_in_progress": is_in_progress,
                "series_timer_id": series_timer_id,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "fields": fields,
                "enable_user_data": enable_user_data,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recordings_series(**kwargs)
        if action == "get_series_timers":
            kwargs = {"sort_by": sort_by, "sort_order": sort_order}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_series_timers(**kwargs)
        if action == "create_series_timer":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_series_timer(**kwargs)
        if action == "get_series_timer":
            kwargs = {"timer_id": timer_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_series_timer(**kwargs)
        if action == "update_series_timer":
            kwargs = {"timer_id": timer_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_series_timer(**kwargs)
        if action == "get_timers":
            kwargs = {
                "channel_id": channel_id,
                "series_timer_id": series_timer_id,
                "is_active": is_active,
                "is_scheduled": is_scheduled,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_timers(**kwargs)
        if action == "create_timer":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_timer(**kwargs)
        if action == "get_timer":
            kwargs = {"timer_id": timer_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_timer(**kwargs)
        if action == "update_timer":
            kwargs = {"timer_id": timer_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_timer(**kwargs)
        if action == "get_default_timer":
            kwargs = {"program_id": program_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_default_timer(**kwargs)
        if action == "add_tuner_host":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_tuner_host(**kwargs)
        if action == "get_tuner_host_types":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_tuner_host_types(**kwargs)
        if action == "discover_tuners":
            kwargs = {"new_devices_only": new_devices_only}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.discover_tuners(**kwargs)
        if action == "discvover_tuners":
            kwargs = {"new_devices_only": new_devices_only}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.discvover_tuners(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_channel_mapping_options', 'set_channel_mapping', 'get_live_tv_channels', 'get_channel', 'get_guide_info', 'get_live_tv_info', 'add_listing_provider', 'get_default_listing_provider', 'get_lineups', 'get_schedules_direct_countries', 'get_live_recording_file', 'get_live_stream_file', 'get_live_tv_programs', 'get_programs', 'get_program', 'get_recommended_programs', 'get_recordings', 'get_recording', 'get_recording_folders', 'get_recording_groups', 'get_recording_group', 'get_recordings_series', 'get_series_timers', 'create_series_timer', 'get_series_timer', 'update_series_timer', 'get_timers', 'create_timer', 'get_timer', 'update_timer', 'get_default_timer', 'add_tuner_host', 'get_tuner_host_types', 'discover_tuners', 'discvover_tuners"
        )


def register_localization_tools(mcp: FastMCP):
    @mcp.tool(tags={"Localization"})
    async def jellyfin_localization(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_countries', 'get_cultures', 'get_localization_options', 'get_parental_ratings'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage localization operations.

        Actions:
          - 'get_countries': Gets known countries.
          - 'get_cultures': Gets known cultures.
          - 'get_localization_options': Gets localization options.
          - 'get_parental_ratings': Gets known parental ratings.
        """
        kwargs: dict[str, Any]
        if action == "get_countries":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_countries(**kwargs)
        if action == "get_cultures":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_cultures(**kwargs)
        if action == "get_localization_options":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_localization_options(**kwargs)
        if action == "get_parental_ratings":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_parental_ratings(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_countries', 'get_cultures', 'get_localization_options', 'get_parental_ratings"
        )


def register_lyrics_tools(mcp: FastMCP):
    @mcp.tool(tags={"Lyrics"})
    async def jellyfin_lyrics(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_lyrics', 'search_remote_lyrics', 'get_remote_lyrics'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        lyric_id: str | None = Field(default=None, description="lyric id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage lyrics operations.

        Actions:
          - 'get_lyrics': Gets an item's lyrics.
          - 'search_remote_lyrics': Search remote lyrics.
          - 'get_remote_lyrics': Gets the remote lyrics.
        """
        kwargs: dict[str, Any]
        if action == "get_lyrics":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_lyrics(**kwargs)
        if action == "search_remote_lyrics":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.search_remote_lyrics(**kwargs)
        if action == "get_remote_lyrics":
            kwargs = {"lyric_id": lyric_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_remote_lyrics(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_lyrics', 'search_remote_lyrics', 'get_remote_lyrics"
        )


def register_mediainfo_tools(mcp: FastMCP):
    @mcp.tool(tags={"MediaInfo"})
    async def jellyfin_mediainfo(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_playback_info', 'get_posted_playback_info', 'open_live_stream', 'get_bitrate_test_bytes'"
        ),
        item_id: Any | None = Field(default=None, description="item id"),
        user_id: str | None = Field(default=None, description="user id"),
        max_streaming_bitrate: int | None = Field(
            default=None, description="max streaming bitrate"
        ),
        start_time_ticks: int | None = Field(
            default=None, description="start time ticks"
        ),
        audio_stream_index: int | None = Field(
            default=None, description="audio stream index"
        ),
        subtitle_stream_index: int | None = Field(
            default=None, description="subtitle stream index"
        ),
        max_audio_channels: int | None = Field(
            default=None, description="max audio channels"
        ),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        live_stream_id: str | None = Field(default=None, description="live stream id"),
        auto_open_live_stream: bool | None = Field(
            default=None, description="auto open live stream"
        ),
        enable_direct_play: bool | None = Field(
            default=None, description="enable direct play"
        ),
        enable_direct_stream: bool | None = Field(
            default=None, description="enable direct stream"
        ),
        enable_transcoding: bool | None = Field(
            default=None, description="enable transcoding"
        ),
        allow_video_stream_copy: bool | None = Field(
            default=None, description="allow video stream copy"
        ),
        allow_audio_stream_copy: bool | None = Field(
            default=None, description="allow audio stream copy"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        open_token: str | None = Field(default=None, description="open token"),
        play_session_id: str | None = Field(
            default=None, description="play session id"
        ),
        always_burn_in_subtitle_when_transcoding: bool | None = Field(
            default=None, description="always burn in subtitle when transcoding"
        ),
        size: int | None = Field(default=None, description="size"),
        client=Depends(get_client),
    ) -> dict:
        """Manage mediainfo operations.

        Actions:
          - 'get_playback_info': Gets live playback media info for an item.
          - 'get_posted_playback_info': Gets live playback media info for an item.
          - 'open_live_stream': Opens a media source.
          - 'get_bitrate_test_bytes': Tests the network with a request with the size of the bitrate.
        """
        kwargs: dict[str, Any]
        if action == "get_playback_info":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_playback_info(**kwargs)
        if action == "get_posted_playback_info":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "max_streaming_bitrate": max_streaming_bitrate,
                "start_time_ticks": start_time_ticks,
                "audio_stream_index": audio_stream_index,
                "subtitle_stream_index": subtitle_stream_index,
                "max_audio_channels": max_audio_channels,
                "media_source_id": media_source_id,
                "live_stream_id": live_stream_id,
                "auto_open_live_stream": auto_open_live_stream,
                "enable_direct_play": enable_direct_play,
                "enable_direct_stream": enable_direct_stream,
                "enable_transcoding": enable_transcoding,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_posted_playback_info(**kwargs)
        if action == "open_live_stream":
            kwargs = {
                "open_token": open_token,
                "user_id": user_id,
                "play_session_id": play_session_id,
                "max_streaming_bitrate": max_streaming_bitrate,
                "start_time_ticks": start_time_ticks,
                "audio_stream_index": audio_stream_index,
                "subtitle_stream_index": subtitle_stream_index,
                "max_audio_channels": max_audio_channels,
                "item_id": item_id,
                "enable_direct_play": enable_direct_play,
                "enable_direct_stream": enable_direct_stream,
                "always_burn_in_subtitle_when_transcoding": always_burn_in_subtitle_when_transcoding,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.open_live_stream(**kwargs)
        if action == "get_bitrate_test_bytes":
            kwargs = {"size": size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_bitrate_test_bytes(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_playback_info', 'get_posted_playback_info', 'open_live_stream', 'get_bitrate_test_bytes"
        )


def register_mediasegments_tools(mcp: FastMCP):
    @mcp.tool(tags={"MediaSegments"})
    async def jellyfin_mediasegments(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_item_segments'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        include_segment_types: list[Any] | None = Field(
            default=None, description="include segment types"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage mediasegments operations.

        Actions:
          - 'get_item_segments': Gets all media segments based on an itemId.
        """
        kwargs: dict[str, Any]
        if action == "get_item_segments":
            kwargs = {
                "item_id": item_id,
                "include_segment_types": include_segment_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_item_segments(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_item_segments")


def register_movies_tools(mcp: FastMCP):
    @mcp.tool(tags={"Movies"})
    async def jellyfin_movies(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_movie_recommendations'"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        category_limit: int | None = Field(default=None, description="category limit"),
        item_limit: int | None = Field(default=None, description="item limit"),
        client=Depends(get_client),
    ) -> dict:
        """Manage movies operations.

        Actions:
          - 'get_movie_recommendations': Gets movie recommendations.
        """
        kwargs: dict[str, Any]
        if action == "get_movie_recommendations":
            kwargs = {
                "user_id": user_id,
                "parent_id": parent_id,
                "fields": fields,
                "category_limit": category_limit,
                "item_limit": item_limit,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_movie_recommendations(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_movie_recommendations"
        )


def register_musicgenres_tools(mcp: FastMCP):
    @mcp.tool(tags={"MusicGenres"})
    async def jellyfin_musicgenres(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_music_genres', 'get_music_genre'"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        search_term: str | None = Field(default=None, description="search term"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        name_starts_with_or_greater: str | None = Field(
            default=None, description="name starts with or greater"
        ),
        name_starts_with: str | None = Field(
            default=None, description="name starts with"
        ),
        name_less_than: str | None = Field(default=None, description="name less than"),
        sort_by: list[Any] | None = Field(default=None, description="sort by"),
        sort_order: list[Any] | None = Field(default=None, description="sort order"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        genre_name: str | None = Field(default=None, description="genre name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage musicgenres operations.

        Actions:
          - 'get_music_genres': Gets all music genres from a given item, folder, or the entire library.
          - 'get_music_genre': Gets a music genre, by name.
        """
        kwargs: dict[str, Any]
        if action == "get_music_genres":
            kwargs = {
                "start_index": start_index,
                "limit": limit,
                "search_term": search_term,
                "parent_id": parent_id,
                "fields": fields,
                "exclude_item_types": exclude_item_types,
                "include_item_types": include_item_types,
                "is_favorite": is_favorite,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "user_id": user_id,
                "name_starts_with_or_greater": name_starts_with_or_greater,
                "name_starts_with": name_starts_with,
                "name_less_than": name_less_than,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "enable_images": enable_images,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_music_genres(**kwargs)
        if action == "get_music_genre":
            kwargs = {"genre_name": genre_name, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_music_genre(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_music_genres', 'get_music_genre"
        )


def register_package_tools(mcp: FastMCP):
    @mcp.tool(tags={"Package"})
    async def jellyfin_package(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_packages', 'get_package_info', 'install_package', 'get_repositories', 'set_repositories'"
        ),
        name: str | None = Field(default=None, description="name"),
        assembly_guid: str | None = Field(default=None, description="assembly guid"),
        version: str | None = Field(default=None, description="version"),
        repository_url: str | None = Field(default=None, description="repository url"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage package operations.

        Actions:
          - 'get_packages': Gets available packages.
          - 'get_package_info': Gets a package by name or assembly GUID.
          - 'install_package': Installs a package.
          - 'get_repositories': Gets all package repositories.
          - 'set_repositories': Sets the enabled and existing package repositories.
        """
        kwargs: dict[str, Any]
        if action == "get_packages":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_packages(**kwargs)
        if action == "get_package_info":
            kwargs = {"name": name, "assembly_guid": assembly_guid}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_package_info(**kwargs)
        if action == "install_package":
            kwargs = {
                "name": name,
                "assembly_guid": assembly_guid,
                "version": version,
                "repository_url": repository_url,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.install_package(**kwargs)
        if action == "get_repositories":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_repositories(**kwargs)
        if action == "set_repositories":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_repositories(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_packages', 'get_package_info', 'install_package', 'get_repositories', 'set_repositories"
        )


def register_persons_tools(mcp: FastMCP):
    @mcp.tool(tags={"Persons"})
    async def jellyfin_persons(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_persons', 'get_person'"
        ),
        limit: int | None = Field(default=None, description="limit"),
        search_term: str | None = Field(default=None, description="search term"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        filters: list[Any] | None = Field(default=None, description="filters"),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        exclude_person_types: list[Any] | None = Field(
            default=None, description="exclude person types"
        ),
        person_types: list[Any] | None = Field(
            default=None, description="person types"
        ),
        appears_in_item_id: str | None = Field(
            default=None, description="appears in item id"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        name: str | None = Field(default=None, description="name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage persons operations.

        Actions:
          - 'get_persons': Gets all persons.
          - 'get_person': Get person by name.
        """
        kwargs: dict[str, Any]
        if action == "get_persons":
            kwargs = {
                "limit": limit,
                "search_term": search_term,
                "fields": fields,
                "filters": filters,
                "is_favorite": is_favorite,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "exclude_person_types": exclude_person_types,
                "person_types": person_types,
                "appears_in_item_id": appears_in_item_id,
                "user_id": user_id,
                "enable_images": enable_images,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_persons(**kwargs)
        if action == "get_person":
            kwargs = {"name": name, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_person(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_persons', 'get_person"
        )


def register_playlists_tools(mcp: FastMCP):
    @mcp.tool(tags={"Playlists"})
    async def jellyfin_playlists(
        action: str = Field(
            description="Action to perform. Must be one of: 'create_playlist', 'update_playlist', 'get_playlist', 'add_item_to_playlist', 'get_playlist_items', 'move_item', 'get_playlist_users', 'get_playlist_user', 'update_playlist_user'"
        ),
        name: str | None = Field(default=None, description="name"),
        ids: list[Any] | None = Field(default=None, description="ids"),
        user_id: Any | None = Field(default=None, description="user id"),
        media_type: str | None = Field(default=None, description="media type"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        playlist_id: str | None = Field(default=None, description="playlist id"),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        new_index: int | None = Field(default=None, description="new index"),
        client=Depends(get_client),
    ) -> dict:
        """Manage playlists operations.

        Actions:
          - 'create_playlist': Creates a new playlist.
          - 'update_playlist': Updates a playlist.
          - 'get_playlist': Get a playlist.
          - 'add_item_to_playlist': Adds items to a playlist.
          - 'get_playlist_items': Gets the original items of a playlist.
          - 'move_item': Moves a playlist item.
          - 'get_playlist_users': Get a playlist's users.
          - 'get_playlist_user': Get a playlist user.
          - 'update_playlist_user': Modify a user of a playlist's users.
        """
        kwargs: dict[str, Any]
        if action == "create_playlist":
            kwargs = {
                "name": name,
                "ids": ids,
                "user_id": user_id,
                "media_type": media_type,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_playlist(**kwargs)
        if action == "update_playlist":
            kwargs = {"playlist_id": playlist_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_playlist(**kwargs)
        if action == "get_playlist":
            kwargs = {"playlist_id": playlist_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_playlist(**kwargs)
        if action == "add_item_to_playlist":
            kwargs = {
                "playlist_id": playlist_id,
                "ids": ids,
                "user_id": user_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_item_to_playlist(**kwargs)
        if action == "get_playlist_items":
            kwargs = {
                "playlist_id": playlist_id,
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "fields": fields,
                "enable_images": enable_images,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_playlist_items(**kwargs)
        if action == "move_item":
            kwargs = {
                "playlist_id": playlist_id,
                "item_id": item_id,
                "new_index": new_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.move_item(**kwargs)
        if action == "get_playlist_users":
            kwargs = {"playlist_id": playlist_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_playlist_users(**kwargs)
        if action == "get_playlist_user":
            kwargs = {"playlist_id": playlist_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_playlist_user(**kwargs)
        if action == "update_playlist_user":
            kwargs = {
                "playlist_id": playlist_id,
                "user_id": user_id,
                "body": body,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_playlist_user(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: create_playlist', 'update_playlist', 'get_playlist', 'add_item_to_playlist', 'get_playlist_items', 'move_item', 'get_playlist_users', 'get_playlist_user', 'update_playlist_user"
        )


def register_playstate_tools(mcp: FastMCP):
    @mcp.tool(tags={"Playstate"})
    async def jellyfin_playstate(
        action: str = Field(
            description="Action to perform. Must be one of: 'on_playback_start', 'on_playback_progress', 'report_playback_start', 'ping_playback_session', 'report_playback_progress', 'mark_played_item', 'mark_unplayed_item'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        audio_stream_index: int | None = Field(
            default=None, description="audio stream index"
        ),
        subtitle_stream_index: int | None = Field(
            default=None, description="subtitle stream index"
        ),
        play_method: str | None = Field(default=None, description="play method"),
        live_stream_id: str | None = Field(default=None, description="live stream id"),
        play_session_id: str | None = Field(
            default=None, description="play session id"
        ),
        can_seek: bool | None = Field(default=None, description="can seek"),
        position_ticks: int | None = Field(default=None, description="position ticks"),
        volume_level: int | None = Field(default=None, description="volume level"),
        repeat_mode: str | None = Field(default=None, description="repeat mode"),
        is_paused: bool | None = Field(default=None, description="is paused"),
        is_muted: bool | None = Field(default=None, description="is muted"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        user_id: str | None = Field(default=None, description="user id"),
        date_played: str | None = Field(default=None, description="date played"),
        client=Depends(get_client),
    ) -> dict:
        """Manage playstate operations.

        Actions:
          - 'on_playback_start': Reports that a session has begun playing an item.
          - 'on_playback_progress': Reports a session's playback progress.
          - 'report_playback_start': Reports playback has started within a session.
          - 'ping_playback_session': Pings a playback session.
          - 'report_playback_progress': Reports playback progress within a session.
          - 'mark_played_item': Marks an item as played for user.
          - 'mark_unplayed_item': Marks an item as unplayed for user.
        """
        kwargs: dict[str, Any]
        if action == "on_playback_start":
            kwargs = {
                "item_id": item_id,
                "media_source_id": media_source_id,
                "audio_stream_index": audio_stream_index,
                "subtitle_stream_index": subtitle_stream_index,
                "play_method": play_method,
                "live_stream_id": live_stream_id,
                "play_session_id": play_session_id,
                "can_seek": can_seek,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.on_playback_start(**kwargs)
        if action == "on_playback_progress":
            kwargs = {
                "item_id": item_id,
                "media_source_id": media_source_id,
                "position_ticks": position_ticks,
                "audio_stream_index": audio_stream_index,
                "subtitle_stream_index": subtitle_stream_index,
                "volume_level": volume_level,
                "play_method": play_method,
                "live_stream_id": live_stream_id,
                "play_session_id": play_session_id,
                "repeat_mode": repeat_mode,
                "is_paused": is_paused,
                "is_muted": is_muted,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.on_playback_progress(**kwargs)
        if action == "report_playback_start":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.report_playback_start(**kwargs)
        if action == "ping_playback_session":
            kwargs = {"play_session_id": play_session_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.ping_playback_session(**kwargs)
        if action == "report_playback_progress":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.report_playback_progress(**kwargs)
        if action == "mark_played_item":
            kwargs = {
                "item_id": item_id,
                "user_id": user_id,
                "date_played": date_played,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.mark_played_item(**kwargs)
        if action == "mark_unplayed_item":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.mark_unplayed_item(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: on_playback_start', 'on_playback_progress', 'report_playback_start', 'ping_playback_session', 'report_playback_progress', 'mark_played_item', 'mark_unplayed_item"
        )


def register_plugins_tools(mcp: FastMCP):
    @mcp.tool(tags={"Plugins"})
    async def jellyfin_plugins(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_plugins', 'enable_plugin', 'get_plugin_image', 'get_plugin_configuration', 'update_plugin_configuration', 'get_plugin_manifest'"
        ),
        plugin_id: str | None = Field(default=None, description="plugin id"),
        version: str | None = Field(default=None, description="version"),
        client=Depends(get_client),
    ) -> dict:
        """Manage plugins operations.

        Actions:
          - 'get_plugins': Gets a list of currently installed plugins.
          - 'enable_plugin': Enables a disabled plugin.
          - 'get_plugin_image': Gets a plugin's image.
          - 'get_plugin_configuration': Gets plugin configuration.
          - 'update_plugin_configuration': Updates plugin configuration.
          - 'get_plugin_manifest': Gets a plugin's manifest.
        """
        kwargs: dict[str, Any]
        if action == "get_plugins":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_plugins(**kwargs)
        if action == "enable_plugin":
            kwargs = {"plugin_id": plugin_id, "version": version}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.enable_plugin(**kwargs)
        if action == "get_plugin_image":
            kwargs = {"plugin_id": plugin_id, "version": version}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_plugin_image(**kwargs)
        if action == "get_plugin_configuration":
            kwargs = {"plugin_id": plugin_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_plugin_configuration(**kwargs)
        if action == "update_plugin_configuration":
            kwargs = {"plugin_id": plugin_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_plugin_configuration(**kwargs)
        if action == "get_plugin_manifest":
            kwargs = {"plugin_id": plugin_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_plugin_manifest(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_plugins', 'enable_plugin', 'get_plugin_image', 'get_plugin_configuration', 'update_plugin_configuration', 'get_plugin_manifest"
        )


def register_quickconnect_tools(mcp: FastMCP):
    @mcp.tool(tags={"QuickConnect"})
    async def jellyfin_quickconnect(
        action: str = Field(
            description="Action to perform. Must be one of: 'authorize_quick_connect', 'get_quick_connect_state', 'get_quick_connect_enabled', 'initiate_quick_connect'"
        ),
        code: str | None = Field(default=None, description="code"),
        user_id: str | None = Field(default=None, description="user id"),
        secret: str | None = Field(default=None, description="secret"),
        client=Depends(get_client),
    ) -> dict:
        """Manage quickconnect operations.

        Actions:
          - 'authorize_quick_connect': Authorizes a pending quick connect request.
          - 'get_quick_connect_state': Attempts to retrieve authentication information.
          - 'get_quick_connect_enabled': Gets the current quick connect state.
          - 'initiate_quick_connect': Initiate a new quick connect request.
        """
        kwargs: dict[str, Any]
        if action == "authorize_quick_connect":
            kwargs = {"code": code, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.authorize_quick_connect(**kwargs)
        if action == "get_quick_connect_state":
            kwargs = {"secret": secret}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_quick_connect_state(**kwargs)
        if action == "get_quick_connect_enabled":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_quick_connect_enabled(**kwargs)
        if action == "initiate_quick_connect":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.initiate_quick_connect(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: authorize_quick_connect', 'get_quick_connect_state', 'get_quick_connect_enabled', 'initiate_quick_connect"
        )


def register_remoteimage_tools(mcp: FastMCP):
    @mcp.tool(tags={"RemoteImage"})
    async def jellyfin_remoteimage(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_remote_images', 'get_remote_image_providers'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        type: str | None = Field(default=None, description="type"),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        provider_name: str | None = Field(default=None, description="provider name"),
        include_all_languages: bool | None = Field(
            default=None, description="include all languages"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage remoteimage operations.

        Actions:
          - 'get_remote_images': Gets available remote images for an item.
          - 'get_remote_image_providers': Gets available remote image providers for an item.
        """
        kwargs: dict[str, Any]
        if action == "get_remote_images":
            kwargs = {
                "item_id": item_id,
                "type": type,
                "start_index": start_index,
                "limit": limit,
                "provider_name": provider_name,
                "include_all_languages": include_all_languages,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_remote_images(**kwargs)
        if action == "get_remote_image_providers":
            kwargs = {"item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_remote_image_providers(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_remote_images', 'get_remote_image_providers"
        )


def register_scheduledtasks_tools(mcp: FastMCP):
    @mcp.tool(tags={"ScheduledTasks"})
    async def jellyfin_scheduledtasks(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_tasks', 'get_task', 'update_task', 'start_task'"
        ),
        is_hidden: bool | None = Field(default=None, description="is hidden"),
        is_enabled: bool | None = Field(default=None, description="is enabled"),
        task_id: str | None = Field(default=None, description="task id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage scheduledtasks operations.

        Actions:
          - 'get_tasks': Get tasks.
          - 'get_task': Get task by id.
          - 'update_task': Update specified task triggers.
          - 'start_task': Start specified task.
        """
        kwargs: dict[str, Any]
        if action == "get_tasks":
            kwargs = {"is_hidden": is_hidden, "is_enabled": is_enabled}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_tasks(**kwargs)
        if action == "get_task":
            kwargs = {"task_id": task_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_task(**kwargs)
        if action == "update_task":
            kwargs = {"task_id": task_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_task(**kwargs)
        if action == "start_task":
            kwargs = {"task_id": task_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.start_task(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_tasks', 'get_task', 'update_task', 'start_task"
        )


def register_search_tools(mcp: FastMCP):
    @mcp.tool(tags={"Search"})
    async def jellyfin_search(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_search_hints'"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        user_id: str | None = Field(default=None, description="user id"),
        search_term: str | None = Field(default=None, description="search term"),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        media_types: list[Any] | None = Field(default=None, description="media types"),
        parent_id: str | None = Field(default=None, description="parent id"),
        is_movie: bool | None = Field(default=None, description="is movie"),
        is_series: bool | None = Field(default=None, description="is series"),
        is_news: bool | None = Field(default=None, description="is news"),
        is_kids: bool | None = Field(default=None, description="is kids"),
        is_sports: bool | None = Field(default=None, description="is sports"),
        include_people: bool | None = Field(default=None, description="include people"),
        include_media: bool | None = Field(default=None, description="include media"),
        include_genres: bool | None = Field(default=None, description="include genres"),
        include_studios: bool | None = Field(
            default=None, description="include studios"
        ),
        include_artists: bool | None = Field(
            default=None, description="include artists"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage search operations.

        Actions:
          - 'get_search_hints': Gets the search hint result.
        """
        kwargs: dict[str, Any]
        if action == "get_search_hints":
            kwargs = {
                "start_index": start_index,
                "limit": limit,
                "user_id": user_id,
                "search_term": search_term,
                "include_item_types": include_item_types,
                "exclude_item_types": exclude_item_types,
                "media_types": media_types,
                "parent_id": parent_id,
                "is_movie": is_movie,
                "is_series": is_series,
                "is_news": is_news,
                "is_kids": is_kids,
                "is_sports": is_sports,
                "include_people": include_people,
                "include_media": include_media,
                "include_genres": include_genres,
                "include_studios": include_studios,
                "include_artists": include_artists,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_search_hints(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_search_hints")


def register_session_tools(mcp: FastMCP):
    @mcp.tool(tags={"Session"})
    async def jellyfin_session(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_auth_providers', 'get_sessions', 'send_full_general_command', 'send_general_command', 'send_message_command', 'play', 'send_playstate_command', 'send_system_command', 'add_user_to_session', 'display_content', 'post_capabilities', 'post_full_capabilities', 'report_session_ended', 'report_viewing'"
        ),
        controllable_by_user_id: str | None = Field(
            default=None, description="controllable by user id"
        ),
        device_id: str | None = Field(default=None, description="device id"),
        active_within_seconds: int | None = Field(
            default=None, description="active within seconds"
        ),
        session_id: Any | None = Field(default=None, description="session id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        command: str | None = Field(default=None, description="command"),
        play_command: str | None = Field(default=None, description="play command"),
        item_ids: list[Any] | None = Field(default=None, description="item ids"),
        start_position_ticks: int | None = Field(
            default=None, description="start position ticks"
        ),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        audio_stream_index: int | None = Field(
            default=None, description="audio stream index"
        ),
        subtitle_stream_index: int | None = Field(
            default=None, description="subtitle stream index"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        seek_position_ticks: int | None = Field(
            default=None, description="seek position ticks"
        ),
        controlling_user_id: str | None = Field(
            default=None, description="controlling user id"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        item_type: str | None = Field(default=None, description="item type"),
        item_id: str | None = Field(default=None, description="item id"),
        item_name: str | None = Field(default=None, description="item name"),
        id: str | None = Field(default=None, description="id"),
        playable_media_types: list[Any] | None = Field(
            default=None, description="playable media types"
        ),
        supported_commands: list[Any] | None = Field(
            default=None, description="supported commands"
        ),
        supports_media_control: bool | None = Field(
            default=None, description="supports media control"
        ),
        supports_persistent_identifier: bool | None = Field(
            default=None, description="supports persistent identifier"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage session operations.

        Actions:
          - 'get_auth_providers': Get all auth providers.
          - 'get_sessions': Gets a list of sessions.
          - 'send_full_general_command': Issues a full general command to a client.
          - 'send_general_command': Issues a general command to a client.
          - 'send_message_command': Issues a command to a client to display a message to the user.
          - 'play': Instructs a session to play an item.
          - 'send_playstate_command': Issues a playstate command to a client.
          - 'send_system_command': Issues a system command to a client.
          - 'add_user_to_session': Adds an additional user to a session.
          - 'display_content': Instructs a session to browse to an item or view.
          - 'post_capabilities': Updates capabilities for a device.
          - 'post_full_capabilities': Updates capabilities for a device.
          - 'report_session_ended': Reports that a session has ended.
          - 'report_viewing': Reports that a session is viewing an item.
        """
        kwargs: dict[str, Any]
        if action == "get_auth_providers":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_auth_providers(**kwargs)
        if action == "get_sessions":
            kwargs = {
                "controllable_by_user_id": controllable_by_user_id,
                "device_id": device_id,
                "active_within_seconds": active_within_seconds,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_sessions(**kwargs)
        if action == "send_full_general_command":
            kwargs = {"session_id": session_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.send_full_general_command(**kwargs)
        if action == "send_general_command":
            kwargs = {"session_id": session_id, "command": command}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.send_general_command(**kwargs)
        if action == "send_message_command":
            kwargs = {"session_id": session_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.send_message_command(**kwargs)
        if action == "play":
            kwargs = {
                "session_id": session_id,
                "play_command": play_command,
                "item_ids": item_ids,
                "start_position_ticks": start_position_ticks,
                "media_source_id": media_source_id,
                "audio_stream_index": audio_stream_index,
                "subtitle_stream_index": subtitle_stream_index,
                "start_index": start_index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.play(**kwargs)
        if action == "send_playstate_command":
            kwargs = {
                "session_id": session_id,
                "command": command,
                "seek_position_ticks": seek_position_ticks,
                "controlling_user_id": controlling_user_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.send_playstate_command(**kwargs)
        if action == "send_system_command":
            kwargs = {"session_id": session_id, "command": command}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.send_system_command(**kwargs)
        if action == "add_user_to_session":
            kwargs = {"session_id": session_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_user_to_session(**kwargs)
        if action == "display_content":
            kwargs = {
                "session_id": session_id,
                "item_type": item_type,
                "item_id": item_id,
                "item_name": item_name,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.display_content(**kwargs)
        if action == "post_capabilities":
            kwargs = {
                "id": id,
                "playable_media_types": playable_media_types,
                "supported_commands": supported_commands,
                "supports_media_control": supports_media_control,
                "supports_persistent_identifier": supports_persistent_identifier,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_capabilities(**kwargs)
        if action == "post_full_capabilities":
            kwargs = {"id": id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_full_capabilities(**kwargs)
        if action == "report_session_ended":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.report_session_ended(**kwargs)
        if action == "report_viewing":
            kwargs = {"session_id": session_id, "item_id": item_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.report_viewing(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_auth_providers', 'get_sessions', 'send_full_general_command', 'send_general_command', 'send_message_command', 'play', 'send_playstate_command', 'send_system_command', 'add_user_to_session', 'display_content', 'post_capabilities', 'post_full_capabilities', 'report_session_ended', 'report_viewing"
        )


def register_startup_tools(mcp: FastMCP):
    @mcp.tool(tags={"Startup"})
    async def jellyfin_startup(
        action: str = Field(
            description="Action to perform. Must be one of: 'complete_wizard', 'get_startup_configuration', 'update_initial_configuration', 'get_first_user_2', 'set_remote_access', 'get_first_user', 'update_startup_user'"
        ),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage startup operations.

        Actions:
          - 'complete_wizard': Completes the startup wizard.
          - 'get_startup_configuration': Gets the initial startup wizard configuration.
          - 'update_initial_configuration': Sets the initial startup wizard configuration.
          - 'get_first_user_2': Gets the first user.
          - 'set_remote_access': Sets remote access and UPnP.
          - 'get_first_user': Gets the first user.
          - 'update_startup_user': Sets the user name and password.
        """
        kwargs: dict[str, Any]
        if action == "complete_wizard":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.complete_wizard(**kwargs)
        if action == "get_startup_configuration":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_startup_configuration(**kwargs)
        if action == "update_initial_configuration":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_initial_configuration(**kwargs)
        if action == "get_first_user_2":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_first_user_2(**kwargs)
        if action == "set_remote_access":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_remote_access(**kwargs)
        if action == "get_first_user":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_first_user(**kwargs)
        if action == "update_startup_user":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_startup_user(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: complete_wizard', 'get_startup_configuration', 'update_initial_configuration', 'get_first_user_2', 'set_remote_access', 'get_first_user', 'update_startup_user"
        )


def register_studios_tools(mcp: FastMCP):
    @mcp.tool(tags={"Studios"})
    async def jellyfin_studios(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_studios', 'get_studio'"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        search_term: str | None = Field(default=None, description="search term"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        name_starts_with_or_greater: str | None = Field(
            default=None, description="name starts with or greater"
        ),
        name_starts_with: str | None = Field(
            default=None, description="name starts with"
        ),
        name_less_than: str | None = Field(default=None, description="name less than"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        name: str | None = Field(default=None, description="name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage studios operations.

        Actions:
          - 'get_studios': Gets all studios from a given item, folder, or the entire library.
          - 'get_studio': Gets a studio by name.
        """
        kwargs: dict[str, Any]
        if action == "get_studios":
            kwargs = {
                "start_index": start_index,
                "limit": limit,
                "search_term": search_term,
                "parent_id": parent_id,
                "fields": fields,
                "exclude_item_types": exclude_item_types,
                "include_item_types": include_item_types,
                "is_favorite": is_favorite,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "user_id": user_id,
                "name_starts_with_or_greater": name_starts_with_or_greater,
                "name_starts_with": name_starts_with,
                "name_less_than": name_less_than,
                "enable_images": enable_images,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_studios(**kwargs)
        if action == "get_studio":
            kwargs = {"name": name, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_studio(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_studios', 'get_studio"
        )


def register_subtitle_tools(mcp: FastMCP):
    @mcp.tool(tags={"Subtitle"})
    async def jellyfin_subtitle(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_fallback_font_list', 'get_fallback_font', 'search_remote_subtitles', 'get_remote_subtitles', 'get_subtitle_playlist', 'get_subtitle_with_ticks', 'get_subtitle'"
        ),
        name: str | None = Field(default=None, description="name"),
        item_id: Any | None = Field(default=None, description="item id"),
        language: str | None = Field(default=None, description="language"),
        is_perfect_match: bool | None = Field(
            default=None, description="is perfect match"
        ),
        subtitle_id: str | None = Field(default=None, description="subtitle id"),
        index: Any | None = Field(default=None, description="index"),
        media_source_id: Any | None = Field(
            default=None, description="media source id"
        ),
        segment_length: int | None = Field(default=None, description="segment length"),
        route_item_id: str | None = Field(default=None, description="route item id"),
        route_media_source_id: str | None = Field(
            default=None, description="route media source id"
        ),
        route_index: int | None = Field(default=None, description="route index"),
        route_start_position_ticks: int | None = Field(
            default=None, description="route start position ticks"
        ),
        route_format: str | None = Field(default=None, description="route format"),
        start_position_ticks: int | None = Field(
            default=None, description="start position ticks"
        ),
        format: str | None = Field(default=None, description="format"),
        end_position_ticks: int | None = Field(
            default=None, description="end position ticks"
        ),
        copy_timestamps: bool | None = Field(
            default=None, description="copy timestamps"
        ),
        add_vtt_time_map: bool | None = Field(
            default=None, description="add vtt time map"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage subtitle operations.

        Actions:
          - 'get_fallback_font_list': Gets a list of available fallback font files.
          - 'get_fallback_font': Gets a fallback font file.
          - 'search_remote_subtitles': Search remote subtitles.
          - 'get_remote_subtitles': Gets the remote subtitles.
          - 'get_subtitle_playlist': Gets an HLS subtitle playlist.
          - 'get_subtitle_with_ticks': Gets subtitles in a specified format.
          - 'get_subtitle': Gets subtitles in a specified format.
        """
        kwargs: dict[str, Any]
        if action == "get_fallback_font_list":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_fallback_font_list(**kwargs)
        if action == "get_fallback_font":
            kwargs = {"name": name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_fallback_font(**kwargs)
        if action == "search_remote_subtitles":
            kwargs = {
                "item_id": item_id,
                "language": language,
                "is_perfect_match": is_perfect_match,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.search_remote_subtitles(**kwargs)
        if action == "get_remote_subtitles":
            kwargs = {"subtitle_id": subtitle_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_remote_subtitles(**kwargs)
        if action == "get_subtitle_playlist":
            kwargs = {
                "item_id": item_id,
                "index": index,
                "media_source_id": media_source_id,
                "segment_length": segment_length,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_subtitle_playlist(**kwargs)
        if action == "get_subtitle_with_ticks":
            kwargs = {
                "route_item_id": route_item_id,
                "route_media_source_id": route_media_source_id,
                "route_index": route_index,
                "route_start_position_ticks": route_start_position_ticks,
                "route_format": route_format,
                "item_id": item_id,
                "media_source_id": media_source_id,
                "index": index,
                "start_position_ticks": start_position_ticks,
                "format": format,
                "end_position_ticks": end_position_ticks,
                "copy_timestamps": copy_timestamps,
                "add_vtt_time_map": add_vtt_time_map,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_subtitle_with_ticks(**kwargs)
        if action == "get_subtitle":
            kwargs = {
                "route_item_id": route_item_id,
                "route_media_source_id": route_media_source_id,
                "route_index": route_index,
                "route_format": route_format,
                "item_id": item_id,
                "media_source_id": media_source_id,
                "index": index,
                "format": format,
                "end_position_ticks": end_position_ticks,
                "copy_timestamps": copy_timestamps,
                "add_vtt_time_map": add_vtt_time_map,
                "start_position_ticks": start_position_ticks,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_subtitle(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_fallback_font_list', 'get_fallback_font', 'search_remote_subtitles', 'get_remote_subtitles', 'get_subtitle_playlist', 'get_subtitle_with_ticks', 'get_subtitle"
        )


def register_suggestions_tools(mcp: FastMCP):
    @mcp.tool(tags={"Suggestions"})
    async def jellyfin_suggestions(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_suggestions'"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        media_type: list[Any] | None = Field(default=None, description="media type"),
        type: list[Any] | None = Field(default=None, description="type"),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage suggestions operations.

        Actions:
          - 'get_suggestions': Gets suggestions.
        """
        kwargs: dict[str, Any]
        if action == "get_suggestions":
            kwargs = {
                "user_id": user_id,
                "media_type": media_type,
                "type": type,
                "start_index": start_index,
                "limit": limit,
                "enable_total_record_count": enable_total_record_count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_suggestions(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_suggestions")


def register_system_tools(mcp: FastMCP):
    @mcp.tool(tags={"System"})
    async def jellyfin_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_endpoint_info', 'get_system_info', 'get_public_system_info', 'get_system_storage', 'get_server_logs', 'get_log_file', 'get_ping_system', 'post_ping_system'"
        ),
        name: str | None = Field(default=None, description="name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage system operations.

        Actions:
          - 'get_endpoint_info': Gets information about the request endpoint.
          - 'get_system_info': Gets information about the server.
          - 'get_public_system_info': Gets public information about the server.
          - 'get_system_storage': Gets information about the server.
          - 'get_server_logs': Gets a list of available server log files.
          - 'get_log_file': Gets a log file.
          - 'get_ping_system': Pings the system.
          - 'post_ping_system': Pings the system.
        """
        kwargs: dict[str, Any]
        if action == "get_endpoint_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_endpoint_info(**kwargs)
        if action == "get_system_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_system_info(**kwargs)
        if action == "get_public_system_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_public_system_info(**kwargs)
        if action == "get_system_storage":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_system_storage(**kwargs)
        if action == "get_server_logs":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_server_logs(**kwargs)
        if action == "get_log_file":
            kwargs = {"name": name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_log_file(**kwargs)
        if action == "get_ping_system":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_ping_system(**kwargs)
        if action == "post_ping_system":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_ping_system(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_endpoint_info', 'get_system_info', 'get_public_system_info', 'get_system_storage', 'get_server_logs', 'get_log_file', 'get_ping_system', 'post_ping_system"
        )


def register_timesync_tools(mcp: FastMCP):
    @mcp.tool(tags={"TimeSync"})
    async def jellyfin_timesync(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_utc_time'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage timesync operations.

        Actions:
          - 'get_utc_time': Gets the current UTC time.
        """
        kwargs: dict[str, Any]
        if action == "get_utc_time":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_utc_time(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_utc_time")


def register_tmdb_tools(mcp: FastMCP):
    @mcp.tool(tags={"Tmdb"})
    async def jellyfin_tmdb(
        action: str = Field(
            description="Action to perform. Must be one of: 'tmdb_client_configuration'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage tmdb operations.

        Actions:
          - 'tmdb_client_configuration': Gets the TMDb image configuration options.
        """
        kwargs: dict[str, Any]
        if action == "tmdb_client_configuration":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.tmdb_client_configuration(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: tmdb_client_configuration"
        )


def register_trailers_tools(mcp: FastMCP):
    @mcp.tool(tags={"Trailers"})
    async def jellyfin_trailers(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_trailers'"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        max_official_rating: str | None = Field(
            default=None, description="max official rating"
        ),
        has_theme_song: bool | None = Field(default=None, description="has theme song"),
        has_theme_video: bool | None = Field(
            default=None, description="has theme video"
        ),
        has_subtitles: bool | None = Field(default=None, description="has subtitles"),
        has_special_feature: bool | None = Field(
            default=None, description="has special feature"
        ),
        has_trailer: bool | None = Field(default=None, description="has trailer"),
        adjacent_to: str | None = Field(default=None, description="adjacent to"),
        parent_index_number: int | None = Field(
            default=None, description="parent index number"
        ),
        has_parental_rating: bool | None = Field(
            default=None, description="has parental rating"
        ),
        is_hd: bool | None = Field(default=None, description="is hd"),
        is4_k: bool | None = Field(default=None, description="is4 k"),
        location_types: list[Any] | None = Field(
            default=None, description="location types"
        ),
        exclude_location_types: list[Any] | None = Field(
            default=None, description="exclude location types"
        ),
        is_missing: bool | None = Field(default=None, description="is missing"),
        is_unaired: bool | None = Field(default=None, description="is unaired"),
        min_community_rating: float | None = Field(
            default=None, description="min community rating"
        ),
        min_critic_rating: float | None = Field(
            default=None, description="min critic rating"
        ),
        min_premiere_date: str | None = Field(
            default=None, description="min premiere date"
        ),
        min_date_last_saved: str | None = Field(
            default=None, description="min date last saved"
        ),
        min_date_last_saved_for_user: str | None = Field(
            default=None, description="min date last saved for user"
        ),
        max_premiere_date: str | None = Field(
            default=None, description="max premiere date"
        ),
        has_overview: bool | None = Field(default=None, description="has overview"),
        has_imdb_id: bool | None = Field(default=None, description="has imdb id"),
        has_tmdb_id: bool | None = Field(default=None, description="has tmdb id"),
        has_tvdb_id: bool | None = Field(default=None, description="has tvdb id"),
        is_movie: bool | None = Field(default=None, description="is movie"),
        is_series: bool | None = Field(default=None, description="is series"),
        is_news: bool | None = Field(default=None, description="is news"),
        is_kids: bool | None = Field(default=None, description="is kids"),
        is_sports: bool | None = Field(default=None, description="is sports"),
        exclude_item_ids: list[Any] | None = Field(
            default=None, description="exclude item ids"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        recursive: bool | None = Field(default=None, description="recursive"),
        search_term: str | None = Field(default=None, description="search term"),
        sort_order: list[Any] | None = Field(default=None, description="sort order"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        filters: list[Any] | None = Field(default=None, description="filters"),
        is_favorite: bool | None = Field(default=None, description="is favorite"),
        media_types: list[Any] | None = Field(default=None, description="media types"),
        image_types: list[Any] | None = Field(default=None, description="image types"),
        sort_by: list[Any] | None = Field(default=None, description="sort by"),
        is_played: bool | None = Field(default=None, description="is played"),
        genres: list[Any] | None = Field(default=None, description="genres"),
        official_ratings: list[Any] | None = Field(
            default=None, description="official ratings"
        ),
        tags: list[Any] | None = Field(default=None, description="tags"),
        years: list[Any] | None = Field(default=None, description="years"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        person: str | None = Field(default=None, description="person"),
        person_ids: list[Any] | None = Field(default=None, description="person ids"),
        person_types: list[Any] | None = Field(
            default=None, description="person types"
        ),
        studios: list[Any] | None = Field(default=None, description="studios"),
        artists: list[Any] | None = Field(default=None, description="artists"),
        exclude_artist_ids: list[Any] | None = Field(
            default=None, description="exclude artist ids"
        ),
        artist_ids: list[Any] | None = Field(default=None, description="artist ids"),
        album_artist_ids: list[Any] | None = Field(
            default=None, description="album artist ids"
        ),
        contributing_artist_ids: list[Any] | None = Field(
            default=None, description="contributing artist ids"
        ),
        albums: list[Any] | None = Field(default=None, description="albums"),
        album_ids: list[Any] | None = Field(default=None, description="album ids"),
        ids: list[Any] | None = Field(default=None, description="ids"),
        video_types: list[Any] | None = Field(default=None, description="video types"),
        min_official_rating: str | None = Field(
            default=None, description="min official rating"
        ),
        is_locked: bool | None = Field(default=None, description="is locked"),
        is_place_holder: bool | None = Field(
            default=None, description="is place holder"
        ),
        has_official_rating: bool | None = Field(
            default=None, description="has official rating"
        ),
        collapse_box_set_items: bool | None = Field(
            default=None, description="collapse box set items"
        ),
        min_width: int | None = Field(default=None, description="min width"),
        min_height: int | None = Field(default=None, description="min height"),
        max_width: int | None = Field(default=None, description="max width"),
        max_height: int | None = Field(default=None, description="max height"),
        is3_d: bool | None = Field(default=None, description="is3 d"),
        series_status: list[Any] | None = Field(
            default=None, description="series status"
        ),
        name_starts_with_or_greater: str | None = Field(
            default=None, description="name starts with or greater"
        ),
        name_starts_with: str | None = Field(
            default=None, description="name starts with"
        ),
        name_less_than: str | None = Field(default=None, description="name less than"),
        studio_ids: list[Any] | None = Field(default=None, description="studio ids"),
        genre_ids: list[Any] | None = Field(default=None, description="genre ids"),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        enable_images: bool | None = Field(default=None, description="enable images"),
        client=Depends(get_client),
    ) -> dict:
        """Manage trailers operations.

        Actions:
          - 'get_trailers': Finds movies and trailers similar to a given trailer.
        """
        kwargs: dict[str, Any]
        if action == "get_trailers":
            kwargs = {
                "user_id": user_id,
                "max_official_rating": max_official_rating,
                "has_theme_song": has_theme_song,
                "has_theme_video": has_theme_video,
                "has_subtitles": has_subtitles,
                "has_special_feature": has_special_feature,
                "has_trailer": has_trailer,
                "adjacent_to": adjacent_to,
                "parent_index_number": parent_index_number,
                "has_parental_rating": has_parental_rating,
                "is_hd": is_hd,
                "is4_k": is4_k,
                "location_types": location_types,
                "exclude_location_types": exclude_location_types,
                "is_missing": is_missing,
                "is_unaired": is_unaired,
                "min_community_rating": min_community_rating,
                "min_critic_rating": min_critic_rating,
                "min_premiere_date": min_premiere_date,
                "min_date_last_saved": min_date_last_saved,
                "min_date_last_saved_for_user": min_date_last_saved_for_user,
                "max_premiere_date": max_premiere_date,
                "has_overview": has_overview,
                "has_imdb_id": has_imdb_id,
                "has_tmdb_id": has_tmdb_id,
                "has_tvdb_id": has_tvdb_id,
                "is_movie": is_movie,
                "is_series": is_series,
                "is_news": is_news,
                "is_kids": is_kids,
                "is_sports": is_sports,
                "exclude_item_ids": exclude_item_ids,
                "start_index": start_index,
                "limit": limit,
                "recursive": recursive,
                "search_term": search_term,
                "sort_order": sort_order,
                "parent_id": parent_id,
                "fields": fields,
                "exclude_item_types": exclude_item_types,
                "filters": filters,
                "is_favorite": is_favorite,
                "media_types": media_types,
                "image_types": image_types,
                "sort_by": sort_by,
                "is_played": is_played,
                "genres": genres,
                "official_ratings": official_ratings,
                "tags": tags,
                "years": years,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "person": person,
                "person_ids": person_ids,
                "person_types": person_types,
                "studios": studios,
                "artists": artists,
                "exclude_artist_ids": exclude_artist_ids,
                "artist_ids": artist_ids,
                "album_artist_ids": album_artist_ids,
                "contributing_artist_ids": contributing_artist_ids,
                "albums": albums,
                "album_ids": album_ids,
                "ids": ids,
                "video_types": video_types,
                "min_official_rating": min_official_rating,
                "is_locked": is_locked,
                "is_place_holder": is_place_holder,
                "has_official_rating": has_official_rating,
                "collapse_box_set_items": collapse_box_set_items,
                "min_width": min_width,
                "min_height": min_height,
                "max_width": max_width,
                "max_height": max_height,
                "is3_d": is3_d,
                "series_status": series_status,
                "name_starts_with_or_greater": name_starts_with_or_greater,
                "name_starts_with": name_starts_with,
                "name_less_than": name_less_than,
                "studio_ids": studio_ids,
                "genre_ids": genre_ids,
                "enable_total_record_count": enable_total_record_count,
                "enable_images": enable_images,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_trailers(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_trailers")


def register_trickplay_tools(mcp: FastMCP):
    @mcp.tool(tags={"Trickplay"})
    async def jellyfin_trickplay(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_trickplay_tile_image', 'get_trickplay_hls_playlist'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        width: int | None = Field(default=None, description="width"),
        index: int | None = Field(default=None, description="index"),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage trickplay operations.

        Actions:
          - 'get_trickplay_tile_image': Gets a trickplay tile image.
          - 'get_trickplay_hls_playlist': Gets an image tiles playlist for trickplay.
        """
        kwargs: dict[str, Any]
        if action == "get_trickplay_tile_image":
            kwargs = {
                "item_id": item_id,
                "width": width,
                "index": index,
                "media_source_id": media_source_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_trickplay_tile_image(**kwargs)
        if action == "get_trickplay_hls_playlist":
            kwargs = {
                "item_id": item_id,
                "width": width,
                "media_source_id": media_source_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_trickplay_hls_playlist(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_trickplay_tile_image', 'get_trickplay_hls_playlist"
        )


def register_tvshows_tools(mcp: FastMCP):
    @mcp.tool(tags={"TvShows"})
    async def jellyfin_tvshows(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_episodes', 'get_seasons', 'get_next_up', 'get_upcoming_episodes'"
        ),
        series_id: Any | None = Field(default=None, description="series id"),
        user_id: str | None = Field(default=None, description="user id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        season: int | None = Field(default=None, description="season"),
        season_id: str | None = Field(default=None, description="season id"),
        is_missing: bool | None = Field(default=None, description="is missing"),
        adjacent_to: str | None = Field(default=None, description="adjacent to"),
        start_item_id: str | None = Field(default=None, description="start item id"),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        sort_by: str | None = Field(default=None, description="sort by"),
        is_special_season: bool | None = Field(
            default=None, description="is special season"
        ),
        parent_id: str | None = Field(default=None, description="parent id"),
        next_up_date_cutoff: str | None = Field(
            default=None, description="next up date cutoff"
        ),
        enable_total_record_count: bool | None = Field(
            default=None, description="enable total record count"
        ),
        disable_first_episode: bool | None = Field(
            default=None, description="disable first episode"
        ),
        enable_resumable: bool | None = Field(
            default=None, description="enable resumable"
        ),
        enable_rewatching: bool | None = Field(
            default=None, description="enable rewatching"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage tvshows operations.

        Actions:
          - 'get_episodes': Gets episodes for a tv season.
          - 'get_seasons': Gets seasons for a tv series.
          - 'get_next_up': Gets a list of next up episodes.
          - 'get_upcoming_episodes': Gets a list of upcoming episodes.
        """
        kwargs: dict[str, Any]
        if action == "get_episodes":
            kwargs = {
                "series_id": series_id,
                "user_id": user_id,
                "fields": fields,
                "season": season,
                "season_id": season_id,
                "is_missing": is_missing,
                "adjacent_to": adjacent_to,
                "start_item_id": start_item_id,
                "start_index": start_index,
                "limit": limit,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "enable_user_data": enable_user_data,
                "sort_by": sort_by,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_episodes(**kwargs)
        if action == "get_seasons":
            kwargs = {
                "series_id": series_id,
                "user_id": user_id,
                "fields": fields,
                "is_special_season": is_special_season,
                "is_missing": is_missing,
                "adjacent_to": adjacent_to,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "enable_user_data": enable_user_data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_seasons(**kwargs)
        if action == "get_next_up":
            kwargs = {
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "fields": fields,
                "series_id": series_id,
                "parent_id": parent_id,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "enable_user_data": enable_user_data,
                "next_up_date_cutoff": next_up_date_cutoff,
                "enable_total_record_count": enable_total_record_count,
                "disable_first_episode": disable_first_episode,
                "enable_resumable": enable_resumable,
                "enable_rewatching": enable_rewatching,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_next_up(**kwargs)
        if action == "get_upcoming_episodes":
            kwargs = {
                "user_id": user_id,
                "start_index": start_index,
                "limit": limit,
                "fields": fields,
                "parent_id": parent_id,
                "enable_images": enable_images,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "enable_user_data": enable_user_data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_upcoming_episodes(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_episodes', 'get_seasons', 'get_next_up', 'get_upcoming_episodes"
        )


def register_universalaudio_tools(mcp: FastMCP):
    @mcp.tool(tags={"UniversalAudio"})
    async def jellyfin_universalaudio(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_universal_audio_stream'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        container: list[Any] | None = Field(default=None, description="container"),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        device_id: str | None = Field(default=None, description="device id"),
        user_id: str | None = Field(default=None, description="user id"),
        audio_codec: str | None = Field(default=None, description="audio codec"),
        max_audio_channels: int | None = Field(
            default=None, description="max audio channels"
        ),
        transcoding_audio_channels: int | None = Field(
            default=None, description="transcoding audio channels"
        ),
        max_streaming_bitrate: int | None = Field(
            default=None, description="max streaming bitrate"
        ),
        audio_bit_rate: int | None = Field(default=None, description="audio bit rate"),
        start_time_ticks: int | None = Field(
            default=None, description="start time ticks"
        ),
        transcoding_container: str | None = Field(
            default=None, description="transcoding container"
        ),
        transcoding_protocol: str | None = Field(
            default=None, description="transcoding protocol"
        ),
        max_audio_sample_rate: int | None = Field(
            default=None, description="max audio sample rate"
        ),
        max_audio_bit_depth: int | None = Field(
            default=None, description="max audio bit depth"
        ),
        enable_remote_media: bool | None = Field(
            default=None, description="enable remote media"
        ),
        enable_audio_vbr_encoding: bool | None = Field(
            default=None, description="enable audio vbr encoding"
        ),
        break_on_non_key_frames: bool | None = Field(
            default=None, description="break on non key frames"
        ),
        enable_redirection: bool | None = Field(
            default=None, description="enable redirection"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage universalaudio operations.

        Actions:
          - 'get_universal_audio_stream': Gets an audio stream.
        """
        kwargs: dict[str, Any]
        if action == "get_universal_audio_stream":
            kwargs = {
                "item_id": item_id,
                "container": container,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "user_id": user_id,
                "audio_codec": audio_codec,
                "max_audio_channels": max_audio_channels,
                "transcoding_audio_channels": transcoding_audio_channels,
                "max_streaming_bitrate": max_streaming_bitrate,
                "audio_bit_rate": audio_bit_rate,
                "start_time_ticks": start_time_ticks,
                "transcoding_container": transcoding_container,
                "transcoding_protocol": transcoding_protocol,
                "max_audio_sample_rate": max_audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "enable_remote_media": enable_remote_media,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
                "break_on_non_key_frames": break_on_non_key_frames,
                "enable_redirection": enable_redirection,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_universal_audio_stream(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_universal_audio_stream"
        )


def register_user_tools(mcp: FastMCP):
    @mcp.tool(tags={"User"})
    async def jellyfin_user(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_users', 'update_user', 'get_user_by_id', 'update_user_policy', 'update_user_configuration', 'forgot_password', 'forgot_password_pin', 'get_current_user', 'create_user_by_name', 'update_user_password', 'get_public_users'"
        ),
        is_hidden: bool | None = Field(default=None, description="is hidden"),
        is_disabled: bool | None = Field(default=None, description="is disabled"),
        user_id: Any | None = Field(default=None, description="user id"),
        body: dict[str, Any] | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage user operations.

        Actions:
          - 'get_users': Gets a list of users.
          - 'update_user': Updates a user.
          - 'get_user_by_id': Gets a user by Id.
          - 'update_user_policy': Updates a user policy.
          - 'update_user_configuration': Updates a user configuration.
          - 'forgot_password': Initiates the forgot password process for a local user.
          - 'forgot_password_pin': Redeems a forgot password pin.
          - 'get_current_user': Gets the user based on auth token.
          - 'create_user_by_name': Creates a user.
          - 'update_user_password': Updates a user's password.
          - 'get_public_users': Gets a list of publicly visible users for display on a login screen.
        """
        kwargs: dict[str, Any]
        if action == "get_users":
            kwargs = {
                "is_hidden": is_hidden,
                "is_disabled": is_disabled,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_users(**kwargs)
        if action == "update_user":
            kwargs = {"user_id": user_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user(**kwargs)
        if action == "get_user_by_id":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_user_by_id(**kwargs)
        if action == "update_user_policy":
            kwargs = {"user_id": user_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user_policy(**kwargs)
        if action == "update_user_configuration":
            kwargs = {"user_id": user_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user_configuration(**kwargs)
        if action == "forgot_password":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.forgot_password(**kwargs)
        if action == "forgot_password_pin":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.forgot_password_pin(**kwargs)
        if action == "get_current_user":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_current_user(**kwargs)
        if action == "create_user_by_name":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_user_by_name(**kwargs)
        if action == "update_user_password":
            kwargs = {"user_id": user_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user_password(**kwargs)
        if action == "get_public_users":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_public_users(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_users', 'update_user', 'get_user_by_id', 'update_user_policy', 'update_user_configuration', 'forgot_password', 'forgot_password_pin', 'get_current_user', 'create_user_by_name', 'update_user_password', 'get_public_users"
        )


def register_userviews_tools(mcp: FastMCP):
    @mcp.tool(tags={"UserViews"})
    async def jellyfin_userviews(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_user_views', 'get_grouping_options'"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        include_external_content: bool | None = Field(
            default=None, description="include external content"
        ),
        preset_views: list[Any] | None = Field(
            default=None, description="preset views"
        ),
        include_hidden: bool | None = Field(default=None, description="include hidden"),
        client=Depends(get_client),
    ) -> dict:
        """Manage userviews operations.

        Actions:
          - 'get_user_views': Get user views.
          - 'get_grouping_options': Get user view grouping options.
        """
        kwargs: dict[str, Any]
        if action == "get_user_views":
            kwargs = {
                "user_id": user_id,
                "include_external_content": include_external_content,
                "preset_views": preset_views,
                "include_hidden": include_hidden,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_user_views(**kwargs)
        if action == "get_grouping_options":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_grouping_options(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_user_views', 'get_grouping_options"
        )


def register_videoattachments_tools(mcp: FastMCP):
    @mcp.tool(tags={"VideoAttachments"})
    async def jellyfin_videoattachments(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_attachment'"
        ),
        video_id: str | None = Field(default=None, description="video id"),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        index: int | None = Field(default=None, description="index"),
        client=Depends(get_client),
    ) -> dict:
        """Manage videoattachments operations.

        Actions:
          - 'get_attachment': Get video attachment.
        """
        kwargs: dict[str, Any]
        if action == "get_attachment":
            kwargs = {
                "video_id": video_id,
                "media_source_id": media_source_id,
                "index": index,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_attachment(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_attachment")


def register_videos_tools(mcp: FastMCP):
    @mcp.tool(tags={"Videos"})
    async def jellyfin_videos(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_additional_part', 'get_video_stream', 'get_video_stream_by_container', 'merge_versions'"
        ),
        item_id: str | None = Field(default=None, description="item id"),
        user_id: str | None = Field(default=None, description="user id"),
        container: Any | None = Field(default=None, description="container"),
        static: bool | None = Field(default=None, description="static"),
        stream_params: str | None = Field(default=None, description="stream params"),
        tag: str | None = Field(default=None, description="tag"),
        device_profile_id: str | None = Field(
            default=None, description="device profile id"
        ),
        play_session_id: str | None = Field(
            default=None, description="play session id"
        ),
        segment_container: str | None = Field(
            default=None, description="segment container"
        ),
        segment_length: int | None = Field(default=None, description="segment length"),
        min_segments: int | None = Field(default=None, description="min segments"),
        media_source_id: str | None = Field(
            default=None, description="media source id"
        ),
        device_id: str | None = Field(default=None, description="device id"),
        audio_codec: str | None = Field(default=None, description="audio codec"),
        enable_auto_stream_copy: bool | None = Field(
            default=None, description="enable auto stream copy"
        ),
        allow_video_stream_copy: bool | None = Field(
            default=None, description="allow video stream copy"
        ),
        allow_audio_stream_copy: bool | None = Field(
            default=None, description="allow audio stream copy"
        ),
        break_on_non_key_frames: bool | None = Field(
            default=None, description="break on non key frames"
        ),
        audio_sample_rate: int | None = Field(
            default=None, description="audio sample rate"
        ),
        max_audio_bit_depth: int | None = Field(
            default=None, description="max audio bit depth"
        ),
        audio_bit_rate: int | None = Field(default=None, description="audio bit rate"),
        audio_channels: int | None = Field(default=None, description="audio channels"),
        max_audio_channels: int | None = Field(
            default=None, description="max audio channels"
        ),
        profile: str | None = Field(default=None, description="profile"),
        level: str | None = Field(default=None, description="level"),
        framerate: float | None = Field(default=None, description="framerate"),
        max_framerate: float | None = Field(default=None, description="max framerate"),
        copy_timestamps: bool | None = Field(
            default=None, description="copy timestamps"
        ),
        start_time_ticks: int | None = Field(
            default=None, description="start time ticks"
        ),
        width: int | None = Field(default=None, description="width"),
        height: int | None = Field(default=None, description="height"),
        max_width: int | None = Field(default=None, description="max width"),
        max_height: int | None = Field(default=None, description="max height"),
        video_bit_rate: int | None = Field(default=None, description="video bit rate"),
        subtitle_stream_index: int | None = Field(
            default=None, description="subtitle stream index"
        ),
        subtitle_method: str | None = Field(
            default=None, description="subtitle method"
        ),
        max_ref_frames: int | None = Field(default=None, description="max ref frames"),
        max_video_bit_depth: int | None = Field(
            default=None, description="max video bit depth"
        ),
        require_avc: bool | None = Field(default=None, description="require avc"),
        de_interlace: bool | None = Field(default=None, description="de interlace"),
        require_non_anamorphic: bool | None = Field(
            default=None, description="require non anamorphic"
        ),
        transcoding_max_audio_channels: int | None = Field(
            default=None, description="transcoding max audio channels"
        ),
        cpu_core_limit: int | None = Field(default=None, description="cpu core limit"),
        live_stream_id: str | None = Field(default=None, description="live stream id"),
        enable_mpegts_m2_ts_mode: bool | None = Field(
            default=None, description="enable mpegts m2 ts mode"
        ),
        video_codec: str | None = Field(default=None, description="video codec"),
        subtitle_codec: str | None = Field(default=None, description="subtitle codec"),
        transcode_reasons: str | None = Field(
            default=None, description="transcode reasons"
        ),
        audio_stream_index: int | None = Field(
            default=None, description="audio stream index"
        ),
        video_stream_index: int | None = Field(
            default=None, description="video stream index"
        ),
        context: str | None = Field(default=None, description="context"),
        stream_options: dict[str, Any] | None = Field(
            default=None, description="stream options"
        ),
        enable_audio_vbr_encoding: bool | None = Field(
            default=None, description="enable audio vbr encoding"
        ),
        ids: list[Any] | None = Field(default=None, description="ids"),
        client=Depends(get_client),
    ) -> dict:
        """Manage videos operations.

        Actions:
          - 'get_additional_part': Gets additional parts for a video.
          - 'get_video_stream': Gets a video stream.
          - 'get_video_stream_by_container': Gets a video stream.
          - 'merge_versions': Merges videos into a single record.
        """
        kwargs: dict[str, Any]
        if action == "get_additional_part":
            kwargs = {"item_id": item_id, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_additional_part(**kwargs)
        if action == "get_video_stream":
            kwargs = {
                "item_id": item_id,
                "container": container,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "max_width": max_width,
                "max_height": max_height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_video_stream(**kwargs)
        if action == "get_video_stream_by_container":
            kwargs = {
                "item_id": item_id,
                "container": container,
                "static": static,
                "stream_params": stream_params,
                "tag": tag,
                "device_profile_id": device_profile_id,
                "play_session_id": play_session_id,
                "segment_container": segment_container,
                "segment_length": segment_length,
                "min_segments": min_segments,
                "media_source_id": media_source_id,
                "device_id": device_id,
                "audio_codec": audio_codec,
                "enable_auto_stream_copy": enable_auto_stream_copy,
                "allow_video_stream_copy": allow_video_stream_copy,
                "allow_audio_stream_copy": allow_audio_stream_copy,
                "break_on_non_key_frames": break_on_non_key_frames,
                "audio_sample_rate": audio_sample_rate,
                "max_audio_bit_depth": max_audio_bit_depth,
                "audio_bit_rate": audio_bit_rate,
                "audio_channels": audio_channels,
                "max_audio_channels": max_audio_channels,
                "profile": profile,
                "level": level,
                "framerate": framerate,
                "max_framerate": max_framerate,
                "copy_timestamps": copy_timestamps,
                "start_time_ticks": start_time_ticks,
                "width": width,
                "height": height,
                "max_width": max_width,
                "max_height": max_height,
                "video_bit_rate": video_bit_rate,
                "subtitle_stream_index": subtitle_stream_index,
                "subtitle_method": subtitle_method,
                "max_ref_frames": max_ref_frames,
                "max_video_bit_depth": max_video_bit_depth,
                "require_avc": require_avc,
                "de_interlace": de_interlace,
                "require_non_anamorphic": require_non_anamorphic,
                "transcoding_max_audio_channels": transcoding_max_audio_channels,
                "cpu_core_limit": cpu_core_limit,
                "live_stream_id": live_stream_id,
                "enable_mpegts_m2_ts_mode": enable_mpegts_m2_ts_mode,
                "video_codec": video_codec,
                "subtitle_codec": subtitle_codec,
                "transcode_reasons": transcode_reasons,
                "audio_stream_index": audio_stream_index,
                "video_stream_index": video_stream_index,
                "context": context,
                "stream_options": stream_options,
                "enable_audio_vbr_encoding": enable_audio_vbr_encoding,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_video_stream_by_container(**kwargs)
        if action == "merge_versions":
            kwargs = {"ids": ids}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.merge_versions(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_additional_part', 'get_video_stream', 'get_video_stream_by_container', 'merge_versions"
        )


def register_years_tools(mcp: FastMCP):
    @mcp.tool(tags={"Years"})
    async def jellyfin_years(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_years', 'get_year'"
        ),
        start_index: int | None = Field(default=None, description="start index"),
        limit: int | None = Field(default=None, description="limit"),
        sort_order: list[Any] | None = Field(default=None, description="sort order"),
        parent_id: str | None = Field(default=None, description="parent id"),
        fields: list[Any] | None = Field(default=None, description="fields"),
        exclude_item_types: list[Any] | None = Field(
            default=None, description="exclude item types"
        ),
        include_item_types: list[Any] | None = Field(
            default=None, description="include item types"
        ),
        media_types: list[Any] | None = Field(default=None, description="media types"),
        sort_by: list[Any] | None = Field(default=None, description="sort by"),
        enable_user_data: bool | None = Field(
            default=None, description="enable user data"
        ),
        image_type_limit: int | None = Field(
            default=None, description="image type limit"
        ),
        enable_image_types: list[Any] | None = Field(
            default=None, description="enable image types"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        recursive: bool | None = Field(default=None, description="recursive"),
        enable_images: bool | None = Field(default=None, description="enable images"),
        year: int | None = Field(default=None, description="year"),
        client=Depends(get_client),
    ) -> dict:
        """Manage years operations.

        Actions:
          - 'get_years': Get years.
          - 'get_year': Gets a year.
        """
        kwargs: dict[str, Any]
        if action == "get_years":
            kwargs = {
                "start_index": start_index,
                "limit": limit,
                "sort_order": sort_order,
                "parent_id": parent_id,
                "fields": fields,
                "exclude_item_types": exclude_item_types,
                "include_item_types": include_item_types,
                "media_types": media_types,
                "sort_by": sort_by,
                "enable_user_data": enable_user_data,
                "image_type_limit": image_type_limit,
                "enable_image_types": enable_image_types,
                "user_id": user_id,
                "recursive": recursive,
                "enable_images": enable_images,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_years(**kwargs)
        if action == "get_year":
            kwargs = {"year": year, "user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_year(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_years', 'get_year"
        )


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="jellyfin-mcp MCP",
        version=__version__,
        instructions="jellyfin-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_ACTIVITYLOGTOOL = to_boolean(os.getenv("ACTIVITYLOGTOOL", "True"))
    if DEFAULT_ACTIVITYLOGTOOL:
        register_activitylog_tools(mcp)
    DEFAULT_APIKEYTOOL = to_boolean(os.getenv("APIKEYTOOL", "True"))
    if DEFAULT_APIKEYTOOL:
        register_apikey_tools(mcp)
    DEFAULT_ARTISTSTOOL = to_boolean(os.getenv("ARTISTSTOOL", "True"))
    if DEFAULT_ARTISTSTOOL:
        register_artists_tools(mcp)
    DEFAULT_AUDIOTOOL = to_boolean(os.getenv("AUDIOTOOL", "True"))
    if DEFAULT_AUDIOTOOL:
        register_audio_tools(mcp)
    DEFAULT_BACKUPTOOL = to_boolean(os.getenv("BACKUPTOOL", "True"))
    if DEFAULT_BACKUPTOOL:
        register_backup_tools(mcp)
    DEFAULT_BRANDINGTOOL = to_boolean(os.getenv("BRANDINGTOOL", "True"))
    if DEFAULT_BRANDINGTOOL:
        register_branding_tools(mcp)
    DEFAULT_CHANNELSTOOL = to_boolean(os.getenv("CHANNELSTOOL", "True"))
    if DEFAULT_CHANNELSTOOL:
        register_channels_tools(mcp)
    DEFAULT_CLIENTLOGTOOL = to_boolean(os.getenv("CLIENTLOGTOOL", "True"))
    if DEFAULT_CLIENTLOGTOOL:
        register_clientlog_tools(mcp)
    DEFAULT_COLLECTIONTOOL = to_boolean(os.getenv("COLLECTIONTOOL", "True"))
    if DEFAULT_COLLECTIONTOOL:
        register_collection_tools(mcp)
    DEFAULT_CONFIGURATIONTOOL = to_boolean(os.getenv("CONFIGURATIONTOOL", "True"))
    if DEFAULT_CONFIGURATIONTOOL:
        register_configuration_tools(mcp)
    DEFAULT_DASHBOARDTOOL = to_boolean(os.getenv("DASHBOARDTOOL", "True"))
    if DEFAULT_DASHBOARDTOOL:
        register_dashboard_tools(mcp)
    DEFAULT_DEVICESTOOL = to_boolean(os.getenv("DEVICESTOOL", "True"))
    if DEFAULT_DEVICESTOOL:
        register_devices_tools(mcp)
    DEFAULT_DISPLAYPREFERENCESTOOL = to_boolean(
        os.getenv("DISPLAYPREFERENCESTOOL", "True")
    )
    if DEFAULT_DISPLAYPREFERENCESTOOL:
        register_displaypreferences_tools(mcp)
    DEFAULT_DYNAMICHLSTOOL = to_boolean(os.getenv("DYNAMICHLSTOOL", "True"))
    if DEFAULT_DYNAMICHLSTOOL:
        register_dynamichls_tools(mcp)
    DEFAULT_ENVIRONMENTTOOL = to_boolean(os.getenv("ENVIRONMENTTOOL", "True"))
    if DEFAULT_ENVIRONMENTTOOL:
        register_environment_tools(mcp)
    DEFAULT_FILTERTOOL = to_boolean(os.getenv("FILTERTOOL", "True"))
    if DEFAULT_FILTERTOOL:
        register_filter_tools(mcp)
    DEFAULT_GENRESTOOL = to_boolean(os.getenv("GENRESTOOL", "True"))
    if DEFAULT_GENRESTOOL:
        register_genres_tools(mcp)
    DEFAULT_HLSSEGMENTTOOL = to_boolean(os.getenv("HLSSEGMENTTOOL", "True"))
    if DEFAULT_HLSSEGMENTTOOL:
        register_hlssegment_tools(mcp)
    DEFAULT_IMAGETOOL = to_boolean(os.getenv("IMAGETOOL", "True"))
    if DEFAULT_IMAGETOOL:
        register_image_tools(mcp)
    DEFAULT_INSTANTMIXTOOL = to_boolean(os.getenv("INSTANTMIXTOOL", "True"))
    if DEFAULT_INSTANTMIXTOOL:
        register_instantmix_tools(mcp)
    DEFAULT_ITEMLOOKUPTOOL = to_boolean(os.getenv("ITEMLOOKUPTOOL", "True"))
    if DEFAULT_ITEMLOOKUPTOOL:
        register_itemlookup_tools(mcp)
    DEFAULT_ITEMREFRESHTOOL = to_boolean(os.getenv("ITEMREFRESHTOOL", "True"))
    if DEFAULT_ITEMREFRESHTOOL:
        register_itemrefresh_tools(mcp)
    DEFAULT_ITEMSTOOL = to_boolean(os.getenv("ITEMSTOOL", "True"))
    if DEFAULT_ITEMSTOOL:
        register_items_tools(mcp)
    DEFAULT_LIBRARYTOOL = to_boolean(os.getenv("LIBRARYTOOL", "True"))
    if DEFAULT_LIBRARYTOOL:
        register_library_tools(mcp)
    DEFAULT_ITEMUPDATETOOL = to_boolean(os.getenv("ITEMUPDATETOOL", "True"))
    if DEFAULT_ITEMUPDATETOOL:
        register_itemupdate_tools(mcp)
    DEFAULT_USERLIBRARYTOOL = to_boolean(os.getenv("USERLIBRARYTOOL", "True"))
    if DEFAULT_USERLIBRARYTOOL:
        register_userlibrary_tools(mcp)
    DEFAULT_LIBRARYSTRUCTURETOOL = to_boolean(os.getenv("LIBRARYSTRUCTURETOOL", "True"))
    if DEFAULT_LIBRARYSTRUCTURETOOL:
        register_librarystructure_tools(mcp)
    DEFAULT_LIVETVTOOL = to_boolean(os.getenv("LIVETVTOOL", "True"))
    if DEFAULT_LIVETVTOOL:
        register_livetv_tools(mcp)
    DEFAULT_LOCALIZATIONTOOL = to_boolean(os.getenv("LOCALIZATIONTOOL", "True"))
    if DEFAULT_LOCALIZATIONTOOL:
        register_localization_tools(mcp)
    DEFAULT_LYRICSTOOL = to_boolean(os.getenv("LYRICSTOOL", "True"))
    if DEFAULT_LYRICSTOOL:
        register_lyrics_tools(mcp)
    DEFAULT_MEDIAINFOTOOL = to_boolean(os.getenv("MEDIAINFOTOOL", "True"))
    if DEFAULT_MEDIAINFOTOOL:
        register_mediainfo_tools(mcp)
    DEFAULT_MEDIASEGMENTSTOOL = to_boolean(os.getenv("MEDIASEGMENTSTOOL", "True"))
    if DEFAULT_MEDIASEGMENTSTOOL:
        register_mediasegments_tools(mcp)
    DEFAULT_MOVIESTOOL = to_boolean(os.getenv("MOVIESTOOL", "True"))
    if DEFAULT_MOVIESTOOL:
        register_movies_tools(mcp)
    DEFAULT_MUSICGENRESTOOL = to_boolean(os.getenv("MUSICGENRESTOOL", "True"))
    if DEFAULT_MUSICGENRESTOOL:
        register_musicgenres_tools(mcp)
    DEFAULT_PACKAGETOOL = to_boolean(os.getenv("PACKAGETOOL", "True"))
    if DEFAULT_PACKAGETOOL:
        register_package_tools(mcp)
    DEFAULT_PERSONSTOOL = to_boolean(os.getenv("PERSONSTOOL", "True"))
    if DEFAULT_PERSONSTOOL:
        register_persons_tools(mcp)
    DEFAULT_PLAYLISTSTOOL = to_boolean(os.getenv("PLAYLISTSTOOL", "True"))
    if DEFAULT_PLAYLISTSTOOL:
        register_playlists_tools(mcp)
    DEFAULT_PLAYSTATETOOL = to_boolean(os.getenv("PLAYSTATETOOL", "True"))
    if DEFAULT_PLAYSTATETOOL:
        register_playstate_tools(mcp)
    DEFAULT_PLUGINSTOOL = to_boolean(os.getenv("PLUGINSTOOL", "True"))
    if DEFAULT_PLUGINSTOOL:
        register_plugins_tools(mcp)
    DEFAULT_QUICKCONNECTTOOL = to_boolean(os.getenv("QUICKCONNECTTOOL", "True"))
    if DEFAULT_QUICKCONNECTTOOL:
        register_quickconnect_tools(mcp)
    DEFAULT_REMOTEIMAGETOOL = to_boolean(os.getenv("REMOTEIMAGETOOL", "True"))
    if DEFAULT_REMOTEIMAGETOOL:
        register_remoteimage_tools(mcp)
    DEFAULT_SCHEDULEDTASKSTOOL = to_boolean(os.getenv("SCHEDULEDTASKSTOOL", "True"))
    if DEFAULT_SCHEDULEDTASKSTOOL:
        register_scheduledtasks_tools(mcp)
    DEFAULT_SEARCHTOOL = to_boolean(os.getenv("SEARCHTOOL", "True"))
    if DEFAULT_SEARCHTOOL:
        register_search_tools(mcp)
    DEFAULT_SESSIONTOOL = to_boolean(os.getenv("SESSIONTOOL", "True"))
    if DEFAULT_SESSIONTOOL:
        register_session_tools(mcp)
    DEFAULT_STARTUPTOOL = to_boolean(os.getenv("STARTUPTOOL", "True"))
    if DEFAULT_STARTUPTOOL:
        register_startup_tools(mcp)
    DEFAULT_STUDIOSTOOL = to_boolean(os.getenv("STUDIOSTOOL", "True"))
    if DEFAULT_STUDIOSTOOL:
        register_studios_tools(mcp)
    DEFAULT_SUBTITLETOOL = to_boolean(os.getenv("SUBTITLETOOL", "True"))
    if DEFAULT_SUBTITLETOOL:
        register_subtitle_tools(mcp)
    DEFAULT_SUGGESTIONSTOOL = to_boolean(os.getenv("SUGGESTIONSTOOL", "True"))
    if DEFAULT_SUGGESTIONSTOOL:
        register_suggestions_tools(mcp)
    DEFAULT_SYSTEMTOOL = to_boolean(os.getenv("SYSTEMTOOL", "True"))
    if DEFAULT_SYSTEMTOOL:
        register_system_tools(mcp)
    DEFAULT_TIMESYNCTOOL = to_boolean(os.getenv("TIMESYNCTOOL", "True"))
    if DEFAULT_TIMESYNCTOOL:
        register_timesync_tools(mcp)
    DEFAULT_TMDBTOOL = to_boolean(os.getenv("TMDBTOOL", "True"))
    if DEFAULT_TMDBTOOL:
        register_tmdb_tools(mcp)
    DEFAULT_TRAILERSTOOL = to_boolean(os.getenv("TRAILERSTOOL", "True"))
    if DEFAULT_TRAILERSTOOL:
        register_trailers_tools(mcp)
    DEFAULT_TRICKPLAYTOOL = to_boolean(os.getenv("TRICKPLAYTOOL", "True"))
    if DEFAULT_TRICKPLAYTOOL:
        register_trickplay_tools(mcp)
    DEFAULT_TVSHOWSTOOL = to_boolean(os.getenv("TVSHOWSTOOL", "True"))
    if DEFAULT_TVSHOWSTOOL:
        register_tvshows_tools(mcp)
    DEFAULT_UNIVERSALAUDIOTOOL = to_boolean(os.getenv("UNIVERSALAUDIOTOOL", "True"))
    if DEFAULT_UNIVERSALAUDIOTOOL:
        register_universalaudio_tools(mcp)
    DEFAULT_USERTOOL = to_boolean(os.getenv("USERTOOL", "True"))
    if DEFAULT_USERTOOL:
        register_user_tools(mcp)
    DEFAULT_USERVIEWSTOOL = to_boolean(os.getenv("USERVIEWSTOOL", "True"))
    if DEFAULT_USERVIEWSTOOL:
        register_userviews_tools(mcp)
    DEFAULT_VIDEOATTACHMENTSTOOL = to_boolean(os.getenv("VIDEOATTACHMENTSTOOL", "True"))
    if DEFAULT_VIDEOATTACHMENTSTOOL:
        register_videoattachments_tools(mcp)
    DEFAULT_VIDEOSTOOL = to_boolean(os.getenv("VIDEOSTOOL", "True"))
    if DEFAULT_VIDEOSTOOL:
        register_videos_tools(mcp)
    DEFAULT_YEARSTOOL = to_boolean(os.getenv("YEARSTOOL", "True"))
    if DEFAULT_YEARSTOOL:
        register_years_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
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
