# Change: Filter Pets by Max Adoption Fee

## Why

Adoption coordinators need a way to filter available pets by maximum adoption
fee so families can find pets that fit their budget. This addresses GitHub
issue #88 and requires no new services, persistence, or external dependencies.

## Source

- GitHub issue: #88 — Filter pets by max adoption fee
- Story: As an adoption coordinator, I want to filter available pets by maximum adoption fee so families can find pets that fit their budget.
- Automation: SDLC Automation Demo — canvas factory run `codex-smoke-canvas-factory`

## Assumptions

- The max fee filter applies to **available** pets only (product rule: default search returns available pets).
- The fee threshold is inclusive: a pet whose fee equals the max is included.
- The fee value is stored as integer cents in the backend (`adoption_fee_cents`).
- The UI input is in whole dollars; the filter converts to cents for comparison.
- A missing or empty max fee input means no upper bound (the parameter is optional).
- Negative max_fee_cents values are invalid and raise `ValueError`.
- No new packages, persistence, auth, payment, or deployment changes are needed.

## Non-Goals

- Payment processing or billing.
- Persisting user filter preferences.
- Currency conversion or locale formatting changes.
- Filtering pending pets by fee.
- New backend services or deployment configuration.

## What Changes

- `app/petstore_app/catalog.py`: `search_pets()` gains an optional `max_fee_cents: int | None` parameter with validation and a per-pet filter predicate.
- `app/tests/test_pet_catalog.py`: four focused tests for the new parameter.
- `app/web/index.html`: a max fee dollar input inside the toolbar.
- `app/web/app.js`: `feeToCents()` helper and filter predicate wired to the new input.

## Impact

- **App behavior**: available pets with `adoption_fee_cents > max_fee_cents` are excluded from results when the filter is active.
- **Tests**: four new backend unit tests; no existing tests change.
- **Humans**: scope approval, code review, merge, and deployment remain human-gated.

## Human Gates

- Scope approval: required before implementation begins.
- Review approval: PR review before merge.
- Merge approval: human merges the PR.
- Deployment approval: human deploys to production.
