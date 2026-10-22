# CONN-JELLYFIN-MCP — Jellyfin server authentication

Owner: jellyfin-mcp. Cross-repo IDs: none.

## Purpose and user stories

An agent must call the Jellyfin server API through this connector. The server must accept the configured API key on every request.

## Requirements and acceptance

- FR-001: The client in `jellyfin_mcp/api/api_client_base.py` must send the API key in the `Authorization` header as `MediaBrowser Token="<key>"`. The client must not send the `X-Emby-Token` header.
- SC-001: `tests/test_auth_header.py` shows the session header value and the absence of the old header, with no network call.

## Why a new spec

The `specs/` tree held only the template and the index.
No local spec owned this behavior, so this spec is the first capability spec.

## Scope and interfaces

The connector owns its Jellyfin operations, their mappings and their MCP tool annotations.
The connector SDK owns tool registration, transport and the shared client contracts.
Code: ../../jellyfin_mcp/api/api_client_base.py ../../scripts/generate_code.py ../../tests/test_auth_header.py

## Traceability

| Requirement | Design section | Test ID | Evidence |
|---|---|---|---|
| FR-001 | plan.md#architecture | T-001 | `tests/test_auth_header.py` |

## Open questions

- None.
