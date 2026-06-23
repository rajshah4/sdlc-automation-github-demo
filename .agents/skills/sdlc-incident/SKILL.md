---
name: sdlc-incident
description: Incident triage and safe-remediation rules for the SDLC Automation Demo.
triggers:
  - openhands-incident
  - incident triage
---

# SDLC Incident Triage

Use this skill when a GitHub issue or comment reports a production symptom.

## Flow

1. State symptom and impact.
2. Gather logs and recent change context.
3. Separate facts from hypotheses.
4. Determine confidence and safe remediation status.
5. Post an operator report or create a small PR only when the fix is bounded and testable.

## Safe Remediation Criteria

Open a fix PR only if:

- the incident maps to one local code path
- reproduction is available
- the fix is small
- regression tests can be added
- no schema, auth, IAM, secret, billing, or data migration decision is required

## Report Shape

```markdown
# Petstore Incident Triage

Symptom:
Impact:
Timeline:
Evidence:
Likely root cause:
Confidence:
Recommended action:
Automation action taken:
```

