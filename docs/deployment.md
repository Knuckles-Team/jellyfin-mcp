# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`jellyfin-mcp` exposes its MCP server (console script `jellyfin-mcp`) four ways. Pick the row that
matches where the server runs relative to your MCP client, then copy the matching
`mcp_config.json` below. Replace the `<your-…>` placeholders with the values from the **Configuration / Environment Variables** section.

| # | Option | Transport | Where it runs | `mcp_config.json` key |
|---|--------|-----------|---------------|------------------------|
| 1 | stdio | `stdio` | client launches a subprocess | `command` |
| 2 | Streamable-HTTP (local) | `streamable-http` | a local network port | `command` or `url` |
| 3 | Local container / uv | `stdio` or `streamable-http` | Docker / Podman / uv on this host | `command` or `url` |
| 4 | Remote URL | `streamable-http` | a remote host behind Caddy | `url` |

### 1. stdio (local subprocess)

The client launches the server over stdio via `uvx` — best for local IDEs
(Cursor, Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "uvx",
      "args": ["--from", "jellyfin-mcp", "jellyfin-mcp"],
      "env": {
        "JELLYFIN_URL": "<your-jellyfin_url>",
        "JELLYFIN_BASE_URL": "<your-jellyfin_base_url>",
        "JELLYFIN_ACCESS_TOKEN": "<your-jellyfin_access_token>"
      }
    }
  }
}
```

### 2. Streamable-HTTP (local process)

Run the server as a long-lived HTTP process:

```bash
uvx --from jellyfin-mcp jellyfin-mcp --transport streamable-http --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health        # {"status":"OK"}
```

Then either let the client launch it:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "uvx",
      "args": ["--from", "jellyfin-mcp", "jellyfin-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "JELLYFIN_URL": "<your-jellyfin_url>",
        "JELLYFIN_BASE_URL": "<your-jellyfin_base_url>",
        "JELLYFIN_ACCESS_TOKEN": "<your-jellyfin_access_token>"
      }
    }
  }
}
```

…or connect to the already-running process by URL:

```json
{
  "mcpServers": {
    "jellyfin-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 3. Local container / uv

**(a) Launch a container directly from `mcp_config.json`** (stdio over the container —
no ports to manage). Swap `docker` for `podman` for a daemonless runtime:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "TRANSPORT=stdio",
        "-e", "JELLYFIN_URL=<your-jellyfin_url>",
        "-e", "JELLYFIN_BASE_URL=<your-jellyfin_base_url>",
        "-e", "JELLYFIN_ACCESS_TOKEN=<your-jellyfin_access_token>",
        "knucklessg1/jellyfin-mcp:latest"
      ]
    }
  }
}
```

**(b) Run a local streamable-http container, then connect by URL:**

```bash
docker run -d --name jellyfin-mcp -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e JELLYFIN_URL="<your-jellyfin_url>" \
  -e JELLYFIN_BASE_URL="<your-jellyfin_base_url>" \
  -e JELLYFIN_ACCESS_TOKEN="<your-jellyfin_access_token>" \
  knucklessg1/jellyfin-mcp:latest
# or, from a clone of this repo:
docker compose -f docker/mcp.compose.yml up -d
```

```json
{
  "mcpServers": {
    "jellyfin-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

**(c) From a local checkout with `uv`:**

```bash
uv run jellyfin-mcp --transport streamable-http --port 8000
```

### 4. Remote URL (deployed behind Caddy)

When the server is deployed remotely (e.g. as a Docker service) and published through
Caddy on the internal `*.arpa` zone, connect with the `"url"` key — no local process or
image required:

```json
{
  "mcpServers": {
    "jellyfin-mcp": { "url": "http://jellyfin-mcp.arpa/mcp" }
  }
}
```

Caddy reverse-proxies `http://jellyfin-mcp.arpa` to the container's `:8000`
streamable-http listener; `http://jellyfin-mcp.arpa/health` returns
`{"status":"OK"}` when the service is live.
<!-- END GENERATED: deployment-options -->

