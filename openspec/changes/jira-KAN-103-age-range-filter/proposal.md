# Change: Pet Age Range Filter

## Why

Support reports indicate that customers are seeing pets they cannot adopt, creating confusion and extra work for operations. Customers need the ability to filter pets by age range to find pets appropriate for their household and lifestyle.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-103
- Trigger: Replicated Factory Automation (Jira-to-PR delegation)
- Automation: replicated-factory-20260715-131342

## Assumptions

- Age filtering uses integer months (consistent with existing `Pet.age_months` field)
- Both `min_age_months` and `max_age_months` are optional parameters
- Default search behavior (no age filters specified) remains unchanged
- Age range must be valid: no negative ages, min cannot exceed max
- Filtering applies to the existing pet catalog without requiring new dependencies or data

## Non-Goals

- Age calculation or date-of-birth tracking
- Dynamic age updates over time
- UI changes (backend-only for this iteration)
- Persistence or database changes
- New services or deployment configuration

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets()`
- Filter pets by age range when parameters are provided
- Validate age range parameters (reject negative ages and inverted ranges)
- Add focused backend tests for age filtering scenarios

## Impact

- App behavior: Customers can filter pet search results by minimum and/or maximum age
- Tests: New test cases for age range filtering, boundary conditions, and validation
- Humans: Code review required before merge; QA should verify age filtering works correctly

## Human Gates

- Scope approval: Automation inferred scope from Jira story; human should review assumptions
- Review approval: Human must review code changes and tests
- Merge approval: Human must approve PR merge
- Deployment approval: Human must approve deployment to production
