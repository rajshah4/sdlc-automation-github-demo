# Change: Fix Pending Pets Visible in Default Search

## Why

Customers are seeing pending pets (like Nova, pet-103) in the default available-pets experience. This violates the catalog availability rule that states: "Default customer-facing catalog search must show only pets with `status='available'`."

The issue creates customer confusion when they see pets they cannot adopt, extra operational burden handling questions about unavailable pets, and trust issues with the platform.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-126
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The bug is caused by empty status strings bypassing the availability filter
- Explicit `status="pending"` requests (from support/operations) remain valid
- No upstream callers depend on empty status showing all pets
- The fix can be deployed without database or configuration changes

## Non-Goals

- Changing the behavior of explicit `status="pending"` searches
- Adding new status values or pet lifecycle states
- Modifying UI or adoption flow logic
- Changing authentication or authorization rules

## What Changes

- Modify `app/petstore_app/catalog.py::search_pets()` to treat empty or whitespace-only status parameters as requests for available pets only
- Add regression tests to verify empty status handling

## Impact

- App behavior: Default search will consistently exclude pending pets even when empty status is passed
- Tests: Two new regression tests added to verify empty and whitespace status handling
- Humans: Code review, QA validation, merge approval, and deployment approval required

## Human Gates

- Scope approval: Automated (within bounds of bug fix)
- Review approval: Required before merge
- Merge approval: Required by human reviewer
- Deployment approval: Required before production release
