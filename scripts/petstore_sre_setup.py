#!/usr/bin/env python3
"""One-command setup for the Petstore SRE Cloud Run incident demo."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

from petstore_gcp_common import ROOT_DIR, add_common_args, configure_gcloud_auth, detect_project, print_json


def run_step(args: list[str]) -> dict:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"step failed: {args}")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy, break, and observe the Petstore SRE demo.")
    add_common_args(parser)
    parser.add_argument("--skip-deploy", action="store_true")
    parser.add_argument("--min-instances", type=int, default=1)
    args = parser.parse_args()

    configure_gcloud_auth()
    project = detect_project(args.project)
    common = [f"--project={project}", f"--region={args.region}", f"--service={args.service}"]

    deploy = None
    if not args.skip_deploy:
        deploy = run_step(["scripts/petstore_gcp_deploy.py", *common, f"--min-instances={args.min_instances}"])
    broken = run_step(["scripts/petstore_gcp_break.py", *common])
    observed = run_step(["scripts/petstore_gcp_observe.py", *common])

    print_json(
        {
            "action": "setup_petstore_sre_incident",
            "project": project,
            "region": args.region,
            "service": args.service,
            "deploy": deploy,
            "broken_state": broken,
            "observation": observed,
            "trigger": "Create or comment on an Azure Boards work item with: openhands-incident investigate Petstore website regression",
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
