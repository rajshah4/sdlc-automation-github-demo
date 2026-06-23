#!/usr/bin/env python3
"""Start local servers, run a command, then clean them up."""

from __future__ import annotations

import argparse
import shlex
import socket
import subprocess
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class ServerSpec:
    command: str
    port: int


def is_ready(port: int, timeout: int) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a command while one or more local servers are available.")
    parser.add_argument("--server", action="append", dest="servers", required=True)
    parser.add_argument("--port", action="append", dest="ports", type=int, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        raise SystemExit("No command supplied after --")
    if len(args.servers) != len(args.ports):
        raise SystemExit("Each --server must have a matching --port")
    return args


def main() -> int:
    args = parse_args()
    specs = [ServerSpec(command=cmd, port=port) for cmd, port in zip(args.servers, args.ports)]
    processes: list[subprocess.Popen[str]] = []

    try:
        for index, spec in enumerate(specs, start=1):
            print(f"Starting server {index}/{len(specs)} on port {spec.port}: {spec.command}")
            process = subprocess.Popen(
                shlex.split(spec.command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            processes.append(process)
            if not is_ready(spec.port, args.timeout):
                raise RuntimeError(f"Server on port {spec.port} was not ready within {args.timeout}s")
            print(f"Server ready on port {spec.port}")

        print(f"Running command: {' '.join(args.command)}")
        completed = subprocess.run(args.command, check=False)
        return completed.returncode
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        if processes:
            print("Stopped local server processes")


if __name__ == "__main__":
    raise SystemExit(main())
