# Change: Add Age Range Filter to Pet Catalog

## Why

Customers want to filter pets by age to find pets that match their preferences and living situations. Currently, customers can only search by name, species, status, and tags, but cannot narrow results by age.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-152
- Trigger: Jira webhook (issue_created)
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- Age filtering is optional and works alongside existing filters
- Age is already stored in `age_months` field for all pets
- Age boundaries are inclusive (min_age_months <= pet.age_months <= max_age_months)
- Negative age values are invalid and should raise an error
- Inverted ranges (min > max) are invalid and should raise an error
- The default status="available" behavior remains unchanged

## Non-Goals

- UI changes (backend-only feature for this change)
- Changing age storage format or units
- Age calculation from birthdate
- Pet lifecycle or age-related business logic
- New dependencies or database changes

## What Changes

- Add optional `min_age_months` parameter to `search_pets()`
- Add optional `max_age_months` parameter to `search_pets()`
- Add validation to reject negative age values
- Add validation to reject inverted ranges (min > max)
- Add comprehensive tests for age filtering scenarios

## Impact

- App behavior: Pet catalog search accepts new optional age parameters
- Tests: New tests for age filtering (happy path, boundaries, validation)
- Humans: PR review and merge approval required

## Human Gates

- Scope approval: Required before merge
- Review approval: Required (automated review will be triggered via openhands-review label)
- Merge approval: Human decision required
- Deployment approval: Required before production release
