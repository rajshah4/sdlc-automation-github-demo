# GitHub Demo Walkthrough

This is the live flow for the GitHub-native SDLC Automation Demo.

## 0. Optional Context Scout

For the memory-and-cost version of the demo, create or reuse a sparse GitHub issue and add `openhands-context` before `openhands-build`.

This triggers the OpenHands automation through the GitHub `issues.labeled` event. It runs only on issues, skips items already marked `openhands:done`, and posts a context reuse comment before any coding work begins.

OpenHands should produce a context reuse report that shows:

- `AGENTS.md` durable repo memory
- selected repo-local skills
- existing logs, QA reports, and incident references
- targeted GitHub repo search results
- previous OpenHands conversations or run records
- recommended lower-cost scout and stronger coding/review model routing

Use this as the setup for the rest of the live demo: the expensive model should start after the scout has narrowed context.

If you need to run the scout again on the same issue, remove the status label that would cause the filter to skip the item, then remove and reapply `openhands-context`.

## 1. Create An Issue

Create a GitHub issue with a sparse title such as:

```text
Filter pets by max adoption fee
```

Add the label `openhands-build`.

OpenHands should clarify the request inside the conversation, infer the smallest safe Petstore change, create a feature branch, run focused tests, and open a draft PR. The PR should document assumptions, acceptance criteria, evidence, and human review notes.

## 2. Automation Creates OpenSpec-Style Artifacts And PR

Show the generated OpenSpec-style change folder, usually:

```text
openspec/changes/github-issue-<number>-<slug>/
```

Call out how the sparse issue became:

- `proposal.md`
- `design.md`
- `tasks.md`
- `specs/<capability>/spec.md`
- assumptions
- non-goals
- requirements and scenarios
- human gates
- validation plan

Lineage note: this demo follows the Fission-AI/OpenSpec change-folder model. The live automation writes the artifacts directly instead of installing or invoking the OpenSpec CLI during the timed label-triggered run, which keeps the customer demo deterministic.

Then show the generated PR.

Call out the human controls:

- PR is draft or reviewable, not auto-merged.
- Reviewers decide whether the implementation is acceptable.
- CI and branch protections still apply.
- Humans choose whether to merge.

## 3. Trigger Code Review

On the PR, add the label `openhands-review`.

OpenHands should inspect the diff, apply the repo-local `sdlc-code-review` skill, classify risk, check Petstore contracts, and post a structured code review comment. It should not claim tests passed unless it ran them or verified evidence.

## 4. Trigger QA And Test Generation

On the PR, add the label `openhands-qa`.

OpenHands should run or add focused tests, exercise the changed behavior, map results back to the OpenSpec-style change artifacts, and include UI evidence when the static web app changed.

For a concrete browser-evidence example, show:

- `app/web/tests/catalog-search.playwright.mjs`
- the PR QA comment with an inline GIF
- PR-branch artifact links for the screenshot, video, and report

If the remote runtime lacks Playwright or BrowserToolSet, the automation should say that and fall back to deterministic checks rather than claiming browser coverage.

## 5. Human Review And Merge

Show the normal GitHub review path:

- humans inspect OpenHands comments and code diffs
- humans resolve findings or ask follow-up questions
- humans approve and merge only when ready

## 6. Optional SRE Incident Flow

Create an incident issue and add the label `openhands-incident`.

Use the sample symptom:

```text
The Petstore website is showing pending pets in the available-pets experience.
Please inspect GCP logs and propose the safest fix.
```

OpenHands should collect GCP evidence, summarize impact, identify whether remediation is safe, and either post an operator report or open a small fix PR. It must not mutate cloud resources unless the bounded safe-remediation check passes and humans allow the demo remediation path.

## Four Skills To Show

- `skills/sdlc-story`: issue to OpenSpec-style change artifacts to PR.
- `skills/sdlc-qa`: automated test suite and UI evidence.
- `skills/sdlc-incident`: SRE incident triage with GCP evidence.
- `skills/sdlc-code-review`: OpenHands `/codereview` plus Petstore-specific risk checks.
