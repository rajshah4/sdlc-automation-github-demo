# Design

## Context

The Petstore application has an incident simulation mode that was originally designed to test observability and error handling. The `visible_pets()` function in `cloud_run_app.py` currently has this logic:

```python
def visible_pets() -> list[Pet]:
    if current_mode() == INCIDENT_MODE:
        return list(PETS)  # Returns ALL pets including pending ones
    return [pet for pet in PETS if pet.status == "available"]
```

This implementation was intended to simulate a catalog regression, but it creates actual customer-facing bugs by exposing pending pets in production when incident mode is accidentally enabled or used for testing.

The adoption validation already correctly rejects attempts to adopt pending pets (see `adoptions.py`), but customers still see them in the catalog and can start the flow, leading to confusion.

## Decision

- Change `visible_pets()` to always filter to "available" status only, regardless of mode
- Keep incident mode for observability purposes:
  - Health check failures (500 status)
  - Error logging with incident markers
  - UI banners indicating degraded state
- This makes incident mode safe for testing observability without affecting business logic
- The fix is a single-line change in `visible_pets()` function

## Alternative Considered

We considered adding a separate configuration flag specifically for "catalog regression simulation," but this adds complexity without clear benefit. Incident mode can still test observability without actually breaking the catalog filter.

## Risks

- **Low risk**: The change is isolated to one function
- **Testing**: Existing tests cover catalog filtering; we'll add a regression test for incident mode
- **Observability**: Incident mode will still produce logs, health check failures, and UI warnings
- **Backwards compatibility**: No API or data model changes

## Validation Plan

1. Run existing unit tests: `pytest app/tests/test_pet_catalog.py -v`
2. Run full test suite: `pytest app/tests/ -v`
3. Add regression test for incident mode catalog filtering
4. Manual verification: Start app in incident mode and verify only available pets are returned
