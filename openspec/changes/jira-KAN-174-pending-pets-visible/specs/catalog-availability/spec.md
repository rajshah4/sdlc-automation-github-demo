# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search returns only available pets

The default pet catalog search must exclude pets with `status="pending"` and return only pets with `status="available"`.

#### Scenario: Default search excludes pending pets

- **Given** a catalog containing both available pets (Mochi, Scout, Pip) and pending pets (Nova/pet-103)
- **When** a user searches with no explicit status parameter (using the default)
- **Then** only available pets are returned
- **And** pending pets are excluded from results

#### Scenario: Searching for pending pets explicitly

- **Given** a catalog containing pending pets (Nova/pet-103)
- **When** support or operations explicitly requests `status="pending"` pets
- **Then** pending pets are returned
- **And** this workflow continues to work for authorized users

#### Scenario: Nova never appears in default searches

- **Given** Nova (pet-103) has `status="pending"`
- **When** a user performs any default search (name, species, tag)
- **Then** Nova does not appear in results
- **And** an empty state is shown if no other pets match

## VERIFIED Implementation

### Backend: `app/petstore_app/catalog.py`

- **Line 31**: `status: str = "available"` - default parameter correctly set
- **Lines 50-51**: Filter logic correctly excludes pets that don't match the normalized status

### Frontend: `app/web/app.js`

- **Line 17**: `pet.status === "available"` - hardcoded filter correctly excludes pending pets
- The frontend filter is defensive and ensures UI correctness regardless of API behavior

## Test Coverage Requirements

### EXISTING Tests (Verified)

1. `test_search_pets_filters_by_species_and_status()` - Verifies dog search returns only Scout, not Nova
2. `test_search_pets_can_find_pending_pets_when_requested()` - Verifies explicit pending searches work
3. `test_search_pets_filters_by_tag()` - Verifies tag filtering respects default status
4. Playwright UI tests - Verify searching for "nova" shows empty state

### ADDED Test

- `test_default_search_excludes_pending_pets()` - Explicitly verifies pending pets never appear in default results, making the requirement more visible
