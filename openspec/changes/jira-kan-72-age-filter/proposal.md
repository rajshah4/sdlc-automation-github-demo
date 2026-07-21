# Change: Pet Age Range Filter

## Why

Adopters want to search for pets by age category (puppies, adults, seniors) but the current search ignores age preferences, showing all pets regardless of age. This prevents adopters from finding age-appropriate matches and creates a poor search experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-72
- Trigger: jira:issue_created
- Automation: Jira-to-PR work cell

## Assumptions

- Age is already stored in `age_months` field on Pet records.
- Age filtering uses minimum and maximum age boundaries in months.
- Default search behavior (status="available") remains unchanged.
- No UI changes are required initially; backend capability is sufficient.
- Age ranges are inclusive (min ≤ age ≤ max).

## Non-Goals

- UI components for age range input (can be added later).
- Age category labels like "puppy", "adult", "senior" (use numeric months).
- Age-based sorting or recommendations.
- Schema changes or new data persistence.
- Changes to adoption workflow or other catalog features.

## What Changes

- Add optional `min_age_months` parameter to `search_pets()`.
- Add optional `max_age_months` parameter to `search_pets()`.
- Validate that age values are non-negative.
- Validate that min_age ≤ max_age when both are provided.
- Filter search results to include only pets within the specified age range.

## Impact

- App behavior: Adopters can filter pets by age range. Default search (no age filters) returns all available pets as before.
- Tests: Add focused tests for age filtering with valid ranges, boundary cases, and invalid inputs.
- Humans: PR review required. No schema, auth, or deployment changes needed.

## Human Gates

- Scope approval: Automated based on Jira issue creation.
- Review approval: Human reviewer must approve PR before merge.
- Merge approval: Human reviewer must merge after approval.
- Deployment approval: Standard deployment process applies.
