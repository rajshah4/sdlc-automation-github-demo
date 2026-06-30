# Design

## Context

The Petstore application has two filtering layers:

1. **Core catalog search** (`catalog.py::search_pets`): Correctly filters by `status="available"` by default.
2. **Web UI layer** (`cloud_run_app.py::visible_pets`): Returns pets for the web UI, but currently returns ALL pets when in `INCIDENT_MODE`.

The bug is in the web layer. The `visible_pets()` function has intentional incident-injection logic that returns all pets (including pending) when runtime config mode is `bad_catalog_filter`. This simulates a catalog regression for demo purposes.

Log evidence confirms the symptom: `PENDING_PET_VISIBLE` error with `pending_pet_ids: ["pet-103"]`.

Wiki documentation (`docs/wiki/petstore-catalog-availability.md`) explicitly states:
> Default customer-facing catalog search must show only pets with `status="available"`.

## Decision

- **Fix location**: `app/petstore_app/cloud_run_app.py`, `visible_pets()` function.
- **Fix approach**: Remove the incident mode bypass that returns all pets. Always filter to available-only for the default catalog view.
- **Preserve ops capability**: The core `search_pets()` function already supports explicit `status="pending"` searches for operations workflows.
- **Test coverage**: Add regression test that validates pending pets don't appear in web UI default view.

## Risks

- **Risk**: Removing incident mode logic might break demo scenarios that intentionally inject this bug.
  - **Mitigation**: The fix restores correct behavior per product requirements. If demo scenarios need controlled failures, they should use a different mechanism (e.g., feature flags, separate test fixtures).

- **Risk**: Changing filter logic might affect performance or other catalog behaviors.
  - **Mitigation**: The fix uses the same filtering approach already present in the code (status check). Existing tests validate core catalog behavior.

## Validation Plan

1. Run existing catalog tests: `pytest app/tests/test_pet_catalog.py -v`
2. Run new regression test for web UI pending pet exclusion
3. Validate log evidence scenario no longer produces `PENDING_PET_VISIBLE` error
4. Manual smoke test: verify available pets page shows only Mochi, Scout, and Pip (not Nova)
