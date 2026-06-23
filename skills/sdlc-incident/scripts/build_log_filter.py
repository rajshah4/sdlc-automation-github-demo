#!/usr/bin/env python3
"""Print the Cloud Logging filter used for the known Petstore incident class."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from petstore_gcp_common import DEFAULT_LOG_FRESHNESS, DEFAULT_SERVICE, cloud_logging_filter  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Petstore Cloud Logging filter.")
    parser.add_argument("--service", default=DEFAULT_SERVICE)
    parser.add_argument("--freshness", default=DEFAULT_LOG_FRESHNESS)
    args = parser.parse_args()
    print(cloud_logging_filter(args.service, args.freshness))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
