# Design

## Context

The Petstore catalog search function (`catalog.py::search_pets()`) already supports multiple optional filters including species, status, tag, and max adoption fee. The Pet dataclass already contains an `age_months` field (integer) for every pet in the catalog.

The current implementation pattern:
- Parameters default to `None` to indicate "no filter"
- Validation happens early and raises `ValueError` for invalid inputs
- Filtering happens sequentially in a for-loop over `PETS`
- Each filter condition uses `continue` to skip non-matching pets

## Decision

- Add two optional keyword parameters to `search_pets()`: `min_age_months: int | None = None` and `max_age_months: int | None = None`
- Validate age parameters before filtering: reject negative ages and inverted ranges
- Add age range filtering after existing filters, before the max_results slice
- Follow the existing pattern of `continue` for excluded pets
- Use inclusive boundaries for both min and max (consistent with existing max_fee_cents boundary behavior)

## Risks

### Risk: Inverted range logic error

If we forget to validate `min > max`, users could pass inverted ranges that match nothing.

**Mitigation:** Add explicit validation that raises `ValueError` when both are provided and `min_age_months > max_age_months`.

### Risk: Boundary inclusion inconsistency

If boundaries are not inclusive on both sides, we might exclude pets at exact age thresholds.

**Mitigation:** Use `>=` for min and `<=` for max, consistent with the existing `max_fee_cents` boundary behavior (tested in `test_search_pets_includes_pets_at_exact_fee_boundary`).

### Risk: Breaking existing callers

Adding required parameters would break backward compatibility.

**Mitigation:** Both parameters default to `None` and are keyword-only, so existing calls continue to work unchanged.

## Validation Plan

- Run focused unit tests for age filtering scenarios: min only, max only, range, no filter
- Test boundary conditions: exact age matches, pets just outside boundaries
- Test validation: negative ages, inverted ranges
- Run full test suite to confirm no regression: `pytest app/tests/test_pet_catalog.py -v`
