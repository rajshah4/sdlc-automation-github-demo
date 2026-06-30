# Design

## Context

The `cloud_run_app.py::visible_pets()` function (lines 92-95) implements its own pet filtering logic instead of delegating to the centralized `catalog.py::search_pets()` function:

```python
def visible_pets() -> list[Pet]:
    if current_mode() == INCIDENT_MODE:
        return list(PETS)
    return [pet for pet in PETS if pet.status == "available"]  # Manual filter
```

This creates two problems:
1. **Duplication**: The filtering logic exists in two places
2. **Inconsistency risk**: Future changes to catalog behavior might miss this location

The backend `catalog.py::search_pets()` already implements the correct default behavior (`status="available"` default parameter).

## Decision

Replace manual filtering with delegation to the catalog module:

```python
from .catalog import search_pets

def visible_pets() -> list[Pet]:
    if current_mode() == INCIDENT_MODE:
        return list(PETS)  # Incident mode still returns all pets for demo
    return search_pets()  # Use centralized catalog function
```

Add regression test to `app/tests/test_pet_catalog.py`:

```python
def test_search_pets_default_excludes_pending() -> None:
    """Default search returns only available pets, excluding pending ones like Nova."""
    results = search_pets()
    
    assert len(results) == 3  # Mochi, Scout, Pip (available)
    assert all(pet.status == "available" for pet in results)
    assert "Nova" not in [pet.name for pet in results]  # Nova is pending
```

## Risks

- **INCIDENT_MODE behavior**: The incident mode still intentionally exposes all pets (including pending) for demo purposes. This is preserved by the fix.
- **Test coverage**: The new regression test covers the default case, but comprehensive testing of all catalog filters is beyond this scope.
- **Static UI**: The UI already filters correctly, so no UI changes are needed.

## Validation Plan

1. Run catalog tests: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Run all app tests: `python3 -m pytest app/tests/ -q`
3. Validate OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-35-pending-pets-visible/`

