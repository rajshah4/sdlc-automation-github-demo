# Change: Filter Pending Pets from Available List

## Why

Families visiting the online petstore are finding animals in the available pets list, then learning at the adoption desk that those animals are not ready to be adopted. This creates a poor customer experience and wastes staff time. The available pets list must show only pets that are actually ready for adoption.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-33
- Trigger: Jira issue created event with label `jira-to-pr-demo`
- Automation: SDLC Automation Demo - Jira to PR work cell

## Assumptions

- The default available pets list should exclude pets with `status="pending"`.
- Support and operations staff may still explicitly request pending pets when needed for their workflows.
- This is a catalog filter bug, not a data integrity issue.
- The fix can be implemented without schema changes, new dependencies, or deployment configuration changes.

## Non-Goals

- Changing the underlying pet data structure or status values.
- Adding new pet statuses beyond `available` and `pending`.
- Modifying authentication, authorization, or access control.
- Changing the UI beyond what is necessary to reflect the correct catalog filter.
- Adding new APIs or endpoints.

## What Changes

- The `/api/pets` endpoint will return only pets with `status="available"` by default.
- The website home page will display only available pets.
- Explicit requests for pending pets (e.g., `status="pending"`) will still work for operations staff.
- The `visible_pets()` function will apply the correct filter in healthy mode.

## Impact

- App behavior: Default catalog searches will exclude pending pets.
- Tests: Add regression tests proving pending pets are filtered from default results.
- Humans: Requires PR review approval and merge approval before deployment.

## Human Gates

- Scope approval: Automated based on Jira issue label trigger.
- Review approval: Required from human reviewer.
- Merge approval: Required from human approver.
- Deployment approval: Required before deploying to production.
