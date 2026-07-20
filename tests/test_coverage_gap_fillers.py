import os
import runpy
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from starlette.datastructures import Headers
from starlette.requests import Request

# --- Tests for jellyfin_mcp/__init__.py ---


def test_init_module_lazy_attributes():
    """Verify lazy-loading attribute resolution.

    CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
    """
    import jellyfin_mcp

    # Check lazy attributes
    assert hasattr(jellyfin_mcp, "_MCP_AVAILABLE")
    assert hasattr(jellyfin_mcp, "_AGENT_AVAILABLE")

    # Test getting dynamic lazy attributes
    assert jellyfin_mcp._MCP_AVAILABLE is True
    assert jellyfin_mcp._AGENT_AVAILABLE is True

    # Test requesting nonexistent attribute raises AttributeError
    with pytest.raises(AttributeError):
        _ = jellyfin_mcp.non_existent_attribute_name

    # Test __dir__
    dir_contents = dir(jellyfin_mcp)
    assert "Api" in dir_contents


def test_init_module_missing_availability():
    """Verify availability status returns False if modules are missing.

    CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
    """
    import jellyfin_mcp

    # Mock OPTIONAL_MODULES to trigger false return branches
    with patch.dict(jellyfin_mcp.OPTIONAL_MODULES, {}, clear=True):
        assert jellyfin_mcp._MCP_AVAILABLE is False
        assert jellyfin_mcp._AGENT_AVAILABLE is False


def test_init_lazy_import_failure():
    """Verify import safety wrapper handles missing modules.

    CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
    """
    # Mock importlib.import_module to raise ImportError for optional modules
    import importlib

    import jellyfin_mcp

    original_import = importlib.import_module

    def mock_import(name, *args, **kwargs):
        if "non_existent" in name:
            raise ImportError("Mocked import error")
        return original_import(name, *args, **kwargs)

    with patch("importlib.import_module", side_effect=mock_import):
        assert jellyfin_mcp._import_module_safely("jellyfin_mcp.non_existent") is None


