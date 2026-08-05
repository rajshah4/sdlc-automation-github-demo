# Design

## Context

The Petstore catalog UI currently shows a simple text message "No available pets match this search." when filters produce no results. The existing empty state uses CSS class `.empty` and displays in the results list. Users have no quick way to reset filters without manually clearing each input.

The current implementation filters pets by:
- Name (text search)
- Species (dropdown selection)
- Status (hardcoded to "available" only)

## Decision

- Add a "Clear filters" button to the empty-state message that resets all filter inputs to their default values.
- Update the `renderResults()` function in `app/web/app.js` to render the button when no matches are found.
- Attach a click event listener to the button that:
  - Clears the name search input (`#query`)
  - Resets the species dropdown to "Any" (`#species`)
  - Re-renders the results to show all available pets
- Keep the empty-state styling consistent with the existing `.empty` class.
- Make the button visually distinct but simple (reuse existing button styles with a secondary appearance).

## Risks

- Users might expect filters to persist across page refreshes (out of scope; no localStorage changes planned).
- The clear action should feel intuitive; if users don't notice the button, they may still be confused (mitigated by clear button text and placement).

## Validation Plan

- Run the existing Playwright test suite: `app/web/tests/catalog-search.playwright.mjs`
- Extend the test to verify:
  - Empty state appears when filters exclude all pets
  - Clear filters button is visible and clickable
  - Clicking the button resets filters and shows all available pets
- Verify the UI manually if Playwright is unavailable in the runtime.
