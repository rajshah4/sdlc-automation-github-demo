#!/usr/bin/env python3
"""Create or update demo labels with the GitHub CLI."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LABELS_PATH = REPO_ROOT / "config" / "github-labels.json"


def run_gh(args: list[str], apply: bool) -> None:
    print("gh " + " ".join(args))
    if apply:
        subprocess.run(["gh", *args], check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="GitHub repo as OWNER/REPO")
    parser.add_argument("--apply", action="store_true", help="actually call gh; default is dry-run")
    args = parser.parse_args()

    labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    for label in labels:
        create_args = [
            "label",
            "create",
            label["name"],
            "--repo",
            args.repo,
            "--color",
            label["color"],
            "--description",
            label["description"],
        ]
        edit_args = [
            "label",
            "edit",
            label["name"],
            "--repo",
            args.repo,
            "--color",
            label["color"],
            "--description",
            label["description"],
        ]
        if args.apply:
            result = subprocess.run(["gh", *create_args], check=False)
            if result.returncode != 0:
                subprocess.run(["gh", *edit_args], check=True)
        else:
            run_gh(create_args, apply=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

