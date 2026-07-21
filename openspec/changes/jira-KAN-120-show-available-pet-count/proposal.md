# Change: Show the number of available pets in catalog results

## Why

As an adopter, I want to see how many available pets match my catalog search so I can understand the results at a glance. This improves user experience by providing immediate feedback on search results.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-120
- Issue key: KAN-120
- Trigger: jira:issue_created webhook
- Automation: jira-to-pr (sdlc-story)

## Assumptions

- The count should display the number of available pets in the current filtered results.
- Pending pets must not be included in the count (only available pets).
- The count updates dynamically when catalog search or filters change.
- Implementation covers both backend API and UI display.

## Non-Goals

- Real-time updates from database changes (this is a static catalog demo).
- Complex analytics or pet statistics beyond simple count.
- Count persistence or user preferences.
- Auth, deployment, or infrastructure changes.

## What Changes

- Add a `count_available` method to the catalog module that returns the count of available pets matching current filters.
- Update the UI to display the count prominently near the results section.
- Add comprehensive backend tests covering count behavior with various filters.
- Ensure count excludes pending pets and updates when filters change.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira issue KAN-120 with acceptance criteria for count display.
- `Stop 2 - Wiki/Docs`: No specific wiki entries; used AGENTS.md and Petstore product rules.
- `Stop 3 - Logs`: No log fixtures required for this feature.
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py`, `app/web/app.js`, `app/web/index.html`.
- `Stop 5 - Tests/PR`: Backend tests in `app/tests/test_pet_catalog.py`, draft PR for human review.

## Impact

- App behavior: Users see a count of available pets matching their search.
- Tests: Backend tests ensure count accuracy and filter behavior.
- UI: Static HTML and JS display the count dynamically.
- Humans: Reviewers approve scope, implementation, and merge decision.

## Human Gates

- Scope approval: Jira issue acceptance criteria.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation.
