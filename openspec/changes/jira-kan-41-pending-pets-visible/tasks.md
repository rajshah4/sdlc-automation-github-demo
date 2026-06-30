# Tasks

- [x] Create OpenSpec-style change folder at `openspec/changes/jira-kan-41-pending-pets-visible/`
- [x] Write proposal.md with source, assumptions, impact, and human gates
- [x] Write specs/catalog/spec.md with requirements for status filtering
- [x] Write design.md with context, decisions, risks, and validation plan
- [x] Remove incident mode bypass logic from `visible_pets()` function
- [x] Update or remove tests that validate the incident simulation behavior
- [x] Add regression test to ensure pending pets never appear in default results
- [x] Run validation: `pytest app/tests/test_cloud_run_app.py -v` - all 3 tests passed
- [x] Run full app tests: `pytest app/tests/ -v` - all 14 tests passed
- [ ] Open draft PR with evidence waypoints and KAN-41 reference
- [ ] Add `openhands-qa` label to trigger QA automation
