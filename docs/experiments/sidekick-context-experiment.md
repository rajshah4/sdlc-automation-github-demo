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
| Visible Sidekick V2 | `sidekick-v2` | `automations/jira/jira-to-story-sidekick-v2/` | Starts visible docs/logs/repo scout conversations, then starts the main Jira-to-PR implementation conversation and the separate QA agent. |

The normal Jira automation should exclude `control-experiment`,
`sidekick-experiment`, and `sidekick-v2`, so each ticket wakes only one Jira
implementation automation. The `sidekick-v2` path can stay enabled in normal
demo posture because it is gated by the explicit Jira label.

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

## Sidekick V2 Manual Launcher Result

Date: 2026-06-30 UTC

This run used the new API launcher in `scripts/launch_sidekick_v2.py` to prove
the visible side-agent architecture. The Jira ticket was created first, then the
launcher started a parent conversation, three scout child conversations, and the
main implementation child conversation. The regular broad Jira automation was
temporarily disabled during the test so it would not duplicate the work.

Important caveat: this proves the architecture and timing, but it is not yet a
dedicated Jira webhook automation. The next step is packaging this launcher as
the `sidekick-v2` Jira automation path.

| Role | Link | Result | Cost |
| --- | --- | --- | ---: |
| Jira ticket | `https://rajiv-shah.atlassian.net/browse/KAN-39` | Sparse bug ticket: available pets list shows unavailable animals. | n/a |
| Parent orchestrator | `https://app.replicated.rajistics.com/conversations/64befb59e4de49e0999d36a8fff538e9` | Grouped the visible child conversations. | $0.0625 |
| `docs-scout` | `https://app.replicated.rajistics.com/conversations/f00b4d70f7794a1a9f99c81d60aa2135` | Found product rules in `AGENTS.md` and `docs/wiki/petstore-catalog-availability.md`. | $0.0804 |
| `logs-scout` | `https://app.replicated.rajistics.com/conversations/015f205b6835402e987a0e42a9295f05` | Found `PENDING_PET_VISIBLE` evidence in `docs/logs/pending-pet-visible.ndjson`. | $0.0846 |
| `repo-scout` | `https://app.replicated.rajistics.com/conversations/f39ad87fe32447ad99889680feec0a23` | Found likely implementation/test files in `app/petstore_app/catalog.py` and `app/tests/test_pet_catalog.py`. | $0.1151 |
| Main implementation | `https://app.replicated.rajistics.com/conversations/e307dfbd8a624947bccac88ffa3d495f` | Opened PR #47 and added `openhands-qa`. | $0.6928 |
| PR | `https://github.com/rajshah4/sdlc-automation-github-demo/pull/47` | `[KAN-39] Fix available pets filter to exclude pending pets`. | n/a |
| QA automation | `https://app.replicated.rajistics.com/conversations/c928b6c1-9cfe-4520-9cc5-1f394105a5bd` | Posted passing QA report on PR #47. | $1.2641 |
| QA comment | `https://github.com/rajshah4/sdlc-automation-github-demo/pull/47#issuecomment-4839777514` | Validated backend fix, regression tests, and UI fallback evidence. | n/a |

Timing from the live run:

| Segment | Start | End | Duration |
| --- | --- | --- | ---: |
| Parent/scout launch to PR opened | 03:59:07 | 04:03:12 | ~4.1 min |
| Scouts launched to all scouts finished | 03:59:17 | 04:00:41 | ~1.4 min |
| Main implementation child to PR opened | 04:00:40 | 04:03:12 | ~2.5 min |
| Main implementation child to finished | 04:00:40 | 04:03:35 | ~2.9 min |
| QA handoff started | 04:03:22 | n/a | not timed; separate QA automation kicked off |

Observed improvements:

- The UI now clearly shows separate side-agent conversations instead of one
  inline `CONTEXT_BRIEF` inside the main conversation.
- The side-agent work fit inside the five-minute PR target when paired with the
  main implementation child: PR opened in about 4.1 minutes from parent launch.
- The separate QA agent worked as the second post-PR conversation and posted a
  readable report. QA timing is not part of the sidekick speed target.

Observed tradeoffs:

- `POST /api/v1/app-conversations` accepts concrete LiteLLM model strings, not
  saved profile names. Passing `Bedrock-Claude-Sonnet-4-5-fast` directly caused
  `LLMBadRequestError`; the launcher now defaults to
  `litellm_proxy/us.anthropic.claude-sonnet-4-5-20250929-v1:0`.
- Fresh app-conversation reads can briefly return `BearerTokenError`, and event
  reads can return 429 when several scouts finish together. The launcher now
  retries those transient reads.
- Using `selected_repository` makes the conversations easy to launch and visible
  in the UI, but scouts still load substantial repo context. The three scouts
  plus parent cost about $0.34 before the main implementation. For a cost demo,
  test a manual shallow-clone scout path or a deterministic scout script.
