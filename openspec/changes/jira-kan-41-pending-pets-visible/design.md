# Design

## Context

The Petstore application has a `visible_pets()` function in `app/petstore_app/cloud_run_app.py` that serves as the primary filter for the available pets list. This function had incident simulation logic that would return all pets (including pending ones) when `current_mode() == INCIDENT_MODE`, bypassing the status filter.

Product rules from `AGENTS.md`:
- Default pet search returns only available pets
- Pending pets can be shown only when explicitly requested and cannot be adopted
- Money is represented as integer cents

Evidence from logs (`docs/logs/pending-pet-visible.ndjson`):
- Error code: `PENDING_PET_VISIBLE`
- Pending pet IDs: ["pet-103"] (Nova)
- Customer impact confirmed at 2026-06-29T12:00:00Z

## Decision

- Remove the incident mode bypass logic from `visible_pets()` (lines 92-95)
- Simplify the function to always filter by `status == "available"`
- Keep the incident detection and reporting functions intact for observability
- Update tests to reflect the corrected behavior

## Risks

- **Risk**: Removing incident mode logic might break incident simulation/testing workflows
  - **Mitigation**: The incident detection functions (`incident()`, `current_mode()`) remain for observability; only the production filter logic is corrected

- **Risk**: Tests that validate incident mode behavior will fail
  - **Mitigation**: Update or remove `test_bad_catalog_filter_exposes_pending_pet` to reflect correct behavior

- **Risk**: If there are other code paths that depend on incident mode filtering
  - **Mitigation**: Grep showed no other dependencies; `adoptions.py` has its own status validation

## Validation Plan

- Run `pytest app/tests/test_cloud_run_app.py::test_visible_pets_excludes_pending_by_default -v` to verify default filtering works
- Run full test suite: `pytest app/tests/ -v` to ensure no regressions
- Verify Nova (pet-103) does not appear in visible pets results
