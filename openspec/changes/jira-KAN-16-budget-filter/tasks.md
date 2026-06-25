# Tasks

- [x] Create OpenSpec-style change artifacts for KAN-16.
- [x] Document proposal, design, spec delta, and validation plan.
- [ ] Update `app/web/index.html` to add "Maximum Budget" input field.
- [ ] Update `app/web/app.js` to add `feeCents` property to pet data.
- [ ] Update `app/web/app.js` filtering logic to handle budget filter.
- [ ] Run backend tests to verify no regression: `pytest app/tests/test_pet_catalog.py`.
- [ ] Visual verification: open index.html and test budget filter scenarios.
- [ ] Create feature branch `jira/KAN-16-budget-filter-ui`.
- [ ] Commit OpenSpec artifacts and UI changes.
- [ ] Open draft PR with evidence and human review notes.
- [ ] Post Jira comment with PR link, implementation details, and validation results.

## Evidence Checklist

- [ ] Screenshot or description showing budget input field in UI.
- [ ] Test results showing all budget filter scenarios work correctly.
- [ ] Backend test results showing no regression.
- [ ] Link to OpenSpec change folder in PR description.

## Assumptions Validated

- Backend `max_adoption_fee_cents` parameter exists: ✓ (catalog.py line 33)
- Backend tests exist: ✓ (test_pet_catalog.py lines 24-38)
- Money is in integer cents: ✓ (AGENTS.md line 29, catalog.py Pet dataclass)
- UI is static client-side HTML/JS: ✓ (app/web/ directory)
