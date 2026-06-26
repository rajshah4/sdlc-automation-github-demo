# Change: Add age-range filtering to pet search

## Why

Adopters need a way to find pets within a specific age range that fits their household and lifestyle preferences.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/26
- Trigger label: `openhands-build`
- Automation: `sdlc-story`

## Assumptions

- Pet ages are represented as integer months in the Petstore domain model.
- The request is limited to catalog search behavior.
- Age filtering applies only to returned results; data model does not change.

## Non-Goals

- UI changes are not included unless explicitly requested.
- No changes to pet data persistence, lifecycle, or other catalog filters.
- No changes to adoption process or fee calculations.

## What Changes

- Catalog search accepts optional `min_age` and `max_age` parameters (in months).
- Pets outside the specified age range are excluded from results.
- Negative ages are rejected.
- Inverted ranges (min > max) are rejected.

## Impact

- App behavior: adopters can narrow search results by age range.
- Tests: catalog tests cover matching, exclusion, negative ages, and inverted ranges.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: GitHub issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
