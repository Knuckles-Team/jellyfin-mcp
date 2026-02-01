#!/usr/bin/python
# coding: utf-8

import os
import argparse
import sys
import logging
from typing import Optional, List, Dict, Union, Any

import requests
from pydantic import Field
from eunomia_mcp.middleware import EunomiaMcpMiddleware
from fastmcp import FastMCP
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.server.auth import OAuthProxy, RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier, StaticTokenVerifier
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.utilities.logging import get_logger
from jellyfin_mcp.jellyfin_api import Api
from jellyfin_mcp.utils import to_boolean, to_integer
from jellyfin_mcp.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.1.1"
print(f"Jellyfin MCP v{__version__}")

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)

config = {
    "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
    "audience": os.environ.get("AUDIENCE", None),
    "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
    "token_endpoint": None,  # Will be fetched dynamically from OIDC config
    "oidc_client_id": os.environ.get("OIDC_CLIENT_ID", None),
    "oidc_client_secret": os.environ.get("OIDC_CLIENT_SECRET", None),
    "oidc_config_url": os.environ.get("OIDC_CONFIG_URL", None),
    "jwt_jwks_uri": os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI", None),
    "jwt_issuer": os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER", None),
    "jwt_audience": os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE", None),
    "jwt_algorithm": os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM", None),
    "jwt_secret": os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY", None),
    "jwt_required_scopes": os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES", None),
}

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "8000"))


def get_api_client():
    base_url = os.environ.get("JELLYFIN_BASE_URL")
    token = os.environ.get("JELLYFIN_TOKEN")
    username = os.environ.get("JELLYFIN_USERNAME")
    password = os.environ.get("JELLYFIN_PASSWORD")
    verify = to_boolean(os.environ.get("JELLYFIN_VERIFY", "False"))
    if not base_url:
        raise ValueError("JELLYFIN_BASE_URL environment variable is required")
    return Api(
        base_url, token=token, username=username, password=password, verify=verify
    )


