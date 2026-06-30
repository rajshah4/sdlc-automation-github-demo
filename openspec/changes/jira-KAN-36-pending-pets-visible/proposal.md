# Change: Fix Pending Pets Visible in Customer Catalog

## Why

Customers report seeing pets in the online catalog that the adoption desk cannot offer yet. The default customer-facing catalog must show only available pets. Support staff should still be able to explicitly search for pending pets when investigating cases, but pending pets must not appear in the default available-pets experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-36
- Trigger: jira:issue_created with label `control-experiment`
- Automation: SDLC Automation Demo - Jira to PR control work cell

## Assumptions

- The `search_pets()` function in `catalog.py` correctly filters by status and should be the source of truth for catalog behavior.
- The web interface `visible_pets()` function bypasses this filter when in incident mode, exposing all pets regardless of status.
- The runtime incident mode is a demo feature and should not affect production customer-facing catalog behavior.
- Nova (pet-103) with status="pending" is the known test case per `docs/wiki/petstore-catalog-availability.md`.
- The `PENDING_PET_VISIBLE` error code in logs indicates this regression.

## Non-Goals

- Cloud remediation or runtime configuration changes
- Deployment settings or infrastructure changes
- Authentication, secrets, or IAM changes
- Database or persistence layer changes
- UI redesign beyond catalog data correctness
- Removing incident mode simulation entirely (it may be useful for demo purposes in non-production paths)

## What Changes

- The `/api/pets` endpoint will use `search_pets()` from `catalog.py` to ensure only available pets are returned by default.
- The home page rendering will use `search_pets()` to ensure only available pets are displayed by default.
- Incident mode will be preserved for demo/testing purposes but will not affect the customer catalog filter.
- Existing explicit status filter support (e.g., `status="pending"`) will be preserved for staff workflows.

## Impact

- App behavior: Default catalog API and web page will correctly show only available pets. Nova (pet-103) will not appear in default results.
- Tests: Add regression tests to verify pending pets do not appear in default catalog results.
- Humans: PR review required to confirm the fix correctly addresses the customer issue without breaking staff workflows or incident simulation.

## Human Gates

- Scope approval: Required if additional endpoints or UI changes are needed beyond `/api/pets` and home page.
- Review approval: Required before merge.
- Merge approval: Required.
- Deployment approval: Required before production rollout.
