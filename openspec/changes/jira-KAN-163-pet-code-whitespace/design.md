# Design

## Context

The Petstore adoption flow uses exact string matching to look up pets by ID. The `create_adoption_order()` function in `app/petstore_app/adoptions.py` calls `_find_pet(pet_id)`, which compares the provided `pet_id` against stored pet IDs using the `==` operator without any whitespace normalization. Meanwhile, the `search_pets()` function in `catalog.py` already normalizes all string inputs with `.strip()` for name, species, status, and tag searches.

## Decision

- Normalize `pet_id` by trimming whitespace at the entry point of `create_adoption_order()` before calling `_find_pet()`.
- Use Python's built-in `str.strip()` method to remove leading and trailing whitespace (spaces, tabs, newlines).
- Keep `_find_pet()` unchanged so it remains a pure lookup function.
- Add three test cases to `app/tests/test_adoptions.py` for leading, trailing, and surrounding whitespace.
- Match the normalization pattern already used in `search_pets()` for consistency.

## Risks

- Low risk: Whitespace trimming is standard expected behavior and unlikely to break existing use cases.
- No one should depend on whitespace being significant in pet IDs.
- All pet IDs in the `PETS` tuple have no whitespace, so trimming will not affect existing data.

## Validation Plan

- Run adoption tests: `pytest app/tests/test_adoptions.py -v`
- Confirm all three new whitespace tests pass.
- Confirm all existing adoption tests continue to pass (backward compatibility).
- If repository guidance requires broader validation, run: `pytest app/tests/ -v`
