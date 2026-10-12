# Change: Fix Pending Pets Appearing in Available Catalog

## Why

Support reports that customers are able to see and start adoption flows for pets with `status="pending"`. This violates the product rule that the default customer-facing catalog search must show only pets with `status="available"`. Log evidence shows `PENDING_PET_VISIBLE` errors with `pet-103` (Nova) appearing in the available-pets experience, confirming a catalog availability regression.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-233
- Trigger: Jira webhook on issue creation
- Automation: SDLC Automation Demo - Jira issue to draft pull request

## Assumptions

- The bug is in `app/petstore_app/catalog.py` line 50 where an empty status string bypasses the filter
- No external services, database changes, or UI modifications are needed
- The existing `status` parameter default of `"available"` is correct product behavior
- Support workflows that explicitly request `status="pending"` should continue to work

## Non-Goals

- Not changing the `status="pending"` search capability for operations
- Not modifying pet data, adoption flows, or UI components
- Not adding new status types or filtering capabilities

## What Changes

- Fix the pet catalog search filter logic in `catalog.py` to ensure status filter always applies
- Remove truthy check that allows empty status strings to bypass the filter
- Add regression test proving pending pets excluded from default search

## Impact

- App behavior: Default searches now correctly return only available pets; pending pets excluded
- Tests: New regression test `test_default_search_excludes_pending_pets` added
- Humans: Support ticket volume reduces; customers no longer see unavailable pets

## Human Gates

- Scope approval: Humans confirm this catalog fix aligns with product requirements
- Review approval: Humans review code changes and test coverage
- Merge approval: Humans approve merge after CI passes
- Deployment approval: Humans decide deployment timing
