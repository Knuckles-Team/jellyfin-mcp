# Generated System client
from typing import Any

from jellyfin_mcp.api.api_client_base import ApiBase


class SystemClient(ApiBase):
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

    def log_file(self, body: dict[str, Any] | None = None) -> Any:
        """Upload a document."""
        endpoint = "/ClientLog/Document"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

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

    def ping_playback_session(self, play_session_id: str | None = None) -> Any:
        """Pings a playback session."""
        endpoint = "/Sessions/Playing/Ping"
        params: dict[str, Any] = {}
        if play_session_id is not None:
            params["playSessionId"] = play_session_id
        return self.request("POST", endpoint, params=params)

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

    def send_system_command(self, session_id: str, command: str) -> Any:
        """Issues a system command to a client."""
        endpoint = "/Sessions/{sessionId}/System/{command}"
        endpoint = endpoint.replace("{sessionId}", str(session_id))
        endpoint = endpoint.replace("{command}", str(command))
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

    def sync_play_ping(self, body: dict[str, Any] | None = None) -> Any:
        """Update session ping."""
        endpoint = "/SyncPlay/Ping"
        params = None
        return self.request("POST", endpoint, params=params, json_data=body)

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

    def tmdb_client_configuration(self) -> Any:
        """Gets the TMDb image configuration options."""
        endpoint = "/Tmdb/ClientConfiguration"
        params = None
        return self.request("GET", endpoint, params=params)

    def update_user_configuration(
        self, user_id: str | None = None, body: dict[str, Any] | None = None
    ) -> Any:
        """Updates a user configuration."""
        endpoint = "/Users/Configuration"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("POST", endpoint, params=params, json_data=body)

    def get_grouping_options(self, user_id: str | None = None) -> Any:
        """Get user view grouping options."""
        endpoint = "/UserViews/GroupingOptions"
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self.request("GET", endpoint, params=params)
