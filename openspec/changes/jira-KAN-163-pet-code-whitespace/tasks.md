# Tasks: Pet Code Whitespace Fix

## Evidence Gathering ✅

- [x] **Stop 1 - Ticket**: Reviewed Jira issue KAN-163 describing support agents copying pet codes with accidental whitespace
- [x] **Stop 2 - Wiki/Docs**: Reviewed AGENTS.md and repo structure (no specific docs for pet code format)
- [x] **Stop 3 - Logs**: No log fixtures available for this issue (not a logged error scenario)
- [x] **Stop 4 - Repo/Files**: 
  - Investigated `app/petstore_app/adoptions.py` (lines 19-37) - confirmed exact string match without `.strip()`
  - Investigated `app/petstore_app/catalog.py` (lines 27-58) - confirmed `search_pets()` does normalize with `.strip()`
  - Reviewed existing tests in `app/tests/test_adoptions.py` - confirmed no whitespace test coverage
- [x] **Code Explorer Investigation**: Delegated investigation confirmed root cause with HIGH confidence (95%)

## Implementation Tasks

- [ ] Modify `app/petstore_app/adoptions.py`:
  - [ ] Add `pet_id = pet_id.strip()` in `create_adoption_order()` before calling `_find_pet()`
  - [ ] Verify change aligns with existing `search_pets()` normalization pattern

- [ ] Add test coverage in `app/tests/test_adoptions.py`:
  - [ ] Add `test_create_adoption_order_trims_leading_whitespace()` for `" pet-100"`
  - [ ] Add `test_create_adoption_order_trims_trailing_whitespace()` for `"pet-100 "`
  - [ ] Add `test_create_adoption_order_trims_surrounding_whitespace()` for `" pet-100 "`

## Validation Tasks

- [ ] Run adoption tests: `pytest app/tests/test_adoptions.py -v`
- [ ] Run full test suite: `pytest app/tests/ -v` (if repository guidance requires broader validation)
- [ ] Validate OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-163-pet-code-whitespace/`

## PR and Handoff Tasks

- [ ] Create feature branch from main
- [ ] Commit changes with clear message referencing KAN-163
- [ ] Open draft PR with:
  - [ ] Link to Jira issue KAN-163
  - [ ] Evidence waypoints summary
  - [ ] OpenSpec change path reference
  - [ ] Test results
  - [ ] Assumptions and risks
  - [ ] Note that humans approve review and merge
  - [ ] Include OpenHands conversation link from `$AUTOMATION_SESSION_URL`
  - [ ] End with: "Created by an AI agent (OpenHands) on behalf of Rajiv Shah."
- [ ] Add `openhands-review` label to PR for code review automation

## Human Gates

- [ ] **Review Gate**: Human reviewer must approve the PR before merge
- [ ] **Merge Gate**: Human must perform the actual merge to main
- [ ] **Deployment Gate**: Human must approve any deployment to production (if applicable)

## Risk Assessment

**Low Risk:**
- Whitespace trimming is standard expected behavior
- No breaking changes to API or data structures
- Aligns with existing normalization in `search_pets()`
- Comprehensive test coverage added

**No identified blockers or security concerns.**
