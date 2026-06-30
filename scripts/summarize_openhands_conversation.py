#!/usr/bin/env python3
"""Summarize OpenHands conversation timing and usage without printing secrets."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key.replace("_", "").isalnum():
            os.environ.setdefault(key, value.strip().strip("'").strip('"'))


def api_key() -> str:
    value = (
        os.getenv("OPENHANDS_API_KEY_ORG")
        or os.getenv("OPENHANDS_API_KEY_GITHUB")
        or os.getenv("OPENHANDS_API_KEY_RAJISTICS")
        or os.getenv("OPENHANDS_API_KEY")
    )
    if not value:
        raise SystemExit("OpenHands API key is required")
    return value


def host() -> str:
    return (
        os.getenv("OPENHANDS_HOST_GITHUB")
        or os.getenv("OPENHANDS_HOST_RAJISTICS")
        or os.getenv("OPENHANDS_HOST")
        or "https://app.replicated.rajistics.com"
    ).rstrip("/")


def fetch_events(conversation_id: str, limit: int) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    page_id = ""
    while True:
        params = {"limit": min(limit, 100), "sort_order": "TIMESTAMP"}
        if page_id:
            params["page_id"] = page_id
        endpoint = f"{host()}/api/v1/conversation/{conversation_id}/events/search?{urlencode(params)}"
        request = Request(
            endpoint,
            headers={"X-Access-Token": api_key()},
        )
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenHands API returned {exc.code}: {body}") from exc
        batch = payload.get("events") or payload.get("data") or payload.get("items") or []
        events.extend(batch)
        page_id = payload.get("next_page_id") or payload.get("next") or ""
        if not page_id or len(batch) < min(limit, 100):
            break
    return events


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def event_time(event: dict[str, Any]) -> str | None:
    return event.get("timestamp") or event.get("created_at")


def find_usage(node: Any) -> dict[str, Any] | None:
    if isinstance(node, dict):
        usage = node.get("usage_to_metrics")
        if isinstance(usage, dict):
            return usage
        for value in node.values():
            found = find_usage(value)
            if found:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_usage(value)
            if found:
                return found
    return None


def final_usage(events: list[dict[str, Any]]) -> dict[str, Any]:
    latest: dict[str, Any] = {}
    for event in events:
        usage = find_usage(event)
        if usage:
            latest = usage
    return latest


def compact_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {}
    for profile, values in metrics.items():
        if not isinstance(values, dict):
            continue
        compact[profile] = {
            key: values.get(key)
            for key in (
                "accumulated_cost",
                "accumulated_token_usage",
                "prompt_tokens",
                "cache_read_tokens",
                "cache_write_tokens",
                "completion_tokens",
                "reasoning_tokens",
                "per_turn_token",
                "context_window",
            )
            if key in values
        }
    return compact


def summarize(conversation_id: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    timestamps = [parse_time(event_time(event)) for event in events if event_time(event)]
    timestamps = [timestamp for timestamp in timestamps if timestamp]
    started = min(timestamps).isoformat() if timestamps else None
    ended = max(timestamps).isoformat() if timestamps else None
    elapsed = None
    if timestamps:
        elapsed = round((max(timestamps) - min(timestamps)).total_seconds() / 60, 2)
    return {
        "conversation_id": conversation_id,
        "conversation_url": f"{host()}/conversations/{conversation_id}",
        "event_count": len(events),
        "event_types": dict(Counter(event.get("kind") or event.get("type") for event in events)),
        "started_at": started,
        "ended_at": ended,
        "elapsed_minutes": elapsed,
        "usage": compact_metrics(final_usage(events)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("conversation_id")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if args.env_file:
        load_env_file(args.env_file)
    print(json.dumps(summarize(args.conversation_id, fetch_events(args.conversation_id, args.limit)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
