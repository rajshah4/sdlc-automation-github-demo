# OpenSpec: Weekend Pet Availability Filter

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/3
- Trigger: `openhands-build` label applied
- Automation: GitHub webhook → OpenHands build work cell

## Request Summary

Allow adopters to filter the pet catalog to show only pets available for visits this weekend, helping them plan weekend adoption center visits.

## Assumptions

- Weekend availability is a boolean property of each pet (either available or not).
- Weekend availability is independent of adoption status (a pet can be "available" for adoption but not available for weekend visits).
- No scheduling system, time zones, or dynamic calendar logic is required.
- Weekend availability data is static, managed in the catalog data.
- No UI changes are required unless explicitly requested in the issue scope.

## Non-Goals

- Dynamic scheduling or calendar integration
- Time zone handling or date calculations
- Appointment booking or reservation system
- Email notifications for weekend availability
- Integration with external systems
- Database or persistence layer changes
- Authentication or authorization changes

## Acceptance Criteria

- [x] Catalog search supports an optional weekend availability filter.
- [x] Pets without weekend availability are excluded when the filter is enabled.
- [x] Existing search behavior is unchanged when the filter is omitted.
- [x] Tests cover matching, exclusion, and default behavior.

## Human Gates

- Scope approval: Humans review and approve the minimal implementation approach.
- Review approval: Humans review code quality, test coverage, and architecture.
- Merge approval: Humans approve the PR for merge after review.
- Deployment approval: Humans decide when and how to deploy changes.

## Implementation Plan

1. Add `weekend_available` boolean field to the `Pet` dataclass in `catalog.py`.
2. Update existing `PETS` test data to include weekend availability values.
3. Add optional `weekend_available` parameter to `search_pets()` function signature (default: `None`).
4. Implement filtering logic: when `weekend_available` is `True`, exclude pets where the field is `False`.
5. Preserve all existing search behavior when `weekend_available` is `None` or omitted.
6. Add focused tests to `test_pet_catalog.py` covering:
   - Filtering to only weekend-available pets
   - Excluding non-weekend-available pets
   - Default behavior when filter is omitted
   - Combination with other filters (species, status, tag)

## Validation Plan

- Run `python3 -m pytest -q app/tests/test_pet_catalog.py` to verify catalog tests pass.
- Run `python3 -m pytest -q app/tests/` to verify no regressions in other tests.
- Validate open spec with `python3 skills/sdlc-story/scripts/validate_open_spec.py specs/github-issue-3/open-spec.md`.

## Evidence Checklist

- [ ] Tests added or updated.
- [ ] Commands run.
- [ ] UI evidence captured when UI changed (N/A - no UI changes).
- [ ] Residual risk documented.
