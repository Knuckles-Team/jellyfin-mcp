# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.9] - 2026-11-06

### Added
- Surface contracts: a tool-use contract step, link and data location for every one of the 370 tools, five business roles, and complete agent-definition prompts for the operator and four roles (media librarian, server administrator, playback coordinator, live TV manager).
- Skills `jellyfin-server-administration` and `jellyfin-live-tv`; workflows added to the library, playback and ingestion skills.

### Changed
- Require `scion-sdk>=0.9.0,<0.10`.
- The operations catalog names the typed tools, not the removed `jellyfin_system`, `jellyfin_library` and `jellyfin_media` tools.

## [2.3.8] - 2026-11-06

### Fixed
- Remove the three action-routed `jellyfin_media`/`jellyfin_library`/`jellyfin_system` tools; the 370 per-operation tools remain. `jellyfin_ingest_library` takes typed arguments instead of `params_json`. Skills, docs and the source mapping name the typed tools.

## [2.3.7] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.5] - 2026-10-27

### Added
- Add the packaged development skill and canonical Pages spec dashboard wiring.

## [2.3.4] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [Unreleased]

### Added
- Standardized OIDC token delegation environment variables configurations in `.env.example`.
- Concept traceability markers to tie files back to Knowledge Graph conceptual nodes.

## [0.15.0] - 2026-05-22

### Added
- Completed **100% statement test coverage** via targeted, robust branch testing inside `tests/test_coverage_gap_fillers.py`.
- Action-Routed dynamic metaprogramming to drastically reduce tool limits while preserving 1:1 endpoint parity.

### Changed
- Replaced 368 independent tools with 60 tag-grouped dynamic routers.
- Standardized tool schemas and removed any underscored parameters.

### Fixed
- Pydantic V2 validations and Pytest failures related to missing parameters or schema conflicts.

## [0.2.56] - 2026-04-29

### Added
- Initial release.

[Unreleased]: https://github.com/Knuckles-Team/jellyfin-mcp/compare/v0.15.0...HEAD
[0.15.0]: https://github.com/Knuckles-Team/jellyfin-mcp/compare/v0.2.56...v0.15.0
[0.2.56]: https://github.com/Knuckles-Team/jellyfin-mcp/releases/tag/v0.2.56
