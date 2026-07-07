# SDLC Automation Demo for GitHub

**Sparse GitHub bug -> OpenHands automation -> spec, code, tests, review, and evidence back in GitHub.**

This repo is a customer-facing GitHub-native SDLC Automation Demo. It shows how
OpenHands can turn lightweight GitHub signals into controlled engineering work
while humans keep authority through issues, PRs, labels, comments, reviews, and
merge decisions.

The target app is intentionally small: a Petstore catalog and adoption service.
That keeps the demo easy to follow while still producing real artifacts: code
diffs, tests, UI checks, review comments, and PRs.

This repo is GitHub-first: labels are the automation boundary, GitHub remains
the system of record, and OpenHands does the agent work only when a human asks
for it.

## What Problem This Solves

Teams want agentic SDLC automation, but they do not want a parallel workflow
where requests disappear into a black box. The common bottleneck is:

1. A bug or product request starts as a sparse issue or comment.
2. Engineers need to understand the issue, find the right code, implement a fix, add tests, and preserve review judgment.
3. Demo operators need a path that is easy to explain, repeat, and inspect.

This repo shows two ways to run that loop:

- **Step-by-Step Control:** a human applies labels, and each label triggers one
  bounded OpenHands automation.
- **Complete Automation:** one request starts a supervisor conversation, which
  delegates implementation, review, and QA to child conversations.

## Choose Your Demo Path

