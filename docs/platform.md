# Backing Platform — Jellyfin

`jellyfin-mcp` is a **client** of a Jellyfin media server. This page provides a Docker
recipe for deploying one locally to serve as the target of `JELLYFIN_URL`. For
production topologies, follow the upstream
[Jellyfin documentation](https://jellyfin.org/docs/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

Jellyfin publishes the `jellyfin/jellyfin` image. The following stack runs one server
on `:8096`, with persistent config/cache volumes and bind-mounted media libraries:

```yaml
# docker/jellyfin.compose.yml
services:
  jellyfin:
    image: docker.io/jellyfin/jellyfin:latest
    container_name: jellyfin
    hostname: jellyfin
    restart: unless-stopped
    user: 1000:1000
    ports:
      - "8096:8096"            # HTTP web UI / REST API
    environment:
      - TZ=America/Chicago
      - JELLYFIN_PublishedServerUrl=http://localhost:8096
    volumes:
      - jellyfin_config:/config
      - jellyfin_cache:/cache
      - ./media/movies:/movies
      - ./media/tv:/tv
      - ./media/music:/music

volumes:
  jellyfin_config:
  jellyfin_cache:
```

```bash
docker compose -f docker/jellyfin.compose.yml up -d

# Wait for the server to answer, then complete the first-run wizard in the browser
curl -s http://localhost:8096/System/Info/Public
```

After the first-run wizard, create an API key under **Dashboard → API Keys** and use
it as `JELLYFIN_API_KEY`.

## Connect jellyfin-mcp

```bash
export JELLYFIN_URL=http://localhost:8096
export JELLYFIN_API_KEY=your_api_key
export JELLYFIN_SSL_VERIFY=True

jellyfin-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places the Jellyfin server and the MCP server on one Docker network,
so the connector reaches Jellyfin by container name:

```yaml
# docker/stack.compose.yml
services:
  jellyfin:
    image: docker.io/jellyfin/jellyfin:latest
    hostname: jellyfin
    ports: ["8096:8096"]
    volumes:
      - jellyfin_config:/config
      - jellyfin_cache:/cache

  jellyfin-mcp:
    image: knucklessg1/jellyfin-mcp:latest
    depends_on: [jellyfin]
    environment:
      - JELLYFIN_URL=http://jellyfin:8096
      - JELLYFIN_API_KEY=your_api_key
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  jellyfin_config:
  jellyfin_cache:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

With the server running and an API key configured, the MCP tools and the
[agent CLI](usage.md#as-an-a2a-agent) can browse the library, query system
information, and manage collections.
</content>
