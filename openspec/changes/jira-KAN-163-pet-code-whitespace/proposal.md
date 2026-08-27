# Change: Fix Pet Code Whitespace Validation

## Why

Support agents frequently copy pet codes from support messages, emails, or spreadsheets. Accidental leading or trailing whitespace causes adoption requests to fail with "pet cannot be found" errors, even when the pet code itself is valid. This creates support friction and customer frustration.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-163
- Trigger: Jira webhook `jira:issue_created`
- Automation: `jira-request-to-pr` / `sdlc-story`
- Evidence: Code investigation confirmed exact string matching without whitespace normalization in `app/petstore_app/adoptions.py`

## Assumptions

- Pet codes in the system do not intentionally use leading/trailing whitespace.
- Support agents are the primary users affected by this issue.
- The fix should match the existing normalization behavior in `search_pets()`.
- Backward compatibility is maintained (no one depends on whitespace being significant).

## Non-Goals

- Changing pet code format or structure.
- Modifying UI input fields.
- Adding new validation rules beyond whitespace trimming.
- Changing any pet availability or status validation logic.

## What Changes

- Normalize pet codes by trimming leading and trailing whitespace in `create_adoption_order()`.
- Add three test cases for whitespace handling (leading, trailing, both).
- Align adoption flow with catalog search behavior (which already trims whitespace).

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira issue KAN-163 describing support agents copying pet codes with accidental whitespace.
- `Stop 2 - Wiki/Docs`: Reviewed `AGENTS.md` and repository structure (no specific docs for pet code format).
- `Stop 3 - Logs`: No log fixtures available for this issue (not a logged error scenario).
- `Stop 4 - Repo/Files`: Code investigation confirmed `adoptions.py` uses exact string match without `.strip()`, while `catalog.py` does normalize inputs.
- `Stop 5 - Tests/PR`: Three new test cases added, validation passed, draft PR created.

## Impact

- App behavior: Support agents can successfully copy pet codes without manual whitespace cleanup.
- Tests: Three new test cases cover leading, trailing, and surrounding whitespace scenarios.
- Humans: Reviewers approve the scope, review the PR, and make the merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation.
