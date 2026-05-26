# Generated unified api client inheriting from modular sub-clients
from jellyfin_mcp.api.api_client_library import LibraryClient
from jellyfin_mcp.api.api_client_media import MediaClient
from jellyfin_mcp.api.api_client_system import SystemClient
from jellyfin_mcp.api.api_client_user import UserClient


class Api(SystemClient, MediaClient, UserClient, LibraryClient):
    pass
