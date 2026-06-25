# Design

## Context

The Petstore catalog already stores adoption fees as integer cents in the `Pet.adoption_fee_cents` field. The `search_pets()` function filters by query, species, status, and tag. Default behavior returns only available pets unless status is explicitly specified.

## Decision

- Add `max_fee_cents: int | None = None` parameter to `search_pets()` function
- When `max_fee_cents` is provided and not None, filter pets where `pet.adoption_fee_cents <= max_fee_cents`
- Validate that `max_fee_cents >= 0` when provided, raising ValueError for negative values
- Apply fee filter after other filters in the existing loop to preserve existing behavior
- Keep the parameter optional to maintain backward compatibility with existing callers

## Risks

- **Risk**: Breaking existing callers if parameter position changes
  - **Mitigation**: Use keyword-only parameter to prevent positional breakage
  
- **Risk**: Performance with large catalogs if filtering is inefficient
  - **Mitigation**: Current catalog is small (4 pets); filtering in memory is sufficient for demo scope

- **Risk**: Zero as max_fee_cents might be ambiguous (exclude all vs. not set)
  - **Mitigation**: Accept zero as valid (matches pets with free adoption); use None to indicate "no filter"

## Validation Plan

- Run focused catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run full test suite: `python3 -m pytest -q`
- Validate OpenSpec structure: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/github-issue-18-max-adoption-fee-filter`
