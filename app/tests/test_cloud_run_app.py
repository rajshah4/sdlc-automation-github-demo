import json
from http.server import HTTPServer
from io import BytesIO
from unittest.mock import Mock

from petstore_app import cloud_run_app


def test_visible_pets_excludes_pending_by_default(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    pets = cloud_run_app.visible_pets()

    assert {pet.status for pet in pets} == {"available"}
    assert "Nova" not in {pet.name for pet in pets}


def test_bad_catalog_filter_exposes_pending_pet(monkeypatch, tmp_path) -> None:
    config_path = tmp_path / "runtime.json"
    config_path.write_text(json.dumps({"mode": cloud_run_app.INCIDENT_MODE}))
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", config_path)
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    pets = cloud_run_app.visible_pets()
    payload = cloud_run_app.status_payload()

    assert "Nova" in {pet.name for pet in pets}
    assert payload["status"] == "degraded"
    assert payload["incident"]["error_code"] == "PENDING_PET_VISIBLE"


def test_runtime_remediation_restores_healthy_mode(monkeypatch, tmp_path) -> None:
    config_path = tmp_path / "runtime.json"
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", config_path)
    cloud_run_app.write_runtime_config({"mode": cloud_run_app.INCIDENT_MODE})

    cloud_run_app.write_runtime_config({"mode": cloud_run_app.HEALTHY_MODE})

    assert cloud_run_app.current_mode() == "healthy"
    assert cloud_run_app.status_payload()["status"] == "healthy"


def test_api_pets_endpoint_excludes_pending_by_default(monkeypatch, tmp_path) -> None:
    """Regression test for KAN-58: /api/pets must not return pending pets by default."""
    from petstore_app.catalog import search_pets
    
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")
    
    # Test the search_pets function that the endpoint now uses
    pets = search_pets()  # Default status="available"
    
    pet_names = [pet.name for pet in pets]
    pet_ids = [pet.id for pet in pets]
    pet_statuses = [pet.status for pet in pets]
    
    assert "Nova" not in pet_names, "Nova (pet-103) is pending and should not appear"
    assert "pet-103" not in pet_ids, "Pending pet pet-103 should not appear in default API response"
    assert all(status == "available" for status in pet_statuses), "Default /api/pets must only return available pets"


def test_api_pets_endpoint_can_explicitly_request_pending(monkeypatch, tmp_path) -> None:
    """Pending pets should be visible when explicitly requested via status parameter."""
    from petstore_app.catalog import search_pets
    
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")
    
    # Test the search_pets function with status="pending"
    pets = search_pets(status="pending")
    
    pet_names = [pet.name for pet in pets]
    
    assert "Nova" in pet_names, "Nova should be visible when explicitly requesting pending pets"
