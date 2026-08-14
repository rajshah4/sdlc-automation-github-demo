# Change: Pet Age Range Filter

## Why

Adopters want to search for pets by age preferences (puppies, adults, or senior pets). Currently, the search page shows all available pets regardless of age, making it difficult for adopters to find pets that match their age preferences.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-50
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira to PR work cell

## Assumptions

- Age is already stored as `age_months` in the Pet dataclass
- Age filtering should work alongside existing status, species, and tag filters
- Age preferences are expressed as integer months (min/max range)
- Default search behavior (available pets only) must be preserved
- No UI changes are required in this iteration

## Non-Goals

- UI form inputs for age selection (static web app remains unchanged)
- Age display formatting (years/months conversion)
- New dependencies or external services
- Data persistence or schema changes
- Authentication or authorization changes

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets()` function
- Filter pets by age range when parameters are provided
- Validate age parameters (reject negative values and inverted ranges)
- Add focused backend tests for age filtering

## Impact

- App behavior: Pet search can now filter by age range; default search unchanged
- Tests: New test cases for age filtering, boundary validation, and combined filters
- Humans: Requires code review and QA validation before merge

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required after PR submission
- Merge approval: Required by human reviewer
- Deployment approval: Required before production release
