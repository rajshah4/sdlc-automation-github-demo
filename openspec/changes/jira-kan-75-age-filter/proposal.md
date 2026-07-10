# Change: Filter Pets by Age Category

## Why

Adopters need a way to search for pets by age category (puppies, adults, or
senior pets) so they can find pets that match their lifestyle and experience
level. This addresses Jira issue KAN-75 where customers reported that age
preferences are being ignored in search results.

## Source

- GitHub issue: https://rajiv-shah.atlassian.net/browse/KAN-75 (tracked in Jira) — Customers say filters aren't working
- Story: Adopters say the search page is showing too many pets because age preferences are ignored. They expect searches for puppies, adults, or senior pets to return only matching pets.
- Automation: SDLC Automation Demo — Replicated Jira delegated factory run `replicated-factory-20260710-134914`

## Assumptions

- Age categories map to `age_months` ranges:
  - Puppy/kitten: 0-12 months
  - Adult: 13-84 months (13 months to 7 years)
  - Senior: 85+ months (7+ years)
- The age filter is optional; when not specified, pets of all ages are returned.
- The age filter applies to **available** pets only (product rule: default search returns available pets).
- The backend filter parameter is `min_age_months` and `max_age_months` (both optional).
- The UI offers predefined age category buttons or labels for common searches.
- Invalid age ranges (min > max, negative values) raise `ValueError`.
- No new packages, persistence, auth, or deployment changes are needed.

## Non-Goals

- Calculating exact pet ages from birth dates (we use the existing `age_months` field).
- Persisting user filter preferences.
- Adding age filtering for pending pets.
- New backend services or deployment configuration.

## What Changes

- `app/petstore_app/catalog.py`: `search_pets()` gains optional `min_age_months: int | None` and `max_age_months: int | None` parameters with validation and per-pet filter predicates.
- `app/tests/test_pet_catalog.py`: focused tests for the new age filtering parameters.
- `app/web/index.html`: age category filter buttons or select dropdown in the toolbar.
- `app/web/app.js`: age filter logic wired to the new UI controls.

## Impact

- **App behavior**: available pets outside the specified age range are excluded from results when the age filter is active.
- **Tests**: new backend unit tests for age filtering; no existing tests change.
- **Humans**: scope approval, code review, merge, and deployment remain human-gated.

## Human Gates

- Scope approval: required before implementation begins.
- Review approval: PR review before merge.
- Merge approval: human merges the PR.
- Deployment approval: human deploys to production.