def test_init_lazy_expose_members():
    """Verify global namespace registration on demand.

    CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
    """
    import jellyfin_mcp

    # Remove attributes from module globals if already exposed to force __getattr__ invocation
    for name in [
        "get_mcp_instance",
        "mcp_server",
        "get_agent_instance",
        "agent_server",
    ]:
        if name in jellyfin_mcp.__dict__:
            del jellyfin_mcp.__dict__[name]
    # Clear mcp_server from loaded optional modules to force dynamic lookup
    if "jellyfin_mcp.mcp_server" in jellyfin_mcp._loaded_optional_modules:
        del jellyfin_mcp._loaded_optional_modules["jellyfin_mcp.mcp_server"]
    # Trigger hasattr and getattr via __getattr__ exposing dynamic members
    assert jellyfin_mcp.get_mcp_instance is not None


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
async def test_mcp_server_custom_route():
    """Verify custom routes (e.g. /health) inside MCP instance.

    CONCEPT:JF-OS.config.dynamic-tool-routing — Dynamic Tool Routing
    """
    from jellyfin_mcp.mcp_server import get_mcp_instance

    mcp_data = get_mcp_instance()
    mcp = mcp_data[0] if isinstance(mcp_data, tuple) else mcp_data

    # Retrieve custom routes from mcp.http_app()
    app = mcp.http_app()
    route_handler = None
    for route in app.routes:
        if route.path == "/health":
            route_handler = route.endpoint
            break

    assert route_handler is not None

    # Construct a mock Starlette Request object
    mock_scope = {
        "type": "http",
        "method": "GET",
        "path": "/health",
        "headers": Headers().raw,
    }
    mock_req = Request(scope=mock_scope)
    response = await route_handler(mock_req)

    # Verify response
    assert response.status_code == 200
    import json

    payload = json.loads(response.body.decode())
    assert payload.get("status", "").lower() == "ok"


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
    assert "Invalid params_json" in res["error"]
    mock_context.info.assert_called_with("Executing media action: get_system_info...")

    # Unknown dynamic action
    res = await media_tool(
        action="non_existent_method", params_json="{}", client=mock_client
    )
    assert "error" in res
    assert "Unknown action 'non_existent_method'" in res["error"]
    assert "list_actions" in res["error"]

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
    assert "Media action failed: Mocked action error" in res["error"]

    # 2. Test library tool
    library_tool_obj = await mcp.get_tool("jellyfin_library")
    assert library_tool_obj is not None
    library_tool = library_tool_obj.fn  # type: ignore

    res = await library_tool(
        action="get_items", params_json="{invalid", client=None, ctx=mock_context
    )
    assert "error" in res
    assert "Invalid params_json" in res["error"]

    res = await library_tool(
        action="non_existent_method", params_json="{}", client=mock_client
    )
    assert "error" in res
    assert "Unknown action 'non_existent_method'" in res["error"]
    assert "list_actions" in res["error"]

    mock_error_client = MagicMock(spec=["get_items"])
    mock_error_client.get_items.side_effect = RuntimeError("Library error")
    res = await library_tool(
        action="get_items", params_json="{}", client=mock_error_client
    )
    assert "error" in res
    assert "Library action failed: Library error" in res["error"]

    # 3. Test system tool
    system_tool_obj = await mcp.get_tool("jellyfin_system")
    assert system_tool_obj is not None
    system_tool = system_tool_obj.fn  # type: ignore

    res = await system_tool(
        action="get_system_info", params_json="{invalid", client=None, ctx=mock_context
    )
    assert "error" in res
    assert "Invalid params_json" in res["error"]

    res = await system_tool(
        action="non_existent_method", params_json="{}", client=mock_client
    )
    assert "error" in res
    assert "Unknown action 'non_existent_method'" in res["error"]
    assert "list_actions" in res["error"]

    mock_error_client = MagicMock(spec=["get_system_info"])
    mock_error_client.get_system_info.side_effect = RuntimeError("System error")
    res = await system_tool(
        action="get_system_info", params_json="{}", client=mock_error_client
    )
    assert "error" in res
    assert "System action failed: System error" in res["error"]


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


def test_mcp_server_startup_transports():
    """Verify startup transport command-line flag handling.

    CONCEPT:JF-OS.config.dynamic-tool-routing — Dynamic Tool Routing
    """
    from jellyfin_mcp.mcp_server import mcp_server

    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_args.host = "localhost"
    mock_args.port = 8000
    mock_args.auth_type = "none"

    mock_mcp = MagicMock()

    with (
        patch(
            "jellyfin_mcp.mcp_server.get_mcp_instance",
            return_value=(mock_mcp, mock_args, []),
        ),
        patch("sys.exit") as mock_exit,
    ):
        # 1. stdio transport
        mock_args.transport = "stdio"
        mcp_server()
        mock_mcp.run.assert_called_with(transport="stdio")

        # 2. streamable-http transport
        mock_args.transport = "streamable-http"
        mcp_server()
        mock_mcp.run.assert_called_with(
            transport="streamable-http", host="localhost", port=8000
        )

        # 3. sse transport
        mock_args.transport = "sse"
        mcp_server()
        mock_mcp.run.assert_called_with(transport="sse", host="localhost", port=8000)

        # 4. Invalid transport
        mock_args.transport = "invalid-transport"
        mcp_server()
        mock_exit.assert_called_with(1)


def test_mcp_server_main_execution():
    """Verify main block execution of the MCP server module.

    CONCEPT:JF-OS.config.dynamic-tool-routing — Dynamic Tool Routing
    """
    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_args.host = "localhost"
    mock_args.port = 8000
    mock_args.auth_type = "none"

    mock_mcp = MagicMock()
    mock_mcp.custom_route.return_value = lambda x: x

    with (
        patch(
            "agent_utilities.mcp.server_factory.create_mcp_server",
            return_value=(mock_args, mock_mcp, []),
        ),
        patch("sys.exit"),
    ):
        runpy.run_module("jellyfin_mcp.mcp_server", run_name="__main__")
        mock_mcp.run.assert_called_with(transport="stdio")


