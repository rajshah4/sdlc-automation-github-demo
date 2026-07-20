# Design

## Context

The Petstore catalog currently supports filtering by species, status, and tag. Pets have a `tags` field (tuple of strings) that includes behavioral characteristics like "calm", "active", "quiet", and "indoor". Adopters need a way to search for pets by temperament to find matches for their home environment.

## Decision

- Add an optional `temperament` parameter to the `search_pets` function.
- The temperament parameter filters pets by matching against their tags (case-insensitive).
- Follow the existing pattern used for the `tag` parameter implementation.
- When temperament is specified, only pets with that temperament tag are included.
- The temperament filter combines with existing filters (species, status, tag) using AND logic.
- Default status remains "available" to ensure only adoptable pets are shown.

## Implementation Approach

1. Add `temperament: str | None = None` parameter to `search_pets()`.
2. Normalize the temperament parameter (strip and lowercase) if provided.
3. Add a filter condition that checks if the normalized temperament is in the pet's tags.
4. Follow the same pattern as the existing `tag` filter for consistency.

## Edge Cases

- Empty or whitespace temperament values should be treated as None (no filtering).
- Case-insensitive matching ensures "Calm" matches "calm" tag.
- If a pet has no tags, it won't match any temperament filter.
- Temperament filtering does not exclude other filters; all filters work together.

## Risks

- Minimal risk: this is an additive feature that doesn't change existing behavior.
- No database schema changes or data migrations needed.
- No new dependencies or external services.

## Validation Plan

- Add focused tests for temperament matching (pets with specified temperament).
- Add tests for exclusion (pets without specified temperament).
- Add tests for clearing the filter (temperament=None returns all available pets).
- Verify that temperament filter works with other filters (species, status).
- Run the full pytest suite before opening the PR.
