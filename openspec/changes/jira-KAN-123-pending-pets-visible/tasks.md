# Tasks

- [x] Review Jira issue KAN-123 and extract requirements.
- [x] Check wiki documentation at `docs/wiki/petstore-catalog-availability.md`.
- [x] Review log evidence at `docs/logs/pending-pet-visible.ndjson`.
- [x] Identify root cause in `app/petstore_app/catalog.py`.
- [x] Create OpenSpec-style change artifacts in `openspec/changes/jira-KAN-123-pending-pets-visible/`.
- [x] Validate OpenSpec change folder structure.
- [ ] Implement the fix: remove truthiness check from status filter condition.
- [ ] Add test `test_search_pets_excludes_pending_by_default` to verify default behavior.
- [ ] Run existing tests to ensure no regressions.
- [ ] Run new test to verify fix.
- [ ] Create draft pull request with evidence waypoints and validation results.
- [ ] Add `openhands-review` label to trigger code review automation.
