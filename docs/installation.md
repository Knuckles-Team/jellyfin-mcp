# Installation

`jellyfin-mcp` is a standard Python package and a prebuilt container image. Pick the
path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Jellyfin media server** — see [Backing Platform](platform.md) to
  deploy one locally.

## From PyPI (recommended)

```bash
pip install jellyfin-mcp
```

The base install already includes the FastMCP MCP-server runtime
(`agent-utilities[mcp]`), so the `jellyfin-mcp` console script is ready immediately.

### Optional extras

Install an extra only when you need the integrated agent or the test tooling:

| Extra | Install | Pulls in |
|---|---|---|
| _(base)_ | `pip install jellyfin-mcp` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "jellyfin-mcp[agent]"` | Pydantic-AI agent + Logfire tracing (`agent-utilities[agent,logfire]`) |
| `all` | `pip install "jellyfin-mcp[all]"` | MCP server **and** the agent runtime |
| `test` | `pip install "jellyfin-mcp[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run the MCP server and the integrated A2A agent
pip install "jellyfin-mcp[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/jellyfin-mcp.git
cd jellyfin-mcp
pip install -e ".[all]"          # editable install with the agent runtime
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run jellyfin-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (installs
`jellyfin-mcp[all]`, entrypoint `jellyfin-mcp`):

```bash
docker pull knucklessg1/jellyfin-mcp:latest

docker run --rm -i \
  -e JELLYFIN_URL=http://your-jellyfin:8096 \
  -e JELLYFIN_API_KEY=your_api_key \
  knucklessg1/jellyfin-mcp:latest        # stdio transport (default)
```

For an HTTP server with a published port, and for the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
jellyfin-mcp --help
jellyfin-agent --help
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server (and agent) behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the `Api` client, and the agent CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
</content>
