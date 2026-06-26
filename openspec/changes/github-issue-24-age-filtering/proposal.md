# Change: Age-Range Filtering for Pet Search

## Why

Petstore users need to filter pets by age to find companions that match their lifestyle and experience level. Young pets may require more training and energy, while older pets might be calmer and better suited for families with less active lifestyles.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/24
- Trigger label: `openhands-build`
- Automation: `sdlc-story`

## Assumptions

- Age is already captured in the pet catalog as `age_months`.
- Users want to filter by minimum and/or maximum age.
- Age filtering should work alongside existing species, status, and tag filters.
- Default search behavior (available pets only) is preserved.

## Non-Goals

- Changing how age is stored or displayed (stays as months).
- Adding age to the static UI (this is backend-only unless scope changes).
- Calculating age from date of birth.
- Grouping by age categories like "puppy", "adult", "senior".

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets()`.
- Validate that age values are non-negative.
- Validate that `min_age_months <= max_age_months` when both are provided.
- Filter results to include only pets within the specified age range.

## Impact

- App behavior: Users can now search for pets within a specific age range.
- Tests: New test cases for age filtering, boundary conditions, and validation.
- Humans: Reviewers should verify that edge cases (negative values, inverted ranges) are handled correctly.

## Human Gates

- Scope approval: Product owner confirms this matches the intent of issue #24.
- Review approval: Code reviewer verifies implementation quality and test coverage.
- Merge approval: Maintainer approves the PR for merge to main.
- Deployment approval: Operator decides when to deploy to production.
