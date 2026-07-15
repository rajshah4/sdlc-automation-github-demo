import json

from petstore_app import cloud_run_app


def test_visible_pets_excludes_pending_by_default(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    pets = cloud_run_app.visible_pets()

    assert {pet.status for pet in pets} == {"available"}
    assert "Nova" not in {pet.name for pet in pets}


def test_incident_mode_does_not_expose_pending_pets(monkeypatch, tmp_path) -> None:
    """Regression test for KAN-105: incident mode should not affect catalog filtering."""
    config_path = tmp_path / "runtime.json"
    config_path.write_text(json.dumps({"mode": cloud_run_app.INCIDENT_MODE}))
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", config_path)
    monkeypatch.setenv("INCIDENT_MODE", "healthy")

    pets = cloud_run_app.visible_pets()
    payload = cloud_run_app.status_payload()

    # Incident mode still reports degraded status for observability
    assert payload["status"] == "degraded"
    assert payload["incident"]["error_code"] == "PENDING_PET_VISIBLE"
    
    # But pending pets are no longer exposed to customers
    assert {pet.status for pet in pets} == {"available"}
    assert "Nova" not in {pet.name for pet in pets}


def test_runtime_remediation_restores_healthy_mode(monkeypatch, tmp_path) -> None:
    config_path = tmp_path / "runtime.json"
    monkeypatch.setattr(cloud_run_app, "RUNTIME_CONFIG_PATH", config_path)
    cloud_run_app.write_runtime_config({"mode": cloud_run_app.INCIDENT_MODE})

    cloud_run_app.write_runtime_config({"mode": cloud_run_app.HEALTHY_MODE})

    assert cloud_run_app.current_mode() == "healthy"
    assert cloud_run_app.status_payload()["status"] == "healthy"
