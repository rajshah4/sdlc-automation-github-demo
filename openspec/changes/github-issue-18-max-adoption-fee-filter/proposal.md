# Change: Max Adoption Fee Filter

## Why

Adopters need to find pets within their budget by filtering the catalog by maximum adoption fee, enabling more adopters to discover affordable pets.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/18
- Trigger label: `openhands-build`
- Automation: `openhands-build` work cell

## Assumptions

- Adoption fees are already stored as integer cents in the Pet model.
- The filter is optional; omitting it returns all pets matching other criteria.
- Negative fee values are invalid and should raise an error.
- The default status filter (available pets only) remains unchanged.

## Non-Goals

- Payment processing or checkout functionality
- Persistence of filter preferences
- Currency conversion or localization
- Billing, invoicing, or transaction history
- New external dependencies

## What Changes

- Add optional `max_fee_cents` parameter to `search_pets()` function in `catalog.py`
- Filter pets where `adoption_fee_cents <= max_fee_cents` when parameter is provided
- Validate that `max_fee_cents` is non-negative when provided
- Add focused backend tests for inclusion, exclusion, and validation

## Impact

- App behavior: Catalog search can now filter by maximum adoption fee
- Tests: New test cases for max_fee_cents filtering and validation
- Humans: PR requires review and merge approval before deployment

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required for PR merge
- Merge approval: Required before deployment
- Deployment approval: Required for production release
