# Change: Filter Available Pets by Maximum Age

## Why

Adopters want to find pets that fit their household, and age is an important factor. This change adds an optional maximum age filter to the pet catalog search, helping adopters narrow results to pets that match their preferences.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-112
- Trigger: Replicated Jira-delegated factory
- Automation: Replicated factory run ID `replicated-factory-20260715-165740`

## Assumptions

- Maximum age filter is optional and does not affect default search behavior.
- Age is measured in months (existing `age_months` field).
- Negative age values are rejected as invalid input.
- Default status filtering (`status="available"`) is preserved.
- No UI changes are required for this backend feature.

## Non-Goals

- Minimum age filter (not requested).
- UI form updates (backend-only change).
- Age-based sorting or prioritization.
- Changes to pet data structure or persistence.
- Deployment or infrastructure changes.

## What Changes

- `catalog.py`: Add optional `max_age_months` parameter to `search_pets()` function.
- `catalog.py`: Validate that `max_age_months`, if provided, is non-negative.
- `catalog.py`: Filter out pets older than `max_age_months` when the parameter is provided.
- `test_pet_catalog.py`: Add tests for matching pets, excluded pets, and negative age validation.

## Impact

- App behavior: Adopters can optionally filter pets by maximum age. Default catalog behavior is unchanged.
- Tests: New tests added to cover age filtering scenarios.
- Humans: PR requires review and merge approval before deployment.

## Human Gates

- Scope approval: Jira ticket provides acceptance criteria.
- Review approval: Humans review the PR and approve merge.
- Merge approval: Humans merge the PR after validation.
- Deployment approval: Humans control deployment timing.