# --- Tests for jellyfin_mcp/agent_server.py ---


def test_agent_server_debug_mode():
    """Verify agent server debug mode activation.

    CONCEPT:JF-OS.config.a2a-agent-interface — A2A Agent Interface
    """
    with (
        patch("agent_utilities.initialize_workspace"),
        patch("agent_utilities.load_identity", return_value={"name": "test"}),
        patch(
            "agent_utilities.build_system_prompt_from_workspace", return_value="prompt"
        ),
        patch("agent_utilities.create_agent_server") as mock_server,
        patch("agent_utilities.create_agent_parser") as mock_parser,
        patch("sys.argv", ["agent_server.py"]),
    ):
        mock_args = MagicMock()
        mock_args.debug = True
        mock_args.mcp_url = None
        mock_args.mcp_config = None
        mock_args.host = "localhost"
        mock_args.port = 8000
        mock_args.provider = "openai"
        mock_args.model_id = "gpt-4"
        mock_args.base_url = None
        mock_args.api_key = "test"
        mock_args.custom_skills_directory = None
        mock_args.web = False
        mock_args.otel = False
        mock_args.otel_endpoint = None
        mock_args.otel_headers = None
        mock_args.otel_public_key = None
        mock_args.otel_secret_key = None
        mock_args.otel_protocol = "http/protobuf"
        mock_parser.return_value.parse_args.return_value = mock_args

        # Force reimport with mocked dependencies
        import importlib
        import sys

        mod = sys.modules.get("jellyfin_mcp.agent_server")
        if not mod:
            mod = importlib.import_module("jellyfin_mcp.agent_server")

        importlib.reload(mod)
        mod.agent_server()
        assert mock_server.called


def test_agent_server_main_execution():
    """Verify agent server main execution setup.

    CONCEPT:JF-OS.config.a2a-agent-interface — A2A Agent Interface
    """
    with (
        patch("agent_utilities.initialize_workspace"),
        patch("agent_utilities.load_identity", return_value={"name": "test"}),
        patch(
            "agent_utilities.build_system_prompt_from_workspace", return_value="prompt"
        ),
        patch("agent_utilities.create_agent_server") as mock_server,
        patch("agent_utilities.create_agent_parser") as mock_parser,
        patch("sys.argv", ["agent_server.py"]),
    ):
        mock_args = MagicMock()
        mock_args.debug = False
        mock_args.mcp_url = None
        mock_args.mcp_config = None
        mock_args.host = "localhost"
        mock_args.port = 8000
        mock_args.provider = "openai"
        mock_args.model_id = "gpt-4"
        mock_args.base_url = None
        mock_args.api_key = "test"
        mock_args.custom_skills_directory = None
        mock_args.web = False
        mock_args.otel = False
        mock_args.otel_endpoint = None
        mock_args.otel_headers = None
        mock_args.otel_public_key = None
        mock_args.otel_secret_key = None
        mock_args.otel_protocol = "http/protobuf"
        mock_parser.return_value.parse_args.return_value = mock_args

        runpy.run_module("jellyfin_mcp.agent_server", run_name="__main__")
        assert mock_server.called


# --- Tests for jellyfin_mcp/__main__.py ---


def test_main_module():
    """Verify primary __main__ module entry delegation.

    CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
    """
    with patch("jellyfin_mcp.agent_server.agent_server") as mock_agent_server:
        runpy.run_module("jellyfin_mcp.__main__", run_name="__main__")
        mock_agent_server.assert_called_once()


def test_api_client_error_coverage():
    """Verify ApiClient error states and non-JSON output mapping.

    CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
    """
    from agent_utilities.core.exceptions import AuthError, UnauthorizedError

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
