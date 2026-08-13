# Change: Pet Age Range Filtering

## Why

Customers need the ability to filter pets by age range to find pets that match their preferences and living situations. Some customers prefer younger pets, while others may be looking for older, calmer companions. This feature enables customers to narrow their search results to pets within a specific age range.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-149
- Trigger: Jira webhook (issue_created)
- Automation: jira-request-to-pr

## Assumptions

- Age filtering should work alongside existing filters (species, status, tags)
- Age is represented in months (as per existing Pet dataclass: `age_months`)
- Both minimum and maximum age filters are optional
- Negative age values should be rejected
- Min age cannot exceed max age when both are provided
- Default search behavior (available-only pets) remains unchanged

## Non-Goals

- UI changes are not included in this implementation
- Age display formatting or unit conversion (months to years)
- Changing the underlying Pet data structure
- Adding age-related sorting or recommendations

## What Changes

- Add `min_age_months` and `max_age_months` optional parameters to `search_pets()`
- Implement age range validation and filtering logic
- Add comprehensive tests for age filtering scenarios

## Impact

- App behavior: Customers can optionally filter pets by minimum and/or maximum age in months
- Tests: New test cases for age range matching, boundaries, and validation
- Humans: Product owner must review acceptance criteria; engineering must review implementation and approve merge

## Human Gates

- Scope approval: Product owner reviews that age filtering meets customer needs without UI changes
- Review approval: Engineering reviewer approves code quality and test coverage
- Merge approval: Maintainer approves merge to main branch
- Deployment approval: Operations team approves deployment to production
