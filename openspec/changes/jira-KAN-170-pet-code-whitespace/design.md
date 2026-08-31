# Design

## Context

The Petstore adoption flow validates pet codes with exact string matching, while the catalog search flow already normalizes inputs by stripping whitespace. This inconsistency causes support agents' copy-paste workflows to fail when accidental spaces are included.

From the code-explorer investigation:
- `catalog.py` `search_pets()` normalizes all inputs with `.strip()` (lines 39-42)
- `adoptions.py` `_find_pet()` uses exact string match without normalization (line 21)
- `adoptions.py` `create_adoption_order()` passes pet_id directly to lookup without sanitization (line 33)
- Pet codes are public identifiers stored as clean strings in a hardcoded tuple
- No existing tests cover whitespace handling in pet codes

## Decision

- Add `pet_id = pet_id.strip()` at the start of `create_adoption_order()`, immediately after receiving the parameter
- This aligns adoption behavior with catalog search normalization
- Placement before `_find_pet()` ensures all downstream validation uses the normalized value
- The final `AdoptionOrder` already uses `pet.id` (canonical) not the input, so output remains clean

## Risks

**Security risk: LOW**
- Pet codes are not credentials or access tokens
- No injection risk (matching against fixed tuple, no database queries)
- No authentication or authorization tied to exact format
- Trimming reduces false negatives without introducing false positives

**Breaking change risk: NONE**
- Valid inputs (already trimmed) continue to work identically
- Invalid inputs remain invalid after normalization
- Availability checks remain unchanged

**Behavior change risk: LOW**
- Change only affects inputs that currently fail lookup
- All existing validations (status, email, donation) remain in place
- Consistent with existing catalog behavior

## Validation Plan

- Add three new test cases for whitespace scenarios (leading, trailing, both)
- Add test for invalid pet code to prove validation still works after normalization
- Run existing adoption tests to prove no regression
- Run full pytest suite to confirm no cross-module impact
