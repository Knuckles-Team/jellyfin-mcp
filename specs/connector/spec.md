# CONN-JELLYFIN-MCP — Jellyfin server authentication

Owner: jellyfin-mcp. Cross-repo IDs: none.

## Purpose and user stories

An agent must call the Jellyfin server API through this connector. The server must accept the configured API key on every request.

## Why a new spec

The `specs/` tree held only the template and the index.
No local spec owned this behavior, so this spec is the first capability spec.

## Scope and interfaces

The connector owns its Jellyfin operations, their mappings and their MCP tool annotations.
The connector SDK owns tool registration, transport and the shared client contracts.
Code: ../../jellyfin_mcp/api/api_client_base.py ../../scripts/generate_code.py ../../tests/test_auth_header.py

## Open questions

- None.

## User Scenarios & Testing

### User Story 1 - Jellyfin server authentication (Priority: P1)

An agent must call the Jellyfin server API through this connector. The server must accept the configured API key on every request.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-JELLYFIN-MCP-R002` (env declarations match the code) is exercised, **Then** `tests/test_env_declarations.py::test_env_declarations_match_the_code_read_surface` must pass.

2. **Given** an API key is configured, **When** the behaviour of row `CONN-JELLYFIN-MCP-R001` (MediaBrowser token header) is exercised, **Then** `tests/test_auth_header.py::test_token_sent_as_mediabrowser_authorization_header` must pass.

### Edge Cases

- If `CONN-JELLYFIN-MCP-R002` is not met, its proving test fails: env declarations match the code.

## Requirements

- **FR-001**: Env declarations match the code. Rows: `CONN-JELLYFIN-MCP-R002`.
- **FR-002**: The API key is sent as the MediaBrowser Authorization header. Rows: `CONN-JELLYFIN-MCP-R001`.
- **FR-005**: The whole surface is declared. Rows: `CONN-JELLYFIN-MCP-R005`.

## Success Criteria

- **SC-001**: `tests/test_env_declarations.py::test_env_declarations_match_the_code_read_surface` must pass. Rows: `CONN-JELLYFIN-MCP-R002`.
- **SC-002**: `tests/test_auth_header.py::test_token_sent_as_mediabrowser_authorization_header` must pass. Rows: `CONN-JELLYFIN-MCP-R001`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-JELLYFIN-MCP-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-JELLYFIN-MCP-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-005 | `CONN-JELLYFIN-MCP-R005` | [plan.md](plan.md) | T-005 | [test-spec.md](test-spec.md) |
