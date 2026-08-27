# Change: Normalize pet codes with leading/trailing whitespace

## Why

Support agents sometimes copy a pet code with an accidental space before or after it. The adoption request then says the pet cannot be found even though the code is valid. This creates friction for support teams and a poor customer experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-164
- Trigger: Jira webhook `jira:issue_created`
- Automation: `jira-request-to-pr`
- Issue key: KAN-164

## Assumptions

- Pet codes follow the format `pet-XXX` with no internal whitespace.
- The whitespace is unintentional (copy-paste artifacts).
- Trimming leading/trailing whitespace will not break any valid pet codes.
- The fix should not weaken existing pet availability checks (pending pets must remain unadoptable).
- The catalog search already normalizes inputs with `.strip()`, so this brings adoption behavior into alignment.

## Non-Goals

- UI changes to prevent whitespace entry are out of scope.
- Validation of pet code format (length, character set) is not part of this fix.
- API endpoint changes, authentication, or deployment configuration are out of scope.

## What Changes

- Pet code inputs in adoption requests are normalized by trimming leading/trailing whitespace.
- Adoption behavior for valid pet codes remains unchanged.
- Pending pet availability checks continue to work correctly.
- Focused regression tests cover whitespace handling in pet code validation.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira issue KAN-164 describes support agents copying pet codes with accidental spaces.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` and `docs/repo-memory/petstore-intelligence.md` checked; no specific guidance on whitespace handling.
- `Stop 3 - Logs`: No log fixtures found for this specific issue.
- `Stop 4 - Repo/Files`: `app/petstore_app/adoptions.py` lines 19-23 (`_find_pet()`) uses exact string matching without normalization; `app/petstore_app/catalog.py` lines 39-42 already normalizes search inputs with `.strip()`.
- `Stop 5 - Tests/PR`: Added regression tests for whitespace handling and draft PR for human review.

## Impact

- App behavior: Pet codes with leading/trailing whitespace are now accepted and correctly matched.
- Tests: Existing tests pass unchanged; new tests cover whitespace normalization.
- Humans: Reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation.
