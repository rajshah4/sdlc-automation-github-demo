# Change: Fix pending pets visible in customer catalog

## Why

Customers report seeing pets in the online pet list that the adoption desk cannot process because those pets are not yet available for adoption. Pending pets should only appear when staff explicitly request them, not in the default public-facing catalog.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-35
- Issue summary: "Pet list still shows animals customers cannot adopt yet"
- Labels: `bug`, `fast-profile-test`, `jira-to-pr-demo`
- Automation: `sdlc-story` (Jira-triggered)
- Evidence: `PENDING_PET_VISIBLE` error code in structured logs

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore data.
- The request is limited to default catalog availability filtering.
- Explicit pending-pet searches must continue to work when staff explicitly requests `status="pending"`.
- The backend `catalog.py::search_pets()` function already has the correct default behavior.
- The inconsistency is in `cloud_run_app.py::visible_pets()` which implements its own filter instead of using the centralized catalog function.

## Non-Goals

- Runtime remediation workflows
- Deployment configuration changes
- Cloud resource modifications
- Authentication or authorization changes
- Database schema changes
- Persistence layer changes
- Static UI redesign beyond necessary fixes
- New dependencies

## What Changes

1. **Backend consistency**: Update `cloud_run_app.py::visible_pets()` to use `catalog.py::search_pets()` instead of manually filtering pets
2. **Test coverage**: Add regression tests proving default searches exclude pending pets
3. **Evidence**: Document all waypoints from ticket → wiki/docs → logs → code → tests → PR

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-35 - "Pet list still shows animals customers cannot adopt yet" + "Customers keep seeing animals in the online pet list and then the adoption desk has to explain that those animals are not ready to be adopted."
- **Stop 2 - Wiki/Docs**: Checked `docs/wiki/petstore-catalog-availability.md` - confirms default catalog must show only `status="available"` pets, Nova is pet-103 with status="pending"
- **Stop 3 - Logs**: Checked `docs/logs/pending-pet-visible.ndjson` - found `PENDING_PET_VISIBLE` error code for pet-103 (Nova)
- **Stop 4 - Repo/Files**: 
  - `app/petstore_app/catalog.py` - `search_pets()` correctly defaults to `status="available"` ✓
  - `app/petstore_app/cloud_run_app.py` - `visible_pets()` manually filters instead of using catalog module ✗
  - `app/tests/test_pet_catalog.py` - existing tests pass but missing default search test
- **Stop 5 - Tests/PR**: Regression tests added, validation passed, draft PR created

## Impact

- **Customer experience**: Default pet list shows only adoptable pets
- **Staff workflows**: Explicit pending-pet searches continue to work as designed
- **Code consistency**: Single source of truth for catalog filtering logic
- **Test coverage**: Regression tests prevent future catalog filter bugs
- **Deployment**: No infrastructure or configuration changes required

## Human Gates

- **Scope approval**: Jira issue defines the product requirement
- **Implementation review**: GitHub PR review by repository maintainers
- **Merge decision**: Human approver merges after review
- **Deployment decision**: Outside automation scope
