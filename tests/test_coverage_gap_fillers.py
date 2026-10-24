import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError

# --- Tests for jellyfin_mcp/__init__.py ---






# --- Tests for jellyfin_mcp/auth.py ---


def test_auth_empty_params():
    """Verify empty parameters fail authentication.

    CONCEPT:JF-OS.identity.access-delegation — Access Delegation
    """
    from jellyfin_mcp.auth import get_client

    with pytest.raises(ValueError, match="No auth method"):
        get_client(base_url="http://test", token=None, username=None, password=None)


def test_auth_missing_url():
    """Verify missing URL error behavior.

    CONCEPT:JF-OS.identity.access-delegation — Access Delegation
    """
    from jellyfin_mcp.auth import get_client

    with pytest.raises(RuntimeError, match="JELLYFIN_URL not set"):
        get_client(base_url=None)


def test_auth_oidc_delegation_success():
    """Verify successful OIDC delegation client setup.

    CONCEPT:JF-OS.identity.access-delegation — Access Delegation
    """
    from jellyfin_mcp.auth import get_client, local

    # Setup OIDC env vars
    env_mock = {
        "ENABLE_DELEGATION": "True",
        "JELLYFIN_AUDIENCE": "jellyfin-aud",
        "OIDC_TOKEN_ENDPOINT": "http://oidc/token",
        "OIDC_CLIENT_ID": "client-id",
        "OIDC_CLIENT_SECRET": "client-secret",
    }

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"access_token": "delegated_access_token"}

    with (
        patch.dict(os.environ, env_mock),
        patch("requests.Session") as mock_session,
        patch("jellyfin_mcp.auth.Api") as mock_api,
    ):
        delegation_session = mock_session.return_value.__enter__.return_value
        delegation_session.post.return_value = mock_resp

        local.user_token = "mcp_token"
        try:
            client = get_client(base_url="http://jellyfin-server")
            assert client is mock_api.return_value
            delegation_session.post.assert_called_once()
        finally:
            local.user_token = None


def test_auth_oidc_delegation_failure():
    """Verify error propagation on delegation failures.

    CONCEPT:JF-OS.identity.access-delegation — Access Delegation
    """
    from jellyfin_mcp.auth import get_client, local

    env_mock = {
        "ENABLE_DELEGATION": "True",
        "OIDC_TOKEN_ENDPOINT": "http://oidc/token",
        "OIDC_CLIENT_ID": "client-id",
        "OIDC_CLIENT_SECRET": "client-secret",
    }

    with (
        patch.dict(os.environ, env_mock),
        patch("requests.Session") as mock_session,
    ):
        mock_session.return_value.__enter__.return_value.post.side_effect = Exception(
            "Connection timed out"
        )
        local.user_token = "mcp_token"
        try:
            with pytest.raises(RuntimeError, match="^Credential delegation failed$"):
                get_client(base_url="http://jellyfin-server")
        finally:
            local.user_token = None


def test_auth_oidc_delegation_invalid_credentials_on_api():
    """Verify access errors raise standard RuntimeErrors with custom messages.

    CONCEPT:JF-OS.identity.access-delegation — Access Delegation
    """
    from jellyfin_mcp.auth import get_client, local

    env_mock = {
        "ENABLE_DELEGATION": "True",
        "OIDC_TOKEN_ENDPOINT": "http://oidc/token",
        "OIDC_CLIENT_ID": "client-id",
        "OIDC_CLIENT_SECRET": "client-secret",
    }

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"access_token": "delegated_access_token"}

    with (
        patch.dict(os.environ, env_mock),
        patch("requests.Session") as mock_session,
        patch(
            "jellyfin_mcp.auth.Api", side_effect=AuthError("Invalid delegated token")
        ),
    ):
        mock_session.return_value.__enter__.return_value.post.return_value = mock_resp
        local.user_token = "mcp_token"
        try:
            with pytest.raises(
                RuntimeError,
                match="AUTHENTICATION ERROR: The delegated Jellyfin credentials",
            ):
                get_client(base_url="http://jellyfin-server")
        finally:
            local.user_token = None


def test_auth_credentials_invalid():
    """Verify invalid credentials raise standard auth error.

    CONCEPT:JF-OS.identity.access-delegation — Access Delegation
    """
    from jellyfin_mcp.auth import get_client

    with patch(
        "jellyfin_mcp.auth.Api", side_effect=UnauthorizedError("Access forbidden")
    ):
        with pytest.raises(
            RuntimeError,
            match="AUTHENTICATION ERROR: The configured Jellyfin credentials are not valid",
        ):
            get_client(base_url="http://jellyfin-server", token="invalid-token")


# --- Tests for jellyfin_mcp/mcp_server.py ---