- The parent orchestrator currently consumes model tokens even though it is
  intended as a grouping node. A custom automation package should avoid spending
  LLM tokens for the parent when possible.

Decision after KAN-39: the sidekick architecture is demo-worthy if the goal is to
show multi-agent orchestration. The normal single-agent Jira-to-PR path is still
simpler for a pure speed demo, but Sidekick V2 is within the five-minute
PR-opening target when the launcher starts directly and tells the customer story
much better.

## Sidekick V2 Webhook Result

Date: 2026-06-30 UTC

This run proves the full event path: Jira webhook to OpenHands automation,
visible sidekick scout conversations, main implementation conversation, GitHub
PR, then the separate GitHub QA conversation.

| Role | Link | Result | Cost |
| --- | --- | --- | ---: |
| Jira ticket | `https://rajiv-shah.atlassian.net/browse/KAN-41` | Sparse bug ticket labeled `sidekick-v2`. | n/a |
| Jira launcher automation | `https://app.replicated.rajistics.com/conversations/34bfd883-8520-4276-9891-87ab9c679bf8` | Prompt-preset automation cloned the repo and ran `scripts/launch_sidekick_v2.py`. | $0.3642 |
| Parent orchestrator | `https://app.replicated.rajistics.com/conversations/4a96f19d97354f2f9acaf12f82341a1c` | Grouped the visible side-agent child conversations. | $0.3453 |
| `logs-scout` | `https://app.replicated.rajistics.com/conversations/0b1436fec56a4411b011477d57c537ad` | Found log evidence for pending pets leaking into available listings. | $0.2239 |
| `docs-scout` | `https://app.replicated.rajistics.com/conversations/5813c3c4970f4c4f9d62264791e43022` | Found product availability guidance in repo docs/wiki context. | $0.2493 |
| `repo-scout` | `https://app.replicated.rajistics.com/conversations/897a9a5c6cb14765982d381fa4a7551d` | Identified the catalog implementation and regression-test files. | $0.2576 |
| Main implementation | `https://app.replicated.rajistics.com/conversations/f5f758a453a247cb9146f088d61548d0` | Opened PR #48 and added `openhands-qa`. | $1.1110 |
| PR | `https://github.com/rajshah4/sdlc-automation-github-demo/pull/48` | `Fix KAN-41: Pending pets showing in available pets list`. | n/a |
| QA automation | `https://app.replicated.rajistics.com/conversations/3fa9264a-fab9-4381-a37a-fc5e0f7bee1a` | Posted a passing QA report on PR #48. | $0.9879 |
| QA comment | `https://github.com/rajshah4/sdlc-automation-github-demo/pull/48#issuecomment-4839894899` | Reported PASS with backend tests and static UI validation; Playwright unavailable in the runtime. | n/a |

Timing from the webhook-triggered run:

| Segment | Start | End | Duration |
| --- | --- | --- | ---: |
| Jira automation run created to PR opened | 04:22:48 | 04:30:08 | ~7.3 min |
| Jira automation run total | 04:22:48 | 04:31:09 | ~8.3 min |
| Visible sidekick tree to PR opened | 04:24:43 | 04:30:08 | ~5.4 min |
| Scout conversation timelines | n/a | n/a | ~1.7-2.1 min each |
| Main implementation child to PR opened | 04:25:36 | 04:30:08 | ~4.5 min |
| Main implementation child total | n/a | n/a | ~5.1 min |
| QA handoff started | 04:30:15 | n/a | not timed; separate QA automation kicked off |

Viewer-facing step map:

| Step | Conversation | What to point out | Timing cue |
| --- | --- | --- | --- |
| Step 0 | Jira launcher automation | Jira webhook event woke OpenHands and launched the visible sidekick run. | This is prompt-preset overhead in the current design. |
| Step 1 | Parent orchestrator | Groups the child sidekick conversations. | Parent/scout launch began around 04:24:43. |
| Step 2A | Docs scout | Searches product/wiki context only. | Scouts finish in roughly 1.7-2.1 minutes. |
| Step 2B | Logs scout | Searches log evidence only. | This makes the log context visible without editing. |
| Step 2C | Repo scout | Searches implementation/test candidates only. | This makes repo discovery visible before coding. |
| Step 3 | Main implementation | Uses scout links/briefs, fixes code, adds tests, opens PR, adds `openhands-qa`. | Main child to PR was about 4.5 minutes. |
| Step 4 | GitHub QA automation | Separate QA conversation validates and comments; humans still review/merge. | Not timed; show that `openhands-qa` starts the second conversation. |

What this proves:

- The customer-visible architecture now exists: Jira starts a launcher, the
  launcher starts separate side-agent conversations for docs/logs/repo context,
  the main implementation agent owns the code and PR, and QA is a separate
  post-PR conversation.
- The scouts are easy to point to in the UI and are no longer just a long prompt
  section inside the main implementation conversation.
- The GitHub QA handoff is working from the PR label and remains human-reviewed:
  QA reports evidence, but does not approve, merge, or deploy.
