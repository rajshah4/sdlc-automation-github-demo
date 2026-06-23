# Petstore Cloud Logging Schema

Structured operational events should use consistent fields so OpenHands can diagnose incidents from logs.

## Common Fields

| Field | Example |
| --- | --- |
| `service` | Petstore Cloud Run service name |
| `component` | `adoption-api` |
| `operation` | `adoption.create_order` |
| `severity` | `ERROR` |
| `trace_id` | `demo-trace-123` |
| `release.version` | `demo-2026-06-16` |
| `release.pr` | `42` |
| `provider` | `azure_devops` |

## Incident Object

```json
{
  "incident": {
    "type": "adoption_validation_error",
    "mode": "synthetic_demo",
    "safe_to_remediate": false
  }
}
```

## Adoption Validation Error

```json
{
  "service": "<petstore-cloud-run-service>",
  "component": "adoption-api",
  "operation": "adoption.create_order",
  "severity": "ERROR",
  "incident": {
    "type": "adoption_validation_error",
    "mode": "synthetic_demo",
    "safe_to_remediate": false
  },
  "pet_id": "pet-103",
  "pet_status": "pending",
  "error_code": "PENDING_PET_ADOPTION_ATTEMPTED",
  "message": "Pending pet was submitted to adoption order flow"
}
```

## Search Latency

```json
{
  "service": "<petstore-cloud-run-service>",
  "component": "catalog-api",
  "operation": "catalog.search",
  "severity": "WARNING",
  "incident": {
    "type": "search_latency",
    "mode": "synthetic_demo",
    "safe_to_remediate": false
  },
  "duration_ms": 1800,
  "query": "dog",
  "species": "dog"
}
```
