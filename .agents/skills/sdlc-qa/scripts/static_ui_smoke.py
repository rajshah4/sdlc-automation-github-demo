#!/usr/bin/env python3
"""Dependency-free smoke check for the static Petstore UI."""

from __future__ import annotations

import argparse
import sys
from urllib.request import urlopen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:4173")
    args = parser.parse_args()

    with urlopen(args.url, timeout=5) as response:
        html = response.read().decode("utf-8", errors="replace")

    required = ["Petstore", "Search", "adoption"]
    missing = [text for text in required if text.lower() not in html.lower()]
    if missing:
        print(f"Missing expected UI text: {', '.join(missing)}", file=sys.stderr)
        return 1
    print(f"Static UI smoke passed for {args.url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

