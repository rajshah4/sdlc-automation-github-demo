#!/usr/bin/env python3
"""Apply the approved runtime repair for the Petstore SRE demo."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

from petstore_gcp_common import (
    ROOT_DIR,
    add_common_args,
    configure_gcloud_auth,
    detect_project,
    http_json,
    print_json,
    service_url,
)


def observe(project: str, region: str, service: str) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/petstore_gcp_observe.py",
            f"--project={project}",
            f"--region={region}",
            f"--service={service}",
        ],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "observation failed")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair the Petstore catalog filter runtime state.")
    add_common_args(parser)
    parser.add_argument("--force", action="store_true", help="Skip diagnosis safety guard.")
    args = parser.parse_args()

    configure_gcloud_auth()
    token = os.getenv("DEMO_ADMIN_TOKEN")
    if not token:
        raise RuntimeError("DEMO_ADMIN_TOKEN is required to apply the runtime remediation.")
    project = detect_project(args.project)
    before = observe(project, args.region, args.service)
    diagnosis = before.get("diagnosis", {})
    if diagnosis.get("safe_to_remediate") is not True and not args.force:
        raise RuntimeError(f"Refusing remediation because diagnosis was not safe: {diagnosis}")

    url = service_url(project, args.region, args.service)
    remediation = http_json(
        url,
        "/api/admin/remediate/catalog-filter",
        method="POST",
        token=token,
        payload={"reason": "Cloud Logging confirmed pending pet visible on available-pets website."},
    )
    after_status = http_json(url, "/api/status")
    after_pets = http_json(url, "/api/pets")
    after = observe(project, args.region, args.service)

    print_json(
        {
            "action": "repair_petstore_catalog_filter_runtime_state",
            "project": project,
            "region": args.region,
            "service": args.service,
            "service_url": url,
            "pre_remediation": before,
            "remediation": remediation,
            "verification": {
                "status_check": after_status,
                "pets_check": after_pets,
                "post_remediation_observation": after,
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

