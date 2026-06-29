import json

from petstore_app import cloud_run_app


def test_visible_pets_excludes_pending_by_default(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    pets = cloud_run_app.visible_pets()

    assert {pet.status for pet in pets} == {"available"}
    assert "Nova" not in {pet.name for pet in pets}


def test_incident_mode_detection_with_proper_filtering(monkeypatch, tmp_path) -> None:
    config_path = tmp_path / "runtime.json"
    config_path.write_text(json.dumps({"mode": cloud_run_app.INCIDENT_MODE}))
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", config_path)
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    pets = cloud_run_app.visible_pets()
    payload = cloud_run_app.status_payload()

    assert "Nova" not in {pet.name for pet in pets}
    assert {pet.status for pet in pets} == {"available"}
    assert payload["status"] == "degraded"
    assert payload["incident"]["error_code"] == "PENDING_PET_VISIBLE"


def test_runtime_remediation_restores_healthy_mode(monkeypatch, tmp_path) -> None:
    config_path = tmp_path / "runtime.json"
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", config_path)
    cloud_run_app.write_runtime_config({"mode": cloud_run_app.INCIDENT_MODE})

    cloud_run_app.write_runtime_config({"mode": cloud_run_app.HEALTHY_MODE})

    assert cloud_run_app.current_mode() == "healthy"
    assert cloud_run_app.status_payload()["status"] == "healthy"


def test_pending_pet_never_visible_regression(monkeypatch, tmp_path) -> None:
    """Regression test for KAN-20: Nova (pet-103, pending) must never appear in visible pets."""
    config_path = tmp_path / "runtime.json"
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", config_path)
    
    for mode in [cloud_run_app.HEALTHY_MODE, cloud_run_app.INCIDENT_MODE]:
        config_path.write_text(json.dumps({"mode": mode}))
        pets = cloud_run_app.visible_pets()
        
        pet_ids = {pet.id for pet in pets}
        pet_names = {pet.name for pet in pets}
        pet_statuses = {pet.status for pet in pets}
        
        assert "pet-103" not in pet_ids, f"Nova (pet-103) should not be visible in {mode} mode"
        assert "Nova" not in pet_names, f"Nova should not be visible by name in {mode} mode"
        assert pet_statuses == {"available"}, f"Only available pets should be visible in {mode} mode"
