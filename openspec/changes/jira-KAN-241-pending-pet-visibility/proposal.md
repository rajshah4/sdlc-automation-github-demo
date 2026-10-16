# Change: Prevent Pending Pets from Appearing in Available Pet Search

## Why

Support reports that customers are seeing pets marked as "pending" in their available-pets search results. This violates the petstore's core catalog availability rules: only pets with `status="available"` should appear in the default customer-facing catalog experience. Pending pets should remain hidden unless explicitly requested by support or operations staff.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-241
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Issue to PR

## Evidence Waypoints

### Stop 1 - Ticket

**Issue**: KAN-241 "Customers are seeing pets that are not available"

**Description**: Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations.

### Stop 2 - Wiki/Docs

**Checked**: `docs/wiki/petstore-catalog-availability.md`

**Findings**: 
- Default customer-facing catalog search must show only pets with `status="available"`
- Support/operations may explicitly request `status="pending"` when investigating
- Nova is `pet-103` with `status="pending"`
- `PENDING_PET_VISIBLE` log error indicates a pending pet appeared in available-pets experience (catalog regression)

### Stop 3 - Logs

**Checked**: `docs/logs/pending-pet-visible.ndjson`

**Findings**:
- Error code: `PENDING_PET_VISIBLE`
- Pending pet ID: `pet-103` (Nova)
- Customer impact: "Pending pets were visible in the available-pets experience"
- Bug signal: `catalog_availability_regression`, `safe_to_fix: true`
- Timestamp: 2026-06-29T12:00:00Z

### Stop 4 - Repo/Files

**Backend Code** (`app/petstore_app/catalog.py`):
- `search_pets()` function has correct default: `status: str = "available"` (line 31)
- Filter logic correctly checks: `if normalized_status and normalized_status != pet.status` (line 50)
- Backend behavior is correct

**UI Code** (`app/web/app.js`):
- Filter includes: `pet.status === "available"` (line 17)
- UI behavior is correct

**Adoption Code** (`app/petstore_app/adoptions.py`):
- Validates: `if pet.status != "available"` with error "pet is not available for adoption" (line 34-35)
- Adoption validation is correct

**Test Gap** (`app/tests/test_pet_catalog.py`):
- `test_search_pets_filters_by_species_and_status` (lines 6-9) tests `search_pets(species="dog")` and expects only `pet-101` (Scout, available)
- This implicitly tests that Nova (pet-103, pending) is excluded
- **BUT**: the test doesn't explicitly assert that pending pets are excluded, making the regression prevention implicit rather than explicit
- `test_search_pets_can_find_pending_pets_when_requested` (lines 12-15) correctly tests explicit pending searches
- Test for adoption rejection exists: `test_create_adoption_order_rejects_pending_pet` (test_adoptions.py lines 19-21)

### Stop 5 - Tests/PR

Tests and PR to be created after spec approval.

## Root Cause

The code itself works correctly. The issue is a **test coverage gap**: there is no explicit test that directly asserts "default search excludes pending pets." The existing test `test_search_pets_filters_by_species_and_status` relies on implicit behavior rather than explicitly documenting and testing the pending-pet-exclusion rule.

## Assumptions

- The historical `PENDING_PET_VISIBLE` log indicates there was customer impact
- Adding explicit test coverage will prevent regressions and make the availability rule clear
- No code changes needed; only test additions required
- This is a safe documentation/test-coverage fix with no behavior change

## Non-Goals

- Changing the backend filtering logic (already correct)
- Changing the UI filtering logic (already correct)
- Changing adoption validation (already correct)
- Adding new pet statuses or catalog features
- Modifying how support/operations access pending pets

## What Changes

- Add explicit regression test: `test_default_search_excludes_pending_pets()` that specifically asserts Nova (pet-103, pending) does not appear in `search_pets()` results
- Update test to make the pending-pet-exclusion rule explicit and self-documenting

## Impact

- **App behavior**: None - no functional changes, only improved test coverage
- **Tests**: One new test added to `app/tests/test_pet_catalog.py`
- **Humans**: Clearer test documentation reduces risk of future regressions. Review and merge approval required.

## Human Gates

- Scope approval: Required (this proposal)
- Review approval: Required before merge
- Merge approval: Required before production
- Deployment: Follows existing process
