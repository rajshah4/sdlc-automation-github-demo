#!/usr/bin/env python3
"""Turn petstore_gcp_observe.py JSON into a GitHub-ready incident report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def yes_no(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "unknown"


def render_report(payload: dict[str, Any]) -> str:
    diagnosis = payload.get("diagnosis") if isinstance(payload.get("diagnosis"), dict) else {}
    checks = diagnosis.get("confirmation_checks") if isinstance(diagnosis.get("confirmation_checks"), dict) else {}
    logs = payload.get("cloud_logging") if isinstance(payload.get("cloud_logging"), dict) else {}
    summary = logs.get("summary") if isinstance(logs.get("summary"), dict) else {}

    lines = [
        "# Petstore Incident Triage",
        "",
        f"Project: `{payload.get('project', 'unknown')}`",
        f"Region: `{payload.get('region', 'unknown')}`",
        f"Service: `{payload.get('service', 'unknown')}`",
        f"Service URL: {payload.get('service_url', 'unknown')}",
        "",
        "## Diagnosis",
        "",
        f"- Incident type: `{diagnosis.get('incident_type', 'unknown')}`",
        f"- Error code: `{diagnosis.get('error_code', 'unknown')}`",
        f"- Pending pets visible: `{diagnosis.get('pending_pets_visible', [])}`",
        f"- Safe to remediate: **{yes_no(diagnosis.get('safe_to_remediate'))}**",
        f"- Recommended action: {diagnosis.get('recommended_action', 'unknown')}",
        "",
        "## Confirmation Checks",
        "",
    ]
    for key in sorted(checks):
        lines.append(f"- `{key}`: {yes_no(checks.get(key))}")
    lines.extend(
        [
            "",
            "## Cloud Logging",
            "",
            f"- Freshness: `{logs.get('freshness', 'unknown')}`",
            f"- Matching log count: `{summary.get('count', 0)}`",
            f"- Error counts: `{summary.get('by_error_code', {})}`",
            f"- Logs Explorer: {logs.get('explorer_url', 'not available')}",
            "",
            "## Automation Action",
            "",
        ]
    )
    if diagnosis.get("safe_to_remediate") is True:
        lines.append("Observation says the bounded Petstore runtime remediation is eligible, pending human/demo approval.")
    else:
        lines.append("Report-only. Do not mutate cloud resources; ask a human to review the evidence.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Petstore SRE observation report.")
    parser.add_argument("observation_json", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.observation_json.read_text(encoding="utf-8"))
    print(render_report(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
