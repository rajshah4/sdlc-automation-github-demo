# KAN-121: Add Age Range Filtering to Pet Search

## Issue Reference
- **Jira Issue:** KAN-121
- **Summary:** Customers cannot filter pets by age range
- **Priority:** Medium
- **Reporter:** Rajiv Shah

## Problem Statement

Customers currently cannot filter pets by age when searching the catalog. This limits their ability to find pets that match their preferences for younger or older animals. The search function supports filtering by species, status, and tags, but lacks age-based filtering capabilities.

## Current Behavior

The `search_pets()` function in `app/petstore_app/catalog.py` accepts:
- `query`: text search on pet name
- `species`: filter by animal type
- `status`: filter by availability (defaults to "available")
- `tag`: filter by behavioral tags
- `max_results`: limit results

Each pet has an `age_months` attribute (integer representing age in months), but there is no way to filter by this field.

## Proposed Solution

Add optional `min_age_months` and `max_age_months` parameters to the `search_pets()` function to enable age range filtering.

### Design Decisions

1. **Age representation**: Continue using months (consistent with existing `Pet.age_months` field)
2. **Range specification**: Use min/max parameters (both optional, can specify one or both)
3. **Inclusive bounds**: Range should be inclusive on both ends (min <= age <= max)
4. **Validation**: Ensure min_age >= 0 and max_age >= min_age when both provided
5. **Default behavior**: When no age filters provided, return all ages (no change to existing behavior)

### API Changes

```python
def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",
    tag: str | None = None,
    min_age_months: int | None = None,  # NEW
    max_age_months: int | None = None,  # NEW
    max_results: int = 10,
) -> list[Pet]:
```

### Validation Rules

- If `min_age_months` is provided, it must be >= 0
- If `max_age_months` is provided, it must be >= 0
- If both are provided, `max_age_months` must be >= `min_age_months`
- Raise `ValueError` with descriptive message for invalid inputs

### Filter Logic

```python
# After existing filters, before appending to matches:
if min_age_months is not None and pet.age_months < min_age_months:
    continue
if max_age_months is not None and pet.age_months > max_age_months:
    continue
```

## Test Plan

### Unit Tests (app/tests/test_pet_catalog.py)

1. **Test filtering by minimum age only**
   - Search with `min_age_months=15`
   - Should return pets with age >= 15 months (Scout: 28, Mochi: 18)

2. **Test filtering by maximum age only**
   - Search with `max_age_months=15`
   - Should return pets with age <= 15 months (Nova: 14, Pip: 9)

3. **Test filtering by age range**
   - Search with `min_age_months=10, max_age_months=20`
   - Should return pets in range (Nova: 14, Mochi: 18)

4. **Test age filter with other filters**
   - Search with `species="dog", min_age_months=20`
   - Should return only Scout (dog >= 20 months)

5. **Test validation: negative min_age**
   - Search with `min_age_months=-1`
   - Should raise ValueError

6. **Test validation: negative max_age**
   - Search with `max_age_months=-1`
   - Should raise ValueError

7. **Test validation: max < min**
   - Search with `min_age_months=20, max_age_months=10`
   - Should raise ValueError

8. **Test no age filter maintains existing behavior**
   - Search without age parameters
   - Should return all available pets (unchanged)

## Implementation Checklist

- [ ] Add `min_age_months` and `max_age_months` parameters to `search_pets()`
- [ ] Add validation for age parameters
- [ ] Add age filtering logic to search loop
- [ ] Add 8 unit tests covering all scenarios
- [ ] Run existing tests to ensure no regression
- [ ] Update function docstring

## Non-Goals

- This change does NOT add UI components for age filtering (backend only)
- This change does NOT modify the Pet model or data
- This change does NOT add age-based sorting

## Risks & Assumptions

**Assumptions:**
- Age in months is sufficient granularity (vs. years or days)
- Inclusive bounds are intuitive for users
- No need for "unknown age" handling (all pets have valid age_months)

**Risks:**
- Low risk: Pure additive change with optional parameters
- No breaking changes to existing API
- All existing callers continue to work unchanged

## Success Criteria

- All new tests pass
- All existing tests pass (no regression)
- Code follows existing patterns and style
- Age filtering works in isolation and combined with other filters
