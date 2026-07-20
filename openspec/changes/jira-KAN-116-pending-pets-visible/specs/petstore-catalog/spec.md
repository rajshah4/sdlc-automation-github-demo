# Spec: Petstore Catalog Availability Filter

## ADDED Requirements

### Requirement: R1 - Empty status filter defaults to available

When `search_pets()` is called with an empty status string, it behaves the same as the default and returns only available pets.

**Acceptance Criteria:**
- Calling `search_pets(status="")` with empty status returns only available pets.
- Empty status after stripping whitespace is normalized to "available".

#### Scenario: S1.1 - Customer searches with empty status string

**Given** the catalog contains pets with mixed statuses:
- Mochi (`pet-100`, status="available")
- Scout (`pet-101`, status="available")
- Pip (`pet-102`, status="available")
- Nova (`pet-103`, status="pending")

**When** a search is performed with an empty status string:
```python
results = search_pets(status="")
```

**Then** the results include only available pets: Mochi, Scout, Pip  
**And** the results exclude pending pets: Nova

## MODIFIED Requirements

### Requirement: R2 - Default search excludes pending pets (strengthened)

When `search_pets()` is called without a status parameter, only pets with `status="available"` are returned. This now also applies when empty status is provided.

**Acceptance Criteria:**
- Calling `search_pets()` with no status parameter returns only available pets.
- Calling `search_pets(status="available")` explicitly returns only available pets.
- Nova (`pet-103`) with `status="pending"` is excluded from default searches.

#### Scenario: S2.1 - Customer browses available pets (default)

**Given** the catalog contains:
- Mochi (`pet-100`, status="available")
- Scout (`pet-101`, status="available")
- Pip (`pet-102`, status="available")
- Nova (`pet-103`, status="pending")

**When** a customer searches without specifying status:
```python
results = search_pets()
```

**Then** the results include only available pets: Mochi, Scout, Pip  
**And** the results exclude pending pets: Nova

#### Scenario: S2.2 - Species filter with default status

**Given** the catalog contains dogs with mixed statuses

**When** a customer searches for dogs without specifying status:
```python
results = search_pets(species="dog")
```

**Then** the results include only available dogs (Scout)  
**And** pending dogs (Nova) are excluded

### Requirement: R3 - Explicit pending search works (unchanged)

When `search_pets()` is called with `status="pending"`, only pending pets are returned.

**Acceptance Criteria:**
- Calling `search_pets(status="pending")` returns only pending pets.
- Nova (`pet-103`) is included when explicitly requesting pending pets.

#### Scenario: S3.1 - Support searches for pending pets

**Given** the catalog contains pets with mixed statuses

**When** support explicitly searches for pending pets:
```python
results = search_pets(status="pending")
```

**Then** the results include only pending pets  
**And** available pets are excluded

## Delta Summary

**Before:** Empty status string bypassed the status filter, showing all pets including pending ones.

**After:** Empty status string is normalized to "available", ensuring only available pets are shown by default.

## Test Coverage

- `test_search_pets_default_excludes_pending` - verify default search excludes pending
- `test_search_pets_empty_status_excludes_pending` - NEW: verify empty status excludes pending
- `test_search_pets_can_find_pending_pets_when_requested` - verify explicit pending search works
- `test_search_pets_filters_by_species_and_status` - verify species + default status excludes pending
