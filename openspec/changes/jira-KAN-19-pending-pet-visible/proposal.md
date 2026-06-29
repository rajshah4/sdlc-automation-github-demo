# Change: Fix Pending Pet Visibility in Available Catalog

## Why

Customers are seeing pets that are not available for adoption in the available-pets experience. Specifically, Nova (a pending pet) is appearing in the catalog when only available pets should be shown by default.

## Source

- **Primary source**: Jira webhook `jira:issue_created` event
- Jira issue: https://rajistics.atlassian.net/browse/KAN-19
- GitHub issue: N/A (Jira-triggered automation)
- Issue summary: "Customers are seeing pets that are not available - live webhook test 1782753925"
- Automation: `openhands-build` (Jira-triggered work cell)

## Evidence Waypoints

### Stop 1 - Ticket
- **Jira KAN-19**: "Customers are seeing pets that are not available"
- **Business clue**: "Support reports that Nova appears in the available pets list even though she should not be adoptable"
- **Log clue**: `PENDING_PET_VISIBLE`
- **Direction**: "Please use the wiki/docs and logs before changing code"

### Stop 2 - Wiki/Docs
- **File**: `docs/wiki/petstore-catalog-availability.md`
- **Rule**: "Default customer-facing catalog search must show only pets with `status="available"`"
- **Constraint**: "Pending pets must not appear in the default available-pets experience"
- **Mapping**: Nova is `pet-103` with `status="pending"`
- **Interpretation**: `PENDING_PET_VISIBLE` log indicates a catalog regression

### Stop 3 - Logs
- **File**: `docs/logs/pending-pet-visible.ndjson`
- **Error code**: `PENDING_PET_VISIBLE`
- **Incident type**: `petstore_website_catalog_regression`
- **Evidence**: `"pending_pet_ids":["pet-103"]`
- **Customer impact**: "Pending pets were visible in the available-pets experience"

### Stop 4 - Repo/Files
- **Repository**: `sdlc-automation-github-demo`
- **Bug location**: `app/petstore_app/cloud_run_app.py`, function `visible_pets()` (lines 92-95)
- **Root cause**: When `current_mode() == INCIDENT_MODE`, the function returns all pets including pending ones, violating the catalog availability rule
- **Correct implementation**: `app/petstore_app/catalog.py`, function `search_pets()` with default `status="available"`
- **Existing tests**: `app/tests/test_pet_catalog.py` confirms catalog search should filter by status

### Stop 5 - Tests/PR
- Will add focused regression test for the web API `/api/pets` endpoint
- Will verify that pending pets never appear in the available-pets response
- Will create draft PR with fix and evidence

## Assumptions

- The `visible_pets()` function should always return only available pets, regardless of runtime mode
- The INCIDENT_MODE simulation is for demo purposes but should not bypass product rules
- The fix should use the existing `search_pets()` function from `catalog.py` instead of reimplementing filtering logic
- No changes to deployment settings, secrets, auth, or cloud resources are needed

## Non-Goals

- Do not change the incident simulation infrastructure (mode switching, runtime config)
- Do not modify the `search_pets()` function in `catalog.py` (it's already correct)
- Do not change how explicit pending-pet queries work (support/ops workflows)
- Do not add new dependencies or change deployment configuration

## What Changes

- Replace the `visible_pets()` function implementation to use `catalog.search_pets(status="available")`
- Remove the mode-dependent logic that returns all pets in INCIDENT_MODE
- Ensure pending pets never appear in customer-facing catalog, regardless of runtime state

## Impact

- **App behavior**: The `/api/pets` endpoint and home page will now always show only available pets
- **Tests**: Add focused regression test for pending pet filtering in web API
- **Humans**: PR reviewers must verify the fix doesn't break incident simulation capabilities

## Human Gates

- **Scope approval**: Automated via Jira `openhands-requested` label
- **Review approval**: Required before merge
- **Merge approval**: Required before merge
- **Deployment approval**: Required before production deployment
