# CONN-JELLYFIN-MCP — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

`ApiBase.__init__` in `jellyfin_mcp/api/api_client_base.py` builds one requests session. Every generated operation uses that session. `ApiBase.__init__` sets the `Authorization` session header from the configured token. The `/System/Info` probe and every operation call carry that header.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest; the proof level each row names
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; shared capabilities come from the SDK
- **Scale/Scope**: 1 rows

## Constitution Check

- One owner per concept: pass. The connector owns one external system's calls, mappings and tools only.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
mcp_config.json  existing
jellyfin_mcp/__init__.py  existing
jellyfin_mcp/auth.py  existing
README.md  existing
tests/test_env_declarations.py  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

### Interfaces and data model

The configuration keeps `JELLYFIN_API_KEY`. Only the wire header changes.

### Live integration path

The fleet gateway calls a tool. The SDK tool surface calls the client method, and `ApiBase.request` sends the session header.

### Quality and release gates

The focused tests run with `pytest -q`. A merge to the default branch publishes the package and the image.

### Risks, alternatives, and decisions

The server rejects `X-Emby-Token` with status 401. The client sends only the `Authorization` form.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-JELLYFIN-MCP-R002`: the `jellyfin-mcp = scion_sdk.cli:serve` console script -> entry point `jellyfin_mcp:connector` (`jellyfin_mcp/__init__.py` line 12) -> `get_client` (`jellyfin_mcp/auth.py` line 21), which reads the JELLYFIN_* and delegation variables through `scion_sdk.config.setting`.

## Cross-repo seams

none
