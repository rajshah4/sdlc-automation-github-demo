import json

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


def test_api_pets_excludes_pending_by_default(monkeypatch, tmp_path) -> None:
    """Regression test for KAN-26: API must exclude pending pets from default catalog."""
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    from unittest.mock import Mock
    handler = Mock(spec=cloud_run_app.PetstoreHandler)
    handler.route_get = cloud_run_app.PetstoreHandler.route_get.__get__(handler, cloud_run_app.PetstoreHandler)
    
    status, body, content_type = handler.route_get("/api/pets", {}, "test-request-id")

    assert status == 200
    assert content_type == "application/json"
    pet_ids = [pet["id"] for pet in body["pets"]]
    pet_names = [pet["name"] for pet in body["pets"]]
    assert "pet-103" not in pet_ids, "Nova (pending) should not appear in default /api/pets"
    assert "Nova" not in pet_names, "Nova (pending) should not appear in default /api/pets"
    assert "pet-100" in pet_ids
    assert "pet-101" in pet_ids
    assert "pet-102" in pet_ids
    assert len(body["pets"]) == 3


def test_api_pets_returns_pending_when_explicitly_requested(monkeypatch, tmp_path) -> None:
    """Support workflows must be able to search for pending pets explicitly."""
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    from unittest.mock import Mock
    handler = Mock(spec=cloud_run_app.PetstoreHandler)
    handler.route_get = cloud_run_app.PetstoreHandler.route_get.__get__(handler, cloud_run_app.PetstoreHandler)
    
    status, body, content_type = handler.route_get("/api/pets", {"status": ["pending"]}, "test-request-id")

    assert status == 200
    assert content_type == "application/json"
    pet_ids = [pet["id"] for pet in body["pets"]]
    pet_names = [pet["name"] for pet in body["pets"]]
    assert "pet-103" in pet_ids, "Nova (pending) should appear when status=pending"
    assert "Nova" in pet_names, "Nova (pending) should appear when status=pending"
    assert len(body["pets"]) == 1


def test_api_pets_filters_by_available_when_explicit(monkeypatch, tmp_path) -> None:
    """Explicit available filter should work the same as default."""
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    from unittest.mock import Mock
    handler = Mock(spec=cloud_run_app.PetstoreHandler)
    handler.route_get = cloud_run_app.PetstoreHandler.route_get.__get__(handler, cloud_run_app.PetstoreHandler)
    
    status, body, content_type = handler.route_get("/api/pets", {"status": ["available"]}, "test-request-id")

    assert status == 200
    assert content_type == "application/json"
    pet_ids = [pet["id"] for pet in body["pets"]]
    assert "pet-103" not in pet_ids
    assert len(body["pets"]) == 3
