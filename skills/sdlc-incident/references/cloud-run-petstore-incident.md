# Cloud Run Petstore Incident Runbook

Use this reference for the optional SRE incident flow in the SDLC Automation Demo.

## Required Configuration

The automation may read these values from OpenHands secrets or local environment:

- `GCP_PROJECT`
- `GCP_REGION`
- `GCP_SERVICE`
- `GOOGLE_APPLICATION_CREDENTIALS_JSON_B64`
- `DEMO_ADMIN_TOKEN` only when the approved runtime remediation is explicitly allowed

Never print service-account JSON, API tokens, admin tokens, or raw secret values.

## Observe First

Run:

```bash
python3 scripts/petstore_gcp_observe.py
```

Useful options:

```bash
python3 scripts/petstore_gcp_observe.py --project "$GCP_PROJECT" --region "$GCP_REGION" --service "$GCP_SERVICE" --freshness 30m --limit 25
```

The script gathers:

- Cloud Run service URL
- `/api/status`
- `/api/pets`
- Cloud Logging entries for the known incident class
- diagnosis fields, including `safe_to_remediate`

Summarize the JSON into a GitHub-ready operator report:

```bash
python3 scripts/petstore_gcp_observe.py > /tmp/petstore-observation.json
python3 skills/sdlc-incident/scripts/triage_observation.py /tmp/petstore-observation.json
```

## Expected Evidence

The known incident has all of these signals:

- `diagnosis.incident_type` is `petstore_website_catalog_regression`
- `diagnosis.error_code` is `PENDING_PET_VISIBLE`
- `diagnosis.pending_pets_visible` is not empty
- `diagnosis.confirmation_checks.status_endpoint_degraded` is true
- `diagnosis.confirmation_checks.cloud_logging_error_seen` is true
- `diagnosis.confirmation_checks.runtime_says_safe` is true
- `diagnosis.safe_to_remediate` is true

If any signal is missing, do not remediate. Post the evidence and ask for human input.

## Approved Runtime Remediation

The only approved runtime mutation is:

```bash
python3 scripts/petstore_config_fix.py
```

This script observes before it acts and refuses to run unless the diagnosis is safe, unless a human intentionally passes `--force`. Do not use `--force` in the demo automation.

After remediation, include:

- pre-remediation diagnosis
- remediation endpoint result
- post-remediation status
- post-remediation pets check
- Cloud Logging link

## Report-Only Mode

Use report-only mode when:

- GCP credentials are unavailable
- the GitHub issue lacks enough incident context
- the incident class is unknown
- remediation requires IAM, secrets, billing, deployment, data, or schema decisions
- the action would mutate production/cloud resources outside the approved runtime endpoint

## Cost And Security Talk Track

- The GitHub label/comment is event driven; no LLM call happens until a human asks for triage.
- `petstore_gcp_observe.py` gathers deterministic facts before the model reasons about root cause.
- Runtime remediation is bounded by a deterministic safety gate.
- Humans approve PRs, merges, deployments, and any production-facing action.
