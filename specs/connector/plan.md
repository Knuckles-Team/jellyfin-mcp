# CONN-JELLYFIN-MCP — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Existing system and reuse

`ApiBase.__init__` in `jellyfin_mcp/api/api_client_base.py` builds one requests session. Every generated operation uses that session.

## Architecture

`ApiBase.__init__` sets the `Authorization` session header from the configured token. The `/System/Info` probe and every operation call carry that header.

## Interfaces and data model

The configuration keeps `JELLYFIN_API_KEY`. Only the wire header changes.

## Live integration path

The fleet gateway calls a tool. The SDK tool surface calls the client method, and `ApiBase.request` sends the session header.

## Quality and release gates

The focused tests run with `pytest -q`. A merge to the default branch publishes the package and the image.

## Risks, alternatives, and decisions

The server rejects `X-Emby-Token` with status 401. The client sends only the `Authorization` form.
