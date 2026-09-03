# Change: Verify and strengthen pending pet exclusion from available catalog

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default pet search must return only available pets, never pending pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-174
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story` (Jira request to pull request)
- Evidence: `PENDING_PET_VISIBLE` log signal from `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova (pet-103) has `status="pending"` and should never appear in default searches.
- The default catalog search behavior is controlled by `app/petstore_app/catalog.py` (backend) and `app/web/app.js` (frontend).
- Explicit pending-pet searches (`status="pending"`) should continue to work when explicitly requested by support or operations.
- This is primarily a verification task with potential test strengthening; the current implementation may already be correct.

## Non-Goals

- Deployment changes, authentication, database persistence, and unrelated UI features are out of scope.
- Schema changes, new dependencies, or architectural changes are not required.
- Changes to adoption flow, payment processing, or user management are not in scope.

## What Changes

- Verify that backend default search correctly filters pending pets (catalog.py line 31: `status="available"`).
- Verify that frontend UI correctly filters pending pets (app.js line 17: `pet.status === "available"`).
- Add explicit regression test `test_default_search_excludes_pending_pets()` to make the requirement more visible and prevent future regressions.
- Ensure test coverage explicitly verifies Nova (pet-103) never appears in default available searches.
- Document findings in the PR with evidence waypoints.

## Evidence Waypoints

- **Stop 1 - Ticket**: KAN-174 reports "Customers are seeing pets that are not available".
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms Nova is pet-103 with status="pending" and that `PENDING_PET_VISIBLE` logs indicate catalog regressions.
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows ERROR with code `PENDING_PET_VISIBLE` for pet-103 (Nova) on 2026-06-29.
- **Stop 4 - Repo/Files**: Backend catalog.py (lines 27-56) and frontend app.js (lines 14-18) reviewed. Both have correct filtering logic in place.
- **Stop 5 - Tests/PR**: Add explicit regression test; run pytest; open PR with findings.

## Impact

- **App behavior**: Customers continue to see only available pets in default catalog search. No behavior change if code is already correct.
- **Tests**: New explicit regression test `test_default_search_excludes_pending_pets()` makes the requirement visible and prevents future regressions.
- **Humans**: Reviewers approve scope, review findings, approve merge, and deployment decisions.

## Human Gates

- **Scope approval**: Jira issue triage and priority review.
- **Review approval**: GitHub PR review by repository maintainers.
- **Merge approval**: Repository maintainers with write access.
- **Deployment approval**: Outside this automation scope; requires human approval.
