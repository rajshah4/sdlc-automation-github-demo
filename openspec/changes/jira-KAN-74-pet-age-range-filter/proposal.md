# Change: Filter Pets by Age Range

## Why

Adopters report that the search page shows too many pets because their age preferences are ignored. They expect searches for puppies, adults, or senior pets to return only matching pets. This addresses Jira ticket KAN-74 and requires only a small catalog filter change.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-74 — Customers cannot filter pets by age range
- GitHub issue: (tracked via Jira KAN-74)
- Story title: Customers cannot filter pets by age range
- Story body: Adopters say the search page is showing too many pets because age preferences are ignored. They expect searches for puppies, adults, or senior pets to return only matching pets.
- Automation: SDLC Automation Demo — Replicated Factory run `replicated-factory-20260708-151829`

## Assumptions

- The age range filters apply to **available** pets by default (product rule: default search returns available pets).
- Age is stored as integer months in the backend (`age_months` field).
- Both `min_age_months` and `max_age_months` are optional parameters.
- Age range is inclusive: a pet whose age equals min or max is included.
- Negative age values are invalid and raise `ValueError`.
- Inverted ranges (min > max) are invalid and raise `ValueError`.
- No UI changes are needed unless explicitly requested; backend filter is sufficient.
- No new packages, persistence, auth, or deployment changes are needed.

## Non-Goals

- UI changes (keeping this backend-only unless requested).
- Age category labels like "puppy", "adult", "senior" (can be added later).
- Filtering by age in other units (years, weeks).
- Persisting user filter preferences.
- New backend services or deployment configuration.

## What Changes

- `app/petstore_app/catalog.py`: `search_pets()` gains optional `min_age_months: int | None` and `max_age_months: int | None` parameters with validation and filter predicates.
- `app/tests/test_pet_catalog.py`: focused tests for the new parameters covering happy paths, boundaries, validation, and edge cases.

## Impact

- **App behavior**: available pets outside the specified age range are excluded from results when the filters are active.
- **Tests**: new backend unit tests; no existing tests change.
- **Humans**: scope approval, code review, merge, and deployment remain human-gated.

## Human Gates

- Scope approval: required before implementation begins.
- Review approval: PR review before merge.
- Merge approval: human merges the PR.
- Deployment approval: human deploys to production.
