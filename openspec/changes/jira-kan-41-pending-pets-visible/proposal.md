# Change: Fix pending pets showing in available pets list

## Why

Customers report that the available pets page includes animals that should not be adoptable. Specifically, pets with "pending" status (such as Nova, pet-103) are appearing in the default available pets experience, violating the product rule that only pets with "available" status should be shown by default.

## Source

- Jira issue: https://rajshah.atlassian.net/browse/KAN-41
- Actual URL: https://api.atlassian.com/ex/jira/19c67202-a774-4b89-9aed-0466783f68e2/browse/KAN-41
- Trigger: Jira webhook sidekick v2
- Automation: SDLC Automation Demo - main implementation agent

## Assumptions

- The `visible_pets()` function in `app/petstore_app/cloud_run_app.py` is the primary filter for the available pets list
- The incident mode simulation logic (lines 92-95) is intentionally bypassing the status filter, causing pending pets to appear
- Removing the incident mode bypass will restore correct behavior
- No runtime config file currently exists to override this behavior
- The intended behavior is for `visible_pets()` to always filter by status == "available" in production

## Non-Goals

- This fix does not add support for explicit pending pet searches
- This fix does not modify the adoption validation logic in `adoptions.py`
- This fix does not change the Pet data model or catalog structure
- This fix does not modify UI components or add new features

## What Changes

- Remove the incident mode bypass logic from `visible_pets()` function
- Ensure `visible_pets()` always filters pets by `status == "available"`
- Update or add tests to verify pending pets are never visible in default results
- Remove or update the `test_bad_catalog_filter_exposes_pending_pet` test that validates the now-removed incident simulation behavior

## Impact

- App behavior: Default available pets list will correctly exclude pending pets
- Tests: Tests that validate incident mode behavior need to be updated or removed
- Humans: PR requires scope, review, merge, and deployment approval

## Human Gates

- Scope approval: Required - confirm removing incident simulation is the correct fix
- Review approval: Required - human must review the code changes
- Merge approval: Required - human must approve merge to main
- Deployment approval: Required - human must approve production deployment
