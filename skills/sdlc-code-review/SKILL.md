---
name: sdlc-code-review
description: Petstore-specific GitHub PR review rules for the SDLC Automation Demo.
triggers:
  - openhands-review
  - pr review
---

# SDLC Code Review

Use this skill with the official OpenHands review behavior.

## Review Priorities

Lead with concrete findings:

- correctness bugs
- security or secret-handling risks
- missing tests for changed behavior
- user-visible behavior without QA evidence
- automation loops or comments that retrigger themselves

## Petstore Rules

- Default catalog search returns only available pets.
- Pending pets cannot be adopted.
- Money uses integer cents, never floats.
- UI changes need UI evidence.
- Automation result comments should avoid exact trigger text.

## Output Shape

```markdown
# Automated Code Review via OpenHands

Status: approved | changes recommended | needs human follow-up
Goal:

## Findings
- [Important] `path:line` - issue, impact, fix direction

## Petstore Contract Checks
- Pending/adopted visibility:
- Adoption validation:
- Money-as-cents:
- Evidence:

## Residual Risk
```

