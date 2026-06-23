# Google Cloud Integration

Google Cloud is the operational evidence layer for the Petstore SDLC automation.

The first GCP integration should use:

- Cloud Run for a live Petstore service
- Cloud Logging for incident evidence
- synthetic traffic for reproducible demo signals

This intentionally avoids email and personal Gmail setup.

## Target Shape

```text
Petstore Cloud Run service
  -> structured JSON logs
  -> Cloud Logging query link
  -> OpenHands incident automation
  -> PR/operator report
  -> Slack update
```

## Recommended Environment Variables

```text
GCP_PROJECT=
GCP_REGION=us-central1
GCP_SERVICE=<petstore-cloud-run-service>
GCP_LOG_NAME=petstore-sdlc
```

## Evidence Rules

- Cloud Logging evidence must come from the live Cloud Run service or synthetic traffic hitting that service.
- Do not fabricate offline log evidence.
- Always include a Cloud Logging Explorer link when reporting an incident.
- Do not delete GCP resources during an automation run.
- Do not change IAM, service accounts, log buckets, secrets, or billing.

## First Incident Class: Website Catalog Regression

```text
petstore_website_catalog_regression
```

Expected structured log fields:

```json
{
  "component": "petstore-web",
  "operation": "web.available_pets",
  "incident": {
    "type": "petstore_website_catalog_regression",
    "safe_to_remediate": true
  },
  "error_code": "PENDING_PET_VISIBLE",
  "pending_pet_ids": ["pet-103"]
}
```

Approved bounded remediation:

```bash
python scripts/petstore_config_fix.py
```

This calls the live service's token-gated runtime remediation endpoint. It does not delete or reconfigure GCP resources.

## Secondary Incident Class

```text
adoption_validation_error
```

Expected structured log fields:

```json
{
  "component": "adoption-api",
  "operation": "adoption.create_order",
  "incident": {
    "type": "adoption_validation_error"
  },
  "pet_id": "pet-103",
  "pet_status": "pending",
  "error_code": "PENDING_PET_ADOPTION_ATTEMPTED"
}
```

## Safe Automation Boundary

The first SRE repair version is observe-first:

1. confirm public symptom
2. collect Cloud Logging evidence
3. correlate with recent PR/work item
4. run bounded runtime repair only when the known diagnosis is safe
5. post operator report or PR comment
6. notify Slack

If the diagnosis is not `petstore_website_catalog_regression` with `safe_to_remediate=true`, stop and post an operator report.
