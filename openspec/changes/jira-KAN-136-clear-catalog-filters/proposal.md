# Change: Clear Catalog Filters

## Why

Adopters narrow the pet catalog using filters for name and species. When they want to return to viewing all available pets, they must manually clear each filter individually, which creates friction and slows down the browsing experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-136
- Trigger: Jira issue_created webhook
- Automation: jira-request-to-pr

## Assumptions

- A single "Clear Filters" button is sufficient; no need for granular per-filter clearing
- Clearing filters should return to the default state: showing all available pets with empty name and species filters
- The button should be visible whenever any filter has a value
- Backend changes are not needed; this is a UI-only feature since filtering happens client-side

## Non-Goals

- Backend API changes for filter state management
- Persisting filter state across sessions
- Advanced filter history or undo/redo functionality
- Additional filters beyond name and species (those are separate features)

## What Changes

- Add a "Clear Filters" button to the UI search controls
- Wire the button to reset name input and species dropdown to default values
- Automatically refresh search results to show all available pets

## Impact

- **App behavior**: Users can reset all catalog filters with a single click
- **Tests**: Add UI interaction test for clear filters button functionality
- **Humans**: Product owner should confirm button placement and labeling meets UX expectations

## Human Gates

- Scope approval: This Jira issue requested the feature
- Review approval: Required before merge
- Merge approval: Required before deployment
- Deployment approval: Required before production release
