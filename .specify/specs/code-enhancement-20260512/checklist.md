# Verification Checklist: Code Enhancement: jellyfin-mcp

## Functional Requirements Verification
- [ ] **FR-001**: 34 functions exceed 200 lines (actionable refactoring targets): register_dynamichls_tools (1753L), register_image_tools (1169L), register_livetv_tools (1069L), register_library_tools (572L), register_videos_tools (548L)
- [ ] **FR-002**: Monolithic: mcp_server.py (13101L) — 19 functions with high complexity (worst: register_dynamichls_tools at 1753L, CC=1); Low cohesion: 67 distinct concepts in one file
- [ ] **FR-003**: Monolithic: api_client.py (7818L) — 32 functions with high complexity (worst: Api.get_items at 265L, CC=87); God class: Api (370 methods) — consider mixins/composition
- [ ] **FR-004**: 6 functions with nesting depth >4
- [ ] **FR-005**: Test suite lacks intent diversity (only one type)
- [ ] **FR-006**: 23 potential doc-test drift items
- [ ] **FR-007**: README.md missing sections: installation
- [ ] **FR-008**: README missing: Has a Table of Contents
- [ ] **FR-009**: README missing: References /docs directory material
- [ ] **FR-010**: SRP: 2 modules exceed 500 lines (god modules)
- [ ] **FR-011**: SRP: 1 classes have >15 methods
- [ ] **FR-012**: No discernible layer architecture (no domain/service/adapter separation)
- [ ] **FR-013**: Low traceability ratio: 0% concepts fully traced
- [ ] **FR-014**: 4 test functions missing concept markers
- [ ] **FR-015**: 462 significant functions (>10 lines) missing concept markers in docstrings
- [ ] **FR-016**: Total lint findings: 368 (high/error: 368, medium/warning: 0, low: 0)
- [ ] **FR-017**: 2 hook(s) may be outdated: ruff-pre-commit, uv-pre-commit
- [ ] **FR-018**: 1 rogue/throwaway scripts detected (fix_*, validate_*, patch_*, etc.): scripts/validate_a2a_agent.py
- [ ] **FR-019**: CHANGELOG.md exists but could not be parsed — check format compliance
- [ ] **FR-020**: No changelog entries within the last 30 days
- [ ] **FR-021**: keepachangelog not installed — pip install 'universal-skills[code-enhancer]'
- [ ] **FR-022**: 2 tests have no assertions
- [ ] **FR-023**: Undocumented env vars: ALLOWED_CLIENT_REDIRECT_URIS, AUTH_TYPE, EUNOMIA_POLICY_FILE, EUNOMIA_REMOTE_URL, EUNOMIA_TYPE, OAUTH_BASE_URL, OAUTH_UPSTREAM_AUTH_ENDPOINT, OAUTH_UPSTREAM_CLIENT_ID, OAUTH_UPSTREAM_CLIENT_SECRET, OAUTH_UPSTREAM_TOKEN_ENDPOINT
- [ ] **FR-024**: 75 Python env vars not in .env.example: ACTIVITYLOGTOOL, APIKEYTOOL, ARTISTSTOOL, AUDIOTOOL, BACKUPTOOL

## User Stories / Acceptance Criteria
- [ ] As a **developer**, I want to **address Project Analysis findings (grade: C, score: 74)**, so that **improve project project analysis from C to at least B (80+)**.
- [ ] As a **developer**, I want to **address Codebase Optimization findings (grade: F, score: 55)**, so that **improve project codebase optimization from F to at least B (80+)**.
- [ ] As a **developer**, I want to **address Test Coverage findings (grade: D, score: 65)**, so that **improve project test coverage from D to at least B (80+)**.
- [ ] As a **developer**, I want to **address Architecture & Design Patterns findings (grade: C, score: 75)**, so that **improve project architecture & design patterns from C to at least B (80+)**.
- [ ] As a **developer**, I want to **address Concept Traceability findings (grade: F, score: 42)**, so that **improve project concept traceability from F to at least B (80+)**.
- [ ] As a **developer**, I want to **address Linting & Formatting findings (grade: F, score: 0)**, so that **improve project linting & formatting from F to at least B (80+)**.
- [ ] As a **developer**, I want to **address Changelog Audit findings (grade: C, score: 75)**, so that **improve project changelog audit from C to at least B (80+)**.

## Success Criteria
- [ ] Overall GPA: 2.59 → 3.0
- [ ] Domains at B or above: 10 → 17
- [ ] Actionable findings: 24 → 0

## Technical Quality Gates
- [x] Pre-commit linting (Ruff check/format) passed
- [x] Repository standards checked and verified
- [x] Zero deprecated / local absolute `file:///` URLs

## Review & Acceptance
- **Overall Verification Score**: 0%
- **Final Review Status**: **Needs Revision**
