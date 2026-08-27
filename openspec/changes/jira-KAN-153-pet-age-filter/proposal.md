# Change: Pet Age Range Filter

## Why

Customers need the ability to filter pets by age range to find pets that match their preferences and living situation. Currently, customers cannot narrow their search to specific age ranges, which forces them to manually review all available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-153
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- Age filtering should accept optional minimum and maximum age parameters in months
- Filters should work independently (users can specify min only, max only, or both)
- Age filters should compose with existing filters (species, status, tag)
- Invalid ranges (negative values, min > max) should be rejected with clear error messages
- The Pet dataclass already contains age_months field (no schema changes needed)

## Non-Goals

- Changing pet age data or adding new pets
- UI changes to expose age filtering controls
- Age grouping or categorical filters (e.g., "puppy", "senior")
- Age-based sorting or ranking
- Persistence or database changes

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets()` function
- Add validation for age range parameters (reject negative values and inverted ranges)
- Filter pets by age range when parameters are provided
- Add comprehensive test coverage for age filtering scenarios

## Impact

- App behavior: Customers can filter pet search results by age range
- Tests: New test cases for age filtering, boundary conditions, and error cases
- Humans: PR requires review approval before merge; no deployment changes needed

## Human Gates

- Scope approval: Jira issue defines the requirement
- Review approval: Draft PR must be reviewed by team
- Merge approval: Human must approve and merge PR
- Deployment approval: No deployment changes required (code-only change)
