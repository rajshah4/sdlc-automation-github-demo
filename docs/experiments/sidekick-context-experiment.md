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

Conversation API summaries:

| Variant | Conversation events | Event timeline | Model profile | Reported cost | Prompt tokens | Completion tokens |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| Control | 147 | 5.51 min | `Bedrock-Claude-Sonnet-4-5` | $1.4807 | 2,533,288 | 18,297 |
| Sidekick | 182 | 6.93 min | `Bedrock-Claude-Sonnet-4-5` | $1.8158 | 3,391,164 | 23,326 |

The sidekick run added 35 events, 1.42 minutes of conversation timeline, and
about $0.335 of reported model cost in this run. That is a meaningful live-demo
tax unless the clearer context story is the point of the demo segment.

Readability judgment from PR bodies:

- Control PR is clear and direct, but the context discovery path is mostly folded into the implementation narrative.
- Sidekick PR foregrounds evidence waypoints more clearly and is easier to explain as architecture, but it costs live-demo time.

Initial decision: keep the single-agent Jira-to-PR path for the main five-minute
demo. Present the sidekick as an optional architecture experiment or use it only
when the demo slot can tolerate roughly two extra minutes.

Cleanup: after the first live A/B run, the temporary experiment automations were
disabled and the normal Enterprise Jira automation was re-enabled.

## What We Learned From The First Sidekick Run

The first sidekick package was not a true multi-agent architecture. It was an
inline prompt-preset workflow: the main Jira-to-PR conversation loaded the
context sidekick skill, generated a brief, then continued into the story skill.
That made the evidence path clearer, but it also meant the main agent still
waited for the scout work and then reread parts of the same docs/logs/code.

Observed conversation behavior:

- The sidekick launch was not visually distinct enough. A viewer could see the
  context brief, but not separate docs/logs/repo agents starting.
- The main agent loaded `skills/sdlc-context-sidekick/SKILL.md` and
  `skills/sdlc-story/SKILL.md` in the same early phase, so the scout was not
  kept minimal.
- After the helper produced the brief, the main agent still reread docs, logs,
  app code, and tests. Some duplication is useful before editing, but the run did
  more broad context gathering than the demo needs.
- Late Jira comment attempts added noise and time after the PR was already open.
  For the timing experiment, Jira comments should be either known-good or skipped
  in favor of the PR link/artifact trail.

## Sidekick V2

V2 should compare three approaches instead of treating all sidekick designs as
one thing:

| Approach | What launches | Expected benefit | Risk |
| --- | --- | --- | --- |
| Current single-agent | One implementation conversation. | Fastest live demo path. | Context search is less explicit. |
| Deterministic fan-out scouts | One script starts `docs-scout`, `logs-scout`, and `repo-scout` concurrently. | Clear launch markers, near-zero model cost, minimal context loading. | It is not a true child-agent architecture. |
| True side-agent scouts | Three read-only child conversations, ideally on cheaper profiles, return briefs to the main conversation. | Best architecture story and model-routing demo. | More orchestration, more elapsed time, and possible token overhead. |

The repo now includes the deterministic baseline:

```bash
python3 skills/sdlc-context-sidekick/scripts/fanout_context_scouts.py \
  --jira-key KAN-123 \
  --title "Available pets list still shows unavailable animals" \
  --body "Customers say the available pets page includes animals that should not be adoptable."
```

This prints `CONTEXT_SCOUT_FANOUT`, separate `SCOUT_RESULT` blocks, and the
aggregate `CONTEXT_BRIEF`. It intentionally does not search workflow skills, so
the scout does not load the implementation playbook before the main agent needs
it.

Example local runtime for the deterministic fan-out on the standard sparse bug:
about 0.004 seconds on a laptop, with docs/logs/repo launches visible in the
output and no model call.

## True Side-Agent Design

For the actual sidekick architecture, use a custom orchestration automation
rather than a single prompt preset:

1. Main orchestrator receives the Jira webhook and extracts only ticket key,
   summary, description, labels, and URL.
2. It starts three child conversations at the same time:
   - `docs-scout`: read-only search of `README.md`, `AGENTS.md`, `docs/wiki/`,
     and `openspec/project.md`.
   - `logs-scout`: read-only search of `docs/logs/`.
   - `repo-scout`: read-only search of `app/` and `tests/`.
3. Each child conversation uses a cheap profile when available and has a strict
   output contract: paths checked, snippets, confidence, and missing info. No
   skills, no edits, no Jira/GitHub mutations.
4. The orchestrator waits for a short barrier, such as 45 seconds, then starts
   the main Sonnet Jira-to-PR conversation with whatever briefs are available.
5. The main conversation loads `skills/sdlc-story/SKILL.md`, inspects likely
   implementation/test files, makes the change, runs tests, opens the PR, and
   adds `openhands-qa`.

This makes the demo line easy to explain: "The main agent owns the PR. The small
side agents only search docs, logs, and repo context, and we cap them so they
cannot wander."

Live API support checked on the Rajistics instance:

- `POST /api/v1/app-conversations` supports `parent_conversation_id`, so side
  scouts can appear as child conversations under a parent run.
- It supports `llm_model`, which is enough for a first pass at cheaper scout
  models if saved profiles are not needed.
- It supports `selected_repository` and `selected_branch`, which lets the scouts
  target the demo repo and branch.
- It supports `plugins`; use an empty list or omit plugins for scout
  conversations, then verify whether repo-local skills still auto-load in the
  sandbox. The scout prompt must explicitly say "do not load workflow skills."
- It does not expose a simple `max_iterations` field in the app conversation
  start schema, so the scout prompts need hard tool budgets and the orchestrator
  should enforce timeout/cancellation externally.

Recommended scout prompts should be tiny. For example:

```text
You are docs-scout. Read only. Search README.md, AGENTS.md, docs/wiki/, and
openspec/project.md for this Jira symptom. Do not edit files, load workflow
skills, comment on Jira/GitHub, or inspect app code. Use at most four searches
and return SCOUT_RESULT docs-scout with files checked, snippets, confidence, and
missing info.
```

## Measurement

Use the conversation event API to measure elapsed time and usage after each run:

```bash
python3 scripts/summarize_openhands_conversation.py \
  9b361dd2-f2ac-4f24-afdb-b48b2d5f8b10 \
  --env-file /path/to/local/.env
```

Compare:

- Time to PR.
- Total run completion time.
- `accumulated_cost` and token counters by model profile.
- Number of broad file reads before first edit.
- Whether a customer can identify the context launches in under 30 seconds.

Do not use true child-agent sidekicks in the five-minute live demo until they
beat or match the deterministic fan-out baseline on elapsed time and readability.
