"""Dependency-free Cloud Run surface for the Petstore SRE demo."""

from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .adoptions import create_adoption_order
from .catalog import PETS, Pet, search_pets
from .telemetry import adoption_validation_error_event

APP_NAME = os.getenv("APP_NAME", "sdlc-automation-petstore")
SERVICE_NAME = os.getenv("K_SERVICE", os.getenv("GCP_SERVICE", APP_NAME))
REVISION = os.getenv("K_REVISION", "local")
REGION = os.getenv("GCP_REGION", os.getenv("GOOGLE_CLOUD_REGION", "unknown"))
RUNTIME_CONFIG_PATH = Path(
    os.getenv("RUNTIME_CONFIG_PATH", "/tmp/sdlc-automation-petstore-runtime-config.json")
)

INCIDENT_TYPE = "petstore_website_catalog_regression"
INCIDENT_MODE = "bad_catalog_filter"
HEALTHY_MODE = "healthy"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit_log(severity: str, message: str, **fields: Any) -> None:
    payload = {
        "severity": severity,
        "message": message,
        "service": SERVICE_NAME,
        "app": APP_NAME,
        "revision": REVISION,
        "region": REGION,
        "timestamp": utc_now(),
        **fields,
    }
    print(json.dumps(payload, sort_keys=True), flush=True)


