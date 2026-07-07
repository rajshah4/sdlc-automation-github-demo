# SDLC Automation Demo for GitHub

**Sparse GitHub request -> OpenHands automation -> spec, code, tests, review, and incident evidence back in GitHub.**

This repo is a customer-facing GitHub-native SDLC Automation Demo. It shows how
OpenHands can turn lightweight GitHub signals into controlled engineering work
while humans keep authority through issues, PRs, labels, comments, reviews, and
merge decisions.

The target app is intentionally small: a Petstore catalog and adoption service.
That keeps the demo easy to follow while still producing real artifacts: code
diffs, tests, UI checks, review comments, incident notes, and PRs.

The Azure DevOps demo remains preserved in its original repository. This repo is
GitHub-first: labels are the automation boundary, GitHub remains the system of
record, and OpenHands does the agent work only when a human asks for it.

## What Problem This Solves

Teams want agentic SDLC automation, but they do not want a parallel workflow
where requests disappear into a black box. The common bottleneck is:

1. A product request starts as a sparse issue or comment.
2. Engineers need a spec, implementation, tests, review, and rollout judgment.
3. Incident follow-up needs logs, evidence, and safe remediation without giving
   an agent unlimited production authority.

The default demo keeps that loop inside GitHub. A human applies a label,
OpenHands runs one bounded automation, then posts evidence back where the team
already works. The repo also includes opt-in delegated paths for teams that want
one request to run the whole SDLC loop through a visible supervisor
conversation.

## Choose Your Demo Path

| Goal | Use this path | Starts from | Start here |
| --- | --- | --- | --- |
| **Step-by-Step Control** | Human-gated labels and triggers | GitHub issue or PR label | [GitHub demo walkthrough](docs/github-demo-walkthrough.md) |
| **Complete Automation: OpenHands Enterprise/Cloud** | Parent supervisor conversation with child conversations | Jira Task event | [Replicated Jira delegated factory demo](docs/replicated-jira-delegated-factory-demo.md) |
| **Complete Automation: Agent Canvas** | Parent Canvas conversation with delegated child conversations | Agent Canvas supervisor prompt | [Agent Canvas delegated factory](agent-canvas/README.md) |

## Two Ways To Run The SDLC Loop

**Step-by-Step Control** is best when humans want review or approval at each
phase. A person applies labels such as `openhands-build`,
`openhands-review`, and `openhands-qa`; each label starts one bounded
automation.

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

## Step-by-Step Control: The Four Work Cells

| Work cell | Trigger | What OpenHands does | What humans control |
| --- | --- | --- | --- |
| **Story to PR** | Apply `openhands-build` to a sparse issue | Clarifies the request, writes OpenSpec-style change artifacts, implements the change, runs tests, and opens a PR | Scope, review, approval, and merge |
| **Code Review** | Apply `openhands-review` to a PR | Reads the diff, checks risk areas, and posts review findings as a PR comment | Which findings block the PR |
| **Automated QA** | Apply `openhands-qa` to a PR | Builds or updates test coverage, runs deterministic checks, and includes UI test evidence where applicable | Test acceptance and merge readiness |
| **SRE Incident** | Apply `openhands-incident` to an incident issue | Gathers Cloud Run / Cloud Logging evidence, diagnoses likely cause, and proposes a fix or asks for human help | Production credentials, remediation approval, and merge |

## Complete Automation: Parent-Child Factory

The parent-child factory uses the same work-cell idea, but removes the need for
a human to trigger each phase. The implementation differs by runtime:

| Runtime | Parent entry point | Child conversation helper | What to copy |
| --- | --- | --- | --- |
| **OpenHands Enterprise/Cloud** | `automations/replicated-jira-delegated-factory/prompt.md` | `scripts/openhands_v1_delegate.py` | `automations/replicated-jira-delegated-factory/`, `scripts/run_replicated_factory.py`, `scripts/openhands_v1_delegate.py`, `skills/delegated-conversation-factory/` |
| **Agent Canvas** | `agent-canvas/prompts/supervisor.md` | `scripts/agent_canvas_delegate.py` | `agent-canvas/prompts/`, `scripts/run_agent_canvas_factory.py`, `scripts/agent_canvas_delegate.py`, `skills/delegated-conversation-factory/` |

The core orchestration rule is the same in both paths: one parent conversation
is the control plane, child conversations own bounded work, and final responses
are treated as small contracts that the parent can summarize and gate.

The Enterprise/Cloud parent ultimately runs:

```bash
python3 scripts/run_replicated_factory.py \
  --base-url https://app.replicated.rajistics.com \
  --repo-slug rajshah4/sdlc-automation-github-demo \
  --branch "$GITHUB_DEMO_REF" \
  --issue-key KAN-73 \
  --post-jira-comment
```

