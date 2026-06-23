---
name: sdlc-incident
description: SRE incident triage for the SDLC Automation Demo, using GitHub issues/comments, Google Cloud logs, Cloud Run evidence, and bounded Petstore remediation rules.
triggers:
  - openhands-incident
  - incident triage
  - gcp logs
  - cloud run
---

# SDLC SRE Incident Triage

Use this skill when a GitHub issue or comment reports a production symptom.

This skill is based on the SRE Cloud Run remediation demo pattern: observe first, separate evidence from hypotheses, use deterministic scripts before broad reasoning, and keep production changes behind explicit safety checks and human control.

## GitHub Boundaries

- Trigger labels/comments: `openhands-incident`
- Status labels: `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, `openhands:done`
- Incident automation may post an operator report or open a small PR.
- Incident automation must not merge, deploy, change IAM, rotate secrets, or mutate cloud resources without the bounded safe-remediation criteria.

## Flow

1. State symptom and impact.
2. Gather recent issue/PR context, Cloud Run target, and Cloud Logging evidence.
3. Use `scripts/petstore_gcp_observe.py` for read-only observation when GCP credentials are available.
4. Summarize observation JSON with `skills/sdlc-incident/scripts/triage_observation.py`.
5. Separate facts, hypotheses, and unknowns.
6. Determine incident class, confidence, and safe remediation status.
7. Post an operator report, or create a small fix PR only when the fix is bounded and testable.

Read `references/cloud-run-petstore-incident.md` when the symptom involves GCP, Cloud Run, Cloud Logging, pending pets, degraded status, or runtime remediation.

## Known Incident Class

`petstore_website_catalog_regression`:

- Symptom: pending pets appear in the available-pets experience.
- Cloud Run status: `/api/status` returns degraded/500 in incident mode.
- Log evidence: `jsonPayload.incident.type="petstore_website_catalog_regression"` and `error_code="PENDING_PET_VISIBLE"`.
- Safe action: restore runtime catalog filter to available pets only.
- Approved script: `python3 scripts/petstore_config_fix.py` only after observation reports `diagnosis.safe_to_remediate=true`.

## Safe Remediation Criteria

Open a fix PR only if:

- the incident maps to one local code path
- reproduction is available
- the fix is small
- regression tests can be added
- no schema, auth, IAM, secret, billing, or data migration decision is required

Run runtime remediation only if:

- a human explicitly asked for the bounded remediation, or the demo script says this run is allowed
- `scripts/petstore_gcp_observe.py` reports `diagnosis.safe_to_remediate=true`
- the action is limited to `scripts/petstore_config_fix.py`
- `DEMO_ADMIN_TOKEN` exists in the OpenHands secret store or local environment
- the report includes before/after evidence

If any condition is missing, stay report-only and label `openhands:needs-human`.

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

## Evidence Requirements

- Cloud Run service, region, and project names without credentials.
- Logs Explorer link when available.
- Confirmation checks from `diagnosis.confirmation_checks`.
- Sample structured log fields without secrets.
- Clear distinction between "observed", "inferred", and "not tested".

## Stop Conditions

Stop and ask for human input if the incident points to IAM, secrets, billing, deployment config, data correction, destructive actions, unknown incident classes, or cloud evidence that contradicts the issue symptom.
