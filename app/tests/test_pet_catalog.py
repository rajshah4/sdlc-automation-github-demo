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


def test_search_pets_empty_status_defaults_to_available() -> None:
    """Regression test for KAN-63: empty status should default to available."""
    results = search_pets(status="")

    assert all(pet.status == "available" for pet in results), \
        "Empty status should filter to available pets only"
    assert "Nova" not in [pet.name for pet in results], \
        "Pending pet Nova should not appear in default search"


def test_search_pets_whitespace_status_defaults_to_available() -> None:
    """Regression test for KAN-63: whitespace-only status should default to available."""
    results = search_pets(status="  ")

    assert all(pet.status == "available" for pet in results)
    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)
