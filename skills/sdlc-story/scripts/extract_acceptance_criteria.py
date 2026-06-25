#!/usr/bin/env python3
"""Extract lightweight acceptance criteria from a GitHub issue body."""

from __future__ import annotations

import json
import re
import sys


CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[(?: |x|X)\]\s+(?P<text>.+?)\s*$")


def infer_from_request(title: str, body: str = "") -> list[str]:
    normalized = f"{title}\n{body}".lower()
    mentions_fee_cap = (
        "max adoption fee" in normalized
        or "maximum adoption fee" in normalized
        or "fee cap" in normalized
        or "adoption fee" in normalized
    )
    mentions_budget_language = any(
        phrase in normalized
        for phrase in (
            "in their budget",
            "within budget",
            "fit their budget",
            "families can afford",
            "pets they can afford",
            "affordable pets",
            "cost range",
        )
    )
    mentions_pet_context = any(
        phrase in normalized
        for phrase in ("pet", "pets", "adoption", "adopter", "families", "counselor")
    )
    if mentions_fee_cap or (mentions_budget_language and mentions_pet_context):
        return [
            "Catalog search accepts an optional max adoption fee in cents.",
            "Pets above the maximum fee are excluded.",
            "Invalid negative maximum fees are rejected.",
            "Focused tests cover matching, exclusion, and invalid input.",
        ]
    if "age" in normalized and "filter" in normalized:
        return [
            "Catalog search accepts optional minimum and maximum age filters.",
            "Invalid negative ages and inverted ranges are rejected.",
            "Focused tests cover min, max, combined range, and invalid input.",
        ]
    return []


def main() -> int:
    title = sys.argv[1] if len(sys.argv) > 1 else ""
    body = sys.stdin.read()
    explicit = [
        match.group("text")
        for line in body.splitlines()
        if (match := CHECKBOX_RE.match(line))
    ]
    inferred = infer_from_request(title, body)
    print(
        json.dumps(
            {
                "title": title,
                "explicit_acceptance_criteria": explicit,
                "inferred_acceptance_criteria": inferred,
                "has_sparse_issue_shape": not explicit and bool(inferred),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
