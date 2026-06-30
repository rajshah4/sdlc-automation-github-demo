# Change: Fix Available Pets Filter

## Why

Customers report seeing pending pets in the available pets list. The default pet search must return only pets with `status="available"` per product requirements. The catalog regression affects customer experience and violates documented behavior.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-38
- Trigger: Jira webhook `jira:issue_created` with label `sidekick-experiment`
- Automation: SDLC Automation Demo - Jira-to-PR with context sidekick

## Assumptions

- The bug is in the web UI layer (`visible_pets()` function), not core catalog logic.
- The `search_pets()` function correctly filters by status.
- Runtime config mode control is intentional for demo purposes; the fix restores default filtering.
- No schema, auth, or cloud infrastructure changes are needed.

## Non-Goals

- Changes to explicit pending-pet searches (ops/support workflows).
- UI redesign or new filtering capabilities.
- Database or persistence layer changes.
- Changes to adoption or payment flows.

## What Changes

- Restore default available-only filtering in the `visible_pets()` function.
- Ensure pending pets never appear in the available-pets web experience.
- Add regression test coverage for the default catalog view.

## Impact

- App behavior: Default pet catalog returns available pets only; pending pets excluded.
- Tests: New regression test added to validate pending pets don't appear in default view.
- Humans: PR review required before merge; QA automation validates web behavior.

## Human Gates

- Scope approval: Jira ticket KAN-38 approved by requester.
- Review approval: Human reviewer must approve PR.
- Merge approval: Human must approve merge to main.
- Deployment approval: Human must approve production deployment.
