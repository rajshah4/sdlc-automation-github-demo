# Change: Age Range Search Filter

## Why

Adoption coordinators need to help families find age-appropriate pets. Currently, the catalog search only supports species, status, and tag filters. Adding minimum and maximum age filters lets coordinators match pets to household needs (e.g., finding young pets for active families or mature pets for quieter homes).

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-73
- Trigger: jira:issue_created
- Automation: jira-to-pr

## Assumptions

- Age is represented in months (`age_months` field already exists on Pet dataclass)
- Age range filtering is backend-only; no UI changes required unless explicitly requested
- Default status filtering (available pets only) remains unchanged
- Negative ages are invalid and should be rejected
- Inverted ranges (min > max) are invalid and should be rejected

## Non-Goals

- UI changes (static HTML/JS forms)
- Persistence or database changes
- Authentication or authorization changes
- New dependencies
- Deployment changes

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets` function
- Validate that age values are non-negative
- Validate that min_age <= max_age when both are provided
- Filter pets by age range when parameters are provided
- Add comprehensive tests for age range filtering

## Impact

- App behavior: Pet search can now filter by age range
- Tests: New test cases for age range matching, exclusion, boundary conditions, and validation errors
- Humans: PR requires review and merge approval; no deployment changes needed

## Human Gates

- Scope approval: Jira ticket accepted as-is
- Review approval: Human must review PR
- Merge approval: Human must approve merge
- Deployment approval: Standard deployment process, no special approval needed
