# Change: Budget-Based Pet Search

## Why

Adoption counselors report that families keep asking to see pets they can afford before they visit. Without budget filtering in the search, families waste time reviewing pets outside their price range, and counselors can't efficiently narrow options during intake calls.

## Source

- Jira issue: KAN-13 - Families need to find pets in their budget (received via Jira direct webhook)
- GitHub issue: N/A (Jira-native workflow)
- Trigger: Jira direct webhook integration
- Automation: SDLC Automation Demo (jira-direct source)

## Assumptions

- "Budget," "afford," "fee cap," and "cost range" all map to the adoption fee filtering capability.
- Adoption fees are represented in integer cents (existing Petstore convention).
- This is a search filter feature, not payment processing, checkout, or billing.
- Default search behavior (available pets only) must remain unchanged.
- Pending pets remain hidden unless status is explicitly requested.

## Non-Goals

- Payment processing or checkout UI
- Fee persistence or database schema changes
- Currency conversion
- Authentication or authorization
- New dependencies
- Modification of adoption fee data

## What Changes

- Catalog search accepts an optional `max_adoption_fee_cents` parameter.
- Pets with adoption fees above the maximum are excluded from results.
- Invalid negative fee caps are rejected with a clear error.
- Default search behavior (status filtering, available pets) remains unchanged.

## Impact

- App behavior: Search can now filter by maximum adoption fee, helping families find affordable pets.
- Tests: Added focused tests for pets included within budget, excluded above budget, and invalid negative fees.
- Humans: Counselors can use this filter during intake calls; families can self-filter before visiting.

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Required (no auto-merge)
- Deployment approval: Required for production release
