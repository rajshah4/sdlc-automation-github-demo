# Tasks

## Investigation
- [x] Read Jira issue KAN-70
- [x] Check `docs/wiki/petstore-catalog-availability.md` for catalog rules
- [x] Check `docs/logs/pending-pet-visible.ndjson` for error evidence
- [x] Identify root cause in `app/petstore_app/catalog.py`

## Implementation
- [ ] Fix status filter logic in `search_pets()` function
- [ ] Add regression test for empty status string
- [ ] Add regression test for default search behavior

## Validation
- [ ] Run all existing catalog tests
- [ ] Run new regression tests
- [ ] Verify pending search still works for explicit requests

## Documentation
- [ ] Create OpenSpec change artifacts
- [ ] Update PR with evidence waypoints
- [ ] Post status to Jira issue

## Handoff
- [ ] Open draft PR
- [ ] Add `openhands-qa` label to trigger QA automation
- [ ] Link PR in Jira issue
