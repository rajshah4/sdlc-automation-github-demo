from petstore_app.telemetry import adoption_validation_error_event, search_latency_event


def test_adoption_validation_error_event_matches_gcp_schema() -> None:
    event = adoption_validation_error_event(
        pet_id="pet-103",
        pet_status="pending",
        release_pr="42",
    )

    assert event["service"] == "sdlc-automation-petstore"
    assert event["component"] == "adoption-api"
    assert event["operation"] == "adoption.create_order"
    assert event["incident"]["type"] == "adoption_validation_error"
    assert event["incident"]["safe_to_remediate"] is False
    assert event["error_code"] == "PENDING_PET_ADOPTION_ATTEMPTED"
    assert event["release"]["pr"] == "42"


def test_search_latency_event_matches_gcp_schema() -> None:
    event = search_latency_event(
        query="dog",
        species="dog",
        duration_ms=1800,
    )

    assert event["service"] == "sdlc-automation-petstore"
    assert event["component"] == "catalog-api"
    assert event["operation"] == "catalog.search"
    assert event["incident"]["type"] == "search_latency"
    assert event["duration_ms"] == 1800
