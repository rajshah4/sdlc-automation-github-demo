# Change: Filter pets by maximum adoption fee

## Why

Adoption coordinators need to help families find pets that fit their budget. The
catalog search has no way to cap results by adoption fee, so coordinators must
manually discard pets that are too expensive. Adding an optional
`max_fee_cents` filter closes this gap with minimal surface-area change.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/88
- Run id: `canvas-verify-full`
- Workcell: `story-to-pr`
- Story: "As an adoption coordinator, I want to filter available pets by maximum
  adoption fee so families can find pets that fit their budget."

## Assumptions

- Adoption fee is already stored as integer cents in `Pet.adoption_fee_cents`.
- An unset filter (no value supplied) returns all available pets as before — no
  default cap is imposed.
- A negative max fee is invalid and raises `ValueError`; a max fee of 0 means
  only free pets (if any exist), which is valid.
- The filter applies after the existing status filter, so pending pets remain
  hidden by default.
- No payment processing, persistence, auth, or billing changes are in scope.
- The UI exposes the filter as a dollars input (whole dollars); the backend
  works in cents.

## Non-Goals

- Minimum fee filter.
- Sorting by fee.
- Persistent user preferences.
- New services, external APIs, or schema migrations.

## What Changes

- `app/petstore_app/catalog.py`: add optional `max_fee_cents: int | None`
  parameter to `search_pets`; apply filter and validate non-negative.
- `app/web/index.html`: add a "Max adoption fee" number input to the search
  toolbar.
- `app/web/app.js`: read the dollar input, convert to cents, apply filter in
  `renderResults`.
- `app/tests/test_pet_catalog.py`: add focused tests for match, exclusion, and
  invalid negative fee.
- `app/web/tests/catalog-search.playwright.mjs`: add browser scenario for the
  fee filter.

## Evidence Waypoints

- Stop 1 – Ticket: Issue #88, sparse feature request with no implementation clues.
- Stop 2 – Wiki/Docs: `openspec/project.md` reviewed; no conflicting spec found.
- Stop 3 – Logs: No error logs relevant to this new feature.
- Stop 4 – Repo/Files: `catalog.py` (existing params), `app.js` (existing
  filter loop), `index.html` (toolbar controls), `test_pet_catalog.py`
  (existing coverage).
- Stop 5 – Tests/PR: Backend unit tests + Playwright browser scenario added;
  draft PR opened by this workcell.

## Impact

- App behavior: adoption fee filter is opt-in; all existing queries are unchanged.
- Tests: backend coverage extended; Playwright scenario covers UI path.
- Humans: reviewers approve, merge, and deploy.

## Human Gates

- Scope: this proposal.
- Code review: GitHub PR review (pending delegate).
- QA: Playwright + pytest validation (pending delegate).
- Merge: repository maintainer.
