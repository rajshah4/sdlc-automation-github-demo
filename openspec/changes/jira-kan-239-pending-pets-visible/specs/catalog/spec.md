# Catalog Search Status Filter Spec Delta

## MODIFIED Requirements

### Requirement: Empty status parameter defaults to "available"

When the `search_pets` function is called with an empty status string, it must default to filtering by `status="available"` instead of bypassing the status filter entirely.

#### Scenario: Empty status string defaults to available pets

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- And the catalog contains other pets with status="available"
- When `search_pets(status="")` is called
- Then the results must include only pets with status="available"
- And Nova must not appear in the results

#### Scenario: Whitespace-only status defaults to available pets

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- When `search_pets(status="   ")` is called (whitespace-only string)
- Then the results must include only pets with status="available"
- And Nova must not appear in the results

#### Scenario: Default parameter continues to work

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- When `search_pets()` is called without a status parameter
- Then the results must include only pets with status="available"
- And Nova must not appear in the results

#### Scenario: Explicit status values continue to work

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- When `search_pets(status="pending")` is called
- Then the results must include only pets with status="pending"
- And Nova appears in the results

## Implementation

### Change in `app/petstore_app/catalog.py`

Line 41 modification:

```python
# Before:
normalized_status = status.strip().lower()

# After:
normalized_status = status.strip().lower() or "available"
```

### New Test in `app/tests/test_pet_catalog.py`

```python
def test_search_pets_defaults_empty_status_to_available() -> None:
    """Empty status string should default to 'available', not bypass the filter."""
    results = search_pets(status="")
    
    # Should only return available pets, not pending ones
    assert all(pet.status == "available" for pet in results)
    assert "pet-103" not in [pet.id for pet in results]  # Nova (pending) excluded
```

## Acceptance Criteria

- [ ] `search_pets(status="")` returns only available pets
- [ ] `search_pets(status="   ")` returns only available pets
- [ ] `search_pets()` continues to work (default parameter)
- [ ] `search_pets(status="pending")` continues to work (explicit override)
- [ ] New test `test_search_pets_defaults_empty_status_to_available()` passes
- [ ] All existing tests in `test_pet_catalog.py` pass
- [ ] Nova (pet-103) is excluded from empty-status searches
