"""CONN-JELLYFIN-MCP-R005: the whole connector surface is declared."""

import asyncio

import pytest


@pytest.mark.spec("CONN-JELLYFIN-MCP-R005")
def test_every_tool_is_called_by_a_contract_step():
    from fastmcp import Client
    from jellyfin_mcp.connector_contracts import CONTRACTS
    from scion_sdk.connector import build_server

    _, mcp = build_server("jellyfin_mcp", command_args=[])

    async def collect():
        async with Client(mcp) as client:
            return await client.list_tools()

    names = {tool.name for tool in asyncio.run(collect())}
    called = {step.tool for contract in CONTRACTS for step in contract.steps}
    assert not sorted(names - called), "tools no contract calls"
