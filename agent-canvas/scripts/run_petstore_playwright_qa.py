#!/usr/bin/env python3
# Runs the Petstore browser QA evidence flow against a temporary local server.
"""Run the Petstore max-fee Playwright QA flow on an available local port."""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", required=True, type=Path)
    parser.add_argument("--playwright-node-path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    artifact_dir = args.artifact_dir.resolve()
    env = os.environ.copy()
    if args.playwright_node_path:
        env["NODE_PATH"] = args.playwright_node_path

    command = [
        sys.executable,
        str(ROOT / "skills" / "sdlc-qa" / "scripts" / "with_server.py"),
        "--server",
        f"{sys.executable} -m http.server {port} --bind 127.0.0.1 --directory app/web",
        "--port",
        str(port),
        "--",
        "node",
        str(ROOT / "app" / "web" / "tests" / "max-adoption-fee-filter.playwright.mjs"),
        "--url",
        url,
        "--artifact-dir",
        str(artifact_dir),
    ]
    print("Running Petstore Playwright QA:")
    print(" ".join(command))
    completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
