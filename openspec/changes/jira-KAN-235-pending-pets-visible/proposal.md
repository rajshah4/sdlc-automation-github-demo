# Change: Fix Pending Pets Visible in Default Search

## Why

Support reports that customers are seeing pets with pending status in the default available-pets experience. This violates the product rule that default pet search must return only available pets, creating confusion for customers and extra work for operations staff.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-235
- Trigger: Jira webhook `jira:issue_created` event
- Automation: SDLC Automation Demo - Issue to PR

## Assumptions

- The bug is in the catalog search logic where an empty status string bypasses the status filter
- Fixing the status filter logic will not break explicit pending-pet searches that operations uses
- Nova (pet-103) is the demo pet with pending status that should not appear in default results
- No database or schema changes are needed

## Non-Goals

- Changing the UI behavior beyond what the backend fix naturally provides
- Adding new pet statuses or workflow states
- Modifying adoption flow logic
- Changing authentication or authorization rules

## What Changes

- Fix the `search_pets` function in `app/petstore_app/catalog.py` to properly enforce status filtering even when an empty status string is passed
- Add regression tests to ensure pending pets never appear in default available-only searches
- Ensure explicit `status="pending"` searches continue to work for operations workflows

## Impact

- App behavior: Default searches will correctly exclude pending pets; explicit pending searches will continue to work
- Tests: Add focused regression test for the empty-status-string case
- Humans: Operations will no longer receive complaints about pending pets appearing in customer-facing catalog

## Human Gates

- Scope approval: Automated via Jira issue creation
- Review approval: Required before merge
- Merge approval: Required by repository maintainer
- Deployment approval: Required before production release
