# Change: Fix available pets filter to exclude pending pets

## Why

Customers report that the available pets page includes animals that should not be adoptable. The default customer-facing catalog search must show only pets with `status="available"`. Pending pets like Nova (pet-103) should not appear in available-pets views unless explicitly requested by support or operations workflows.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-39
- Trigger: Sidekick demo v2 full
- Automation: SDLC implementation agent

## Assumptions

- The bug is in `catalog.py` `search_pets()` function where empty status strings bypass the filter
- Nova (pet-103) has `status="pending"` and is the demo test case
- Explicit `status="pending"` requests from support workflows must still work
- The fix should not change API contracts or existing test expectations
- No schema, deployment, or environment changes are needed

## Non-Goals

- Changing the `cloud_run_app.py` `visible_pets()` function (separate UI concern)
- Adding new status types or transitions
- Modifying pet data or fixture definitions
- Changing authentication or authorization behavior

## What Changes

- Fix `catalog.py` `search_pets()` to enforce the default `status="available"` filter even when called with empty status string
- Add regression test proving empty status defaults to available-only results
- Add test proving Nova (pet-103) does not appear in default available searches

## Impact

- App behavior: Default catalog searches will correctly filter to available pets only
- Tests: New focused regression tests added to prevent future occurrences
- Humans: PR requires scope, review, merge, and deployment approval

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Required by branch protection
- Deployment approval: Required before production rollout
