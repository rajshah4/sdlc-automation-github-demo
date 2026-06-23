"""Structured telemetry helpers for Petstore integration demos."""

from __future__ import annotations

from typing import Any


def adoption_validation_error_event(
    *,
    pet_id: str,
    pet_status: str,
    release_pr: str | None = None,
    provider: str = "github",
) -> dict[str, Any]:
    """Return the canonical structured log payload for adoption validation incidents."""
    return {
        "service": "sdlc-automation-petstore",
        "component": "adoption-api",
        "operation": "adoption.create_order",
        "severity": "ERROR",
        "provider": provider,
        "release": {
            "version": "demo",
            "pr": release_pr or "unknown",
        },
        "incident": {
            "type": "adoption_validation_error",
            "mode": "synthetic_demo",
            "safe_to_remediate": False,
        },
        "pet_id": pet_id,
        "pet_status": pet_status,
        "error_code": "PENDING_PET_ADOPTION_ATTEMPTED",
        "message": "Pending pet was submitted to adoption order flow",
    }


def search_latency_event(
    *,
    query: str,
    species: str | None,
    duration_ms: int,
    release_pr: str | None = None,
    provider: str = "github",
) -> dict[str, Any]:
    """Return the canonical structured log payload for synthetic search latency."""
    return {
        "service": "sdlc-automation-petstore",
        "component": "catalog-api",
        "operation": "catalog.search",
        "severity": "WARNING",
        "provider": provider,
        "release": {
            "version": "demo",
            "pr": release_pr or "unknown",
        },
        "incident": {
            "type": "search_latency",
            "mode": "synthetic_demo",
            "safe_to_remediate": False,
        },
        "duration_ms": duration_ms,
        "query": query,
        "species": species,
    }
