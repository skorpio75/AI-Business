<!-- Copyright (c) Dario Pizzolante -->
# Testing Strategy

Test layers:
- unit tests for services and utilities
- integration tests for API and DB
- workflow tests for branching and approvals

Baseline tools:
- pytest
- httpx

Operator-facing test commands now live in `README.md` under `Test Execution`.

## Shared Sample Data
The suite now has a lightweight shared sample-data layer in `tests/sample_data.py`.

Use the shared builders when a test needs:
- email workflow payloads or `EmailWorkflowRequest` objects
- approval decision payloads
- knowledge-query or proposal-generation request bodies
- normalized connector bootstrap-status responses
- Track B runtime path and settings kwargs for tenant-scoped tests

Current convention:
- keep stable, repeated payload shapes in `tests/sample_data.py`
- keep one-off values close to the test that needs them
- prefer small builder functions over a large global fixture registry while the suite is still evolving

## Unit Test Base Structure
The unit test suite now has a small shared base layer in `tests/unit/base.py`.

Use `UnitTestCase` when a test needs common helpers such as:
- repo-root access through `ROOT`
- `Settings(_env_file=None, ...)` construction via `build_settings(...)`
- temporary directories via `temporary_directory()`
- in-memory SQLite sessions with metadata ready via `sqlite_session()`

Use `TrackBSeededClientTestCase` when a test needs tenant-scoped client seeding and automatic cleanup for:
- generated `config/clients/*.yaml` and `config/clients/*.env` files
- tenant data, prompt, and secret roots
- temporary `RUNTIME_ENV_FILE` switching with cache reset

Package markers now live at:
- `tests/__init__.py`
- `tests/unit/__init__.py`

Current convention:
- keep generic helpers in `tests/unit/base.py`
- keep test-local fakes inside the individual test module until a second test needs them
- promote repeated fakes or fixtures only when reuse is proven

## API Integration Structure
The API integration suite now has a small shared base layer in `tests/integration/base.py`.

Use `ApiIntegrationTestCase` when a test needs:
- an in-process FastAPI `TestClient`
- an isolated in-memory SQLite database wired through FastAPI dependency overrides
- patched startup/lifespan helpers so API integration tests avoid external bootstrap side effects
- lightweight patch helpers for swapping global API services or provider/bootstrap functions

Current convention:
- keep API integration tests under `tests/integration/`
- prefer exercising real HTTP routes with dependency overrides over calling endpoint functions directly
- patch global service singletons only when a route would otherwise depend on external infrastructure or non-deterministic runtime state

## Workflow Branch Structure
Workflow-branch tests now live under `tests/workflow/`.

Use workflow tests when the goal is to validate:
- approval decision branches such as approve, reject, and edit
- escalation and routing branches such as local-only resolution, cloud escalation, and fallback behavior
- workflow-specific state transitions that are broader than one unit but more focused than a full application integration suite

Current convention:
- keep branch-heavy workflow behavior in `tests/workflow/`
- reuse `UnitTestCase` for service-level routing branches
- reuse `ApiIntegrationTestCase` for approval branches that should be exercised through HTTP endpoints
- source repeated request and decision payloads from `tests/sample_data.py` where possible
