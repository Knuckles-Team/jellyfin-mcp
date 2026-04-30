#!/usr/bin/env python


from typing import Any
from urllib.parse import urljoin

import requests


class Api:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        verify: bool = False,
    ):
        self.base_url = base_url
        self.token = token
        self.username = username
        self.password = password
        self._session = requests.Session()
        self._session.verify = verify
        if token:
            self._session.headers.update({"X-Emby-Token": token})

        try:
            response = self._session.get(urljoin(self.base_url, "/System/Info"))
            if response.status_code == 401:
                from agent_utilities.core.exceptions import AuthError

                raise AuthError(
                    "Jellyfin authentication failed: Invalid token or credentials."
                )
            elif response.status_code == 403:
                from agent_utilities.core.exceptions import UnauthorizedError

                raise UnauthorizedError(
                    "Jellyfin access forbidden: Insufficient permissions."
                )
            response.raise_for_status()
        except Exception as e:
            if isinstance(e, (AuthError, UnauthorizedError)):
                raise e

            pass

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        json_data: dict | None = None,
    ) -> Any:
        url = urljoin(self.base_url, endpoint)
        response = self._session.request(
            method, url, params=params, data=data, json=json_data
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response.text

    def get_log_entries(
        self,
        start_index: int | None = None,
        limit: int | None = None,
        min_date: str | None = None,
        has_user_id: bool | None = None,
    ) -> Any:
        """Gets activity log entries."""
        endpoint = "/System/ActivityLog/Entries"
        params: dict[str, Any] = {}
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if min_date is not None:
            params["minDate"] = min_date
        if has_user_id is not None:
            params["hasUserId"] = has_user_id
        return self.request("GET", endpoint, params=params)

    def get_keys(self) -> Any:
        """Get all keys."""
        endpoint = "/Auth/Keys"
        params = None
        return self.request("GET", endpoint, params=params)

    def create_key(self, app: str | None = None) -> Any:
        """Create a new api key."""
        endpoint = "/Auth/Keys"
        params: dict[str, Any] = {}
        if app is not None:
            params["app"] = app
        return self.request("POST", endpoint, params=params)

    def revoke_key(self, key: str) -> Any:
        """Remove an api key."""
        endpoint = "/Auth/Keys/{key}"
        endpoint = endpoint.replace("{key}", str(key))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_artists(
        self,
        min_community_rating: float | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        search_term: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        filters: list[Any] | None = None,
        is_favorite: bool | None = None,
        media_types: list[Any] | None = None,
        genres: list[Any] | None = None,
        genre_ids: list[Any] | None = None,
        official_ratings: list[Any] | None = None,
        tags: list[Any] | None = None,
        years: list[Any] | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        person: str | None = None,
        person_ids: list[Any] | None = None,
        person_types: list[Any] | None = None,
        studios: list[Any] | None = None,
        studio_ids: list[Any] | None = None,
        user_id: str | None = None,
        name_starts_with_or_greater: str | None = None,
        name_starts_with: str | None = None,
        name_less_than: str | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets all artists from a given item, folder, or the entire library."""
        endpoint = "/Artists"
        params: dict[str, Any] = {}
        if min_community_rating is not None:
            params["minCommunityRating"] = min_community_rating
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if search_term is not None:
            params["searchTerm"] = search_term
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if filters is not None:
            params["filters"] = filters
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if media_types is not None:
            params["mediaTypes"] = media_types
        if genres is not None:
            params["genres"] = genres
        if genre_ids is not None:
            params["genreIds"] = genre_ids
        if official_ratings is not None:
            params["officialRatings"] = official_ratings
        if tags is not None:
            params["tags"] = tags
        if years is not None:
            params["years"] = years
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if person is not None:
            params["person"] = person
        if person_ids is not None:
            params["personIds"] = person_ids
        if person_types is not None:
            params["personTypes"] = person_types
        if studios is not None:
            params["studios"] = studios
        if studio_ids is not None:
            params["studioIds"] = studio_ids
        if user_id is not None:
            params["userId"] = user_id
        if name_starts_with_or_greater is not None:
            params["nameStartsWithOrGreater"] = name_starts_with_or_greater
        if name_starts_with is not None:
            params["nameStartsWith"] = name_starts_with
        if name_less_than is not None:
            params["nameLessThan"] = name_less_than
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_artist_by_name(self, name: str, user_id: str | None = None) -> Any:
        """Gets an artist by name."""
        endpoint = "/Artists/{name}"
        endpoint = endpoint.replace("{name}", str(name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_album_artists(
        self,
        min_community_rating: float | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        search_term: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        filters: list[Any] | None = None,
        is_favorite: bool | None = None,
        media_types: list[Any] | None = None,
        genres: list[Any] | None = None,
        genre_ids: list[Any] | None = None,
        official_ratings: list[Any] | None = None,
        tags: list[Any] | None = None,
        years: list[Any] | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        person: str | None = None,
        person_ids: list[Any] | None = None,
        person_types: list[Any] | None = None,
        studios: list[Any] | None = None,
        studio_ids: list[Any] | None = None,
        user_id: str | None = None,
        name_starts_with_or_greater: str | None = None,
        name_starts_with: str | None = None,
        name_less_than: str | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets all album artists from a given item, folder, or the entire library."""
        endpoint = "/Artists/AlbumArtists"
        params: dict[str, Any] = {}
        if min_community_rating is not None:
            params["minCommunityRating"] = min_community_rating
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if search_term is not None:
            params["searchTerm"] = search_term
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if filters is not None:
            params["filters"] = filters
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if media_types is not None:
            params["mediaTypes"] = media_types
        if genres is not None:
            params["genres"] = genres
        if genre_ids is not None:
            params["genreIds"] = genre_ids
        if official_ratings is not None:
            params["officialRatings"] = official_ratings
        if tags is not None:
            params["tags"] = tags
        if years is not None:
            params["years"] = years
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if person is not None:
            params["person"] = person
        if person_ids is not None:
            params["personIds"] = person_ids
        if person_types is not None:
            params["personTypes"] = person_types
        if studios is not None:
            params["studios"] = studios
        if studio_ids is not None:
            params["studioIds"] = studio_ids
        if user_id is not None:
            params["userId"] = user_id
        if name_starts_with_or_greater is not None:
            params["nameStartsWithOrGreater"] = name_starts_with_or_greater
        if name_starts_with is not None:
            params["nameStartsWith"] = name_starts_with
        if name_less_than is not None:
            params["nameLessThan"] = name_less_than
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_audio_stream(
        self,
        item_id: str,
        container: str | None = None,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
    ) -> Any:
        """Gets an audio stream."""
        endpoint = "/Audio/{itemId}/stream"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}  # type: ignore
        if container is not None:
            params["container"] = container  # type: ignore
        if static is not None:
            params["static"] = static  # type: ignore
        if stream_params is not None:
            params["params"] = stream_params  # type: ignore
        if tag is not None:
            params["tag"] = tag  # type: ignore
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        return self.request("GET", endpoint, params=params)

    def get_audio_stream_by_container(
        self,
        item_id: str,
        container: str,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
    ) -> Any:
        """Gets an audio stream."""
        endpoint = "/Audio/{itemId}/stream.{container}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{container}", str(container))
        params: dict[str, Any] = {}
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        return self.request("GET", endpoint, params=params)

    def list_backups(self) -> Any:
        """Gets a list of all currently present backups in the backup directory."""
        endpoint = "/Backup"
        params = None
        return self.request("GET", endpoint, params=params)

    def create_backup(self, body: dict[str, Any] | None = None) -> Any:
        """Creates a new Backup."""
        endpoint = "/Backup/Create"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_backup(self, path: str | None = None) -> Any:
        """Gets the descriptor from an existing archive is present."""
        endpoint = "/Backup/Manifest"
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", endpoint, params=params)

    def start_restore_backup(self, body: dict[str, Any] | None = None) -> Any:
        """Restores to a backup by restarting the server and applying the backup."""
        endpoint = "/Backup/Restore"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_branding_options(self) -> Any:
        """Gets branding configuration."""
        endpoint = "/Branding/Configuration"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_branding_css(self) -> Any:
        """Gets branding css."""
        endpoint = "/Branding/Css"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_branding_css_2(self) -> Any:
        """Gets branding css."""
        endpoint = "/Branding/Css.css"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_channels(
        self,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        supports_latest_items: bool | None = None,
        supports_media_deletion: bool | None = None,
        is_favorite: bool | None = None,
    ) -> Any:
        """Gets available channels."""
        endpoint = "/Channels"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if supports_latest_items is not None:
            params["supportsLatestItems"] = supports_latest_items
        if supports_media_deletion is not None:
            params["supportsMediaDeletion"] = supports_media_deletion
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        return self.request("GET", endpoint, params=params)

    def get_channel_features(self, channel_id: str) -> Any:
        """Get channel features."""
        endpoint = "/Channels/{channelId}/Features"
        endpoint = endpoint.replace("{channelId}", str(channel_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_channel_items(
        self,
        channel_id: str,
        folder_id: str | None = None,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        sort_order: list[Any] | None = None,
        filters: list[Any] | None = None,
        sort_by: list[Any] | None = None,
        fields: list[Any] | None = None,
    ) -> Any:
        """Get channel items."""
        endpoint = "/Channels/{channelId}/Items"
        endpoint = endpoint.replace("{channelId}", str(channel_id))
        params: dict[str, Any] = {}
        if folder_id is not None:
            params["folderId"] = folder_id
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if filters is not None:
            params["filters"] = filters
        if sort_by is not None:
            params["sortBy"] = sort_by
        if fields is not None:
            params["fields"] = fields
        return self.request("GET", endpoint, params=params)

    def get_all_channel_features(self) -> Any:
        """Get all channel features."""
        endpoint = "/Channels/Features"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_latest_channel_items(
        self,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        filters: list[Any] | None = None,
        fields: list[Any] | None = None,
        channel_ids: list[Any] | None = None,
    ) -> Any:
        """Gets latest channel items."""
        endpoint = "/Channels/Items/Latest"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if filters is not None:
            params["filters"] = filters
        if fields is not None:
            params["fields"] = fields
        if channel_ids is not None:
            params["channelIds"] = channel_ids
        return self.request("GET", endpoint, params=params)

    def log_file(self, body: dict[str, Any] | None = None) -> Any:
        """Upload a document."""
        endpoint = "/ClientLog/Document"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def create_collection(
        self,
        name: str | None = None,
        ids: list[Any] | None = None,
        parent_id: str | None = None,
        is_locked: bool | None = None,
    ) -> Any:
        """Creates a new collection."""
        endpoint = "/Collections"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if ids is not None:
            params["ids"] = ids
        if parent_id is not None:
            params["parentId"] = parent_id
        if is_locked is not None:
            params["isLocked"] = is_locked
        return self.request("POST", endpoint, params=params)

    def add_to_collection(
        self, collection_id: str, ids: list[Any] | None = None
    ) -> Any:
        """Adds items to a collection."""
        endpoint = "/Collections/{collectionId}/Items"
        endpoint = endpoint.replace("{collectionId}", str(collection_id))
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        return self.request("POST", endpoint, params=params)

    def remove_from_collection(
        self, collection_id: str, ids: list[Any] | None = None
    ) -> Any:
        """Removes items from a collection."""
        endpoint = "/Collections/{collectionId}/Items"
        endpoint = endpoint.replace("{collectionId}", str(collection_id))
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        return self.request("DELETE", endpoint, params=params)

    def get_configuration(self) -> Any:
        """Gets application configuration."""
        endpoint = "/System/Configuration"
        params = None
        return self.request("GET", endpoint, params=params)

    def update_configuration(self, body: dict[str, Any] | None = None) -> Any:
        """Updates application configuration."""
        endpoint = "/System/Configuration"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_named_configuration(self, key: str) -> Any:
        """Gets a named configuration."""
        endpoint = "/System/Configuration/{key}"
        endpoint = endpoint.replace("{key}", str(key))
        params = None
        return self.request("GET", endpoint, params=params)

    def update_named_configuration(
        self, key: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates named configuration."""
        endpoint = "/System/Configuration/{key}"
        endpoint = endpoint.replace("{key}", str(key))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def update_branding_configuration(self, body: dict[str, Any] | None = None) -> Any:
        """Updates branding configuration."""
        endpoint = "/System/Configuration/Branding"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_default_metadata_options(self) -> Any:
        """Gets a default MetadataOptions object."""
        endpoint = "/System/Configuration/MetadataOptions/Default"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_dashboard_configuration_page(self, name: str | None = None) -> Any:
        """Gets a dashboard configuration page."""
        endpoint = "/web/ConfigurationPage"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        return self.request("GET", endpoint, params=params)

    def get_configuration_pages(self, enable_in_main_menu: bool | None = None) -> Any:
        """Gets the configuration pages."""
        endpoint = "/web/ConfigurationPages"
        params: dict[str, Any] = {}
        if enable_in_main_menu is not None:
            params["enableInMainMenu"] = enable_in_main_menu
        return self.request("GET", endpoint, params=params)

    def get_devices(self, user_id: str | None = None) -> Any:
        """Get Devices."""
        endpoint = "/Devices"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def delete_device(self, id: str | None = None) -> Any:
        """Deletes a device."""
        endpoint = "/Devices"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        return self.request("DELETE", endpoint, params=params)

    def get_device_info(self, id: str | None = None) -> Any:
        """Get info for a device."""
        endpoint = "/Devices/Info"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        return self.request("GET", endpoint, params=params)

    def get_device_options(self, id: str | None = None) -> Any:
        """Get options for a device."""
        endpoint = "/Devices/Options"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        return self.request("GET", endpoint, params=params)

    def update_device_options(
        self, id: str | None = None, body: dict[str, Any] | None = None
    ) -> Any:
        """Update device options."""
        endpoint = "/Devices/Options"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_display_preferences(
        self,
        display_preferences_id: str,
        user_id: str | None = None,
        client: str | None = None,
    ) -> Any:
        """Get Display Preferences."""
        endpoint = "/DisplayPreferences/{displayPreferencesId}"
        endpoint = endpoint.replace(
            "{displayPreferencesId}", str(display_preferences_id)
        )
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if client is not None:
            params["client"] = client
        return self.request("GET", endpoint, params=params)

    def update_display_preferences(
        self,
        display_preferences_id: str,
        user_id: str | None = None,
        client: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update Display Preferences."""
        endpoint = "/DisplayPreferences/{displayPreferencesId}"
        endpoint = endpoint.replace(
            "{displayPreferencesId}", str(display_preferences_id)
        )
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if client is not None:
            params["client"] = client
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_hls_audio_segment(
        self,
        item_id: str,
        playlist_id: str,
        segment_id: int,
        container: str,
        runtime_ticks: int | None = None,
        actual_segment_length_ticks: int | None = None,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        max_streaming_bitrate: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
    ) -> Any:
        """Gets a video stream using HTTP live streaming."""
        endpoint = "/Audio/{itemId}/hls1/{playlistId}/{segmentId}.{container}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        endpoint = endpoint.replace("{segmentId}", str(segment_id))
        endpoint = endpoint.replace("{container}", str(container))
        params: dict[str, Any] = {}
        if runtime_ticks is not None:
            params["runtimeTicks"] = runtime_ticks
        if actual_segment_length_ticks is not None:
            params["actualSegmentLengthTicks"] = actual_segment_length_ticks
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if max_streaming_bitrate is not None:
            params["maxStreamingBitrate"] = max_streaming_bitrate
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        return self.request("GET", endpoint, params=params)

    def get_variant_hls_audio_playlist(
        self,
        item_id: str,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        max_streaming_bitrate: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
    ) -> Any:
        """Gets an audio stream using HTTP live streaming."""
        endpoint = "/Audio/{itemId}/main.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if max_streaming_bitrate is not None:
            params["maxStreamingBitrate"] = max_streaming_bitrate
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        return self.request("GET", endpoint, params=params)

    def get_master_hls_audio_playlist(
        self,
        item_id: str,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        max_streaming_bitrate: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_adaptive_bitrate_streaming: bool | None = None,
        enable_audio_vbr_encoding: bool | None = None,
    ) -> Any:
        """Gets an audio hls playlist stream."""
        endpoint = "/Audio/{itemId}/master.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if max_streaming_bitrate is not None:
            params["maxStreamingBitrate"] = max_streaming_bitrate
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_adaptive_bitrate_streaming is not None:
            params["enableAdaptiveBitrateStreaming"] = enable_adaptive_bitrate_streaming
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        return self.request("GET", endpoint, params=params)

    def get_hls_video_segment(
        self,
        item_id: str,
        playlist_id: str,
        segment_id: int,
        container: str,
        runtime_ticks: int | None = None,
        actual_segment_length_ticks: int | None = None,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
        always_burn_in_subtitle_when_transcoding: bool | None = None,
    ) -> Any:
        """Gets a video stream using HTTP live streaming."""
        endpoint = "/Videos/{itemId}/hls1/{playlistId}/{segmentId}.{container}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        endpoint = endpoint.replace("{segmentId}", str(segment_id))
        endpoint = endpoint.replace("{container}", str(container))
        params: dict[str, Any] = {}
        if runtime_ticks is not None:
            params["runtimeTicks"] = runtime_ticks
        if actual_segment_length_ticks is not None:
            params["actualSegmentLengthTicks"] = actual_segment_length_ticks
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        if always_burn_in_subtitle_when_transcoding is not None:
            params["alwaysBurnInSubtitleWhenTranscoding"] = (
                always_burn_in_subtitle_when_transcoding
            )
        return self.request("GET", endpoint, params=params)

    def get_live_hls_stream(
        self,
        item_id: str,
        container: str | None = None,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        enable_subtitles_in_manifest: bool | None = None,
        enable_audio_vbr_encoding: bool | None = None,
        always_burn_in_subtitle_when_transcoding: bool | None = None,
    ) -> Any:
        """Gets a hls live stream."""
        endpoint = "/Videos/{itemId}/live.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if container is not None:
            params["container"] = container
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if enable_subtitles_in_manifest is not None:
            params["enableSubtitlesInManifest"] = enable_subtitles_in_manifest
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        if always_burn_in_subtitle_when_transcoding is not None:
            params["alwaysBurnInSubtitleWhenTranscoding"] = (
                always_burn_in_subtitle_when_transcoding
            )
        return self.request("GET", endpoint, params=params)

    def get_variant_hls_video_playlist(
        self,
        item_id: str,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
        always_burn_in_subtitle_when_transcoding: bool | None = None,
    ) -> Any:
        """Gets a video stream using HTTP live streaming."""
        endpoint = "/Videos/{itemId}/main.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        if always_burn_in_subtitle_when_transcoding is not None:
            params["alwaysBurnInSubtitleWhenTranscoding"] = (
                always_burn_in_subtitle_when_transcoding
            )
        return self.request("GET", endpoint, params=params)

    def get_master_hls_video_playlist(
        self,
        item_id: str,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_adaptive_bitrate_streaming: bool | None = None,
        enable_trickplay: bool | None = None,
        enable_audio_vbr_encoding: bool | None = None,
        always_burn_in_subtitle_when_transcoding: bool | None = None,
    ) -> Any:
        """Gets a video hls playlist stream."""
        endpoint = "/Videos/{itemId}/master.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_adaptive_bitrate_streaming is not None:
            params["enableAdaptiveBitrateStreaming"] = enable_adaptive_bitrate_streaming
        if enable_trickplay is not None:
            params["enableTrickplay"] = enable_trickplay
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        if always_burn_in_subtitle_when_transcoding is not None:
            params["alwaysBurnInSubtitleWhenTranscoding"] = (
                always_burn_in_subtitle_when_transcoding
            )
        return self.request("GET", endpoint, params=params)

    def get_default_directory_browser(self) -> Any:
        """Get Default directory browser."""
        endpoint = "/Environment/DefaultDirectoryBrowser"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_directory_contents(
        self,
        path: str | None = None,
        include_files: bool | None = None,
        include_directories: bool | None = None,
    ) -> Any:
        """Gets the contents of a given directory in the file system."""
        endpoint = "/Environment/DirectoryContents"
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        if include_files is not None:
            params["includeFiles"] = include_files
        if include_directories is not None:
            params["includeDirectories"] = include_directories
        return self.request("GET", endpoint, params=params)

    def get_drives(self) -> Any:
        """Gets available drives from the server's file system."""
        endpoint = "/Environment/Drives"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_network_shares(self) -> Any:
        """Gets network paths."""
        endpoint = "/Environment/NetworkShares"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_parent_path(self, path: str | None = None) -> Any:
        """Gets the parent path of a given path."""
        endpoint = "/Environment/ParentPath"
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", endpoint, params=params)

    def validate_path(self, body: dict[str, Any] | None = None) -> Any:
        """Validates path."""
        endpoint = "/Environment/ValidatePath"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_query_filters_legacy(
        self,
        user_id: str | None = None,
        parent_id: str | None = None,
        include_item_types: list[Any] | None = None,
        media_types: list[Any] | None = None,
    ) -> Any:
        """Gets legacy query filters."""
        endpoint = "/Items/Filters"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if parent_id is not None:
            params["parentId"] = parent_id
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if media_types is not None:
            params["mediaTypes"] = media_types
        return self.request("GET", endpoint, params=params)

    def get_query_filters(
        self,
        user_id: str | None = None,
        parent_id: str | None = None,
        include_item_types: list[Any] | None = None,
        is_airing: bool | None = None,
        is_movie: bool | None = None,
        is_sports: bool | None = None,
        is_kids: bool | None = None,
        is_news: bool | None = None,
        is_series: bool | None = None,
        recursive: bool | None = None,
    ) -> Any:
        """Gets query filters."""
        endpoint = "/Items/Filters2"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if parent_id is not None:
            params["parentId"] = parent_id
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if is_airing is not None:
            params["isAiring"] = is_airing
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_sports is not None:
            params["isSports"] = is_sports
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_news is not None:
            params["isNews"] = is_news
        if is_series is not None:
            params["isSeries"] = is_series
        if recursive is not None:
            params["recursive"] = recursive
        return self.request("GET", endpoint, params=params)

    def get_genres(
        self,
        start_index: int | None = None,
        limit: int | None = None,
        search_term: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        is_favorite: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        user_id: str | None = None,
        name_starts_with_or_greater: str | None = None,
        name_starts_with: str | None = None,
        name_less_than: str | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets all genres from a given item, folder, or the entire library."""
        endpoint = "/Genres"
        params: dict[str, Any] = {}
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if search_term is not None:
            params["searchTerm"] = search_term
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if user_id is not None:
            params["userId"] = user_id
        if name_starts_with_or_greater is not None:
            params["nameStartsWithOrGreater"] = name_starts_with_or_greater
        if name_starts_with is not None:
            params["nameStartsWith"] = name_starts_with
        if name_less_than is not None:
            params["nameLessThan"] = name_less_than
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_genre(self, genre_name: str, user_id: str | None = None) -> Any:
        """Gets a genre, by name."""
        endpoint = "/Genres/{genreName}"
        endpoint = endpoint.replace("{genreName}", str(genre_name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_hls_audio_segment_legacy_aac(self, item_id: str, segment_id: str) -> Any:
        """Gets the specified audio segment for an audio item."""
        endpoint = "/Audio/{itemId}/hls/{segmentId}/stream.aac"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{segmentId}", str(segment_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_hls_audio_segment_legacy_mp3(self, item_id: str, segment_id: str) -> Any:
        """Gets the specified audio segment for an audio item."""
        endpoint = "/Audio/{itemId}/hls/{segmentId}/stream.mp3"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{segmentId}", str(segment_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_hls_video_segment_legacy(
        self, item_id: str, playlist_id: str, segment_id: str, segment_container: str
    ) -> Any:
        """Gets a hls video segment."""
        endpoint = "/Videos/{itemId}/hls/{playlistId}/{segmentId}.{segmentContainer}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        endpoint = endpoint.replace("{segmentId}", str(segment_id))
        endpoint = endpoint.replace("{segmentContainer}", str(segment_container))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_hls_playlist_legacy(self, item_id: str, playlist_id: str) -> Any:
        """Gets a hls video playlist."""
        endpoint = "/Videos/{itemId}/hls/{playlistId}/stream.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def stop_encoding_process(
        self, device_id: str | None = None, play_session_id: str | None = None
    ) -> Any:
        """Stops an active encoding."""
        endpoint = "/Videos/ActiveEncodings"
        params: dict[str, Any] = {}
        if device_id is not None:
            params["deviceId"] = device_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        return self.request("DELETE", endpoint, params=params)

    def get_artist_image(
        self,
        name: str,
        image_type: str,
        image_index: int,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
    ) -> Any:
        """Get artist image by name."""
        endpoint = "/Artists/{name}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        return self.request("GET", endpoint, params=params)

    def get_splashscreen(
        self, tag: str | None = None, format: str | None = None
    ) -> Any:
        """Generates or gets the splashscreen."""
        endpoint = "/Branding/Splashscreen"
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        return self.request("GET", endpoint, params=params)

    def upload_custom_splashscreen(self, body: dict[str, Any] | None = None) -> Any:
        """Uploads a custom splashscreen.
        The body is expected to the image contents base64 encoded."""
        endpoint = "/Branding/Splashscreen"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def delete_custom_splashscreen(self) -> Any:
        """Delete a custom splashscreen."""
        endpoint = "/Branding/Splashscreen"
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_genre_image(
        self,
        name: str,
        image_type: str,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
        image_index: int | None = None,
    ) -> Any:
        """Get genre image by name."""
        endpoint = "/Genres/{name}/Images/{imageType}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        if image_index is not None:
            params["imageIndex"] = image_index
        return self.request("GET", endpoint, params=params)

    def get_genre_image_by_index(
        self,
        name: str,
        image_type: str,
        image_index: int,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
    ) -> Any:
        """Get genre image by name."""
        endpoint = "/Genres/{name}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        return self.request("GET", endpoint, params=params)

    def get_item_image_infos(self, item_id: str) -> Any:
        """Get item image infos."""
        endpoint = "/Items/{itemId}/Images"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def delete_item_image(
        self, item_id: str, image_type: str, image_index: int | None = None
    ) -> Any:
        """Delete an item's image."""
        endpoint = "/Items/{itemId}/Images/{imageType}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        params: dict[str, Any] = {}
        if image_index is not None:
            params["imageIndex"] = image_index
        return self.request("DELETE", endpoint, params=params)

    def set_item_image(
        self, item_id: str, image_type: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Set item image."""
        endpoint = "/Items/{itemId}/Images/{imageType}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_item_image(
        self,
        item_id: str,
        image_type: str,
        max_width: int | None = None,
        max_height: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        tag: str | None = None,
        format: str | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
        image_index: int | None = None,
    ) -> Any:
        """Gets the item's image."""
        endpoint = "/Items/{itemId}/Images/{imageType}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        params: dict[str, Any] = {}
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        if image_index is not None:
            params["imageIndex"] = image_index
        return self.request("GET", endpoint, params=params)

    def delete_item_image_by_index(
        self, item_id: str, image_type: str, image_index: int
    ) -> Any:
        """Delete an item's image."""
        endpoint = "/Items/{itemId}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def set_item_image_by_index(
        self,
        item_id: str,
        image_type: str,
        image_index: int,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Set item image."""
        endpoint = "/Items/{itemId}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_item_image_by_index(
        self,
        item_id: str,
        image_type: str,
        image_index: int,
        max_width: int | None = None,
        max_height: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        tag: str | None = None,
        format: str | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
    ) -> Any:
        """Gets the item's image."""
        endpoint = "/Items/{itemId}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        return self.request("GET", endpoint, params=params)

    def get_item_image2(
        self,
        item_id: str,
        image_type: str,
        max_width: int,
        max_height: int,
        tag: str,
        format: str,
        percent_played: float,
        unplayed_count: int,
        image_index: int,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
    ) -> Any:
        """Gets the item's image."""
        endpoint = "/Items/{itemId}/Images/{imageType}/{imageIndex}/{tag}/{format}/{maxWidth}/{maxHeight}/{percentPlayed}/{unplayedCount}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{maxWidth}", str(max_width))
        endpoint = endpoint.replace("{maxHeight}", str(max_height))
        endpoint = endpoint.replace("{tag}", str(tag))
        endpoint = endpoint.replace("{format}", str(format))
        endpoint = endpoint.replace("{percentPlayed}", str(percent_played))
        endpoint = endpoint.replace("{unplayedCount}", str(unplayed_count))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        return self.request("GET", endpoint, params=params)

    def update_item_image_index(
        self,
        item_id: str,
        image_type: str,
        image_index: int,
        new_index: int | None = None,
    ) -> Any:
        """Updates the index for an item image."""
        endpoint = "/Items/{itemId}/Images/{imageType}/{imageIndex}/Index"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if new_index is not None:
            params["newIndex"] = new_index
        return self.request("POST", endpoint, params=params)

    def get_music_genre_image(
        self,
        name: str,
        image_type: str,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
        image_index: int | None = None,
    ) -> Any:
        """Get music genre image by name."""
        endpoint = "/MusicGenres/{name}/Images/{imageType}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        if image_index is not None:
            params["imageIndex"] = image_index
        return self.request("GET", endpoint, params=params)

    def get_music_genre_image_by_index(
        self,
        name: str,
        image_type: str,
        image_index: int,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
    ) -> Any:
        """Get music genre image by name."""
        endpoint = "/MusicGenres/{name}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        return self.request("GET", endpoint, params=params)

    def get_person_image(
        self,
        name: str,
        image_type: str,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
        image_index: int | None = None,
    ) -> Any:
        """Get person image by name."""
        endpoint = "/Persons/{name}/Images/{imageType}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        if image_index is not None:
            params["imageIndex"] = image_index
        return self.request("GET", endpoint, params=params)

    def get_person_image_by_index(
        self,
        name: str,
        image_type: str,
        image_index: int,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
    ) -> Any:
        """Get person image by name."""
        endpoint = "/Persons/{name}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        return self.request("GET", endpoint, params=params)

    def get_studio_image(
        self,
        name: str,
        image_type: str,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
        image_index: int | None = None,
    ) -> Any:
        """Get studio image by name."""
        endpoint = "/Studios/{name}/Images/{imageType}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        if image_index is not None:
            params["imageIndex"] = image_index
        return self.request("GET", endpoint, params=params)

    def get_studio_image_by_index(
        self,
        name: str,
        image_type: str,
        image_index: int,
        tag: str | None = None,
        format: str | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        percent_played: float | None = None,
        unplayed_count: int | None = None,
        width: int | None = None,
        height: int | None = None,
        quality: int | None = None,
        fill_width: int | None = None,
        fill_height: int | None = None,
        blur: int | None = None,
        background_color: str | None = None,
        foreground_layer: str | None = None,
    ) -> Any:
        """Get studio image by name."""
        endpoint = "/Studios/{name}/Images/{imageType}/{imageIndex}"
        endpoint = endpoint.replace("{name}", str(name))
        endpoint = endpoint.replace("{imageType}", str(image_type))
        endpoint = endpoint.replace("{imageIndex}", str(image_index))
        params: dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if percent_played is not None:
            params["percentPlayed"] = percent_played
        if unplayed_count is not None:
            params["unplayedCount"] = unplayed_count
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if quality is not None:
            params["quality"] = quality
        if fill_width is not None:
            params["fillWidth"] = fill_width
        if fill_height is not None:
            params["fillHeight"] = fill_height
        if blur is not None:
            params["blur"] = blur
        if background_color is not None:
            params["backgroundColor"] = background_color
        if foreground_layer is not None:
            params["foregroundLayer"] = foreground_layer
        return self.request("GET", endpoint, params=params)

    def post_user_image(
        self, user_id: str | None = None, body: dict[str, Any] | None = None
    ) -> Any:
        """Sets the user image."""
        endpoint = "/UserImage"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params, json_data=body)

    def delete_user_image(self, user_id: str | None = None) -> Any:
        """Delete the user's image."""
        endpoint = "/UserImage"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("DELETE", endpoint, params=params)

    def get_user_image(
        self,
        user_id: str | None = None,
        tag: str | None = None,
        format: str | None = None,
    ) -> Any:
        """Get user profile image."""
        endpoint = "/UserImage"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if tag is not None:
            params["tag"] = tag
        if format is not None:
            params["format"] = format
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_album(
        self,
        item_id: str,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given album."""
        endpoint = "/Albums/{itemId}/InstantMix"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_artists(
        self,
        item_id: str,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given artist."""
        endpoint = "/Artists/{itemId}/InstantMix"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_artists2(
        self,
        id: str | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given artist."""
        endpoint = "/Artists/InstantMix"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_item(
        self,
        item_id: str,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given item."""
        endpoint = "/Items/{itemId}/InstantMix"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_music_genre_by_name(
        self,
        name: str,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given genre."""
        endpoint = "/MusicGenres/{name}/InstantMix"
        endpoint = endpoint.replace("{name}", str(name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_music_genre_by_id(
        self,
        id: str | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given genre."""
        endpoint = "/MusicGenres/InstantMix"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_playlist(
        self,
        item_id: str,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given playlist."""
        endpoint = "/Playlists/{itemId}/InstantMix"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_instant_mix_from_song(
        self,
        item_id: str,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Creates an instant playlist based on a given song."""
        endpoint = "/Songs/{itemId}/InstantMix"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def get_external_id_infos(self, item_id: str) -> Any:
        """Get the item's external id info."""
        endpoint = "/Items/{itemId}/ExternalIdInfos"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def apply_search_criteria(
        self,
        item_id: str,
        replace_all_images: bool | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Applies search criteria to an item and refreshes metadata."""
        endpoint = "/Items/RemoteSearch/Apply/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if replace_all_images is not None:
            params["replaceAllImages"] = replace_all_images
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_book_remote_search_results(self, body: dict[str, Any] | None = None) -> Any:
        """Get book remote search."""
        endpoint = "/Items/RemoteSearch/Book"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_box_set_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get box set remote search."""
        endpoint = "/Items/RemoteSearch/BoxSet"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_movie_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get movie remote search."""
        endpoint = "/Items/RemoteSearch/Movie"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_music_album_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get music album remote search."""
        endpoint = "/Items/RemoteSearch/MusicAlbum"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_music_artist_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get music artist remote search."""
        endpoint = "/Items/RemoteSearch/MusicArtist"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_music_video_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get music video remote search."""
        endpoint = "/Items/RemoteSearch/MusicVideo"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_person_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get person remote search."""
        endpoint = "/Items/RemoteSearch/Person"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_series_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get series remote search."""
        endpoint = "/Items/RemoteSearch/Series"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_trailer_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get trailer remote search."""
        endpoint = "/Items/RemoteSearch/Trailer"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def refresh_item(
        self,
        item_id: str,
        metadata_refresh_mode: str | None = None,
        image_refresh_mode: str | None = None,
        replace_all_metadata: bool | None = None,
        replace_all_images: bool | None = None,
        regenerate_trickplay: bool | None = None,
    ) -> Any:
        """Refreshes metadata for an item."""
        endpoint = "/Items/{itemId}/Refresh"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if metadata_refresh_mode is not None:
            params["metadataRefreshMode"] = metadata_refresh_mode
        if image_refresh_mode is not None:
            params["imageRefreshMode"] = image_refresh_mode
        if replace_all_metadata is not None:
            params["replaceAllMetadata"] = replace_all_metadata
        if replace_all_images is not None:
            params["replaceAllImages"] = replace_all_images
        if regenerate_trickplay is not None:
            params["regenerateTrickplay"] = regenerate_trickplay
        return self.request("POST", endpoint, params=params)

    def get_items(
        self,
        user_id: str | None = None,
        max_official_rating: str | None = None,
        has_theme_song: bool | None = None,
        has_theme_video: bool | None = None,
        has_subtitles: bool | None = None,
        has_special_feature: bool | None = None,
        has_trailer: bool | None = None,
        adjacent_to: str | None = None,
        index_number: int | None = None,
        parent_index_number: int | None = None,
        has_parental_rating: bool | None = None,
        is_hd: bool | None = None,
        is4_k: bool | None = None,
        location_types: list[Any] | None = None,
        exclude_location_types: list[Any] | None = None,
        is_missing: bool | None = None,
        is_unaired: bool | None = None,
        min_community_rating: float | None = None,
        min_critic_rating: float | None = None,
        min_premiere_date: str | None = None,
        min_date_last_saved: str | None = None,
        min_date_last_saved_for_user: str | None = None,
        max_premiere_date: str | None = None,
        has_overview: bool | None = None,
        has_imdb_id: bool | None = None,
        has_tmdb_id: bool | None = None,
        has_tvdb_id: bool | None = None,
        is_movie: bool | None = None,
        is_series: bool | None = None,
        is_news: bool | None = None,
        is_kids: bool | None = None,
        is_sports: bool | None = None,
        exclude_item_ids: list[Any] | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        recursive: bool | None = None,
        search_term: str | None = None,
        sort_order: list[Any] | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        filters: list[Any] | None = None,
        is_favorite: bool | None = None,
        media_types: list[Any] | None = None,
        image_types: list[Any] | None = None,
        sort_by: list[Any] | None = None,
        is_played: bool | None = None,
        genres: list[Any] | None = None,
        official_ratings: list[Any] | None = None,
        tags: list[Any] | None = None,
        years: list[Any] | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        person: str | None = None,
        person_ids: list[Any] | None = None,
        person_types: list[Any] | None = None,
        studios: list[Any] | None = None,
        artists: list[Any] | None = None,
        exclude_artist_ids: list[Any] | None = None,
        artist_ids: list[Any] | None = None,
        album_artist_ids: list[Any] | None = None,
        contributing_artist_ids: list[Any] | None = None,
        albums: list[Any] | None = None,
        album_ids: list[Any] | None = None,
        ids: list[Any] | None = None,
        video_types: list[Any] | None = None,
        min_official_rating: str | None = None,
        is_locked: bool | None = None,
        is_place_holder: bool | None = None,
        has_official_rating: bool | None = None,
        collapse_box_set_items: bool | None = None,
        min_width: int | None = None,
        min_height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        is3_d: bool | None = None,
        series_status: list[Any] | None = None,
        name_starts_with_or_greater: str | None = None,
        name_starts_with: str | None = None,
        name_less_than: str | None = None,
        studio_ids: list[Any] | None = None,
        genre_ids: list[Any] | None = None,
        enable_total_record_count: bool | None = None,
        enable_images: bool | None = None,
    ) -> Any:
        """Gets items based on a query."""
        endpoint = "/Items"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if max_official_rating is not None:
            params["maxOfficialRating"] = max_official_rating
        if has_theme_song is not None:
            params["hasThemeSong"] = has_theme_song
        if has_theme_video is not None:
            params["hasThemeVideo"] = has_theme_video
        if has_subtitles is not None:
            params["hasSubtitles"] = has_subtitles
        if has_special_feature is not None:
            params["hasSpecialFeature"] = has_special_feature
        if has_trailer is not None:
            params["hasTrailer"] = has_trailer
        if adjacent_to is not None:
            params["adjacentTo"] = adjacent_to
        if index_number is not None:
            params["indexNumber"] = index_number
        if parent_index_number is not None:
            params["parentIndexNumber"] = parent_index_number
        if has_parental_rating is not None:
            params["hasParentalRating"] = has_parental_rating
        if is_hd is not None:
            params["isHd"] = is_hd
        if is4_k is not None:
            params["is4K"] = is4_k
        if location_types is not None:
            params["locationTypes"] = location_types
        if exclude_location_types is not None:
            params["excludeLocationTypes"] = exclude_location_types
        if is_missing is not None:
            params["isMissing"] = is_missing
        if is_unaired is not None:
            params["isUnaired"] = is_unaired
        if min_community_rating is not None:
            params["minCommunityRating"] = min_community_rating
        if min_critic_rating is not None:
            params["minCriticRating"] = min_critic_rating
        if min_premiere_date is not None:
            params["minPremiereDate"] = min_premiere_date
        if min_date_last_saved is not None:
            params["minDateLastSaved"] = min_date_last_saved
        if min_date_last_saved_for_user is not None:
            params["minDateLastSavedForUser"] = min_date_last_saved_for_user
        if max_premiere_date is not None:
            params["maxPremiereDate"] = max_premiere_date
        if has_overview is not None:
            params["hasOverview"] = has_overview
        if has_imdb_id is not None:
            params["hasImdbId"] = has_imdb_id
        if has_tmdb_id is not None:
            params["hasTmdbId"] = has_tmdb_id
        if has_tvdb_id is not None:
            params["hasTvdbId"] = has_tvdb_id
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_series is not None:
            params["isSeries"] = is_series
        if is_news is not None:
            params["isNews"] = is_news
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_sports is not None:
            params["isSports"] = is_sports
        if exclude_item_ids is not None:
            params["excludeItemIds"] = exclude_item_ids
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if recursive is not None:
            params["recursive"] = recursive
        if search_term is not None:
            params["searchTerm"] = search_term
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if filters is not None:
            params["filters"] = filters
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if media_types is not None:
            params["mediaTypes"] = media_types
        if image_types is not None:
            params["imageTypes"] = image_types
        if sort_by is not None:
            params["sortBy"] = sort_by
        if is_played is not None:
            params["isPlayed"] = is_played
        if genres is not None:
            params["genres"] = genres
        if official_ratings is not None:
            params["officialRatings"] = official_ratings
        if tags is not None:
            params["tags"] = tags
        if years is not None:
            params["years"] = years
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if person is not None:
            params["person"] = person
        if person_ids is not None:
            params["personIds"] = person_ids
        if person_types is not None:
            params["personTypes"] = person_types
        if studios is not None:
            params["studios"] = studios
        if artists is not None:
            params["artists"] = artists
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if artist_ids is not None:
            params["artistIds"] = artist_ids
        if album_artist_ids is not None:
            params["albumArtistIds"] = album_artist_ids
        if contributing_artist_ids is not None:
            params["contributingArtistIds"] = contributing_artist_ids
        if albums is not None:
            params["albums"] = albums
        if album_ids is not None:
            params["albumIds"] = album_ids
        if ids is not None:
            params["ids"] = ids
        if video_types is not None:
            params["videoTypes"] = video_types
        if min_official_rating is not None:
            params["minOfficialRating"] = min_official_rating
        if is_locked is not None:
            params["isLocked"] = is_locked
        if is_place_holder is not None:
            params["isPlaceHolder"] = is_place_holder
        if has_official_rating is not None:
            params["hasOfficialRating"] = has_official_rating
        if collapse_box_set_items is not None:
            params["collapseBoxSetItems"] = collapse_box_set_items
        if min_width is not None:
            params["minWidth"] = min_width
        if min_height is not None:
            params["minHeight"] = min_height
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if is3_d is not None:
            params["is3D"] = is3_d
        if series_status is not None:
            params["seriesStatus"] = series_status
        if name_starts_with_or_greater is not None:
            params["nameStartsWithOrGreater"] = name_starts_with_or_greater
        if name_starts_with is not None:
            params["nameStartsWith"] = name_starts_with
        if name_less_than is not None:
            params["nameLessThan"] = name_less_than
        if studio_ids is not None:
            params["studioIds"] = studio_ids
        if genre_ids is not None:
            params["genreIds"] = genre_ids
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        if enable_images is not None:
            params["enableImages"] = enable_images
        return self.request("GET", endpoint, params=params)

    def delete_items(self, ids: list[Any] | None = None) -> Any:
        """Deletes items from the library and filesystem."""
        endpoint = "/Items"
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        return self.request("DELETE", endpoint, params=params)

    def get_item_user_data(self, item_id: str, user_id: str | None = None) -> Any:
        """Get Item User Data."""
        endpoint = "/UserItems/{itemId}/UserData"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def update_item_user_data(
        self,
        item_id: str,
        user_id: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update Item User Data."""
        endpoint = "/UserItems/{itemId}/UserData"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_resume_items(
        self,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        search_term: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        media_types: list[Any] | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        enable_total_record_count: bool | None = None,
        enable_images: bool | None = None,
        exclude_active_sessions: bool | None = None,
    ) -> Any:
        """Gets items based on a query."""
        endpoint = "/UserItems/Resume"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if search_term is not None:
            params["searchTerm"] = search_term
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if media_types is not None:
            params["mediaTypes"] = media_types
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        if enable_images is not None:
            params["enableImages"] = enable_images
        if exclude_active_sessions is not None:
            params["excludeActiveSessions"] = exclude_active_sessions
        return self.request("GET", endpoint, params=params)

    def update_item(self, item_id: str, body: dict[str, Any] | None = None) -> Any:
        """Updates an item."""
        endpoint = "/Items/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def delete_item(self, item_id: str) -> Any:
        """Deletes an item from the library and filesystem."""
        endpoint = "/Items/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_item(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets an item from a user's library."""
        endpoint = "/Items/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def update_item_content_type(
        self, item_id: str, content_type: str | None = None
    ) -> Any:
        """Updates an item's content type."""
        endpoint = "/Items/{itemId}/ContentType"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if content_type is not None:
            params["contentType"] = content_type
        return self.request("POST", endpoint, params=params)

    def get_metadata_editor_info(self, item_id: str) -> Any:
        """Gets metadata editor info for an item."""
        endpoint = "/Items/{itemId}/MetadataEditor"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_similar_albums(
        self,
        item_id: str,
        exclude_artist_ids: list[Any] | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
    ) -> Any:
        """Gets similar items."""
        endpoint = "/Albums/{itemId}/Similar"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        return self.request("GET", endpoint, params=params)

    def get_similar_artists(
        self,
        item_id: str,
        exclude_artist_ids: list[Any] | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
    ) -> Any:
        """Gets similar items."""
        endpoint = "/Artists/{itemId}/Similar"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        return self.request("GET", endpoint, params=params)

    def get_ancestors(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets all parents of an item."""
        endpoint = "/Items/{itemId}/Ancestors"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_critic_reviews(self, item_id: str) -> Any:
        """Gets critic review for an item."""
        endpoint = "/Items/{itemId}/CriticReviews"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_download(self, item_id: str) -> Any:
        """Downloads item media."""
        endpoint = "/Items/{itemId}/Download"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_file(self, item_id: str) -> Any:
        """Get the original file of an item."""
        endpoint = "/Items/{itemId}/File"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_similar_items(
        self,
        item_id: str,
        exclude_artist_ids: list[Any] | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
    ) -> Any:
        """Gets similar items."""
        endpoint = "/Items/{itemId}/Similar"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        return self.request("GET", endpoint, params=params)

    def get_theme_media(
        self,
        item_id: str,
        user_id: str | None = None,
        inherit_from_parent: bool | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
    ) -> Any:
        """Get theme songs and videos for an item."""
        endpoint = "/Items/{itemId}/ThemeMedia"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if inherit_from_parent is not None:
            params["inheritFromParent"] = inherit_from_parent
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        return self.request("GET", endpoint, params=params)

    def get_theme_songs(
        self,
        item_id: str,
        user_id: str | None = None,
        inherit_from_parent: bool | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
    ) -> Any:
        """Get theme songs for an item."""
        endpoint = "/Items/{itemId}/ThemeSongs"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if inherit_from_parent is not None:
            params["inheritFromParent"] = inherit_from_parent
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        return self.request("GET", endpoint, params=params)

    def get_theme_videos(
        self,
        item_id: str,
        user_id: str | None = None,
        inherit_from_parent: bool | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
    ) -> Any:
        """Get theme videos for an item."""
        endpoint = "/Items/{itemId}/ThemeVideos"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if inherit_from_parent is not None:
            params["inheritFromParent"] = inherit_from_parent
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        return self.request("GET", endpoint, params=params)

    def get_item_counts(
        self, user_id: str | None = None, is_favorite: bool | None = None
    ) -> Any:
        """Get item counts."""
        endpoint = "/Items/Counts"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        return self.request("GET", endpoint, params=params)

    def get_library_options_info(
        self,
        library_content_type: str | None = None,
        is_new_library: bool | None = None,
    ) -> Any:
        """Gets the library options info."""
        endpoint = "/Libraries/AvailableOptions"
        params: dict[str, Any] = {}
        if library_content_type is not None:
            params["libraryContentType"] = library_content_type
        if is_new_library is not None:
            params["isNewLibrary"] = is_new_library
        return self.request("GET", endpoint, params=params)

    def post_updated_media(self, body: dict[str, Any] | None = None) -> Any:
        """Reports that new movies have been added by an external source."""
        endpoint = "/Library/Media/Updated"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_media_folders(self, is_hidden: bool | None = None) -> Any:
        """Gets all user media folders."""
        endpoint = "/Library/MediaFolders"
        params: dict[str, Any] = {}
        if is_hidden is not None:
            params["isHidden"] = is_hidden
        return self.request("GET", endpoint, params=params)

    def post_added_movies(
        self, tmdb_id: str | None = None, imdb_id: str | None = None
    ) -> Any:
        """Reports that new movies have been added by an external source."""
        endpoint = "/Library/Movies/Added"
        params: dict[str, Any] = {}
        if tmdb_id is not None:
            params["tmdbId"] = tmdb_id
        if imdb_id is not None:
            params["imdbId"] = imdb_id
        return self.request("POST", endpoint, params=params)

    def post_updated_movies(
        self, tmdb_id: str | None = None, imdb_id: str | None = None
    ) -> Any:
        """Reports that new movies have been added by an external source."""
        endpoint = "/Library/Movies/Updated"
        params: dict[str, Any] = {}
        if tmdb_id is not None:
            params["tmdbId"] = tmdb_id
        if imdb_id is not None:
            params["imdbId"] = imdb_id
        return self.request("POST", endpoint, params=params)

    def get_physical_paths(self) -> Any:
        """Gets a list of physical paths from virtual folders."""
        endpoint = "/Library/PhysicalPaths"
        params = None
        return self.request("GET", endpoint, params=params)

    def refresh_library(self) -> Any:
        """Starts a library scan."""
        endpoint = "/Library/Refresh"
        params = None
        return self.request("POST", endpoint, params=params)

    def post_added_series(self, tvdb_id: str | None = None) -> Any:
        """Reports that new episodes of a series have been added by an external source."""
        endpoint = "/Library/Series/Added"
        params: dict[str, Any] = {}
        if tvdb_id is not None:
            params["tvdbId"] = tvdb_id
        return self.request("POST", endpoint, params=params)

    def post_updated_series(self, tvdb_id: str | None = None) -> Any:
        """Reports that new episodes of a series have been added by an external source."""
        endpoint = "/Library/Series/Updated"
        params: dict[str, Any] = {}
        if tvdb_id is not None:
            params["tvdbId"] = tvdb_id
        return self.request("POST", endpoint, params=params)

    def get_similar_movies(
        self,
        item_id: str,
        exclude_artist_ids: list[Any] | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
    ) -> Any:
        """Gets similar items."""
        endpoint = "/Movies/{itemId}/Similar"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        return self.request("GET", endpoint, params=params)

    def get_similar_shows(
        self,
        item_id: str,
        exclude_artist_ids: list[Any] | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
    ) -> Any:
        """Gets similar items."""
        endpoint = "/Shows/{itemId}/Similar"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        return self.request("GET", endpoint, params=params)

    def get_similar_trailers(
        self,
        item_id: str,
        exclude_artist_ids: list[Any] | None = None,
        user_id: str | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
    ) -> Any:
        """Gets similar items."""
        endpoint = "/Trailers/{itemId}/Similar"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        return self.request("GET", endpoint, params=params)

    def get_virtual_folders(self) -> Any:
        """Gets all virtual folders."""
        endpoint = "/Library/VirtualFolders"
        params = None
        return self.request("GET", endpoint, params=params)

    def add_virtual_folder(
        self,
        name: str | None = None,
        collection_type: str | None = None,
        paths: list[Any] | None = None,
        refresh_library: bool | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Adds a virtual folder."""
        endpoint = "/Library/VirtualFolders"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if collection_type is not None:
            params["collectionType"] = collection_type
        if paths is not None:
            params["paths"] = paths
        if refresh_library is not None:
            params["refreshLibrary"] = refresh_library
        return self.request("POST", endpoint, params=params, json_data=body)

    def remove_virtual_folder(
        self, name: str | None = None, refresh_library: bool | None = None
    ) -> Any:
        """Removes a virtual folder."""
        endpoint = "/Library/VirtualFolders"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if refresh_library is not None:
            params["refreshLibrary"] = refresh_library
        return self.request("DELETE", endpoint, params=params)

    def update_library_options(self, body: dict[str, Any] | None = None) -> Any:
        """Update library options."""
        endpoint = "/Library/VirtualFolders/LibraryOptions"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def rename_virtual_folder(
        self,
        name: str | None = None,
        new_name: str | None = None,
        refresh_library: bool | None = None,
    ) -> Any:
        """Renames a virtual folder."""
        endpoint = "/Library/VirtualFolders/Name"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if new_name is not None:
            params["newName"] = new_name
        if refresh_library is not None:
            params["refreshLibrary"] = refresh_library
        return self.request("POST", endpoint, params=params)

    def add_media_path(
        self,
        refresh_library: bool | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Add a media path to a library."""
        endpoint = "/Library/VirtualFolders/Paths"
        params: dict[str, Any] = {}
        if refresh_library is not None:
            params["refreshLibrary"] = refresh_library
        return self.request("POST", endpoint, params=params, json_data=body)

    def remove_media_path(
        self,
        name: str | None = None,
        path: str | None = None,
        refresh_library: bool | None = None,
    ) -> Any:
        """Remove a media path."""
        endpoint = "/Library/VirtualFolders/Paths"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if path is not None:
            params["path"] = path
        if refresh_library is not None:
            params["refreshLibrary"] = refresh_library
        return self.request("DELETE", endpoint, params=params)

    def update_media_path(self, body: dict[str, Any] | None = None) -> Any:
        """Updates a media path."""
        endpoint = "/Library/VirtualFolders/Paths/Update"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_channel_mapping_options(self, provider_id: str | None = None) -> Any:
        """Get channel mapping options."""
        endpoint = "/LiveTv/ChannelMappingOptions"
        params: dict[str, Any] = {}
        if provider_id is not None:
            params["providerId"] = provider_id
        return self.request("GET", endpoint, params=params)

    def set_channel_mapping(self, body: dict[str, Any] | None = None) -> Any:
        """Set channel mappings."""
        endpoint = "/LiveTv/ChannelMappings"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_live_tv_channels(
        self,
        type: str | None = None,
        user_id: str | None = None,
        start_index: int | None = None,
        is_movie: bool | None = None,
        is_series: bool | None = None,
        is_news: bool | None = None,
        is_kids: bool | None = None,
        is_sports: bool | None = None,
        limit: int | None = None,
        is_favorite: bool | None = None,
        is_liked: bool | None = None,
        is_disliked: bool | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        fields: list[Any] | None = None,
        enable_user_data: bool | None = None,
        sort_by: list[Any] | None = None,
        sort_order: str | None = None,
        enable_favorite_sorting: bool | None = None,
        add_current_program: bool | None = None,
    ) -> Any:
        """Gets available live tv channels."""
        endpoint = "/LiveTv/Channels"
        params: dict[str, Any] = {}
        if type is not None:
            params["type"] = type
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_series is not None:
            params["isSeries"] = is_series
        if is_news is not None:
            params["isNews"] = is_news
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_sports is not None:
            params["isSports"] = is_sports
        if limit is not None:
            params["limit"] = limit
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if is_liked is not None:
            params["isLiked"] = is_liked
        if is_disliked is not None:
            params["isDisliked"] = is_disliked
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if fields is not None:
            params["fields"] = fields
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if enable_favorite_sorting is not None:
            params["enableFavoriteSorting"] = enable_favorite_sorting
        if add_current_program is not None:
            params["addCurrentProgram"] = add_current_program
        return self.request("GET", endpoint, params=params)

    def get_channel(self, channel_id: str, user_id: str | None = None) -> Any:
        """Gets a live tv channel."""
        endpoint = "/LiveTv/Channels/{channelId}"
        endpoint = endpoint.replace("{channelId}", str(channel_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_guide_info(self) -> Any:
        """Get guide info."""
        endpoint = "/LiveTv/GuideInfo"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_live_tv_info(self) -> Any:
        """Gets available live tv services."""
        endpoint = "/LiveTv/Info"
        params = None
        return self.request("GET", endpoint, params=params)

    def add_listing_provider(
        self,
        pw: str | None = None,
        validate_listings: bool | None = None,
        validate_login: bool | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Adds a listings provider."""
        endpoint = "/LiveTv/ListingProviders"
        params: dict[str, Any] = {}
        if pw is not None:
            params["pw"] = pw
        if validate_listings is not None:
            params["validateListings"] = validate_listings
        if validate_login is not None:
            params["validateLogin"] = validate_login
        return self.request("POST", endpoint, params=params, json_data=body)

    def delete_listing_provider(self, id: str | None = None) -> Any:
        """Delete listing provider."""
        endpoint = "/LiveTv/ListingProviders"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        return self.request("DELETE", endpoint, params=params)

    def get_default_listing_provider(self) -> Any:
        """Gets default listings provider info."""
        endpoint = "/LiveTv/ListingProviders/Default"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_lineups(
        self,
        id: str | None = None,
        type: str | None = None,
        location: str | None = None,
        country: str | None = None,
    ) -> Any:
        """Gets available lineups."""
        endpoint = "/LiveTv/ListingProviders/Lineups"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if type is not None:
            params["type"] = type
        if location is not None:
            params["location"] = location
        if country is not None:
            params["country"] = country
        return self.request("GET", endpoint, params=params)

    def get_schedules_direct_countries(self) -> Any:
        """Gets available countries."""
        endpoint = "/LiveTv/ListingProviders/SchedulesDirect/Countries"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_live_recording_file(self, recording_id: str) -> Any:
        """Gets a live tv recording stream."""
        endpoint = "/LiveTv/LiveRecordings/{recordingId}/stream"
        endpoint = endpoint.replace("{recordingId}", str(recording_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_live_stream_file(self, stream_id: str, container: str) -> Any:
        """Gets a live tv channel stream."""
        endpoint = "/LiveTv/LiveStreamFiles/{streamId}/stream.{container}"
        endpoint = endpoint.replace("{streamId}", str(stream_id))
        endpoint = endpoint.replace("{container}", str(container))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_live_tv_programs(
        self,
        channel_ids: list[Any] | None = None,
        user_id: str | None = None,
        min_start_date: str | None = None,
        has_aired: bool | None = None,
        is_airing: bool | None = None,
        max_start_date: str | None = None,
        min_end_date: str | None = None,
        max_end_date: str | None = None,
        is_movie: bool | None = None,
        is_series: bool | None = None,
        is_news: bool | None = None,
        is_kids: bool | None = None,
        is_sports: bool | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
        genres: list[Any] | None = None,
        genre_ids: list[Any] | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        enable_user_data: bool | None = None,
        series_timer_id: str | None = None,
        library_series_id: str | None = None,
        fields: list[Any] | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets available live tv epgs."""
        endpoint = "/LiveTv/Programs"
        params: dict[str, Any] = {}
        if channel_ids is not None:
            params["channelIds"] = channel_ids
        if user_id is not None:
            params["userId"] = user_id
        if min_start_date is not None:
            params["minStartDate"] = min_start_date
        if has_aired is not None:
            params["hasAired"] = has_aired
        if is_airing is not None:
            params["isAiring"] = is_airing
        if max_start_date is not None:
            params["maxStartDate"] = max_start_date
        if min_end_date is not None:
            params["minEndDate"] = min_end_date
        if max_end_date is not None:
            params["maxEndDate"] = max_end_date
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_series is not None:
            params["isSeries"] = is_series
        if is_news is not None:
            params["isNews"] = is_news
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_sports is not None:
            params["isSports"] = is_sports
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if genres is not None:
            params["genres"] = genres
        if genre_ids is not None:
            params["genreIds"] = genre_ids
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if series_timer_id is not None:
            params["seriesTimerId"] = series_timer_id
        if library_series_id is not None:
            params["librarySeriesId"] = library_series_id
        if fields is not None:
            params["fields"] = fields
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_programs(self, body: dict[str, Any] | None = None) -> Any:
        """Gets available live tv epgs."""
        endpoint = "/LiveTv/Programs"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_program(self, program_id: str, user_id: str | None = None) -> Any:
        """Gets a live tv program."""
        endpoint = "/LiveTv/Programs/{programId}"
        endpoint = endpoint.replace("{programId}", str(program_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_recommended_programs(
        self,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        is_airing: bool | None = None,
        has_aired: bool | None = None,
        is_series: bool | None = None,
        is_movie: bool | None = None,
        is_news: bool | None = None,
        is_kids: bool | None = None,
        is_sports: bool | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        genre_ids: list[Any] | None = None,
        fields: list[Any] | None = None,
        enable_user_data: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets recommended live tv epgs."""
        endpoint = "/LiveTv/Programs/Recommended"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if is_airing is not None:
            params["isAiring"] = is_airing
        if has_aired is not None:
            params["hasAired"] = has_aired
        if is_series is not None:
            params["isSeries"] = is_series
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_news is not None:
            params["isNews"] = is_news
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_sports is not None:
            params["isSports"] = is_sports
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if genre_ids is not None:
            params["genreIds"] = genre_ids
        if fields is not None:
            params["fields"] = fields
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_recordings(
        self,
        channel_id: str | None = None,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        is_in_progress: bool | None = None,
        series_timer_id: str | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        fields: list[Any] | None = None,
        enable_user_data: bool | None = None,
        is_movie: bool | None = None,
        is_series: bool | None = None,
        is_kids: bool | None = None,
        is_sports: bool | None = None,
        is_news: bool | None = None,
        is_library_item: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets live tv recordings."""
        endpoint = "/LiveTv/Recordings"
        params: dict[str, Any] = {}
        if channel_id is not None:
            params["channelId"] = channel_id
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if status is not None:
            params["status"] = status
        if is_in_progress is not None:
            params["isInProgress"] = is_in_progress
        if series_timer_id is not None:
            params["seriesTimerId"] = series_timer_id
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if fields is not None:
            params["fields"] = fields
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_series is not None:
            params["isSeries"] = is_series
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_sports is not None:
            params["isSports"] = is_sports
        if is_news is not None:
            params["isNews"] = is_news
        if is_library_item is not None:
            params["isLibraryItem"] = is_library_item
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_recording(self, recording_id: str, user_id: str | None = None) -> Any:
        """Gets a live tv recording."""
        endpoint = "/LiveTv/Recordings/{recordingId}"
        endpoint = endpoint.replace("{recordingId}", str(recording_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def delete_recording(self, recording_id: str) -> Any:
        """Deletes a live tv recording."""
        endpoint = "/LiveTv/Recordings/{recordingId}"
        endpoint = endpoint.replace("{recordingId}", str(recording_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_recording_folders(self, user_id: str | None = None) -> Any:
        """Gets recording folders."""
        endpoint = "/LiveTv/Recordings/Folders"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_recording_groups(self, user_id: str | None = None) -> Any:
        """Gets live tv recording groups."""
        endpoint = "/LiveTv/Recordings/Groups"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_recording_group(self, group_id: str) -> Any:
        """Get recording group."""
        endpoint = "/LiveTv/Recordings/Groups/{groupId}"
        endpoint = endpoint.replace("{groupId}", str(group_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_recordings_series(
        self,
        channel_id: str | None = None,
        user_id: str | None = None,
        group_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        is_in_progress: bool | None = None,
        series_timer_id: str | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        fields: list[Any] | None = None,
        enable_user_data: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets live tv recording series."""
        endpoint = "/LiveTv/Recordings/Series"
        params: dict[str, Any] = {}
        if channel_id is not None:
            params["channelId"] = channel_id
        if user_id is not None:
            params["userId"] = user_id
        if group_id is not None:
            params["groupId"] = group_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if status is not None:
            params["status"] = status
        if is_in_progress is not None:
            params["isInProgress"] = is_in_progress
        if series_timer_id is not None:
            params["seriesTimerId"] = series_timer_id
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if fields is not None:
            params["fields"] = fields
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_series_timers(
        self, sort_by: str | None = None, sort_order: str | None = None
    ) -> Any:
        """Gets live tv series timers."""
        endpoint = "/LiveTv/SeriesTimers"
        params: dict[str, Any] = {}
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        return self.request("GET", endpoint, params=params)

    def create_series_timer(self, body: dict[str, Any] | None = None) -> Any:
        """Creates a live tv series timer."""
        endpoint = "/LiveTv/SeriesTimers"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_series_timer(self, timer_id: str) -> Any:
        """Gets a live tv series timer."""
        endpoint = "/LiveTv/SeriesTimers/{timerId}"
        endpoint = endpoint.replace("{timerId}", str(timer_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def cancel_series_timer(self, timer_id: str) -> Any:
        """Cancels a live tv series timer."""
        endpoint = "/LiveTv/SeriesTimers/{timerId}"
        endpoint = endpoint.replace("{timerId}", str(timer_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def update_series_timer(
        self, timer_id: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates a live tv series timer."""
        endpoint = "/LiveTv/SeriesTimers/{timerId}"
        endpoint = endpoint.replace("{timerId}", str(timer_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_timers(
        self,
        channel_id: str | None = None,
        series_timer_id: str | None = None,
        is_active: bool | None = None,
        is_scheduled: bool | None = None,
    ) -> Any:
        """Gets the live tv timers."""
        endpoint = "/LiveTv/Timers"
        params: dict[str, Any] = {}
        if channel_id is not None:
            params["channelId"] = channel_id
        if series_timer_id is not None:
            params["seriesTimerId"] = series_timer_id
        if is_active is not None:
            params["isActive"] = is_active
        if is_scheduled is not None:
            params["isScheduled"] = is_scheduled
        return self.request("GET", endpoint, params=params)

    def create_timer(self, body: dict[str, Any] | None = None) -> Any:
        """Creates a live tv timer."""
        endpoint = "/LiveTv/Timers"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_timer(self, timer_id: str) -> Any:
        """Gets a timer."""
        endpoint = "/LiveTv/Timers/{timerId}"
        endpoint = endpoint.replace("{timerId}", str(timer_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def cancel_timer(self, timer_id: str) -> Any:
        """Cancels a live tv timer."""
        endpoint = "/LiveTv/Timers/{timerId}"
        endpoint = endpoint.replace("{timerId}", str(timer_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def update_timer(self, timer_id: str, body: dict[str, Any] | None = None) -> Any:
        """Updates a live tv timer."""
        endpoint = "/LiveTv/Timers/{timerId}"
        endpoint = endpoint.replace("{timerId}", str(timer_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_default_timer(self, program_id: str | None = None) -> Any:
        """Gets the default values for a new timer."""
        endpoint = "/LiveTv/Timers/Defaults"
        params: dict[str, Any] = {}
        if program_id is not None:
            params["programId"] = program_id
        return self.request("GET", endpoint, params=params)

    def add_tuner_host(self, body: dict[str, Any] | None = None) -> Any:
        """Adds a tuner host."""
        endpoint = "/LiveTv/TunerHosts"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def delete_tuner_host(self, id: str | None = None) -> Any:
        """Deletes a tuner host."""
        endpoint = "/LiveTv/TunerHosts"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        return self.request("DELETE", endpoint, params=params)

    def get_tuner_host_types(self) -> Any:
        """Get tuner host types."""
        endpoint = "/LiveTv/TunerHosts/Types"
        params = None
        return self.request("GET", endpoint, params=params)

    def reset_tuner(self, tuner_id: str) -> Any:
        """Resets a tv tuner."""
        endpoint = "/LiveTv/Tuners/{tunerId}/Reset"
        endpoint = endpoint.replace("{tunerId}", str(tuner_id))
        params = None
        return self.request("POST", endpoint, params=params)

    def discover_tuners(self, new_devices_only: bool | None = None) -> Any:
        """Discover tuners."""
        endpoint = "/LiveTv/Tuners/Discover"
        params: dict[str, Any] = {}
        if new_devices_only is not None:
            params["newDevicesOnly"] = new_devices_only
        return self.request("GET", endpoint, params=params)

    def discvover_tuners(self, new_devices_only: bool | None = None) -> Any:
        """Discover tuners."""
        endpoint = "/LiveTv/Tuners/Discvover"
        params: dict[str, Any] = {}
        if new_devices_only is not None:
            params["newDevicesOnly"] = new_devices_only
        return self.request("GET", endpoint, params=params)

    def get_countries(self) -> Any:
        """Gets known countries."""
        endpoint = "/Localization/Countries"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_cultures(self) -> Any:
        """Gets known cultures."""
        endpoint = "/Localization/Cultures"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_localization_options(self) -> Any:
        """Gets localization options."""
        endpoint = "/Localization/Options"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_parental_ratings(self) -> Any:
        """Gets known parental ratings."""
        endpoint = "/Localization/ParentalRatings"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_lyrics(self, item_id: str) -> Any:
        """Gets an item's lyrics."""
        endpoint = "/Audio/{itemId}/Lyrics"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def upload_lyrics(
        self,
        item_id: str,
        file_name: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Upload an external lyric file."""
        endpoint = "/Audio/{itemId}/Lyrics"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if file_name is not None:
            params["fileName"] = file_name
        return self.request("POST", endpoint, params=params, json_data=body)

    def delete_lyrics(self, item_id: str) -> Any:
        """Deletes an external lyric file."""
        endpoint = "/Audio/{itemId}/Lyrics"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def search_remote_lyrics(self, item_id: str) -> Any:
        """Search remote lyrics."""
        endpoint = "/Audio/{itemId}/RemoteSearch/Lyrics"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def download_remote_lyrics(self, item_id: str, lyric_id: str) -> Any:
        """Downloads a remote lyric."""
        endpoint = "/Audio/{itemId}/RemoteSearch/Lyrics/{lyricId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{lyricId}", str(lyric_id))
        params = None
        return self.request("POST", endpoint, params=params)

    def get_remote_lyrics(self, lyric_id: str) -> Any:
        """Gets the remote lyrics."""
        endpoint = "/Providers/Lyrics/{lyricId}"
        endpoint = endpoint.replace("{lyricId}", str(lyric_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_playback_info(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets live playback media info for an item."""
        endpoint = "/Items/{itemId}/PlaybackInfo"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_posted_playback_info(
        self,
        item_id: str,
        user_id: str | None = None,
        max_streaming_bitrate: int | None = None,
        start_time_ticks: int | None = None,
        audio_stream_index: int | None = None,
        subtitle_stream_index: int | None = None,
        max_audio_channels: int | None = None,
        media_source_id: str | None = None,
        live_stream_id: str | None = None,
        auto_open_live_stream: bool | None = None,
        enable_direct_play: bool | None = None,
        enable_direct_stream: bool | None = None,
        enable_transcoding: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Gets live playback media info for an item."""
        endpoint = "/Items/{itemId}/PlaybackInfo"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if max_streaming_bitrate is not None:
            params["maxStreamingBitrate"] = max_streaming_bitrate
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if auto_open_live_stream is not None:
            params["autoOpenLiveStream"] = auto_open_live_stream
        if enable_direct_play is not None:
            params["enableDirectPlay"] = enable_direct_play
        if enable_direct_stream is not None:
            params["enableDirectStream"] = enable_direct_stream
        if enable_transcoding is not None:
            params["enableTranscoding"] = enable_transcoding
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        return self.request("POST", endpoint, params=params, json_data=body)

    def close_live_stream(self, live_stream_id: str | None = None) -> Any:
        """Closes a media source."""
        endpoint = "/LiveStreams/Close"
        params: dict[str, Any] = {}
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        return self.request("POST", endpoint, params=params)

    def open_live_stream(
        self,
        open_token: str | None = None,
        user_id: str | None = None,
        play_session_id: str | None = None,
        max_streaming_bitrate: int | None = None,
        start_time_ticks: int | None = None,
        audio_stream_index: int | None = None,
        subtitle_stream_index: int | None = None,
        max_audio_channels: int | None = None,
        item_id: str | None = None,
        enable_direct_play: bool | None = None,
        enable_direct_stream: bool | None = None,
        always_burn_in_subtitle_when_transcoding: bool | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Opens a media source."""
        endpoint = "/LiveStreams/Open"
        params: dict[str, Any] = {}
        if open_token is not None:
            params["openToken"] = open_token
        if user_id is not None:
            params["userId"] = user_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if max_streaming_bitrate is not None:
            params["maxStreamingBitrate"] = max_streaming_bitrate
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if item_id is not None:
            params["itemId"] = item_id
        if enable_direct_play is not None:
            params["enableDirectPlay"] = enable_direct_play
        if enable_direct_stream is not None:
            params["enableDirectStream"] = enable_direct_stream
        if always_burn_in_subtitle_when_transcoding is not None:
            params["alwaysBurnInSubtitleWhenTranscoding"] = (
                always_burn_in_subtitle_when_transcoding
            )
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_bitrate_test_bytes(self, size: int | None = None) -> Any:
        """Tests the network with a request with the size of the bitrate."""
        endpoint = "/Playback/BitrateTest"
        params: dict[str, Any] = {}
        if size is not None:
            params["size"] = size
        return self.request("GET", endpoint, params=params)

    def get_item_segments(
        self, item_id: str, include_segment_types: list[Any] | None = None
    ) -> Any:
        """Gets all media segments based on an itemId."""
        endpoint = "/MediaSegments/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if include_segment_types is not None:
            params["includeSegmentTypes"] = include_segment_types
        return self.request("GET", endpoint, params=params)

    def get_movie_recommendations(
        self,
        user_id: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        category_limit: int | None = None,
        item_limit: int | None = None,
    ) -> Any:
        """Gets movie recommendations."""
        endpoint = "/Movies/Recommendations"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if category_limit is not None:
            params["categoryLimit"] = category_limit
        if item_limit is not None:
            params["itemLimit"] = item_limit
        return self.request("GET", endpoint, params=params)

    def get_music_genres(
        self,
        start_index: int | None = None,
        limit: int | None = None,
        search_term: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        is_favorite: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        user_id: str | None = None,
        name_starts_with_or_greater: str | None = None,
        name_starts_with: str | None = None,
        name_less_than: str | None = None,
        sort_by: list[Any] | None = None,
        sort_order: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets all music genres from a given item, folder, or the entire library."""
        endpoint = "/MusicGenres"
        params: dict[str, Any] = {}
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if search_term is not None:
            params["searchTerm"] = search_term
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if user_id is not None:
            params["userId"] = user_id
        if name_starts_with_or_greater is not None:
            params["nameStartsWithOrGreater"] = name_starts_with_or_greater
        if name_starts_with is not None:
            params["nameStartsWith"] = name_starts_with
        if name_less_than is not None:
            params["nameLessThan"] = name_less_than
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_music_genre(self, genre_name: str, user_id: str | None = None) -> Any:
        """Gets a music genre, by name."""
        endpoint = "/MusicGenres/{genreName}"
        endpoint = endpoint.replace("{genreName}", str(genre_name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_packages(self) -> Any:
        """Gets available packages."""
        endpoint = "/Packages"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_package_info(self, name: str, assembly_guid: str | None = None) -> Any:
        """Gets a package by name or assembly GUID."""
        endpoint = "/Packages/{name}"
        endpoint = endpoint.replace("{name}", str(name))
        params: dict[str, Any] = {}
        if assembly_guid is not None:
            params["assemblyGuid"] = assembly_guid
        return self.request("GET", endpoint, params=params)

    def install_package(
        self,
        name: str,
        assembly_guid: str | None = None,
        version: str | None = None,
        repository_url: str | None = None,
    ) -> Any:
        """Installs a package."""
        endpoint = "/Packages/Installed/{name}"
        endpoint = endpoint.replace("{name}", str(name))
        params: dict[str, Any] = {}
        if assembly_guid is not None:
            params["assemblyGuid"] = assembly_guid
        if version is not None:
            params["version"] = version
        if repository_url is not None:
            params["repositoryUrl"] = repository_url
        return self.request("POST", endpoint, params=params)

    def cancel_package_installation(self, package_id: str) -> Any:
        """Cancels a package installation."""
        endpoint = "/Packages/Installing/{packageId}"
        endpoint = endpoint.replace("{packageId}", str(package_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_repositories(self) -> Any:
        """Gets all package repositories."""
        endpoint = "/Repositories"
        params = None
        return self.request("GET", endpoint, params=params)

    def set_repositories(self, body: dict[str, Any] | None = None) -> Any:
        """Sets the enabled and existing package repositories."""
        endpoint = "/Repositories"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_persons(
        self,
        limit: int | None = None,
        search_term: str | None = None,
        fields: list[Any] | None = None,
        filters: list[Any] | None = None,
        is_favorite: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        exclude_person_types: list[Any] | None = None,
        person_types: list[Any] | None = None,
        appears_in_item_id: str | None = None,
        user_id: str | None = None,
        enable_images: bool | None = None,
    ) -> Any:
        """Gets all persons."""
        endpoint = "/Persons"
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if search_term is not None:
            params["searchTerm"] = search_term
        if fields is not None:
            params["fields"] = fields
        if filters is not None:
            params["filters"] = filters
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if exclude_person_types is not None:
            params["excludePersonTypes"] = exclude_person_types
        if person_types is not None:
            params["personTypes"] = person_types
        if appears_in_item_id is not None:
            params["appearsInItemId"] = appears_in_item_id
        if user_id is not None:
            params["userId"] = user_id
        if enable_images is not None:
            params["enableImages"] = enable_images
        return self.request("GET", endpoint, params=params)

    def get_person(self, name: str, user_id: str | None = None) -> Any:
        """Get person by name."""
        endpoint = "/Persons/{name}"
        endpoint = endpoint.replace("{name}", str(name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def create_playlist(
        self,
        name: str | None = None,
        ids: list[Any] | None = None,
        user_id: str | None = None,
        media_type: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Creates a new playlist."""
        endpoint = "/Playlists"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if ids is not None:
            params["ids"] = ids
        if user_id is not None:
            params["userId"] = user_id
        if media_type is not None:
            params["mediaType"] = media_type
        return self.request("POST", endpoint, params=params, json_data=body)

    def update_playlist(
        self, playlist_id: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates a playlist."""
        endpoint = "/Playlists/{playlistId}"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_playlist(self, playlist_id: str) -> Any:
        """Get a playlist."""
        endpoint = "/Playlists/{playlistId}"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def add_item_to_playlist(
        self,
        playlist_id: str,
        ids: list[Any] | None = None,
        user_id: str | None = None,
    ) -> Any:
        """Adds items to a playlist."""
        endpoint = "/Playlists/{playlistId}/Items"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params)

    def remove_item_from_playlist(
        self, playlist_id: str, entry_ids: list[Any] | None = None
    ) -> Any:
        """Removes items from a playlist."""
        endpoint = "/Playlists/{playlistId}/Items"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        params: dict[str, Any] = {}
        if entry_ids is not None:
            params["entryIds"] = entry_ids
        return self.request("DELETE", endpoint, params=params)

    def get_playlist_items(
        self,
        playlist_id: str,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        enable_images: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
    ) -> Any:
        """Gets the original items of a playlist."""
        endpoint = "/Playlists/{playlistId}/Items"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        return self.request("GET", endpoint, params=params)

    def move_item(self, playlist_id: str, item_id: str, new_index: int) -> Any:
        """Moves a playlist item."""
        endpoint = "/Playlists/{playlistId}/Items/{itemId}/Move/{newIndex}"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{newIndex}", str(new_index))
        params = None
        return self.request("POST", endpoint, params=params)

    def get_playlist_users(self, playlist_id: str) -> Any:
        """Get a playlist's users."""
        endpoint = "/Playlists/{playlistId}/Users"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_playlist_user(self, playlist_id: str, user_id: str) -> Any:
        """Get a playlist user."""
        endpoint = "/Playlists/{playlistId}/Users/{userId}"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def update_playlist_user(
        self, playlist_id: str, user_id: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Modify a user of a playlist's users."""
        endpoint = "/Playlists/{playlistId}/Users/{userId}"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def remove_user_from_playlist(self, playlist_id: str, user_id: str) -> Any:
        """Remove a user from a playlist's users."""
        endpoint = "/Playlists/{playlistId}/Users/{userId}"
        endpoint = endpoint.replace("{playlistId}", str(playlist_id))
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def on_playback_start(
        self,
        item_id: str,
        media_source_id: str | None = None,
        audio_stream_index: int | None = None,
        subtitle_stream_index: int | None = None,
        play_method: str | None = None,
        live_stream_id: str | None = None,
        play_session_id: str | None = None,
        can_seek: bool | None = None,
    ) -> Any:
        """Reports that a session has begun playing an item."""
        endpoint = "/PlayingItems/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if play_method is not None:
            params["playMethod"] = play_method
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if can_seek is not None:
            params["canSeek"] = can_seek
        return self.request("POST", endpoint, params=params)

    def on_playback_stopped(
        self,
        item_id: str,
        media_source_id: str | None = None,
        next_media_type: str | None = None,
        position_ticks: int | None = None,
        live_stream_id: str | None = None,
        play_session_id: str | None = None,
    ) -> Any:
        """Reports that a session has stopped playing an item."""
        endpoint = "/PlayingItems/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if next_media_type is not None:
            params["nextMediaType"] = next_media_type
        if position_ticks is not None:
            params["positionTicks"] = position_ticks
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        return self.request("DELETE", endpoint, params=params)

    def on_playback_progress(
        self,
        item_id: str,
        media_source_id: str | None = None,
        position_ticks: int | None = None,
        audio_stream_index: int | None = None,
        subtitle_stream_index: int | None = None,
        volume_level: int | None = None,
        play_method: str | None = None,
        live_stream_id: str | None = None,
        play_session_id: str | None = None,
        repeat_mode: str | None = None,
        is_paused: bool | None = None,
        is_muted: bool | None = None,
    ) -> Any:
        """Reports a session's playback progress."""
        endpoint = "/PlayingItems/{itemId}/Progress"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if position_ticks is not None:
            params["positionTicks"] = position_ticks
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if volume_level is not None:
            params["volumeLevel"] = volume_level
        if play_method is not None:
            params["playMethod"] = play_method
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if repeat_mode is not None:
            params["repeatMode"] = repeat_mode
        if is_paused is not None:
            params["isPaused"] = is_paused
        if is_muted is not None:
            params["isMuted"] = is_muted
        return self.request("POST", endpoint, params=params)

    def report_playback_start(self, body: dict[str, Any] | None = None) -> Any:
        """Reports playback has started within a session."""
        endpoint = "/Sessions/Playing"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def ping_playback_session(self, play_session_id: str | None = None) -> Any:
        """Pings a playback session."""
        endpoint = "/Sessions/Playing/Ping"
        params: dict[str, Any] = {}
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        return self.request("POST", endpoint, params=params)

    def report_playback_progress(self, body: dict[str, Any] | None = None) -> Any:
        """Reports playback progress within a session."""
        endpoint = "/Sessions/Playing/Progress"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def report_playback_stopped(self, body: dict[str, Any] | None = None) -> Any:
        """Reports playback has stopped within a session."""
        endpoint = "/Sessions/Playing/Stopped"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def mark_played_item(
        self,
        item_id: str,
        user_id: str | None = None,
        date_played: str | None = None,
    ) -> Any:
        """Marks an item as played for user."""
        endpoint = "/UserPlayedItems/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if date_played is not None:
            params["datePlayed"] = date_played
        return self.request("POST", endpoint, params=params)

    def mark_unplayed_item(self, item_id: str, user_id: str | None = None) -> Any:
        """Marks an item as unplayed for user."""
        endpoint = "/UserPlayedItems/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("DELETE", endpoint, params=params)

    def get_plugins(self) -> Any:
        """Gets a list of currently installed plugins."""
        endpoint = "/Plugins"
        params = None
        return self.request("GET", endpoint, params=params)

    def uninstall_plugin(self, plugin_id: str) -> Any:
        """Uninstalls a plugin."""
        endpoint = "/Plugins/{pluginId}"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def uninstall_plugin_by_version(self, plugin_id: str, version: str) -> Any:
        """Uninstalls a plugin by version."""
        endpoint = "/Plugins/{pluginId}/{version}"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        endpoint = endpoint.replace("{version}", str(version))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def disable_plugin(self, plugin_id: str, version: str) -> Any:
        """Disable a plugin."""
        endpoint = "/Plugins/{pluginId}/{version}/Disable"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        endpoint = endpoint.replace("{version}", str(version))
        params = None
        return self.request("POST", endpoint, params=params)

    def enable_plugin(self, plugin_id: str, version: str) -> Any:
        """Enables a disabled plugin."""
        endpoint = "/Plugins/{pluginId}/{version}/Enable"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        endpoint = endpoint.replace("{version}", str(version))
        params = None
        return self.request("POST", endpoint, params=params)

    def get_plugin_image(self, plugin_id: str, version: str) -> Any:
        """Gets a plugin's image."""
        endpoint = "/Plugins/{pluginId}/{version}/Image"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        endpoint = endpoint.replace("{version}", str(version))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_plugin_configuration(self, plugin_id: str) -> Any:
        """Gets plugin configuration."""
        endpoint = "/Plugins/{pluginId}/Configuration"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def update_plugin_configuration(self, plugin_id: str) -> Any:
        """Updates plugin configuration."""
        endpoint = "/Plugins/{pluginId}/Configuration"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        params = None
        return self.request("POST", endpoint, params=params)

    def get_plugin_manifest(self, plugin_id: str) -> Any:
        """Gets a plugin's manifest."""
        endpoint = "/Plugins/{pluginId}/Manifest"
        endpoint = endpoint.replace("{pluginId}", str(plugin_id))
        params = None
        return self.request("POST", endpoint, params=params)

    def authorize_quick_connect(
        self, code: str | None = None, user_id: str | None = None
    ) -> Any:
        """Authorizes a pending quick connect request."""
        endpoint = "/QuickConnect/Authorize"
        params: dict[str, Any] = {}
        if code is not None:
            params["code"] = code
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params)

    def get_quick_connect_state(self, secret: str | None = None) -> Any:
        """Attempts to retrieve authentication information."""
        endpoint = "/QuickConnect/Connect"
        params: dict[str, Any] = {}
        if secret is not None:
            params["secret"] = secret
        return self.request("GET", endpoint, params=params)

    def get_quick_connect_enabled(self) -> Any:
        """Gets the current quick connect state."""
        endpoint = "/QuickConnect/Enabled"
        params = None
        return self.request("GET", endpoint, params=params)

    def initiate_quick_connect(self) -> Any:
        """Initiate a new quick connect request."""
        endpoint = "/QuickConnect/Initiate"
        params = None
        return self.request("POST", endpoint, params=params)

    def get_remote_images(
        self,
        item_id: str,
        type: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        provider_name: str | None = None,
        include_all_languages: bool | None = None,
    ) -> Any:
        """Gets available remote images for an item."""
        endpoint = "/Items/{itemId}/RemoteImages"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if type is not None:
            params["type"] = type
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if provider_name is not None:
            params["providerName"] = provider_name
        if include_all_languages is not None:
            params["includeAllLanguages"] = include_all_languages
        return self.request("GET", endpoint, params=params)

    def download_remote_image(
        self, item_id: str, type: str | None = None, image_url: str | None = None
    ) -> Any:
        """Downloads a remote image for an item."""
        endpoint = "/Items/{itemId}/RemoteImages/Download"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if type is not None:
            params["type"] = type
        if image_url is not None:
            params["imageUrl"] = image_url
        return self.request("POST", endpoint, params=params)

    def get_remote_image_providers(self, item_id: str) -> Any:
        """Gets available remote image providers for an item."""
        endpoint = "/Items/{itemId}/RemoteImages/Providers"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_tasks(
        self, is_hidden: bool | None = None, is_enabled: bool | None = None
    ) -> Any:
        """Get tasks."""
        endpoint = "/ScheduledTasks"
        params: dict[str, Any] = {}
        if is_hidden is not None:
            params["isHidden"] = is_hidden
        if is_enabled is not None:
            params["isEnabled"] = is_enabled
        return self.request("GET", endpoint, params=params)

    def get_task(self, task_id: str) -> Any:
        """Get task by id."""
        endpoint = "/ScheduledTasks/{taskId}"
        endpoint = endpoint.replace("{taskId}", str(task_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def update_task(self, task_id: str, body: dict[str, Any] | None = None) -> Any:
        """Update specified task triggers."""
        endpoint = "/ScheduledTasks/{taskId}/Triggers"
        endpoint = endpoint.replace("{taskId}", str(task_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def start_task(self, task_id: str) -> Any:
        """Start specified task."""
        endpoint = "/ScheduledTasks/Running/{taskId}"
        endpoint = endpoint.replace("{taskId}", str(task_id))
        params = None
        return self.request("POST", endpoint, params=params)

    def stop_task(self, task_id: str) -> Any:
        """Stop specified task."""
        endpoint = "/ScheduledTasks/Running/{taskId}"
        endpoint = endpoint.replace("{taskId}", str(task_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_search_hints(
        self,
        start_index: int | None = None,
        limit: int | None = None,
        user_id: str | None = None,
        search_term: str | None = None,
        include_item_types: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        media_types: list[Any] | None = None,
        parent_id: str | None = None,
        is_movie: bool | None = None,
        is_series: bool | None = None,
        is_news: bool | None = None,
        is_kids: bool | None = None,
        is_sports: bool | None = None,
        include_people: bool | None = None,
        include_media: bool | None = None,
        include_genres: bool | None = None,
        include_studios: bool | None = None,
        include_artists: bool | None = None,
    ) -> Any:
        """Gets the search hint result."""
        endpoint = "/Search/Hints"
        params: dict[str, Any] = {}
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if user_id is not None:
            params["userId"] = user_id
        if search_term is not None:
            params["searchTerm"] = search_term
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if media_types is not None:
            params["mediaTypes"] = media_types
        if parent_id is not None:
            params["parentId"] = parent_id
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_series is not None:
            params["isSeries"] = is_series
        if is_news is not None:
            params["isNews"] = is_news
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_sports is not None:
            params["isSports"] = is_sports
        if include_people is not None:
            params["includePeople"] = include_people
        if include_media is not None:
            params["includeMedia"] = include_media
        if include_genres is not None:
            params["includeGenres"] = include_genres
        if include_studios is not None:
            params["includeStudios"] = include_studios
        if include_artists is not None:
            params["includeArtists"] = include_artists
        return self.request("GET", endpoint, params=params)

    def get_password_reset_providers(self) -> Any:
        """Get all password reset providers."""
        endpoint = "/Auth/PasswordResetProviders"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_auth_providers(self) -> Any:
        """Get all auth providers."""
        endpoint = "/Auth/Providers"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_sessions(
        self,
        controllable_by_user_id: str | None = None,
        device_id: str | None = None,
        active_within_seconds: int | None = None,
    ) -> Any:
        """Gets a list of sessions."""
        endpoint = "/Sessions"
        params: dict[str, Any] = {}
        if controllable_by_user_id is not None:
            params["controllableByUserId"] = controllable_by_user_id
        if device_id is not None:
            params["deviceId"] = device_id
        if active_within_seconds is not None:
            params["activeWithinSeconds"] = active_within_seconds
        return self.request("GET", endpoint, params=params)

    def send_full_general_command(
        self, session_id: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Issues a full general command to a client."""
        endpoint = "/Sessions/{sessionId}/Command"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def send_general_command(self, session_id: str, command: str) -> Any:
        """Issues a general command to a client."""
        endpoint = "/Sessions/{sessionId}/Command/{command}"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        endpoint = endpoint.replace("{command}", str(command))
        params = None
        return self.request("POST", endpoint, params=params)

    def send_message_command(
        self, session_id: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Issues a command to a client to display a message to the user."""
        endpoint = "/Sessions/{sessionId}/Message"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def play(
        self,
        session_id: str,
        play_command: str | None = None,
        item_ids: list[Any] | None = None,
        start_position_ticks: int | None = None,
        media_source_id: str | None = None,
        audio_stream_index: int | None = None,
        subtitle_stream_index: int | None = None,
        start_index: int | None = None,
    ) -> Any:
        """Instructs a session to play an item."""
        endpoint = "/Sessions/{sessionId}/Playing"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        params: dict[str, Any] = {}
        if play_command is not None:
            params["playCommand"] = play_command
        if item_ids is not None:
            params["itemIds"] = item_ids
        if start_position_ticks is not None:
            params["startPositionTicks"] = start_position_ticks
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if start_index is not None:
            params["startIndex"] = start_index
        return self.request("POST", endpoint, params=params)

    def send_playstate_command(
        self,
        session_id: str,
        command: str,
        seek_position_ticks: int | None = None,
        controlling_user_id: str | None = None,
    ) -> Any:
        """Issues a playstate command to a client."""
        endpoint = "/Sessions/{sessionId}/Playing/{command}"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        endpoint = endpoint.replace("{command}", str(command))
        params: dict[str, Any] = {}
        if seek_position_ticks is not None:
            params["seekPositionTicks"] = seek_position_ticks
        if controlling_user_id is not None:
            params["controllingUserId"] = controlling_user_id
        return self.request("POST", endpoint, params=params)

    def send_system_command(self, session_id: str, command: str) -> Any:
        """Issues a system command to a client."""
        endpoint = "/Sessions/{sessionId}/System/{command}"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        endpoint = endpoint.replace("{command}", str(command))
        params = None
        return self.request("POST", endpoint, params=params)

    def add_user_to_session(self, session_id: str, user_id: str) -> Any:
        """Adds an additional user to a session."""
        endpoint = "/Sessions/{sessionId}/User/{userId}"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("POST", endpoint, params=params)

    def remove_user_from_session(self, session_id: str, user_id: str) -> Any:
        """Removes an additional user from a session."""
        endpoint = "/Sessions/{sessionId}/User/{userId}"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def display_content(
        self,
        session_id: str,
        item_type: str | None = None,
        item_id: str | None = None,
        item_name: str | None = None,
    ) -> Any:
        """Instructs a session to browse to an item or view."""
        endpoint = "/Sessions/{sessionId}/Viewing"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        params: dict[str, Any] = {}
        if item_type is not None:
            params["itemType"] = item_type
        if item_id is not None:
            params["itemId"] = item_id
        if item_name is not None:
            params["itemName"] = item_name
        return self.request("POST", endpoint, params=params)

    def post_capabilities(
        self,
        id: str | None = None,
        playable_media_types: list[Any] | None = None,
        supported_commands: list[Any] | None = None,
        supports_media_control: bool | None = None,
        supports_persistent_identifier: bool | None = None,
    ) -> Any:
        """Updates capabilities for a device."""
        endpoint = "/Sessions/Capabilities"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if playable_media_types is not None:
            params["playableMediaTypes"] = playable_media_types
        if supported_commands is not None:
            params["supportedCommands"] = supported_commands
        if supports_media_control is not None:
            params["supportsMediaControl"] = supports_media_control
        if supports_persistent_identifier is not None:
            params["supportsPersistentIdentifier"] = supports_persistent_identifier
        return self.request("POST", endpoint, params=params)

    def post_full_capabilities(
        self, id: str | None = None, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates capabilities for a device."""
        endpoint = "/Sessions/Capabilities/Full"
        params: dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        return self.request("POST", endpoint, params=params, json_data=body)

    def report_session_ended(self) -> Any:
        """Reports that a session has ended."""
        endpoint = "/Sessions/Logout"
        params = None
        return self.request("POST", endpoint, params=params)

    def report_viewing(
        self, session_id: str | None = None, item_id: str | None = None
    ) -> Any:
        """Reports that a session is viewing an item."""
        endpoint = "/Sessions/Viewing"
        params: dict[str, Any] = {}
        if session_id is not None:
            params["sessionId"] = session_id
        if item_id is not None:
            params["itemId"] = item_id
        return self.request("POST", endpoint, params=params)

    def complete_wizard(self) -> Any:
        """Completes the startup wizard."""
        endpoint = "/Startup/Complete"
        params = None
        return self.request("POST", endpoint, params=params)

    def get_startup_configuration(self) -> Any:
        """Gets the initial startup wizard configuration."""
        endpoint = "/Startup/Configuration"
        params = None
        return self.request("GET", endpoint, params=params)

    def update_initial_configuration(self, body: dict[str, Any] | None = None) -> Any:
        """Sets the initial startup wizard configuration."""
        endpoint = "/Startup/Configuration"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_first_user_2(self) -> Any:
        """Gets the first user."""
        endpoint = "/Startup/FirstUser"
        params = None
        return self.request("GET", endpoint, params=params)

    def set_remote_access(self, body: dict[str, Any] | None = None) -> Any:
        """Sets remote access and UPnP."""
        endpoint = "/Startup/RemoteAccess"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_first_user(self) -> Any:
        """Gets the first user."""
        endpoint = "/Startup/User"
        params = None
        return self.request("GET", endpoint, params=params)

    def update_startup_user(self, body: dict[str, Any] | None = None) -> Any:
        """Sets the user name and password."""
        endpoint = "/Startup/User"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_studios(
        self,
        start_index: int | None = None,
        limit: int | None = None,
        search_term: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        is_favorite: bool | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        user_id: str | None = None,
        name_starts_with_or_greater: str | None = None,
        name_starts_with: str | None = None,
        name_less_than: str | None = None,
        enable_images: bool | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets all studios from a given item, folder, or the entire library."""
        endpoint = "/Studios"
        params: dict[str, Any] = {}
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if search_term is not None:
            params["searchTerm"] = search_term
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if user_id is not None:
            params["userId"] = user_id
        if name_starts_with_or_greater is not None:
            params["nameStartsWithOrGreater"] = name_starts_with_or_greater
        if name_starts_with is not None:
            params["nameStartsWith"] = name_starts_with
        if name_less_than is not None:
            params["nameLessThan"] = name_less_than
        if enable_images is not None:
            params["enableImages"] = enable_images
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def get_studio(self, name: str, user_id: str | None = None) -> Any:
        """Gets a studio by name."""
        endpoint = "/Studios/{name}"
        endpoint = endpoint.replace("{name}", str(name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_fallback_font_list(self) -> Any:
        """Gets a list of available fallback font files."""
        endpoint = "/FallbackFont/Fonts"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_fallback_font(self, name: str) -> Any:
        """Gets a fallback font file."""
        endpoint = "/FallbackFont/Fonts/{name}"
        endpoint = endpoint.replace("{name}", str(name))
        params = None
        return self.request("GET", endpoint, params=params)

    def search_remote_subtitles(
        self, item_id: str, language: str, is_perfect_match: bool | None = None
    ) -> Any:
        """Search remote subtitles."""
        endpoint = "/Items/{itemId}/RemoteSearch/Subtitles/{language}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{language}", str(language))
        params: dict[str, Any] = {}
        if is_perfect_match is not None:
            params["isPerfectMatch"] = is_perfect_match
        return self.request("GET", endpoint, params=params)

    def download_remote_subtitles(self, item_id: str, subtitle_id: str) -> Any:
        """Downloads a remote subtitle."""
        endpoint = "/Items/{itemId}/RemoteSearch/Subtitles/{subtitleId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{subtitleId}", str(subtitle_id))
        params = None
        return self.request("POST", endpoint, params=params)

    def get_remote_subtitles(self, subtitle_id: str) -> Any:
        """Gets the remote subtitles."""
        endpoint = "/Providers/Subtitles/Subtitles/{subtitleId}"
        endpoint = endpoint.replace("{subtitleId}", str(subtitle_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_subtitle_playlist(
        self,
        item_id: str,
        index: int,
        media_source_id: str,
        segment_length: int | None = None,
    ) -> Any:
        """Gets an HLS subtitle playlist."""
        endpoint = "/Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/subtitles.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{index}", str(index))
        endpoint = endpoint.replace("{mediaSourceId}", str(media_source_id))
        params: dict[str, Any] = {}
        if segment_length is not None:
            params["segmentLength"] = segment_length
        return self.request("GET", endpoint, params=params)

    def upload_subtitle(self, item_id: str, body: dict[str, Any] | None = None) -> Any:
        """Upload an external subtitle file."""
        endpoint = "/Videos/{itemId}/Subtitles"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def delete_subtitle(self, item_id: str, index: int) -> Any:
        """Deletes an external subtitle file."""
        endpoint = "/Videos/{itemId}/Subtitles/{index}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{index}", str(index))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_subtitle_with_ticks(
        self,
        route_item_id: str,
        route_media_source_id: str,
        route_index: int,
        route_start_position_ticks: int,
        route_format: str,
        item_id: str | None = None,
        media_source_id: str | None = None,
        index: int | None = None,
        start_position_ticks: int | None = None,
        format: str | None = None,
        end_position_ticks: int | None = None,
        copy_timestamps: bool | None = None,
        add_vtt_time_map: bool | None = None,
    ) -> Any:
        """Gets subtitles in a specified format."""
        endpoint = "/Videos/{routeItemId}/{routeMediaSourceId}/Subtitles/{routeIndex}/{routeStartPositionTicks}/Stream.{routeFormat}"
        endpoint = endpoint.replace("{routeItemId}", str(route_item_id))
        endpoint = endpoint.replace("{routeMediaSourceId}", str(route_media_source_id))
        endpoint = endpoint.replace("{routeIndex}", str(route_index))
        endpoint = endpoint.replace(
            "{routeStartPositionTicks}", str(route_start_position_ticks)
        )
        endpoint = endpoint.replace("{routeFormat}", str(route_format))
        params: dict[str, Any] = {}
        if item_id is not None:
            params["itemId"] = item_id
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if index is not None:
            params["index"] = index
        if start_position_ticks is not None:
            params["startPositionTicks"] = start_position_ticks
        if format is not None:
            params["format"] = format
        if end_position_ticks is not None:
            params["endPositionTicks"] = end_position_ticks
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if add_vtt_time_map is not None:
            params["addVttTimeMap"] = add_vtt_time_map
        return self.request("GET", endpoint, params=params)

    def get_subtitle(
        self,
        route_item_id: str,
        route_media_source_id: str,
        route_index: int,
        route_format: str,
        item_id: str | None = None,
        media_source_id: str | None = None,
        index: int | None = None,
        format: str | None = None,
        end_position_ticks: int | None = None,
        copy_timestamps: bool | None = None,
        add_vtt_time_map: bool | None = None,
        start_position_ticks: int | None = None,
    ) -> Any:
        """Gets subtitles in a specified format."""
        endpoint = "/Videos/{routeItemId}/{routeMediaSourceId}/Subtitles/{routeIndex}/Stream.{routeFormat}"
        endpoint = endpoint.replace("{routeItemId}", str(route_item_id))
        endpoint = endpoint.replace("{routeMediaSourceId}", str(route_media_source_id))
        endpoint = endpoint.replace("{routeIndex}", str(route_index))
        endpoint = endpoint.replace("{routeFormat}", str(route_format))
        params: dict[str, Any] = {}
        if item_id is not None:
            params["itemId"] = item_id
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if index is not None:
            params["index"] = index
        if format is not None:
            params["format"] = format
        if end_position_ticks is not None:
            params["endPositionTicks"] = end_position_ticks
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if add_vtt_time_map is not None:
            params["addVttTimeMap"] = add_vtt_time_map
        if start_position_ticks is not None:
            params["startPositionTicks"] = start_position_ticks
        return self.request("GET", endpoint, params=params)

    def get_suggestions(
        self,
        user_id: str | None = None,
        media_type: list[Any] | None = None,
        type: list[Any] | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        enable_total_record_count: bool | None = None,
    ) -> Any:
        """Gets suggestions."""
        endpoint = "/Items/Suggestions"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if media_type is not None:
            params["mediaType"] = media_type
        if type is not None:
            params["type"] = type
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        return self.request("GET", endpoint, params=params)

    def sync_play_get_group(self, id: str) -> Any:
        """Gets a SyncPlay group by id."""
        endpoint = "/SyncPlay/{id}"
        endpoint = endpoint.replace("{id}", str(id))
        params = None
        return self.request("GET", endpoint, params=params)

    def sync_play_buffering(self, body: dict[str, Any] | None = None) -> Any:
        """Notify SyncPlay group that member is buffering."""
        endpoint = "/SyncPlay/Buffering"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_join_group(self, body: dict[str, Any] | None = None) -> Any:
        """Join an existing SyncPlay group."""
        endpoint = "/SyncPlay/Join"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_leave_group(self) -> Any:
        """Leave the joined SyncPlay group."""
        endpoint = "/SyncPlay/Leave"
        params = None
        return self.request("POST", endpoint, params=params)

    def sync_play_get_groups(self) -> Any:
        """Gets all SyncPlay groups."""
        endpoint = "/SyncPlay/List"
        params = None
        return self.request("GET", endpoint, params=params)

    def sync_play_move_playlist_item(self, body: dict[str, Any] | None = None) -> Any:
        """Request to move an item in the playlist in SyncPlay group."""
        endpoint = "/SyncPlay/MovePlaylistItem"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_create_group(self, body: dict[str, Any] | None = None) -> Any:
        """Create a new SyncPlay group."""
        endpoint = "/SyncPlay/New"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_next_item(self, body: dict[str, Any] | None = None) -> Any:
        """Request next item in SyncPlay group."""
        endpoint = "/SyncPlay/NextItem"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_pause(self) -> Any:
        """Request pause in SyncPlay group."""
        endpoint = "/SyncPlay/Pause"
        params = None
        return self.request("POST", endpoint, params=params)

    def sync_play_ping(self, body: dict[str, Any] | None = None) -> Any:
        """Update session ping."""
        endpoint = "/SyncPlay/Ping"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_previous_item(self, body: dict[str, Any] | None = None) -> Any:
        """Request previous item in SyncPlay group."""
        endpoint = "/SyncPlay/PreviousItem"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_queue(self, body: dict[str, Any] | None = None) -> Any:
        """Request to queue items to the playlist of a SyncPlay group."""
        endpoint = "/SyncPlay/Queue"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_ready(self, body: dict[str, Any] | None = None) -> Any:
        """Notify SyncPlay group that member is ready for playback."""
        endpoint = "/SyncPlay/Ready"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_remove_from_playlist(self, body: dict[str, Any] | None = None) -> Any:
        """Request to remove items from the playlist in SyncPlay group."""
        endpoint = "/SyncPlay/RemoveFromPlaylist"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_seek(self, body: dict[str, Any] | None = None) -> Any:
        """Request seek in SyncPlay group."""
        endpoint = "/SyncPlay/Seek"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_set_ignore_wait(self, body: dict[str, Any] | None = None) -> Any:
        """Request SyncPlay group to ignore member during group-wait."""
        endpoint = "/SyncPlay/SetIgnoreWait"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_set_new_queue(self, body: dict[str, Any] | None = None) -> Any:
        """Request to set new playlist in SyncPlay group."""
        endpoint = "/SyncPlay/SetNewQueue"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_set_playlist_item(self, body: dict[str, Any] | None = None) -> Any:
        """Request to change playlist item in SyncPlay group."""
        endpoint = "/SyncPlay/SetPlaylistItem"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_set_repeat_mode(self, body: dict[str, Any] | None = None) -> Any:
        """Request to set repeat mode in SyncPlay group."""
        endpoint = "/SyncPlay/SetRepeatMode"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_set_shuffle_mode(self, body: dict[str, Any] | None = None) -> Any:
        """Request to set shuffle mode in SyncPlay group."""
        endpoint = "/SyncPlay/SetShuffleMode"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def sync_play_stop(self) -> Any:
        """Request stop in SyncPlay group."""
        endpoint = "/SyncPlay/Stop"
        params = None
        return self.request("POST", endpoint, params=params)

    def sync_play_unpause(self) -> Any:
        """Request unpause in SyncPlay group."""
        endpoint = "/SyncPlay/Unpause"
        params = None
        return self.request("POST", endpoint, params=params)

    def get_endpoint_info(self) -> Any:
        """Gets information about the request endpoint."""
        endpoint = "/System/Endpoint"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_system_info(self) -> Any:
        """Gets information about the server."""
        endpoint = "/System/Info"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_public_system_info(self) -> Any:
        """Gets public information about the server."""
        endpoint = "/System/Info/Public"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_system_storage(self) -> Any:
        """Gets information about the server."""
        endpoint = "/System/Info/Storage"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_server_logs(self) -> Any:
        """Gets a list of available server log files."""
        endpoint = "/System/Logs"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_log_file(self, name: str | None = None) -> Any:
        """Gets a log file."""
        endpoint = "/System/Logs/Log"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        return self.request("GET", endpoint, params=params)

    def get_ping_system(self) -> Any:
        """Pings the system."""
        endpoint = "/System/Ping"
        params = None
        return self.request("GET", endpoint, params=params)

    def post_ping_system(self) -> Any:
        """Pings the system."""
        endpoint = "/System/Ping"
        params = None
        return self.request("POST", endpoint, params=params)

    def restart_application(self) -> Any:
        """Restarts the application."""
        endpoint = "/System/Restart"
        params = None
        return self.request("POST", endpoint, params=params)

    def shutdown_application(self) -> Any:
        """Shuts down the application."""
        endpoint = "/System/Shutdown"
        params = None
        return self.request("POST", endpoint, params=params)

    def get_utc_time(self) -> Any:
        """Gets the current UTC time."""
        endpoint = "/GetUtcTime"
        params = None
        return self.request("GET", endpoint, params=params)

    def tmdb_client_configuration(self) -> Any:
        """Gets the TMDb image configuration options."""
        endpoint = "/Tmdb/ClientConfiguration"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_trailers(
        self,
        user_id: str | None = None,
        max_official_rating: str | None = None,
        has_theme_song: bool | None = None,
        has_theme_video: bool | None = None,
        has_subtitles: bool | None = None,
        has_special_feature: bool | None = None,
        has_trailer: bool | None = None,
        adjacent_to: str | None = None,
        parent_index_number: int | None = None,
        has_parental_rating: bool | None = None,
        is_hd: bool | None = None,
        is4_k: bool | None = None,
        location_types: list[Any] | None = None,
        exclude_location_types: list[Any] | None = None,
        is_missing: bool | None = None,
        is_unaired: bool | None = None,
        min_community_rating: float | None = None,
        min_critic_rating: float | None = None,
        min_premiere_date: str | None = None,
        min_date_last_saved: str | None = None,
        min_date_last_saved_for_user: str | None = None,
        max_premiere_date: str | None = None,
        has_overview: bool | None = None,
        has_imdb_id: bool | None = None,
        has_tmdb_id: bool | None = None,
        has_tvdb_id: bool | None = None,
        is_movie: bool | None = None,
        is_series: bool | None = None,
        is_news: bool | None = None,
        is_kids: bool | None = None,
        is_sports: bool | None = None,
        exclude_item_ids: list[Any] | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        recursive: bool | None = None,
        search_term: str | None = None,
        sort_order: list[Any] | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        filters: list[Any] | None = None,
        is_favorite: bool | None = None,
        media_types: list[Any] | None = None,
        image_types: list[Any] | None = None,
        sort_by: list[Any] | None = None,
        is_played: bool | None = None,
        genres: list[Any] | None = None,
        official_ratings: list[Any] | None = None,
        tags: list[Any] | None = None,
        years: list[Any] | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        person: str | None = None,
        person_ids: list[Any] | None = None,
        person_types: list[Any] | None = None,
        studios: list[Any] | None = None,
        artists: list[Any] | None = None,
        exclude_artist_ids: list[Any] | None = None,
        artist_ids: list[Any] | None = None,
        album_artist_ids: list[Any] | None = None,
        contributing_artist_ids: list[Any] | None = None,
        albums: list[Any] | None = None,
        album_ids: list[Any] | None = None,
        ids: list[Any] | None = None,
        video_types: list[Any] | None = None,
        min_official_rating: str | None = None,
        is_locked: bool | None = None,
        is_place_holder: bool | None = None,
        has_official_rating: bool | None = None,
        collapse_box_set_items: bool | None = None,
        min_width: int | None = None,
        min_height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        is3_d: bool | None = None,
        series_status: list[Any] | None = None,
        name_starts_with_or_greater: str | None = None,
        name_starts_with: str | None = None,
        name_less_than: str | None = None,
        studio_ids: list[Any] | None = None,
        genre_ids: list[Any] | None = None,
        enable_total_record_count: bool | None = None,
        enable_images: bool | None = None,
    ) -> Any:
        """Finds movies and trailers similar to a given trailer."""
        endpoint = "/Trailers"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if max_official_rating is not None:
            params["maxOfficialRating"] = max_official_rating
        if has_theme_song is not None:
            params["hasThemeSong"] = has_theme_song
        if has_theme_video is not None:
            params["hasThemeVideo"] = has_theme_video
        if has_subtitles is not None:
            params["hasSubtitles"] = has_subtitles
        if has_special_feature is not None:
            params["hasSpecialFeature"] = has_special_feature
        if has_trailer is not None:
            params["hasTrailer"] = has_trailer
        if adjacent_to is not None:
            params["adjacentTo"] = adjacent_to
        if parent_index_number is not None:
            params["parentIndexNumber"] = parent_index_number
        if has_parental_rating is not None:
            params["hasParentalRating"] = has_parental_rating
        if is_hd is not None:
            params["isHd"] = is_hd
        if is4_k is not None:
            params["is4K"] = is4_k
        if location_types is not None:
            params["locationTypes"] = location_types
        if exclude_location_types is not None:
            params["excludeLocationTypes"] = exclude_location_types
        if is_missing is not None:
            params["isMissing"] = is_missing
        if is_unaired is not None:
            params["isUnaired"] = is_unaired
        if min_community_rating is not None:
            params["minCommunityRating"] = min_community_rating
        if min_critic_rating is not None:
            params["minCriticRating"] = min_critic_rating
        if min_premiere_date is not None:
            params["minPremiereDate"] = min_premiere_date
        if min_date_last_saved is not None:
            params["minDateLastSaved"] = min_date_last_saved
        if min_date_last_saved_for_user is not None:
            params["minDateLastSavedForUser"] = min_date_last_saved_for_user
        if max_premiere_date is not None:
            params["maxPremiereDate"] = max_premiere_date
        if has_overview is not None:
            params["hasOverview"] = has_overview
        if has_imdb_id is not None:
            params["hasImdbId"] = has_imdb_id
        if has_tmdb_id is not None:
            params["hasTmdbId"] = has_tmdb_id
        if has_tvdb_id is not None:
            params["hasTvdbId"] = has_tvdb_id
        if is_movie is not None:
            params["isMovie"] = is_movie
        if is_series is not None:
            params["isSeries"] = is_series
        if is_news is not None:
            params["isNews"] = is_news
        if is_kids is not None:
            params["isKids"] = is_kids
        if is_sports is not None:
            params["isSports"] = is_sports
        if exclude_item_ids is not None:
            params["excludeItemIds"] = exclude_item_ids
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if recursive is not None:
            params["recursive"] = recursive
        if search_term is not None:
            params["searchTerm"] = search_term
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if filters is not None:
            params["filters"] = filters
        if is_favorite is not None:
            params["isFavorite"] = is_favorite
        if media_types is not None:
            params["mediaTypes"] = media_types
        if image_types is not None:
            params["imageTypes"] = image_types
        if sort_by is not None:
            params["sortBy"] = sort_by
        if is_played is not None:
            params["isPlayed"] = is_played
        if genres is not None:
            params["genres"] = genres
        if official_ratings is not None:
            params["officialRatings"] = official_ratings
        if tags is not None:
            params["tags"] = tags
        if years is not None:
            params["years"] = years
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if person is not None:
            params["person"] = person
        if person_ids is not None:
            params["personIds"] = person_ids
        if person_types is not None:
            params["personTypes"] = person_types
        if studios is not None:
            params["studios"] = studios
        if artists is not None:
            params["artists"] = artists
        if exclude_artist_ids is not None:
            params["excludeArtistIds"] = exclude_artist_ids
        if artist_ids is not None:
            params["artistIds"] = artist_ids
        if album_artist_ids is not None:
            params["albumArtistIds"] = album_artist_ids
        if contributing_artist_ids is not None:
            params["contributingArtistIds"] = contributing_artist_ids
        if albums is not None:
            params["albums"] = albums
        if album_ids is not None:
            params["albumIds"] = album_ids
        if ids is not None:
            params["ids"] = ids
        if video_types is not None:
            params["videoTypes"] = video_types
        if min_official_rating is not None:
            params["minOfficialRating"] = min_official_rating
        if is_locked is not None:
            params["isLocked"] = is_locked
        if is_place_holder is not None:
            params["isPlaceHolder"] = is_place_holder
        if has_official_rating is not None:
            params["hasOfficialRating"] = has_official_rating
        if collapse_box_set_items is not None:
            params["collapseBoxSetItems"] = collapse_box_set_items
        if min_width is not None:
            params["minWidth"] = min_width
        if min_height is not None:
            params["minHeight"] = min_height
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if is3_d is not None:
            params["is3D"] = is3_d
        if series_status is not None:
            params["seriesStatus"] = series_status
        if name_starts_with_or_greater is not None:
            params["nameStartsWithOrGreater"] = name_starts_with_or_greater
        if name_starts_with is not None:
            params["nameStartsWith"] = name_starts_with
        if name_less_than is not None:
            params["nameLessThan"] = name_less_than
        if studio_ids is not None:
            params["studioIds"] = studio_ids
        if genre_ids is not None:
            params["genreIds"] = genre_ids
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        if enable_images is not None:
            params["enableImages"] = enable_images
        return self.request("GET", endpoint, params=params)

    def get_trickplay_tile_image(
        self,
        item_id: str,
        width: int,
        index: int,
        media_source_id: str | None = None,
    ) -> Any:
        """Gets a trickplay tile image."""
        endpoint = "/Videos/{itemId}/Trickplay/{width}/{index}.jpg"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{width}", str(width))
        endpoint = endpoint.replace("{index}", str(index))
        params: dict[str, Any] = {}
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        return self.request("GET", endpoint, params=params)

    def get_trickplay_hls_playlist(
        self, item_id: str, width: int, media_source_id: str | None = None
    ) -> Any:
        """Gets an image tiles playlist for trickplay."""
        endpoint = "/Videos/{itemId}/Trickplay/{width}/tiles.m3u8"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{width}", str(width))
        params: dict[str, Any] = {}
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        return self.request("GET", endpoint, params=params)

    def get_episodes(
        self,
        series_id: str,
        user_id: str | None = None,
        fields: list[Any] | None = None,
        season: int | None = None,
        season_id: str | None = None,
        is_missing: bool | None = None,
        adjacent_to: str | None = None,
        start_item_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        enable_user_data: bool | None = None,
        sort_by: str | None = None,
    ) -> Any:
        """Gets episodes for a tv season."""
        endpoint = "/Shows/{seriesId}/Episodes"
        endpoint = endpoint.replace("{seriesId}", str(series_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if fields is not None:
            params["fields"] = fields
        if season is not None:
            params["season"] = season
        if season_id is not None:
            params["seasonId"] = season_id
        if is_missing is not None:
            params["isMissing"] = is_missing
        if adjacent_to is not None:
            params["adjacentTo"] = adjacent_to
        if start_item_id is not None:
            params["startItemId"] = start_item_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if sort_by is not None:
            params["sortBy"] = sort_by
        return self.request("GET", endpoint, params=params)

    def get_seasons(
        self,
        series_id: str,
        user_id: str | None = None,
        fields: list[Any] | None = None,
        is_special_season: bool | None = None,
        is_missing: bool | None = None,
        adjacent_to: str | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        enable_user_data: bool | None = None,
    ) -> Any:
        """Gets seasons for a tv series."""
        endpoint = "/Shows/{seriesId}/Seasons"
        endpoint = endpoint.replace("{seriesId}", str(series_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if fields is not None:
            params["fields"] = fields
        if is_special_season is not None:
            params["isSpecialSeason"] = is_special_season
        if is_missing is not None:
            params["isMissing"] = is_missing
        if adjacent_to is not None:
            params["adjacentTo"] = adjacent_to
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        return self.request("GET", endpoint, params=params)

    def get_next_up(
        self,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        series_id: str | None = None,
        parent_id: str | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        enable_user_data: bool | None = None,
        next_up_date_cutoff: str | None = None,
        enable_total_record_count: bool | None = None,
        disable_first_episode: bool | None = None,
        enable_resumable: bool | None = None,
        enable_rewatching: bool | None = None,
    ) -> Any:
        """Gets a list of next up episodes."""
        endpoint = "/Shows/NextUp"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if series_id is not None:
            params["seriesId"] = series_id
        if parent_id is not None:
            params["parentId"] = parent_id
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if next_up_date_cutoff is not None:
            params["nextUpDateCutoff"] = next_up_date_cutoff
        if enable_total_record_count is not None:
            params["enableTotalRecordCount"] = enable_total_record_count
        if disable_first_episode is not None:
            params["disableFirstEpisode"] = disable_first_episode
        if enable_resumable is not None:
            params["enableResumable"] = enable_resumable
        if enable_rewatching is not None:
            params["enableRewatching"] = enable_rewatching
        return self.request("GET", endpoint, params=params)

    def get_upcoming_episodes(
        self,
        user_id: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[Any] | None = None,
        parent_id: str | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        enable_user_data: bool | None = None,
    ) -> Any:
        """Gets a list of upcoming episodes."""
        endpoint = "/Shows/Upcoming"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if fields is not None:
            params["fields"] = fields
        if parent_id is not None:
            params["parentId"] = parent_id
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        return self.request("GET", endpoint, params=params)

    def get_universal_audio_stream(
        self,
        item_id: str,
        container: list[Any] | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        user_id: str | None = None,
        audio_codec: str | None = None,
        max_audio_channels: int | None = None,
        transcoding_audio_channels: int | None = None,
        max_streaming_bitrate: int | None = None,
        audio_bit_rate: int | None = None,
        start_time_ticks: int | None = None,
        transcoding_container: str | None = None,
        transcoding_protocol: str | None = None,
        max_audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        enable_remote_media: bool | None = None,
        enable_audio_vbr_encoding: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        enable_redirection: bool | None = None,
    ) -> Any:
        """Gets an audio stream."""
        endpoint = "/Audio/{itemId}/universal"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if container is not None:
            params["container"] = container
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if user_id is not None:
            params["userId"] = user_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if transcoding_audio_channels is not None:
            params["transcodingAudioChannels"] = transcoding_audio_channels
        if max_streaming_bitrate is not None:
            params["maxStreamingBitrate"] = max_streaming_bitrate
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if transcoding_container is not None:
            params["transcodingContainer"] = transcoding_container
        if transcoding_protocol is not None:
            params["transcodingProtocol"] = transcoding_protocol
        if max_audio_sample_rate is not None:
            params["maxAudioSampleRate"] = max_audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if enable_remote_media is not None:
            params["enableRemoteMedia"] = enable_remote_media
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if enable_redirection is not None:
            params["enableRedirection"] = enable_redirection
        return self.request("GET", endpoint, params=params)

    def get_users(
        self, is_hidden: bool | None = None, is_disabled: bool | None = None
    ) -> Any:
        """Gets a list of users."""
        endpoint = "/Users"
        params: dict[str, Any] = {}
        if is_hidden is not None:
            params["isHidden"] = is_hidden
        if is_disabled is not None:
            params["isDisabled"] = is_disabled
        return self.request("GET", endpoint, params=params)

    def update_user(
        self, user_id: str | None = None, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates a user."""
        endpoint = "/Users"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_user_by_id(self, user_id: str) -> Any:
        """Gets a user by Id."""
        endpoint = "/Users/{userId}"
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("GET", endpoint, params=params)

    def delete_user(self, user_id: str) -> Any:
        """Deletes a user."""
        endpoint = "/Users/{userId}"
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def update_user_policy(
        self, user_id: str, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates a user policy."""
        endpoint = "/Users/{userId}/Policy"
        endpoint = endpoint.replace("{userId}", str(user_id))
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def authenticate_user_by_name(self, body: dict[str, Any] | None = None) -> Any:
        """Authenticates a user by name."""
        endpoint = "/Users/AuthenticateByName"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def authenticate_with_quick_connect(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Authenticates a user with quick connect."""
        endpoint = "/Users/AuthenticateWithQuickConnect"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def update_user_configuration(
        self, user_id: str | None = None, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates a user configuration."""
        endpoint = "/Users/Configuration"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params, json_data=body)

    def forgot_password(self, body: dict[str, Any] | None = None) -> Any:
        """Initiates the forgot password process for a local user."""
        endpoint = "/Users/ForgotPassword"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def forgot_password_pin(self, body: dict[str, Any] | None = None) -> Any:
        """Redeems a forgot password pin."""
        endpoint = "/Users/ForgotPassword/Pin"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_current_user(self) -> Any:
        """Gets the user based on auth token."""
        endpoint = "/Users/Me"
        params = None
        return self.request("GET", endpoint, params=params)

    def create_user_by_name(self, body: dict[str, Any] | None = None) -> Any:
        """Creates a user."""
        endpoint = "/Users/New"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

    def update_user_password(
        self, user_id: str | None = None, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates a user's password."""
        endpoint = "/Users/Password"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_public_users(self) -> Any:
        """Gets a list of publicly visible users for display on a login screen."""
        endpoint = "/Users/Public"
        params = None
        return self.request("GET", endpoint, params=params)

    def get_intros(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets intros to play before the main media item plays."""
        endpoint = "/Items/{itemId}/Intros"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_local_trailers(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets local trailers for an item."""
        endpoint = "/Items/{itemId}/LocalTrailers"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_special_features(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets special features for an item."""
        endpoint = "/Items/{itemId}/SpecialFeatures"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_latest_media(
        self,
        user_id: str | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        is_played: bool | None = None,
        enable_images: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        enable_user_data: bool | None = None,
        limit: int | None = None,
        group_items: bool | None = None,
    ) -> Any:
        """Gets latest media."""
        endpoint = "/Items/Latest"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if is_played is not None:
            params["isPlayed"] = is_played
        if enable_images is not None:
            params["enableImages"] = enable_images
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if limit is not None:
            params["limit"] = limit
        if group_items is not None:
            params["groupItems"] = group_items
        return self.request("GET", endpoint, params=params)

    def get_root_folder(self, user_id: str | None = None) -> Any:
        """Gets the root folder from a user's library."""
        endpoint = "/Items/Root"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def mark_favorite_item(self, item_id: str, user_id: str | None = None) -> Any:
        """Marks an item as a favorite."""
        endpoint = "/UserFavoriteItems/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params)

    def unmark_favorite_item(self, item_id: str, user_id: str | None = None) -> Any:
        """Unmarks item as a favorite."""
        endpoint = "/UserFavoriteItems/{itemId}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("DELETE", endpoint, params=params)

    def delete_user_item_rating(self, item_id: str, user_id: str | None = None) -> Any:
        """Deletes a user's saved personal rating for an item."""
        endpoint = "/UserItems/{itemId}/Rating"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("DELETE", endpoint, params=params)

    def update_user_item_rating(
        self, item_id: str, user_id: str | None = None, likes: bool | None = None
    ) -> Any:
        """Updates a user's rating for an item."""
        endpoint = "/UserItems/{itemId}/Rating"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if likes is not None:
            params["likes"] = likes
        return self.request("POST", endpoint, params=params)

    def get_user_views(
        self,
        user_id: str | None = None,
        include_external_content: bool | None = None,
        preset_views: list[Any] | None = None,
        include_hidden: bool | None = None,
    ) -> Any:
        """Get user views."""
        endpoint = "/UserViews"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if include_external_content is not None:
            params["includeExternalContent"] = include_external_content
        if preset_views is not None:
            params["presetViews"] = preset_views
        if include_hidden is not None:
            params["includeHidden"] = include_hidden
        return self.request("GET", endpoint, params=params)

    def get_grouping_options(self, user_id: str | None = None) -> Any:
        """Get user view grouping options."""
        endpoint = "/UserViews/GroupingOptions"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def get_attachment(self, video_id: str, media_source_id: str, index: int) -> Any:
        """Get video attachment."""
        endpoint = "/Videos/{videoId}/{mediaSourceId}/Attachments/{index}"
        endpoint = endpoint.replace("{videoId}", str(video_id))
        endpoint = endpoint.replace("{mediaSourceId}", str(media_source_id))
        endpoint = endpoint.replace("{index}", str(index))
        params = None
        return self.request("GET", endpoint, params=params)

    def get_additional_part(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets additional parts for a video."""
        endpoint = "/Videos/{itemId}/AdditionalParts"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

    def delete_alternate_sources(self, item_id: str) -> Any:
        """Removes alternate video sources."""
        endpoint = "/Videos/{itemId}/AlternateSources"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params = None
        return self.request("DELETE", endpoint, params=params)

    def get_video_stream(
        self,
        item_id: str,
        container: str | None = None,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
    ) -> Any:
        """Gets a video stream."""
        endpoint = "/Videos/{itemId}/stream"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        params: dict[str, Any] = {}
        if container is not None:
            params["container"] = container
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        return self.request("GET", endpoint, params=params)

    def get_video_stream_by_container(
        self,
        item_id: str,
        container: str,
        static: bool | None = None,
        stream_params: str | None = None,
        tag: str | None = None,
        device_profile_id: str | None = None,
        play_session_id: str | None = None,
        segment_container: str | None = None,
        segment_length: int | None = None,
        min_segments: int | None = None,
        media_source_id: str | None = None,
        device_id: str | None = None,
        audio_codec: str | None = None,
        enable_auto_stream_copy: bool | None = None,
        allow_video_stream_copy: bool | None = None,
        allow_audio_stream_copy: bool | None = None,
        break_on_non_key_frames: bool | None = None,
        audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        audio_bit_rate: int | None = None,
        audio_channels: int | None = None,
        max_audio_channels: int | None = None,
        profile: str | None = None,
        level: str | None = None,
        framerate: float | None = None,
        max_framerate: float | None = None,
        copy_timestamps: bool | None = None,
        start_time_ticks: int | None = None,
        width: int | None = None,
        height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        video_bit_rate: int | None = None,
        subtitle_stream_index: int | None = None,
        subtitle_method: str | None = None,
        max_ref_frames: int | None = None,
        max_video_bit_depth: int | None = None,
        require_avc: bool | None = None,
        de_interlace: bool | None = None,
        require_non_anamorphic: bool | None = None,
        transcoding_max_audio_channels: int | None = None,
        cpu_core_limit: int | None = None,
        live_stream_id: str | None = None,
        enable_mpegts_m2_ts_mode: bool | None = None,
        video_codec: str | None = None,
        subtitle_codec: str | None = None,
        transcode_reasons: str | None = None,
        audio_stream_index: int | None = None,
        video_stream_index: int | None = None,
        context: str | None = None,
        stream_options: dict[str, Any] | None = None,
        enable_audio_vbr_encoding: bool | None = None,
    ) -> Any:
        """Gets a video stream."""
        endpoint = "/Videos/{itemId}/stream.{container}"
        endpoint = endpoint.replace("{itemId}", str(item_id))
        endpoint = endpoint.replace("{container}", str(container))
        params: dict[str, Any] = {}
        if static is not None:
            params["static"] = static
        if stream_params is not None:
            params["params"] = stream_params
        if tag is not None:
            params["tag"] = tag
        if device_profile_id is not None:
            params["deviceProfileId"] = device_profile_id
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        if segment_container is not None:
            params["segmentContainer"] = segment_container
        if segment_length is not None:
            params["segmentLength"] = segment_length
        if min_segments is not None:
            params["minSegments"] = min_segments
        if media_source_id is not None:
            params["mediaSourceId"] = media_source_id
        if device_id is not None:
            params["deviceId"] = device_id
        if audio_codec is not None:
            params["audioCodec"] = audio_codec
        if enable_auto_stream_copy is not None:
            params["enableAutoStreamCopy"] = enable_auto_stream_copy
        if allow_video_stream_copy is not None:
            params["allowVideoStreamCopy"] = allow_video_stream_copy
        if allow_audio_stream_copy is not None:
            params["allowAudioStreamCopy"] = allow_audio_stream_copy
        if break_on_non_key_frames is not None:
            params["breakOnNonKeyFrames"] = break_on_non_key_frames
        if audio_sample_rate is not None:
            params["audioSampleRate"] = audio_sample_rate
        if max_audio_bit_depth is not None:
            params["maxAudioBitDepth"] = max_audio_bit_depth
        if audio_bit_rate is not None:
            params["audioBitRate"] = audio_bit_rate
        if audio_channels is not None:
            params["audioChannels"] = audio_channels
        if max_audio_channels is not None:
            params["maxAudioChannels"] = max_audio_channels
        if profile is not None:
            params["profile"] = profile
        if level is not None:
            params["level"] = level
        if framerate is not None:
            params["framerate"] = framerate
        if max_framerate is not None:
            params["maxFramerate"] = max_framerate
        if copy_timestamps is not None:
            params["copyTimestamps"] = copy_timestamps
        if start_time_ticks is not None:
            params["startTimeTicks"] = start_time_ticks
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        if video_bit_rate is not None:
            params["videoBitRate"] = video_bit_rate
        if subtitle_stream_index is not None:
            params["subtitleStreamIndex"] = subtitle_stream_index
        if subtitle_method is not None:
            params["subtitleMethod"] = subtitle_method
        if max_ref_frames is not None:
            params["maxRefFrames"] = max_ref_frames
        if max_video_bit_depth is not None:
            params["maxVideoBitDepth"] = max_video_bit_depth
        if require_avc is not None:
            params["requireAvc"] = require_avc
        if de_interlace is not None:
            params["deInterlace"] = de_interlace
        if require_non_anamorphic is not None:
            params["requireNonAnamorphic"] = require_non_anamorphic
        if transcoding_max_audio_channels is not None:
            params["transcodingMaxAudioChannels"] = transcoding_max_audio_channels
        if cpu_core_limit is not None:
            params["cpuCoreLimit"] = cpu_core_limit
        if live_stream_id is not None:
            params["liveStreamId"] = live_stream_id
        if enable_mpegts_m2_ts_mode is not None:
            params["enableMpegtsM2TsMode"] = enable_mpegts_m2_ts_mode
        if video_codec is not None:
            params["videoCodec"] = video_codec
        if subtitle_codec is not None:
            params["subtitleCodec"] = subtitle_codec
        if transcode_reasons is not None:
            params["transcodeReasons"] = transcode_reasons
        if audio_stream_index is not None:
            params["audioStreamIndex"] = audio_stream_index
        if video_stream_index is not None:
            params["videoStreamIndex"] = video_stream_index
        if context is not None:
            params["context"] = context
        if stream_options is not None:
            params["streamOptions"] = stream_options
        if enable_audio_vbr_encoding is not None:
            params["enableAudioVbrEncoding"] = enable_audio_vbr_encoding
        return self.request("GET", endpoint, params=params)

    def merge_versions(self, ids: list[Any] | None = None) -> Any:
        """Merges videos into a single record."""
        endpoint = "/Videos/MergeVersions"
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        return self.request("POST", endpoint, params=params)

    def get_years(
        self,
        start_index: int | None = None,
        limit: int | None = None,
        sort_order: list[Any] | None = None,
        parent_id: str | None = None,
        fields: list[Any] | None = None,
        exclude_item_types: list[Any] | None = None,
        include_item_types: list[Any] | None = None,
        media_types: list[Any] | None = None,
        sort_by: list[Any] | None = None,
        enable_user_data: bool | None = None,
        image_type_limit: int | None = None,
        enable_image_types: list[Any] | None = None,
        user_id: str | None = None,
        recursive: bool | None = None,
        enable_images: bool | None = None,
    ) -> Any:
        """Get years."""
        endpoint = "/Years"
        params: dict[str, Any] = {}
        if start_index is not None:
            params["startIndex"] = start_index
        if limit is not None:
            params["limit"] = limit
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if parent_id is not None:
            params["parentId"] = parent_id
        if fields is not None:
            params["fields"] = fields
        if exclude_item_types is not None:
            params["excludeItemTypes"] = exclude_item_types
        if include_item_types is not None:
            params["includeItemTypes"] = include_item_types
        if media_types is not None:
            params["mediaTypes"] = media_types
        if sort_by is not None:
            params["sortBy"] = sort_by
        if enable_user_data is not None:
            params["enableUserData"] = enable_user_data
        if image_type_limit is not None:
            params["imageTypeLimit"] = image_type_limit
        if enable_image_types is not None:
            params["enableImageTypes"] = enable_image_types
        if user_id is not None:
            params["userId"] = user_id
        if recursive is not None:
            params["recursive"] = recursive
        if enable_images is not None:
            params["enableImages"] = enable_images
        return self.request("GET", endpoint, params=params)

    def get_year(self, year: int, user_id: str | None = None) -> Any:
        """Gets a year."""
        endpoint = "/Years/{year}"
        endpoint = endpoint.replace("{year}", str(year))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)
