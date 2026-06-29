# Change: Fix Pending Pets Visible in Available Catalog

## Why

Customers are seeing and interacting with pets that should not be available yet. When the catalog search function receives an empty status parameter, it incorrectly bypasses the status filter and returns all pets, including those with pending status. This violates the product rule that default searches must return only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-25
- Trigger: Jira issue created webhook
- Automation: jira-to-pr orchestrator

## Assumptions

- The bug is in the `search_pets()` function's handling of empty status values
- The fix can be isolated to the catalog module without cloud or deployment changes
- Existing explicit status="pending" searches must continue to work for operations workflows
- No schema, auth, or infrastructure changes are needed

## Non-Goals

- Cloud resource remediation
- Deployment configuration changes
- Auth, secrets, or IAM changes
- UI redesign beyond what's needed for catalog correctness
- Changes to the incident mode system in cloud_run_app.py

## What Changes

- The `search_pets()` function in `catalog.py` will default empty/whitespace status values to "available"
- The status filter condition will always apply (removing the falsy check that allowed bypass)
- New test coverage will verify that empty status parameters return only available pets

## Impact

- App behavior: Empty status searches will correctly return only available pets instead of all pets
- Tests: New test case added to verify empty status handling
- Humans: Requires PR review and merge approval before deployment

## Human Gates

- Scope approval: Automated (narrow bug fix within established product rules)
- Review approval: Required (humans review the PR)
- Merge approval: Required (humans approve and merge)
- Deployment approval: Required (humans approve deployment to production)
