# Proposal: Filter pets by maximum adoption fee

**Source issue:** [#101 – Filter pets by max adoption fee](https://github.com/rajshah4/sdlc-automation-github-demo/issues/101)
**Run ID:** eval-slim-20260707-094135

## Why

Adoption coordinators need a way to show families only pets whose adoption fees
are within their budget. Without this filter, families must manually scan each
listing and may disengage when they see fees they cannot afford.

## What changes

- `app/petstore_app/catalog.py`: add an optional `max_fee_cents: int | None`
  parameter to `search_pets`. When supplied and non-negative, exclude pets
  whose `adoption_fee_cents` exceeds the limit.
- `app/web/index.html`: add a "Max adoption fee (dollars)" text input to the
  search toolbar.
- `app/web/app.js`: read the new input, convert dollars to cents (multiply by
  100, floor), and filter the static pet list client-side.
- `app/tests/test_pet_catalog.py`: add focused tests for the new filter.

## Impact

- Backend filter is additive and opt-in; all callers that omit `max_fee_cents`
  behave identically to the current code.
- UI change adds one labelled input; layout and existing controls are unchanged.
- No schema migration, auth change, new service, or external dependency.

## Assumptions

1. Fee input is in whole US dollars (families think in dollars, not cents).
   The UI converts to cents before filtering.
2. A blank or zero max-fee input means "no cap" (show all affordable pets).
3. Negative values are rejected with `ValueError` in the backend.
4. Pending pets remain hidden in default search (status="available" default
   is preserved).

## Non-goals

- No payment processing, billing, or persistence.
- No new API endpoint or microservice.
- No deployment or infrastructure change.
- No currency formatting beyond the existing `$` prefix in the UI.
