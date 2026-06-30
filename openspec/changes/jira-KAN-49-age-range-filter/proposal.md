# Change: Age-Range Filtering for Pet Search

## Why

Adopters want to search for pets within specific age ranges to find companions that match their lifestyle and preferences. This feature allows filtering by minimum and maximum age in months, helping adopters find pets that meet their needs.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-49
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Demo Jira-to-PR work cell

## Assumptions

- Age is represented in months (consistent with existing `age_months` field).
- Default search behavior (available pets only) remains unchanged.
- Both min and max age filters are optional; either, both, or neither can be specified.
- Invalid age ranges (negative values or min > max) are rejected with clear error messages.
- No UI changes are included in this implementation; the backend API is the focus.

## Non-Goals

- UI changes for age-range inputs (static UI remains unchanged).
- Changes to pet data model or storage.
- Integration with external age verification systems.
- Conversion between age units (months, years, weeks).

## What Changes

- Add `min_age_months` and `max_age_months` optional parameters to `search_pets()` function.
- Validate age range parameters (non-negative, min ≤ max).
- Filter search results to include only pets within the specified age range.
- Add comprehensive test coverage for age filtering scenarios.

## Impact

- App behavior: Pet search API now supports age-range filtering via optional parameters.
- Tests: New test cases added for age filtering, boundary validation, and error handling.
- Humans: Adopters can find pets within desired age ranges; requires human review and merge approval.

## Human Gates

- Scope approval: Humans approve that age-range filtering is the correct interpretation of the requirement.
- Review approval: Code review required before merge.
- Merge approval: Human approval required for PR merge.
- Deployment approval: Human approval required for production deployment.

## Note on Requirement Discrepancy

The Jira issue summary states "Add age-range filtering" but the description mentions "filter pets by maximum adoption fee." This implementation addresses the **summary** requirement (age-range filtering) as it is the primary identifier. If adoption fee filtering is also required, a separate story should be created to maintain focused, reviewable changes.
