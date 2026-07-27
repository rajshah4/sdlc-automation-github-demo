import pytest

from petstore_app.catalog import search_pets


def test_search_pets_filters_by_species_and_status() -> None:
    results = search_pets(species="dog")

    assert [pet.id for pet in results] == ["pet-101"]


def test_search_pets_can_find_pending_pets_when_requested() -> None:
    results = search_pets(species="dog", status="pending")

    assert [pet.name for pet in results] == ["Nova"]


def test_search_pets_filters_by_tag() -> None:
    results = search_pets(tag="indoor")

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)


def test_search_pets_empty_status_should_not_return_unavailable_pets() -> None:
    """Regression test: empty status string should not bypass status filtering."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Pending pet Nova should not appear with empty status"


def test_search_pets_defaults_to_available_only() -> None:
    """Default behavior should return only available pets."""
    results = search_pets()

    statuses = {pet.status for pet in results}
    assert statuses == {"available"}, "Default search should only return available pets"
    assert len(results) == 3, "Should return 3 available pets"
