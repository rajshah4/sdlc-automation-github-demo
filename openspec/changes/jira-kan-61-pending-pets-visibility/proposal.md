# Change: Fix Pending Pets Visibility Regression

## Why

Support reports that Nova (pet-103, status="pending") is appearing in the available pets list, violating the product rule that default pet search must return only available pets. The `PENDING_PET_VISIBLE` error log from 2026-06-29 confirms pending pets leaked into the customer-facing catalog experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-61
- Trigger: Jira webhook
- Automation: SDLC sidekick demo with parallel docs/logs/repo scouts

## Assumptions

- The backend catalog filter is working correctly (verified by existing tests)
- The frontend UI JavaScript correctly filters by `status === "available"` (verified by Playwright test expectations)
- The bug was either already fixed or manifested in a previous state

## Non-Goals

- Changing UI behavior or adding new catalog features
- Modifying pet status workflow or adoption business logic
- Adding authentication, authorization, or multi-user features

## What Changes

- Add comprehensive regression test coverage to prevent pending pets from appearing in default available-only search results
- The backend `search_pets()` function already implements the correct filter logic with `status="available"` as the default parameter
- This change focuses on test coverage to prevent future regressions

## Impact

- App behavior: No changes—filter logic already correct
- Tests: New explicit regression test for Nova exclusion with `PENDING_PET_VISIBLE` error marker
- Humans: Confidence that pending pets will stay hidden from customer search

## Human Gates

- Scope approval: Automated based on ticket analysis
- Review approval: Human must review and approve PR
- Merge approval: Human must approve merge to main
- Deployment approval: Human controls production deployment
