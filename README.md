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

*Version: 0.15.0*

---

## Overview

**Jellyfin Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Jellyfin MCP Server for Agentic AI!.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Jellyfin MCP Server for Agentic AI! API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/jellyfin-mcp/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Condensed Jellyfin** | `CONDENSED_JELLYFIN_TOOL` | `True` | Register highly optimized, condensed tools mapping dynamically to Jellyfin client methods. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/jellyfin-mcp/docs/mcp.md).

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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/jellyfin-mcp/docs/agent.md).

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
