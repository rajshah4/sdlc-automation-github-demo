#!/usr/bin/env python3
"""Validate the OpenSpec-style change contract used by the demo."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LEGACY_TITLE_OPTIONS = [
    "# Open Specification:",
    "# OpenSpec:",
]

LEGACY_REQUIRED_HEADINGS = [
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


CHANGE_REQUIRED_FILES = {
    "proposal.md": [
        "# Change:",
        "## Why",
        "## Source",
        "## Assumptions",
        "## Non-Goals",
        "## What Changes",
        "## Impact",
        "## Human Gates",
    ],
    "design.md": [
        "# Design",
        "## Context",
        "## Decision",
        "## Risks",
        "## Validation Plan",
    ],
    "tasks.md": [
        "# Tasks",
    ],
}

SPEC_DELTA_MARKERS = [
    "## ADDED Requirements",
    "## MODIFIED Requirements",
    "## REMOVED Requirements",
]

SOURCE_LINK_PATTERNS = [
    re.compile(r"GitHub issue:\s+https://github\.com/[^\s]+/[^\s]+/issues/\d+"),
    re.compile(r"Jira issue:\s+https://[A-Za-z0-9.-]+\.atlassian\.net/browse/[A-Z][A-Z0-9]+-\d+"),
]


def has_checkbox(text: str) -> bool:
    return "- [ ]" in text or "- [x]" in text.lower()


def has_source_issue_link(text: str) -> bool:
    return any(pattern.search(text) for pattern in SOURCE_LINK_PATTERNS)


def validate_legacy_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not any(title in text for title in LEGACY_TITLE_OPTIONS):
        errors.append("missing title: # Open Specification: or # OpenSpec:")
    for heading in LEGACY_REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")
    if not has_checkbox(text):
        errors.append("acceptance/evidence checklist should include markdown checkboxes")
    if not has_source_issue_link(text):
        errors.append("source section should include a GitHub or Jira issue link")
    return errors


def validate_change_dir(path: Path) -> list[str]:
    errors: list[str] = []
    for relative, headings in CHANGE_REQUIRED_FILES.items():
        file_path = path / relative
        if not file_path.exists():
            errors.append(f"missing file: {relative}")
            continue
        text = file_path.read_text(encoding="utf-8")
        for heading in headings:
            if heading not in text:
                errors.append(f"{relative}: missing heading: {heading}")
        if relative == "proposal.md" and not has_source_issue_link(text):
            errors.append("proposal.md: source section should include a GitHub or Jira issue link")
        if relative == "tasks.md" and not has_checkbox(text):
            errors.append("tasks.md: task list should include markdown checkboxes")

    specs_dir = path / "specs"
    if not specs_dir.exists():
        errors.append("missing directory: specs")
        return errors

    spec_paths = sorted(specs_dir.glob("**/spec.md"))
    if not spec_paths:
        errors.append("missing spec delta: specs/<capability>/spec.md")
        return errors

    for spec_path in spec_paths:
        text = spec_path.read_text(encoding="utf-8")
        display_path = spec_path.relative_to(path)
        if not any(marker in text for marker in SPEC_DELTA_MARKERS):
            errors.append(f"{display_path}: missing ADDED/MODIFIED/REMOVED requirements section")
        if "### Requirement:" not in text:
            errors.append(f"{display_path}: missing requirement heading")
        if "#### Scenario:" not in text:
            errors.append(f"{display_path}: missing scenario heading")

    return errors


def validate(path: Path) -> list[str]:
    if path.is_dir():
        return validate_change_dir(path)
    return validate_legacy_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an SDLC Automation Demo OpenSpec-style change.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if not args.path.exists():
        print(f"{args.path}: file does not exist", file=sys.stderr)
        return 2

    errors = validate(args.path)
    if errors:
        print(f"{args.path}: OpenSpec-style validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{args.path}: OpenSpec-style validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
