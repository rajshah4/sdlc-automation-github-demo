# Change: Filter pets by max adoption fee

## Why

Adopters need a quick way to find pets whose adoption fees fit their budget.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/21
- Trigger label: `openhands-build`
- Automation: `sdlc-story`

## Assumptions

- Adoption fees are represented as integer cents in the Petstore domain model.
- The request is limited to catalog search behavior.
- The issue title "Can you build a new filter" is interpreted as a max adoption fee filter based on common Petstore use cases.

## Non-Goals

- Payment processing, billing, discounts, and persistence changes are out of scope.
- UI changes are not included unless explicitly requested.

## What Changes

- Catalog search accepts an optional maximum adoption fee in cents.
- Pets with fees above the maximum are excluded from search results.
- Negative maximum fees are rejected with a ValueError.

## Impact

- App behavior: adopters can narrow search results by budget constraint.
- Tests: catalog tests cover matching, exclusion, and validation of negative fees.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: GitHub issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
