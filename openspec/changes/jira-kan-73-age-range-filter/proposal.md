# Change: Pet Age Range Filter

## Why

Adoption coordinators need to help families find pets that match their household needs. Different families have different capacity for young energetic pets versus older calmer companions. An age range filter lets adopters narrow their search to pets whose age fits their lifestyle and experience level.

## Source

- GitHub issue: N/A (Jira-triggered delegated factory workflow)
- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-73
- Issue: `KAN-73`
- Title: `Live delegated factory smoke test: let adopters search by age range (2026-07-07 20:52:30Z)`
- Automation: Replicated Jira delegated factory
- Run ID: `replicated-factory-20260707-205428`

## Assumptions

- Age is already stored in the Pet catalog as `age_months` (integer months)
- Age range filters are optional; when omitted, all available pets are returned
- The filter applies as inclusive range: `min_age_months <= pet.age_months <= max_age_months`
- Either or both boundaries can be specified independently
- Negative ages are invalid and should be rejected
- Inverted ranges (min > max) are invalid and should be rejected
- The default status filter ("available") remains in place

## Non-Goals

- UI changes (this is backend catalog search only)
- Persistence or database changes
- Changes to Pet data model structure
- New dependencies or services
- Deployment configuration changes
- Integration with external systems

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets()` function
- Add validation: reject negative ages and inverted ranges
- Update filter logic to apply age range when parameters are provided
- Add focused backend tests for age range filtering scenarios

## Impact

- App behavior: Catalog search gains optional age range filtering
- Tests: New test cases for age range filtering, validation, and edge cases
- Humans: Code reviewer validates spec adherence, test coverage, and boundary handling; merge approval required before integration

## Human Gates

- Scope approval: Delegated supervisor reviewed Jira ticket scope
- Review approval: Human must review code and approve PR
- Merge approval: Human must approve merge to main branch
- Deployment approval: Human must approve any production deployment
