# Change: Add temperament filter to pet catalog

## Why

Adopters need to filter pets by temperament so they can find pets that fit their home environment. This helps match pets to appropriate homes based on behavioral characteristics.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-118
- Issue key: `KAN-118`
- Automation: `sdlc-story` (delegated from replicated-factory)
- Run id: `replicated-factory-20260720-221040`

## Assumptions

- Temperament information is already captured in the `tags` field of Pet objects (e.g., "calm", "active", "quiet").
- The temperament filter is optional and should not affect existing search behavior when not specified.
- Only available pets should be returned by default when using temperament filter.
- The filter should match pets that have the specified temperament tag.

## Non-Goals

- Adding new temperament values to existing pet data.
- UI implementation (backend API change only).
- Changing how tags are stored or managed.
- Adding persistence, auth, or deployment changes.

## What Changes

- Add optional `temperament` parameter to the `search_pets` function in `catalog.py`.
- Filter pets by matching temperament against the pet's tags.
- Maintain default available-only behavior for filtered results.
- Add focused tests covering temperament matching, exclusion, and filter clearing.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-118 requests temperament filtering with specific acceptance criteria.
- `Stop 2 - Wiki/Docs`: No specific wiki docs for temperament; using existing catalog patterns.
- `Stop 3 - Logs`: No log evidence needed; this is a feature addition, not a bug fix.
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` and `app/tests/test_pet_catalog.py`.
- `Stop 5 - Tests/PR`: Focused tests for matching, exclusion, and clearing filter; draft PR for human review.

## Impact

- App behavior: adopters can filter pets by temperament to find compatible pets.
- Tests: catalog tests cover temperament filtering scenarios.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
