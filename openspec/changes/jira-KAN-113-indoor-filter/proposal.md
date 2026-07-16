# Change: Indoor-Friendly Pet Filter

## Why

Adopters living in apartments or indoor-only environments need a way to filter the pet catalog to show only pets suitable for indoor living. Currently, they must manually review each pet's tags to identify indoor-friendly options.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-113
- Trigger: Replicated Jira Delegated Factory
- Automation: Story to PR work cell

## Assumptions

- The existing `tag` filter in the backend can serve as the basis for this feature
- The `indoor` tag already exists on suitable pets (Mochi and Pip)
- UI changes are in scope per the acceptance criteria
- No backend API changes are needed beyond what already exists
- The filter should be additive and work with existing name and species filters

## Non-Goals

- Adding new pet tags or modifying existing pet data beyond this demo
- Implementing multi-tag filtering (AND/OR logic)
- Adding tag management or tag creation features
- Backend API changes or new endpoints
- Persistence of filter preferences

## What Changes

- Add an "Indoor only" checkbox control to the static UI
- Wire the checkbox to filter pets using the existing `indoor` tag
- Ensure the filter works with existing name and species filters
- Maintain the default behavior (all available pets) when unchecked

## Impact

- App behavior: Adopters can now filter the catalog to show only indoor-friendly pets
- Tests: Add focused backend tests for indoor tag filtering; add UI smoke test coverage
- Humans: Review scope, implementation, test coverage, and merge decision

## Human Gates

- Scope approval: Jira story and acceptance criteria define the scope
- Review approval: Human reviewer must approve the PR
- Merge approval: Human reviewer must approve and merge
- Deployment approval: Human controls deployment timing
