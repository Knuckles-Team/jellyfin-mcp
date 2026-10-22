# CONN-JELLYFIN-MCP — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Level | Setup and input | Expected observation | Evidence |
|---|---|---|---|---|---|
| T-001 | FR-001 | Unit | Patched session GET, token `abc123` | The session header `Authorization` equals `MediaBrowser Token="abc123"`. No `X-Emby-Token` header exists. | `tests/test_auth_header.py` |
| T-002 | FR-002 | Unit | Repository env declarations | The SDK env-drift check exits 0 with no dead or undocumented variable. | `tests/test_env_declarations.py` |

## Negative and boundary cases

The test asserts that the rejected header is absent.

## Quality and release proof

Run `pytest -q tests/test_auth_header.py`. The served proof is the fleet acceptance check through the gateway.
