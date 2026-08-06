# Design: Show Available Pet Count

## Context

The Petstore catalog displays available pets but does not show users how many pets match their current search. Users need immediate feedback to understand the scope of results at a glance.

The existing `search_pets` function filters by query, species, status, and tag. The count feature should use the same filtering logic to ensure consistency between count and results.

## Decision

- Add a `count_available` function to `app/petstore_app/catalog.py` that mirrors `search_pets` filtering logic
- Return an integer count instead of a list of pets
- Update UI to display count near the "Available Pets" heading
- Calculate count from filtered results in `app.js` using existing filter logic
- Ensure pending pets are excluded from the count (status="available" default)

Alternative considered: Adding a count return value to `search_pets` was rejected to keep the function focused and avoid breaking existing callers.

## Risks

- **Risk**: Count and search results could diverge if filtering logic differs
  - **Mitigation**: Use identical filtering logic in both functions
  
- **Risk**: UI could show stale counts
  - **Mitigation**: Update count in same render function that updates results

## Validation Plan

- Run focused catalog tests for count with various filter combinations
- Verify pending pets are excluded from count
- Test count updates when filters change in UI
- Run full pytest suite before opening PR
