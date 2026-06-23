#!/usr/bin/env python3
"""Validate the lightweight OpenSpec markdown contract used by the demo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "# OpenSpec:",
    "## Source",
    "## Request Summary",
    "## Assumptions",
    "## Non-Goals",
    "## Acceptance Criteria",
    "## Human Gates",
    "## Implementation Plan",
    "## Validation Plan",
    "## Evidence Checklist",
]


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")
    if "- [ ]" not in text and "- [x]" not in text.lower():
        errors.append("acceptance/evidence checklist should include markdown checkboxes")
    if "GitHub issue:" not in text:
        errors.append("source section should include a GitHub issue link")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an SDLC Automation Demo OpenSpec file.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if not args.path.exists():
        print(f"{args.path}: file does not exist", file=sys.stderr)
        return 2

    errors = validate(args.path)
    if errors:
        print(f"{args.path}: OpenSpec validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{args.path}: OpenSpec validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