def read_runtime_config() -> dict[str, Any]:
    try:
        data = json.loads(RUNTIME_CONFIG_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {"mode": INCIDENT_MODE, "config_error": "runtime config is not valid JSON"}
    return data if isinstance(data, dict) else {}


def write_runtime_config(config: dict[str, Any]) -> None:
    RUNTIME_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_CONFIG_PATH.write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")


def current_mode() -> str:
    override = read_runtime_config().get("mode")
    if isinstance(override, str) and override.strip():
        return override.strip().lower()
    return os.getenv("INCIDENT_MODE", HEALTHY_MODE).strip().lower() or HEALTHY_MODE


def incident() -> dict[str, Any] | None:
    if current_mode() != INCIDENT_MODE:
        return None
    return {
        "type": INCIDENT_TYPE,
        "status_code": 500,
        "title": "Petstore catalog regression",
        "summary": "The website is showing pending pets in the available-pet experience.",
        "component": "petstore-web",
        "operation": "web.available_pets",
        "error_code": "PENDING_PET_VISIBLE",
        "risk_level": "LOW",
        "safe_to_remediate": True,
        "recommended_action": "Restore the runtime catalog filter to available pets only.",
        "remediation": "catalog_filter_runtime_override",
    }


def visible_pets() -> list[Pet]:
    if current_mode() == INCIDENT_MODE:
        return list(PETS)
    return [pet for pet in PETS if pet.status == "available"]


def pet_to_dict(pet: Pet) -> dict[str, Any]:
    return {
        "id": pet.id,
        "name": pet.name,
        "species": pet.species,
        "status": pet.status,
        "tags": list(pet.tags),
        "age_months": pet.age_months,
        "adoption_fee_cents": pet.adoption_fee_cents,
    }


def status_payload() -> dict[str, Any]:
    problem = incident()
    return {
        "service": SERVICE_NAME,
        "status": "degraded" if problem else "healthy",
        "mode": current_mode(),
        "revision": REVISION,
        "runtime_config_path": str(RUNTIME_CONFIG_PATH),
        "incident": problem,
    }


def log_catalog_regression_if_present(request_id: str) -> None:
    problem = incident()
    if not problem:
        return
    pending_pets = [pet for pet in visible_pets() if pet.status == "pending"]
    if not pending_pets:
        return
    emit_log(
        "ERROR",
        "pending pets visible on available-pets website",
        request_id=request_id,
        component=problem["component"],
        operation=problem["operation"],
        incident=problem,
        error_code=problem["error_code"],
        pending_pet_ids=[pet.id for pet in pending_pets],
        pending_pet_names=[pet.name for pet in pending_pets],
    )


def render_home(request_id: str) -> str:
    problem = incident()
    pets = search_pets()
    log_catalog_regression_if_present(request_id)
    status = "degraded" if problem else "healthy"
    items = "\n".join(
        f"<li><strong>{escape(pet.name)}</strong> "
        f"<span>{escape(pet.species)} · {escape(pet.status)} · ${pet.adoption_fee_cents // 100}</span></li>"
        for pet in pets
    )
    banner = (
        "<section class='banner'>Catalog regression detected: pending pets are visible.</section>"
        if problem
        else "<section class='banner ok'>Catalog filter healthy.</section>"
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Petstore SDLC Demo</title>
    <style>
      body {{ font-family: system-ui, sans-serif; margin: 0; background: #f8fafc; color: #172033; }}
      main {{ max-width: 840px; margin: 48px auto; padding: 0 24px; }}
      .banner {{ padding: 14px 16px; border: 1px solid #f97316; background: #fff7ed; border-radius: 8px; }}
      .banner.ok {{ border-color: #16a34a; background: #f0fdf4; }}
      ul {{ display: grid; gap: 12px; padding: 0; list-style: none; }}
      li {{ background: white; border: 1px solid #d7dee8; border-radius: 8px; padding: 14px 16px; }}
      span {{ display: block; color: #536174; margin-top: 4px; }}
      code {{ background: #e5e7eb; padding: 2px 5px; border-radius: 4px; }}
    </style>
  </head>
  <body>
    <main>
      <h1>Petstore SDLC Demo</h1>
      <p>Status: <code>{escape(status)}</code></p>
      {banner}
      <h2>Available Pets</h2>
      <ul>{items}</ul>
    </main>
  </body>
</html>"""


class PetstoreHandler(BaseHTTPRequestHandler):
    server_version = "PetstoreSDLCDemo/1.0"

    def do_GET(self) -> None:
        started = time.monotonic()
        request_id = self.headers.get("X-Cloud-Trace-Context", "").split("/", 1)[0] or str(uuid.uuid4())
        parsed = urlparse(self.path)
        try:
            status, body, content_type = self.route_get(parsed.path, parse_qs(parsed.query), request_id)
        except Exception as exc:  # pragma: no cover - defensive server boundary
            emit_log("ERROR", "unhandled request error", request_id=request_id, error=type(exc).__name__)
            status, body, content_type = 500, {"error": "internal server error"}, "application/json"
        self.send_body(status, body, content_type)
        self.log_request_event(started, request_id, parsed.path, status)

    def do_POST(self) -> None:
        started = time.monotonic()
        request_id = self.headers.get("X-Cloud-Trace-Context", "").split("/", 1)[0] or str(uuid.uuid4())
        parsed = urlparse(self.path)
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            payload = json.loads(raw or "{}")
            status, body = self.route_post(parsed.path, payload, request_id)
        except json.JSONDecodeError:
            status, body = 400, {"error": "request body must be JSON"}
        except Exception as exc:  # pragma: no cover - defensive server boundary
            emit_log("ERROR", "unhandled admin request error", request_id=request_id, error=type(exc).__name__)
            status, body = 500, {"error": "internal server error"}
        self.send_body(status, body, "application/json")
        self.log_request_event(started, request_id, parsed.path, status)

    def route_get(
        self, path: str, query: dict[str, list[str]], request_id: str
    ) -> tuple[int, str | dict[str, Any], str]:
        problem = incident()
        if path == "/":
            return 200, render_home(request_id), "text/html; charset=utf-8"
        if path in {"/healthz", "/api/status"}:
            if problem:
                emit_log(
                    "ERROR",
                    "health check failed for catalog regression",
                    request_id=request_id,
                    incident=problem,
                    component=problem["component"],
                    operation=problem["operation"],
                    error_code=problem["error_code"],
                )
                return 500, status_payload(), "application/json"
            return 200, status_payload(), "application/json"
        if path == "/api/pets":
            log_catalog_regression_if_present(request_id)
            available_pets = search_pets()
            return 200, {"pets": [pet_to_dict(pet) for pet in available_pets]}, "application/json"
        if path == "/api/adoptions":
            pet_id = (query.get("pet_id") or [""])[0]
            try:
                order = create_adoption_order(pet_id, "demo.adopter@example.com")
            except ValueError as exc:
                pet_status = next((pet.status for pet in PETS if pet.id == pet_id), "unknown")
                event = adoption_validation_error_event(pet_id=pet_id, pet_status=pet_status)
                emit_log("ERROR", str(exc), request_id=request_id, **event)
                return 400, {"error": str(exc), "pet_id": pet_id}, "application/json"
            return 200, {"order": order.__dict__}, "application/json"
        return 404, {"error": "not found"}, "application/json"

    def route_post(self, path: str, payload: dict[str, Any], request_id: str) -> tuple[int, dict[str, Any]]:
        if path not in {"/api/admin/state", "/api/admin/remediate/catalog-filter"}:
            return 404, {"error": "not found"}
        if not self.admin_authorized():
            return 401, {"error": "missing or invalid demo admin token"}
        if path == "/api/admin/state":
            mode = str(payload.get("mode", "")).strip().lower()
            if mode not in {HEALTHY_MODE, INCIDENT_MODE}:
                return 400, {"error": f"mode must be {HEALTHY_MODE} or {INCIDENT_MODE}"}
            write_runtime_config({"mode": mode, "updated_at": utc_now(), "source": "admin_state"})
            emit_log("WARNING", "demo runtime state changed", request_id=request_id, mode=mode)
            return 200, status_payload()
        write_runtime_config(
            {
                "mode": HEALTHY_MODE,
                "updated_at": utc_now(),
                "source": "approved_runtime_remediation",
                "reason": payload.get("reason", "catalog filter remediation"),
            }
        )
        emit_log(
            "WARNING",
            "approved runtime remediation applied",
            request_id=request_id,
            remediation="catalog_filter_runtime_override",
        )
        return 200, status_payload()

    def admin_authorized(self) -> bool:
        expected = os.getenv("DEMO_ADMIN_TOKEN", "")
        if not expected:
            return False
        provided = self.headers.get("X-Demo-Admin-Token", "")
        auth = self.headers.get("Authorization", "")
        if auth.lower().startswith("bearer "):
            provided = auth.split(" ", 1)[1]
        return provided == expected

    def send_body(self, status: int, body: str | dict[str, Any], content_type: str) -> None:
        if isinstance(body, str):
            data = body.encode("utf-8")
        else:
            data = json.dumps(body, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_request_event(self, started: float, request_id: str, path: str, status: int) -> None:
        emit_log(
            "ERROR" if status >= 500 else "INFO",
            "request completed",
            request_id=request_id,
            method=self.command,
            path=path,
            status=status,
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def log_message(self, format: str, *args: Any) -> None:
        return


def run() -> None:
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), PetstoreHandler)
    emit_log("INFO", "starting Petstore Cloud Run server", port=port, mode=current_mode())
    server.serve_forever()


if __name__ == "__main__":
    run()
