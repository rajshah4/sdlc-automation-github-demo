#!/usr/bin/env python3
"""Observe the live Petstore Cloud Run incident state and Cloud Logging evidence."""

from __future__ import annotations

import argparse
from collections import Counter
from typing import Any

from petstore_gcp_common import (
    DEFAULT_LOG_FRESHNESS,
    add_common_args,
    configure_gcloud_auth,
    detect_project,
    http_json,
    logs_explorer_url,
    print_json,
    read_incident_logs,
    service_url,
)


def compact_log(entry: dict[str, Any]) -> dict[str, Any]:
    payload = entry.get("jsonPayload") or {}
    incident = payload.get("incident") if isinstance(payload.get("incident"), dict) else {}
    return {
        "timestamp": entry.get("timestamp"),
        "severity": entry.get("severity"),
        "revision": entry.get("resource", {}).get("labels", {}).get("revision_name"),
        "message": payload.get("message"),
        "path": payload.get("path"),
        "status": payload.get("status"),
        "component": payload.get("component"),
        "operation": payload.get("operation"),
        "incident_type": incident.get("type"),
        "safe_to_remediate": incident.get("safe_to_remediate"),
        "error_code": payload.get("error_code"),
        "pending_pet_ids": payload.get("pending_pet_ids"),
    }


def summarize(logs: list[dict[str, Any]]) -> dict[str, Any]:
    compact = [compact_log(entry) for entry in logs]
    return {
        "count": len(compact),
        "by_error_code": dict(Counter(item.get("error_code") for item in compact if item.get("error_code"))),
        "by_component": dict(Counter(item.get("component") for item in compact if item.get("component"))),
        "by_operation": dict(Counter(item.get("operation") for item in compact if item.get("operation"))),
        "sample": compact[:5],
    }


def diagnose(status: dict[str, Any], pets: dict[str, Any], log_summary: dict[str, Any]) -> dict[str, Any]:
    status_body = status.get("body") if isinstance(status.get("body"), dict) else {}
    incident = status_body.get("incident") if isinstance(status_body.get("incident"), dict) else {}
    pet_body = pets.get("body") if isinstance(pets.get("body"), dict) else {}
    pending_visible = [
        pet.get("id")
        for pet in pet_body.get("pets", [])
        if isinstance(pet, dict) and pet.get("status") == "pending"
    ]
    has_log_evidence = log_summary["by_error_code"].get("PENDING_PET_VISIBLE", 0) > 0
    safe = (
        status.get("status") == 500
        and incident.get("type") == "petstore_website_catalog_regression"
        and bool(pending_visible)
        and has_log_evidence
        and incident.get("safe_to_remediate") is True
    )
    return {
        "safe_to_remediate": safe,
        "incident_type": incident.get("type"),
        "error_code": incident.get("error_code"),
        "pending_pets_visible": pending_visible,
        "confirmation_checks": {
            "status_endpoint_degraded": status.get("status") == 500,
            "pending_pet_visible": bool(pending_visible),
            "cloud_logging_error_seen": has_log_evidence,
            "runtime_says_safe": incident.get("safe_to_remediate") is True,
        },
        "recommended_action": (
            "Run the approved catalog-filter runtime remediation."
            if safe
            else "Stop and ask a human to review the incident evidence."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Observe Petstore Cloud Run and Cloud Logging incident evidence.")
    add_common_args(parser)
    parser.add_argument("--freshness", default=DEFAULT_LOG_FRESHNESS)
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()

    configure_gcloud_auth()
    project = detect_project(args.project)
    url = service_url(project, args.region, args.service)

    status = http_json(url, "/api/status")
    pets = http_json(url, "/api/pets")
    logs = read_incident_logs(project, args.service, freshness=args.freshness, limit=args.limit)
    log_summary = summarize(logs)
    diagnosis = diagnose(status, pets, log_summary)

    print_json(
        {
            "project": project,
            "region": args.region,
            "service": args.service,
            "service_url": url,
            "status_check": status,
            "pets_check": pets,
            "cloud_logging": {
                "freshness": args.freshness,
                "explorer_url": logs_explorer_url(project, args.service, args.freshness),
                "summary": log_summary,
            },
            "diagnosis": diagnosis,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

