# Generated Library client
from typing import Any

from jellyfin_mcp.api.api_client_base import ApiBase


def _put_if_not_none(params: dict[str, Any], key: str, value: Any) -> None:
    """Set params[key] = value iff value was provided (mirrors the generated
    client's `if <arg> is not None: params[<key>] = <arg>` call-site idiom).

    Preserves falsy-but-provided values (False, 0, "", []) exactly as the
    inline `is not None` checks did; this is not a truthiness check.
    """
    if value is not None:
        params[key] = value


class LibraryClient(ApiBase):
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
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "includeItemTypes", include_item_types)
        _put_if_not_none(params, "isAiring", is_airing)
        _put_if_not_none(params, "isMovie", is_movie)
        _put_if_not_none(params, "isSports", is_sports)
        _put_if_not_none(params, "isKids", is_kids)
        _put_if_not_none(params, "isNews", is_news)
        _put_if_not_none(params, "isSeries", is_series)
        _put_if_not_none(params, "recursive", recursive)
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
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "searchTerm", search_term)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "excludeItemTypes", exclude_item_types)
        _put_if_not_none(params, "includeItemTypes", include_item_types)
        _put_if_not_none(params, "isFavorite", is_favorite)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "nameStartsWithOrGreater", name_starts_with_or_greater)
        _put_if_not_none(params, "nameStartsWith", name_starts_with)
        _put_if_not_none(params, "nameLessThan", name_less_than)
        _put_if_not_none(params, "sortBy", sort_by)
        _put_if_not_none(params, "sortOrder", sort_order)
        _put_if_not_none(params, "enableImages", enable_images)
        _put_if_not_none(params, "enableTotalRecordCount", enable_total_record_count)
        return self.request("GET", endpoint, params=params)

    def get_genre(self, genre_name: str, user_id: str | None = None) -> Any:
        """Gets a genre, by name."""
        endpoint = "/Genres/{genreName}"
        endpoint = endpoint.replace("{genreName}", str(genre_name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

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
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
        _put_if_not_none(params, "imageIndex", image_index)
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
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
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
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
        _put_if_not_none(params, "imageIndex", image_index)
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
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
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
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
        _put_if_not_none(params, "imageIndex", image_index)
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
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
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
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
        _put_if_not_none(params, "imageIndex", image_index)
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
        _put_if_not_none(params, "tag", tag)
        _put_if_not_none(params, "format", format)
        _put_if_not_none(params, "maxWidth", max_width)
        _put_if_not_none(params, "maxHeight", max_height)
        _put_if_not_none(params, "percentPlayed", percent_played)
        _put_if_not_none(params, "unplayedCount", unplayed_count)
        _put_if_not_none(params, "width", width)
        _put_if_not_none(params, "height", height)
        _put_if_not_none(params, "quality", quality)
        _put_if_not_none(params, "fillWidth", fill_width)
        _put_if_not_none(params, "fillHeight", fill_height)
        _put_if_not_none(params, "blur", blur)
        _put_if_not_none(params, "backgroundColor", background_color)
        _put_if_not_none(params, "foregroundLayer", foreground_layer)
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
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "maxOfficialRating", max_official_rating)
        _put_if_not_none(params, "hasThemeSong", has_theme_song)
        _put_if_not_none(params, "hasThemeVideo", has_theme_video)
        _put_if_not_none(params, "hasSubtitles", has_subtitles)
        _put_if_not_none(params, "hasSpecialFeature", has_special_feature)
        _put_if_not_none(params, "hasTrailer", has_trailer)
        _put_if_not_none(params, "adjacentTo", adjacent_to)
        _put_if_not_none(params, "indexNumber", index_number)
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
        _put_if_not_none(
            params, "minDateLastSavedForUser", min_date_last_saved_for_user
        )
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
        _put_if_not_none(params, "includeItemTypes", include_item_types)
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

    def delete_items(self, ids: list[Any] | None = None) -> Any:
        """Deletes items from the library and filesystem."""
        endpoint = "/Items"
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        return self.request("DELETE", endpoint, params=params)

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
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "searchTerm", search_term)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "mediaTypes", media_types)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "excludeItemTypes", exclude_item_types)
        _put_if_not_none(params, "includeItemTypes", include_item_types)
        _put_if_not_none(params, "enableTotalRecordCount", enable_total_record_count)
        _put_if_not_none(params, "enableImages", enable_images)
        _put_if_not_none(params, "excludeActiveSessions", exclude_active_sessions)
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

    def get_bitrate_test_bytes(self, size: int | None = None) -> Any:
        """Tests the network with a request with the size of the bitrate."""
        endpoint = "/Playback/BitrateTest"
        params: dict[str, Any] = {}
        if size is not None:
            params["size"] = size
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
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "searchTerm", search_term)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "filters", filters)
        _put_if_not_none(params, "isFavorite", is_favorite)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "excludePersonTypes", exclude_person_types)
        _put_if_not_none(params, "personTypes", person_types)
        _put_if_not_none(params, "appearsInItemId", appears_in_item_id)
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "enableImages", enable_images)
        return self.request("GET", endpoint, params=params)

    def get_person(self, name: str, user_id: str | None = None) -> Any:
        """Get person by name."""
        endpoint = "/Persons/{name}"
        endpoint = endpoint.replace("{name}", str(name))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)

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
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "searchTerm", search_term)
        _put_if_not_none(params, "includeItemTypes", include_item_types)
        _put_if_not_none(params, "excludeItemTypes", exclude_item_types)
        _put_if_not_none(params, "mediaTypes", media_types)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "isMovie", is_movie)
        _put_if_not_none(params, "isSeries", is_series)
        _put_if_not_none(params, "isNews", is_news)
        _put_if_not_none(params, "isKids", is_kids)
        _put_if_not_none(params, "isSports", is_sports)
        _put_if_not_none(params, "includePeople", include_people)
        _put_if_not_none(params, "includeMedia", include_media)
        _put_if_not_none(params, "includeGenres", include_genres)
        _put_if_not_none(params, "includeStudios", include_studios)
        _put_if_not_none(params, "includeArtists", include_artists)
        return self.request("GET", endpoint, params=params)

    def complete_wizard(self) -> Any:
        """Completes the startup wizard."""
        endpoint = "/Startup/Complete"
        params = None
        return self.request("POST", endpoint, params=params)

    def set_remote_access(self, body: dict[str, Any] | None = None) -> Any:
        """Sets remote access and UPnP."""
        endpoint = "/Startup/RemoteAccess"
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
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "searchTerm", search_term)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "excludeItemTypes", exclude_item_types)
        _put_if_not_none(params, "includeItemTypes", include_item_types)
        _put_if_not_none(params, "isFavorite", is_favorite)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "nameStartsWithOrGreater", name_starts_with_or_greater)
        _put_if_not_none(params, "nameStartsWith", name_starts_with)
        _put_if_not_none(params, "nameLessThan", name_less_than)
        _put_if_not_none(params, "enableImages", enable_images)
        _put_if_not_none(params, "enableTotalRecordCount", enable_total_record_count)
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

    def get_utc_time(self) -> Any:
        """Gets the current UTC time."""
        endpoint = "/GetUtcTime"
        params = None
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
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "season", season)
        _put_if_not_none(params, "seasonId", season_id)
        _put_if_not_none(params, "isMissing", is_missing)
        _put_if_not_none(params, "adjacentTo", adjacent_to)
        _put_if_not_none(params, "startItemId", start_item_id)
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "enableImages", enable_images)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "sortBy", sort_by)
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
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "seriesId", series_id)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "enableImages", enable_images)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "nextUpDateCutoff", next_up_date_cutoff)
        _put_if_not_none(params, "enableTotalRecordCount", enable_total_record_count)
        _put_if_not_none(params, "disableFirstEpisode", disable_first_episode)
        _put_if_not_none(params, "enableResumable", enable_resumable)
        _put_if_not_none(params, "enableRewatching", enable_rewatching)
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

    def get_intros(self, item_id: str, user_id: str | None = None) -> Any:
        """Gets intros to play before the main media item plays."""
        endpoint = "/Items/{itemId}/Intros"
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
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "includeItemTypes", include_item_types)
        _put_if_not_none(params, "isPlayed", is_played)
        _put_if_not_none(params, "enableImages", enable_images)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "groupItems", group_items)
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
        _put_if_not_none(params, "startIndex", start_index)
        _put_if_not_none(params, "limit", limit)
        _put_if_not_none(params, "sortOrder", sort_order)
        _put_if_not_none(params, "parentId", parent_id)
        _put_if_not_none(params, "fields", fields)
        _put_if_not_none(params, "excludeItemTypes", exclude_item_types)
        _put_if_not_none(params, "includeItemTypes", include_item_types)
        _put_if_not_none(params, "mediaTypes", media_types)
        _put_if_not_none(params, "sortBy", sort_by)
        _put_if_not_none(params, "enableUserData", enable_user_data)
        _put_if_not_none(params, "imageTypeLimit", image_type_limit)
        _put_if_not_none(params, "enableImageTypes", enable_image_types)
        _put_if_not_none(params, "userId", user_id)
        _put_if_not_none(params, "recursive", recursive)
        _put_if_not_none(params, "enableImages", enable_images)
        return self.request("GET", endpoint, params=params)

    def get_year(self, year: int, user_id: str | None = None) -> Any:
        """Gets a year."""
        endpoint = "/Years/{year}"
        endpoint = endpoint.replace("{year}", str(year))
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)
