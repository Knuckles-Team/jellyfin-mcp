---
name: jellyfin-mcp-development
skill_type: skill
description: >-
  Develop and validate the jellyfin-mcp connector using its actual
  scion-sdk entrypoint, Jellyfin API clients, ontology assets, packaged
  skills, and focused tests. Use this skill for source changes and delivery gates;
  use the provider skills for live Jellyfin operations.
license: MIT
tags: [jellyfin, mcp, connector, development, scion-sdk]
metadata:
  author: Repository Maintainers
  version: '0.1.0'
---

# Jellyfin MCP Development

This package is the Jellyfin connector for the `scion-sdk`. Keep changes
bound to the existing connector surface and verify the packaged assets together with
the runtime code.

## Source map

- `pyproject.toml` declares the `jellyfin-mcp` console script at
  `scion_sdk.cli:serve` and the `scion_sdk.connector` entry point
  `jellyfin_mcp:connector`.
- `jellyfin_mcp/mcp_server.py` (import path `jellyfin_mcp.mcp_server`) registers the
  MCP server and action-routed tools.
- `jellyfin_mcp/api/api_client_base.py` and the `api_client_{library,media,system,user}.py`
  modules own the Jellyfin REST calls; `jellyfin_mcp/auth.py` owns credential and
  delegated-auth setup.
- `jellyfin_mcp/connector_sources.py` declares live source metadata. Keep it aligned
  with `jellyfin_mcp/ontology/media.ttl`, `ontology/mappings/source.yaml`,
  `ontology/fixtures/records.json`, and `ontology/migrations/manifest.json`.
- Packaged `skills/**`, `ontology/**`, `mcp_config.json`, and related assets are
  included by the `[tool.setuptools.package-data]` declaration in `pyproject.toml`.

## Configuration and safety

Use environment or secret injection for `JELLYFIN_URL`, `JELLYFIN_API_KEY`,
`JELLYFIN_USERNAME`, `JELLYFIN_PASSWORD`, and the inherited auth/delegation values
(`AUTH_TYPE`, `ENABLE_DELEGATION`, `DELEGATED_SCOPES`, `JELLYFIN_AUDIENCE`, and the
`OIDC_*` settings). `MCP_TOOL_MODE` and the `CONDENSED_JELLYFINTOOL` toggle select
the served tool surface. OIDC delegation uses the configured token exchange and
TLS profile. Do not commit credentials, live endpoints, or captured personal media
data. Preserve TLS verification and the connector SDK's auth and policy boundaries
when changing clients or tool registration.

## Focused checks

Run the smallest relevant tests before the repository gates. The existing focused
coverage is in `tests/test_env_declarations.py`, `tests/test_auth_header.py`,
`tests/test_action_discovery.py`, `tests/test_init_dynamics.py`, and the KG tests
under `tests/test_kg_*.py`. Use a task-local environment and run:

```bash
uv run --locked --extra test pytest tests/test_env_declarations.py tests/test_auth_header.py
uv run --locked --extra test pytest tests/test_action_discovery.py tests/test_init_dynamics.py
```

For ontology or ingestion changes, add the smallest relevant `tests/test_kg_*.py`
selection. Avoid live Jellyfin calls in unit tests; provide explicit configuration
and refusal behavior for missing credentials instead.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver one small, reviewable slice at a time.

1. Find the owning requirement in `specs/` before editing and cite its literal ID in
   the commit `Spec:` trailer. Extend an existing requirement when it owns the work;
   do not invent a parallel spec.
2. Reuse the existing SDK entrypoint, API client, source declaration, ontology asset,
   skill, or focused test before adding a new one. Keep connector behavior in this
   repository; route shared SDK or pipeline behavior to its owning repository.
3. Bind every delivered requirement to a focused test in the same change. Python
   tests use `@pytest.mark.spec("<ID>")`; generated `specs/*/status.json` files are
   produced by `pipelines-hook spec-status --write`, never hand-edited.
4. Keep credentials, raw media data, and local paths out of source, tests, logs, and
   packaged skill content. Preserve the existing runtime, auth, tool schema, and
   ontology semantics while making the smallest change that satisfies the row.
5. Before a push, run the focused tests and the configured pre-commit/pre-push gates;
   inspect the complete staged diff and package contents. Report any unavailable
   live Jellyfin or Pages evidence separately from source and test results.

## Delivery checklist

- `uv run --locked --extra test pytest <focused tests>` passes.
- `uv build` includes the changed skill and ontology package data.
- `pre-commit run --all-files` passes without bypasses.
- `pipelines-hook spec-status` reports generated status current after the commit.
- The built package includes the changed `jellyfin_mcp/skills/**` asset and preserves
  the entry points, ontology files, and runtime configuration.
- A Pages run, Pages API response, and public HTTP snapshot are required before
  claiming a published spec-delivery page; source presence alone is not publication
  proof.
