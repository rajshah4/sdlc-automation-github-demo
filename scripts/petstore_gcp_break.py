#!/usr/bin/env python3
"""Put the live Petstore Cloud Run service into the approved SRE demo incident state."""

from __future__ import annotations

import argparse
import os

from petstore_gcp_common import (
    add_common_args,
    configure_gcloud_auth,
    detect_project,
    http_json,
    print_json,
    service_url,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Petstore website catalog regression demo state.")
    add_common_args(parser)
    parser.add_argument("--traffic", type=int, default=3, help="Synthetic traffic rounds after breaking the service.")
    args = parser.parse_args()

    configure_gcloud_auth()
    token = os.getenv("DEMO_ADMIN_TOKEN")
    if not token:
        raise RuntimeError("DEMO_ADMIN_TOKEN is required to toggle the demo state.")
    project = detect_project(args.project)
    url = service_url(project, args.region, args.service)

    state = http_json(
        url,
        "/api/admin/state",
        method="POST",
        token=token,
        payload={"mode": "bad_catalog_filter"},
    )
    traffic = []
    for _ in range(args.traffic):
        traffic.append(http_json(url, "/"))
        traffic.append(http_json(url, "/api/status"))
        traffic.append(http_json(url, "/api/pets"))
        traffic.append(http_json(url, "/api/adoptions?pet_id=pet-103"))

    print_json(
        {
            "action": "create_petstore_catalog_regression",
            "project": project,
            "region": args.region,
            "service": args.service,
            "service_url": url,
            "state_change": state,
            "traffic_statuses": [item["status"] for item in traffic],
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

