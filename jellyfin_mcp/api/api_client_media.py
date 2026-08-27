# Generated Media client
from typing import Any

from jellyfin_mcp.api.api_client_base import ApiBase


def _put_if_not_none(params: dict[str, Any], key: str, value: Any) -> None:
    """Set params[key] = value iff value was provided (mirrors the generated
    client's `if <arg> is not None: params[<key>] = <arg>` call-site idiom).

    Preserves falsy-but-provided values (False, 0, "", [], {}) exactly as
    the inline `is not None` checks did; this is not a truthiness check.
    """
    if value is not None:
        params[key] = value


class MediaClient(ApiBase):
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
        _put_if_not_none(params, "runtimeTicks", runtime_ticks)
        _put_if_not_none(params, "actualSegmentLengthTicks", actual_segment_length_ticks)
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "maxStreamingBitrate", max_streaming_bitrate)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
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
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "maxStreamingBitrate", max_streaming_bitrate)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "enableAdaptiveBitrateStreaming", enable_adaptive_bitrate_streaming)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
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
        _put_if_not_none(params, "runtimeTicks", runtime_ticks)
        _put_if_not_none(params, "actualSegmentLengthTicks", actual_segment_length_ticks)
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
        _put_if_not_none(params, "alwaysBurnInSubtitleWhenTranscoding", always_burn_in_subtitle_when_transcoding)
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
        _put_if_not_none(params, "container", container)
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "enableSubtitlesInManifest", enable_subtitles_in_manifest)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
        _put_if_not_none(params, "alwaysBurnInSubtitleWhenTranscoding", always_burn_in_subtitle_when_transcoding)
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
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
        _put_if_not_none(params, "alwaysBurnInSubtitleWhenTranscoding", always_burn_in_subtitle_when_transcoding)
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
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "enableAdaptiveBitrateStreaming", enable_adaptive_bitrate_streaming)
        _put_if_not_none(params, "enableTrickplay", enable_trickplay)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
        _put_if_not_none(params, "alwaysBurnInSubtitleWhenTranscoding", always_burn_in_subtitle_when_transcoding)
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

    def get_trailer_remote_search_results(
        self, body: dict[str, Any] | None = None
    ) -> Any:
        """Get trailer remote search."""
        endpoint = "/Items/RemoteSearch/Trailer"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

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
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "maxOfficialRating", max_official_rating)
        _put_if_not_none(params, "hasThemeSong", has_theme_song)
        _put_if_not_none(params, "hasThemeVideo", has_theme_video)
        _put_if_not_none(params, "hasSubtitles", has_subtitles)
        _put_if_not_none(params, "hasSpecialFeature", has_special_feature)
        _put_if_not_none(params, "hasTrailer", has_trailer)
        _put_if_not_none(params, "adjacentTo", adjacent_to)
        _put_if_not_none(params, "parentIndexNumber", parent_index_number)
        _put_if_not_none(params, "hasParentalRating", has_parental_rating)
        _put_if_not_none(params, "isHd", is_hd)
        _put_if_not_none(params, "is4K", is4_k)
        _put_if_not_none(params, "locationTypes", location_types)
        _put_if_not_none(params, "excludeLocationTypes", exclude_location_types)
        _put_if_not_none(params, "isMissing", is_missing)
        _put_if_not_none(params, "isUnaired", is_unaired)
        _put_if_not_none(params, "minCommunityRating", min_community_rating)
        _put_if_not_none(params, "minCriticRating", min_critic_rating)
        _put_if_not_none(params, "minPremiereDate", min_premiere_date)
        _put_if_not_none(params, "minDateLastSaved", min_date_last_saved)
        _put_if_not_none(params, "minDateLastSavedForUser", min_date_last_saved_for_user)
        _put_if_not_none(params, "maxPremiereDate", max_premiere_date)
        _put_if_not_none(params, "hasOverview", has_overview)
        _put_if_not_none(params, "hasImdbId", has_imdb_id)
        _put_if_not_none(params, "hasTmdbId", has_tmdb_id)
        _put_if_not_none(params, "hasTvdbId", has_tvdb_id)
        _put_if_not_none(params, "isMovie", is_movie)
        _put_if_not_none(params, "isSeries", is_series)
        _put_if_not_none(params, "isNews", is_news)
        _put_if_not_none(params, "isKids", is_kids)
        _put_if_not_none(params, "isSports", is_sports)
        _put_if_not_none(params, "excludeItemIds", exclude_item_ids)
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "recursive", recursive)
        _put_if_not_none(params, "searchTerm", search_term)
        _put_if_not_none(params, "sortOrder", sort_order)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "excludeItemTypes", exclude_item_types)
        _put_if_not_none(params, "filters", filters)
        _put_if_not_none(params, "isFavorite", is_favorite)
        _put_if_not_none(params, "mediaTypes", media_types)
        _put_if_not_none(params, "imageTypes", image_types)
        _put_if_not_none(params, "sortBy", sort_by)
        _put_if_not_none(params, "isPlayed", is_played)
        _put_if_not_none(params, "genres", genres)
        _put_if_not_none(params, "officialRatings", official_ratings)
        _put_if_not_none(params, "tags", tags)
        _put_if_not_none(params, "years", years)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "person", person)
        _put_if_not_none(params, "personIds", person_ids)
        _put_if_not_none(params, "personTypes", person_types)
        _put_if_not_none(params, "studios", studios)
        _put_if_not_none(params, "artists", artists)
        _put_if_not_none(params, "excludeArtistIds", exclude_artist_ids)
        _put_if_not_none(params, "artistIds", artist_ids)
        _put_if_not_none(params, "albumArtistIds", album_artist_ids)
        _put_if_not_none(params, "contributingArtistIds", contributing_artist_ids)
        _put_if_not_none(params, "albums", albums)
        _put_if_not_none(params, "albumIds", album_ids)
        _put_if_not_none(params, "ids", ids)
        _put_if_not_none(params, "videoTypes", video_types)
        _put_if_not_none(params, "minOfficialRating", min_official_rating)
        _put_if_not_none(params, "isLocked", is_locked)
        _put_if_not_none(params, "isPlaceHolder", is_place_holder)
        _put_if_not_none(params, "hasOfficialRating", has_official_rating)
        _put_if_not_none(params, "collapseBoxSetItems", collapse_box_set_items)
        _put_if_not_none(params, "minWidth", min_width)
        _put_if_not_none(params, "minHeight", min_height)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "is3D", is3_d)
        _put_if_not_none(params, "seriesStatus", series_status)
        _put_if_not_none(params, "nameStartsWithOrGreater", name_starts_with_or_greater)
        _put_if_not_none(params, "nameStartsWith", name_starts_with)
        _put_if_not_none(params, "nameLessThan", name_less_than)
        _put_if_not_none(params, "studioIds", studio_ids)
        _put_if_not_none(params, "genreIds", genre_ids)
        _put_if_not_none(params, "enableTotalRecordCount", enable_total_record_count)
        _put_if_not_none(params, "enableImages", enable_images)
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

    def get_local_trailers(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets local trailers for an item."""
        endpoint = "/Items/{itemId}/LocalTrailers"
        endpoint = endpoint.replace("{itemId}", str(item_id))
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
        _put_if_not_none(params, "container", container)
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
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
        _put_if_not_none(params, "static", static)
        _put_if_not_none(params, "params", stream_params)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "deviceProfileId", device_profile_id)
        _put_if_not_none(params, "playSessionId", play_session_id)
        _put_if_not_none(params, "segmentContainer", segment_container)
        _put_if_not_none(params, "segmentLength", segment_length)
        _put_if_not_none(params, "minSegments", min_segments)
        _put_if_not_none(params, "mediaSourceId", media_source_id)
        _put_if_not_none(params, "deviceId", device_id)
        _put_if_not_none(params, "audioCodec", audio_codec)
        _put_if_not_none(params, "enableAutoStreamCopy", enable_auto_stream_copy)
        _put_if_not_none(params, "allowVideoStreamCopy", allow_video_stream_copy)
        _put_if_not_none(params, "allowAudioStreamCopy", allow_audio_stream_copy)
        _put_if_not_none(params, "breakOnNonKeyFrames", break_on_non_key_frames)
        _put_if_not_none(params, "audioSampleRate", audio_sample_rate)
        _put_if_not_none(params, "maxAudioBitDepth", max_audio_bit_depth)
        _put_if_not_none(params, "audioBitRate", audio_bit_rate)
        _put_if_not_none(params, "audioChannels", audio_channels)
        _put_if_not_none(params, "maxAudioChannels", max_audio_channels)
        _put_if_not_none(params, "profile", profile)
        _put_if_not_none(params, "level", level)
        _put_if_not_none(params, "framerate", framerate)
        _put_if_not_none(params, "maxFramerate", max_framerate)
        _put_if_not_none(params, "copyTimestamps", copy_timestamps)
        _put_if_not_none(params, "startTimeTicks", start_time_ticks)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "videoBitRate", video_bit_rate)
        _put_if_not_none(params, "subtitleStreamIndex", subtitle_stream_index)
        _put_if_not_none(params, "subtitleMethod", subtitle_method)
        _put_if_not_none(params, "maxRefFrames", max_ref_frames)
        _put_if_not_none(params, "maxVideoBitDepth", max_video_bit_depth)
        _put_if_not_none(params, "requireAvc", require_avc)
        _put_if_not_none(params, "deInterlace", de_interlace)
        _put_if_not_none(params, "requireNonAnamorphic", require_non_anamorphic)
        _put_if_not_none(params, "transcodingMaxAudioChannels", transcoding_max_audio_channels)
        _put_if_not_none(params, "cpuCoreLimit", cpu_core_limit)
        _put_if_not_none(params, "liveStreamId", live_stream_id)
        _put_if_not_none(params, "enableMpegtsM2TsMode", enable_mpegts_m2_ts_mode)
        _put_if_not_none(params, "videoCodec", video_codec)
        _put_if_not_none(params, "subtitleCodec", subtitle_codec)
        _put_if_not_none(params, "transcodeReasons", transcode_reasons)
        _put_if_not_none(params, "audioStreamIndex", audio_stream_index)
        _put_if_not_none(params, "videoStreamIndex", video_stream_index)
        _put_if_not_none(params, "context", context)
        _put_if_not_none(params, "streamOptions", stream_options)
        _put_if_not_none(params, "enableAudioVbrEncoding", enable_audio_vbr_encoding)
        return self.request("GET", endpoint, params=params)

    def merge_versions(self, ids: list[Any] | None = None) -> Any:
        """Merges videos into a single record."""
        endpoint = "/Videos/MergeVersions"
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        return self.request("POST", endpoint, params=params)
