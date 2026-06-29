# OpenSpec-Style Change Template

Use this template when `sdlc-story` converts a sparse GitHub or Jira issue into implementation work.

## Lineage

This demo intentionally follows the Fission-AI/OpenSpec project:

- Project: `https://github.com/Fission-AI/OpenSpec`
- Site: `https://openspec.pro`
- Upstream workflow: create a change folder, write proposal/spec/design/tasks, implement, then archive.

The live OpenHands automation writes OpenSpec-style artifacts directly instead
of invoking the OpenSpec CLI. That is deliberate for customer demos: the
automation has a bounded timeout, should avoid live package installs, and should
not depend on global Node tooling being present. If the CLI is preinstalled,
operators can use it outside the timed run to initialize, update, or archive.

## Recommended Path

```text
openspec/changes/github-issue-<issue-number>-<short-slug>/
openspec/changes/jira-<issue-key>-<short-slug>/
```

## Required Files

```text
proposal.md
design.md
tasks.md
specs/<capability>/spec.md
```

See `openspec-change-template/` for a complete example folder that can be
validated with:

```bash
python3 skills/sdlc-story/scripts/validate_open_spec.py \
  skills/sdlc-story/references/openspec-change-template
```

## `proposal.md`

```markdown
# Change: <short feature name>

## Why

<One paragraph in customer-facing language.>

## Source

- GitHub issue: <GitHub issue URL, when GitHub-triggered>
- Jira issue: <Jira issue URL, when Jira-triggered>
- Trigger:
- Automation:

## Assumptions

- <Assumption that lets implementation proceed safely.>

## Non-Goals

- <Thing explicitly out of scope.>

## What Changes

- <Observable behavior or implementation change.>

## Impact

- App behavior:
- Tests:
- Humans:

## Human Gates

- Scope approval:
- Review approval:
- Merge approval:
- Deployment approval:
```

## `specs/<capability>/spec.md`

```markdown
# <capability> Spec Delta

## ADDED Requirements

### Requirement: <observable behavior>

#### Scenario: <happy path or boundary path>

- Given <initial state>
- When <user or system action>
- Then <observable result>
```

## `design.md`

```markdown
# Design

## Context

<Relevant Petstore behavior and constraints.>

## Decision

- <Small implementation decision.>

## Risks

- <Risk and mitigation.>

## Validation Plan

- <Focused deterministic command or test.>
```

## `tasks.md`

```markdown
# Tasks

- [ ] Update OpenSpec-style spec delta.
- [ ] Implement the smallest safe code change.
- [ ] Add or update focused tests.
- [ ] Run validation.
- [ ] Document evidence and residual risk in the PR.
```

## Demo Language

- Say "SDLC Automation Demo."
- Say "OpenSpec-style change artifacts" when explaining the bridge from comment to PR.
- Link to `https://github.com/Fission-AI/OpenSpec` when explaining lineage.
- Emphasize that the change folder is version controlled and reviewable.
- Make human control explicit: OpenHands proposes and implements; humans approve scope, review, merge, and deployment.
- Mention cost control naturally: deterministic extraction and validation happen before broad LLM exploration.
- If asked why the CLI was not run live, say: "The demo keeps the timed automation deterministic and avoids package installs; these artifacts follow OpenSpec's folder and review model."

## Scope Guardrails

Keep a request in this skill only when it can produce a small Petstore PR. Stop and ask for human input when the request needs:

- new secrets or production credentials
- auth, IAM, billing, or payment decisions
- schema or data migration decisions
- new dependencies
- infrastructure or deployment changes
- destructive cloud actions
