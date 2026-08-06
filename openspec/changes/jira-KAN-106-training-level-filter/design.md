# Design

## Context

The Petstore catalog provides a `search_pets()` function in `app/petstore_app/catalog.py` that filters pets by name query, species, status, and tag. The function uses normalized lowercase matching for all filters. The Pet dataclass includes a `tags` field (tuple of strings) that currently holds descriptive tags like "calm", "active", "family", "indoor", etc.

Training levels are conceptually similar to tags but represent a distinct filtering dimension. To avoid adding new fields to the Pet dataclass or modifying the data schema, we will treat training levels as a specialized tag pattern and filter using substring matching on the existing tags.

## Decision

- Add an optional `training_level: str | None = None` parameter to `search_pets()`
- When `training_level` is provided, filter pets where the normalized training_level string appears in any of the pet's tags
- Use the same normalization pattern as other filters (strip and lowercase)
- Preserve existing default behavior when training_level is None
- No changes to the Pet dataclass or PETS data structure
- Update existing pets' tags to include training level indicators: "basic", "intermediate", or "advanced"

## Implementation

1. Add `training_level` parameter to `search_pets()` signature after `tag` parameter
2. Normalize the training_level input (strip and lowercase) when provided
3. Add filter logic in the pet matching loop to check if normalized_training_level is in pet.tags
4. Update PETS fixture data to include training level tags:
   - Mochi: Add "basic" training tag
   - Scout: Add "intermediate" training tag
   - Pip: Add "basic" training tag
   - Nova: Add "advanced" training tag

## Risks

- **Tag namespace collision**: If existing tags accidentally contain "basic", "intermediate", or "advanced", they could be matched unintentionally. Mitigation: The current PETS data does not contain these keywords, and the demo scope is limited to these four pets.
- **Substring matching behavior**: The current tag filter uses `in` for substring matching. This is consistent with existing behavior and acceptable for the demo scope.
- **No validation of training_level values**: The function does not enforce a fixed set of valid training levels. This is consistent with how other string parameters work (species, tag) and allows flexibility.

## Validation Plan

1. Run focused unit tests for training level filtering:
   - Test filter by basic training level
   - Test filter by intermediate training level
   - Test filter by advanced training level
   - Test default behavior (no training_level specified)
   - Test combination with other filters (species, status)
   - Test case-insensitive matching
2. Run existing catalog test suite to ensure no regressions
3. Manual verification that all acceptance criteria are met
