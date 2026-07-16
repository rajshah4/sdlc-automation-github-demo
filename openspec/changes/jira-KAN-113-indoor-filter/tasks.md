# Tasks

- [x] Create OpenSpec-style change folder at `openspec/changes/jira-KAN-113-indoor-filter/`
- [x] Write proposal.md with why, assumptions, non-goals, and human gates
- [x] Write spec delta with acceptance criteria as scenarios
- [x] Write design.md with context, decisions, risks, and validation plan
- [ ] Add backend test coverage for indoor tag filtering
- [ ] Update UI to add "Indoor only" checkbox control
- [ ] Update UI JavaScript to wire checkbox to tag filtering
- [ ] Run backend tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- [ ] Run full test suite: `python3 -m pytest -q`
- [ ] Manual UI smoke test to verify checkbox behavior
- [ ] Validate OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-113-indoor-filter`
- [ ] Create feature branch and commit changes
- [ ] Open draft PR with evidence and human review notes
- [ ] Add `openhands-qa` label to PR for QA work cell