Conceptually, the parent helper does this:

```python
for cell in ["story-to-pr", "code-review", "qa"]:
    child = start_child_conversation(cell)
    result = wait_for_final_response(child)
    lifecycle_report.add(cell, result)

post_jira_summary(lifecycle_report)
```

## What You'll See

- A sparse issue becomes a PR with an implementation branch and visible OpenSpec-style proposal/spec/design/task artifacts.
- A PR receives an automated review comment rather than a silent background score.
- QA output lands on the PR with concrete test files and command results. The repo also includes a Playwright browser-evidence example with screenshot, GIF, video, and report generation.
- An incident issue receives an evidence-first triage response; if cloud context
  is unavailable, the automation should say so and mark the item for humans.
- Status labels such as `openhands:in-progress`, `openhands:needs-human`, and
  `openhands:done` make the automation state visible without leaving GitHub.

## How It's Built

This repo is intentionally composed from OpenHands platform features and
repo-local knowledge, not a custom agent runtime.

| Capability | Where it lives | Why it matters |
| --- | --- | --- |
| Step-by-step OpenHands automations | `automations/github/` | Four label-triggered prompt presets registered in the Rajistics OpenHands instance. No polling and no GitHub Actions required for the live flow. |
| Complete automation package | `automations/replicated-jira-delegated-factory/` | Opt-in Jira-to-parent-supervisor package for OpenHands Enterprise/Cloud. It does not modify the existing label automations. |
| Repo-local skills | `skills/` | Reusable skills encode story/spec, QA, SRE, code-review, and delegated-factory behavior with scripts and references that customers can inspect. |
| Agent Canvas delegated demo | `agent-canvas/` | Parent/child delegated workflow for Agent Canvas using the same reusable pattern with Canvas-specific plumbing. |
| OpenSpec-style artifacts | `openspec/` | Repo-local context and generated change folders keep request, proposal, spec delta, design, and tasks version controlled. |
| Deterministic scripts | `scripts/` | Preflight, label setup, fixture simulation, Petstore checks, and GCP helpers run before broader model reasoning where possible. |
| GitHub templates and labels | `.github/` | Issues, PRs, and labels define the human approval boundaries. |
| Petstore app | `app/` | A small API/UI surface gives the automations realistic code, tests, and incident paths to work on. |
| Playwright UI evidence | `app/web/tests/` | Browser QA example that records video, creates a GIF preview, captures a screenshot, and writes a report for PR evidence when Playwright is available. |

Cost and security are part of the demo design: event-driven labels avoid
unnecessary LLM calls, preflight scripts catch configuration issues without
using a model, different LLM profiles can be used for coding/review/ops, and
secrets stay in the OpenHands secret store or local `.env`, never in the repo.

## Fast Local Validation

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
```

## Repo Map

| Folder | Purpose |
| --- | --- |
| `app/` | Small Petstore app, static UI, Cloud Run surface, and app tests. |
| `automations/` | Step-by-step GitHub prompt presets plus the opt-in delegated Jira factory package. |
| `agent-canvas/` | Agent Canvas version of the parent-child delegated workflow. |
| `openspec/` | OpenSpec-style project context and generated change folders for story-to-PR work. |
| `skills/` | Repo-local OpenHands skills with scripts and references, including the reusable delegated-factory skill. |
| `scripts/` | Deterministic setup, registration, preflight, QA, and SRE helpers. |
| `docs/` | Customer-facing setup, walkthrough, and validation notes. |
| `.github/` | Issue/PR templates and label definitions; the live demo uses OpenHands labels, not GitHub Actions. |

## Register OpenHands Automations

OpenHands Automations should be registered with the prompt preset API. The checked-in package specs live under `automations/github/`.

Dry-run the registration payloads:

```bash
python3 scripts/register_github_automations.py --dry-run
```

Apply registration when `OPENHANDS_HOST_GITHUB`, `OPENHANDS_API_KEY_GITHUB`, `GITHUB_DEMO_REPOSITORY`, and `GITHUB_DEMO_REPO_URL` are set:

```bash
python3 scripts/register_github_automations.py --apply
```

No secrets belong in this repo. Store OpenHands, GitHub, Slack, and GCP credentials in the OpenHands secret store or a local `.env` excluded by `.gitignore`.

## Demo Docs

- [GitHub demo walkthrough](docs/github-demo-walkthrough.md)
- [Replicated Jira delegated factory demo](docs/replicated-jira-delegated-factory-demo.md)
- [Agent Canvas delegated factory](agent-canvas/README.md)
- [Setup checklist](docs/setup-checklist.md)
- [Work log](docs/work-log.md)
- [Tested flow and validation notes](docs/tested-demo-flow.md)
