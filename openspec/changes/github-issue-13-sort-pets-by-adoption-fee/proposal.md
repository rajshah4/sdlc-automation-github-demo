# Change: Sort Pets by Adoption Fee

## Why

Adopters want to compare budget-friendly pet adoption options by viewing available pets sorted from lowest to highest adoption fee. This helps potential adopters make informed decisions based on their budget constraints.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/13
- Trigger label: `openhands-build`
- Automation: SDLC Story to PR

## Assumptions

- Sorting applies only to available pets (the default search behavior).
- Sort order is low to high (ascending) by adoption fee.
- Sorting is an optional parameter that defaults to no sorting (preserves current behavior).
- All existing filters (species, status, tag, query) continue to work with sorting.

## Non-Goals

- UI changes are out of scope for this issue.
- Sorting by other fields (age, name, species) is not included.
- Descending (high to low) sort order is not implemented.
- Pagination or infinite scroll features.

## What Changes

- Add optional `sort_by` parameter to `search_pets()` function in `catalog.py`.
- When `sort_by="adoption_fee"`, results are sorted by `adoption_fee_cents` in ascending order.
- When `sort_by` is not specified or is `None`, original order is preserved.

## Impact

- App behavior: Catalog search can now return results sorted by adoption fee when requested.
- Tests: New tests verify sorted order and unchanged default behavior.
- Humans: PR review ensures the implementation is narrow and doesn't break existing functionality.

## Human Gates

- Scope approval: Issue submitter confirms this matches the intended feature.
- Review approval: Code reviewer approves the implementation approach.
- Merge approval: Authorized person merges the PR after tests pass.
- Deployment approval: Deployment follows standard approval process.
