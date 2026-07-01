# Change: Add Pet Age Range Filter

## Why

Adopters want to search for pets by age range (puppies, adults, or seniors) to find pets that match their lifestyle and experience level. Currently, the search page shows all available pets without age filtering, making it difficult for adopters to find age-appropriate pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-52
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira to PR workflow

## Assumptions

- Age filtering is an optional parameter; existing searches without age filters continue to work unchanged
- Age is already stored in months (`age_months`) in the pet catalog
- No UI changes are required in this iteration unless explicitly requested; backend support is sufficient
- Default search behavior (available pets only) remains unchanged
- Negative ages and inverted ranges (min > max) should be rejected

## Non-Goals

- Changing the pet data model or adding new age fields
- Creating new UI components or modifying the web interface
- Adding age-based recommendations or sorting
- Implementing age categories (puppy/adult/senior) as named filters
- Changing authentication, persistence, or deployment

## What Changes

- Add optional `min_age_months` and `max_age_months` parameters to `search_pets()` in `catalog.py`
- Validate that age filters are non-negative and that min ≤ max when both are provided
- Filter pets to only include those within the specified age range

## Impact

- App behavior: Adopters can filter search results by age range; existing searches without age filters are unaffected
- Tests: Add focused backend tests for age filtering with valid ranges, boundary cases, and invalid inputs
- Humans: Product owner approves scope; reviewer approves implementation; operations approves deployment

## Human Gates

- Scope approval: Product owner confirms age filtering in months meets adopter needs
- Review approval: Code reviewer approves implementation, tests, and validation evidence
- Merge approval: Team lead approves merge to main
- Deployment approval: Operations approves deployment when ready