| Goal | Use this path | Starts from | Example PR |
| --- | --- | --- | --- |
| **Step-by-Step Control** | Human-gated labels and triggers | GitHub issue or PR label | [PR #53](https://github.com/rajshah4/sdlc-automation-github-demo/pull/53) |
| **Complete Automation: OpenHands Enterprise/Cloud** | Parent supervisor conversation with child conversations | Jira Task event | [PR #94](https://github.com/rajshah4/sdlc-automation-github-demo/pull/94) |
| **Complete Automation: Agent Canvas** | Parent Canvas conversation with delegated child conversations | Agent Canvas supervisor prompt | [PR #89](https://github.com/rajshah4/sdlc-automation-github-demo/pull/89) |

## Two Ways To Run The SDLC Loop

**Step-by-Step Control** is best when humans want review or approval at each
phase. A person applies labels such as `openhands-build`,
`openhands-review`, and `openhands-qa`; each label starts one bounded
automation. This is the current runnable demo on `main`.

**Complete Automation** is best when one request should drive the whole
lifecycle. A parent supervisor conversation stays active, creates specialized
child conversations, waits for their final outputs, writes a lifecycle report,
and posts the summary back to the system of record.

```text
Request
  -> parent supervisor conversation
    -> child: story-to-PR
    -> child: code-review
    -> child: QA
  -> lifecycle report
  -> Jira or demo summary
```

## Step-by-Step Control: The Work Cells

| Work cell | Trigger | What OpenHands does | What humans control |
| --- | --- | --- | --- |
| **Context Scout** | Apply `openhands-context` to a sparse issue | Navigates existing business wiki/docs, repo context, logs, prior reports, and previous OpenHands run evidence before expensive model work | Whether to proceed to build, review, or QA work |
| **Bug to PR** | Apply `openhands-build` to a sparse bug issue | Clarifies the bug, checks repo-local docs and evidence, writes OpenSpec-style change artifacts, implements the fix, runs tests, and opens a PR | Scope, review, approval, and merge |
| **Code Review** | Apply `openhands-review` to a PR | Reads the diff, checks risk areas, and posts review findings as a PR comment | Which findings block the PR |
| **Automated QA** | Apply `openhands-qa` to a PR | Builds or updates test coverage, runs deterministic checks, and includes UI test evidence where applicable | Test acceptance and merge readiness |

## Complete Automation: Parent-Child Factory

The parent-child factory uses the same work-cell idea, but removes the need for
a human to trigger each phase. The implementation is runtime-specific:

| Runtime | Parent creates | Child conversations do | Replication pieces |
| --- | --- | --- | --- |
| **OpenHands Enterprise/Cloud** | A supervisor conversation from an automation event | Story-to-PR, code review, and QA in separate OpenHands app conversations | Automation prompt, parent orchestrator helper, app-conversation API helper, child prompts, reusable delegated-factory skill |
| **Agent Canvas** | A parent Canvas conversation from a supervisor prompt | Story-to-PR, code review, and QA in delegated Canvas conversations | Canvas supervisor prompt, Canvas delegate helper, child prompts, reusable delegated-factory skill |

The core orchestration rule is the same in both paths: one parent conversation
is the control plane, child conversations own bounded work, and final responses
are treated as small contracts that the parent can summarize and gate.

The current working branch for this pattern is
[`feature/canvas-issue-101-max-adoption-fee-filter`](https://github.com/rajshah4/sdlc-automation-github-demo/tree/feature/canvas-issue-101-max-adoption-fee-filter).
PR #86 carries the concrete files and the live-tested Replicated Jira flow.

## What You'll See

- A low-cost context scout shows which business wiki/docs, repo context, logs,
  prior evidence, and previous OpenHands runs can be reused before expensive
  model work.
- A sparse bug issue becomes a PR with an implementation branch and visible OpenSpec-style proposal/spec/design/task artifacts.
- A PR receives an automated review comment rather than a silent background score.
- QA output lands on the PR with concrete test files and command results. The repo also includes a prebuilt Playwright browser-evidence example with screenshot, GIF, video, and report generation.
- The complete automation pattern shows how a parent conversation can keep the
  whole SDLC lifecycle visible while delegating specialized work to child
  conversations.
- Status labels such as `openhands:in-progress`, `openhands:needs-human`, and
  `openhands:done` make the automation state visible without leaving GitHub.

## How It's Built

This repo is intentionally composed from OpenHands platform features and
repo-local knowledge, not a custom agent runtime.

| Capability | Where it lives | Why it matters |
| --- | --- | --- |
| OpenHands automations | `automations/github/`, `automations/jira/` | Event-triggered automations configured in OpenHands. GitHub labels and Jira webhooks start the work; GitHub and Jira remain the systems of record. |
| Repo-local skills | `skills/` | Reusable skills encode context reuse, story/spec, QA, and code-review behavior with scripts and references that customers can inspect. |
| Delegated factory pattern | PR #86 | Adds the parent-child supervisor path for OpenHands Enterprise/Cloud and Agent Canvas without replacing the label-driven automations. |
| OpenSpec-style artifacts | `openspec/` | Repo-local context and generated change folders keep request, proposal, spec delta, design, and tasks version controlled. |
| Deterministic scripts | `scripts/` | Preflight, label setup, fixture simulation, and Petstore checks run before broader model reasoning where possible. |
| GitHub templates and labels | `.github/` | Issues, PRs, and labels define the human approval boundaries. |
| Petstore app | `app/` | A small API/UI surface gives the automations realistic code and tests to work on. |
| Playwright UI evidence | `app/web/tests/` | Browser QA example that records video, creates a GIF preview, captures a screenshot, and writes a report for PR evidence when Playwright is available. |

Cost and security are part of the demo design: event-driven labels avoid
unnecessary LLM calls, preflight scripts catch configuration issues without
using a model, different LLM profiles can be used for scouting/coding/review/QA, and
secrets stay in the OpenHands secret store or local `.env`, never in the repo.

## Fast Local Validation

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_context.json
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
```

## Register OpenHands Automations

OpenHands Automations should be registered with the prompt preset API. The
GitHub package specs live under `automations/github/`; the normal Jira package
spec lives under `automations/jira/jira-to-story/`; the visible sidekick demo
package lives under `automations/jira/jira-to-story-sidekick-v2/`.

Dry-run the registration payloads:

```bash
python3 scripts/register_github_automations.py --dry-run
python3 scripts/register_jira_automations.py --dry-run
```

Apply registration when `OPENHANDS_HOST_GITHUB`, an OpenHands API key such as `OPENHANDS_API_KEY_GITHUB` or `OPENHANDS_API_KEY_ORG`, `GITHUB_DEMO_REPOSITORY`, and `GITHUB_DEMO_REPO_URL` are set:

```bash
python3 scripts/register_github_automations.py --apply
```

Register Jira packages with:

```bash
python3 scripts/register_jira_automations.py --apply
```

For a fast live demo, keep `jira-to-story` enabled and `jira-to-story-sidekick-v2`
disabled. For the visible multi-conversation demo, switch those states and create
the Jira Task with label `sidekick-v2`.

No secrets belong in this repo. Store OpenHands, GitHub, Jira, and Slack credentials in the OpenHands secret store or a local `.env` excluded by `.gitignore`.

## Demo Docs

- [GitHub demo walkthrough](docs/github-demo-walkthrough.md)
- [Enterprise memory and cost demo](docs/enterprise-memory-cost-demo.md)
- [Setup checklist](docs/setup-checklist.md)
- [Demo upgrade backlog](docs/demo-upgrades.md)
- [Prebuilt UI and Playwright example](docs/ui-playwright-example.md)
