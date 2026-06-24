# Change: Filter Pets by Maximum Adoption Fee

## Why

Adopters want to find pets that fit their budget. Adding a maximum adoption fee filter helps users discover available pets they can afford, improving the search experience and potentially increasing adoption rates.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/11
- Trigger label: `openhands-build`
- Automation: SDLC Automation Demo GitHub Build Work Cell

## Assumptions

- Adoption fees are already stored as integer cents in the catalog
- The filter is optional; searches without a max fee constraint work as before
- UI changes are in scope since the issue mentions adopter-facing behavior
- Money representation remains integer cents (no currency conversion needed)

## Non-Goals

- Payment processing or checkout flow
- Persistent fee data or database changes
- Currency conversion or internationalization
- Billing, invoicing, or financial reporting
- Adding new external dependencies

## What Changes

- Add `max_fee_cents` optional parameter to `search_pets()` function in `app/petstore_app/catalog.py`
- Reject negative fee values with clear error messages
- Add focused backend tests for included pets, excluded pets, and invalid input
- Add max adoption fee input control to the static UI in `app/web/index.html`
- Update frontend filter logic in `app/web/app.js` to respect max fee constraint

## Impact

- App behavior: Users can filter search results by maximum adoption fee; pets above the threshold are excluded from results
- Tests: New test cases for fee filtering, negative value rejection, and boundary conditions
- Humans: PR requires scope approval, code review, and merge approval before changes reach any environment

## Human Gates

- Scope approval: Human confirms that fee filtering without payment processing is the correct interpretation
- Review approval: Human reviews implementation for correctness and security
- Merge approval: Human approves and merges the PR
- Deployment approval: Human controls when changes reach production
