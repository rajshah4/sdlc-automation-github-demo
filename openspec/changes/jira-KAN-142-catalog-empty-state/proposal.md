# Change: Add clear empty-state message for filtered catalog

## Why

When adopters apply filters that exclude all catalog items, the page shows a blank grid with no explanation. Users need a friendly message that tells them no items match and offers a way to clear or adjust filters.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-142
- Trigger: `jira:issue_created`
- Automation: `sdlc-story` via Jira webhook

## Assumptions

- The empty state currently shows "No available pets match this search." but lacks a clear-filters action.
- Users need a one-click way to reset filters and return to the full catalog.
- This is a catalog-page-only change; no backend changes are needed.
- The change should be small and focused on improving the user experience when filters produce no results.

## Non-Goals

- Backend catalog filtering changes.
- New filter types or search capabilities.
- Persistence of filter state.
- Deployment changes, authentication, or infrastructure updates.

## What Changes

- Update the empty-state message in `app/web/app.js` to include a clear-filters action.
- Add a "Clear filters" button that resets the search form to its default state.
- Update the empty-state styling in `app/web/styles.css` if needed to accommodate the button.
- Verify the change works in the browser with Playwright tests.

## Impact

- App behavior: Users see a helpful message and can quickly clear filters when no pets match.
- Tests: Playwright tests verify the empty state and clear-filters functionality.
- Humans: Reviewers approve scope, review, merge, and deployment decisions.

## Human Gates

- Scope approval: Jira issue KAN-142 review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
