# Change: Sort Available Pets by Adoption Fee

## Why

Adopters want to compare affordable options by sorting available pets by adoption fee in ascending or descending order. This helps users make budget-conscious adoption decisions while browsing the pet catalog.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-111
- Trigger: Jira ticket `KAN-111`
- Automation: Replicated factory delegated conversation (run id: `replicated-factory-20260715-164840`)

## Assumptions

- Sorting is an optional filter; default catalog behavior remains unchanged
- The implementation uses the existing `adoption_fee_cents` field (integer cents)
- Sorting applies only to available pets (default status="available" behavior unchanged)
- No UI changes are required unless explicitly scoped; this focuses on backend functionality
- No payment processing, persistence changes, or new dependencies

## Non-Goals

- Payment processing or billing integration
- Persistent user preferences for sort order
- UI redesign or frontend implementation (unless explicitly requested)
- Multi-field sorting (e.g., sort by fee then age)
- Authentication or authorization changes

## What Changes

- Add optional `sort_by` parameter to `search_pets()` with values `"fee_asc"` and `"fee_desc"`
- When `sort_by="fee_asc"`, results are ordered by `adoption_fee_cents` ascending (lowest first)
- When `sort_by="fee_desc"`, results are ordered by `adoption_fee_cents` descending (highest first)
- When `sort_by` is not provided, results maintain current order (no sorting)
- Invalid `sort_by` values raise `ValueError`

## Impact

- App behavior: Catalog search can now return results sorted by adoption fee
- Tests: New focused tests for ascending sort, descending sort, default behavior, and invalid values
- Humans: Code review and merge approval required

## Human Gates

- Scope approval: Jira ticket `KAN-111` provides acceptance criteria
- Review approval: Required before merge
- Merge approval: Required before merging to main
- Deployment approval: Standard deployment process applies
