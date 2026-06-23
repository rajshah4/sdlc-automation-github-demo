# Open Specification Template

Use this template when `sdlc-story` converts a sparse GitHub issue or issue comment into implementation work.

Recommended path:

```text
specs/github-issue-<issue-number>/open-spec.md
```

## Required Headings

```markdown
# OpenSpec: <short feature name>

## Source

- GitHub issue:
- Trigger:
- Automation:

## Request Summary

<One paragraph in customer-facing language.>

## Assumptions

- <Assumption that lets implementation proceed safely.>

## Non-Goals

- <Thing explicitly out of scope.>

## Acceptance Criteria

- [ ] <Observable behavior or testable outcome.>

## Human Gates

- Scope approval:
- Review approval:
- Merge approval:
- Deployment approval:

## Implementation Plan

- <Small, ordered implementation step.>

## Validation Plan

- <Focused test or deterministic command.>

## Evidence Checklist

- [ ] Tests added or updated.
- [ ] Commands run.
- [ ] UI evidence captured when UI changed.
- [ ] Residual risk documented.
```

## Demo Language

- Say "SDLC Automation Demo."
- Say "open specification" when explaining the bridge from comment to PR.
- Emphasize that the spec is version controlled and reviewable.
- Make human control explicit: OpenHands proposes and implements; humans approve scope, review, merge, and deployment.
- Mention cost control naturally: deterministic extraction and validation happen before broad LLM exploration.

## Scope Guardrails

Keep a request in this skill only when it can produce a small Petstore PR. Stop and ask for human input when the request needs:

- new secrets or production credentials
- auth, IAM, billing, or payment decisions
- schema or data migration decisions
- new dependencies
- infrastructure or deployment changes
- destructive cloud actions
