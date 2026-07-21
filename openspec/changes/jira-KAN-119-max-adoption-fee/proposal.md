# Change: Filter Pets by Maximum Adoption Fee

## Why

Adopters need to find pets that fit their budget. Adding a maximum adoption fee filter to the catalog search helps users discover pets they can afford, improving the adoption experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-119
- Trigger: jira:issue_created
- Automation: SDLC Automation Demo - Jira to PR work cell

## Assumptions

- Money is represented as integer cents in the backend (as per petstore product rules).
- The UI filter is optional — users can search with or without a maximum fee.
- Default search behavior (status="available") remains unchanged.
- No payment processing, billing, or adoption flow changes are needed.

## Non-Goals

- Payment processing or checkout flow.
- Persisting user budget preferences.
- Backend authentication or authorization changes.
- Schema migrations or database changes.
- New external dependencies.

## What Changes

- `catalog.py`: Add optional `max_adoption_fee_cents` parameter to `search_pets()`.
- Validation: Reject negative maximum fees with a ValueError.
- UI: Add "Max Adoption Fee" input field in the catalog search form.
- Tests: Add focused backend tests for matching, exclusion, and validation.

## Impact

- App behavior: Users can filter pets by maximum adoption fee in both the backend API and the UI.
- Tests: New test cases for fee filtering logic and boundary validation.
- Humans: This PR requires review and merge approval before deployment.

## Human Gates

- Scope approval: Required before implementation begins.
- Review approval: Required before merge.
- Merge approval: Human decision.
- Deployment approval: Human decision.
