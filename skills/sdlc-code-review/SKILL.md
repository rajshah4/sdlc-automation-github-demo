---
name: sdlc-code-review
description: GitHub PR code-review guidance for the SDLC Automation Demo, layering Petstore-specific correctness, risk, testing, and supply-chain checks onto OpenHands /codereview behavior.
triggers:
  - openhands-review
  - /codereview
  - pr review
  - code review
---

# SDLC Code Review

Use this skill with the official OpenHands `/codereview` behavior. This custom skill adds repo-specific judgment; it does not replace the default OpenHands review workflow.

The review should feel like a senior engineer looking for real defects, not a style pass.

## GitHub Boundaries

- Trigger label: `openhands-review`
- Status labels: `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, `openhands:done`
- Prefer a structured PR review with inline findings when line context is available.
- Do not approve, merge, push fixes, or update branch protection from this skill.
- Avoid result comments that repeat the exact trigger text.

## Context Reuse

Before reviewing, use `skills/sdlc-context-reuse/SKILL.md` or `scripts/build_context_reuse_report.py` to load durable repo rules, prior QA/review evidence, and targeted repo search. Prefer lower-cost context gathering before higher-cost risk judgment.

## Review Priorities

Lead with concrete findings:

- correctness bugs
- security or secret-handling risks
- missing tests for changed behavior
- user-visible behavior without QA evidence
- automation loops or status-label changes that retrigger work

Skip bikeshedding unless it hides a correctness, security, maintainability, or demo-risk problem.

## Petstore Rules

- Default catalog search returns only available pets.
- Pending pets can be found only when status is explicitly requested.
- Pending or adopted pets cannot be adopted.
- Money uses integer cents, never floats.
- New filters reject negative values and invalid ranges.
- UI changes need UI evidence.
- Automation result comments should focus on evidence and next steps.
- Incident remediation must require Cloud Logging evidence and `safe_to_remediate=true`.

Run `python3 skills/sdlc-code-review/scripts/review_checklist.py` for a deterministic Petstore checklist when orienting.

## References

- `references/risk-evaluation.md` for low/medium/high risk classification.
- `references/supply-chain-security.md` when dependencies, package metadata, workflows, or install scripts change.

## Evidence Expectations

- Read the PR body, diff, linked issue, and OpenSpec-style change folder if present.
- Verify tests match changed behavior.
- Call out claims that are not backed by commands or UI evidence.
- If no issues are found, say that clearly and note any residual risk or test gap.

## Output Shape

```markdown
# Automated Code Review via OpenHands

Status: approved | changes recommended | needs human follow-up
Goal:
Risk: low | medium | high

## Findings
- [Important] `path:line` - issue, impact, fix direction

## Petstore Contract Checks
- Pending/adopted visibility:
- Adoption validation:
- Money-as-cents:
- Evidence:

## Tests And QA
- Tests reviewed:
- Missing evidence:

## Residual Risk
```

## Severity Guidance

- Important: likely defect, security issue, regression, broken automation boundary, or missing critical test.
- Medium: plausible edge-case defect, incomplete validation, confusing operational behavior.
- Low: maintainability concern worth mentioning only after higher-value findings.

Do not bury important findings under praise or summary text.
