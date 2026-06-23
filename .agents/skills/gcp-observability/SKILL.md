---
name: gcp-observability
description: Read-only GCP Cloud Run and Cloud Logging evidence guidance for the Petstore incident demo.
triggers:
  - openhands-incident
  - gcp logs
  - cloud run
---

# GCP Observability

Use this skill when incident automation needs Google Cloud evidence.

## Required Configuration

- `GCP_PROJECT`
- `GCP_REGION`
- `GCP_SERVICE`
- `GCP_LOG_NAME`
- read-only credentials in OpenHands secrets

## Safety

- Observe first.
- Do not print service account JSON or access tokens.
- Do not delete or mutate Cloud Run services, revisions, log buckets, secrets, IAM, or billing.
- Do not use local logs as a substitute for Cloud Logging evidence.

## Known Incident Class

`petstore_website_catalog_regression` is safe to remediate only when Cloud Logging evidence reports `safe_to_remediate=true` and the recommended action is the bounded catalog filter runtime fix.

