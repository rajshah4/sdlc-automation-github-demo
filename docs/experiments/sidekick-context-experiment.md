# Sidekick Context Experiment

Branch: `sidekick-context-experiment`

Goal: compare the current single-agent Jira-to-PR flow with a sidekick-assisted
flow that performs a read-only context scout before implementation.

## Hypothesis

Sparse Jira tickets are hard because the agent must infer the repo, docs, logs,
and files from business language. A bounded context sidekick may improve the
conversation's demo readability and reduce wasted search, but it may add elapsed
time. This experiment checks whether that trade-off fits a five-minute demo.

## Variants

| Variant | Jira label | Automation package | Behavior |
| --- | --- | --- | --- |
| Control | `control-experiment` | `automations/jira/jira-to-story-control/` | Current single-agent Jira-to-PR path using `skills/sdlc-story`. |
| Sidekick | `sidekick-experiment` | `automations/jira/jira-to-story-sidekick/` | Runs `skills/sdlc-context-sidekick` first, then hands the brief to `skills/sdlc-story`. |

Keep the normal Jira automation paused during A/B tests, or update its filter to
exclude `control-experiment` and `sidekick-experiment`, so each ticket wakes only
one experiment automation.

## Sidekick Constraints

- Read-only.
- No code edits, comments, labels, branches, commits, PRs, or Jira updates.
- Search only repo docs, logs, app code, tests, skills, and OpenSpec artifacts.
- Produce a compact `CONTEXT_BRIEF`.
- Escalate to a human instead of guessing when confidence is low.

## Test Procedure

1. Register or update the two experiment automations from this branch.
2. Pause the normal Jira-to-story automation for the A/B window.
3. Create two Jira Tasks with the same sparse business-language bug:
   - Summary: `Available pets list still shows unavailable animals`
   - Description: `Customers say the available pets page includes animals that should not be adoptable.`
4. Add `control-experiment` to the control ticket and `sidekick-experiment` to the sidekick ticket.
5. Wait for each run to open a draft PR.
6. Record run IDs, conversation URLs, PR URLs, start/completion times, token or model-cost data when available, and a readability score.
7. Resume the normal Jira-to-story automation after the test.

## Metrics

| Metric | How to Measure | Demo Target |
| --- | --- | --- |
| Time to PR | Automation run `created_at` to PR opened/commented timestamp. | Under 5 minutes. |
| Token/model cost | OpenHands run/conversation usage if exposed; otherwise model profile plus billing estimate. | Sidekick should not materially exceed control unless readability improves. |
| Success rate | PR opened, correct files changed, tests added, Jira updated, no unnecessary human stop. | 2/2 for demo-ready path. |
| Readability | Score conversation with `skills/sdlc-context-sidekick/references/brief-format.md`. | Sidekick should score 4 or 5. |
| Customer explainability | Can a viewer identify ticket, docs, logs, repo files, tests, PR, and human gate quickly? | Yes within 30 seconds. |

## Decision Rule

Use the sidekick in the live demo only if it consistently keeps time to PR within
the five-minute window and makes the conversation easier to explain. Otherwise,
keep it as an optional architecture slide and use the current Jira-to-PR path for
the live run.

## First Live A/B Result

Date: 2026-06-30 UTC

| Variant | Jira | Automation run | Conversation | PR | Time to PR | Completion time | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Control | `KAN-29` | `09bf9e2a-26a7-4b9f-a1ec-0d59cd30cb55` | `https://app.replicated.rajistics.com/conversations/2bfaf1bb-2ce7-4fa9-8b6a-14bad473f807` | `https://github.com/rajshah4/sdlc-automation-github-demo/pull/39` | 4.88 min | 6.26 min | PR opened inside the five-minute target; run completed successfully. |
| Sidekick | `KAN-30` | `cbaa0fc7-a671-4676-be23-3294e01c888d` | `https://app.replicated.rajistics.com/conversations/9b361dd2-f2ac-4f24-afdb-b48b2d5f8b10` | `https://github.com/rajshah4/sdlc-automation-github-demo/pull/40` | 6.19 min | 7.84 min | PR opened successfully, but missed the five-minute target. |

Readability judgment from PR bodies:

- Control PR is clear and direct, but the context discovery path is mostly folded into the implementation narrative.
- Sidekick PR foregrounds evidence waypoints more clearly and is easier to explain as architecture, but it costs live-demo time.

Initial decision: keep the single-agent Jira-to-PR path for the main five-minute
demo. Present the sidekick as an optional architecture experiment or use it only
when the demo slot can tolerate roughly two extra minutes.

Cleanup: after the first live A/B run, the temporary experiment automations were
disabled and the normal Enterprise Jira automation was re-enabled.
