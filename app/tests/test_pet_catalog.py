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


def test_search_pets_treats_empty_status_as_available() -> None:
    """Empty status parameter should default to 'available' per product rules."""
    results_with_empty_status = search_pets(status="")
    results_with_default_status = search_pets()

    assert [pet.id for pet in results_with_empty_status] == [pet.id for pet in results_with_default_status]
    assert all(pet.status == "available" for pet in results_with_empty_status)
    assert "pet-103" not in [pet.id for pet in results_with_empty_status]


def test_search_pets_treats_whitespace_status_as_available() -> None:
    """Whitespace-only status parameter should default to 'available'."""
    results = search_pets(status="  ")

    assert all(pet.status == "available" for pet in results)
    assert "pet-103" not in [pet.id for pet in results]
