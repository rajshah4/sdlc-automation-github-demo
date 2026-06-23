#!/usr/bin/env python3
"""Deterministic preflight for the GitHub-native SDLC Automation Demo."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_ROOT = REPO_ROOT / "automations" / "github"
LABELS_PATH = REPO_ROOT / "config" / "github-labels.json"
REQUIRED_LABELS = {
    "openhands-build",
    "openhands-review",
    "openhands-qa",
    "openhands-incident",
    "openhands:ready",
    "openhands:in-progress",
    "openhands:needs-human",
    "openhands:done",
}
REQUIRED_ENV = [
    "OPENHANDS_HOST_GITHUB",
    "OPENHANDS_API_KEY_GITHUB",
    "GITHUB_DEMO_REPOSITORY",
    "GITHUB_DEMO_REPO_URL",
]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def ok(message: str) -> None:
    print(f"OK: {message}")


def validate_labels(failures: list[str]) -> None:
    labels = load_json(LABELS_PATH)
    names = {label["name"] for label in labels if isinstance(label, dict)}
    missing = REQUIRED_LABELS - names
    if missing:
        fail(f"missing labels: {', '.join(sorted(missing))}", failures)
    else:
        ok("required GitHub labels are defined")


def validate_automation_specs(failures: list[str]) -> None:
    expected = {
        "openhands-build",
        "openhands-review",
        "openhands-qa",
        "openhands-incident",
    }
    found = set()
    for spec_path in sorted(AUTOMATION_ROOT.glob("openhands-*/automation.prompt-preset.json")):
        spec = load_json(spec_path)
        folder = spec_path.parent.name
        found.add(folder)
        prompt_path = spec_path.parent / spec.get("prompt_file", "")
        if spec.get("preset") != "prompt":
            fail(f"{spec_path} is not a prompt preset spec", failures)
        if not prompt_path.exists():
            fail(f"{spec_path} references missing prompt file", failures)
            continue
        prompt = prompt_path.read_text(encoding="utf-8")
        trigger = spec.get("trigger", {})
        trigger_filter = trigger.get("filter", "")
        if folder not in trigger_filter:
            fail(f"{spec_path} filter does not mention its trigger label", failures)
        if f"label.name == '{folder}'" not in trigger_filter:
            fail(f"{spec_path} filter must gate label events on label.name == '{folder}'", failures)
        for phrase in ["Human Control", "Cost And Security", "What You Post Back To GitHub"]:
            if phrase not in prompt:
                fail(f"{prompt_path} missing demo-friendly section: {phrase}", failures)
        if spec.get("timeout", 0) > 600:
            fail(f"{spec_path} timeout exceeds preset-friendly 600 seconds", failures)
    missing = expected - found
    if missing:
        fail(f"missing automation specs: {', '.join(sorted(missing))}", failures)
    else:
        ok("all GitHub automation specs are present")


def validate_env(offline: bool, failures: list[str]) -> None:
    if offline:
        ok("offline mode skips secret/env presence checks")
        return
    missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
    if missing:
        fail(f"missing required env names: {', '.join(missing)}", failures)
    else:
        ok("required env names are set; values were not printed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="skip live env/API checks")
    args = parser.parse_args()

    failures: list[str] = []
    validate_labels(failures)
    validate_automation_specs(failures)
    validate_env(args.offline, failures)
    if failures:
        print(f"Preflight failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1
    print("Preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
