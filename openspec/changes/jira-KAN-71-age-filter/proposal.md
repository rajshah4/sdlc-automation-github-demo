# Change: Pet Age Range Filter

## Why

Adopters want to search for pets by specific life stages (puppies, adults, or senior pets). Currently, age preferences are ignored in search, showing too many irrelevant pets. Filtering by age range will help adopters find pets that match their household needs.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-71
- Trigger: Jira webhook (issue_created)
- Automation: sdlc-automation-github-demo Jira-to-PR work cell

## Assumptions

- Age is already tracked in months (`age_months`) in the Pet dataclass
- Age filtering is an optional search parameter (does not change default behavior)
- Negative ages and inverted ranges (min > max) should be rejected
- Default search continues to return only available pets unless explicitly requested otherwise
- No UI changes are included in this scope (backend API only)

## Non-Goals

- UI implementation for age filter inputs
- Age category labels (e.g., "puppy", "adult", "senior")
- Modifying the Pet dataclass or data structure
- Changing adoption fee logic or other search filters
- Authentication or authorization changes

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets()` function
- Filter results to only include pets within the specified age range
- Validate that age parameters are non-negative and min <= max

## Impact

- App behavior: Search API supports age filtering; default behavior unchanged
- Tests: New focused tests for age range filtering, validation, and boundary cases
- Humans: Must approve scope, review PR, merge, and deployment

## Human Gates

- Scope approval: Humans confirm that backend-only age filter satisfies the requirement
- Review approval: Humans review code quality, test coverage, and edge cases
- Merge approval: Humans approve PR merge after review
- Deployment approval: Humans control when changes reach production