@pytest.mark.asyncio
async def test_mcp_server_tools_exception_handling():
    """Verify tool execution safety & exception handling.

    CONCEPT:JF-OS.config.dynamic-tool-routing — Dynamic Tool Routing
    """
    from fastmcp import FastMCP

    from jellyfin_mcp.mcp_server import register_condensed_jellyfin_tools

    mcp = FastMCP("test")
    register_condensed_jellyfin_tools(mcp)

    class DummyClient:
        def get_system_info(self, *args, **kwargs):
            return {"mocked": "system_info"}

        def get_items(self, *args, **kwargs):
            return {"mocked": "items"}

    mock_client = DummyClient()

    # 1. Test media tool
    media_tool_obj = await mcp.get_tool("jellyfin_media")
    assert media_tool_obj is not None
    media_tool = media_tool_obj.fn  # type: ignore

    mock_context = MagicMock()
    mock_context.info = AsyncMock()

    # Invalid JSON params
    res = await media_tool(
        action="get_system_info", params_json="{invalid", client=None, ctx=mock_context
    )
    assert "error" in res
    # The SDK action dispatcher never echoes caller input back in an error.
    assert res["error"] == "Operation failed"
    mock_context.info.assert_called_with("Executing media action: get_system_info...")

    # Unknown dynamic action
    res = await media_tool(
        action="non_existent_method", params_json="{}", client=mock_client
    )
    assert "error" in res
    assert res["error"] == "Operation failed"

    # Discovery: list_actions returns the available action names
    res = await media_tool(action="list_actions", params_json="{}", client=mock_client)
    assert res["service"] == "jellyfin-mcp"
    assert "get_system_info" in res["actions"]

    # Action raises standard error
    mock_error_client = MagicMock(spec=["get_system_info"])
    mock_error_client.get_system_info.side_effect = RuntimeError("Mocked action error")
    res = await media_tool(
        action="get_system_info", params_json="{}", client=mock_error_client
    )
    assert "error" in res
    assert res["error"] == "Media action failed: RuntimeError"

    # 2. Test library tool
    library_tool_obj = await mcp.get_tool("jellyfin_library")
    assert library_tool_obj is not None
    library_tool = library_tool_obj.fn  # type: ignore

    res = await library_tool(
        action="get_items", params_json="{invalid", client=None, ctx=mock_context
    )
    assert "error" in res
    # The SDK action dispatcher never echoes caller input back in an error.
    assert res["error"] == "Operation failed"

    res = await library_tool(
        action="non_existent_method", params_json="{}", client=mock_client
    )
    assert "error" in res
    assert res["error"] == "Operation failed"

    mock_error_client = MagicMock(spec=["get_items"])
    mock_error_client.get_items.side_effect = RuntimeError("Library error")
    res = await library_tool(
        action="get_items", params_json="{}", client=mock_error_client
    )
    assert "error" in res
    assert res["error"] == "Library action failed: RuntimeError"

    # 3. Test system tool
    system_tool_obj = await mcp.get_tool("jellyfin_system")
    assert system_tool_obj is not None
    system_tool = system_tool_obj.fn  # type: ignore

    res = await system_tool(
        action="get_system_info", params_json="{invalid", client=None, ctx=mock_context
    )
    assert "error" in res
    # The SDK action dispatcher never echoes caller input back in an error.
    assert res["error"] == "Operation failed"

    res = await system_tool(
        action="non_existent_method", params_json="{}", client=mock_client
    )
    assert "error" in res
    assert res["error"] == "Operation failed"

    mock_error_client = MagicMock(spec=["get_system_info"])
    mock_error_client.get_system_info.side_effect = RuntimeError("System error")
    res = await system_tool(
        action="get_system_info", params_json="{}", client=mock_error_client
    )
    assert "error" in res
    assert res["error"] == "System action failed: RuntimeError"


def test_mcp_server_import_error_handling():
    """Verify dependency import fallback block safety.

    CONCEPT:JF-OS.config.dynamic-tool-routing — Dynamic Tool Routing
    """
    # Force ImportError in RequestsDependencyWarning block of mcp_server.py
    import builtins

    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if "requests.exceptions" in name:
            raise ImportError("Simulated import error")
        return original_import(name, *args, **kwargs)

    import importlib

    mod = sys.modules.get("jellyfin_mcp.mcp_server")
    with patch("builtins.__import__", side_effect=mock_import):
        if mod:
            importlib.reload(mod)


# --- Tests for jellyfin_mcp/agent_server.py ---






# --- Tests for jellyfin_mcp/__main__.py ---




def test_api_client_error_coverage():
    """Verify ApiClient error states and non-JSON output mapping.

    CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
    """
    from agent_connector_sdk.exceptions import AuthError, UnauthorizedError

    from jellyfin_mcp.api_client import Api

    # 1. Test 401 AuthError
    mock_resp_401 = MagicMock()
    mock_resp_401.status_code = 401
    with patch("requests.Session.get", return_value=mock_resp_401):
        with pytest.raises(AuthError, match="Jellyfin authentication failed"):
            Api(base_url="http://test")

    # 2. Test 403 UnauthorizedError
    mock_resp_403 = MagicMock()
    mock_resp_403.status_code = 403
    with patch("requests.Session.get", return_value=mock_resp_403):
        with pytest.raises(UnauthorizedError, match="Jellyfin access forbidden"):
            Api(base_url="http://test")

    # 3. Test generic Exception pass inside Api.__init__
    mock_resp_err = MagicMock()
    mock_resp_err.status_code = 500
    mock_resp_err.raise_for_status.side_effect = RuntimeError("Other error")
    with patch("requests.Session.get", return_value=mock_resp_err):
        # Should catch RuntimeError and pass (not raise AuthError/UnauthorizedError)
        Api(base_url="http://test")

    # 4. Test non-JSON response in request()
    mock_resp_200 = MagicMock()
    mock_resp_200.status_code = 200
    mock_resp_200.json.side_effect = ValueError("Not JSON")
    mock_resp_200.text = "plain text"

    mock_init_resp = MagicMock()
    mock_init_resp.status_code = 200

    with (
        patch("requests.Session.get", return_value=mock_init_resp),
        patch("requests.Session.request", return_value=mock_resp_200),
    ):
        api = Api(base_url="http://test")
        res = api.request("GET", "/some-endpoint")
        assert res == "plain text"
