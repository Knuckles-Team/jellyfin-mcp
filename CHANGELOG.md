# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Action-Routed dynamic metaprogramming to drastically reduce tool limits while preserving 1:1 endpoint parity

### Changed
- Replaced 368 independent tools with 60 tag-grouped dynamic routers
- Standardized tool schemas and removed any underscored parameters

### Fixed
- Pydantic V2 validations and Pytest failures related to missing parameters or schema conflicts

## [0.2.56] - 2026-04-29

### Added
- Initial release
