# Usage — MCP / API / Agent

`jellyfin-mcp` exposes the same capability three ways: as **MCP tools** an agent calls,
as a **Python API** (`Api`) you import, and as an **A2A agent CLI**. The agent-package
pattern and MCP configuration are covered in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers a condensed, action-routed tool
set. Each tool takes an `action` (the underlying client method name) and a
`params_json` string of keyword arguments, so a small number of tools cover the full
Jellyfin surface without overwhelming the LLM context window.

| Tool | Tag | Covers |
|---|---|---|
| `jellyfin_media` | `Media` | Playback, streams, artists, playlists, genres, audio/video — e.g. `get_movies`, `get_videos`, `get_artists`, `get_playlists`, `get_audio_stream` |
| `jellyfin_library` | `Library` | Items, search, collections, user views, channels — e.g. `get_items`, `search_items`, `get_collections`, `get_user_views`, `get_library_info` |
| `jellyfin_system` | `System` | Administration, system status, configuration, backups, users — e.g. `get_system_info`, `get_users`, `get_devices`, `list_backups`, `get_configuration` |

Example agent prompts that map onto these tools:

- *"List the movies in my library"* → `jellyfin_media` with `action=get_movies`
- *"Search the library for items named like 'matrix'"* → `jellyfin_library` with `action=search_items`
- *"Show the Jellyfin server's system information"* → `jellyfin_system` with `action=get_system_info`

## As a Python API

`Api` is a unified client composed of modular media, library, system, and user
sub-clients. Build one directly, or from the environment with `get_client()`.

```python
from jellyfin_mcp.api_client import Api

api = Api(
    base_url="http://your-jellyfin:8096",
    token="your_api_key",
    verify=True,
)

# Reads
info = api.get_system_info()           # server name, version, OS
movies = api.get_movies()              # movie library items
results = api.search_items(searchTerm="matrix")
views = api.get_user_views()           # the caller's library views
```

Build a client straight from the environment:

```python
from jellyfin_mcp.auth import get_client

api = get_client()        # reads JELLYFIN_* from the environment / .env
users = api.get_users()
```

`get_client()` selects the authentication flow automatically: a `JELLYFIN_API_KEY`
when present, otherwise `JELLYFIN_USERNAME` + `JELLYFIN_PASSWORD`, or an OIDC
token-exchange delegation when `ENABLE_DELEGATION=true`. When no credentials are
configured it raises a clear error rather than connecting anonymously.

## As an A2A agent

The integrated Pydantic-AI graph agent is published as the `jellyfin-agent` console
script. It connects to the MCP server, routes each query to a focused domain, and
serves an optional Web UI.

```bash
export JELLYFIN_URL=http://your-jellyfin:8096
export JELLYFIN_API_KEY=your_api_key

jellyfin-agent --provider openai --model-id gpt-4o --host 0.0.0.0 --port 9056
```

Point the agent at an already-running MCP server with `--mcp-url`
(`http://jellyfin-mcp-mcp:8000/mcp`), or let it auto-discover servers from
`mcp_config.json`. See [Deployment](deployment.md#agent-server) for the combined
Docker Compose stack.
</content>
