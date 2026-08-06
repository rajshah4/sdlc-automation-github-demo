# Change: Add optional name sort to pet catalog

## Why

Adopters want to sort pets by name to scan the catalog more easily. Currently, the catalog returns pets in the order they appear in the data source, which is not alphabetically organized.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-108
- Story title: "As an adopter, I want to sort pets by name"
- Automation: Replicated Jira delegated factory
- Run ID: `replicated-factory-20260715-142322`

## Assumptions

- The sort parameter is optional; leaving it unset preserves the current catalog order.
- Name sort orders pets alphabetically by name (case-insensitive).
- The sort applies after all filters (species, status, tag, query) are applied.
- The backend catalog search function drives the sort behavior.
- The UI exposes the sort option to adopters.

## Non-Goals

- Multiple sort fields (e.g., sort by age, fee) are out of scope.
- Reverse/descending sort is out of scope.
- Deployment changes, authentication, persistence, and new dependencies are out of scope.

## What Changes

- Add an optional `sort_by` parameter to `search_pets()` in `app/petstore_app/catalog.py`.
- When `sort_by="name"`, return matching pets ordered alphabetically by name.
- When `sort_by` is not set or is `None`, preserve the current catalog order.
- Add a sort dropdown to the UI in `app/web/index.html`.
- Update the UI JavaScript in `app/web/app.js` to apply name sort when selected.
- Add focused backend tests for sorted results and default ordering.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-108 acceptance criteria reviewed.
- `Stop 2 - Wiki/Docs`: No specific docs required for this feature; consulted petstore implementation map.
- `Stop 3 - Logs`: Not applicable (feature request, no error logs).
- `Stop 4 - Repo/Files`: Reviewed `app/petstore_app/catalog.py`, `app/web/app.js`, `app/web/index.html`, and `app/tests/test_pet_catalog.py`.
- `Stop 5 - Tests/PR`: Tests added and run; PR created with evidence.

## Impact

- App behavior: Adopters can optionally sort catalog results by name.
- Tests: Backend tests verify sorted and unsorted results.
- Humans: Reviewers approve scope, merge, and deployment decisions.

## Human Gates

- Scope approval: Jira issue review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
