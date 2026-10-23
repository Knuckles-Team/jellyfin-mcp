# CONN-JELLYFIN-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `jellyfin-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `jellyfin_mcp` from it.
