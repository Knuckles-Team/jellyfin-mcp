"""Shared test configuration for jellyfin-mcp tests."""

import os

# Disable Knowledge Graph background sync during tests to prevent
# DB lock contention on shared knowledge_graph.db
os.environ["KNOWLEDGE_GRAPH_SYNC_BACKGROUND"] = "False"