- Conversation readability is now part of the design: the launcher is Step 0,
  the parent is Step 1, the scouts are Step 2A/2B/2C, the main implementation is
  Step 3, and QA is Step 4.
- The current live v2 registration for that step-labeled path is
  `3e19b338-b282-45c3-9dca-dcf5d3535590`. This registration keeps the launcher
  and main implementation on Sonnet fast and runs the read-only sidekick scouts
  on Haiku.

### QA And UI Evidence

For this experiment, the speed metric stops at PR creation. QA only needs to
prove the handoff: the main implementation adds `openhands-qa`, and the
Enterprise GitHub QA automation starts a separate run/conversation and reports
back to the PR when ready.

Use the prebuilt UI/Playwright example in `docs/ui-playwright-example.md` when a
customer wants to see browser evidence. The live Jira bug can stay a reliable
non-UI path, while PR #6 shows the richer UI flow with Playwright, screenshots,
GIF artifacts, and a QA comment.

What still needs optimization:

- The prompt-preset launcher costs time and tokens because it starts a full
  agent just to run the launcher script. In this run, that overhead pushed the
  true Jira-webhook path past the five-minute target.
- After this run, the launcher was updated to start the main implementation
  after a 90-second scout-result barrier instead of waiting for every scout as a
  hard gate. Completed briefs are passed into the main prompt; still-running
  scouts are passed as links and are collected in the final JSON summary.
- The launcher JSON now includes a `timing_summary` object so the demo can call
  out parent readiness, scout duration, main implementation time, and QA handoff
  without hand-calculating timestamps. QA handoff is a visibility check, not a
  timing goal.
- KAN-42 then showed an infrastructure failure mode: the run timed out with
  `Sandbox not available` while `sandbox_grouping_strategy` was `NO_GROUPING`.
  Switching the org setting to `FEWEST_CONVERSATIONS` allowed KAN-43 to get a
  sandbox.
- KAN-43 exposed a prompt dependency rather than a sidekick code problem: the old
  registered v2 prompt still called the launcher with `--fetch-jira`, but the
  automation runtime did not provide `JIRA_API_BASE_URL`. The corrected v2 prompt
  now passes Jira key, summary, and description directly from the webhook payload
  and avoids that extra Jira API env dependency.
- KAN-44 was created after registering the corrected v2 automation. The run
  completed after roughly 15.3 minutes with no `conversation_id`, no error
  detail, and no PR. During the run, the automation runs endpoint also returned
  HTTP 503 `Service Unavailable` / `no available server`. Do not use KAN-44 as a
  timing result; it is an automation-service/prompt-preset blocker.
- KAN-45 and KAN-46 tested the Haiku-scout registration with UI-scoped Jira
  tickets. Haiku was not reached: the launcher failed before creating scout
  children because the app-conversation control API returned
  `HTTP 401: BearerTokenError` for child start-task reads. KAN-46 also showed
  intermittent automation run-list `401`, `502`, and `503` responses. The next
  optimization step is to fix app-conversation API auth/availability before
  re-measuring Haiku scout timing.
- KAN-47 confirmed a second blocker after the API key refresh: the webhook run
  fired, but produced a single erroring Sonnet conversation instead of the Step
  1/2/3 sidekick tree. Direct local launcher retries with Haiku scouts then
  failed before model execution because `selected_repository` child starts
  returned `Git provider authentication issue when getting remote URL` for both
  owner/repo and full GitHub URL forms. Haiku timing is therefore still
  unmeasured.
- Follow-up instance checks showed app-server auth works with
  `X-Access-Token: <OPENHANDS_API_KEY_ORG>`, while automation APIs require
  `Authorization: Bearer <OPENHANDS_API_KEY_ORG>`. Do not send both headers
  together because app auth can prioritize a stale `Authorization` header. The
  remaining sidekick blocker is the GitHub provider token for user
  `9328d634-bd0d-4125-be44-a71b18548a58`: repo search returns
  `401 Invalid github token`. Re-auth GitHub for that API-key owner user, rerun
  the repo search preflight, then re-measure Haiku scout timing.
- The parent/scout conversations still pay repo startup/context cost because
  they use `selected_repository`. That makes the UI simple and reliable, but it
  is not the cheapest sidekick design.
- Saved OpenHands profile names work for automations, but app-conversation child
  starts need the concrete LiteLLM model string. The launcher uses
  `litellm_proxy/us.anthropic.claude-sonnet-4-5-20250929-v1:0` directly.

Current recommendation:

- Use `sidekick-v2` for the impressive customer demo when the point is
  multi-agent orchestration and explainability.
- Use the normal Jira-to-PR path for the tightest speed demo.
- If Sidekick V2 must stay under five minutes from Jira ticket creation, convert
  `jira-to-story-sidekick-v2` from a prompt-preset launcher into a deterministic
  custom automation that calls `scripts/launch_sidekick_v2.py` directly and skips
  the extra launcher-agent conversation.
