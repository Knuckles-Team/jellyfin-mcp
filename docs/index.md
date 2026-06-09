# jellyfin-mcp

Jellyfin media-server **API + MCP Server + A2A Agent** for the agent-utilities
ecosystem — a typed, deterministic tool surface over the Jellyfin REST API for
agentic media management.

!!! info "Official documentation"
    This site is the canonical reference for `jellyfin-mcp`, maintained alongside every
    release.

[![PyPI](https://img.shields.io/pypi/v/jellyfin-mcp)](https://pypi.org/project/jellyfin-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/jellyfin-mcp)](https://github.com/Knuckles-Team/jellyfin-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/jellyfin-mcp)

## Overview

`jellyfin-mcp` wraps the Jellyfin media server's REST surface with consolidated,
action-routed MCP tools, and ships an integrated Pydantic-AI graph agent. It provides:

- **`Api`** — a unified Python client composed of modular media, library, system, and
  user sub-clients over the Jellyfin REST API.
- **Condensed, action-routed MCP tools** — `jellyfin_media`, `jellyfin_library`, and
  `jellyfin_system` dispatch dynamically to the client methods, minimizing tool bloat
  in the LLM context window.
- **An A2A graph agent** (`jellyfin-agent` console script) — a Pydantic-AI agent with a
  confidence-gated router, optional Web UI (AG-UI), and OpenTelemetry tracing.

Credentials are read from the environment; the server **remains inactive when
credentials are absent** rather than failing at import time.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `Api` client, and the agent CLI.
- :material-movie-open: **[Backing Platform](platform.md)** — deploy a Jellyfin media server with Docker.
- :material-sitemap: **[Architecture](overview.md)** — the agent-package pattern and MCP configuration.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:JELLYFIN-*` registry.

</div>

## Quick start

```bash
pip install jellyfin-mcp
jellyfin-mcp                       # stdio MCP server (default transport)
```

Connect it to a Jellyfin server:

```bash
export JELLYFIN_URL=http://your-jellyfin:8096
export JELLYFIN_API_KEY=your_api_key
jellyfin-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, DNS).
</content>
