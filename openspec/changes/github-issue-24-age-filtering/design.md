# Design

## Context

The Petstore catalog search function (`catalog.py::search_pets`) currently supports filtering by:
- Name query (substring match)
- Species (exact match)
- Status (defaults to "available")
- Tag (presence in tags tuple)
- Max results (validated between 1-50)

Pets have an `age_months` field (integer) representing their age in months. The current implementation does not support filtering by age.

## Decision

- Add two optional parameters to `search_pets()`: `min_age_months` and `max_age_months`.
- Both parameters default to `None` (no age filtering).
- When `min_age_months` is provided, filter out pets with `age_months < min_age_months`.
- When `max_age_months` is provided, filter out pets with `age_months > max_age_months`.
- Validate that both values are non-negative when provided.
- Validate that `min_age_months <= max_age_months` when both are provided.
- Apply age filtering in the same loop as other filters to maintain performance.
- Follow the existing pattern: validate early, normalize inputs, filter in a single pass.

## Risks

- **Inverted range confusion**: Users might accidentally swap min/max. Mitigation: Raise clear error message.
- **Zero age edge case**: Zero is valid (newborn pets). Validation allows zero but rejects negative.
- **None vs zero**: Must distinguish between "no filter" (None) and "zero months" (0). Implementation uses `is not None` checks.
- **Breaking change**: Adding optional parameters maintains backward compatibility.

## Validation Plan

Run focused tests:
```bash
python3 -m pytest -xvs app/tests/test_pet_catalog.py::test_search_pets_filters_by_min_age
python3 -m pytest -xvs app/tests/test_pet_catalog.py::test_search_pets_filters_by_max_age
python3 -m pytest -xvs app/tests/test_pet_catalog.py::test_search_pets_filters_by_age_range
python3 -m pytest -xvs app/tests/test_pet_catalog.py::test_search_pets_rejects_negative_age
python3 -m pytest -xvs app/tests/test_pet_catalog.py::test_search_pets_rejects_inverted_age_range
```

Run full catalog test suite:
```bash
python3 -m pytest -q app/tests/test_pet_catalog.py
```
