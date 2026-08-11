# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

The default customer-facing catalog search must filter pets by `status="available"` and must not show pets with `status="pending"` or any other non-available status. This applies to both backend API and frontend UI.

#### Scenario: Default search excludes pending pets

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- And the catalog contains other pets with status="available"
- When a customer views the default pet list in the web UI
- Then the display must include only pets with status="available"
- And Nova must not appear in the results

#### Scenario: Species filter with default status excludes pending pets

- Given the Petstore catalog contains Scout (pet-101, dog, available) and Nova (pet-103, dog, pending)
- When a customer filters by species="dog" without specifying status
- Then the results must include only Scout
- And Nova must not appear in the results

#### Scenario: Name search with default status excludes pending pets

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- When a customer searches for name="Nova"
- Then the results must be empty (no pets match both name="Nova" AND status="available")
- And a message "No available pets match this search" should be displayed

#### Scenario: Explicit pending search returns pending pets when requested (backend API only)

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- When a support user explicitly calls the backend API with status="pending" and species="dog"
- Then the results must include Nova
- And this is the only valid way for pending pets to appear in search results

## VERIFIED Existing Behavior

### Backend Implementation (`app/petstore_app/catalog.py`)
- Line 31: `search_pets()` has default parameter `status: str = "available"` ✓ CORRECT
- Lines 40-51: Filter logic correctly excludes pets where status doesn't match ✓ CORRECT

### Frontend Implementation (`app/web/app.js`)
- Lines 1-6: `pets` array includes Nova (pet-103) with status="pending"
- Line 17: Filter logic includes `&& pet.status === "available"` ✓ CORRECT IN CODE
- Line 37: `renderResults()` called on page load to apply filter

### Test Coverage (`app/tests/test_pet_catalog.py`)
- `test_search_pets_filters_by_species_and_status()`: Verifies species="dog" search returns only Scout (pet-101), excluding Nova
- `test_search_pets_can_find_pending_pets_when_requested()`: Verifies explicit status="pending" search returns Nova

## Root Cause Assessment

Log evidence (`docs/logs/pending-pet-visible.ndjson`) indicates `PENDING_PET_VISIBLE` error occurred on 2026-06-29, showing pet-103 (Nova) was visible in the available-pets experience. 

Current code inspection shows filtering logic IS present (line 17 of app.js). Possible causes:
1. Logic error in filter condition (double-check operator precedence)
2. Race condition or timing issue on page load
3. Past regression that was fixed but log remains as evidence
4. Missing defensive validation to ensure pending pets never enter display pipeline

## FIX Strategy

**Defensive programming approach:** Add explicit validation to strengthen the guarantee that only available pets are displayed, even if earlier filter is compromised.

Changes:
1. Add explicit comment in `app.js` documenting the availability requirement
2. Strengthen the filter logic (verify operator precedence, consider extracting to named function)
3. Add frontend-focused test or validation step to PR checklist

## Acceptance Criteria

- [ ] Backend default search excludes pending pets (already satisfied)
- [ ] Frontend default display excludes pending pets (strengthen validation)
- [ ] Explicit pending searches work when status="pending" is specified (already satisfied)
- [ ] Nova (pet-103) is excluded from default display (verify manually)
- [ ] Regression tests or validation confirms the behavior
- [ ] Log evidence waypoint documented in PR
