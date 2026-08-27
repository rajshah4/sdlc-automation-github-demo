# Change: Fix unavailable pets appearing in catalog

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The catalog must only show available pets by default to maintain trust and operational efficiency.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-141
- Issue key: KAN-141
- Trigger: Jira issue created webhook
- Automation: jira-request-to-pr

## Assumptions

- Nova (pet-103) has `status="pending"` in the Petstore seed data
- The issue is limited to the default catalog search behavior
- Explicit pending-pet searches (for support/operations) should continue to work when explicitly requested with `status="pending"`
- The bug is in the backend `search_pets()` function, not in the UI layer

## Non-Goals

- Changing the UI filter logic (already correct)
- Modifying the adoption order validation (already correct)
- Deployment configuration, authentication, or database persistence changes

## What Changes

- Fix the `search_pets()` function in `catalog.py` to properly handle empty status parameter
- Ensure default catalog search excludes pending pets even when `status=""` is passed
- Add regression test to verify the bug is fixed and prevent future regressions

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-141 reports customers seeing pets that are not available
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` contains error code `PENDING_PET_VISIBLE` showing pet-103 (Nova) appeared in available-pets experience
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` has a bug on line 50 where empty status string bypasses the status filter
- **Stop 5 - Tests/PR**: Regression test added and draft PR created for human review

## Impact

- App behavior: Default catalog search will correctly exclude pending pets, even when called with empty status parameter
- Tests: New regression test ensures empty status defaults to showing only available pets
- Humans: PR reviewers approve scope, implementation approach, and merge decision

## Human Gates

- Scope approval: Jira issue and PR review
- Review approval: GitHub PR review by repository maintainers
- Merge approval: Repository maintainers after CI passes and review complete
- Deployment approval: Outside this automation scope
