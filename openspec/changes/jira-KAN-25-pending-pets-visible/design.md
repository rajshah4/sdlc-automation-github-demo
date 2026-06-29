# Design

## Context

The Petstore catalog module provides `search_pets()` for filtering pets by various criteria. The product rule requires default searches to return only available pets, with pending pets shown only when explicitly requested.

The current implementation has a subtle bug: when `status=""` is passed, the condition `if normalized_status and normalized_status != pet.status` evaluates to False (empty string is falsy), causing the status filter to be skipped entirely.

## Decision

- Change status normalization to treat empty/whitespace values as "available" (the default)
- Remove the falsy check from the status filter condition
- Keep the status parameter default as "available" for backward compatibility
- Add test coverage for empty status parameter

## Implementation

In `catalog.py`, change:
```python
normalized_status = status.strip().lower()
```
to:
```python
normalized_status = status.strip().lower() or "available"
```

And change:
```python
if normalized_status and normalized_status != pet.status:
```
to:
```python
if normalized_status != pet.status:
```

## Risks

- **Low risk**: Backward compatibility - Default parameter value unchanged; only affects edge case of explicitly passing empty string
- **Low risk**: Operations workflows - Explicit `status="pending"` searches unchanged
- **Mitigation**: Focused test coverage for empty status, existing tests verify other cases

## Validation Plan

```bash
# Run focused catalog tests
python3 -m pytest -xvs app/tests/test_pet_catalog.py

# Run all tests to verify no regressions
python3 -m pytest app/tests/
```