def register_tools(mcp: FastMCP):
    @mcp.tool(
        name="get_log_entries",
        description="Gets activity log entries.",
        tags={"ActivityLog"},
    )
    def get_log_entries_tool(
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        min_date: Optional[str] = Field(
            default=None, description="Optional. The minimum date. Format = ISO."
        ),
        has_user_id: Optional[bool] = Field(
            default=None,
            description="Optional. Filter log entries if it has user id, or not.",
        ),
    ) -> Any:
        """Gets activity log entries."""
        api = get_api_client()
        return api.get_log_entries(
            start_index=start_index,
            limit=limit,
            min_date=min_date,
            has_user_id=has_user_id,
        )

    @mcp.tool(name="get_keys", description="Get all keys.", tags={"ApiKey"})
    def get_keys_tool() -> Any:
        """Get all keys."""
        api = get_api_client()
        return api.get_keys()

    @mcp.tool(name="create_key", description="Create a new api key.", tags={"ApiKey"})
    def create_key_tool(
        app: Optional[str] = Field(
            default=None, description="Name of the app using the authentication key."
        )
    ) -> Any:
        """Create a new api key."""
        api = get_api_client()
        return api.create_key(app=app)

    @mcp.tool(name="revoke_key", description="Remove an api key.", tags={"ApiKey"})
    def revoke_key_tool(
        key: str = Field(description="The access token to delete."),
    ) -> Any:
        """Remove an api key."""
        api = get_api_client()
        return api.revoke_key(key=key)

    @mcp.tool(
        name="get_artists",
        description="Gets all artists from a given item, folder, or the entire library.",
        tags={"Artists"},
    )
    def get_artists_tool(
        min_community_rating: Optional[float] = Field(
            default=None, description="Optional filter by minimum community rating."
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="Optional. Search term."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered out based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        filters: Optional[List[Any]] = Field(
            default=None, description="Optional. Specify additional filters to apply."
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by MediaType. Allows multiple, comma delimited.",
        ),
        genres: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre. This allows multiple, pipe delimited.",
        ),
        genre_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre id. This allows multiple, pipe delimited.",
        ),
        official_ratings: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on OfficialRating. This allows multiple, pipe delimited.",
        ),
        tags: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on tag. This allows multiple, pipe delimited.",
        ),
        years: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on production year. This allows multiple, comma delimited.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional, include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        person: Optional[str] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person.",
        ),
        person_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person ids.",
        ),
        person_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, along with Person, results will be filtered to include only those containing the specified person and PersonType. Allows multiple, comma-delimited.",
        ),
        studios: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio. This allows multiple, pipe delimited.",
        ),
        studio_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio id. This allows multiple, pipe delimited.",
        ),
        user_id: Optional[str] = Field(default=None, description="User id."),
        name_starts_with_or_greater: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally or greater than a given input string.",
        ),
        name_starts_with: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally than a given input string.",
        ),
        name_less_than: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is equally or lesser than a given input string.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending,Descending."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Total record count."
        ),
    ) -> Any:
        """Gets all artists from a given item, folder, or the entire library."""
        api = get_api_client()
        return api.get_artists(
            min_community_rating=min_community_rating,
            start_index=start_index,
            limit=limit,
            search_term=search_term,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            filters=filters,
            is_favorite=is_favorite,
            media_types=media_types,
            genres=genres,
            genre_ids=genre_ids,
            official_ratings=official_ratings,
            tags=tags,
            years=years,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            person=person,
            person_ids=person_ids,
            person_types=person_types,
            studios=studios,
            studio_ids=studio_ids,
            user_id=user_id,
            name_starts_with_or_greater=name_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
            sort_by=sort_by,
            sort_order=sort_order,
            enable_images=enable_images,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="get_artist_by_name",
        description="Gets an artist by name.",
        tags={"Artists"},
    )
    def get_artist_by_name_tool(
        name: str = Field(description="Studio name."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
    ) -> Any:
        """Gets an artist by name."""
        api = get_api_client()
        return api.get_artist_by_name(name=name, user_id=user_id)

    @mcp.tool(
        name="get_album_artists",
        description="Gets all album artists from a given item, folder, or the entire library.",
        tags={"Artists"},
    )
    def get_album_artists_tool(
        min_community_rating: Optional[float] = Field(
            default=None, description="Optional filter by minimum community rating."
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="Optional. Search term."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered out based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        filters: Optional[List[Any]] = Field(
            default=None, description="Optional. Specify additional filters to apply."
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by MediaType. Allows multiple, comma delimited.",
        ),
        genres: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre. This allows multiple, pipe delimited.",
        ),
        genre_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre id. This allows multiple, pipe delimited.",
        ),
        official_ratings: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on OfficialRating. This allows multiple, pipe delimited.",
        ),
        tags: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on tag. This allows multiple, pipe delimited.",
        ),
        years: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on production year. This allows multiple, comma delimited.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional, include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        person: Optional[str] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person.",
        ),
        person_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person ids.",
        ),
        person_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, along with Person, results will be filtered to include only those containing the specified person and PersonType. Allows multiple, comma-delimited.",
        ),
        studios: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio. This allows multiple, pipe delimited.",
        ),
        studio_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio id. This allows multiple, pipe delimited.",
        ),
        user_id: Optional[str] = Field(default=None, description="User id."),
        name_starts_with_or_greater: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally or greater than a given input string.",
        ),
        name_starts_with: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally than a given input string.",
        ),
        name_less_than: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is equally or lesser than a given input string.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending,Descending."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Total record count."
        ),
    ) -> Any:
        """Gets all album artists from a given item, folder, or the entire library."""
        api = get_api_client()
        return api.get_album_artists(
            min_community_rating=min_community_rating,
            start_index=start_index,
            limit=limit,
            search_term=search_term,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            filters=filters,
            is_favorite=is_favorite,
            media_types=media_types,
            genres=genres,
            genre_ids=genre_ids,
            official_ratings=official_ratings,
            tags=tags,
            years=years,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            person=person,
            person_ids=person_ids,
            person_types=person_types,
            studios=studios,
            studio_ids=studio_ids,
            user_id=user_id,
            name_starts_with_or_greater=name_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
            sort_by=sort_by,
            sort_order=sort_order,
            enable_images=enable_images,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="get_audio_stream", description="Gets an audio stream.", tags={"Audio"}
    )
    def get_audio_stream_tool(
        item_id: str = Field(description="The item id."),
        container: Optional[str] = Field(
            default=None, description="The audio container."
        ),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3. If omitted the server will auto-select using the url's extension.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264. If omitted the server will auto-select using the url's extension.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
    ) -> Any:
        """Gets an audio stream."""
        api = get_api_client()
        return api.get_audio_stream(
            item_id=item_id,
            container=container,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
        )

    @mcp.tool(
        name="get_audio_stream_by_container",
        description="Gets an audio stream.",
        tags={"Audio"},
    )
    def get_audio_stream_by_container_tool(
        item_id: str = Field(description="The item id."),
        container: str = Field(description="The audio container."),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3. If omitted the server will auto-select using the url's extension.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264. If omitted the server will auto-select using the url's extension.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
    ) -> Any:
        """Gets an audio stream."""
        api = get_api_client()
        return api.get_audio_stream_by_container(
            item_id=item_id,
            container=container,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
        )

    @mcp.tool(
        name="list_backups",
        description="Gets a list of all currently present backups in the backup directory.",
        tags={"Backup"},
    )
    def list_backups_tool() -> Any:
        """Gets a list of all currently present backups in the backup directory."""
        api = get_api_client()
        return api.list_backups()

    @mcp.tool(
        name="create_backup", description="Creates a new Backup.", tags={"Backup"}
    )
    def create_backup_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Creates a new Backup."""
        api = get_api_client()
        return api.create_backup(body=body)

    @mcp.tool(
        name="get_backup",
        description="Gets the descriptor from an existing archive is present.",
        tags={"Backup"},
    )
    def get_backup_tool(
        path: Optional[str] = Field(
            default=None, description="The data to start a restore process."
        )
    ) -> Any:
        """Gets the descriptor from an existing archive is present."""
        api = get_api_client()
        return api.get_backup(path=path)

    @mcp.tool(
        name="start_restore_backup",
        description="Restores to a backup by restarting the server and applying the backup.",
        tags={"Backup"},
    )
    def start_restore_backup_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Restores to a backup by restarting the server and applying the backup."""
        api = get_api_client()
        return api.start_restore_backup(body=body)

    @mcp.tool(
        name="get_branding_options",
        description="Gets branding configuration.",
        tags={"Branding"},
    )
    def get_branding_options_tool() -> Any:
        """Gets branding configuration."""
        api = get_api_client()
        return api.get_branding_options()

    @mcp.tool(
        name="get_branding_css", description="Gets branding css.", tags={"Branding"}
    )
    def get_branding_css_tool() -> Any:
        """Gets branding css."""
        api = get_api_client()
        return api.get_branding_css()

    @mcp.tool(
        name="get_branding_css_2", description="Gets branding css.", tags={"Branding"}
    )
    def get_branding_css_2_tool() -> Any:
        """Gets branding css."""
        api = get_api_client()
        return api.get_branding_css_2()

    @mcp.tool(
        name="get_channels", description="Gets available channels.", tags={"Channels"}
    )
    def get_channels_tool(
        user_id: Optional[str] = Field(
            default=None,
            description="User Id to filter by. Use System.Guid.Empty to not filter by user.",
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        supports_latest_items: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by channels that support getting latest items.",
        ),
        supports_media_deletion: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by channels that support media deletion.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None, description="Optional. Filter by channels that are favorite."
        ),
    ) -> Any:
        """Gets available channels."""
        api = get_api_client()
        return api.get_channels(
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            supports_latest_items=supports_latest_items,
            supports_media_deletion=supports_media_deletion,
            is_favorite=is_favorite,
        )

    @mcp.tool(
        name="get_channel_features",
        description="Get channel features.",
        tags={"Channels"},
    )
    def get_channel_features_tool(
        channel_id: str = Field(description="Channel id."),
    ) -> Any:
        """Get channel features."""
        api = get_api_client()
        return api.get_channel_features(channel_id=channel_id)

    @mcp.tool(
        name="get_channel_items", description="Get channel items.", tags={"Channels"}
    )
    def get_channel_items_tool(
        channel_id: str = Field(description="Channel Id."),
        folder_id: Optional[str] = Field(
            default=None, description="Optional. Folder Id."
        ),
        user_id: Optional[str] = Field(default=None, description="Optional. User Id."),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Optional. Sort Order - Ascending,Descending."
        ),
        filters: Optional[List[Any]] = Field(
            default=None, description="Optional. Specify additional filters to apply."
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
    ) -> Any:
        """Get channel items."""
        api = get_api_client()
        return api.get_channel_items(
            channel_id=channel_id,
            folder_id=folder_id,
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            sort_order=sort_order,
            filters=filters,
            sort_by=sort_by,
            fields=fields,
        )

    @mcp.tool(
        name="get_all_channel_features",
        description="Get all channel features.",
        tags={"Channels"},
    )
    def get_all_channel_features_tool() -> Any:
        """Get all channel features."""
        api = get_api_client()
        return api.get_all_channel_features()

    @mcp.tool(
        name="get_latest_channel_items",
        description="Gets latest channel items.",
        tags={"Channels"},
    )
    def get_latest_channel_items_tool(
        user_id: Optional[str] = Field(default=None, description="Optional. User Id."),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        filters: Optional[List[Any]] = Field(
            default=None, description="Optional. Specify additional filters to apply."
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        channel_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more channel id's, comma delimited.",
        ),
    ) -> Any:
        """Gets latest channel items."""
        api = get_api_client()
        return api.get_latest_channel_items(
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            filters=filters,
            fields=fields,
            channel_ids=channel_ids,
        )

    @mcp.tool(name="log_file", description="Upload a document.", tags={"ClientLog"})
    def log_file_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Upload a document."""
        api = get_api_client()
        return api.log_file(body=body)

    @mcp.tool(
        name="create_collection",
        description="Creates a new collection.",
        tags={"Collection"},
    )
    def create_collection_tool(
        name: Optional[str] = Field(
            default=None, description="The name of the collection."
        ),
        ids: Optional[List[Any]] = Field(
            default=None, description="Item Ids to add to the collection."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Optional. Create the collection within a specific folder.",
        ),
        is_locked: Optional[bool] = Field(
            default=None, description="Whether or not to lock the new collection."
        ),
    ) -> Any:
        """Creates a new collection."""
        api = get_api_client()
        return api.create_collection(
            name=name, ids=ids, parent_id=parent_id, is_locked=is_locked
        )

    @mcp.tool(
        name="add_to_collection",
        description="Adds items to a collection.",
        tags={"Collection"},
    )
    def add_to_collection_tool(
        collection_id: str = Field(description="The collection id."),
        ids: Optional[List[Any]] = Field(
            default=None, description="Item ids, comma delimited."
        ),
    ) -> Any:
        """Adds items to a collection."""
        api = get_api_client()
        return api.add_to_collection(collection_id=collection_id, ids=ids)

    @mcp.tool(
        name="remove_from_collection",
        description="Removes items from a collection.",
        tags={"Collection"},
    )
    def remove_from_collection_tool(
        collection_id: str = Field(description="The collection id."),
        ids: Optional[List[Any]] = Field(
            default=None, description="Item ids, comma delimited."
        ),
    ) -> Any:
        """Removes items from a collection."""
        api = get_api_client()
        return api.remove_from_collection(collection_id=collection_id, ids=ids)

    @mcp.tool(
        name="get_configuration",
        description="Gets application configuration.",
        tags={"Configuration"},
    )
    def get_configuration_tool() -> Any:
        """Gets application configuration."""
        api = get_api_client()
        return api.get_configuration()

    @mcp.tool(
        name="update_configuration",
        description="Updates application configuration.",
        tags={"Configuration"},
    )
    def update_configuration_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Updates application configuration."""
        api = get_api_client()
        return api.update_configuration(body=body)

    @mcp.tool(
        name="get_named_configuration",
        description="Gets a named configuration.",
        tags={"Configuration"},
    )
    def get_named_configuration_tool(
        key: str = Field(description="Configuration key."),
    ) -> Any:
        """Gets a named configuration."""
        api = get_api_client()
        return api.get_named_configuration(key=key)

    @mcp.tool(
        name="update_named_configuration",
        description="Updates named configuration.",
        tags={"Configuration"},
    )
    def update_named_configuration_tool(
        key: str = Field(description="Configuration key."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates named configuration."""
        api = get_api_client()
        return api.update_named_configuration(key=key, body=body)

    @mcp.tool(
        name="update_branding_configuration",
        description="Updates branding configuration.",
        tags={"Configuration"},
    )
    def update_branding_configuration_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Updates branding configuration."""
        api = get_api_client()
        return api.update_branding_configuration(body=body)

    @mcp.tool(
        name="get_default_metadata_options",
        description="Gets a default MetadataOptions object.",
        tags={"Configuration"},
    )
    def get_default_metadata_options_tool() -> Any:
        """Gets a default MetadataOptions object."""
        api = get_api_client()
        return api.get_default_metadata_options()

    @mcp.tool(
        name="get_dashboard_configuration_page",
        description="Gets a dashboard configuration page.",
        tags={"Dashboard"},
    )
    def get_dashboard_configuration_page_tool(
        name: Optional[str] = Field(default=None, description="The name of the page.")
    ) -> Any:
        """Gets a dashboard configuration page."""
        api = get_api_client()
        return api.get_dashboard_configuration_page(name=name)

    @mcp.tool(
        name="get_configuration_pages",
        description="Gets the configuration pages.",
        tags={"Dashboard"},
    )
    def get_configuration_pages_tool(
        enable_in_main_menu: Optional[bool] = Field(
            default=None, description="Whether to enable in the main menu."
        )
    ) -> Any:
        """Gets the configuration pages."""
        api = get_api_client()
        return api.get_configuration_pages(enable_in_main_menu=enable_in_main_menu)

    @mcp.tool(name="get_devices", description="Get Devices.", tags={"Devices"})
    def get_devices_tool(
        user_id: Optional[str] = Field(
            default=None, description="Gets or sets the user identifier."
        )
    ) -> Any:
        """Get Devices."""
        api = get_api_client()
        return api.get_devices(user_id=user_id)

    @mcp.tool(name="delete_device", description="Deletes a device.", tags={"Devices"})
    def delete_device_tool(
        id: Optional[str] = Field(default=None, description="Device Id.")
    ) -> Any:
        """Deletes a device."""
        api = get_api_client()
        return api.delete_device(id=id)

    @mcp.tool(
        name="get_device_info", description="Get info for a device.", tags={"Devices"}
    )
    def get_device_info_tool(
        id: Optional[str] = Field(default=None, description="Device Id.")
    ) -> Any:
        """Get info for a device."""
        api = get_api_client()
        return api.get_device_info(id=id)

    @mcp.tool(
        name="get_device_options",
        description="Get options for a device.",
        tags={"Devices"},
    )
    def get_device_options_tool(
        id: Optional[str] = Field(default=None, description="Device Id.")
    ) -> Any:
        """Get options for a device."""
        api = get_api_client()
        return api.get_device_options(id=id)

    @mcp.tool(
        name="update_device_options",
        description="Update device options.",
        tags={"Devices"},
    )
    def update_device_options_tool(
        id: Optional[str] = Field(default=None, description="Device Id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Update device options."""
        api = get_api_client()
        return api.update_device_options(id=id, body=body)

    @mcp.tool(
        name="get_display_preferences",
        description="Get Display Preferences.",
        tags={"DisplayPreferences"},
    )
    def get_display_preferences_tool(
        display_preferences_id: str = Field(description="Display preferences id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
        client: Optional[str] = Field(default=None, description="Client."),
    ) -> Any:
        """Get Display Preferences."""
        api = get_api_client()
        return api.get_display_preferences(
            display_preferences_id=display_preferences_id,
            user_id=user_id,
            client=client,
        )

    @mcp.tool(
        name="update_display_preferences",
        description="Update Display Preferences.",
        tags={"DisplayPreferences"},
    )
    def update_display_preferences_tool(
        display_preferences_id: str = Field(description="Display preferences id."),
        user_id: Optional[str] = Field(default=None, description="User Id."),
        client: Optional[str] = Field(default=None, description="Client."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Update Display Preferences."""
        api = get_api_client()
        return api.update_display_preferences(
            display_preferences_id=display_preferences_id,
            user_id=user_id,
            client=client,
            body=body,
        )

    @mcp.tool(
        name="get_hls_audio_segment",
        description="Gets a video stream using HTTP live streaming.",
        tags={"DynamicHls"},
    )
    def get_hls_audio_segment_tool(
        item_id: str = Field(description="The item id."),
        playlist_id: str = Field(description="The playlist id."),
        segment_id: int = Field(description="The segment id."),
        container: str = Field(
            description="The video container. Possible values are: ts, webm, asf, wmv, ogv, mp4, m4v, mkv, mpeg, mpg, avi, 3gp, wmv, wtv, m2ts, mov, iso, flv."
        ),
        runtime_ticks: Optional[int] = Field(
            default=None, description="The position of the requested segment in ticks."
        ),
        actual_segment_length_ticks: Optional[int] = Field(
            default=None, description="The length of the requested segment in ticks."
        ),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        max_streaming_bitrate: Optional[int] = Field(
            default=None, description="Optional. The maximum streaming bitrate."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
    ) -> Any:
        """Gets a video stream using HTTP live streaming."""
        api = get_api_client()
        return api.get_hls_audio_segment(
            item_id=item_id,
            playlist_id=playlist_id,
            segment_id=segment_id,
            container=container,
            runtime_ticks=runtime_ticks,
            actual_segment_length_ticks=actual_segment_length_ticks,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            max_streaming_bitrate=max_streaming_bitrate,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
        )

    @mcp.tool(
        name="get_variant_hls_audio_playlist",
        description="Gets an audio stream using HTTP live streaming.",
        tags={"DynamicHls"},
    )
    def get_variant_hls_audio_playlist_tool(
        item_id: str = Field(description="The item id."),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        max_streaming_bitrate: Optional[int] = Field(
            default=None, description="Optional. The maximum streaming bitrate."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
    ) -> Any:
        """Gets an audio stream using HTTP live streaming."""
        api = get_api_client()
        return api.get_variant_hls_audio_playlist(
            item_id=item_id,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            max_streaming_bitrate=max_streaming_bitrate,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
        )

    @mcp.tool(
        name="get_master_hls_audio_playlist",
        description="Gets an audio hls playlist stream.",
        tags={"DynamicHls"},
    )
    def get_master_hls_audio_playlist_tool(
        item_id: str = Field(description="The item id."),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        max_streaming_bitrate: Optional[int] = Field(
            default=None, description="Optional. The maximum streaming bitrate."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_adaptive_bitrate_streaming: Optional[bool] = Field(
            default=None, description="Enable adaptive bitrate streaming."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
    ) -> Any:
        """Gets an audio hls playlist stream."""
        api = get_api_client()
        return api.get_master_hls_audio_playlist(
            item_id=item_id,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            max_streaming_bitrate=max_streaming_bitrate,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_adaptive_bitrate_streaming=enable_adaptive_bitrate_streaming,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
        )

    @mcp.tool(
        name="get_hls_video_segment",
        description="Gets a video stream using HTTP live streaming.",
        tags={"DynamicHls"},
    )
    def get_hls_video_segment_tool(
        item_id: str = Field(description="The item id."),
        playlist_id: str = Field(description="The playlist id."),
        segment_id: int = Field(description="The segment id."),
        container: str = Field(
            description="The video container. Possible values are: ts, webm, asf, wmv, ogv, mp4, m4v, mkv, mpeg, mpg, avi, 3gp, wmv, wtv, m2ts, mov, iso, flv."
        ),
        runtime_ticks: Optional[int] = Field(
            default=None, description="The position of the requested segment in ticks."
        ),
        actual_segment_length_ticks: Optional[int] = Field(
            default=None, description="The length of the requested segment in ticks."
        ),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The desired segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        max_width: Optional[int] = Field(
            default=None,
            description="Optional. The maximum horizontal resolution of the encoded video.",
        ),
        max_height: Optional[int] = Field(
            default=None,
            description="Optional. The maximum vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
        always_burn_in_subtitle_when_transcoding: Optional[bool] = Field(
            default=None,
            description="Whether to always burn in subtitles when transcoding.",
        ),
    ) -> Any:
        """Gets a video stream using HTTP live streaming."""
        api = get_api_client()
        return api.get_hls_video_segment(
            item_id=item_id,
            playlist_id=playlist_id,
            segment_id=segment_id,
            container=container,
            runtime_ticks=runtime_ticks,
            actual_segment_length_ticks=actual_segment_length_ticks,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            max_width=max_width,
            max_height=max_height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
            always_burn_in_subtitle_when_transcoding=always_burn_in_subtitle_when_transcoding,
        )

    @mcp.tool(
        name="get_live_hls_stream",
        description="Gets a hls live stream.",
        tags={"DynamicHls"},
    )
    def get_live_hls_stream_tool(
        item_id: str = Field(description="The item id."),
        container: Optional[str] = Field(
            default=None, description="The audio container."
        ),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        max_width: Optional[int] = Field(
            default=None, description="Optional. The max width."
        ),
        max_height: Optional[int] = Field(
            default=None, description="Optional. The max height."
        ),
        enable_subtitles_in_manifest: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to enable subtitles in the manifest.",
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
        always_burn_in_subtitle_when_transcoding: Optional[bool] = Field(
            default=None,
            description="Whether to always burn in subtitles when transcoding.",
        ),
    ) -> Any:
        """Gets a hls live stream."""
        api = get_api_client()
        return api.get_live_hls_stream(
            item_id=item_id,
            container=container,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            max_width=max_width,
            max_height=max_height,
            enable_subtitles_in_manifest=enable_subtitles_in_manifest,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
            always_burn_in_subtitle_when_transcoding=always_burn_in_subtitle_when_transcoding,
        )

    @mcp.tool(
        name="get_variant_hls_video_playlist",
        description="Gets a video stream using HTTP live streaming.",
        tags={"DynamicHls"},
    )
    def get_variant_hls_video_playlist_tool(
        item_id: str = Field(description="The item id."),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        max_width: Optional[int] = Field(
            default=None,
            description="Optional. The maximum horizontal resolution of the encoded video.",
        ),
        max_height: Optional[int] = Field(
            default=None,
            description="Optional. The maximum vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
        always_burn_in_subtitle_when_transcoding: Optional[bool] = Field(
            default=None,
            description="Whether to always burn in subtitles when transcoding.",
        ),
    ) -> Any:
        """Gets a video stream using HTTP live streaming."""
        api = get_api_client()
        return api.get_variant_hls_video_playlist(
            item_id=item_id,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            max_width=max_width,
            max_height=max_height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
            always_burn_in_subtitle_when_transcoding=always_burn_in_subtitle_when_transcoding,
        )

    @mcp.tool(
        name="get_master_hls_video_playlist",
        description="Gets a video hls playlist stream.",
        tags={"DynamicHls"},
    )
    def get_master_hls_video_playlist_tool(
        item_id: str = Field(description="The item id."),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        max_width: Optional[int] = Field(
            default=None,
            description="Optional. The maximum horizontal resolution of the encoded video.",
        ),
        max_height: Optional[int] = Field(
            default=None,
            description="Optional. The maximum vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_adaptive_bitrate_streaming: Optional[bool] = Field(
            default=None, description="Enable adaptive bitrate streaming."
        ),
        enable_trickplay: Optional[bool] = Field(
            default=None,
            description="Enable trickplay image playlists being added to master playlist.",
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Whether to enable Audio Encoding."
        ),
        always_burn_in_subtitle_when_transcoding: Optional[bool] = Field(
            default=None,
            description="Whether to always burn in subtitles when transcoding.",
        ),
    ) -> Any:
        """Gets a video hls playlist stream."""
        api = get_api_client()
        return api.get_master_hls_video_playlist(
            item_id=item_id,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            max_width=max_width,
            max_height=max_height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_adaptive_bitrate_streaming=enable_adaptive_bitrate_streaming,
            enable_trickplay=enable_trickplay,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
            always_burn_in_subtitle_when_transcoding=always_burn_in_subtitle_when_transcoding,
        )

    @mcp.tool(
        name="get_default_directory_browser",
        description="Get Default directory browser.",
        tags={"Environment"},
    )
    def get_default_directory_browser_tool() -> Any:
        """Get Default directory browser."""
        api = get_api_client()
        return api.get_default_directory_browser()

    @mcp.tool(
        name="get_directory_contents",
        description="Gets the contents of a given directory in the file system.",
        tags={"Environment"},
    )
    def get_directory_contents_tool(
        path: Optional[str] = Field(default=None, description="The path."),
        include_files: Optional[bool] = Field(
            default=None,
            description="An optional filter to include or exclude files from the results. true/false.",
        ),
        include_directories: Optional[bool] = Field(
            default=None,
            description="An optional filter to include or exclude folders from the results. true/false.",
        ),
    ) -> Any:
        """Gets the contents of a given directory in the file system."""
        api = get_api_client()
        return api.get_directory_contents(
            path=path,
            include_files=include_files,
            include_directories=include_directories,
        )

    @mcp.tool(
        name="get_drives",
        description="Gets available drives from the server's file system.",
        tags={"Environment"},
    )
    def get_drives_tool() -> Any:
        """Gets available drives from the server's file system."""
        api = get_api_client()
        return api.get_drives()

    @mcp.tool(
        name="get_network_shares",
        description="Gets network paths.",
        tags={"Environment"},
    )
    def get_network_shares_tool() -> Any:
        """Gets network paths."""
        api = get_api_client()
        return api.get_network_shares()

    @mcp.tool(
        name="get_parent_path",
        description="Gets the parent path of a given path.",
        tags={"Environment"},
    )
    def get_parent_path_tool(
        path: Optional[str] = Field(default=None, description="The path.")
    ) -> Any:
        """Gets the parent path of a given path."""
        api = get_api_client()
        return api.get_parent_path(path=path)

    @mcp.tool(name="validate_path", description="Validates path.", tags={"Environment"})
    def validate_path_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Validates path."""
        api = get_api_client()
        return api.validate_path(body=body)

    @mcp.tool(
        name="get_query_filters_legacy",
        description="Gets legacy query filters.",
        tags={"Filter"},
    )
    def get_query_filters_legacy_tool(
        user_id: Optional[str] = Field(default=None, description="Optional. User id."),
        parent_id: Optional[str] = Field(
            default=None, description="Optional. Parent id."
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Filter by MediaType. Allows multiple, comma delimited.",
        ),
    ) -> Any:
        """Gets legacy query filters."""
        api = get_api_client()
        return api.get_query_filters_legacy(
            user_id=user_id,
            parent_id=parent_id,
            include_item_types=include_item_types,
            media_types=media_types,
        )

    @mcp.tool(
        name="get_query_filters", description="Gets query filters.", tags={"Filter"}
    )
    def get_query_filters_tool(
        user_id: Optional[str] = Field(default=None, description="Optional. User id."),
        parent_id: Optional[str] = Field(
            default=None,
            description="Optional. Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        is_airing: Optional[bool] = Field(
            default=None, description="Optional. Is item airing."
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional. Is item movie."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional. Is item sports."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional. Is item kids."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional. Is item news."
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional. Is item series."
        ),
        recursive: Optional[bool] = Field(
            default=None, description="Optional. Search recursive."
        ),
    ) -> Any:
        """Gets query filters."""
        api = get_api_client()
        return api.get_query_filters(
            user_id=user_id,
            parent_id=parent_id,
            include_item_types=include_item_types,
            is_airing=is_airing,
            is_movie=is_movie,
            is_sports=is_sports,
            is_kids=is_kids,
            is_news=is_news,
            is_series=is_series,
            recursive=recursive,
        )

    @mcp.tool(
        name="get_genres",
        description="Gets all genres from a given item, folder, or the entire library.",
        tags={"Genres"},
    )
    def get_genres_tool(
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="The search term."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered out based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered in based on item type. This allows multiple, comma delimited.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not.",
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        user_id: Optional[str] = Field(default=None, description="User id."),
        name_starts_with_or_greater: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally or greater than a given input string.",
        ),
        name_starts_with: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally than a given input string.",
        ),
        name_less_than: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is equally or lesser than a given input string.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending,Descending."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Optional. Include total record count."
        ),
    ) -> Any:
        """Gets all genres from a given item, folder, or the entire library."""
        api = get_api_client()
        return api.get_genres(
            start_index=start_index,
            limit=limit,
            search_term=search_term,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            is_favorite=is_favorite,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            user_id=user_id,
            name_starts_with_or_greater=name_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
            sort_by=sort_by,
            sort_order=sort_order,
            enable_images=enable_images,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(name="get_genre", description="Gets a genre, by name.", tags={"Genres"})
    def get_genre_tool(
        genre_name: str = Field(description="The genre name."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
    ) -> Any:
        """Gets a genre, by name."""
        api = get_api_client()
        return api.get_genre(genre_name=genre_name, user_id=user_id)

    @mcp.tool(
        name="get_hls_audio_segment_legacy_aac",
        description="Gets the specified audio segment for an audio item.",
        tags={"HlsSegment"},
    )
    def get_hls_audio_segment_legacy_aac_tool(
        item_id: str = Field(description="The item id."),
        segment_id: str = Field(description="The segment id."),
    ) -> Any:
        """Gets the specified audio segment for an audio item."""
        api = get_api_client()
        return api.get_hls_audio_segment_legacy_aac(
            item_id=item_id, segment_id=segment_id
        )

    @mcp.tool(
        name="get_hls_audio_segment_legacy_mp3",
        description="Gets the specified audio segment for an audio item.",
        tags={"HlsSegment"},
    )
    def get_hls_audio_segment_legacy_mp3_tool(
        item_id: str = Field(description="The item id."),
        segment_id: str = Field(description="The segment id."),
    ) -> Any:
        """Gets the specified audio segment for an audio item."""
        api = get_api_client()
        return api.get_hls_audio_segment_legacy_mp3(
            item_id=item_id, segment_id=segment_id
        )

    @mcp.tool(
        name="get_hls_video_segment_legacy",
        description="Gets a hls video segment.",
        tags={"HlsSegment"},
    )
    def get_hls_video_segment_legacy_tool(
        item_id: str = Field(description="The item id."),
        playlist_id: str = Field(description="The playlist id."),
        segment_id: str = Field(description="The segment id."),
        segment_container: str = Field(description="The segment container."),
    ) -> Any:
        """Gets a hls video segment."""
        api = get_api_client()
        return api.get_hls_video_segment_legacy(
            item_id=item_id,
            playlist_id=playlist_id,
            segment_id=segment_id,
            segment_container=segment_container,
        )

    @mcp.tool(
        name="get_hls_playlist_legacy",
        description="Gets a hls video playlist.",
        tags={"HlsSegment"},
    )
    def get_hls_playlist_legacy_tool(
        item_id: str = Field(description="The video id."),
        playlist_id: str = Field(description="The playlist id."),
    ) -> Any:
        """Gets a hls video playlist."""
        api = get_api_client()
        return api.get_hls_playlist_legacy(item_id=item_id, playlist_id=playlist_id)

    @mcp.tool(
        name="stop_encoding_process",
        description="Stops an active encoding.",
        tags={"HlsSegment"},
    )
    def stop_encoding_process_tool(
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
    ) -> Any:
        """Stops an active encoding."""
        api = get_api_client()
        return api.stop_encoding_process(
            device_id=device_id, play_session_id=play_session_id
        )

    @mcp.tool(
        name="get_artist_image", description="Get artist image by name.", tags={"Image"}
    )
    def get_artist_image_tool(
        name: str = Field(description="Artist name."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="Image index."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
    ) -> Any:
        """Get artist image by name."""
        api = get_api_client()
        return api.get_artist_image(
            name=name,
            image_type=image_type,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
            image_index=image_index,
        )

    @mcp.tool(
        name="get_splashscreen",
        description="Generates or gets the splashscreen.",
        tags={"Image"},
    )
    def get_splashscreen_tool(
        tag: Optional[str] = Field(
            default=None,
            description="Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
    ) -> Any:
        """Generates or gets the splashscreen."""
        api = get_api_client()
        return api.get_splashscreen(tag=tag, format=format)

    @mcp.tool(
        name="upload_custom_splashscreen",
        description="Uploads a custom splashscreen. The body is expected to the image contents base64 encoded.",
        tags={"Image"},
    )
    def upload_custom_splashscreen_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Uploads a custom splashscreen. The body is expected to the image contents base64 encoded."""
        api = get_api_client()
        return api.upload_custom_splashscreen(body=body)

    @mcp.tool(
        name="delete_custom_splashscreen",
        description="Delete a custom splashscreen.",
        tags={"Image"},
    )
    def delete_custom_splashscreen_tool() -> Any:
        """Delete a custom splashscreen."""
        api = get_api_client()
        return api.delete_custom_splashscreen()

    @mcp.tool(
        name="get_genre_image", description="Get genre image by name.", tags={"Image"}
    )
    def get_genre_image_tool(
        name: str = Field(description="Genre name."),
        image_type: str = Field(description="Image type."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
        image_index: Optional[int] = Field(default=None, description="Image index."),
    ) -> Any:
        """Get genre image by name."""
        api = get_api_client()
        return api.get_genre_image(
            name=name,
            image_type=image_type,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
            image_index=image_index,
        )

    @mcp.tool(
        name="get_genre_image_by_index",
        description="Get genre image by name.",
        tags={"Image"},
    )
    def get_genre_image_by_index_tool(
        name: str = Field(description="Genre name."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="Image index."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
    ) -> Any:
        """Get genre image by name."""
        api = get_api_client()
        return api.get_genre_image_by_index(
            name=name,
            image_type=image_type,
            image_index=image_index,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
        )

    @mcp.tool(
        name="get_item_image_infos", description="Get item image infos.", tags={"Image"}
    )
    def get_item_image_infos_tool(item_id: str = Field(description="Item id.")) -> Any:
        """Get item image infos."""
        api = get_api_client()
        return api.get_item_image_infos(item_id=item_id)

    @mcp.tool(
        name="delete_item_image", description="Delete an item's image.", tags={"Image"}
    )
    def delete_item_image_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        image_index: Optional[int] = Field(
            default=None, description="The image index."
        ),
    ) -> Any:
        """Delete an item's image."""
        api = get_api_client()
        return api.delete_item_image(
            item_id=item_id, image_type=image_type, image_index=image_index
        )

    @mcp.tool(name="set_item_image", description="Set item image.", tags={"Image"})
    def set_item_image_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Set item image."""
        api = get_api_client()
        return api.set_item_image(item_id=item_id, image_type=image_type, body=body)

    @mcp.tool(
        name="get_item_image", description="Gets the item's image.", tags={"Image"}
    )
    def get_item_image_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Drawing.ImageFormat of the returned image.",
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
        image_index: Optional[int] = Field(default=None, description="Image index."),
    ) -> Any:
        """Gets the item's image."""
        api = get_api_client()
        return api.get_item_image(
            item_id=item_id,
            image_type=image_type,
            max_width=max_width,
            max_height=max_height,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            tag=tag,
            format=format,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
            image_index=image_index,
        )

    @mcp.tool(
        name="delete_item_image_by_index",
        description="Delete an item's image.",
        tags={"Image"},
    )
    def delete_item_image_by_index_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="The image index."),
    ) -> Any:
        """Delete an item's image."""
        api = get_api_client()
        return api.delete_item_image_by_index(
            item_id=item_id, image_type=image_type, image_index=image_index
        )

    @mcp.tool(
        name="set_item_image_by_index", description="Set item image.", tags={"Image"}
    )
    def set_item_image_by_index_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="(Unused) Image index."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Set item image."""
        api = get_api_client()
        return api.set_item_image_by_index(
            item_id=item_id, image_type=image_type, image_index=image_index, body=body
        )

    @mcp.tool(
        name="get_item_image_by_index",
        description="Gets the item's image.",
        tags={"Image"},
    )
    def get_item_image_by_index_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="Image index."),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Drawing.ImageFormat of the returned image.",
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
    ) -> Any:
        """Gets the item's image."""
        api = get_api_client()
        return api.get_item_image_by_index(
            item_id=item_id,
            image_type=image_type,
            image_index=image_index,
            max_width=max_width,
            max_height=max_height,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            tag=tag,
            format=format,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
        )

    @mcp.tool(
        name="get_item_image2", description="Gets the item's image.", tags={"Image"}
    )
    def get_item_image2_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        max_width: int = Field(description="The maximum image width to return."),
        max_height: int = Field(description="The maximum image height to return."),
        tag: str = Field(
            description="Optional. Supply the cache tag from the item object to receive strong caching headers."
        ),
        format: str = Field(
            description="Determines the output format of the image - original,gif,jpg,png."
        ),
        percent_played: float = Field(
            description="Optional. Percent to render for the percent played overlay."
        ),
        unplayed_count: int = Field(
            description="Optional. Unplayed count overlay to render."
        ),
        image_index: int = Field(description="Image index."),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
    ) -> Any:
        """Gets the item's image."""
        api = get_api_client()
        return api.get_item_image2(
            item_id=item_id,
            image_type=image_type,
            max_width=max_width,
            max_height=max_height,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            tag=tag,
            format=format,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
            image_index=image_index,
        )

    @mcp.tool(
        name="update_item_image_index",
        description="Updates the index for an item image.",
        tags={"Image"},
    )
    def update_item_image_index_tool(
        item_id: str = Field(description="Item id."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="Old image index."),
        new_index: Optional[int] = Field(default=None, description="New image index."),
    ) -> Any:
        """Updates the index for an item image."""
        api = get_api_client()
        return api.update_item_image_index(
            item_id=item_id,
            image_type=image_type,
            image_index=image_index,
            new_index=new_index,
        )

    @mcp.tool(
        name="get_music_genre_image",
        description="Get music genre image by name.",
        tags={"Image"},
    )
    def get_music_genre_image_tool(
        name: str = Field(description="Music genre name."),
        image_type: str = Field(description="Image type."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
        image_index: Optional[int] = Field(default=None, description="Image index."),
    ) -> Any:
        """Get music genre image by name."""
        api = get_api_client()
        return api.get_music_genre_image(
            name=name,
            image_type=image_type,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
            image_index=image_index,
        )

    @mcp.tool(
        name="get_music_genre_image_by_index",
        description="Get music genre image by name.",
        tags={"Image"},
    )
    def get_music_genre_image_by_index_tool(
        name: str = Field(description="Music genre name."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="Image index."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
    ) -> Any:
        """Get music genre image by name."""
        api = get_api_client()
        return api.get_music_genre_image_by_index(
            name=name,
            image_type=image_type,
            image_index=image_index,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
        )

    @mcp.tool(
        name="get_person_image", description="Get person image by name.", tags={"Image"}
    )
    def get_person_image_tool(
        name: str = Field(description="Person name."),
        image_type: str = Field(description="Image type."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
        image_index: Optional[int] = Field(default=None, description="Image index."),
    ) -> Any:
        """Get person image by name."""
        api = get_api_client()
        return api.get_person_image(
            name=name,
            image_type=image_type,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
            image_index=image_index,
        )

    @mcp.tool(
        name="get_person_image_by_index",
        description="Get person image by name.",
        tags={"Image"},
    )
    def get_person_image_by_index_tool(
        name: str = Field(description="Person name."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="Image index."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
    ) -> Any:
        """Get person image by name."""
        api = get_api_client()
        return api.get_person_image_by_index(
            name=name,
            image_type=image_type,
            image_index=image_index,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
        )

    @mcp.tool(
        name="get_studio_image", description="Get studio image by name.", tags={"Image"}
    )
    def get_studio_image_tool(
        name: str = Field(description="Studio name."),
        image_type: str = Field(description="Image type."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
        image_index: Optional[int] = Field(default=None, description="Image index."),
    ) -> Any:
        """Get studio image by name."""
        api = get_api_client()
        return api.get_studio_image(
            name=name,
            image_type=image_type,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
            image_index=image_index,
        )

    @mcp.tool(
        name="get_studio_image_by_index",
        description="Get studio image by name.",
        tags={"Image"},
    )
    def get_studio_image_by_index_tool(
        name: str = Field(description="Studio name."),
        image_type: str = Field(description="Image type."),
        image_index: int = Field(description="Image index."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
        max_width: Optional[int] = Field(
            default=None, description="The maximum image width to return."
        ),
        max_height: Optional[int] = Field(
            default=None, description="The maximum image height to return."
        ),
        percent_played: Optional[float] = Field(
            default=None,
            description="Optional. Percent to render for the percent played overlay.",
        ),
        unplayed_count: Optional[int] = Field(
            default=None, description="Optional. Unplayed count overlay to render."
        ),
        width: Optional[int] = Field(
            default=None, description="The fixed image width to return."
        ),
        height: Optional[int] = Field(
            default=None, description="The fixed image height to return."
        ),
        quality: Optional[int] = Field(
            default=None,
            description="Optional. Quality setting, from 0-100. Defaults to 90 and should suffice in most cases.",
        ),
        fill_width: Optional[int] = Field(
            default=None, description="Width of box to fill."
        ),
        fill_height: Optional[int] = Field(
            default=None, description="Height of box to fill."
        ),
        blur: Optional[int] = Field(default=None, description="Optional. Blur image."),
        background_color: Optional[str] = Field(
            default=None,
            description="Optional. Apply a background color for transparent images.",
        ),
        foreground_layer: Optional[str] = Field(
            default=None,
            description="Optional. Apply a foreground layer on top of the image.",
        ),
    ) -> Any:
        """Get studio image by name."""
        api = get_api_client()
        return api.get_studio_image_by_index(
            name=name,
            image_type=image_type,
            image_index=image_index,
            tag=tag,
            format=format,
            max_width=max_width,
            max_height=max_height,
            percent_played=percent_played,
            unplayed_count=unplayed_count,
            width=width,
            height=height,
            quality=quality,
            fill_width=fill_width,
            fill_height=fill_height,
            blur=blur,
            background_color=background_color,
            foreground_layer=foreground_layer,
        )

    @mcp.tool(
        name="post_user_image", description="Sets the user image.", tags={"Image"}
    )
    def post_user_image_tool(
        user_id: Optional[str] = Field(default=None, description="User Id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Sets the user image."""
        api = get_api_client()
        return api.post_user_image(user_id=user_id, body=body)

    @mcp.tool(
        name="delete_user_image", description="Delete the user's image.", tags={"Image"}
    )
    def delete_user_image_tool(
        user_id: Optional[str] = Field(default=None, description="User Id.")
    ) -> Any:
        """Delete the user's image."""
        api = get_api_client()
        return api.delete_user_image(user_id=user_id)

    @mcp.tool(
        name="get_user_image", description="Get user profile image.", tags={"Image"}
    )
    def get_user_image_tool(
        user_id: Optional[str] = Field(default=None, description="User id."),
        tag: Optional[str] = Field(
            default=None,
            description="Optional. Supply the cache tag from the item object to receive strong caching headers.",
        ),
        format: Optional[str] = Field(
            default=None,
            description="Determines the output format of the image - original,gif,jpg,png.",
        ),
    ) -> Any:
        """Get user profile image."""
        api = get_api_client()
        return api.get_user_image(user_id=user_id, tag=tag, format=format)

    @mcp.tool(
        name="get_instant_mix_from_album",
        description="Creates an instant playlist based on a given album.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_album_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given album."""
        api = get_api_client()
        return api.get_instant_mix_from_album(
            item_id=item_id,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_instant_mix_from_artists",
        description="Creates an instant playlist based on a given artist.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_artists_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given artist."""
        api = get_api_client()
        return api.get_instant_mix_from_artists(
            item_id=item_id,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_instant_mix_from_artists2",
        description="Creates an instant playlist based on a given artist.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_artists2_tool(
        id: Optional[str] = Field(default=None, description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given artist."""
        api = get_api_client()
        return api.get_instant_mix_from_artists2(
            id=id,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_instant_mix_from_item",
        description="Creates an instant playlist based on a given item.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_item_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given item."""
        api = get_api_client()
        return api.get_instant_mix_from_item(
            item_id=item_id,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_instant_mix_from_music_genre_by_name",
        description="Creates an instant playlist based on a given genre.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_music_genre_by_name_tool(
        name: str = Field(description="The genre name."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given genre."""
        api = get_api_client()
        return api.get_instant_mix_from_music_genre_by_name(
            name=name,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_instant_mix_from_music_genre_by_id",
        description="Creates an instant playlist based on a given genre.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_music_genre_by_id_tool(
        id: Optional[str] = Field(default=None, description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given genre."""
        api = get_api_client()
        return api.get_instant_mix_from_music_genre_by_id(
            id=id,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_instant_mix_from_playlist",
        description="Creates an instant playlist based on a given playlist.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_playlist_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given playlist."""
        api = get_api_client()
        return api.get_instant_mix_from_playlist(
            item_id=item_id,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_instant_mix_from_song",
        description="Creates an instant playlist based on a given song.",
        tags={"InstantMix"},
    )
    def get_instant_mix_from_song_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Creates an instant playlist based on a given song."""
        api = get_api_client()
        return api.get_instant_mix_from_song(
            item_id=item_id,
            user_id=user_id,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="get_external_id_infos",
        description="Get the item's external id info.",
        tags={"ItemLookup"},
    )
    def get_external_id_infos_tool(item_id: str = Field(description="Item id.")) -> Any:
        """Get the item's external id info."""
        api = get_api_client()
        return api.get_external_id_infos(item_id=item_id)

    @mcp.tool(
        name="apply_search_criteria",
        description="Applies search criteria to an item and refreshes metadata.",
        tags={"ItemLookup"},
    )
    def apply_search_criteria_tool(
        item_id: str = Field(description="Item id."),
        replace_all_images: Optional[bool] = Field(
            default=None,
            description="Optional. Whether or not to replace all images. Default: True.",
        ),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Applies search criteria to an item and refreshes metadata."""
        api = get_api_client()
        return api.apply_search_criteria(
            item_id=item_id, replace_all_images=replace_all_images, body=body
        )

    @mcp.tool(
        name="get_book_remote_search_results",
        description="Get book remote search.",
        tags={"ItemLookup"},
    )
    def get_book_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get book remote search."""
        api = get_api_client()
        return api.get_book_remote_search_results(body=body)

    @mcp.tool(
        name="get_box_set_remote_search_results",
        description="Get box set remote search.",
        tags={"ItemLookup"},
    )
    def get_box_set_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get box set remote search."""
        api = get_api_client()
        return api.get_box_set_remote_search_results(body=body)

    @mcp.tool(
        name="get_movie_remote_search_results",
        description="Get movie remote search.",
        tags={"ItemLookup"},
    )
    def get_movie_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get movie remote search."""
        api = get_api_client()
        return api.get_movie_remote_search_results(body=body)

    @mcp.tool(
        name="get_music_album_remote_search_results",
        description="Get music album remote search.",
        tags={"ItemLookup"},
    )
    def get_music_album_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get music album remote search."""
        api = get_api_client()
        return api.get_music_album_remote_search_results(body=body)

    @mcp.tool(
        name="get_music_artist_remote_search_results",
        description="Get music artist remote search.",
        tags={"ItemLookup"},
    )
    def get_music_artist_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get music artist remote search."""
        api = get_api_client()
        return api.get_music_artist_remote_search_results(body=body)

    @mcp.tool(
        name="get_music_video_remote_search_results",
        description="Get music video remote search.",
        tags={"ItemLookup"},
    )
    def get_music_video_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get music video remote search."""
        api = get_api_client()
        return api.get_music_video_remote_search_results(body=body)

    @mcp.tool(
        name="get_person_remote_search_results",
        description="Get person remote search.",
        tags={"ItemLookup"},
    )
    def get_person_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get person remote search."""
        api = get_api_client()
        return api.get_person_remote_search_results(body=body)

    @mcp.tool(
        name="get_series_remote_search_results",
        description="Get series remote search.",
        tags={"ItemLookup"},
    )
    def get_series_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get series remote search."""
        api = get_api_client()
        return api.get_series_remote_search_results(body=body)

    @mcp.tool(
        name="get_trailer_remote_search_results",
        description="Get trailer remote search.",
        tags={"ItemLookup"},
    )
    def get_trailer_remote_search_results_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Get trailer remote search."""
        api = get_api_client()
        return api.get_trailer_remote_search_results(body=body)

    @mcp.tool(
        name="refresh_item",
        description="Refreshes metadata for an item.",
        tags={"ItemRefresh"},
    )
    def refresh_item_tool(
        item_id: str = Field(description="Item id."),
        metadata_refresh_mode: Optional[str] = Field(
            default=None, description="(Optional) Specifies the metadata refresh mode."
        ),
        image_refresh_mode: Optional[str] = Field(
            default=None, description="(Optional) Specifies the image refresh mode."
        ),
        replace_all_metadata: Optional[bool] = Field(
            default=None,
            description="(Optional) Determines if metadata should be replaced. Only applicable if mode is FullRefresh.",
        ),
        replace_all_images: Optional[bool] = Field(
            default=None,
            description="(Optional) Determines if images should be replaced. Only applicable if mode is FullRefresh.",
        ),
        regenerate_trickplay: Optional[bool] = Field(
            default=None,
            description="(Optional) Determines if trickplay images should be replaced. Only applicable if mode is FullRefresh.",
        ),
    ) -> Any:
        """Refreshes metadata for an item."""
        api = get_api_client()
        return api.refresh_item(
            item_id=item_id,
            metadata_refresh_mode=metadata_refresh_mode,
            image_refresh_mode=image_refresh_mode,
            replace_all_metadata=replace_all_metadata,
            replace_all_images=replace_all_images,
            regenerate_trickplay=regenerate_trickplay,
        )

    @mcp.tool(
        name="get_items", description="Gets items based on a query.", tags={"Items"}
    )
    def get_items_tool(
        user_id: Optional[str] = Field(
            default=None,
            description="The user id supplied as query parameter; this is required when not using an API key.",
        ),
        max_official_rating: Optional[str] = Field(
            default=None,
            description="Optional filter by maximum official rating (PG, PG-13, TV-MA, etc).",
        ),
        has_theme_song: Optional[bool] = Field(
            default=None, description="Optional filter by items with theme songs."
        ),
        has_theme_video: Optional[bool] = Field(
            default=None, description="Optional filter by items with theme videos."
        ),
        has_subtitles: Optional[bool] = Field(
            default=None, description="Optional filter by items with subtitles."
        ),
        has_special_feature: Optional[bool] = Field(
            default=None, description="Optional filter by items with special features."
        ),
        has_trailer: Optional[bool] = Field(
            default=None, description="Optional filter by items with trailers."
        ),
        adjacent_to: Optional[str] = Field(
            default=None,
            description="Optional. Return items that are siblings of a supplied item.",
        ),
        index_number: Optional[int] = Field(
            default=None, description="Optional filter by index number."
        ),
        parent_index_number: Optional[int] = Field(
            default=None, description="Optional filter by parent index number."
        ),
        has_parental_rating: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have or do not have a parental rating.",
        ),
        is_hd: Optional[bool] = Field(
            default=None, description="Optional filter by items that are HD or not."
        ),
        is4_k: Optional[bool] = Field(
            default=None, description="Optional filter by items that are 4K or not."
        ),
        location_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on LocationType. This allows multiple, comma delimited.",
        ),
        exclude_location_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on the LocationType. This allows multiple, comma delimited.",
        ),
        is_missing: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are missing episodes or not.",
        ),
        is_unaired: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are unaired episodes or not.",
        ),
        min_community_rating: Optional[float] = Field(
            default=None, description="Optional filter by minimum community rating."
        ),
        min_critic_rating: Optional[float] = Field(
            default=None, description="Optional filter by minimum critic rating."
        ),
        min_premiere_date: Optional[str] = Field(
            default=None,
            description="Optional. The minimum premiere date. Format = ISO.",
        ),
        min_date_last_saved: Optional[str] = Field(
            default=None,
            description="Optional. The minimum last saved date. Format = ISO.",
        ),
        min_date_last_saved_for_user: Optional[str] = Field(
            default=None,
            description="Optional. The minimum last saved date for the current user. Format = ISO.",
        ),
        max_premiere_date: Optional[str] = Field(
            default=None,
            description="Optional. The maximum premiere date. Format = ISO.",
        ),
        has_overview: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have an overview or not.",
        ),
        has_imdb_id: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have an IMDb id or not.",
        ),
        has_tmdb_id: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have a TMDb id or not.",
        ),
        has_tvdb_id: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have a TVDb id or not.",
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional filter for live tv movies."
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional filter for live tv series."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional filter for live tv news."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional filter for live tv kids."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional filter for live tv sports."
        ),
        exclude_item_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered by excluding item ids. This allows multiple, comma delimited.",
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        recursive: Optional[bool] = Field(
            default=None,
            description="When searching within folders, this determines whether or not the search will be recursive. true/false.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="Optional. Filter based on a search term."
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending, Descending."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on the item type. This allows multiple, comma delimited.",
        ),
        filters: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional filters to apply. This allows multiple, comma delimited. Options: IsFolder, IsNotFolder, IsUnplayed, IsPlayed, IsFavorite, IsResumable, Likes, Dislikes.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by MediaType. Allows multiple, comma delimited.",
        ),
        image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on those containing image types. This allows multiple, comma delimited.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
        is_played: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are played, or not.",
        ),
        genres: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre. This allows multiple, pipe delimited.",
        ),
        official_ratings: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on OfficialRating. This allows multiple, pipe delimited.",
        ),
        tags: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on tag. This allows multiple, pipe delimited.",
        ),
        years: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on production year. This allows multiple, comma delimited.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional, include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        person: Optional[str] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person.",
        ),
        person_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person id.",
        ),
        person_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, along with Person, results will be filtered to include only those containing the specified person and PersonType. Allows multiple, comma-delimited.",
        ),
        studios: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio. This allows multiple, pipe delimited.",
        ),
        artists: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on artists. This allows multiple, pipe delimited.",
        ),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on artist id. This allows multiple, pipe delimited.",
        ),
        artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified artist id.",
        ),
        album_artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified album artist id.",
        ),
        contributing_artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified contributing artist id.",
        ),
        albums: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on album. This allows multiple, pipe delimited.",
        ),
        album_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on album id. This allows multiple, pipe delimited.",
        ),
        ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specific items are needed, specify a list of item id's to retrieve. This allows multiple, comma delimited.",
        ),
        video_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by VideoType (videofile, dvd, bluray, iso). Allows multiple, comma delimited.",
        ),
        min_official_rating: Optional[str] = Field(
            default=None,
            description="Optional filter by minimum official rating (PG, PG-13, TV-MA, etc).",
        ),
        is_locked: Optional[bool] = Field(
            default=None, description="Optional filter by items that are locked."
        ),
        is_place_holder: Optional[bool] = Field(
            default=None, description="Optional filter by items that are placeholders."
        ),
        has_official_rating: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have official ratings.",
        ),
        collapse_box_set_items: Optional[bool] = Field(
            default=None,
            description="Whether or not to hide items behind their boxsets.",
        ),
        min_width: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the minimum width of the item.",
        ),
        min_height: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the minimum height of the item.",
        ),
        max_width: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the maximum width of the item.",
        ),
        max_height: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the maximum height of the item.",
        ),
        is3_d: Optional[bool] = Field(
            default=None, description="Optional filter by items that are 3D, or not."
        ),
        series_status: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by Series Status. Allows multiple, comma delimited.",
        ),
        name_starts_with_or_greater: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally or greater than a given input string.",
        ),
        name_starts_with: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally than a given input string.",
        ),
        name_less_than: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is equally or lesser than a given input string.",
        ),
        studio_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio id. This allows multiple, pipe delimited.",
        ),
        genre_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre id. This allows multiple, pipe delimited.",
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Optional. Enable the total record count."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
    ) -> Any:
        """Gets items based on a query."""
        api = get_api_client()
        return api.get_items(
            user_id=user_id,
            max_official_rating=max_official_rating,
            has_theme_song=has_theme_song,
            has_theme_video=has_theme_video,
            has_subtitles=has_subtitles,
            has_special_feature=has_special_feature,
            has_trailer=has_trailer,
            adjacent_to=adjacent_to,
            index_number=index_number,
            parent_index_number=parent_index_number,
            has_parental_rating=has_parental_rating,
            is_hd=is_hd,
            is4_k=is4_k,
            location_types=location_types,
            exclude_location_types=exclude_location_types,
            is_missing=is_missing,
            is_unaired=is_unaired,
            min_community_rating=min_community_rating,
            min_critic_rating=min_critic_rating,
            min_premiere_date=min_premiere_date,
            min_date_last_saved=min_date_last_saved,
            min_date_last_saved_for_user=min_date_last_saved_for_user,
            max_premiere_date=max_premiere_date,
            has_overview=has_overview,
            has_imdb_id=has_imdb_id,
            has_tmdb_id=has_tmdb_id,
            has_tvdb_id=has_tvdb_id,
            is_movie=is_movie,
            is_series=is_series,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            exclude_item_ids=exclude_item_ids,
            start_index=start_index,
            limit=limit,
            recursive=recursive,
            search_term=search_term,
            sort_order=sort_order,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            filters=filters,
            is_favorite=is_favorite,
            media_types=media_types,
            image_types=image_types,
            sort_by=sort_by,
            is_played=is_played,
            genres=genres,
            official_ratings=official_ratings,
            tags=tags,
            years=years,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            person=person,
            person_ids=person_ids,
            person_types=person_types,
            studios=studios,
            artists=artists,
            exclude_artist_ids=exclude_artist_ids,
            artist_ids=artist_ids,
            album_artist_ids=album_artist_ids,
            contributing_artist_ids=contributing_artist_ids,
            albums=albums,
            album_ids=album_ids,
            ids=ids,
            video_types=video_types,
            min_official_rating=min_official_rating,
            is_locked=is_locked,
            is_place_holder=is_place_holder,
            has_official_rating=has_official_rating,
            collapse_box_set_items=collapse_box_set_items,
            min_width=min_width,
            min_height=min_height,
            max_width=max_width,
            max_height=max_height,
            is3_d=is3_d,
            series_status=series_status,
            name_starts_with_or_greater=name_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
            studio_ids=studio_ids,
            genre_ids=genre_ids,
            enable_total_record_count=enable_total_record_count,
            enable_images=enable_images,
        )

    @mcp.tool(
        name="delete_items",
        description="Deletes items from the library and filesystem.",
        tags={"Library"},
    )
    def delete_items_tool(
        ids: Optional[List[Any]] = Field(default=None, description="The item ids.")
    ) -> Any:
        """Deletes items from the library and filesystem."""
        api = get_api_client()
        return api.delete_items(ids=ids)

    @mcp.tool(
        name="get_item_user_data", description="Get Item User Data.", tags={"Items"}
    )
    def get_item_user_data_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
    ) -> Any:
        """Get Item User Data."""
        api = get_api_client()
        return api.get_item_user_data(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="update_item_user_data",
        description="Update Item User Data.",
        tags={"Items"},
    )
    def update_item_user_data_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Update Item User Data."""
        api = get_api_client()
        return api.update_item_user_data(user_id=user_id, item_id=item_id, body=body)

    @mcp.tool(
        name="get_resume_items",
        description="Gets items based on a query.",
        tags={"Items"},
    )
    def get_resume_items_tool(
        user_id: Optional[str] = Field(default=None, description="The user id."),
        start_index: Optional[int] = Field(
            default=None, description="The start index."
        ),
        limit: Optional[int] = Field(default=None, description="The item limit."),
        search_term: Optional[str] = Field(
            default=None, description="The search term."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Filter by MediaType. Allows multiple, comma delimited.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on the item type. This allows multiple, comma delimited.",
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Optional. Enable the total record count."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        exclude_active_sessions: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to exclude the currently active sessions.",
        ),
    ) -> Any:
        """Gets items based on a query."""
        api = get_api_client()
        return api.get_resume_items(
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            search_term=search_term,
            parent_id=parent_id,
            fields=fields,
            media_types=media_types,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            enable_total_record_count=enable_total_record_count,
            enable_images=enable_images,
            exclude_active_sessions=exclude_active_sessions,
        )

    @mcp.tool(name="update_item", description="Updates an item.", tags={"ItemUpdate"})
    def update_item_tool(
        item_id: str = Field(description="The item id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates an item."""
        api = get_api_client()
        return api.update_item(item_id=item_id, body=body)

    @mcp.tool(
        name="delete_item",
        description="Deletes an item from the library and filesystem.",
        tags={"Library"},
    )
    def delete_item_tool(item_id: str = Field(description="The item id.")) -> Any:
        """Deletes an item from the library and filesystem."""
        api = get_api_client()
        return api.delete_item(item_id=item_id)

    @mcp.tool(
        name="get_item",
        description="Gets an item from a user's library.",
        tags={"UserLibrary"},
    )
    def get_item_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Gets an item from a user's library."""
        api = get_api_client()
        return api.get_item(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="update_item_content_type",
        description="Updates an item's content type.",
        tags={"ItemUpdate"},
    )
    def update_item_content_type_tool(
        item_id: str = Field(description="The item id."),
        content_type: Optional[str] = Field(
            default=None, description="The content type of the item."
        ),
    ) -> Any:
        """Updates an item's content type."""
        api = get_api_client()
        return api.update_item_content_type(item_id=item_id, content_type=content_type)

    @mcp.tool(
        name="get_metadata_editor_info",
        description="Gets metadata editor info for an item.",
        tags={"ItemUpdate"},
    )
    def get_metadata_editor_info_tool(
        item_id: str = Field(description="The item id."),
    ) -> Any:
        """Gets metadata editor info for an item."""
        api = get_api_client()
        return api.get_metadata_editor_info(item_id=item_id)

    @mcp.tool(
        name="get_similar_albums", description="Gets similar items.", tags={"Library"}
    )
    def get_similar_albums_tool(
        item_id: str = Field(description="The item id."),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None, description="Exclude artist ids."
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
    ) -> Any:
        """Gets similar items."""
        api = get_api_client()
        return api.get_similar_albums(
            item_id=item_id,
            exclude_artist_ids=exclude_artist_ids,
            user_id=user_id,
            limit=limit,
            fields=fields,
        )

    @mcp.tool(
        name="get_similar_artists", description="Gets similar items.", tags={"Library"}
    )
    def get_similar_artists_tool(
        item_id: str = Field(description="The item id."),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None, description="Exclude artist ids."
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
    ) -> Any:
        """Gets similar items."""
        api = get_api_client()
        return api.get_similar_artists(
            item_id=item_id,
            exclude_artist_ids=exclude_artist_ids,
            user_id=user_id,
            limit=limit,
            fields=fields,
        )

    @mcp.tool(
        name="get_ancestors",
        description="Gets all parents of an item.",
        tags={"Library"},
    )
    def get_ancestors_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
    ) -> Any:
        """Gets all parents of an item."""
        api = get_api_client()
        return api.get_ancestors(item_id=item_id, user_id=user_id)

    @mcp.tool(
        name="get_critic_reviews",
        description="Gets critic review for an item.",
        tags={"Library"},
    )
    def get_critic_reviews_tool(item_id: str = Field(description="")) -> Any:
        """Gets critic review for an item."""
        api = get_api_client()
        return api.get_critic_reviews(item_id=item_id)

    @mcp.tool(
        name="get_download", description="Downloads item media.", tags={"Library"}
    )
    def get_download_tool(item_id: str = Field(description="The item id.")) -> Any:
        """Downloads item media."""
        api = get_api_client()
        return api.get_download(item_id=item_id)

    @mcp.tool(
        name="get_file",
        description="Get the original file of an item.",
        tags={"Library"},
    )
    def get_file_tool(item_id: str = Field(description="The item id.")) -> Any:
        """Get the original file of an item."""
        api = get_api_client()
        return api.get_file(item_id=item_id)

    @mcp.tool(
        name="get_similar_items", description="Gets similar items.", tags={"Library"}
    )
    def get_similar_items_tool(
        item_id: str = Field(description="The item id."),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None, description="Exclude artist ids."
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
    ) -> Any:
        """Gets similar items."""
        api = get_api_client()
        return api.get_similar_items(
            item_id=item_id,
            exclude_artist_ids=exclude_artist_ids,
            user_id=user_id,
            limit=limit,
            fields=fields,
        )

    @mcp.tool(
        name="get_theme_media",
        description="Get theme songs and videos for an item.",
        tags={"Library"},
    )
    def get_theme_media_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        inherit_from_parent: Optional[bool] = Field(
            default=None,
            description="Optional. Determines whether or not parent items should be searched for theme media.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Optional. Sort Order - Ascending, Descending."
        ),
    ) -> Any:
        """Get theme songs and videos for an item."""
        api = get_api_client()
        return api.get_theme_media(
            item_id=item_id,
            user_id=user_id,
            inherit_from_parent=inherit_from_parent,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    @mcp.tool(
        name="get_theme_songs",
        description="Get theme songs for an item.",
        tags={"Library"},
    )
    def get_theme_songs_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        inherit_from_parent: Optional[bool] = Field(
            default=None,
            description="Optional. Determines whether or not parent items should be searched for theme media.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Optional. Sort Order - Ascending, Descending."
        ),
    ) -> Any:
        """Get theme songs for an item."""
        api = get_api_client()
        return api.get_theme_songs(
            item_id=item_id,
            user_id=user_id,
            inherit_from_parent=inherit_from_parent,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    @mcp.tool(
        name="get_theme_videos",
        description="Get theme videos for an item.",
        tags={"Library"},
    )
    def get_theme_videos_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        inherit_from_parent: Optional[bool] = Field(
            default=None,
            description="Optional. Determines whether or not parent items should be searched for theme media.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Optional. Sort Order - Ascending, Descending."
        ),
    ) -> Any:
        """Get theme videos for an item."""
        api = get_api_client()
        return api.get_theme_videos(
            item_id=item_id,
            user_id=user_id,
            inherit_from_parent=inherit_from_parent,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    @mcp.tool(name="get_item_counts", description="Get item counts.", tags={"Library"})
    def get_item_counts_tool(
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Get counts from a specific user's library.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None, description="Optional. Get counts of favorite items."
        ),
    ) -> Any:
        """Get item counts."""
        api = get_api_client()
        return api.get_item_counts(user_id=user_id, is_favorite=is_favorite)

    @mcp.tool(
        name="get_library_options_info",
        description="Gets the library options info.",
        tags={"Library"},
    )
    def get_library_options_info_tool(
        library_content_type: Optional[str] = Field(
            default=None, description="Library content type."
        ),
        is_new_library: Optional[bool] = Field(
            default=None, description="Whether this is a new library."
        ),
    ) -> Any:
        """Gets the library options info."""
        api = get_api_client()
        return api.get_library_options_info(
            library_content_type=library_content_type, is_new_library=is_new_library
        )

    @mcp.tool(
        name="post_updated_media",
        description="Reports that new movies have been added by an external source.",
        tags={"Library"},
    )
    def post_updated_media_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Reports that new movies have been added by an external source."""
        api = get_api_client()
        return api.post_updated_media(body=body)

    @mcp.tool(
        name="get_media_folders",
        description="Gets all user media folders.",
        tags={"Library"},
    )
    def get_media_folders_tool(
        is_hidden: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by folders that are marked hidden, or not.",
        )
    ) -> Any:
        """Gets all user media folders."""
        api = get_api_client()
        return api.get_media_folders(is_hidden=is_hidden)

    @mcp.tool(
        name="post_added_movies",
        description="Reports that new movies have been added by an external source.",
        tags={"Library"},
    )
    def post_added_movies_tool(
        tmdb_id: Optional[str] = Field(default=None, description="The tmdbId."),
        imdb_id: Optional[str] = Field(default=None, description="The imdbId."),
    ) -> Any:
        """Reports that new movies have been added by an external source."""
        api = get_api_client()
        return api.post_added_movies(tmdb_id=tmdb_id, imdb_id=imdb_id)

    @mcp.tool(
        name="post_updated_movies",
        description="Reports that new movies have been added by an external source.",
        tags={"Library"},
    )
    def post_updated_movies_tool(
        tmdb_id: Optional[str] = Field(default=None, description="The tmdbId."),
        imdb_id: Optional[str] = Field(default=None, description="The imdbId."),
    ) -> Any:
        """Reports that new movies have been added by an external source."""
        api = get_api_client()
        return api.post_updated_movies(tmdb_id=tmdb_id, imdb_id=imdb_id)

    @mcp.tool(
        name="get_physical_paths",
        description="Gets a list of physical paths from virtual folders.",
        tags={"Library"},
    )
    def get_physical_paths_tool() -> Any:
        """Gets a list of physical paths from virtual folders."""
        api = get_api_client()
        return api.get_physical_paths()

    @mcp.tool(
        name="refresh_library", description="Starts a library scan.", tags={"Library"}
    )
    def refresh_library_tool() -> Any:
        """Starts a library scan."""
        api = get_api_client()
        return api.refresh_library()

    @mcp.tool(
        name="post_added_series",
        description="Reports that new episodes of a series have been added by an external source.",
        tags={"Library"},
    )
    def post_added_series_tool(
        tvdb_id: Optional[str] = Field(default=None, description="The tvdbId.")
    ) -> Any:
        """Reports that new episodes of a series have been added by an external source."""
        api = get_api_client()
        return api.post_added_series(tvdb_id=tvdb_id)

    @mcp.tool(
        name="post_updated_series",
        description="Reports that new episodes of a series have been added by an external source.",
        tags={"Library"},
    )
    def post_updated_series_tool(
        tvdb_id: Optional[str] = Field(default=None, description="The tvdbId.")
    ) -> Any:
        """Reports that new episodes of a series have been added by an external source."""
        api = get_api_client()
        return api.post_updated_series(tvdb_id=tvdb_id)

    @mcp.tool(
        name="get_similar_movies", description="Gets similar items.", tags={"Library"}
    )
    def get_similar_movies_tool(
        item_id: str = Field(description="The item id."),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None, description="Exclude artist ids."
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
    ) -> Any:
        """Gets similar items."""
        api = get_api_client()
        return api.get_similar_movies(
            item_id=item_id,
            exclude_artist_ids=exclude_artist_ids,
            user_id=user_id,
            limit=limit,
            fields=fields,
        )

    @mcp.tool(
        name="get_similar_shows", description="Gets similar items.", tags={"Library"}
    )
    def get_similar_shows_tool(
        item_id: str = Field(description="The item id."),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None, description="Exclude artist ids."
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
    ) -> Any:
        """Gets similar items."""
        api = get_api_client()
        return api.get_similar_shows(
            item_id=item_id,
            exclude_artist_ids=exclude_artist_ids,
            user_id=user_id,
            limit=limit,
            fields=fields,
        )

    @mcp.tool(
        name="get_similar_trailers", description="Gets similar items.", tags={"Library"}
    )
    def get_similar_trailers_tool(
        item_id: str = Field(description="The item id."),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None, description="Exclude artist ids."
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
    ) -> Any:
        """Gets similar items."""
        api = get_api_client()
        return api.get_similar_trailers(
            item_id=item_id,
            exclude_artist_ids=exclude_artist_ids,
            user_id=user_id,
            limit=limit,
            fields=fields,
        )

    @mcp.tool(
        name="get_virtual_folders",
        description="Gets all virtual folders.",
        tags={"LibraryStructure"},
    )
    def get_virtual_folders_tool() -> Any:
        """Gets all virtual folders."""
        api = get_api_client()
        return api.get_virtual_folders()

    @mcp.tool(
        name="add_virtual_folder",
        description="Adds a virtual folder.",
        tags={"LibraryStructure"},
    )
    def add_virtual_folder_tool(
        name: Optional[str] = Field(
            default=None, description="The name of the virtual folder."
        ),
        collection_type: Optional[str] = Field(
            default=None, description="The type of the collection."
        ),
        paths: Optional[List[Any]] = Field(
            default=None, description="The paths of the virtual folder."
        ),
        refresh_library: Optional[bool] = Field(
            default=None, description="Whether to refresh the library."
        ),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Adds a virtual folder."""
        api = get_api_client()
        return api.add_virtual_folder(
            name=name,
            collection_type=collection_type,
            paths=paths,
            refresh_library=refresh_library,
            body=body,
        )

    @mcp.tool(
        name="remove_virtual_folder",
        description="Removes a virtual folder.",
        tags={"LibraryStructure"},
    )
    def remove_virtual_folder_tool(
        name: Optional[str] = Field(
            default=None, description="The name of the folder."
        ),
        refresh_library: Optional[bool] = Field(
            default=None, description="Whether to refresh the library."
        ),
    ) -> Any:
        """Removes a virtual folder."""
        api = get_api_client()
        return api.remove_virtual_folder(name=name, refresh_library=refresh_library)

    @mcp.tool(
        name="update_library_options",
        description="Update library options.",
        tags={"LibraryStructure"},
    )
    def update_library_options_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Update library options."""
        api = get_api_client()
        return api.update_library_options(body=body)

    @mcp.tool(
        name="rename_virtual_folder",
        description="Renames a virtual folder.",
        tags={"LibraryStructure"},
    )
    def rename_virtual_folder_tool(
        name: Optional[str] = Field(
            default=None, description="The name of the virtual folder."
        ),
        new_name: Optional[str] = Field(default=None, description="The new name."),
        refresh_library: Optional[bool] = Field(
            default=None, description="Whether to refresh the library."
        ),
    ) -> Any:
        """Renames a virtual folder."""
        api = get_api_client()
        return api.rename_virtual_folder(
            name=name, new_name=new_name, refresh_library=refresh_library
        )

    @mcp.tool(
        name="add_media_path",
        description="Add a media path to a library.",
        tags={"LibraryStructure"},
    )
    def add_media_path_tool(
        refresh_library: Optional[bool] = Field(
            default=None, description="Whether to refresh the library."
        ),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Add a media path to a library."""
        api = get_api_client()
        return api.add_media_path(refresh_library=refresh_library, body=body)

    @mcp.tool(
        name="remove_media_path",
        description="Remove a media path.",
        tags={"LibraryStructure"},
    )
    def remove_media_path_tool(
        name: Optional[str] = Field(
            default=None, description="The name of the library."
        ),
        path: Optional[str] = Field(default=None, description="The path to remove."),
        refresh_library: Optional[bool] = Field(
            default=None, description="Whether to refresh the library."
        ),
    ) -> Any:
        """Remove a media path."""
        api = get_api_client()
        return api.remove_media_path(
            name=name, path=path, refresh_library=refresh_library
        )

    @mcp.tool(
        name="update_media_path",
        description="Updates a media path.",
        tags={"LibraryStructure"},
    )
    def update_media_path_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Updates a media path."""
        api = get_api_client()
        return api.update_media_path(body=body)

    @mcp.tool(
        name="get_channel_mapping_options",
        description="Get channel mapping options.",
        tags={"LiveTv"},
    )
    def get_channel_mapping_options_tool(
        provider_id: Optional[str] = Field(default=None, description="Provider id.")
    ) -> Any:
        """Get channel mapping options."""
        api = get_api_client()
        return api.get_channel_mapping_options(provider_id=provider_id)

    @mcp.tool(
        name="set_channel_mapping", description="Set channel mappings.", tags={"LiveTv"}
    )
    def set_channel_mapping_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Set channel mappings."""
        api = get_api_client()
        return api.set_channel_mapping(body=body)

    @mcp.tool(
        name="get_live_tv_channels",
        description="Gets available live tv channels.",
        tags={"LiveTv"},
    )
    def get_live_tv_channels_tool(
        type: Optional[str] = Field(
            default=None, description="Optional. Filter by channel type."
        ),
        user_id: Optional[str] = Field(
            default=None, description="Optional. Filter by user and attach user data."
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional. Filter for movies."
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional. Filter for series."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional. Filter for news."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional. Filter for kids."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional. Filter for sports."
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by channels that are favorites, or not.",
        ),
        is_liked: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by channels that are liked, or not.",
        ),
        is_disliked: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by channels that are disliked, or not.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description='"Optional. The image types to include in the output.',
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None, description="Optional. Key to sort by."
        ),
        sort_order: Optional[str] = Field(
            default=None, description="Optional. Sort order."
        ),
        enable_favorite_sorting: Optional[bool] = Field(
            default=None,
            description="Optional. Incorporate favorite and like status into channel sorting.",
        ),
        add_current_program: Optional[bool] = Field(
            default=None,
            description="Optional. Adds current program info to each channel.",
        ),
    ) -> Any:
        """Gets available live tv channels."""
        api = get_api_client()
        return api.get_live_tv_channels(
            type=type,
            user_id=user_id,
            start_index=start_index,
            is_movie=is_movie,
            is_series=is_series,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            limit=limit,
            is_favorite=is_favorite,
            is_liked=is_liked,
            is_disliked=is_disliked,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            fields=fields,
            enable_user_data=enable_user_data,
            sort_by=sort_by,
            sort_order=sort_order,
            enable_favorite_sorting=enable_favorite_sorting,
            add_current_program=add_current_program,
        )

    @mcp.tool(
        name="get_channel", description="Gets a live tv channel.", tags={"LiveTv"}
    )
    def get_channel_tool(
        channel_id: str = Field(description="Channel id."),
        user_id: Optional[str] = Field(
            default=None, description="Optional. Attach user data."
        ),
    ) -> Any:
        """Gets a live tv channel."""
        api = get_api_client()
        return api.get_channel(channel_id=channel_id, user_id=user_id)

    @mcp.tool(name="get_guide_info", description="Get guide info.", tags={"LiveTv"})
    def get_guide_info_tool() -> Any:
        """Get guide info."""
        api = get_api_client()
        return api.get_guide_info()

    @mcp.tool(
        name="get_live_tv_info",
        description="Gets available live tv services.",
        tags={"LiveTv"},
    )
    def get_live_tv_info_tool() -> Any:
        """Gets available live tv services."""
        api = get_api_client()
        return api.get_live_tv_info()

    @mcp.tool(
        name="add_listing_provider",
        description="Adds a listings provider.",
        tags={"LiveTv"},
    )
    def add_listing_provider_tool(
        pw: Optional[str] = Field(default=None, description="Password."),
        validate_listings: Optional[bool] = Field(
            default=None, description="Validate listings."
        ),
        validate_login: Optional[bool] = Field(
            default=None, description="Validate login."
        ),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Adds a listings provider."""
        api = get_api_client()
        return api.add_listing_provider(
            pw=pw,
            validate_listings=validate_listings,
            validate_login=validate_login,
            body=body,
        )

    @mcp.tool(
        name="delete_listing_provider",
        description="Delete listing provider.",
        tags={"LiveTv"},
    )
    def delete_listing_provider_tool(
        id: Optional[str] = Field(default=None, description="Listing provider id.")
    ) -> Any:
        """Delete listing provider."""
        api = get_api_client()
        return api.delete_listing_provider(id=id)

    @mcp.tool(
        name="get_default_listing_provider",
        description="Gets default listings provider info.",
        tags={"LiveTv"},
    )
    def get_default_listing_provider_tool() -> Any:
        """Gets default listings provider info."""
        api = get_api_client()
        return api.get_default_listing_provider()

    @mcp.tool(
        name="get_lineups", description="Gets available lineups.", tags={"LiveTv"}
    )
    def get_lineups_tool(
        id: Optional[str] = Field(default=None, description="Provider id."),
        type: Optional[str] = Field(default=None, description="Provider type."),
        location: Optional[str] = Field(default=None, description="Location."),
        country: Optional[str] = Field(default=None, description="Country."),
    ) -> Any:
        """Gets available lineups."""
        api = get_api_client()
        return api.get_lineups(id=id, type=type, location=location, country=country)

    @mcp.tool(
        name="get_schedules_direct_countries",
        description="Gets available countries.",
        tags={"LiveTv"},
    )
    def get_schedules_direct_countries_tool() -> Any:
        """Gets available countries."""
        api = get_api_client()
        return api.get_schedules_direct_countries()

    @mcp.tool(
        name="get_live_recording_file",
        description="Gets a live tv recording stream.",
        tags={"LiveTv"},
    )
    def get_live_recording_file_tool(
        recording_id: str = Field(description="Recording id."),
    ) -> Any:
        """Gets a live tv recording stream."""
        api = get_api_client()
        return api.get_live_recording_file(recording_id=recording_id)

    @mcp.tool(
        name="get_live_stream_file",
        description="Gets a live tv channel stream.",
        tags={"LiveTv"},
    )
    def get_live_stream_file_tool(
        stream_id: str = Field(description="Stream id."),
        container: str = Field(description="Container type."),
    ) -> Any:
        """Gets a live tv channel stream."""
        api = get_api_client()
        return api.get_live_stream_file(stream_id=stream_id, container=container)

    @mcp.tool(
        name="get_live_tv_programs",
        description="Gets available live tv epgs.",
        tags={"LiveTv"},
    )
    def get_live_tv_programs_tool(
        channel_ids: Optional[List[Any]] = Field(
            default=None, description="The channels to return guide information for."
        ),
        user_id: Optional[str] = Field(
            default=None, description="Optional. Filter by user id."
        ),
        min_start_date: Optional[str] = Field(
            default=None, description="Optional. The minimum premiere start date."
        ),
        has_aired: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by programs that have completed airing, or not.",
        ),
        is_airing: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by programs that are currently airing, or not.",
        ),
        max_start_date: Optional[str] = Field(
            default=None, description="Optional. The maximum premiere start date."
        ),
        min_end_date: Optional[str] = Field(
            default=None, description="Optional. The minimum premiere end date."
        ),
        max_end_date: Optional[str] = Field(
            default=None, description="Optional. The maximum premiere end date."
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional. Filter for movies."
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional. Filter for series."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional. Filter for news."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional. Filter for kids."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional. Filter for sports."
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Name, StartDate.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending,Descending."
        ),
        genres: Optional[List[Any]] = Field(
            default=None, description="The genres to return guide information for."
        ),
        genre_ids: Optional[List[Any]] = Field(
            default=None, description="The genre ids to return guide information for."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        series_timer_id: Optional[str] = Field(
            default=None, description="Optional. Filter by series timer id."
        ),
        library_series_id: Optional[str] = Field(
            default=None, description="Optional. Filter by library series id."
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Retrieve total record count."
        ),
    ) -> Any:
        """Gets available live tv epgs."""
        api = get_api_client()
        return api.get_live_tv_programs(
            channel_ids=channel_ids,
            user_id=user_id,
            min_start_date=min_start_date,
            has_aired=has_aired,
            is_airing=is_airing,
            max_start_date=max_start_date,
            min_end_date=min_end_date,
            max_end_date=max_end_date,
            is_movie=is_movie,
            is_series=is_series,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            start_index=start_index,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            genres=genres,
            genre_ids=genre_ids,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
            series_timer_id=series_timer_id,
            library_series_id=library_series_id,
            fields=fields,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="get_programs", description="Gets available live tv epgs.", tags={"LiveTv"}
    )
    def get_programs_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Gets available live tv epgs."""
        api = get_api_client()
        return api.get_programs(body=body)

    @mcp.tool(
        name="get_program", description="Gets a live tv program.", tags={"LiveTv"}
    )
    def get_program_tool(
        program_id: str = Field(description="Program id."),
        user_id: Optional[str] = Field(
            default=None, description="Optional. Attach user data."
        ),
    ) -> Any:
        """Gets a live tv program."""
        api = get_api_client()
        return api.get_program(program_id=program_id, user_id=user_id)

    @mcp.tool(
        name="get_recommended_programs",
        description="Gets recommended live tv epgs.",
        tags={"LiveTv"},
    )
    def get_recommended_programs_tool(
        user_id: Optional[str] = Field(
            default=None, description="Optional. filter by user id."
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        is_airing: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by programs that are currently airing, or not.",
        ),
        has_aired: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by programs that have completed airing, or not.",
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional. Filter for series."
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional. Filter for movies."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional. Filter for news."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional. Filter for kids."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional. Filter for sports."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        genre_ids: Optional[List[Any]] = Field(
            default=None, description="The genres to return guide information for."
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. include user data."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Retrieve total record count."
        ),
    ) -> Any:
        """Gets recommended live tv epgs."""
        api = get_api_client()
        return api.get_recommended_programs(
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            is_airing=is_airing,
            has_aired=has_aired,
            is_series=is_series,
            is_movie=is_movie,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            genre_ids=genre_ids,
            fields=fields,
            enable_user_data=enable_user_data,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="get_recordings", description="Gets live tv recordings.", tags={"LiveTv"}
    )
    def get_recordings_tool(
        channel_id: Optional[str] = Field(
            default=None, description="Optional. Filter by channel id."
        ),
        user_id: Optional[str] = Field(
            default=None, description="Optional. Filter by user and attach user data."
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        status: Optional[str] = Field(
            default=None, description="Optional. Filter by recording status."
        ),
        is_in_progress: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by recordings that are in progress, or not.",
        ),
        series_timer_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by recordings belonging to a series timer.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional. Filter for movies."
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional. Filter for series."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional. Filter for kids."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional. Filter for sports."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional. Filter for news."
        ),
        is_library_item: Optional[bool] = Field(
            default=None, description="Optional. Filter for is library item."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Optional. Return total record count."
        ),
    ) -> Any:
        """Gets live tv recordings."""
        api = get_api_client()
        return api.get_recordings(
            channel_id=channel_id,
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            status=status,
            is_in_progress=is_in_progress,
            series_timer_id=series_timer_id,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            fields=fields,
            enable_user_data=enable_user_data,
            is_movie=is_movie,
            is_series=is_series,
            is_kids=is_kids,
            is_sports=is_sports,
            is_news=is_news,
            is_library_item=is_library_item,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="get_recording", description="Gets a live tv recording.", tags={"LiveTv"}
    )
    def get_recording_tool(
        recording_id: str = Field(description="Recording id."),
        user_id: Optional[str] = Field(
            default=None, description="Optional. Attach user data."
        ),
    ) -> Any:
        """Gets a live tv recording."""
        api = get_api_client()
        return api.get_recording(recording_id=recording_id, user_id=user_id)

    @mcp.tool(
        name="delete_recording",
        description="Deletes a live tv recording.",
        tags={"LiveTv"},
    )
    def delete_recording_tool(
        recording_id: str = Field(description="Recording id."),
    ) -> Any:
        """Deletes a live tv recording."""
        api = get_api_client()
        return api.delete_recording(recording_id=recording_id)

    @mcp.tool(
        name="get_recording_folders",
        description="Gets recording folders.",
        tags={"LiveTv"},
    )
    def get_recording_folders_tool(
        user_id: Optional[str] = Field(
            default=None, description="Optional. Filter by user and attach user data."
        )
    ) -> Any:
        """Gets recording folders."""
        api = get_api_client()
        return api.get_recording_folders(user_id=user_id)

    @mcp.tool(
        name="get_recording_groups",
        description="Gets live tv recording groups.",
        tags={"LiveTv"},
    )
    def get_recording_groups_tool(
        user_id: Optional[str] = Field(
            default=None, description="Optional. Filter by user and attach user data."
        )
    ) -> Any:
        """Gets live tv recording groups."""
        api = get_api_client()
        return api.get_recording_groups(user_id=user_id)

    @mcp.tool(
        name="get_recording_group", description="Get recording group.", tags={"LiveTv"}
    )
    def get_recording_group_tool(group_id: str = Field(description="Group id.")) -> Any:
        """Get recording group."""
        api = get_api_client()
        return api.get_recording_group(group_id=group_id)

    @mcp.tool(
        name="get_recordings_series",
        description="Gets live tv recording series.",
        tags={"LiveTv"},
    )
    def get_recordings_series_tool(
        channel_id: Optional[str] = Field(
            default=None, description="Optional. Filter by channel id."
        ),
        user_id: Optional[str] = Field(
            default=None, description="Optional. Filter by user and attach user data."
        ),
        group_id: Optional[str] = Field(
            default=None, description="Optional. Filter by recording group."
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        status: Optional[str] = Field(
            default=None, description="Optional. Filter by recording status."
        ),
        is_in_progress: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by recordings that are in progress, or not.",
        ),
        series_timer_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by recordings belonging to a series timer.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Optional. Return total record count."
        ),
    ) -> Any:
        """Gets live tv recording series."""
        api = get_api_client()
        return api.get_recordings_series(
            channel_id=channel_id,
            user_id=user_id,
            group_id=group_id,
            start_index=start_index,
            limit=limit,
            status=status,
            is_in_progress=is_in_progress,
            series_timer_id=series_timer_id,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            fields=fields,
            enable_user_data=enable_user_data,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="get_series_timers",
        description="Gets live tv series timers.",
        tags={"LiveTv"},
    )
    def get_series_timers_tool(
        sort_by: Optional[str] = Field(
            default=None, description="Optional. Sort by SortName or Priority."
        ),
        sort_order: Optional[str] = Field(
            default=None, description="Optional. Sort in Ascending or Descending order."
        ),
    ) -> Any:
        """Gets live tv series timers."""
        api = get_api_client()
        return api.get_series_timers(sort_by=sort_by, sort_order=sort_order)

    @mcp.tool(
        name="create_series_timer",
        description="Creates a live tv series timer.",
        tags={"LiveTv"},
    )
    def create_series_timer_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Creates a live tv series timer."""
        api = get_api_client()
        return api.create_series_timer(body=body)

    @mcp.tool(
        name="get_series_timer",
        description="Gets a live tv series timer.",
        tags={"LiveTv"},
    )
    def get_series_timer_tool(timer_id: str = Field(description="Timer id.")) -> Any:
        """Gets a live tv series timer."""
        api = get_api_client()
        return api.get_series_timer(timer_id=timer_id)

    @mcp.tool(
        name="cancel_series_timer",
        description="Cancels a live tv series timer.",
        tags={"LiveTv"},
    )
    def cancel_series_timer_tool(timer_id: str = Field(description="Timer id.")) -> Any:
        """Cancels a live tv series timer."""
        api = get_api_client()
        return api.cancel_series_timer(timer_id=timer_id)

    @mcp.tool(
        name="update_series_timer",
        description="Updates a live tv series timer.",
        tags={"LiveTv"},
    )
    def update_series_timer_tool(
        timer_id: str = Field(description="Timer id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates a live tv series timer."""
        api = get_api_client()
        return api.update_series_timer(timer_id=timer_id, body=body)

    @mcp.tool(
        name="get_timers", description="Gets the live tv timers.", tags={"LiveTv"}
    )
    def get_timers_tool(
        channel_id: Optional[str] = Field(
            default=None, description="Optional. Filter by channel id."
        ),
        series_timer_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by timers belonging to a series timer.",
        ),
        is_active: Optional[bool] = Field(
            default=None, description="Optional. Filter by timers that are active."
        ),
        is_scheduled: Optional[bool] = Field(
            default=None, description="Optional. Filter by timers that are scheduled."
        ),
    ) -> Any:
        """Gets the live tv timers."""
        api = get_api_client()
        return api.get_timers(
            channel_id=channel_id,
            series_timer_id=series_timer_id,
            is_active=is_active,
            is_scheduled=is_scheduled,
        )

    @mcp.tool(
        name="create_timer", description="Creates a live tv timer.", tags={"LiveTv"}
    )
    def create_timer_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Creates a live tv timer."""
        api = get_api_client()
        return api.create_timer(body=body)

    @mcp.tool(name="get_timer", description="Gets a timer.", tags={"LiveTv"})
    def get_timer_tool(timer_id: str = Field(description="Timer id.")) -> Any:
        """Gets a timer."""
        api = get_api_client()
        return api.get_timer(timer_id=timer_id)

    @mcp.tool(
        name="cancel_timer", description="Cancels a live tv timer.", tags={"LiveTv"}
    )
    def cancel_timer_tool(timer_id: str = Field(description="Timer id.")) -> Any:
        """Cancels a live tv timer."""
        api = get_api_client()
        return api.cancel_timer(timer_id=timer_id)

    @mcp.tool(
        name="update_timer", description="Updates a live tv timer.", tags={"LiveTv"}
    )
    def update_timer_tool(
        timer_id: str = Field(description="Timer id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates a live tv timer."""
        api = get_api_client()
        return api.update_timer(timer_id=timer_id, body=body)

    @mcp.tool(
        name="get_default_timer",
        description="Gets the default values for a new timer.",
        tags={"LiveTv"},
    )
    def get_default_timer_tool(
        program_id: Optional[str] = Field(
            default=None,
            description="Optional. To attach default values based on a program.",
        )
    ) -> Any:
        """Gets the default values for a new timer."""
        api = get_api_client()
        return api.get_default_timer(program_id=program_id)

    @mcp.tool(name="add_tuner_host", description="Adds a tuner host.", tags={"LiveTv"})
    def add_tuner_host_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Adds a tuner host."""
        api = get_api_client()
        return api.add_tuner_host(body=body)

    @mcp.tool(
        name="delete_tuner_host", description="Deletes a tuner host.", tags={"LiveTv"}
    )
    def delete_tuner_host_tool(
        id: Optional[str] = Field(default=None, description="Tuner host id.")
    ) -> Any:
        """Deletes a tuner host."""
        api = get_api_client()
        return api.delete_tuner_host(id=id)

    @mcp.tool(
        name="get_tuner_host_types",
        description="Get tuner host types.",
        tags={"LiveTv"},
    )
    def get_tuner_host_types_tool() -> Any:
        """Get tuner host types."""
        api = get_api_client()
        return api.get_tuner_host_types()

    @mcp.tool(name="reset_tuner", description="Resets a tv tuner.", tags={"LiveTv"})
    def reset_tuner_tool(tuner_id: str = Field(description="Tuner id.")) -> Any:
        """Resets a tv tuner."""
        api = get_api_client()
        return api.reset_tuner(tuner_id=tuner_id)

    @mcp.tool(name="discover_tuners", description="Discover tuners.", tags={"LiveTv"})
    def discover_tuners_tool(
        new_devices_only: Optional[bool] = Field(
            default=None, description="Only discover new tuners."
        )
    ) -> Any:
        """Discover tuners."""
        api = get_api_client()
        return api.discover_tuners(new_devices_only=new_devices_only)

    @mcp.tool(name="discvover_tuners", description="Discover tuners.", tags={"LiveTv"})
    def discvover_tuners_tool(
        new_devices_only: Optional[bool] = Field(
            default=None, description="Only discover new tuners."
        )
    ) -> Any:
        """Discover tuners."""
        api = get_api_client()
        return api.discvover_tuners(new_devices_only=new_devices_only)

    @mcp.tool(
        name="get_countries", description="Gets known countries.", tags={"Localization"}
    )
    def get_countries_tool() -> Any:
        """Gets known countries."""
        api = get_api_client()
        return api.get_countries()

    @mcp.tool(
        name="get_cultures", description="Gets known cultures.", tags={"Localization"}
    )
    def get_cultures_tool() -> Any:
        """Gets known cultures."""
        api = get_api_client()
        return api.get_cultures()

    @mcp.tool(
        name="get_localization_options",
        description="Gets localization options.",
        tags={"Localization"},
    )
    def get_localization_options_tool() -> Any:
        """Gets localization options."""
        api = get_api_client()
        return api.get_localization_options()

    @mcp.tool(
        name="get_parental_ratings",
        description="Gets known parental ratings.",
        tags={"Localization"},
    )
    def get_parental_ratings_tool() -> Any:
        """Gets known parental ratings."""
        api = get_api_client()
        return api.get_parental_ratings()

    @mcp.tool(name="get_lyrics", description="Gets an item's lyrics.", tags={"Lyrics"})
    def get_lyrics_tool(item_id: str = Field(description="Item id.")) -> Any:
        """Gets an item's lyrics."""
        api = get_api_client()
        return api.get_lyrics(item_id=item_id)

    @mcp.tool(
        name="upload_lyrics",
        description="Upload an external lyric file.",
        tags={"Lyrics"},
    )
    def upload_lyrics_tool(
        item_id: str = Field(description="The item the lyric belongs to."),
        file_name: Optional[str] = Field(
            default=None, description="Name of the file being uploaded."
        ),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Upload an external lyric file."""
        api = get_api_client()
        return api.upload_lyrics(item_id=item_id, file_name=file_name, body=body)

    @mcp.tool(
        name="delete_lyrics",
        description="Deletes an external lyric file.",
        tags={"Lyrics"},
    )
    def delete_lyrics_tool(item_id: str = Field(description="The item id.")) -> Any:
        """Deletes an external lyric file."""
        api = get_api_client()
        return api.delete_lyrics(item_id=item_id)

    @mcp.tool(
        name="search_remote_lyrics",
        description="Search remote lyrics.",
        tags={"Lyrics"},
    )
    def search_remote_lyrics_tool(
        item_id: str = Field(description="The item id."),
    ) -> Any:
        """Search remote lyrics."""
        api = get_api_client()
        return api.search_remote_lyrics(item_id=item_id)

    @mcp.tool(
        name="download_remote_lyrics",
        description="Downloads a remote lyric.",
        tags={"Lyrics"},
    )
    def download_remote_lyrics_tool(
        item_id: str = Field(description="The item id."),
        lyric_id: str = Field(description="The lyric id."),
    ) -> Any:
        """Downloads a remote lyric."""
        api = get_api_client()
        return api.download_remote_lyrics(item_id=item_id, lyric_id=lyric_id)

    @mcp.tool(
        name="get_remote_lyrics", description="Gets the remote lyrics.", tags={"Lyrics"}
    )
    def get_remote_lyrics_tool(
        lyric_id: str = Field(description="The remote provider item id."),
    ) -> Any:
        """Gets the remote lyrics."""
        api = get_api_client()
        return api.get_remote_lyrics(lyric_id=lyric_id)

    @mcp.tool(
        name="get_playback_info",
        description="Gets live playback media info for an item.",
        tags={"MediaInfo"},
    )
    def get_playback_info_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
    ) -> Any:
        """Gets live playback media info for an item."""
        api = get_api_client()
        return api.get_playback_info(item_id=item_id, user_id=user_id)

    @mcp.tool(
        name="get_posted_playback_info",
        description="Gets live playback media info for an item.",
        tags={"MediaInfo"},
    )
    def get_posted_playback_info_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
        max_streaming_bitrate: Optional[int] = Field(
            default=None, description="The maximum streaming bitrate."
        ),
        start_time_ticks: Optional[int] = Field(
            default=None, description="The start time in ticks."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None, description="The audio stream index."
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None, description="The subtitle stream index."
        ),
        max_audio_channels: Optional[int] = Field(
            default=None, description="The maximum number of audio channels."
        ),
        media_source_id: Optional[str] = Field(
            default=None, description="The media source id."
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The livestream id."
        ),
        auto_open_live_stream: Optional[bool] = Field(
            default=None, description="Whether to auto open the livestream."
        ),
        enable_direct_play: Optional[bool] = Field(
            default=None, description="Whether to enable direct play. Default: true."
        ),
        enable_direct_stream: Optional[bool] = Field(
            default=None, description="Whether to enable direct stream. Default: true."
        ),
        enable_transcoding: Optional[bool] = Field(
            default=None, description="Whether to enable transcoding. Default: true."
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether to allow to copy the video stream. Default: true.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether to allow to copy the audio stream. Default: true.",
        ),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Gets live playback media info for an item."""
        api = get_api_client()
        return api.get_posted_playback_info(
            item_id=item_id,
            user_id=user_id,
            max_streaming_bitrate=max_streaming_bitrate,
            start_time_ticks=start_time_ticks,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            max_audio_channels=max_audio_channels,
            media_source_id=media_source_id,
            live_stream_id=live_stream_id,
            auto_open_live_stream=auto_open_live_stream,
            enable_direct_play=enable_direct_play,
            enable_direct_stream=enable_direct_stream,
            enable_transcoding=enable_transcoding,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            body=body,
        )

    @mcp.tool(
        name="close_live_stream",
        description="Closes a media source.",
        tags={"MediaInfo"},
    )
    def close_live_stream_tool(
        live_stream_id: Optional[str] = Field(
            default=None, description="The livestream id."
        )
    ) -> Any:
        """Closes a media source."""
        api = get_api_client()
        return api.close_live_stream(live_stream_id=live_stream_id)

    @mcp.tool(
        name="open_live_stream", description="Opens a media source.", tags={"MediaInfo"}
    )
    def open_live_stream_tool(
        open_token: Optional[str] = Field(default=None, description="The open token."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        max_streaming_bitrate: Optional[int] = Field(
            default=None, description="The maximum streaming bitrate."
        ),
        start_time_ticks: Optional[int] = Field(
            default=None, description="The start time in ticks."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None, description="The audio stream index."
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None, description="The subtitle stream index."
        ),
        max_audio_channels: Optional[int] = Field(
            default=None, description="The maximum number of audio channels."
        ),
        item_id: Optional[str] = Field(default=None, description="The item id."),
        enable_direct_play: Optional[bool] = Field(
            default=None, description="Whether to enable direct play. Default: true."
        ),
        enable_direct_stream: Optional[bool] = Field(
            default=None, description="Whether to enable direct stream. Default: true."
        ),
        always_burn_in_subtitle_when_transcoding: Optional[bool] = Field(
            default=None, description="Always burn-in subtitle when transcoding."
        ),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Opens a media source."""
        api = get_api_client()
        return api.open_live_stream(
            open_token=open_token,
            user_id=user_id,
            play_session_id=play_session_id,
            max_streaming_bitrate=max_streaming_bitrate,
            start_time_ticks=start_time_ticks,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            max_audio_channels=max_audio_channels,
            item_id=item_id,
            enable_direct_play=enable_direct_play,
            enable_direct_stream=enable_direct_stream,
            always_burn_in_subtitle_when_transcoding=always_burn_in_subtitle_when_transcoding,
            body=body,
        )

    @mcp.tool(
        name="get_bitrate_test_bytes",
        description="Tests the network with a request with the size of the bitrate.",
        tags={"MediaInfo"},
    )
    def get_bitrate_test_bytes_tool(
        size: Optional[int] = Field(
            default=None, description="The bitrate. Defaults to 102400."
        )
    ) -> Any:
        """Tests the network with a request with the size of the bitrate."""
        api = get_api_client()
        return api.get_bitrate_test_bytes(size=size)

    @mcp.tool(
        name="get_item_segments",
        description="Gets all media segments based on an itemId.",
        tags={"MediaSegments"},
    )
    def get_item_segments_tool(
        item_id: str = Field(description="The ItemId."),
        include_segment_types: Optional[List[Any]] = Field(
            default=None, description="Optional filter of requested segment types."
        ),
    ) -> Any:
        """Gets all media segments based on an itemId."""
        api = get_api_client()
        return api.get_item_segments(
            item_id=item_id, include_segment_types=include_segment_types
        )

    @mcp.tool(
        name="get_movie_recommendations",
        description="Gets movie recommendations.",
        tags={"Movies"},
    )
    def get_movie_recommendations_tool(
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None, description="Optional. The fields to return."
        ),
        category_limit: Optional[int] = Field(
            default=None, description="The max number of categories to return."
        ),
        item_limit: Optional[int] = Field(
            default=None, description="The max number of items to return per category."
        ),
    ) -> Any:
        """Gets movie recommendations."""
        api = get_api_client()
        return api.get_movie_recommendations(
            user_id=user_id,
            parent_id=parent_id,
            fields=fields,
            category_limit=category_limit,
            item_limit=item_limit,
        )

    @mcp.tool(
        name="get_music_genres",
        description="Gets all music genres from a given item, folder, or the entire library.",
        tags={"MusicGenres"},
    )
    def get_music_genres_tool(
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="The search term."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered out based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered in based on item type. This allows multiple, comma delimited.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not.",
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        user_id: Optional[str] = Field(default=None, description="User id."),
        name_starts_with_or_greater: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally or greater than a given input string.",
        ),
        name_starts_with: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally than a given input string.",
        ),
        name_less_than: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is equally or lesser than a given input string.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending,Descending."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Optional. Include total record count."
        ),
    ) -> Any:
        """Gets all music genres from a given item, folder, or the entire library."""
        api = get_api_client()
        return api.get_music_genres(
            start_index=start_index,
            limit=limit,
            search_term=search_term,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            is_favorite=is_favorite,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            user_id=user_id,
            name_starts_with_or_greater=name_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
            sort_by=sort_by,
            sort_order=sort_order,
            enable_images=enable_images,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="get_music_genre",
        description="Gets a music genre, by name.",
        tags={"MusicGenres"},
    )
    def get_music_genre_tool(
        genre_name: str = Field(description="The genre name."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
    ) -> Any:
        """Gets a music genre, by name."""
        api = get_api_client()
        return api.get_music_genre(genre_name=genre_name, user_id=user_id)

    @mcp.tool(
        name="get_packages", description="Gets available packages.", tags={"Package"}
    )
    def get_packages_tool() -> Any:
        """Gets available packages."""
        api = get_api_client()
        return api.get_packages()

    @mcp.tool(
        name="get_package_info",
        description="Gets a package by name or assembly GUID.",
        tags={"Package"},
    )
    def get_package_info_tool(
        name: str = Field(description="The name of the package."),
        assembly_guid: Optional[str] = Field(
            default=None, description="The GUID of the associated assembly."
        ),
    ) -> Any:
        """Gets a package by name or assembly GUID."""
        api = get_api_client()
        return api.get_package_info(name=name, assembly_guid=assembly_guid)

    @mcp.tool(
        name="install_package", description="Installs a package.", tags={"Package"}
    )
    def install_package_tool(
        name: str = Field(description="Package name."),
        assembly_guid: Optional[str] = Field(
            default=None, description="GUID of the associated assembly."
        ),
        version: Optional[str] = Field(
            default=None, description="Optional version. Defaults to latest version."
        ),
        repository_url: Optional[str] = Field(
            default=None,
            description="Optional. Specify the repository to install from.",
        ),
    ) -> Any:
        """Installs a package."""
        api = get_api_client()
        return api.install_package(
            name=name,
            assembly_guid=assembly_guid,
            version=version,
            repository_url=repository_url,
        )

    @mcp.tool(
        name="cancel_package_installation",
        description="Cancels a package installation.",
        tags={"Package"},
    )
    def cancel_package_installation_tool(
        package_id: str = Field(description="Installation Id."),
    ) -> Any:
        """Cancels a package installation."""
        api = get_api_client()
        return api.cancel_package_installation(package_id=package_id)

    @mcp.tool(
        name="get_repositories",
        description="Gets all package repositories.",
        tags={"Package"},
    )
    def get_repositories_tool() -> Any:
        """Gets all package repositories."""
        api = get_api_client()
        return api.get_repositories()

    @mcp.tool(
        name="set_repositories",
        description="Sets the enabled and existing package repositories.",
        tags={"Package"},
    )
    def set_repositories_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Sets the enabled and existing package repositories."""
        api = get_api_client()
        return api.set_repositories(body=body)

    @mcp.tool(name="get_persons", description="Gets all persons.", tags={"Persons"})
    def get_persons_tool(
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="The search term."
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        filters: Optional[List[Any]] = Field(
            default=None, description="Optional. Specify additional filters to apply."
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not. userId is required.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional, include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        exclude_person_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified results will be filtered to exclude those containing the specified PersonType. Allows multiple, comma-delimited.",
        ),
        person_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified results will be filtered to include only those containing the specified PersonType. Allows multiple, comma-delimited.",
        ),
        appears_in_item_id: Optional[str] = Field(
            default=None,
            description="Optional. If specified, person results will be filtered on items related to said persons.",
        ),
        user_id: Optional[str] = Field(default=None, description="User id."),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
    ) -> Any:
        """Gets all persons."""
        api = get_api_client()
        return api.get_persons(
            limit=limit,
            search_term=search_term,
            fields=fields,
            filters=filters,
            is_favorite=is_favorite,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            exclude_person_types=exclude_person_types,
            person_types=person_types,
            appears_in_item_id=appears_in_item_id,
            user_id=user_id,
            enable_images=enable_images,
        )

    @mcp.tool(name="get_person", description="Get person by name.", tags={"Persons"})
    def get_person_tool(
        name: str = Field(description="Person name."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
    ) -> Any:
        """Get person by name."""
        api = get_api_client()
        return api.get_person(name=name, user_id=user_id)

    @mcp.tool(
        name="create_playlist",
        description="Creates a new playlist.",
        tags={"Playlists"},
    )
    def create_playlist_tool(
        name: Optional[str] = Field(default=None, description="The playlist name."),
        ids: Optional[List[Any]] = Field(default=None, description="The item ids."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
        media_type: Optional[str] = Field(default=None, description="The media type."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Creates a new playlist."""
        api = get_api_client()
        return api.create_playlist(
            name=name, ids=ids, user_id=user_id, media_type=media_type, body=body
        )

    @mcp.tool(
        name="update_playlist", description="Updates a playlist.", tags={"Playlists"}
    )
    def update_playlist_tool(
        playlist_id: str = Field(description="The playlist id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates a playlist."""
        api = get_api_client()
        return api.update_playlist(playlist_id=playlist_id, body=body)

    @mcp.tool(name="get_playlist", description="Get a playlist.", tags={"Playlists"})
    def get_playlist_tool(
        playlist_id: str = Field(description="The playlist id."),
    ) -> Any:
        """Get a playlist."""
        api = get_api_client()
        return api.get_playlist(playlist_id=playlist_id)

    @mcp.tool(
        name="add_item_to_playlist",
        description="Adds items to a playlist.",
        tags={"Playlists"},
    )
    def add_item_to_playlist_tool(
        playlist_id: str = Field(description="The playlist id."),
        ids: Optional[List[Any]] = Field(
            default=None, description="Item id, comma delimited."
        ),
        user_id: Optional[str] = Field(default=None, description="The userId."),
    ) -> Any:
        """Adds items to a playlist."""
        api = get_api_client()
        return api.add_item_to_playlist(
            playlist_id=playlist_id, ids=ids, user_id=user_id
        )

    @mcp.tool(
        name="remove_item_from_playlist",
        description="Removes items from a playlist.",
        tags={"Playlists"},
    )
    def remove_item_from_playlist_tool(
        playlist_id: str = Field(description="The playlist id."),
        entry_ids: Optional[List[Any]] = Field(
            default=None, description="The item ids, comma delimited."
        ),
    ) -> Any:
        """Removes items from a playlist."""
        api = get_api_client()
        return api.remove_item_from_playlist(
            playlist_id=playlist_id, entry_ids=entry_ids
        )

    @mcp.tool(
        name="get_playlist_items",
        description="Gets the original items of a playlist.",
        tags={"Playlists"},
    )
    def get_playlist_items_tool(
        playlist_id: str = Field(description="The playlist id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
    ) -> Any:
        """Gets the original items of a playlist."""
        api = get_api_client()
        return api.get_playlist_items(
            playlist_id=playlist_id,
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            fields=fields,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
        )

    @mcp.tool(
        name="move_item", description="Moves a playlist item.", tags={"Playlists"}
    )
    def move_item_tool(
        playlist_id: str = Field(description="The playlist id."),
        item_id: str = Field(description="The item id."),
        new_index: int = Field(description="The new index."),
    ) -> Any:
        """Moves a playlist item."""
        api = get_api_client()
        return api.move_item(
            playlist_id=playlist_id, item_id=item_id, new_index=new_index
        )

    @mcp.tool(
        name="get_playlist_users",
        description="Get a playlist's users.",
        tags={"Playlists"},
    )
    def get_playlist_users_tool(
        playlist_id: str = Field(description="The playlist id."),
    ) -> Any:
        """Get a playlist's users."""
        api = get_api_client()
        return api.get_playlist_users(playlist_id=playlist_id)

    @mcp.tool(
        name="get_playlist_user", description="Get a playlist user.", tags={"Playlists"}
    )
    def get_playlist_user_tool(
        playlist_id: str = Field(description="The playlist id."),
        user_id: str = Field(description="The user id."),
    ) -> Any:
        """Get a playlist user."""
        api = get_api_client()
        return api.get_playlist_user(playlist_id=playlist_id, user_id=user_id)

    @mcp.tool(
        name="update_playlist_user",
        description="Modify a user of a playlist's users.",
        tags={"Playlists"},
    )
    def update_playlist_user_tool(
        playlist_id: str = Field(description="The playlist id."),
        user_id: str = Field(description="The user id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Modify a user of a playlist's users."""
        api = get_api_client()
        return api.update_playlist_user(
            playlist_id=playlist_id, user_id=user_id, body=body
        )

    @mcp.tool(
        name="remove_user_from_playlist",
        description="Remove a user from a playlist's users.",
        tags={"Playlists"},
    )
    def remove_user_from_playlist_tool(
        playlist_id: str = Field(description="The playlist id."),
        user_id: str = Field(description="The user id."),
    ) -> Any:
        """Remove a user from a playlist's users."""
        api = get_api_client()
        return api.remove_user_from_playlist(playlist_id=playlist_id, user_id=user_id)

    @mcp.tool(
        name="on_playback_start",
        description="Reports that a session has begun playing an item.",
        tags={"Playstate"},
    )
    def on_playback_start_tool(
        item_id: str = Field(description="Item id."),
        media_source_id: Optional[str] = Field(
            default=None, description="The id of the MediaSource."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None, description="The audio stream index."
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None, description="The subtitle stream index."
        ),
        play_method: Optional[str] = Field(
            default=None, description="The play method."
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        can_seek: Optional[bool] = Field(
            default=None, description="Indicates if the client can seek."
        ),
    ) -> Any:
        """Reports that a session has begun playing an item."""
        api = get_api_client()
        return api.on_playback_start(
            item_id=item_id,
            media_source_id=media_source_id,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            play_method=play_method,
            live_stream_id=live_stream_id,
            play_session_id=play_session_id,
            can_seek=can_seek,
        )

    @mcp.tool(
        name="on_playback_stopped",
        description="Reports that a session has stopped playing an item.",
        tags={"Playstate"},
    )
    def on_playback_stopped_tool(
        item_id: str = Field(description="Item id."),
        media_source_id: Optional[str] = Field(
            default=None, description="The id of the MediaSource."
        ),
        next_media_type: Optional[str] = Field(
            default=None, description="The next media type that will play."
        ),
        position_ticks: Optional[int] = Field(
            default=None,
            description="Optional. The position, in ticks, where playback stopped. 1 tick = 10000 ms.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
    ) -> Any:
        """Reports that a session has stopped playing an item."""
        api = get_api_client()
        return api.on_playback_stopped(
            item_id=item_id,
            media_source_id=media_source_id,
            next_media_type=next_media_type,
            position_ticks=position_ticks,
            live_stream_id=live_stream_id,
            play_session_id=play_session_id,
        )

    @mcp.tool(
        name="on_playback_progress",
        description="Reports a session's playback progress.",
        tags={"Playstate"},
    )
    def on_playback_progress_tool(
        item_id: str = Field(description="Item id."),
        media_source_id: Optional[str] = Field(
            default=None, description="The id of the MediaSource."
        ),
        position_ticks: Optional[int] = Field(
            default=None,
            description="Optional. The current position, in ticks. 1 tick = 10000 ms.",
        ),
        audio_stream_index: Optional[int] = Field(
            default=None, description="The audio stream index."
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None, description="The subtitle stream index."
        ),
        volume_level: Optional[int] = Field(
            default=None, description="Scale of 0-100."
        ),
        play_method: Optional[str] = Field(
            default=None, description="The play method."
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        repeat_mode: Optional[str] = Field(
            default=None, description="The repeat mode."
        ),
        is_paused: Optional[bool] = Field(
            default=None, description="Indicates if the player is paused."
        ),
        is_muted: Optional[bool] = Field(
            default=None, description="Indicates if the player is muted."
        ),
    ) -> Any:
        """Reports a session's playback progress."""
        api = get_api_client()
        return api.on_playback_progress(
            item_id=item_id,
            media_source_id=media_source_id,
            position_ticks=position_ticks,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            volume_level=volume_level,
            play_method=play_method,
            live_stream_id=live_stream_id,
            play_session_id=play_session_id,
            repeat_mode=repeat_mode,
            is_paused=is_paused,
            is_muted=is_muted,
        )

    @mcp.tool(
        name="report_playback_start",
        description="Reports playback has started within a session.",
        tags={"Playstate"},
    )
    def report_playback_start_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Reports playback has started within a session."""
        api = get_api_client()
        return api.report_playback_start(body=body)

    @mcp.tool(
        name="ping_playback_session",
        description="Pings a playback session.",
        tags={"Playstate"},
    )
    def ping_playback_session_tool(
        play_session_id: Optional[str] = Field(
            default=None, description="Playback session id."
        )
    ) -> Any:
        """Pings a playback session."""
        api = get_api_client()
        return api.ping_playback_session(play_session_id=play_session_id)

    @mcp.tool(
        name="report_playback_progress",
        description="Reports playback progress within a session.",
        tags={"Playstate"},
    )
    def report_playback_progress_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Reports playback progress within a session."""
        api = get_api_client()
        return api.report_playback_progress(body=body)

    @mcp.tool(
        name="report_playback_stopped",
        description="Reports playback has stopped within a session.",
        tags={"Playstate"},
    )
    def report_playback_stopped_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Reports playback has stopped within a session."""
        api = get_api_client()
        return api.report_playback_stopped(body=body)

    @mcp.tool(
        name="mark_played_item",
        description="Marks an item as played for user.",
        tags={"Playstate"},
    )
    def mark_played_item_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
        date_played: Optional[str] = Field(
            default=None, description="Optional. The date the item was played."
        ),
    ) -> Any:
        """Marks an item as played for user."""
        api = get_api_client()
        return api.mark_played_item(
            user_id=user_id, item_id=item_id, date_played=date_played
        )

    @mcp.tool(
        name="mark_unplayed_item",
        description="Marks an item as unplayed for user.",
        tags={"Playstate"},
    )
    def mark_unplayed_item_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Marks an item as unplayed for user."""
        api = get_api_client()
        return api.mark_unplayed_item(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="get_plugins",
        description="Gets a list of currently installed plugins.",
        tags={"Plugins"},
    )
    def get_plugins_tool() -> Any:
        """Gets a list of currently installed plugins."""
        api = get_api_client()
        return api.get_plugins()

    @mcp.tool(
        name="uninstall_plugin", description="Uninstalls a plugin.", tags={"Plugins"}
    )
    def uninstall_plugin_tool(plugin_id: str = Field(description="Plugin id.")) -> Any:
        """Uninstalls a plugin."""
        api = get_api_client()
        return api.uninstall_plugin(plugin_id=plugin_id)

    @mcp.tool(
        name="uninstall_plugin_by_version",
        description="Uninstalls a plugin by version.",
        tags={"Plugins"},
    )
    def uninstall_plugin_by_version_tool(
        plugin_id: str = Field(description="Plugin id."),
        version: str = Field(description="Plugin version."),
    ) -> Any:
        """Uninstalls a plugin by version."""
        api = get_api_client()
        return api.uninstall_plugin_by_version(plugin_id=plugin_id, version=version)

    @mcp.tool(name="disable_plugin", description="Disable a plugin.", tags={"Plugins"})
    def disable_plugin_tool(
        plugin_id: str = Field(description="Plugin id."),
        version: str = Field(description="Plugin version."),
    ) -> Any:
        """Disable a plugin."""
        api = get_api_client()
        return api.disable_plugin(plugin_id=plugin_id, version=version)

    @mcp.tool(
        name="enable_plugin", description="Enables a disabled plugin.", tags={"Plugins"}
    )
    def enable_plugin_tool(
        plugin_id: str = Field(description="Plugin id."),
        version: str = Field(description="Plugin version."),
    ) -> Any:
        """Enables a disabled plugin."""
        api = get_api_client()
        return api.enable_plugin(plugin_id=plugin_id, version=version)

    @mcp.tool(
        name="get_plugin_image", description="Gets a plugin's image.", tags={"Plugins"}
    )
    def get_plugin_image_tool(
        plugin_id: str = Field(description="Plugin id."),
        version: str = Field(description="Plugin version."),
    ) -> Any:
        """Gets a plugin's image."""
        api = get_api_client()
        return api.get_plugin_image(plugin_id=plugin_id, version=version)

    @mcp.tool(
        name="get_plugin_configuration",
        description="Gets plugin configuration.",
        tags={"Plugins"},
    )
    def get_plugin_configuration_tool(
        plugin_id: str = Field(description="Plugin id."),
    ) -> Any:
        """Gets plugin configuration."""
        api = get_api_client()
        return api.get_plugin_configuration(plugin_id=plugin_id)

    @mcp.tool(
        name="update_plugin_configuration",
        description="Updates plugin configuration.",
        tags={"Plugins"},
    )
    def update_plugin_configuration_tool(
        plugin_id: str = Field(description="Plugin id."),
    ) -> Any:
        """Updates plugin configuration."""
        api = get_api_client()
        return api.update_plugin_configuration(plugin_id=plugin_id)

    @mcp.tool(
        name="get_plugin_manifest",
        description="Gets a plugin's manifest.",
        tags={"Plugins"},
    )
    def get_plugin_manifest_tool(
        plugin_id: str = Field(description="Plugin id."),
    ) -> Any:
        """Gets a plugin's manifest."""
        api = get_api_client()
        return api.get_plugin_manifest(plugin_id=plugin_id)

    @mcp.tool(
        name="authorize_quick_connect",
        description="Authorizes a pending quick connect request.",
        tags={"QuickConnect"},
    )
    def authorize_quick_connect_tool(
        code: Optional[str] = Field(
            default=None, description="Quick connect code to authorize."
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="The user the authorize. Access to the requested user is required.",
        ),
    ) -> Any:
        """Authorizes a pending quick connect request."""
        api = get_api_client()
        return api.authorize_quick_connect(code=code, user_id=user_id)

    @mcp.tool(
        name="get_quick_connect_state",
        description="Attempts to retrieve authentication information.",
        tags={"QuickConnect"},
    )
    def get_quick_connect_state_tool(
        secret: Optional[str] = Field(
            default=None,
            description="Secret previously returned from the Initiate endpoint.",
        )
    ) -> Any:
        """Attempts to retrieve authentication information."""
        api = get_api_client()
        return api.get_quick_connect_state(secret=secret)

    @mcp.tool(
        name="get_quick_connect_enabled",
        description="Gets the current quick connect state.",
        tags={"QuickConnect"},
    )
    def get_quick_connect_enabled_tool() -> Any:
        """Gets the current quick connect state."""
        api = get_api_client()
        return api.get_quick_connect_enabled()

    @mcp.tool(
        name="initiate_quick_connect",
        description="Initiate a new quick connect request.",
        tags={"QuickConnect"},
    )
    def initiate_quick_connect_tool() -> Any:
        """Initiate a new quick connect request."""
        api = get_api_client()
        return api.initiate_quick_connect()

    @mcp.tool(
        name="get_remote_images",
        description="Gets available remote images for an item.",
        tags={"RemoteImage"},
    )
    def get_remote_images_tool(
        item_id: str = Field(description="Item Id."),
        type: Optional[str] = Field(default=None, description="The image type."),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        provider_name: Optional[str] = Field(
            default=None, description="Optional. The image provider to use."
        ),
        include_all_languages: Optional[bool] = Field(
            default=None, description="Optional. Include all languages."
        ),
    ) -> Any:
        """Gets available remote images for an item."""
        api = get_api_client()
        return api.get_remote_images(
            item_id=item_id,
            type=type,
            start_index=start_index,
            limit=limit,
            provider_name=provider_name,
            include_all_languages=include_all_languages,
        )

    @mcp.tool(
        name="download_remote_image",
        description="Downloads a remote image for an item.",
        tags={"RemoteImage"},
    )
    def download_remote_image_tool(
        item_id: str = Field(description="Item Id."),
        type: Optional[str] = Field(default=None, description="The image type."),
        image_url: Optional[str] = Field(default=None, description="The image url."),
    ) -> Any:
        """Downloads a remote image for an item."""
        api = get_api_client()
        return api.download_remote_image(
            item_id=item_id, type=type, image_url=image_url
        )

    @mcp.tool(
        name="get_remote_image_providers",
        description="Gets available remote image providers for an item.",
        tags={"RemoteImage"},
    )
    def get_remote_image_providers_tool(
        item_id: str = Field(description="Item Id."),
    ) -> Any:
        """Gets available remote image providers for an item."""
        api = get_api_client()
        return api.get_remote_image_providers(item_id=item_id)

    @mcp.tool(name="get_tasks", description="Get tasks.", tags={"ScheduledTasks"})
    def get_tasks_tool(
        is_hidden: Optional[bool] = Field(
            default=None, description="Optional filter tasks that are hidden, or not."
        ),
        is_enabled: Optional[bool] = Field(
            default=None, description="Optional filter tasks that are enabled, or not."
        ),
    ) -> Any:
        """Get tasks."""
        api = get_api_client()
        return api.get_tasks(is_hidden=is_hidden, is_enabled=is_enabled)

    @mcp.tool(name="get_task", description="Get task by id.", tags={"ScheduledTasks"})
    def get_task_tool(task_id: str = Field(description="Task Id.")) -> Any:
        """Get task by id."""
        api = get_api_client()
        return api.get_task(task_id=task_id)

    @mcp.tool(
        name="update_task",
        description="Update specified task triggers.",
        tags={"ScheduledTasks"},
    )
    def update_task_tool(
        task_id: str = Field(description="Task Id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Update specified task triggers."""
        api = get_api_client()
        return api.update_task(task_id=task_id, body=body)

    @mcp.tool(
        name="start_task", description="Start specified task.", tags={"ScheduledTasks"}
    )
    def start_task_tool(task_id: str = Field(description="Task Id.")) -> Any:
        """Start specified task."""
        api = get_api_client()
        return api.start_task(task_id=task_id)

    @mcp.tool(
        name="stop_task", description="Stop specified task.", tags={"ScheduledTasks"}
    )
    def stop_task_tool(task_id: str = Field(description="Task Id.")) -> Any:
        """Stop specified task."""
        api = get_api_client()
        return api.stop_task(task_id=task_id)

    @mcp.tool(
        name="get_search_hints",
        description="Gets the search hint result.",
        tags={"Search"},
    )
    def get_search_hints_tool(
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Supply a user id to search within a user's library or omit to search all.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="The search term to filter on."
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="If specified, only results with the specified item types are returned. This allows multiple, comma delimited.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="If specified, results with these item types are filtered out. This allows multiple, comma delimited.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="If specified, only results with the specified media types are returned. This allows multiple, comma delimited.",
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="If specified, only children of the parent are returned.",
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional filter for movies."
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional filter for series."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional filter for news."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional filter for kids."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional filter for sports."
        ),
        include_people: Optional[bool] = Field(
            default=None, description="Optional filter whether to include people."
        ),
        include_media: Optional[bool] = Field(
            default=None, description="Optional filter whether to include media."
        ),
        include_genres: Optional[bool] = Field(
            default=None, description="Optional filter whether to include genres."
        ),
        include_studios: Optional[bool] = Field(
            default=None, description="Optional filter whether to include studios."
        ),
        include_artists: Optional[bool] = Field(
            default=None, description="Optional filter whether to include artists."
        ),
    ) -> Any:
        """Gets the search hint result."""
        api = get_api_client()
        return api.get_search_hints(
            start_index=start_index,
            limit=limit,
            user_id=user_id,
            search_term=search_term,
            include_item_types=include_item_types,
            exclude_item_types=exclude_item_types,
            media_types=media_types,
            parent_id=parent_id,
            is_movie=is_movie,
            is_series=is_series,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            include_people=include_people,
            include_media=include_media,
            include_genres=include_genres,
            include_studios=include_studios,
            include_artists=include_artists,
        )

    @mcp.tool(
        name="get_password_reset_providers",
        description="Get all password reset providers.",
        tags={"Session"},
    )
    def get_password_reset_providers_tool() -> Any:
        """Get all password reset providers."""
        api = get_api_client()
        return api.get_password_reset_providers()

    @mcp.tool(
        name="get_auth_providers",
        description="Get all auth providers.",
        tags={"Session"},
    )
    def get_auth_providers_tool() -> Any:
        """Get all auth providers."""
        api = get_api_client()
        return api.get_auth_providers()

    @mcp.tool(
        name="get_sessions", description="Gets a list of sessions.", tags={"Session"}
    )
    def get_sessions_tool(
        controllable_by_user_id: Optional[str] = Field(
            default=None,
            description="Filter by sessions that a given user is allowed to remote control.",
        ),
        device_id: Optional[str] = Field(
            default=None, description="Filter by device Id."
        ),
        active_within_seconds: Optional[int] = Field(
            default=None,
            description="Optional. Filter by sessions that were active in the last n seconds.",
        ),
    ) -> Any:
        """Gets a list of sessions."""
        api = get_api_client()
        return api.get_sessions(
            controllable_by_user_id=controllable_by_user_id,
            device_id=device_id,
            active_within_seconds=active_within_seconds,
        )

    @mcp.tool(
        name="send_full_general_command",
        description="Issues a full general command to a client.",
        tags={"Session"},
    )
    def send_full_general_command_tool(
        session_id: str = Field(description="The session id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Issues a full general command to a client."""
        api = get_api_client()
        return api.send_full_general_command(session_id=session_id, body=body)

    @mcp.tool(
        name="send_general_command",
        description="Issues a general command to a client.",
        tags={"Session"},
    )
    def send_general_command_tool(
        session_id: str = Field(description="The session id."),
        command: str = Field(description="The command to send."),
    ) -> Any:
        """Issues a general command to a client."""
        api = get_api_client()
        return api.send_general_command(session_id=session_id, command=command)

    @mcp.tool(
        name="send_message_command",
        description="Issues a command to a client to display a message to the user.",
        tags={"Session"},
    )
    def send_message_command_tool(
        session_id: str = Field(description="The session id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Issues a command to a client to display a message to the user."""
        api = get_api_client()
        return api.send_message_command(session_id=session_id, body=body)

    @mcp.tool(
        name="play",
        description="Instructs a session to play an item.",
        tags={"Session"},
    )
    def play_tool(
        session_id: str = Field(description="The session id."),
        play_command: Optional[str] = Field(
            default=None,
            description="The type of play command to issue (PlayNow, PlayNext, PlayLast). Clients who have not yet implemented play next and play last may play now.",
        ),
        item_ids: Optional[List[Any]] = Field(
            default=None, description="The ids of the items to play, comma delimited."
        ),
        start_position_ticks: Optional[int] = Field(
            default=None, description="The starting position of the first item."
        ),
        media_source_id: Optional[str] = Field(
            default=None, description="Optional. The media source id."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None, description="Optional. The index of the audio stream to play."
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to play.",
        ),
        start_index: Optional[int] = Field(
            default=None, description="Optional. The start index."
        ),
    ) -> Any:
        """Instructs a session to play an item."""
        api = get_api_client()
        return api.play(
            session_id=session_id,
            play_command=play_command,
            item_ids=item_ids,
            start_position_ticks=start_position_ticks,
            media_source_id=media_source_id,
            audio_stream_index=audio_stream_index,
            subtitle_stream_index=subtitle_stream_index,
            start_index=start_index,
        )

    @mcp.tool(
        name="send_playstate_command",
        description="Issues a playstate command to a client.",
        tags={"Session"},
    )
    def send_playstate_command_tool(
        session_id: str = Field(description="The session id."),
        command: str = Field(
            description="The MediaBrowser.Model.Session.PlaystateCommand."
        ),
        seek_position_ticks: Optional[int] = Field(
            default=None, description="The optional position ticks."
        ),
        controlling_user_id: Optional[str] = Field(
            default=None, description="The optional controlling user id."
        ),
    ) -> Any:
        """Issues a playstate command to a client."""
        api = get_api_client()
        return api.send_playstate_command(
            session_id=session_id,
            command=command,
            seek_position_ticks=seek_position_ticks,
            controlling_user_id=controlling_user_id,
        )

    @mcp.tool(
        name="send_system_command",
        description="Issues a system command to a client.",
        tags={"Session"},
    )
    def send_system_command_tool(
        session_id: str = Field(description="The session id."),
        command: str = Field(description="The command to send."),
    ) -> Any:
        """Issues a system command to a client."""
        api = get_api_client()
        return api.send_system_command(session_id=session_id, command=command)

    @mcp.tool(
        name="add_user_to_session",
        description="Adds an additional user to a session.",
        tags={"Session"},
    )
    def add_user_to_session_tool(
        session_id: str = Field(description="The session id."),
        user_id: str = Field(description="The user id."),
    ) -> Any:
        """Adds an additional user to a session."""
        api = get_api_client()
        return api.add_user_to_session(session_id=session_id, user_id=user_id)

    @mcp.tool(
        name="remove_user_from_session",
        description="Removes an additional user from a session.",
        tags={"Session"},
    )
    def remove_user_from_session_tool(
        session_id: str = Field(description="The session id."),
        user_id: str = Field(description="The user id."),
    ) -> Any:
        """Removes an additional user from a session."""
        api = get_api_client()
        return api.remove_user_from_session(session_id=session_id, user_id=user_id)

    @mcp.tool(
        name="display_content",
        description="Instructs a session to browse to an item or view.",
        tags={"Session"},
    )
    def display_content_tool(
        session_id: str = Field(description="The session Id."),
        item_type: Optional[str] = Field(
            default=None, description="The type of item to browse to."
        ),
        item_id: Optional[str] = Field(default=None, description="The Id of the item."),
        item_name: Optional[str] = Field(
            default=None, description="The name of the item."
        ),
    ) -> Any:
        """Instructs a session to browse to an item or view."""
        api = get_api_client()
        return api.display_content(
            session_id=session_id,
            item_type=item_type,
            item_id=item_id,
            item_name=item_name,
        )

    @mcp.tool(
        name="post_capabilities",
        description="Updates capabilities for a device.",
        tags={"Session"},
    )
    def post_capabilities_tool(
        id: Optional[str] = Field(default=None, description="The session id."),
        playable_media_types: Optional[List[Any]] = Field(
            default=None,
            description="A list of playable media types, comma delimited. Audio, Video, Book, Photo.",
        ),
        supported_commands: Optional[List[Any]] = Field(
            default=None,
            description="A list of supported remote control commands, comma delimited.",
        ),
        supports_media_control: Optional[bool] = Field(
            default=None,
            description="Determines whether media can be played remotely..",
        ),
        supports_persistent_identifier: Optional[bool] = Field(
            default=None,
            description="Determines whether the device supports a unique identifier.",
        ),
    ) -> Any:
        """Updates capabilities for a device."""
        api = get_api_client()
        return api.post_capabilities(
            id=id,
            playable_media_types=playable_media_types,
            supported_commands=supported_commands,
            supports_media_control=supports_media_control,
            supports_persistent_identifier=supports_persistent_identifier,
        )

    @mcp.tool(
        name="post_full_capabilities",
        description="Updates capabilities for a device.",
        tags={"Session"},
    )
    def post_full_capabilities_tool(
        id: Optional[str] = Field(default=None, description="The session id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates capabilities for a device."""
        api = get_api_client()
        return api.post_full_capabilities(id=id, body=body)

    @mcp.tool(
        name="report_session_ended",
        description="Reports that a session has ended.",
        tags={"Session"},
    )
    def report_session_ended_tool() -> Any:
        """Reports that a session has ended."""
        api = get_api_client()
        return api.report_session_ended()

    @mcp.tool(
        name="report_viewing",
        description="Reports that a session is viewing an item.",
        tags={"Session"},
    )
    def report_viewing_tool(
        session_id: Optional[str] = Field(default=None, description="The session id."),
        item_id: Optional[str] = Field(default=None, description="The item id."),
    ) -> Any:
        """Reports that a session is viewing an item."""
        api = get_api_client()
        return api.report_viewing(session_id=session_id, item_id=item_id)

    @mcp.tool(
        name="complete_wizard",
        description="Completes the startup wizard.",
        tags={"Startup"},
    )
    def complete_wizard_tool() -> Any:
        """Completes the startup wizard."""
        api = get_api_client()
        return api.complete_wizard()

    @mcp.tool(
        name="get_startup_configuration",
        description="Gets the initial startup wizard configuration.",
        tags={"Startup"},
    )
    def get_startup_configuration_tool() -> Any:
        """Gets the initial startup wizard configuration."""
        api = get_api_client()
        return api.get_startup_configuration()

    @mcp.tool(
        name="update_initial_configuration",
        description="Sets the initial startup wizard configuration.",
        tags={"Startup"},
    )
    def update_initial_configuration_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Sets the initial startup wizard configuration."""
        api = get_api_client()
        return api.update_initial_configuration(body=body)

    @mcp.tool(
        name="get_first_user_2", description="Gets the first user.", tags={"Startup"}
    )
    def get_first_user_2_tool() -> Any:
        """Gets the first user."""
        api = get_api_client()
        return api.get_first_user_2()

    @mcp.tool(
        name="set_remote_access",
        description="Sets remote access and UPnP.",
        tags={"Startup"},
    )
    def set_remote_access_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Sets remote access and UPnP."""
        api = get_api_client()
        return api.set_remote_access(body=body)

    @mcp.tool(
        name="get_first_user", description="Gets the first user.", tags={"Startup"}
    )
    def get_first_user_tool() -> Any:
        """Gets the first user."""
        api = get_api_client()
        return api.get_first_user()

    @mcp.tool(
        name="update_startup_user",
        description="Sets the user name and password.",
        tags={"Startup"},
    )
    def update_startup_user_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Sets the user name and password."""
        api = get_api_client()
        return api.update_startup_user(body=body)

    @mcp.tool(
        name="get_studios",
        description="Gets all studios from a given item, folder, or the entire library.",
        tags={"Studios"},
    )
    def get_studios_tool(
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="Optional. Search term."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered out based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional, include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        user_id: Optional[str] = Field(default=None, description="User id."),
        name_starts_with_or_greater: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally or greater than a given input string.",
        ),
        name_starts_with: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally than a given input string.",
        ),
        name_less_than: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is equally or lesser than a given input string.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Total record count."
        ),
    ) -> Any:
        """Gets all studios from a given item, folder, or the entire library."""
        api = get_api_client()
        return api.get_studios(
            start_index=start_index,
            limit=limit,
            search_term=search_term,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            is_favorite=is_favorite,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            user_id=user_id,
            name_starts_with_or_greater=name_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
            enable_images=enable_images,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(name="get_studio", description="Gets a studio by name.", tags={"Studios"})
    def get_studio_tool(
        name: str = Field(description="Studio name."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
    ) -> Any:
        """Gets a studio by name."""
        api = get_api_client()
        return api.get_studio(name=name, user_id=user_id)

    @mcp.tool(
        name="get_fallback_font_list",
        description="Gets a list of available fallback font files.",
        tags={"Subtitle"},
    )
    def get_fallback_font_list_tool() -> Any:
        """Gets a list of available fallback font files."""
        api = get_api_client()
        return api.get_fallback_font_list()

    @mcp.tool(
        name="get_fallback_font",
        description="Gets a fallback font file.",
        tags={"Subtitle"},
    )
    def get_fallback_font_tool(
        name: str = Field(description="The name of the fallback font file to get."),
    ) -> Any:
        """Gets a fallback font file."""
        api = get_api_client()
        return api.get_fallback_font(name=name)

    @mcp.tool(
        name="search_remote_subtitles",
        description="Search remote subtitles.",
        tags={"Subtitle"},
    )
    def search_remote_subtitles_tool(
        item_id: str = Field(description="The item id."),
        language: str = Field(description="The language of the subtitles."),
        is_perfect_match: Optional[bool] = Field(
            default=None,
            description="Optional. Only show subtitles which are a perfect match.",
        ),
    ) -> Any:
        """Search remote subtitles."""
        api = get_api_client()
        return api.search_remote_subtitles(
            item_id=item_id, language=language, is_perfect_match=is_perfect_match
        )

    @mcp.tool(
        name="download_remote_subtitles",
        description="Downloads a remote subtitle.",
        tags={"Subtitle"},
    )
    def download_remote_subtitles_tool(
        item_id: str = Field(description="The item id."),
        subtitle_id: str = Field(description="The subtitle id."),
    ) -> Any:
        """Downloads a remote subtitle."""
        api = get_api_client()
        return api.download_remote_subtitles(item_id=item_id, subtitle_id=subtitle_id)

    @mcp.tool(
        name="get_remote_subtitles",
        description="Gets the remote subtitles.",
        tags={"Subtitle"},
    )
    def get_remote_subtitles_tool(
        subtitle_id: str = Field(description="The item id."),
    ) -> Any:
        """Gets the remote subtitles."""
        api = get_api_client()
        return api.get_remote_subtitles(subtitle_id=subtitle_id)

    @mcp.tool(
        name="get_subtitle_playlist",
        description="Gets an HLS subtitle playlist.",
        tags={"Subtitle"},
    )
    def get_subtitle_playlist_tool(
        item_id: str = Field(description="The item id."),
        index: int = Field(description="The subtitle stream index."),
        media_source_id: str = Field(description="The media source id."),
        segment_length: Optional[int] = Field(
            default=None, description="The subtitle segment length."
        ),
    ) -> Any:
        """Gets an HLS subtitle playlist."""
        api = get_api_client()
        return api.get_subtitle_playlist(
            item_id=item_id,
            index=index,
            media_source_id=media_source_id,
            segment_length=segment_length,
        )

    @mcp.tool(
        name="upload_subtitle",
        description="Upload an external subtitle file.",
        tags={"Subtitle"},
    )
    def upload_subtitle_tool(
        item_id: str = Field(description="The item the subtitle belongs to."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Upload an external subtitle file."""
        api = get_api_client()
        return api.upload_subtitle(item_id=item_id, body=body)

    @mcp.tool(
        name="delete_subtitle",
        description="Deletes an external subtitle file.",
        tags={"Subtitle"},
    )
    def delete_subtitle_tool(
        item_id: str = Field(description="The item id."),
        index: int = Field(description="The index of the subtitle file."),
    ) -> Any:
        """Deletes an external subtitle file."""
        api = get_api_client()
        return api.delete_subtitle(item_id=item_id, index=index)

    @mcp.tool(
        name="get_subtitle_with_ticks",
        description="Gets subtitles in a specified format.",
        tags={"Subtitle"},
    )
    def get_subtitle_with_ticks_tool(
        route_item_id: str = Field(description="The (route) item id."),
        route_media_source_id: str = Field(description="The (route) media source id."),
        route_index: int = Field(description="The (route) subtitle stream index."),
        route_start_position_ticks: int = Field(
            description="The (route) start position of the subtitle in ticks."
        ),
        route_format: str = Field(
            description="The (route) format of the returned subtitle."
        ),
        item_id: Optional[str] = Field(default=None, description="The item id."),
        media_source_id: Optional[str] = Field(
            default=None, description="The media source id."
        ),
        index: Optional[int] = Field(
            default=None, description="The subtitle stream index."
        ),
        start_position_ticks: Optional[int] = Field(
            default=None, description="The start position of the subtitle in ticks."
        ),
        format: Optional[str] = Field(
            default=None, description="The format of the returned subtitle."
        ),
        end_position_ticks: Optional[int] = Field(
            default=None,
            description="Optional. The end position of the subtitle in ticks.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None, description="Optional. Whether to copy the timestamps."
        ),
        add_vtt_time_map: Optional[bool] = Field(
            default=None, description="Optional. Whether to add a VTT time map."
        ),
    ) -> Any:
        """Gets subtitles in a specified format."""
        api = get_api_client()
        return api.get_subtitle_with_ticks(
            route_item_id=route_item_id,
            route_media_source_id=route_media_source_id,
            route_index=route_index,
            route_start_position_ticks=route_start_position_ticks,
            route_format=route_format,
            item_id=item_id,
            media_source_id=media_source_id,
            index=index,
            start_position_ticks=start_position_ticks,
            format=format,
            end_position_ticks=end_position_ticks,
            copy_timestamps=copy_timestamps,
            add_vtt_time_map=add_vtt_time_map,
        )

    @mcp.tool(
        name="get_subtitle",
        description="Gets subtitles in a specified format.",
        tags={"Subtitle"},
    )
    def get_subtitle_tool(
        route_item_id: str = Field(description="The (route) item id."),
        route_media_source_id: str = Field(description="The (route) media source id."),
        route_index: int = Field(description="The (route) subtitle stream index."),
        route_format: str = Field(
            description="The (route) format of the returned subtitle."
        ),
        item_id: Optional[str] = Field(default=None, description="The item id."),
        media_source_id: Optional[str] = Field(
            default=None, description="The media source id."
        ),
        index: Optional[int] = Field(
            default=None, description="The subtitle stream index."
        ),
        format: Optional[str] = Field(
            default=None, description="The format of the returned subtitle."
        ),
        end_position_ticks: Optional[int] = Field(
            default=None,
            description="Optional. The end position of the subtitle in ticks.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None, description="Optional. Whether to copy the timestamps."
        ),
        add_vtt_time_map: Optional[bool] = Field(
            default=None, description="Optional. Whether to add a VTT time map."
        ),
        start_position_ticks: Optional[int] = Field(
            default=None, description="The start position of the subtitle in ticks."
        ),
    ) -> Any:
        """Gets subtitles in a specified format."""
        api = get_api_client()
        return api.get_subtitle(
            route_item_id=route_item_id,
            route_media_source_id=route_media_source_id,
            route_index=route_index,
            route_format=route_format,
            item_id=item_id,
            media_source_id=media_source_id,
            index=index,
            format=format,
            end_position_ticks=end_position_ticks,
            copy_timestamps=copy_timestamps,
            add_vtt_time_map=add_vtt_time_map,
            start_position_ticks=start_position_ticks,
        )

    @mcp.tool(
        name="get_suggestions", description="Gets suggestions.", tags={"Suggestions"}
    )
    def get_suggestions_tool(
        user_id: Optional[str] = Field(default=None, description="The user id."),
        media_type: Optional[List[Any]] = Field(
            default=None, description="The media types."
        ),
        type: Optional[List[Any]] = Field(default=None, description="The type."),
        start_index: Optional[int] = Field(
            default=None, description="Optional. The start index."
        ),
        limit: Optional[int] = Field(default=None, description="Optional. The limit."),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Whether to enable the total record count."
        ),
    ) -> Any:
        """Gets suggestions."""
        api = get_api_client()
        return api.get_suggestions(
            user_id=user_id,
            media_type=media_type,
            type=type,
            start_index=start_index,
            limit=limit,
            enable_total_record_count=enable_total_record_count,
        )

    @mcp.tool(
        name="sync_play_get_group",
        description="Gets a SyncPlay group by id.",
        tags={"SyncPlay"},
    )
    def sync_play_get_group_tool(
        id: str = Field(description="The id of the group."),
    ) -> Any:
        """Gets a SyncPlay group by id."""
        api = get_api_client()
        return api.sync_play_get_group(id=id)

    @mcp.tool(
        name="sync_play_buffering",
        description="Notify SyncPlay group that member is buffering.",
        tags={"SyncPlay"},
    )
    def sync_play_buffering_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Notify SyncPlay group that member is buffering."""
        api = get_api_client()
        return api.sync_play_buffering(body=body)

    @mcp.tool(
        name="sync_play_join_group",
        description="Join an existing SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_join_group_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Join an existing SyncPlay group."""
        api = get_api_client()
        return api.sync_play_join_group(body=body)

    @mcp.tool(
        name="sync_play_leave_group",
        description="Leave the joined SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_leave_group_tool() -> Any:
        """Leave the joined SyncPlay group."""
        api = get_api_client()
        return api.sync_play_leave_group()

    @mcp.tool(
        name="sync_play_get_groups",
        description="Gets all SyncPlay groups.",
        tags={"SyncPlay"},
    )
    def sync_play_get_groups_tool() -> Any:
        """Gets all SyncPlay groups."""
        api = get_api_client()
        return api.sync_play_get_groups()

    @mcp.tool(
        name="sync_play_move_playlist_item",
        description="Request to move an item in the playlist in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_move_playlist_item_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request to move an item in the playlist in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_move_playlist_item(body=body)

    @mcp.tool(
        name="sync_play_create_group",
        description="Create a new SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_create_group_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Create a new SyncPlay group."""
        api = get_api_client()
        return api.sync_play_create_group(body=body)

    @mcp.tool(
        name="sync_play_next_item",
        description="Request next item in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_next_item_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request next item in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_next_item(body=body)

    @mcp.tool(
        name="sync_play_pause",
        description="Request pause in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_pause_tool() -> Any:
        """Request pause in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_pause()

    @mcp.tool(
        name="sync_play_ping", description="Update session ping.", tags={"SyncPlay"}
    )
    def sync_play_ping_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Update session ping."""
        api = get_api_client()
        return api.sync_play_ping(body=body)

    @mcp.tool(
        name="sync_play_previous_item",
        description="Request previous item in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_previous_item_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request previous item in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_previous_item(body=body)

    @mcp.tool(
        name="sync_play_queue",
        description="Request to queue items to the playlist of a SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_queue_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request to queue items to the playlist of a SyncPlay group."""
        api = get_api_client()
        return api.sync_play_queue(body=body)

    @mcp.tool(
        name="sync_play_ready",
        description="Notify SyncPlay group that member is ready for playback.",
        tags={"SyncPlay"},
    )
    def sync_play_ready_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Notify SyncPlay group that member is ready for playback."""
        api = get_api_client()
        return api.sync_play_ready(body=body)

    @mcp.tool(
        name="sync_play_remove_from_playlist",
        description="Request to remove items from the playlist in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_remove_from_playlist_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request to remove items from the playlist in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_remove_from_playlist(body=body)

    @mcp.tool(
        name="sync_play_seek",
        description="Request seek in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_seek_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request seek in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_seek(body=body)

    @mcp.tool(
        name="sync_play_set_ignore_wait",
        description="Request SyncPlay group to ignore member during group-wait.",
        tags={"SyncPlay"},
    )
    def sync_play_set_ignore_wait_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request SyncPlay group to ignore member during group-wait."""
        api = get_api_client()
        return api.sync_play_set_ignore_wait(body=body)

    @mcp.tool(
        name="sync_play_set_new_queue",
        description="Request to set new playlist in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_set_new_queue_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request to set new playlist in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_set_new_queue(body=body)

    @mcp.tool(
        name="sync_play_set_playlist_item",
        description="Request to change playlist item in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_set_playlist_item_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request to change playlist item in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_set_playlist_item(body=body)

    @mcp.tool(
        name="sync_play_set_repeat_mode",
        description="Request to set repeat mode in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_set_repeat_mode_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request to set repeat mode in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_set_repeat_mode(body=body)

    @mcp.tool(
        name="sync_play_set_shuffle_mode",
        description="Request to set shuffle mode in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_set_shuffle_mode_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Request to set shuffle mode in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_set_shuffle_mode(body=body)

    @mcp.tool(
        name="sync_play_stop",
        description="Request stop in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_stop_tool() -> Any:
        """Request stop in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_stop()

    @mcp.tool(
        name="sync_play_unpause",
        description="Request unpause in SyncPlay group.",
        tags={"SyncPlay"},
    )
    def sync_play_unpause_tool() -> Any:
        """Request unpause in SyncPlay group."""
        api = get_api_client()
        return api.sync_play_unpause()

    @mcp.tool(
        name="get_endpoint_info",
        description="Gets information about the request endpoint.",
        tags={"System"},
    )
    def get_endpoint_info_tool() -> Any:
        """Gets information about the request endpoint."""
        api = get_api_client()
        return api.get_endpoint_info()

    @mcp.tool(
        name="get_system_info",
        description="Gets information about the server.",
        tags={"System"},
    )
    def get_system_info_tool() -> Any:
        """Gets information about the server."""
        api = get_api_client()
        return api.get_system_info()

    @mcp.tool(
        name="get_public_system_info",
        description="Gets public information about the server.",
        tags={"System"},
    )
    def get_public_system_info_tool() -> Any:
        """Gets public information about the server."""
        api = get_api_client()
        return api.get_public_system_info()

    @mcp.tool(
        name="get_system_storage",
        description="Gets information about the server.",
        tags={"System"},
    )
    def get_system_storage_tool() -> Any:
        """Gets information about the server."""
        api = get_api_client()
        return api.get_system_storage()

    @mcp.tool(
        name="get_server_logs",
        description="Gets a list of available server log files.",
        tags={"System"},
    )
    def get_server_logs_tool() -> Any:
        """Gets a list of available server log files."""
        api = get_api_client()
        return api.get_server_logs()

    @mcp.tool(name="get_log_file", description="Gets a log file.", tags={"System"})
    def get_log_file_tool(
        name: Optional[str] = Field(
            default=None, description="The name of the log file to get."
        )
    ) -> Any:
        """Gets a log file."""
        api = get_api_client()
        return api.get_log_file(name=name)

    @mcp.tool(name="get_ping_system", description="Pings the system.", tags={"System"})
    def get_ping_system_tool() -> Any:
        """Pings the system."""
        api = get_api_client()
        return api.get_ping_system()

    @mcp.tool(name="post_ping_system", description="Pings the system.", tags={"System"})
    def post_ping_system_tool() -> Any:
        """Pings the system."""
        api = get_api_client()
        return api.post_ping_system()

    @mcp.tool(
        name="restart_application",
        description="Restarts the application.",
        tags={"System"},
    )
    def restart_application_tool() -> Any:
        """Restarts the application."""
        api = get_api_client()
        return api.restart_application()

    @mcp.tool(
        name="shutdown_application",
        description="Shuts down the application.",
        tags={"System"},
    )
    def shutdown_application_tool() -> Any:
        """Shuts down the application."""
        api = get_api_client()
        return api.shutdown_application()

    @mcp.tool(
        name="get_utc_time", description="Gets the current UTC time.", tags={"TimeSync"}
    )
    def get_utc_time_tool() -> Any:
        """Gets the current UTC time."""
        api = get_api_client()
        return api.get_utc_time()

    @mcp.tool(
        name="tmdb_client_configuration",
        description="Gets the TMDb image configuration options.",
        tags={"Tmdb"},
    )
    def tmdb_client_configuration_tool() -> Any:
        """Gets the TMDb image configuration options."""
        api = get_api_client()
        return api.tmdb_client_configuration()

    @mcp.tool(
        name="get_trailers",
        description="Finds movies and trailers similar to a given trailer.",
        tags={"Trailers"},
    )
    def get_trailers_tool(
        user_id: Optional[str] = Field(
            default=None,
            description="The user id supplied as query parameter; this is required when not using an API key.",
        ),
        max_official_rating: Optional[str] = Field(
            default=None,
            description="Optional filter by maximum official rating (PG, PG-13, TV-MA, etc).",
        ),
        has_theme_song: Optional[bool] = Field(
            default=None, description="Optional filter by items with theme songs."
        ),
        has_theme_video: Optional[bool] = Field(
            default=None, description="Optional filter by items with theme videos."
        ),
        has_subtitles: Optional[bool] = Field(
            default=None, description="Optional filter by items with subtitles."
        ),
        has_special_feature: Optional[bool] = Field(
            default=None, description="Optional filter by items with special features."
        ),
        has_trailer: Optional[bool] = Field(
            default=None, description="Optional filter by items with trailers."
        ),
        adjacent_to: Optional[str] = Field(
            default=None,
            description="Optional. Return items that are siblings of a supplied item.",
        ),
        parent_index_number: Optional[int] = Field(
            default=None, description="Optional filter by parent index number."
        ),
        has_parental_rating: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have or do not have a parental rating.",
        ),
        is_hd: Optional[bool] = Field(
            default=None, description="Optional filter by items that are HD or not."
        ),
        is4_k: Optional[bool] = Field(
            default=None, description="Optional filter by items that are 4K or not."
        ),
        location_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on LocationType. This allows multiple, comma delimited.",
        ),
        exclude_location_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on the LocationType. This allows multiple, comma delimited.",
        ),
        is_missing: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are missing episodes or not.",
        ),
        is_unaired: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are unaired episodes or not.",
        ),
        min_community_rating: Optional[float] = Field(
            default=None, description="Optional filter by minimum community rating."
        ),
        min_critic_rating: Optional[float] = Field(
            default=None, description="Optional filter by minimum critic rating."
        ),
        min_premiere_date: Optional[str] = Field(
            default=None,
            description="Optional. The minimum premiere date. Format = ISO.",
        ),
        min_date_last_saved: Optional[str] = Field(
            default=None,
            description="Optional. The minimum last saved date. Format = ISO.",
        ),
        min_date_last_saved_for_user: Optional[str] = Field(
            default=None,
            description="Optional. The minimum last saved date for the current user. Format = ISO.",
        ),
        max_premiere_date: Optional[str] = Field(
            default=None,
            description="Optional. The maximum premiere date. Format = ISO.",
        ),
        has_overview: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have an overview or not.",
        ),
        has_imdb_id: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have an IMDb id or not.",
        ),
        has_tmdb_id: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have a TMDb id or not.",
        ),
        has_tvdb_id: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have a TVDb id or not.",
        ),
        is_movie: Optional[bool] = Field(
            default=None, description="Optional filter for live tv movies."
        ),
        is_series: Optional[bool] = Field(
            default=None, description="Optional filter for live tv series."
        ),
        is_news: Optional[bool] = Field(
            default=None, description="Optional filter for live tv news."
        ),
        is_kids: Optional[bool] = Field(
            default=None, description="Optional filter for live tv kids."
        ),
        is_sports: Optional[bool] = Field(
            default=None, description="Optional filter for live tv sports."
        ),
        exclude_item_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered by excluding item ids. This allows multiple, comma delimited.",
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        recursive: Optional[bool] = Field(
            default=None,
            description="When searching within folders, this determines whether or not the search will be recursive. true/false.",
        ),
        search_term: Optional[str] = Field(
            default=None, description="Optional. Filter based on a search term."
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending, Descending."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        filters: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional filters to apply. This allows multiple, comma delimited. Options: IsFolder, IsNotFolder, IsUnplayed, IsPlayed, IsFavorite, IsResumable, Likes, Dislikes.",
        ),
        is_favorite: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are marked as favorite, or not.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by MediaType. Allows multiple, comma delimited.",
        ),
        image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on those containing image types. This allows multiple, comma delimited.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
        is_played: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that are played, or not.",
        ),
        genres: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre. This allows multiple, pipe delimited.",
        ),
        official_ratings: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on OfficialRating. This allows multiple, pipe delimited.",
        ),
        tags: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on tag. This allows multiple, pipe delimited.",
        ),
        years: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on production year. This allows multiple, comma delimited.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional, include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        person: Optional[str] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person.",
        ),
        person_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified person id.",
        ),
        person_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, along with Person, results will be filtered to include only those containing the specified person and PersonType. Allows multiple, comma-delimited.",
        ),
        studios: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio. This allows multiple, pipe delimited.",
        ),
        artists: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on artists. This allows multiple, pipe delimited.",
        ),
        exclude_artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on artist id. This allows multiple, pipe delimited.",
        ),
        artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified artist id.",
        ),
        album_artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified album artist id.",
        ),
        contributing_artist_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered to include only those containing the specified contributing artist id.",
        ),
        albums: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on album. This allows multiple, pipe delimited.",
        ),
        album_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on album id. This allows multiple, pipe delimited.",
        ),
        ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specific items are needed, specify a list of item id's to retrieve. This allows multiple, comma delimited.",
        ),
        video_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by VideoType (videofile, dvd, bluray, iso). Allows multiple, comma delimited.",
        ),
        min_official_rating: Optional[str] = Field(
            default=None,
            description="Optional filter by minimum official rating (PG, PG-13, TV-MA, etc).",
        ),
        is_locked: Optional[bool] = Field(
            default=None, description="Optional filter by items that are locked."
        ),
        is_place_holder: Optional[bool] = Field(
            default=None, description="Optional filter by items that are placeholders."
        ),
        has_official_rating: Optional[bool] = Field(
            default=None,
            description="Optional filter by items that have official ratings.",
        ),
        collapse_box_set_items: Optional[bool] = Field(
            default=None,
            description="Whether or not to hide items behind their boxsets.",
        ),
        min_width: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the minimum width of the item.",
        ),
        min_height: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the minimum height of the item.",
        ),
        max_width: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the maximum width of the item.",
        ),
        max_height: Optional[int] = Field(
            default=None,
            description="Optional. Filter by the maximum height of the item.",
        ),
        is3_d: Optional[bool] = Field(
            default=None, description="Optional filter by items that are 3D, or not."
        ),
        series_status: Optional[List[Any]] = Field(
            default=None,
            description="Optional filter by Series Status. Allows multiple, comma delimited.",
        ),
        name_starts_with_or_greater: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally or greater than a given input string.",
        ),
        name_starts_with: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is sorted equally than a given input string.",
        ),
        name_less_than: Optional[str] = Field(
            default=None,
            description="Optional filter by items whose name is equally or lesser than a given input string.",
        ),
        studio_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on studio id. This allows multiple, pipe delimited.",
        ),
        genre_ids: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on genre id. This allows multiple, pipe delimited.",
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None, description="Optional. Enable the total record count."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
    ) -> Any:
        """Finds movies and trailers similar to a given trailer."""
        api = get_api_client()
        return api.get_trailers(
            user_id=user_id,
            max_official_rating=max_official_rating,
            has_theme_song=has_theme_song,
            has_theme_video=has_theme_video,
            has_subtitles=has_subtitles,
            has_special_feature=has_special_feature,
            has_trailer=has_trailer,
            adjacent_to=adjacent_to,
            parent_index_number=parent_index_number,
            has_parental_rating=has_parental_rating,
            is_hd=is_hd,
            is4_k=is4_k,
            location_types=location_types,
            exclude_location_types=exclude_location_types,
            is_missing=is_missing,
            is_unaired=is_unaired,
            min_community_rating=min_community_rating,
            min_critic_rating=min_critic_rating,
            min_premiere_date=min_premiere_date,
            min_date_last_saved=min_date_last_saved,
            min_date_last_saved_for_user=min_date_last_saved_for_user,
            max_premiere_date=max_premiere_date,
            has_overview=has_overview,
            has_imdb_id=has_imdb_id,
            has_tmdb_id=has_tmdb_id,
            has_tvdb_id=has_tvdb_id,
            is_movie=is_movie,
            is_series=is_series,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            exclude_item_ids=exclude_item_ids,
            start_index=start_index,
            limit=limit,
            recursive=recursive,
            search_term=search_term,
            sort_order=sort_order,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            filters=filters,
            is_favorite=is_favorite,
            media_types=media_types,
            image_types=image_types,
            sort_by=sort_by,
            is_played=is_played,
            genres=genres,
            official_ratings=official_ratings,
            tags=tags,
            years=years,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            person=person,
            person_ids=person_ids,
            person_types=person_types,
            studios=studios,
            artists=artists,
            exclude_artist_ids=exclude_artist_ids,
            artist_ids=artist_ids,
            album_artist_ids=album_artist_ids,
            contributing_artist_ids=contributing_artist_ids,
            albums=albums,
            album_ids=album_ids,
            ids=ids,
            video_types=video_types,
            min_official_rating=min_official_rating,
            is_locked=is_locked,
            is_place_holder=is_place_holder,
            has_official_rating=has_official_rating,
            collapse_box_set_items=collapse_box_set_items,
            min_width=min_width,
            min_height=min_height,
            max_width=max_width,
            max_height=max_height,
            is3_d=is3_d,
            series_status=series_status,
            name_starts_with_or_greater=name_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
            studio_ids=studio_ids,
            genre_ids=genre_ids,
            enable_total_record_count=enable_total_record_count,
            enable_images=enable_images,
        )

    @mcp.tool(
        name="get_trickplay_tile_image",
        description="Gets a trickplay tile image.",
        tags={"Trickplay"},
    )
    def get_trickplay_tile_image_tool(
        item_id: str = Field(description="The item id."),
        width: int = Field(description="The width of a single tile."),
        index: int = Field(description="The index of the desired tile."),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if using an alternate version.",
        ),
    ) -> Any:
        """Gets a trickplay tile image."""
        api = get_api_client()
        return api.get_trickplay_tile_image(
            item_id=item_id, width=width, index=index, media_source_id=media_source_id
        )

    @mcp.tool(
        name="get_trickplay_hls_playlist",
        description="Gets an image tiles playlist for trickplay.",
        tags={"Trickplay"},
    )
    def get_trickplay_hls_playlist_tool(
        item_id: str = Field(description="The item id."),
        width: int = Field(description="The width of a single tile."),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if using an alternate version.",
        ),
    ) -> Any:
        """Gets an image tiles playlist for trickplay."""
        api = get_api_client()
        return api.get_trickplay_hls_playlist(
            item_id=item_id, width=width, media_source_id=media_source_id
        )

    @mcp.tool(
        name="get_episodes",
        description="Gets episodes for a tv season.",
        tags={"TvShows"},
    )
    def get_episodes_tool(
        series_id: str = Field(description="The series id."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
        season: Optional[int] = Field(
            default=None, description="Optional filter by season number."
        ),
        season_id: Optional[str] = Field(
            default=None, description="Optional. Filter by season id."
        ),
        is_missing: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by items that are missing episodes or not.",
        ),
        adjacent_to: Optional[str] = Field(
            default=None,
            description="Optional. Return items that are siblings of a supplied item.",
        ),
        start_item_id: Optional[str] = Field(
            default=None,
            description="Optional. Skip through the list until a given item is found.",
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional, include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional, the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        sort_by: Optional[str] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
    ) -> Any:
        """Gets episodes for a tv season."""
        api = get_api_client()
        return api.get_episodes(
            series_id=series_id,
            user_id=user_id,
            fields=fields,
            season=season,
            season_id=season_id,
            is_missing=is_missing,
            adjacent_to=adjacent_to,
            start_item_id=start_item_id,
            start_index=start_index,
            limit=limit,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
            sort_by=sort_by,
        )

    @mcp.tool(
        name="get_seasons",
        description="Gets seasons for a tv series.",
        tags={"TvShows"},
    )
    def get_seasons_tool(
        series_id: str = Field(description="The series id."),
        user_id: Optional[str] = Field(default=None, description="The user id."),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output. This allows multiple, comma delimited. Options: Budget, Chapters, DateCreated, Genres, HomePageUrl, IndexOptions, MediaStreams, Overview, ParentId, Path, People, ProviderIds, PrimaryImageAspectRatio, Revenue, SortName, Studios, Taglines, TrailerUrls.",
        ),
        is_special_season: Optional[bool] = Field(
            default=None, description="Optional. Filter by special season."
        ),
        is_missing: Optional[bool] = Field(
            default=None,
            description="Optional. Filter by items that are missing episodes or not.",
        ),
        adjacent_to: Optional[str] = Field(
            default=None,
            description="Optional. Return items that are siblings of a supplied item.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
    ) -> Any:
        """Gets seasons for a tv series."""
        api = get_api_client()
        return api.get_seasons(
            series_id=series_id,
            user_id=user_id,
            fields=fields,
            is_special_season=is_special_season,
            is_missing=is_missing,
            adjacent_to=adjacent_to,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
        )

    @mcp.tool(
        name="get_next_up",
        description="Gets a list of next up episodes.",
        tags={"TvShows"},
    )
    def get_next_up_tool(
        user_id: Optional[str] = Field(
            default=None,
            description="The user id of the user to get the next up episodes for.",
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        series_id: Optional[str] = Field(
            default=None, description="Optional. Filter by series id."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Optional. Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        next_up_date_cutoff: Optional[str] = Field(
            default=None,
            description="Optional. Starting date of shows to show in Next Up section.",
        ),
        enable_total_record_count: Optional[bool] = Field(
            default=None,
            description="Whether to enable the total records count. Defaults to true.",
        ),
        disable_first_episode: Optional[bool] = Field(
            default=None,
            description="Whether to disable sending the first episode in a series as next up.",
        ),
        enable_resumable: Optional[bool] = Field(
            default=None,
            description="Whether to include resumable episodes in next up results.",
        ),
        enable_rewatching: Optional[bool] = Field(
            default=None,
            description="Whether to include watched episodes in next up results.",
        ),
    ) -> Any:
        """Gets a list of next up episodes."""
        api = get_api_client()
        return api.get_next_up(
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            fields=fields,
            series_id=series_id,
            parent_id=parent_id,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
            next_up_date_cutoff=next_up_date_cutoff,
            enable_total_record_count=enable_total_record_count,
            disable_first_episode=disable_first_episode,
            enable_resumable=enable_resumable,
            enable_rewatching=enable_rewatching,
        )

    @mcp.tool(
        name="get_upcoming_episodes",
        description="Gets a list of upcoming episodes.",
        tags={"TvShows"},
    )
    def get_upcoming_episodes_tool(
        user_id: Optional[str] = Field(
            default=None,
            description="The user id of the user to get the upcoming episodes for.",
        ),
        start_index: Optional[int] = Field(
            default=None,
            description="Optional. The record index to start at. All items with a lower index will be dropped from the results.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Optional. Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
    ) -> Any:
        """Gets a list of upcoming episodes."""
        api = get_api_client()
        return api.get_upcoming_episodes(
            user_id=user_id,
            start_index=start_index,
            limit=limit,
            fields=fields,
            parent_id=parent_id,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
        )

    @mcp.tool(
        name="get_universal_audio_stream",
        description="Gets an audio stream.",
        tags={"UniversalAudio"},
    )
    def get_universal_audio_stream_tool(
        item_id: str = Field(description="The item id."),
        container: Optional[List[Any]] = Field(
            default=None, description="Optional. The audio container."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        user_id: Optional[str] = Field(
            default=None, description="Optional. The user id."
        ),
        audio_codec: Optional[str] = Field(
            default=None, description="Optional. The audio codec to transcode to."
        ),
        max_audio_channels: Optional[int] = Field(
            default=None, description="Optional. The maximum number of audio channels."
        ),
        transcoding_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The number of how many audio channels to transcode to.",
        ),
        max_streaming_bitrate: Optional[int] = Field(
            default=None, description="Optional. The maximum streaming bitrate."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        transcoding_container: Optional[str] = Field(
            default=None, description="Optional. The container to transcode to."
        ),
        transcoding_protocol: Optional[str] = Field(
            default=None, description="Optional. The transcoding protocol."
        ),
        max_audio_sample_rate: Optional[int] = Field(
            default=None, description="Optional. The maximum audio sample rate."
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        enable_remote_media: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable remote media."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        enable_redirection: Optional[bool] = Field(
            default=None, description="Whether to enable redirection. Defaults to true."
        ),
    ) -> Any:
        """Gets an audio stream."""
        api = get_api_client()
        return api.get_universal_audio_stream(
            item_id=item_id,
            container=container,
            media_source_id=media_source_id,
            device_id=device_id,
            user_id=user_id,
            audio_codec=audio_codec,
            max_audio_channels=max_audio_channels,
            transcoding_audio_channels=transcoding_audio_channels,
            max_streaming_bitrate=max_streaming_bitrate,
            audio_bit_rate=audio_bit_rate,
            start_time_ticks=start_time_ticks,
            transcoding_container=transcoding_container,
            transcoding_protocol=transcoding_protocol,
            max_audio_sample_rate=max_audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            enable_remote_media=enable_remote_media,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
            break_on_non_key_frames=break_on_non_key_frames,
            enable_redirection=enable_redirection,
        )

    @mcp.tool(name="get_users", description="Gets a list of users.", tags={"User"})
    def get_users_tool(
        is_hidden: Optional[bool] = Field(
            default=None, description="Optional filter by IsHidden=true or false."
        ),
        is_disabled: Optional[bool] = Field(
            default=None, description="Optional filter by IsDisabled=true or false."
        ),
    ) -> Any:
        """Gets a list of users."""
        api = get_api_client()
        return api.get_users(is_hidden=is_hidden, is_disabled=is_disabled)

    @mcp.tool(name="update_user", description="Updates a user.", tags={"User"})
    def update_user_tool(
        user_id: Optional[str] = Field(default=None, description="The user id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates a user."""
        api = get_api_client()
        return api.update_user(user_id=user_id, body=body)

    @mcp.tool(name="get_user_by_id", description="Gets a user by Id.", tags={"User"})
    def get_user_by_id_tool(user_id: str = Field(description="The user id.")) -> Any:
        """Gets a user by Id."""
        api = get_api_client()
        return api.get_user_by_id(user_id=user_id)

    @mcp.tool(name="delete_user", description="Deletes a user.", tags={"User"})
    def delete_user_tool(user_id: str = Field(description="The user id.")) -> Any:
        """Deletes a user."""
        api = get_api_client()
        return api.delete_user(user_id=user_id)

    @mcp.tool(
        name="update_user_policy", description="Updates a user policy.", tags={"User"}
    )
    def update_user_policy_tool(
        user_id: str = Field(description="The user id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates a user policy."""
        api = get_api_client()
        return api.update_user_policy(user_id=user_id, body=body)

    @mcp.tool(
        name="authenticate_user_by_name",
        description="Authenticates a user by name.",
        tags={"User"},
    )
    def authenticate_user_by_name_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Authenticates a user by name."""
        api = get_api_client()
        return api.authenticate_user_by_name(body=body)

    @mcp.tool(
        name="authenticate_with_quick_connect",
        description="Authenticates a user with quick connect.",
        tags={"User"},
    )
    def authenticate_with_quick_connect_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Authenticates a user with quick connect."""
        api = get_api_client()
        return api.authenticate_with_quick_connect(body=body)

    @mcp.tool(
        name="update_user_configuration",
        description="Updates a user configuration.",
        tags={"User"},
    )
    def update_user_configuration_tool(
        user_id: Optional[str] = Field(default=None, description="The user id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates a user configuration."""
        api = get_api_client()
        return api.update_user_configuration(user_id=user_id, body=body)

    @mcp.tool(
        name="forgot_password",
        description="Initiates the forgot password process for a local user.",
        tags={"User"},
    )
    def forgot_password_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Initiates the forgot password process for a local user."""
        api = get_api_client()
        return api.forgot_password(body=body)

    @mcp.tool(
        name="forgot_password_pin",
        description="Redeems a forgot password pin.",
        tags={"User"},
    )
    def forgot_password_pin_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Redeems a forgot password pin."""
        api = get_api_client()
        return api.forgot_password_pin(body=body)

    @mcp.tool(
        name="get_current_user",
        description="Gets the user based on auth token.",
        tags={"User"},
    )
    def get_current_user_tool() -> Any:
        """Gets the user based on auth token."""
        api = get_api_client()
        return api.get_current_user()

    @mcp.tool(name="create_user_by_name", description="Creates a user.", tags={"User"})
    def create_user_by_name_tool(
        body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    ) -> Any:
        """Creates a user."""
        api = get_api_client()
        return api.create_user_by_name(body=body)

    @mcp.tool(
        name="update_user_password",
        description="Updates a user's password.",
        tags={"User"},
    )
    def update_user_password_tool(
        user_id: Optional[str] = Field(default=None, description="The user id."),
        body: Optional[Dict[str, Any]] = Field(
            default=None, description="Request body"
        ),
    ) -> Any:
        """Updates a user's password."""
        api = get_api_client()
        return api.update_user_password(user_id=user_id, body=body)

    @mcp.tool(
        name="get_public_users",
        description="Gets a list of publicly visible users for display on a login screen.",
        tags={"User"},
    )
    def get_public_users_tool() -> Any:
        """Gets a list of publicly visible users for display on a login screen."""
        api = get_api_client()
        return api.get_public_users()

    @mcp.tool(
        name="get_intros",
        description="Gets intros to play before the main media item plays.",
        tags={"UserLibrary"},
    )
    def get_intros_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Gets intros to play before the main media item plays."""
        api = get_api_client()
        return api.get_intros(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="get_local_trailers",
        description="Gets local trailers for an item.",
        tags={"UserLibrary"},
    )
    def get_local_trailers_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Gets local trailers for an item."""
        api = get_api_client()
        return api.get_local_trailers(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="get_special_features",
        description="Gets special features for an item.",
        tags={"UserLibrary"},
    )
    def get_special_features_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Gets special features for an item."""
        api = get_api_client()
        return api.get_special_features(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="get_latest_media", description="Gets latest media.", tags={"UserLibrary"}
    )
    def get_latest_media_tool(
        user_id: Optional[str] = Field(default=None, description="User id."),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be filtered based on item type. This allows multiple, comma delimited.",
        ),
        is_played: Optional[bool] = Field(
            default=None, description="Filter by items that are played, or not."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. include image information in output."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. the max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. include user data."
        ),
        limit: Optional[int] = Field(default=None, description="Return item limit."),
        group_items: Optional[bool] = Field(
            default=None,
            description="Whether or not to group items into a parent container.",
        ),
    ) -> Any:
        """Gets latest media."""
        api = get_api_client()
        return api.get_latest_media(
            user_id=user_id,
            parent_id=parent_id,
            fields=fields,
            include_item_types=include_item_types,
            is_played=is_played,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            enable_user_data=enable_user_data,
            limit=limit,
            group_items=group_items,
        )

    @mcp.tool(
        name="get_root_folder",
        description="Gets the root folder from a user's library.",
        tags={"UserLibrary"},
    )
    def get_root_folder_tool(
        user_id: Optional[str] = Field(default=None, description="User id.")
    ) -> Any:
        """Gets the root folder from a user's library."""
        api = get_api_client()
        return api.get_root_folder(user_id=user_id)

    @mcp.tool(
        name="mark_favorite_item",
        description="Marks an item as a favorite.",
        tags={"UserLibrary"},
    )
    def mark_favorite_item_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Marks an item as a favorite."""
        api = get_api_client()
        return api.mark_favorite_item(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="unmark_favorite_item",
        description="Unmarks item as a favorite.",
        tags={"UserLibrary"},
    )
    def unmark_favorite_item_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Unmarks item as a favorite."""
        api = get_api_client()
        return api.unmark_favorite_item(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="delete_user_item_rating",
        description="Deletes a user's saved personal rating for an item.",
        tags={"UserLibrary"},
    )
    def delete_user_item_rating_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
    ) -> Any:
        """Deletes a user's saved personal rating for an item."""
        api = get_api_client()
        return api.delete_user_item_rating(user_id=user_id, item_id=item_id)

    @mcp.tool(
        name="update_user_item_rating",
        description="Updates a user's rating for an item.",
        tags={"UserLibrary"},
    )
    def update_user_item_rating_tool(
        item_id: str = Field(description="Item id."),
        user_id: Optional[str] = Field(default=None, description="User id."),
        likes: Optional[bool] = Field(
            default=None,
            description="Whether this M:Jellyfin.Api.Controllers.UserLibraryController.UpdateUserItemRating(System.Nullable{System.Guid},System.Guid,System.Nullable{System.Boolean}) is likes.",
        ),
    ) -> Any:
        """Updates a user's rating for an item."""
        api = get_api_client()
        return api.update_user_item_rating(
            user_id=user_id, item_id=item_id, likes=likes
        )

    @mcp.tool(name="get_user_views", description="Get user views.", tags={"UserViews"})
    def get_user_views_tool(
        user_id: Optional[str] = Field(default=None, description="User id."),
        include_external_content: Optional[bool] = Field(
            default=None,
            description="Whether or not to include external views such as channels or live tv.",
        ),
        preset_views: Optional[List[Any]] = Field(
            default=None, description="Preset views."
        ),
        include_hidden: Optional[bool] = Field(
            default=None, description="Whether or not to include hidden content."
        ),
    ) -> Any:
        """Get user views."""
        api = get_api_client()
        return api.get_user_views(
            user_id=user_id,
            include_external_content=include_external_content,
            preset_views=preset_views,
            include_hidden=include_hidden,
        )

    @mcp.tool(
        name="get_grouping_options",
        description="Get user view grouping options.",
        tags={"UserViews"},
    )
    def get_grouping_options_tool(
        user_id: Optional[str] = Field(default=None, description="User id.")
    ) -> Any:
        """Get user view grouping options."""
        api = get_api_client()
        return api.get_grouping_options(user_id=user_id)

    @mcp.tool(
        name="get_attachment",
        description="Get video attachment.",
        tags={"VideoAttachments"},
    )
    def get_attachment_tool(
        video_id: str = Field(description="Video ID."),
        media_source_id: str = Field(description="Media Source ID."),
        index: int = Field(description="Attachment Index."),
    ) -> Any:
        """Get video attachment."""
        api = get_api_client()
        return api.get_attachment(
            video_id=video_id, media_source_id=media_source_id, index=index
        )

    @mcp.tool(
        name="get_additional_part",
        description="Gets additional parts for a video.",
        tags={"Videos"},
    )
    def get_additional_part_tool(
        item_id: str = Field(description="The item id."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
    ) -> Any:
        """Gets additional parts for a video."""
        api = get_api_client()
        return api.get_additional_part(item_id=item_id, user_id=user_id)

    @mcp.tool(
        name="delete_alternate_sources",
        description="Removes alternate video sources.",
        tags={"Videos"},
    )
    def delete_alternate_sources_tool(
        item_id: str = Field(description="The item id."),
    ) -> Any:
        """Removes alternate video sources."""
        api = get_api_client()
        return api.delete_alternate_sources(item_id=item_id)

    @mcp.tool(
        name="get_video_stream", description="Gets a video stream.", tags={"Videos"}
    )
    def get_video_stream_tool(
        item_id: str = Field(description="The item id."),
        container: Optional[str] = Field(
            default=None,
            description="The video container. Possible values are: ts, webm, asf, wmv, ogv, mp4, m4v, mkv, mpeg, mpg, avi, 3gp, wmv, wtv, m2ts, mov, iso, flv.",
        ),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3. If omitted the server will auto-select using the url's extension.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        max_width: Optional[int] = Field(
            default=None,
            description="Optional. The maximum horizontal resolution of the encoded video.",
        ),
        max_height: Optional[int] = Field(
            default=None,
            description="Optional. The maximum vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264. If omitted the server will auto-select using the url's extension.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
    ) -> Any:
        """Gets a video stream."""
        api = get_api_client()
        return api.get_video_stream(
            item_id=item_id,
            container=container,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            max_width=max_width,
            max_height=max_height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
        )

    @mcp.tool(
        name="get_video_stream_by_container",
        description="Gets a video stream.",
        tags={"Videos"},
    )
    def get_video_stream_by_container_tool(
        item_id: str = Field(description="The item id."),
        container: str = Field(
            description="The video container. Possible values are: ts, webm, asf, wmv, ogv, mp4, m4v, mkv, mpeg, mpg, avi, 3gp, wmv, wtv, m2ts, mov, iso, flv."
        ),
        static: Optional[bool] = Field(
            default=None,
            description="Optional. If true, the original file will be streamed statically without any encoding. Use either no url extension or the original file extension. true/false.",
        ),
        params: Optional[str] = Field(
            default=None, description="The streaming parameters."
        ),
        tag: Optional[str] = Field(default=None, description="The tag."),
        device_profile_id: Optional[str] = Field(
            default=None, description="Optional. The dlna device profile id to utilize."
        ),
        play_session_id: Optional[str] = Field(
            default=None, description="The play session id."
        ),
        segment_container: Optional[str] = Field(
            default=None, description="The segment container."
        ),
        segment_length: Optional[int] = Field(
            default=None, description="The segment length."
        ),
        min_segments: Optional[int] = Field(
            default=None, description="The minimum number of segments."
        ),
        media_source_id: Optional[str] = Field(
            default=None,
            description="The media version id, if playing an alternate version.",
        ),
        device_id: Optional[str] = Field(
            default=None,
            description="The device id of the client requesting. Used to stop encoding processes when needed.",
        ),
        audio_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify an audio codec to encode to, e.g. mp3. If omitted the server will auto-select using the url's extension.",
        ),
        enable_auto_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow automatic stream copy if requested values match the original source. Defaults to true.",
        ),
        allow_video_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the video stream url.",
        ),
        allow_audio_stream_copy: Optional[bool] = Field(
            default=None,
            description="Whether or not to allow copying of the audio stream url.",
        ),
        break_on_non_key_frames: Optional[bool] = Field(
            default=None, description="Optional. Whether to break on non key frames."
        ),
        audio_sample_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific audio sample rate, e.g. 44100.",
        ),
        max_audio_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum audio bit depth."
        ),
        audio_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify an audio bitrate to encode to, e.g. 128000. If omitted this will be left to encoder defaults.",
        ),
        audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a specific number of audio channels to encode to, e.g. 2.",
        ),
        max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. Specify a maximum number of audio channels to encode to, e.g. 2.",
        ),
        profile: Optional[str] = Field(
            default=None,
            description="Optional. Specify a specific an encoder profile (varies by encoder), e.g. main, baseline, high.",
        ),
        level: Optional[str] = Field(
            default=None,
            description="Optional. Specify a level for the encoder profile (varies by encoder), e.g. 3, 3.1.",
        ),
        framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        max_framerate: Optional[float] = Field(
            default=None,
            description="Optional. A specific maximum video framerate to encode to, e.g. 23.976. Generally this should be omitted unless the device has specific requirements.",
        ),
        copy_timestamps: Optional[bool] = Field(
            default=None,
            description="Whether or not to copy timestamps when transcoding with an offset. Defaults to false.",
        ),
        start_time_ticks: Optional[int] = Field(
            default=None,
            description="Optional. Specify a starting offset, in ticks. 1 tick = 10000 ms.",
        ),
        width: Optional[int] = Field(
            default=None,
            description="Optional. The fixed horizontal resolution of the encoded video.",
        ),
        height: Optional[int] = Field(
            default=None,
            description="Optional. The fixed vertical resolution of the encoded video.",
        ),
        max_width: Optional[int] = Field(
            default=None,
            description="Optional. The maximum horizontal resolution of the encoded video.",
        ),
        max_height: Optional[int] = Field(
            default=None,
            description="Optional. The maximum vertical resolution of the encoded video.",
        ),
        video_bit_rate: Optional[int] = Field(
            default=None,
            description="Optional. Specify a video bitrate to encode to, e.g. 500000. If omitted this will be left to encoder defaults.",
        ),
        subtitle_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the subtitle stream to use. If omitted no subtitles will be used.",
        ),
        subtitle_method: Optional[str] = Field(
            default=None, description="Optional. Specify the subtitle delivery method."
        ),
        max_ref_frames: Optional[int] = Field(default=None, description="Optional."),
        max_video_bit_depth: Optional[int] = Field(
            default=None, description="Optional. The maximum video bit depth."
        ),
        require_avc: Optional[bool] = Field(
            default=None, description="Optional. Whether to require avc."
        ),
        de_interlace: Optional[bool] = Field(
            default=None, description="Optional. Whether to deinterlace the video."
        ),
        require_non_anamorphic: Optional[bool] = Field(
            default=None,
            description="Optional. Whether to require a non anamorphic stream.",
        ),
        transcoding_max_audio_channels: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of audio channels to transcode.",
        ),
        cpu_core_limit: Optional[int] = Field(
            default=None,
            description="Optional. The limit of how many cpu cores to use.",
        ),
        live_stream_id: Optional[str] = Field(
            default=None, description="The live stream id."
        ),
        enable_mpegts_m2_ts_mode: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable the MpegtsM2Ts mode."
        ),
        video_codec: Optional[str] = Field(
            default=None,
            description="Optional. Specify a video codec to encode to, e.g. h264. If omitted the server will auto-select using the url's extension.",
        ),
        subtitle_codec: Optional[str] = Field(
            default=None, description="Optional. Specify a subtitle codec to encode to."
        ),
        transcode_reasons: Optional[str] = Field(
            default=None, description="Optional. The transcoding reason."
        ),
        audio_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the audio stream to use. If omitted the first audio stream will be used.",
        ),
        video_stream_index: Optional[int] = Field(
            default=None,
            description="Optional. The index of the video stream to use. If omitted the first video stream will be used.",
        ),
        context: Optional[str] = Field(
            default=None,
            description="Optional. The MediaBrowser.Model.Dlna.EncodingContext.",
        ),
        stream_options: Optional[Dict[str, Any]] = Field(
            default=None, description="Optional. The streaming options."
        ),
        enable_audio_vbr_encoding: Optional[bool] = Field(
            default=None, description="Optional. Whether to enable Audio Encoding."
        ),
    ) -> Any:
        """Gets a video stream."""
        api = get_api_client()
        return api.get_video_stream_by_container(
            item_id=item_id,
            container=container,
            static=static,
            params=params,
            tag=tag,
            device_profile_id=device_profile_id,
            play_session_id=play_session_id,
            segment_container=segment_container,
            segment_length=segment_length,
            min_segments=min_segments,
            media_source_id=media_source_id,
            device_id=device_id,
            audio_codec=audio_codec,
            enable_auto_stream_copy=enable_auto_stream_copy,
            allow_video_stream_copy=allow_video_stream_copy,
            allow_audio_stream_copy=allow_audio_stream_copy,
            break_on_non_key_frames=break_on_non_key_frames,
            audio_sample_rate=audio_sample_rate,
            max_audio_bit_depth=max_audio_bit_depth,
            audio_bit_rate=audio_bit_rate,
            audio_channels=audio_channels,
            max_audio_channels=max_audio_channels,
            profile=profile,
            level=level,
            framerate=framerate,
            max_framerate=max_framerate,
            copy_timestamps=copy_timestamps,
            start_time_ticks=start_time_ticks,
            width=width,
            height=height,
            max_width=max_width,
            max_height=max_height,
            video_bit_rate=video_bit_rate,
            subtitle_stream_index=subtitle_stream_index,
            subtitle_method=subtitle_method,
            max_ref_frames=max_ref_frames,
            max_video_bit_depth=max_video_bit_depth,
            require_avc=require_avc,
            de_interlace=de_interlace,
            require_non_anamorphic=require_non_anamorphic,
            transcoding_max_audio_channels=transcoding_max_audio_channels,
            cpu_core_limit=cpu_core_limit,
            live_stream_id=live_stream_id,
            enable_mpegts_m2_ts_mode=enable_mpegts_m2_ts_mode,
            video_codec=video_codec,
            subtitle_codec=subtitle_codec,
            transcode_reasons=transcode_reasons,
            audio_stream_index=audio_stream_index,
            video_stream_index=video_stream_index,
            context=context,
            stream_options=stream_options,
            enable_audio_vbr_encoding=enable_audio_vbr_encoding,
        )

    @mcp.tool(
        name="merge_versions",
        description="Merges videos into a single record.",
        tags={"Videos"},
    )
    def merge_versions_tool(
        ids: Optional[List[Any]] = Field(
            default=None,
            description="Item id list. This allows multiple, comma delimited.",
        )
    ) -> Any:
        """Merges videos into a single record."""
        api = get_api_client()
        return api.merge_versions(ids=ids)

    @mcp.tool(name="get_years", description="Get years.", tags={"Years"})
    def get_years_tool(
        start_index: Optional[int] = Field(
            default=None,
            description="Skips over a given number of items within the results. Use for paging.",
        ),
        limit: Optional[int] = Field(
            default=None,
            description="Optional. The maximum number of records to return.",
        ),
        sort_order: Optional[List[Any]] = Field(
            default=None, description="Sort Order - Ascending,Descending."
        ),
        parent_id: Optional[str] = Field(
            default=None,
            description="Specify this to localize the search to a specific item or folder. Omit to use the root.",
        ),
        fields: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify additional fields of information to return in the output.",
        ),
        exclude_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be excluded based on item type. This allows multiple, comma delimited.",
        ),
        include_item_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. If specified, results will be included based on item type. This allows multiple, comma delimited.",
        ),
        media_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Filter by MediaType. Allows multiple, comma delimited.",
        ),
        sort_by: Optional[List[Any]] = Field(
            default=None,
            description="Optional. Specify one or more sort orders, comma delimited. Options: Album, AlbumArtist, Artist, Budget, CommunityRating, CriticRating, DateCreated, DatePlayed, PlayCount, PremiereDate, ProductionYear, SortName, Random, Revenue, Runtime.",
        ),
        enable_user_data: Optional[bool] = Field(
            default=None, description="Optional. Include user data."
        ),
        image_type_limit: Optional[int] = Field(
            default=None,
            description="Optional. The max number of images to return, per image type.",
        ),
        enable_image_types: Optional[List[Any]] = Field(
            default=None,
            description="Optional. The image types to include in the output.",
        ),
        user_id: Optional[str] = Field(default=None, description="User Id."),
        recursive: Optional[bool] = Field(
            default=None, description="Search recursively."
        ),
        enable_images: Optional[bool] = Field(
            default=None, description="Optional. Include image information in output."
        ),
    ) -> Any:
        """Get years."""
        api = get_api_client()
        return api.get_years(
            start_index=start_index,
            limit=limit,
            sort_order=sort_order,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            media_types=media_types,
            sort_by=sort_by,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            user_id=user_id,
            recursive=recursive,
            enable_images=enable_images,
        )

    @mcp.tool(name="get_year", description="Gets a year.", tags={"Years"})
    def get_year_tool(
        year: int = Field(description="The year."),
        user_id: Optional[str] = Field(
            default=None,
            description="Optional. Filter by user id, and attach user data.",
        ),
    ) -> Any:
        """Gets a year."""
        api = get_api_client()
        return api.get_year(year=year, user_id=user_id)


def jellyfin_mcp() -> None:
    """Run the Jellyfin MCP server with specified transport and connection parameters.

    This function parses command-line arguments to configure and start the MCP server for Jellyfin API interactions.
    It supports stdio or TCP transport modes and exits on invalid arguments or help requests.
    """
    parser = argparse.ArgumentParser(description="Jellyfin MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "streamable-http", "sse"],
        help="Transport method: 'stdio', 'streamable-http', or 'sse' [legacy] (default: stdio)",
    )
    parser.add_argument(
        "-s",
        "--host",
        default=DEFAULT_HOST,
        help="Host address for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port number for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--auth-type",
        default="none",
        choices=["none", "static", "jwt", "oauth-proxy", "oidc-proxy", "remote-oauth"],
        help="Authentication type for MCP server: 'none' (disabled), 'static' (internal), 'jwt' (external token verification), 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (external) (default: none)",
    )
    # JWT/Token params
    parser.add_argument(
        "--token-jwks-uri", default=None, help="JWKS URI for JWT verification"
    )
    parser.add_argument(
        "--token-issuer", default=None, help="Issuer for JWT verification"
    )
    parser.add_argument(
        "--token-audience", default=None, help="Audience for JWT verification"
    )
    parser.add_argument(
        "--token-algorithm",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM"),
        choices=[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
        ],
        help="JWT signing algorithm (required for HMAC or static key). Auto-detected for JWKS.",
    )
    parser.add_argument(
        "--token-secret",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Shared secret for HMAC (HS*) or PEM public key for static asymmetric verification.",
    )
    parser.add_argument(
        "--token-public-key",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Path to PEM public key file or inline PEM string (for static asymmetric keys).",
    )
    parser.add_argument(
        "--required-scopes",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES"),
        help="Comma-separated list of required scopes (e.g., jellyfin.read,jellyfin.write).",
    )
    # OAuth Proxy params
    parser.add_argument(
        "--oauth-upstream-auth-endpoint",
        default=None,
        help="Upstream authorization endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-token-endpoint",
        default=None,
        help="Upstream token endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-id",
        default=None,
        help="Upstream client ID for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-secret",
        default=None,
        help="Upstream client secret for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-base-url", default=None, help="Base URL for OAuth Proxy"
    )
    # OIDC Proxy params
    parser.add_argument(
        "--oidc-config-url", default=None, help="OIDC configuration URL"
    )
    parser.add_argument("--oidc-client-id", default=None, help="OIDC client ID")
    parser.add_argument("--oidc-client-secret", default=None, help="OIDC client secret")
    parser.add_argument("--oidc-base-url", default=None, help="Base URL for OIDC Proxy")
    # Remote OAuth params
    parser.add_argument(
        "--remote-auth-servers",
        default=None,
        help="Comma-separated list of authorization servers for Remote OAuth",
    )
    parser.add_argument(
        "--remote-base-url", default=None, help="Base URL for Remote OAuth"
    )
    # Common
    parser.add_argument(
        "--allowed-client-redirect-uris",
        default=None,
        help="Comma-separated list of allowed client redirect URIs",
    )
    # Eunomia params
    parser.add_argument(
        "--eunomia-type",
        default="none",
        choices=["none", "embedded", "remote"],
        help="Eunomia authorization type: 'none' (disabled), 'embedded' (built-in), 'remote' (external) (default: none)",
    )
    parser.add_argument(
        "--eunomia-policy-file",
        default="mcp_policies.json",
        help="Policy file for embedded Eunomia (default: mcp_policies.json)",
    )
    parser.add_argument(
        "--eunomia-remote-url", default=None, help="URL for remote Eunomia server"
    )
    # Delegation params
    parser.add_argument(
        "--enable-delegation",
        action="store_true",
        default=to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
        help="Enable OIDC token delegation",
    )
    parser.add_argument(
        "--audience",
        default=os.environ.get("AUDIENCE", None),
        help="Audience for the delegated token",
    )
    parser.add_argument(
        "--delegated-scopes",
        default=os.environ.get("DELEGATED_SCOPES", "api"),
        help="Scopes for the delegated token (space-separated)",
    )
    parser.add_argument(
        "--openapi-file",
        default=None,
        help="Path to the OpenAPI JSON file to import additional tools from",
    )
    parser.add_argument(
        "--openapi-base-url",
        default=None,
        help="Base URL for the OpenAPI client (overrides instance URL)",
    )
    parser.add_argument(
        "--openapi-use-token",
        action="store_true",
        help="Use the incoming Bearer token (from MCP request) to authenticate OpenAPI import",
    )

    parser.add_argument(
        "--openapi-username",
        default=os.getenv("OPENAPI_USERNAME"),
        help="Username for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-password",
        default=os.getenv("OPENAPI_PASSWORD"),
        help="Password for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-id",
        default=os.getenv("OPENAPI_CLIENT_ID"),
        help="OAuth client ID for OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-secret",
        default=os.getenv("OPENAPI_CLIENT_SECRET"),
        help="OAuth client secret for OpenAPI import",
    )

    args = parser.parse_args()

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    # Update config with CLI arguments
    config["enable_delegation"] = args.enable_delegation
    config["audience"] = args.audience or config["audience"]
    config["delegated_scopes"] = args.delegated_scopes or config["delegated_scopes"]
    config["oidc_config_url"] = args.oidc_config_url or config["oidc_config_url"]
    config["oidc_client_id"] = args.oidc_client_id or config["oidc_client_id"]
    config["oidc_client_secret"] = (
        args.oidc_client_secret or config["oidc_client_secret"]
    )

    # Configure delegation if enabled
    if config["enable_delegation"]:
        if args.auth_type != "oidc-proxy":
            logger.error("Token delegation requires auth-type=oidc-proxy")
            sys.exit(1)
        if not config["audience"]:
            logger.error("audience is required for delegation")
            sys.exit(1)
        if not all(
            [
                config["oidc_config_url"],
                config["oidc_client_id"],
                config["oidc_client_secret"],
            ]
        ):
            logger.error(
                "Delegation requires complete OIDC configuration (oidc-config-url, oidc-client-id, oidc-client-secret)"
            )
            sys.exit(1)

        # Fetch OIDC configuration to get token_endpoint
        try:
            logger.info(
                "Fetching OIDC configuration",
                extra={"oidc_config_url": config["oidc_config_url"]},
            )
            oidc_config_resp = requests.get(config["oidc_config_url"])
            oidc_config_resp.raise_for_status()
            oidc_config = oidc_config_resp.json()
            config["token_endpoint"] = oidc_config.get("token_endpoint")
            if not config["token_endpoint"]:
                logger.error("No token_endpoint found in OIDC configuration")
                raise ValueError("No token_endpoint found in OIDC configuration")
            logger.info(
                "OIDC configuration fetched successfully",
                extra={"token_endpoint": config["token_endpoint"]},
            )
        except Exception as e:
            print(f"Failed to fetch OIDC configuration: {e}")
            logger.error(
                "Failed to fetch OIDC configuration",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            sys.exit(1)

    # Set auth based on type
    auth = None
    allowed_uris = (
        args.allowed_client_redirect_uris.split(",")
        if args.allowed_client_redirect_uris
        else None
    )

    if args.auth_type == "none":
        auth = None
    elif args.auth_type == "static":
        auth = StaticTokenVerifier(
            tokens={
                "test-token": {"client_id": "test-user", "scopes": ["read", "write"]},
                "admin-token": {"client_id": "admin", "scopes": ["admin"]},
            }
        )
    elif args.auth_type == "jwt":
        # Fallback to env vars if not provided via CLI
        jwks_uri = args.token_jwks_uri or os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI")
        issuer = args.token_issuer or os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER")
        audience = args.token_audience or os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE")
        algorithm = args.token_algorithm
        secret_or_key = args.token_secret or args.token_public_key
        public_key_pem = None

        if not (jwks_uri or secret_or_key):
            logger.error(
                "JWT auth requires either --token-jwks-uri or --token-secret/--token-public-key"
            )
            sys.exit(1)
        if not (issuer and audience):
            logger.error("JWT requires --token-issuer and --token-audience")
            sys.exit(1)

        # Load static public key from file if path is given
        if args.token_public_key and os.path.isfile(args.token_public_key):
            try:
                with open(args.token_public_key, "r") as f:
                    public_key_pem = f.read()
                logger.info(f"Loaded static public key from {args.token_public_key}")
            except Exception as e:
                print(f"Failed to read public key file: {e}")
                logger.error(f"Failed to read public key file: {e}")
                sys.exit(1)
        elif args.token_public_key:
            public_key_pem = args.token_public_key  # Inline PEM

        # Validation: Conflicting options
        if jwks_uri and (algorithm or secret_or_key):
            logger.warning(
                "JWKS mode ignores --token-algorithm and --token-secret/--token-public-key"
            )

        # HMAC mode
        if algorithm and algorithm.startswith("HS"):
            if not secret_or_key:
                logger.error(f"HMAC algorithm {algorithm} requires --token-secret")
                sys.exit(1)
            if jwks_uri:
                logger.error("Cannot use --token-jwks-uri with HMAC")
                sys.exit(1)
            public_key = secret_or_key
        else:
            public_key = public_key_pem

        # Required scopes
        required_scopes = None
        if args.required_scopes:
            required_scopes = [
                s.strip() for s in args.required_scopes.split(",") if s.strip()
            ]

        try:
            auth = JWTVerifier(
                jwks_uri=jwks_uri,
                public_key=public_key,
                issuer=issuer,
                audience=audience,
                algorithm=(
                    algorithm if algorithm and algorithm.startswith("HS") else None
                ),
                required_scopes=required_scopes,
            )
            logger.info(
                "JWTVerifier configured",
                extra={
                    "mode": (
                        "JWKS"
                        if jwks_uri
                        else (
                            "HMAC"
                            if algorithm and algorithm.startswith("HS")
                            else "Static Key"
                        )
                    ),
                    "algorithm": algorithm,
                    "required_scopes": required_scopes,
                },
            )
        except Exception as e:
            print(f"Failed to initialize JWTVerifier: {e}")
            logger.error(f"Failed to initialize JWTVerifier: {e}")
            sys.exit(1)
    elif args.auth_type == "oauth-proxy":
        if not (
            args.oauth_upstream_auth_endpoint
            and args.oauth_upstream_token_endpoint
            and args.oauth_upstream_client_id
            and args.oauth_upstream_client_secret
            and args.oauth_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            print(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience"
            )
            logger.error(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience",
                extra={
                    "auth_endpoint": args.oauth_upstream_auth_endpoint,
                    "token_endpoint": args.oauth_upstream_token_endpoint,
                    "client_id": args.oauth_upstream_client_id,
                    "base_url": args.oauth_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = OAuthProxy(
            upstream_authorization_endpoint=args.oauth_upstream_auth_endpoint,
            upstream_token_endpoint=args.oauth_upstream_token_endpoint,
            upstream_client_id=args.oauth_upstream_client_id,
            upstream_client_secret=args.oauth_upstream_client_secret,
            token_verifier=token_verifier,
            base_url=args.oauth_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "oidc-proxy":
        if not (
            args.oidc_config_url
            and args.oidc_client_id
            and args.oidc_client_secret
            and args.oidc_base_url
        ):
            logger.error(
                "oidc-proxy requires oidc-config-url, oidc-client-id, oidc-client-secret, oidc-base-url",
                extra={
                    "config_url": args.oidc_config_url,
                    "client_id": args.oidc_client_id,
                    "base_url": args.oidc_base_url,
                },
            )
            sys.exit(1)
        auth = OIDCProxy(
            config_url=args.oidc_config_url,
            client_id=args.oidc_client_id,
            client_secret=args.oidc_client_secret,
            base_url=args.oidc_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "remote-oauth":
        if not (
            args.remote_auth_servers
            and args.remote_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            logger.error(
                "remote-oauth requires remote-auth-servers, remote-base-url, token-jwks-uri, token-issuer, token-audience",
                extra={
                    "auth_servers": args.remote_auth_servers,
                    "base_url": args.remote_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        auth_servers = [url.strip() for url in args.remote_auth_servers.split(",")]
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=auth_servers,
            base_url=args.remote_base_url,
        )

    # === 2. Build Middleware List ===
    middlewares: List[
        Union[
            UserTokenMiddleware,
            ErrorHandlingMiddleware,
            RateLimitingMiddleware,
            TimingMiddleware,
            LoggingMiddleware,
            JWTClaimsLoggingMiddleware,
            EunomiaMcpMiddleware,
        ]
    ] = [
        ErrorHandlingMiddleware(include_traceback=True, transform_errors=True),
        RateLimitingMiddleware(max_requests_per_second=10.0, burst_capacity=20),
        TimingMiddleware(),
        LoggingMiddleware(),
        JWTClaimsLoggingMiddleware(),
    ]
    if config["enable_delegation"] or args.auth_type == "jwt":
        middlewares.insert(0, UserTokenMiddleware(config=config))  # Must be first

    if args.eunomia_type in ["embedded", "remote"]:
        try:
            from eunomia_mcp import create_eunomia_middleware

            policy_file = args.eunomia_policy_file or "mcp_policies.json"
            eunomia_endpoint = (
                args.eunomia_remote_url if args.eunomia_type == "remote" else None
            )
            eunomia_mw = create_eunomia_middleware(
                policy_file=policy_file, eunomia_endpoint=eunomia_endpoint
            )
            middlewares.append(eunomia_mw)
            logger.info(f"Eunomia middleware enabled ({args.eunomia_type})")
        except Exception as e:
            print(f"Failed to load Eunomia middleware: {e}")
            logger.error("Failed to load Eunomia middleware", extra={"error": str(e)})
            sys.exit(1)

    mcp = FastMCP("Jellyfin", auth=auth)
    register_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print("\nStarting Jellyfin MCP Server")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Delegation: {'ON' if config['enable_delegation'] else 'OFF'}")
    print(f"  Eunomia: {args.eunomia_type}")

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
    jellyfin_mcp()
