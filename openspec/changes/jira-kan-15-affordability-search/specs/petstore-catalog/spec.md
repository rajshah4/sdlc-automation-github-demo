# Petstore Catalog Spec Delta

## Capability

**Petstore Catalog Search** - `app/petstore_app/catalog.py`

## ADDED Requirements

### Requirement: Search by maximum adoption fee

Catalog search MUST accept an optional maximum adoption fee expressed in integer cents.

#### Scenario: Matching pets at or below the maximum fee

- **Given** available pets with adoption fees (Mochi: 7500¢, Scout: 12500¢, Pip: 4500¢)
- **When** a maximum adoption fee of 7500¢ is supplied
- **Then** pets at or below that fee are included (Mochi, Pip)
- **And** pets above that fee are excluded (Scout)

**Test**: `test_search_pets_filters_by_max_adoption_fee` verifies:
```python
results = search_pets(max_adoption_fee_cents=7500)
assert [pet.name for pet in results] == ["Mochi", "Pip"]
```

#### Scenario: Excluding pets above the maximum fee

- **Given** a search for pets with a family-friendly tag
- **And** Scout has family tag and 12500¢ adoption fee
- **When** a maximum adoption fee of 10000¢ is supplied with tag filter
- **Then** Scout is excluded (fee exceeds maximum)

**Test**: `test_search_pets_combines_fee_cap_with_existing_filters` verifies:
```python
results = search_pets(tag="family", max_adoption_fee_cents=10000)
assert results == []  # Scout excluded by fee, no other family-tagged pets under limit
```

#### Scenario: Rejecting negative maximum fees

- **Given** a negative maximum adoption fee (-1)
- **When** catalog search is called
- **Then** the search is rejected with a ValueError
- **And** the error message mentions "max_adoption_fee_cents"

**Test**: `test_search_pets_rejects_negative_max_adoption_fee` verifies:
```python
with pytest.raises(ValueError, match="max_adoption_fee_cents"):
    search_pets(max_adoption_fee_cents=-1)
```

### Requirement: Preserve default search behavior

When the maximum adoption fee parameter is omitted, search behavior MUST be unchanged.

#### Scenario: Default available-pet search

- **Given** no maximum adoption fee is specified
- **When** search_pets() is called with default parameters
- **Then** all available pets are returned (Mochi, Scout, Pip)
- **And** pending pets are excluded (Nova)

**Coverage**: Existing tests continue to pass without modification.

## UNCHANGED Requirements

- Default status filter remains `"available"`
- Pending pets require explicit `status="pending"` parameter
- Money continues to be represented as integer cents
- Existing filters (query, species, status, tag, max_results) work unchanged
- Validation rules for max_results (1-50) remain enforced

## Acceptance Criteria

✅ A family searching with max_adoption_fee_cents=7500 receives only Mochi ($75) and Pip ($45), not Scout ($125)  
✅ The fee filter combines correctly with existing species/status/tag filters  
✅ Negative fee values are rejected with a clear error message  
✅ Omitting the fee parameter preserves existing search behavior  
✅ All existing catalog tests continue to pass  
✅ Log scenario from `docs/logs/pet-search-budget-limit.ndjson` is satisfied
