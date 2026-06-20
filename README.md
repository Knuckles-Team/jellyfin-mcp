# Jellyfin Mcp
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/jellyfin-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/jellyfin-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/jellyfin-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/jellyfin-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/jellyfin-mcp)
![PyPI - License](https://img.shields.io/pypi/l/jellyfin-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/jellyfin-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/jellyfin-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/jellyfin-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/jellyfin-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/jellyfin-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/jellyfin-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/jellyfin-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/jellyfin-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/jellyfin-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/jellyfin-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/jellyfin-mcp)

*Version: 0.45.0*

> **Documentation** — Installation, deployment, usage across the MCP, API, and A2A
> agent interfaces, and guidance for provisioning the Jellyfin media server are
> maintained in the [official documentation](https://knuckles-team.github.io/jellyfin-mcp/).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI or API](#cli-or-api)
- [MCP Integration](#mcp)
  - [Available MCP Tools](#available-mcp-tools)
  - [MCP Configuration Examples](#mcp-configuration-examples)
- [Agent Capabilities](#agent)
  - [Running the Agent CLI](#running-the-agent-cli)
  - [Docker Compose Orchestration](#docker-compose-orchestration)
- [Security & Governance](#security--governance)
- [Documentation](#documentation)
- [Contribute](#contribute)

---

## Overview

**Jellyfin Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Jellyfin MCP Server for Agentic AI!.

---

## Quick Start

### 1. Installation
Install the package directly from PyPI:
```bash
uv pip install jellyfin-mcp[all]
```

### 2. Configure Environment
Set up your connection keys and Jellyfin host details (see `.env.example` for comprehensive list):
```bash
export JELLYFIN_URL="http://localhost:8096"
export JELLYFIN_API_KEY="your_api_key_here"
```

### 3. Run the MCP Server
Launch the server over standard standard I/O (stdio) transport:
```bash
jellyfin-mcp
```

### 4. Run the Agent CLI
To launch the interactive Graph Agent terminal interface:
```bash
jellyfin-agent --provider openai --model-id gpt-4o
```

---

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Jellyfin MCP Server for Agentic AI! API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

_Auto-generated from the live MCP server — do not edit by hand._

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `jellyfin_library` | `CONDENSED_JELLYFINTOOL` | Execute library searches, items, collection updates, and catalog queries dynamically. |
| `jellyfin_media` | `CONDENSED_JELLYFINTOOL` | Execute media playback, stream, artist, playlist, and audio/video queries dynamically. |
| `jellyfin_system` | `CONDENSED_JELLYFINTOOL` | Execute administrative actions, system status, configurations, backups, and user management. |

_3 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/index.md#mcp](docs/index.md#mcp).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "jellyfin-mcp",
        "jellyfin-mcp"
      ],
      "env": {
        "JELLYFIN_URL": "your_jellyfin_url_here",
        "JELLYFIN_USERNAME": "your_jellyfin_username_here",
        "JELLYFIN_PASSWORD": "your_jellyfin_password_here",
        "JELLYFIN_TOKEN": "your_jellyfin_token_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "jellyfin-mcp",
        "jellyfin-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "JELLYFIN_URL": "your_jellyfin_url_here",
        "JELLYFIN_USERNAME": "your_jellyfin_username_here",
        "JELLYFIN_PASSWORD": "your_jellyfin_password_here",
        "JELLYFIN_TOKEN": "your_jellyfin_token_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "url": "http://localhost:8000/jellyfin-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name jellyfin-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e JELLYFIN_URL="your_value" \
  -e JELLYFIN_USERNAME="your_value" \
  -e JELLYFIN_PASSWORD="your_value" \
  -e JELLYFIN_TOKEN="your_value" \
  knucklessg1/jellyfin-mcp:latest
```

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`jellyfin-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/jellyfin-mcp/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://jellyfin-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export JELLYFIN_URL="your_value"
export JELLYFIN_USERNAME="your_value"
export JELLYFIN_PASSWORD="your_value"
export JELLYFIN_TOKEN="your_value"

# Run the agent server
jellyfin-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  jellyfin-mcp-mcp:
    image: knucklessg1/jellyfin-mcp:latest
    container_name: jellyfin-mcp-mcp
    hostname: jellyfin-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  jellyfin-mcp-agent:
    image: knucklessg1/jellyfin-mcp:latest
    container_name: jellyfin-mcp-agent
    hostname: jellyfin-mcp-agent
    restart: always
    depends_on:
      - jellyfin-mcp-mcp
    env_file:
      - ../.env
    command: [ "jellyfin-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9056
      - MCP_URL=http://jellyfin-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9056:9056"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9056/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/index.md#a2a-agent](docs/index.md#a2a-agent).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/jellyfin-mcp/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/jellyfin-mcp/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/jellyfin-mcp/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/jellyfin-mcp/usage/) | the MCP tools, the `Api` client, the agent CLI |
| [Backing Platform](https://knuckles-team.github.io/jellyfin-mcp/platform/) | deploy a Jellyfin media server with Docker |
| [Overview](https://knuckles-team.github.io/jellyfin-mcp/overview/) | the agent-package pattern and MCP configuration |
| [Concepts](https://knuckles-team.github.io/jellyfin-mcp/concepts/) | concept registry (`CONCEPT:JELLYFIN-*`) |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install jellyfin-mcp[all]

# Using standard pip
python -m pip install jellyfin-mcp[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `jellyfin-mcp` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx jellyfin-mcp` · or `uv tool install jellyfin-mcp` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/jellyfin-mcp:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
