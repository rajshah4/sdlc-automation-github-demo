# Change: Fix Pending Pet Visibility in Available Catalog

## Why

Support reports that Nova (a pending pet) appears in the customer-facing available pets catalog. Pending pets must not be shown to customers until operations has cleared them. This is a catalog availability regression that allows customers to start adoption flows for pets that are not ready.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-20 "Nova is showing up as adoptable - demo run 1782760729"
- GitHub issue: N/A (Jira-triggered workflow)
- Trigger: Jira webhook event `jira:issue_created`
- Automation: openhands-build work cell (Jira-triggered SDLC Automation Demo)
- Evidence:
  - Wiki: docs/wiki/petstore-catalog-availability.md
  - Log: docs/logs/pending-pet-visible.ndjson (error code PENDING_PET_VISIBLE)

## Assumptions

- The `/api/pets` endpoint represents the customer-facing available pets catalog
- The `visible_pets()` function in `cloud_run_app.py` should always filter by available status
- Nova (pet-103) has status="pending" and must not appear in default catalog results
- Operations may explicitly request pending pets via `search_pets(status="pending")` for support workflows

## Non-Goals

- Not changing the incident simulation mechanism for demo purposes
- Not modifying authentication, deployment, or cloud resources
- Not adding new dependencies or data persistence
- Not changing adoption flow validation rules

## What Changes

- Modify `visible_pets()` in `app/petstore_app/cloud_run_app.py` to always filter by `status="available"`, regardless of incident mode
- Ensure `/api/pets` endpoint never returns pending pets to customers
- Add regression test to verify pending pets are never included in the pets API response

## Impact

- App behavior: `/api/pets` endpoint will only return available pets, blocking customers from seeing or adopting pending pets
- Tests: Add regression test to verify pending pets are excluded from API responses
- Humans: PR requires review and merge approval before deployment

## Human Gates

- Scope approval: Humans authorized this work via Jira issue creation
- Review approval: Required before merge
- Merge approval: Required before deployment
- Deployment approval: Required before production changes
