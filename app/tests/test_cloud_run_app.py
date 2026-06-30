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


def test_api_pets_endpoint_uses_catalog_search_in_healthy_mode(monkeypatch, tmp_path) -> None:
    """Regression test for KAN-33: /api/pets must use catalog search with default available filter."""
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    class MockHandler:
        def route_get(self, path, query, request_id):
            return cloud_run_app.PetstoreHandler.route_get(self, path, query, request_id)

    handler = MockHandler()
    status, body, content_type = handler.route_get("/api/pets", {}, "test-request-id")

    assert status == 200
    assert content_type == "application/json"
    pet_names = [pet["name"] for pet in body["pets"]]
    pet_statuses = {pet["status"] for pet in body["pets"]}
    assert "Nova" not in pet_names, "Pending pet Nova (pet-103) should not appear in default search"
    assert pet_statuses == {"available"}, "Only available pets should be returned by default"
