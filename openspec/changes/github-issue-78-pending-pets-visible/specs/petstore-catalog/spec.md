# Petstore Catalog Spec Delta

## FIXED Defect

### Defect: Empty status bypasses availability filter

**Symptom**: Pending pets appear in default available-pets results when status is an empty string.

**Root Cause**: The `search_pets()` function checks `if normalized_status and normalized_status != pet.status:` which skips the status filter when `normalized_status` is an empty string (falsy value).

**Evidence**:
- Error code: `PENDING_PET_VISIBLE` in `docs/logs/pending-pet-visible.ndjson`
- Affected pet: Nova (pet-103) with `status="pending"`
- Source: GitHub issue #78

## ADDED Requirements

### Requirement: Default catalog search excludes unavailable pets

Catalog search MUST exclude pending pets from the default available-pets experience, even when status parameter is empty or blank.

#### Scenario: Default available-pets search excludes pending pets

- Given Nova (pet-103) has status `"pending"`
- When catalog search is called with default options (no status parameter)
- Then Nova is NOT included in the results

#### Scenario: Empty status string defaults to available-only filter

- Given Nova (pet-103) has status `"pending"`
- When catalog search is called with `status=""`
- Then Nova is NOT included in the results
- And only available pets are returned

#### Scenario: Blank status string defaults to available-only filter

- Given Nova (pet-103) has status `"pending"`
- When catalog search is called with `status="  "`
- Then Nova is NOT included in the results
- And only available pets are returned

#### Scenario: Explicit pending-pet search still works

- Given Nova (pet-103) has status `"pending"`
- When catalog search is called with `status="pending"`
- Then Nova IS included in the results

#### Scenario: Available dog search excludes pending dogs

- Given Scout (pet-101) is available and Nova (pet-103) is pending
- When catalog search is called for available dogs (`species="dog"`)
- Then Scout is included and Nova is excluded

## UNCHANGED Requirements

- `max_results` validation (1-50) remains unchanged.
- Species, tag, and query filtering remain unchanged.
- Explicit status override (e.g., `status="pending"`) continues to work.
