#!/usr/bin/env python3
"""Shared helpers for the Petstore Cloud Run SRE demo."""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "app"
DEFAULT_REGION = "us-central1"
DEFAULT_SERVICE = "sdlc-automation-petstore"
DEFAULT_LOG_FRESHNESS = "30m"


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project", default=os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT"))
    parser.add_argument("--region", default=os.getenv("GCP_REGION", DEFAULT_REGION))
    parser.add_argument("--service", default=os.getenv("GCP_SERVICE", DEFAULT_SERVICE))


def configure_gcloud_auth() -> None:
    """Activate service-account auth when a base64 JSON credential is supplied."""
    encoded = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_B64")
    if not encoded:
        return
    temp = tempfile.NamedTemporaryFile(prefix="petstore-gcp-", suffix=".json", delete=False)
    try:
        temp.write(base64.b64decode(encoded))
        temp.close()
        run(["gcloud", "auth", "activate-service-account", "--key-file", temp.name], check=True)
    finally:
        try:
            Path(temp.name).unlink()
        except FileNotFoundError:
            pass


def run(cmd: list[str], *, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"command failed: {cmd}")
    return result


def gcloud_json(args: list[str], *, project: str | None = None) -> Any:
    cmd = ["gcloud", *args, "--format=json"]
    if project:
        cmd.extend(["--project", project])
    result = run(cmd)
    return json.loads(result.stdout or "null")


def detect_project(project: str | None) -> str:
    if project:
        return project
    result = run(["gcloud", "config", "get-value", "project"], check=False)
    detected = result.stdout.strip()
    if not detected:
        raise RuntimeError("GCP project is required. Set GCP_PROJECT or pass --project.")
    return detected


def service_description(project: str, region: str, service: str) -> dict[str, Any]:
    return gcloud_json(["run", "services", "describe", service, "--region", region], project=project)


def service_url(project: str, region: str, service: str) -> str:
    desc = service_description(project, region, service)
    url = desc.get("status", {}).get("url")
    if not url:
        raise RuntimeError(f"Cloud Run service {service} has no status.url")
    return str(url)


def http_json(
    url: str,
    path: str,
    *,
    method: str = "GET",
    token: str | None = None,
    payload: dict[str, Any] | None = None,
    timeout: int = 20,
) -> dict[str, Any]:
    data = json.dumps(payload or {}).encode("utf-8") if method != "GET" else None
    headers = {"Accept": "application/json"}
    if method != "GET":
        headers["Content-Type"] = "application/json"
    if token:
        headers["X-Demo-Admin-Token"] = token
    request = urllib.request.Request(
        f"{url.rstrip('/')}{path}",
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            status = response.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        status = exc.code
    try:
        body: Any = json.loads(raw) if raw else None
    except json.JSONDecodeError:
        body = raw[:1000]
    return {"status": status, "ok": 200 <= status < 300, "body": body}


def freshness_to_since(freshness: str) -> str:
    value = freshness.strip().lower()
    if value.endswith("m"):
        delta = timedelta(minutes=int(value[:-1]))
    elif value.endswith("h"):
        delta = timedelta(hours=int(value[:-1]))
    else:
        delta = timedelta(minutes=30)
    return (datetime.now(timezone.utc) - delta).isoformat()


def cloud_logging_filter(service: str, freshness: str = DEFAULT_LOG_FRESHNESS) -> str:
    since = freshness_to_since(freshness)
    return (
        'resource.type="cloud_run_revision" '
        f'resource.labels.service_name="{service}" '
        f'timestamp>="{since}" '
        'jsonPayload.incident.type="petstore_website_catalog_regression"'
    )


def logs_explorer_url(project: str, service: str, freshness: str = DEFAULT_LOG_FRESHNESS) -> str:
    query = cloud_logging_filter(service, freshness)
    encoded = urllib.parse.quote(query, safe="")
    return f"https://console.cloud.google.com/logs/query;query={encoded}?project={project}"


def read_incident_logs(
    project: str,
    service: str,
    *,
    freshness: str = DEFAULT_LOG_FRESHNESS,
    limit: int = 25,
) -> list[dict[str, Any]]:
    return gcloud_json(
        [
            "logging",
            "read",
            cloud_logging_filter(service, freshness),
            f"--freshness={freshness}",
            f"--limit={limit}",
        ],
        project=project,
    ) or []


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))
