# Design

## Context

The Petstore adoption flow validates pet codes in the `_find_pet()` function located in `app/petstore_app/adoptions.py` (lines 19-23). Currently, this function performs an exact string match: `if pet.id == pet_id`. Support agents sometimes copy pet codes with accidental leading or trailing whitespace from messages, causing valid pet codes to fail validation.

The catalog search function in `app/petstore_app/catalog.py` (lines 39-42) already normalizes search inputs by calling `.strip()` on query parameters. This inconsistency between catalog and adoption behavior is the root cause of the issue.

All valid pet codes follow the format `pet-XXX` (7 characters, lowercase alphanumeric with hyphen, no internal whitespace):
- `pet-100` (Mochi, cat, available)
- `pet-101` (Scout, dog, available)
- `pet-102` (Pip, rabbit, available)
- `pet-103` (Nova, dog, pending)

## Decision

- Add `.strip()` normalization to the `pet_id` parameter in the `_find_pet()` function at line 21.
- Normalize at the validation point rather than at the entry point to centralize the normalization logic and protect against whitespace regardless of caller.
- Use Python's built-in `.strip()` method, which removes only leading and trailing whitespace (spaces, tabs, newlines) but preserves internal characters.
- This brings adoption behavior into alignment with the existing catalog search normalization pattern.

## Risks

**Low Risk:**
- `.strip()` is idempotent on clean strings: existing valid inputs remain valid.
- All 4 existing tests pass unchanged because they use clean inputs (`"pet-100"`, `"pet-103"`).
- No valid pet codes contain meaningful leading/trailing whitespace.
- `.strip()` preserves internal characters, so invalid pet codes with internal spaces (like `"pet 100"`) correctly remain invalid.
- Pending pet availability checks happen after pet lookup (line 34), so this change does not weaken availability controls.
- No security risk: pet codes are matched against a fixed in-memory tuple (`PETS`), not database queries or external calls.

**Mitigation:**
- Add focused regression tests for whitespace scenarios to document intended behavior and prevent future regressions.
- Verify that pending pet rejection still works correctly with normalized input.

## Validation Plan

1. Run existing adoption tests to confirm no regressions: `python3 -m pytest app/tests/test_adoptions.py -v`
2. Add and run new tests for whitespace handling:
   - Test `" pet-100"` (leading space)
   - Test `"pet-100 "` (trailing space)
   - Test `" pet-100 "` (both)
   - Test `" pet-103 "` (pending pet with whitespace, should still be rejected)
3. Verify that the catalog search and adoption validation now handle whitespace consistently.
