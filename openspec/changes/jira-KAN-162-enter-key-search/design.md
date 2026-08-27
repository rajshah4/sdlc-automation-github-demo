# Design

## Context

The Petstore static UI (`app/web/`) provides a search interface with:
- Pet name input field (`#query`)
- Species dropdown (`#species`)
- "Find Pets" button (`#search-button`)
- Results display (`#results`)

The search logic in `app/web/app.js` filters pets by name match, species match, and availability status. Currently, only the button click triggers `renderResults()`. Keyboard users must tab to the button and press Space or Enter, or use the mouse.

## Decision

- Add a `keydown` event listener to the pet name input that calls `renderResults()` when Enter (key code 13 or key "Enter") is pressed
- Add a `keydown` event listener to the species dropdown that calls `renderResults()` when Enter is pressed
- Reuse the existing `renderResults()` function without modification
- Do not add form submission handling (no `<form>` tag, no preventDefault needed unless browser shows unexpected behavior)

## Risks

- Risk: Browser default Enter behavior on `<input type="search">` might trigger unwanted actions
  - Mitigation: Test in Playwright and add `event.preventDefault()` if needed
- Risk: Multiple rapid Enter presses could trigger redundant renders
  - Mitigation: Accept this as low impact; `renderResults()` is fast and idempotent
- Risk: Users might expect Enter in the search field to clear results or perform other actions
  - Mitigation: Standard web behavior is that Enter triggers search/filter; matches user expectation

## Validation Plan

- Add Playwright test scenario: fill pet name input, press Enter, assert results match expected pets
- Add Playwright test scenario: select species, press Enter in dropdown, assert filtered results
- Run existing Playwright test suite to ensure no regressions
- Capture screenshot and video evidence showing Enter key search working
