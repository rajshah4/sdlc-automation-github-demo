#!/usr/bin/env python3
"""Deploy the Petstore SRE demo service to Cloud Run."""

from __future__ import annotations

import argparse
import os

from petstore_gcp_common import APP_DIR, add_common_args, configure_gcloud_auth, detect_project, http_json, print_json, run, service_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy sdlc-automation-petstore to Cloud Run from app/Dockerfile.")
    add_common_args(parser)
    parser.add_argument("--min-instances", type=int, default=0)
    parser.add_argument("--incident-mode", default="healthy", choices=["healthy", "bad_catalog_filter"])
    args = parser.parse_args()

    configure_gcloud_auth()
    token = os.getenv("DEMO_ADMIN_TOKEN")
    if not token:
        raise RuntimeError("DEMO_ADMIN_TOKEN is required so setup/break/repair can safely control demo state.")
    project = detect_project(args.project)

    env_vars = ",".join(
        [
            "APP_NAME=sdlc-automation-petstore",
            f"GCP_REGION={args.region}",
            f"GCP_SERVICE={args.service}",
            f"INCIDENT_MODE={args.incident_mode}",
            f"DEMO_ADMIN_TOKEN={token}",
        ]
    )
    run(
        [
            "gcloud",
            "run",
            "deploy",
            args.service,
            "--source",
            ".",
            "--region",
            args.region,
            "--project",
            project,
            "--allow-unauthenticated",
            "--no-invoker-iam-check",
            "--quiet",
            "--min-instances",
            str(args.min_instances),
            "--set-env-vars",
            env_vars,
        ],
        cwd=APP_DIR,
    )
    url = service_url(project, args.region, args.service)
    print_json(
        {
            "action": "deploy_petstore_cloud_run",
            "project": project,
            "region": args.region,
            "service": args.service,
            "service_url": url,
            "status_check": http_json(url, "/api/status"),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
