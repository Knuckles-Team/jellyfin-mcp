# CONN-JELLYFIN-MCP — Requirements

Governing spec: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-JELLYFIN-MCP-R001` | **MediaBrowser token header.** The client in `jellyfin_mcp/api/api_client_base.py` must send the API key as `Authorization: MediaBrowser Token="<key>"`. The client must not send `X-Emby-Token`. The generator in `scripts/generate_code.py` must emit the same header. | `tests/test_auth_header.py` must show the `Authorization` header value and no `X-Emby-Token` header. |
