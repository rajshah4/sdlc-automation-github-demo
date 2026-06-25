# Change: Add maximum adoption fee filter to pet search

## Source

Jira issue: [KAN-15](https://all-hands-company.atlassian.net/browse/KAN-15)  
GitHub issue: Not applicable (Jira-direct automation)  
Trigger: `openhands-requested` label on Jira issue created event  
Assignee: OpenHands automation (jira-direct build work cell)

## Why

Adoption counselors report that families frequently ask to see pets within their budget before visiting the shelter. Currently, search results include all pets regardless of adoption fee, forcing families to manually filter results or visit only to find pets they cannot afford.

This request uses business language ("families need to find pets they can afford") which maps to the Petstore Catalog Search capability's need for a maximum adoption fee filter, as documented in `docs/wiki/pet-discovery-affordability.md`.

Log evidence in `docs/logs/pet-search-budget-limit.ndjson` shows a family searched with a $75 budget limit but received Scout ($125) in results, confirming the filter is needed.

## What Changes

- **File**: `app/petstore_app/catalog.py`
  - Add optional `max_adoption_fee_cents` parameter to `search_pets()` function
  - Filter out pets where `adoption_fee_cents > max_adoption_fee_cents`
  - Validate that max_adoption_fee_cents is non-negative when provided

- **File**: `app/tests/test_pet_catalog.py`
  - Add test for basic fee cap filtering
  - Add test for fee cap combined with other filters
  - Add test for negative fee rejection

## Impact

- **Who benefits**: Families searching for affordable pets, adoption counselors helping families pre-filter options
- **How behavior changes**: Search results will exclude pets above the specified maximum adoption fee when the filter is provided
- **What stays the same**: 
  - Default search behavior (returns only available pets) is unchanged
  - All existing filters (species, status, tag) continue to work
  - Pending pets remain hidden unless explicitly requested via status filter
  - Money is still represented as integer cents

## Assumptions

1. "Families need to find pets they can afford" → maximum adoption fee filtering capability
2. "Budget", "afford", "fee cap", "cost range" are business synonyms for maximum adoption fee
3. The filter is optional; omitting it preserves current behavior
4. The feature applies to catalog search only, not adoption checkout or payment processing
5. Integer cents representation is sufficient (no currency conversion needed)
6. The wiki and log context correctly represent product intent

## Non-Goals

- Payment processing or checkout
- Adoption application workflow changes
- Persistent saved searches or user preferences
- Currency conversion
- Authentication or authorization
- New external dependencies
- UI changes (static web UI in app/web/ is out of scope unless explicitly requested)
- Email notifications or alerts
- Database schema changes

## Human Gates

1. **Scope approval**: Does the interpretation "families need affordable pets" → "maximum adoption fee search filter" match product intent?
2. **Implementation review**: Is the parameter name `max_adoption_fee_cents` clear and consistent with the codebase?
3. **Test sufficiency**: Do the three test scenarios (matching, combination, validation) cover the requirement adequately?
4. **PR approval**: Review OpenSpec artifacts, code changes, and test evidence before merge
5. **Production decision**: Human decides when this feature is deployed to production
