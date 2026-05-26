# Generated User client
from typing import Any

from jellyfin_mcp.api.api_client_base import ApiBase


class UserClient(ApiBase):
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

    def get_first_user_2(self) -> Any:
        """Gets the first user."""
        endpoint = "/Startup/FirstUser"
        params = None
        return self.request("GET", endpoint, params=params)

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