This page covers running `jellyfin-mcp` as a long-lived server: the transports, a
Docker Compose stack, the integrated A2A agent, putting it behind a Caddy reverse
proxy, and giving it a DNS name with Technitium. To provision the **Jellyfin media
server** it connects to, see [Backing Platform](platform.md).

> `jellyfin-mcp` ships **two** servers: an **MCP server** (console script
> `jellyfin-mcp`) and an **A2A graph agent** (console script `jellyfin-agent`). The MCP
> server is a typed, deterministic tool surface; the agent wraps it with a Pydantic-AI
> graph, an optional Web UI, and OpenTelemetry tracing.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    jellyfin-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    jellyfin-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    jellyfin-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`jellyfin-mcp` is configured entirely from the environment. The **required**
connection set:

| Var | Default | Meaning |
|---|---|---|
| `JELLYFIN_URL` | `http://localhost:8096` | Jellyfin server base URL |
| `JELLYFIN_API_KEY` | _(unset)_ | API key / access token (preferred auth) |
| `JELLYFIN_USERNAME` | `admin` | Username (credential login, if no key) |
| `JELLYFIN_PASSWORD` | _(unset)_ | Password (credential login, if no key) |
| `JELLYFIN_SSL_VERIFY` | `True` | Verify TLS certificates |
| `AUTH_TYPE` | `apiKey` | Authorization flow: `apiKey`, `credentials`, or `delegated` |
| `CONDENSED_JELLYFIN_TOOL` | `True` | Register the condensed Jellyfin tool set |

Provide **either** `JELLYFIN_API_KEY` **or** `JELLYFIN_USERNAME` + `JELLYFIN_PASSWORD`;
when neither is present the server remains inactive rather than failing at import time.
Optional OIDC token delegation (`ENABLE_DELEGATION`, `OIDC_TOKEN_ENDPOINT`,
`OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `JELLYFIN_AUDIENCE`, `DELEGATED_SCOPES`) and
telemetry (`ENABLE_OTEL`, `OTEL_EXPORTER_OTLP_*`) settings are documented in
[`.env.example`](https://github.com/Knuckles-Team/jellyfin-mcp/blob/main/.env.example).
Copy it to `.env` and populate only what you use. Plus `HOST` / `PORT` / `TRANSPORT`
for HTTP transports.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/jellyfin-mcp/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
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
```

```bash
cp .env.example .env          # then edit JELLYFIN_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Agent server

The integrated A2A graph agent is published as the `jellyfin-agent` console script. It
connects to the MCP server over HTTP (`MCP_URL`), exposes a Web UI / Agent Control
Protocol surface, and is driven by a configurable LLM provider.

```bash
export JELLYFIN_URL=http://your-jellyfin:8096
export JELLYFIN_API_KEY=your_api_key
jellyfin-agent --provider openai --model-id gpt-4o --host 0.0.0.0 --port 9056
```

The repo ships [`docker/agent.compose.yml`](https://github.com/Knuckles-Team/jellyfin-mcp/blob/main/docker/agent.compose.yml),
which runs the MCP server and the agent together. The agent listens on `:9056` and is
wired to the MCP server by container name:

```yaml
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
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
jellyfin-mcp.arpa {
    tls internal
    reverse_proxy jellyfin-mcp-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
jellyfin-mcp.example.com {
    reverse_proxy jellyfin-mcp-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=jellyfin-mcp.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `jellyfin-mcp.arpa → <caddy-host-ip>` in the Technitium web
console (`http://technitium.arpa:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "jellyfin-mcp": {
      "command": "uv",
      "args": ["run", "jellyfin-mcp"],
      "env": {
        "JELLYFIN_URL": "http://your-jellyfin:8096",
        "JELLYFIN_API_KEY": "your_api_key"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://jellyfin-mcp.arpa/mcp` instead.
</content>
