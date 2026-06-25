# Change: Expose budget filter in UI for pet adoption search

## Why

Adoption counselors report that families want to find pets that fit their budget before visiting the shelter. The backend already supports maximum adoption fee filtering, but the UI doesn't expose this capability. Families currently have to browse all available pets without knowing which ones are affordable.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-16
- Summary: "Counselors say families want to find pets that fit their budget before they visit"
- Trigger: Jira webhook `jira:issue_created` via `jira-direct` source
- Automation: `openhands-build` (Jira-to-Story)

## Assumptions

- Adoption fees are represented as integer cents in the Petstore domain model (confirmed in AGENTS.md).
- The backend `search_pets` function already has `max_adoption_fee_cents` parameter with full implementation and tests.
- The UI needs to convert user-friendly dollar input to cents for backend compatibility.
- Default search behavior (show only available pets) remains unchanged.
- The request is limited to UI changes; no backend changes needed.

## Non-Goals

- Backend implementation (already complete)
- Payment processing, billing, discounts
- Persistence or database changes
- Authentication or authorization
- Currency conversion beyond dollars/cents
- New dependencies

## What Changes

- Static UI (`app/web/index.html`) adds a "Maximum Budget" input field with dollar formatting.
- UI JavaScript (`app/web/app.js`) converts dollar input to cents and filters pets by adoption fee.
- Pets with fees above the maximum budget are excluded from results.
- Invalid or empty budget input shows all pets (graceful degradation).

## Impact

- App behavior: Families can narrow pet search results by their budget before visiting.
- Tests: Backend tests already cover the fee filtering logic. UI change is visually verifiable.
- Humans: Reviewers approve the UI design, scope, and merge decision.

## Human Gates

- Scope approval: Jira issue review and PR review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation.
