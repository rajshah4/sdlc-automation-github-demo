#!/usr/bin/env python3
"""Print a deterministic Petstore review checklist."""

from __future__ import annotations


CHECKS = [
    "Default search excludes pending pets unless status is explicit.",
    "Pending and adopted pets cannot be adopted.",
    "Fee and donation math uses integer cents.",
    "New filters reject invalid ranges or negative values.",
    "User-visible behavior has tests and QA evidence.",
    "Automation comments avoid exact trigger text to prevent loops.",
    "Open spec acceptance criteria map to code and tests.",
    "Incident remediation requires Cloud Logging evidence and safe_to_remediate=true.",
    "Dependency, workflow, Dockerfile, and installer changes get supply-chain review.",
]


def main() -> int:
    for index, check in enumerate(CHECKS, start=1):
        print(f"{index}. {check}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
