# Change: Trim Whitespace from Pet Codes

## Why

Support agents sometimes copy pet codes with accidental spaces before or after them. The adoption request then says the pet cannot be found even though the code is valid. This change makes copied pet codes work as expected without weakening the pet availability checks.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-170
- Trigger: Jira webhook (issue_created)
- Automation: SDLC Automation Demo - Jira to PR

## Assumptions

- Pet codes with leading or trailing whitespace should be treated as equivalent to the trimmed version.
- Trimming whitespace does not weaken security or availability validation (pet codes are public identifiers, not credentials).
- The catalog already normalizes search inputs by stripping whitespace; adoptions should follow the same pattern.
- No existing workflows depend on exact whitespace preservation in pet codes.

## Non-Goals

- Internal whitespace handling (e.g., "pet - 100" remains invalid).
- Changing pet code format validation beyond whitespace trimming.
- Email address trimming (separate concern).
- UI changes (this is a backend fix).

## What Changes

- Add `pet_id = pet_id.strip()` in `create_adoption_order()` before pet lookup.
- Add tests proving whitespace-padded pet codes now succeed.
- Update existing test to verify unknown pet IDs still fail properly.

## Impact

- App behavior: Valid pet codes work regardless of accidental leading/trailing whitespace.
- Tests: Three new test cases for whitespace handling.
- Humans: Support agents can copy pet codes without manual cleanup.

## Human Gates

- Scope approval: Humans validate this fix addresses support agent pain without introducing risk.
- Review approval: Humans review code, tests, and security implications.
- Merge approval: Humans approve merge after CI passes.
- Deployment approval: Humans control deployment timing.
