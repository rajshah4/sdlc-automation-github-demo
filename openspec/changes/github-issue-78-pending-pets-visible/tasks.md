# Tasks

- [x] Review GitHub issue #78 and extract requirements.
- [x] Check wiki documentation (`docs/wiki/petstore-catalog-availability.md`) for product rules.
- [x] Check log evidence (`docs/logs/pending-pet-visible.ndjson`) for error codes and affected pets.
- [x] Identify the bug in `app/petstore_app/catalog.py` where empty status bypasses the filter.
- [x] Create OpenSpec-style change folder with proposal, design, tasks, and spec delta.
- [ ] Implement the minimal fix: normalize empty status to "available".
- [ ] Add focused regression tests for empty status and default pending-pet exclusion.
- [ ] Run focused catalog tests to validate the fix.
- [ ] Run full test suite to ensure no regressions.
- [ ] Validate OpenSpec change folder structure.
- [ ] Create draft PR with evidence waypoints and human review notes.
- [ ] Post concise status comment to GitHub issue #78 with PR link and validation summary.
