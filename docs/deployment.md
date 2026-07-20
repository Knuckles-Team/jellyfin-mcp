# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`jellyfin-mcp` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "jellyfin": {
      "command": "jellyfin-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
jellyfin-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/jellyfin-mcp@sha256:<digest> jellyfin-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "jellyfin": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
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
| `JELLYFIN_TLS_PROFILE` | _(unset)_ | Named runtime TLS profile |
| `JELLYFIN_TLS_PROFILE_REF` | _(unset)_ | Secret reference for private PKI, mTLS, or proxy policy |
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
    image: example/jellyfin-mcp@sha256:<digest>
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
    image: example/jellyfin-mcp@sha256:<digest>
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
    image: example/jellyfin-mcp@sha256:<digest>
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
# Internal (self-signed) — homelab .example.invalid zone
jellyfin-mcp.example.invalid {
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
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=jellyfin-mcp.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `jellyfin-mcp.example.invalid → <caddy-host-ip>` in the Technitium web
console (`http://technitium.example.invalid:5380`). The ecosystem
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

For a remote HTTP server, point the client at `http://jellyfin-mcp.example.invalid/mcp` instead.
</content>
