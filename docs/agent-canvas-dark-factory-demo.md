# Agent Canvas Dark Factory Demo

This is the delegated-conversation version of the GitHub-native SDLC Automation
Demo in `rajshah4/sdlc-automation-github-demo`.

The existing GitHub-native demo uses GitHub labels as the work-cell trigger
boundary. This version keeps one parent Agent Canvas conversation in front of
the operator and lets that parent delegate the lifecycle to child
conversations. Labels can be passed along as descriptive historical context, but
they are not the trigger mechanism, gate, or sequencing control for this Canvas
demo.

## What The Audience Sees

1. The operator starts one Canvas conversation: the supervisor.
2. The supervisor runs the repo-local orchestrator, which creates a run
   manifest and delegates story-to-PR.
3. The story-to-PR child creates OpenSpec-style artifacts, implements the small
   Petstore change, runs validation, and opens or prepares a draft PR.
4. The supervisor delegates code review and QA as separate conversations.
5. The supervisor writes one lifecycle report with every child conversation
   link, artifact path, gate result, and human next step.

## Why This Version Matters

The GitHub-label demo proves event-driven automation. The Canvas version proves
orchestration: one parent agent can supervise a lifecycle while specialized
children perform bounded work and report back. It makes delegation visible
without using GitHub labels as the control plane.

## Run It Locally

Prerequisites:

- Agent Canvas is running locally.
- `http://localhost:8000/server_info` returns Agent Server `1.31.0` or newer.
- `$HOME/.openhands/agent-canvas/api-key.txt` exists, or one of
  `SESSION_API_KEY`, `OH_SESSION_API_KEYS_0`, or `LOCAL_BACKEND_API_KEY` is set.
- The repo is available locally.

Start the supervisor:

```bash
python3 scripts/start_agent_canvas_factory.py \
  --repo . \
  --repo-slug rajshah4/sdlc-automation-github-demo
```

Optional custom story:

```bash
python3 scripts/start_agent_canvas_factory.py \
  --repo . \
  --repo-slug rajshah4/sdlc-automation-github-demo \
  --issue-number 214 \
  --request-title "Filter pets by max adoption fee" \
  --request-body "Families need to filter available pets by maximum adoption fee."
```

Optional separate code-review model profile:

```bash
python3 scripts/start_agent_canvas_factory.py \
  --repo . \
  --repo-slug rajshah4/sdlc-automation-github-demo \
  --code-review-profile Minimax
```

Optional Playwright QA stress run:

```bash
python3 scripts/start_agent_canvas_factory.py \
  --repo . \
  --repo-slug rajshah4/sdlc-automation-github-demo \
  --require-playwright-qa \
  --playwright-node-path /path/to/node_modules
```

The command prints the parent conversation link. Open that link in Canvas and
watch the supervisor delegate.

This local Canvas path does not require registering a new OpenHands automation.
The input can come from a GitHub issue, PR, or human-provided story; the operator
passes the issue number, title, and body into the parent Canvas launcher.

## Run Artifacts

Each run writes artifacts to:

```text
factory_runs/<run-id>/
```

Expected files:

| File | Meaning |
| --- | --- |
| `parent.conversation.json` | Parent supervisor conversation id and UI/API links. |
| `manifest.md` | Supervisor-created run manifest. |
| `children.json` | Child conversation ids and UI/API links. |
| `story-to-pr.*` | Build conversation metadata and report. |
| `code-review.*` | Review conversation metadata and report. |
| `qa.*` | QA conversation metadata and evidence summary. |
| `lifecycle-report.md` | Final parent report for the live demo. |

## Demo Script

Narrative:

```text
"The old version used GitHub tags as separate work-cell triggers. In this
version, I start one Canvas conversation. Labels are just background context,
not the trigger. That supervisor does not code
everything itself. It creates child conversations, gives each one a bounded
contract, waits for evidence, and decides whether the next human gate is safe."
```

Callouts:

- Parent conversation is the visible control plane.
- Children are independent conversations with their own tools, final responses,
  and Canvas links.
- The parent does not hand-roll Canvas credentials or settings payloads; the
  repo-local helper handles encrypted settings in memory.
- Code review can use a different Agent Canvas profile via
  `--code-review-profile`.
- QA can be forced to run Playwright UI evidence via `--require-playwright-qa`.
- The child prompts are self-contained and auditable in the repo.
- GitHub remains the system of record for PRs and comments when credentials are
  available.
- Human authority stays at scope, review, merge, deploy, and remediation gates.
- The existing GitHub-label automation demo remains intact; this Canvas demo is
  an additive orchestration variant.
- Jira and Rajistics automation are deliberately out of scope for this phase and
  should be built as a separate follow-up once this Canvas demo is stable.

## Fallbacks

- If GitHub credentials are unavailable, the build child leaves a local branch
  or diff and reports the missing capability at a safe level.
- If browser tooling is unavailable, QA uses deterministic API/static UI checks
  and marks the result as fallback evidence.
- If any child hits `needs-human`, the supervisor records the blocker and stops
  before unsafe work.
