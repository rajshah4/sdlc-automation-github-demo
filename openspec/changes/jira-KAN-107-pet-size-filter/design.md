# Design

## Context

The Petstore catalog currently supports filtering by species, status, tag, and text query. The `search_pets()` function in `app/petstore_app/catalog.py` accepts optional filter parameters and returns matching pets from an in-memory tuple.

The Pet dataclass defines the structure of each pet. To support size filtering, we need to:
1. Add a size field to the Pet dataclass
2. Assign size values to existing pet fixtures
3. Add size parameter to search_pets()
4. Implement size filtering logic
5. Expose the filter in the web UI

## Decision

- Add `size: str` field to the Pet dataclass after `species`
- Use three size categories: "small", "medium", "large"
- Categorize existing pets:
  - Mochi (cat): small
  - Scout (dog): medium
  - Pip (rabbit): small
  - Nova (dog): medium
- Add optional `size: str | None = None` parameter to `search_pets()`
- Implement case-insensitive matching similar to existing filters
- Add size dropdown to web UI with options: Any, small, medium, large
- Update JavaScript to include size in search requests

## Risks

- **Risk**: Size categorization may not match real-world expectations for specific breeds
  - **Mitigation**: Use sensible defaults; size is descriptive, not restrictive
  
- **Risk**: Adding a new field could break existing code that creates Pet instances
  - **Mitigation**: All Pet instances in catalog.py are updated together; tests will catch any issues

- **Risk**: UI change could affect existing Playwright tests
  - **Mitigation**: Run smoke tests after UI changes

## Validation Plan

- Run focused backend tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run all tests: `python3 -m pytest -q`
- Smoke test UI: Serve the static app and verify size filter appears and functions
