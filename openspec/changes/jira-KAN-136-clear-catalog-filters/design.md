# Design: Clear Catalog Filters

## Context

The petstore UI currently has two filter controls: a text input for pet name search and a dropdown for species selection. Users can apply these filters by clicking "Find Pets", but there's no quick way to reset both filters simultaneously. Users must manually clear the text input and change the dropdown back to "Any", which is tedious when exploring different searches.

The catalog filtering logic is entirely client-side in `app/web/app.js`, with no backend state management. This makes the solution straightforward: add a UI button that resets the form controls and refreshes the display.

## Decision

Add a "Clear Filters" button that resets both filter inputs and automatically refreshes results.

## Implementation Approach

This is a UI-only change. The catalog filtering logic already exists in `app/web/app.js` and operates client-side. We need to add a button and handler that resets the filter controls to their default values and triggers a search.

## Files to Modify

### `app/web/index.html`

Add a "Clear Filters" button in the toolbar section, positioned after the "Find Pets" button.

```html
<button id="clear-button">Clear Filters</button>
```

### `app/web/app.js`

Add an event listener for the clear button that:
1. Sets the query input value to empty string
2. Sets the species select value to empty string (default "Any")
3. Calls `renderResults()` to refresh the display

```javascript
document.querySelector("#clear-button").addEventListener("click", () => {
  document.querySelector("#query").value = "";
  document.querySelector("#species").value = "";
  renderResults();
});
```

## Testing Strategy

### Backend Tests
No backend changes required, so no new backend tests needed.

### UI Tests
Add a Playwright test to `app/web/tests/catalog-search.playwright.mjs` that:
1. Opens the petstore UI
2. Enters filter values (name and species)
3. Verifies filtered results appear
4. Clicks the "Clear Filters" button
5. Verifies all available pets are shown again

## Validation Plan

1. Run existing backend tests to ensure no regression: `python3 -m pytest -q app/tests/`
2. Start local web server: `python3 -m http.server 4173 --directory app/web`
3. Manually verify button appears and works correctly
4. Run Playwright tests if environment supports it

## Edge Cases

- **Empty filters**: Clicking clear when filters are already empty should have no adverse effect
- **Single filter set**: Should clear even if only one filter has a value
- **Multiple filters set**: Should clear all filters simultaneously

## Non-Changes

- No backend API modifications
- No persistence of filter state
- No changes to existing search logic or pet data
- No new dependencies

## Risks

- **Low risk**: This is a purely additive UI change with no impact on existing functionality
- **UX consideration**: Button placement and label should be reviewed for user experience
- **Regression potential**: Minimal, as existing search behavior is unchanged
- **Browser compatibility**: Uses standard DOM APIs that work in all modern browsers
