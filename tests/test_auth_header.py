"""The Jellyfin client authenticates with the MediaBrowser Authorization header."""

from unittest.mock import MagicMock, patch

import pytest

from jellyfin_mcp.api.api_client_base import ApiBase


@pytest.mark.spec("CONN-JELLYFIN-MCP-R001")
def test_token_sent_as_mediabrowser_authorization_header():
    with patch("requests.Session.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200)
        client = ApiBase("http://jellyfin.invalid", token="abc123")
    headers = client._session.headers
    assert headers["Authorization"] == 'MediaBrowser Token="abc123"'
    assert "X-Emby-Token" not in headers
