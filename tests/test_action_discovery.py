"""Action-discovery standardization tests for the jellyfin-mcp condensed tools.

Verifies the shared agent-utilities ``dispatch`` helper provides ``list_actions``
discovery and rich did-you-mean errors across the action-routed tools.

CONCEPT:JELLYFIN-2.0 — Dynamic Tool Routing
"""

from unittest.mock import MagicMock

import pytest
from fastmcp import FastMCP

from jellyfin_mcp.mcp_server import register_condensed_jellyfin_tools


def _make_client() -> MagicMock:
    client = MagicMock(spec=["get_system_info", "get_items", "get_movie"])
    client.get_system_info.return_value = {"ok": "system"}
    client.get_items.return_value = {"ok": "items"}
    client.get_movie.return_value = {"ok": "movie"}
    return client


async def _get_fn(name: str):
    mcp = FastMCP("test")
    register_condensed_jellyfin_tools(mcp)
    tool_obj = await mcp.get_tool(name)
    assert tool_obj is not None
    return tool_obj.fn  # type: ignore[attr-defined]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool_name", ["jellyfin_media", "jellyfin_library", "jellyfin_system"]
)
async def test_list_actions_returns_names(tool_name: str):
    """``list_actions`` returns the discoverable action names for each tool."""
    fn = await _get_fn(tool_name)
    res = await fn(action="list_actions", params_json="{}", client=_make_client())
    assert res["service"] == "jellyfin-mcp"
    assert "get_system_info" in res["actions"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool_name", ["jellyfin_media", "jellyfin_library", "jellyfin_system"]
)
async def test_unknown_action_mentions_list_actions(tool_name: str):
    """A bogus action returns a rich error mentioning ``list_actions``."""
    fn = await _get_fn(tool_name)
    res = await fn(action="totally_bogus", params_json="{}", client=_make_client())
    assert "error" in res
    assert "Unknown action 'totally_bogus'" in res["error"]
    assert "list_actions" in res["error"]


@pytest.mark.asyncio
async def test_plural_alias_resolves_to_singular():
    """Plural guesses (get_movies) resolve to the real singular method (get_movie)."""
    fn = await _get_fn("jellyfin_media")
    client = _make_client()
    res = await fn(action="get_movies", params_json="{}", client=client)
    assert res == {"ok": "movie"}
    client.get_movie.assert_called_once()
