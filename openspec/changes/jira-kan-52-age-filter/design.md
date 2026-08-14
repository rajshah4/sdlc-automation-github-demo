# Design

## Context

The Petstore catalog search (`app/petstore_app/catalog.py`) currently supports filtering by:
- Pet name (query string)
- Species
- Status (default: "available")
- Tags

Pets already have an `age_months` field in the `Pet` dataclass. The current implementation filters pets sequentially through a series of `if` checks and continues to the next pet when a filter doesn't match.

Per `AGENTS.md` and demo product rules:
- Default pet search returns only available pets
- Money is represented as integer cents
- The catalog uses immutable dataclasses

## Decision

- Add two optional keyword-only parameters to `search_pets()`: `min_age_months` and `max_age_months`
- Type both as `int | None` with default `None`
- Validate age parameters before filtering:
  - Both must be non-negative if provided
  - If both are provided, `min_age_months` must be <= `max_age_months`
  - Raise `ValueError` with descriptive message on validation failure
- Add age range check to the existing sequential filter loop
- No changes to the Pet dataclass or catalog data
- No UI changes in this iteration

## Risks

- **Risk**: Age validation logic could reject valid edge cases
  - **Mitigation**: Use clear validation rules (non-negative, min <= max) with focused tests for boundaries (0, equal min/max)

- **Risk**: Adding parameters could break existing callers
  - **Mitigation**: Parameters are optional with default `None`; existing calls continue to work unchanged

- **Risk**: Performance impact on large catalogs
  - **Mitigation**: Current catalog is small (4 pets); age check is a simple integer comparison; no indexing needed for demo

## Validation Plan

- Run existing tests to ensure no regression: `pytest app/tests/test_pet_catalog.py -v`
- Run new age filter tests: `pytest app/tests/test_pet_catalog.py::test_search_pets_filters_by_min_age -v`
- Validate OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-kan-52-age-filter`
