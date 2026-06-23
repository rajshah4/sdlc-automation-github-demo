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

This demo keeps that loop inside GitHub. A human applies a label, OpenHands runs
one bounded automation, then posts evidence back where the team already works.

## The Four Work Cells

| Work cell | Trigger | What OpenHands does | What humans control |
| --- | --- | --- | --- |
| **Story to PR** | Apply `openhands-build` to a sparse issue | Clarifies the request, writes an open specification, implements the change, runs tests, and opens a PR | Scope, review, approval, and merge |
| **Code Review** | Apply `openhands-review` to a PR | Reads the diff, checks risk areas, and posts review findings as a PR comment | Which findings block the PR |
| **Automated QA** | Apply `openhands-qa` to a PR | Builds or updates test coverage, runs deterministic checks, and includes UI test evidence where applicable | Test acceptance and merge readiness |
| **SRE Incident** | Apply `openhands-incident` to an incident issue | Gathers Cloud Run / Cloud Logging evidence, diagnoses likely cause, and proposes a fix or asks for human help | Production credentials, remediation approval, and merge |

## What You'll See

- A sparse issue becomes a PR with an implementation branch and a visible spec.
- A PR receives an automated review comment rather than a silent background score.
- QA output lands on the PR with concrete test files and command results.
- An incident issue receives an evidence-first triage response; if cloud context
  is unavailable, the automation should say so and mark the item for humans.
- Status labels such as `openhands:in-progress`, `openhands:needs-human`, and
  `openhands:done` make the automation state visible without leaving GitHub.

## How It's Built

This repo is intentionally composed from OpenHands platform features and
repo-local knowledge, not a custom agent runtime.

| Capability | Where it lives | Why it matters |
| --- | --- | --- |
| OpenHands Automations | `automations/github/` | Four label-triggered prompt presets registered in the Rajistics OpenHands instance. No polling and no GitHub Actions required for the live flow. |
| Repo-local skills | `skills/` | Four reusable skills encode story/spec, QA, SRE, and code-review behavior with scripts and references that customers can inspect. |
| Deterministic scripts | `scripts/` | Preflight, label setup, fixture simulation, Petstore checks, and GCP helpers run before broader model reasoning where possible. |
| GitHub templates and labels | `.github/` | Issues, PRs, and labels define the human approval boundaries. |
| Petstore app | `app/` | A small API/UI surface gives the automations realistic code, tests, and incident paths to work on. |

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
| `automations/` | Four OpenHands prompt-preset automations registered in Rajistics. |
| `skills/` | Four repo-local OpenHands skills with scripts and references. |
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
- [Setup checklist](docs/setup-checklist.md)
- [Work log](docs/work-log.md)
- [Tested flow and validation notes](docs/tested-demo-flow.md)
