# OpenSpec: Filter Pets by Max Adoption Fee

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/7
- Trigger: `openhands-build` label added to issue #7
- Automation: SDLC Automation Demo build work cell

## Request Summary

Add an optional filter to the pet catalog search that allows users to find pets within their budget by specifying a maximum adoption fee. This feature helps potential adopters quickly identify pets they can afford without having to browse through all listings.

## Assumptions

- Adoption fees are already stored as integer cents in the Pet dataclass.
- The filter is optional—when not provided, all pets matching other criteria are returned.
- This is a search filter only; no payment processing or checkout logic is needed.
- The filter applies to the existing search behavior without changing default status filtering (available pets only by default).

## Non-Goals

- Payment processing, billing, or checkout functionality
- Currency conversion or multi-currency support
- Persistence of user preferences
- Authentication or authorization
- New external dependencies
- Changes to the Pet dataclass or data schema
- UI changes (backend filter only for this sparse issue)

## Acceptance Criteria

- [ ] `search_pets()` accepts an optional `max_adoption_fee_cents` parameter
- [ ] Pets with `adoption_fee_cents <= max_adoption_fee_cents` are included in results
- [ ] Pets with `adoption_fee_cents > max_adoption_fee_cents` are excluded from results
- [ ] When `max_adoption_fee_cents` is not provided, all pets matching other criteria are returned
- [ ] Negative values raise a `ValueError`
- [ ] Existing search behavior (species, status, tag, query) remains unchanged
- [ ] All existing tests continue to pass

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Human decision
- Deployment approval: Human decision

## Implementation Plan

1. Add `max_adoption_fee_cents: int | None = None` parameter to `search_pets()` in `catalog.py`
2. Add validation to reject negative values (raise `ValueError`)
3. Add filtering logic in the search loop to exclude pets above the max fee
4. Add focused backend tests in `test_pet_catalog.py`:
   - Test that pets within budget are included
   - Test that pets above budget are excluded
   - Test that negative values raise ValueError
   - Test that omitting the parameter returns all matches

## Validation Plan

- Run `python3 -m pytest -q app/tests/test_pet_catalog.py` to verify new tests pass
- Run `python3 -m pytest -q app/tests/` to ensure no regressions
- Verify test coverage includes: match, exclusion, negative validation, and optional parameter

## Evidence Checklist

- [ ] Tests added for max fee filtering
- [ ] All tests pass (new and existing)
- [ ] No UI changes required (backend filter only)
- [ ] Residual risk documented in PR
