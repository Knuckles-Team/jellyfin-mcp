#!/usr/bin/env python
"""Jellyfin MCP client package initialization.

CONCEPT:JF-OS.governance.lazy-initialization — Lazy Initialization
"""

from agent_connector_sdk.connector import Connector

from jellyfin_mcp.api_client import Api
from jellyfin_mcp.auth import get_client

connector = Connector(
    api=Api,
    get_client=get_client,
    tools="jellyfin_mcp.mcp_server",
    instructions="jellyfin-mcp MCP Server — one tool per API operation.",
)
