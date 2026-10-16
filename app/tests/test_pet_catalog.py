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
    """Empty or whitespace-only status should default to 'available'."""
    results_empty = search_pets(status="")
    results_whitespace = search_pets(status="   ")
    results_default = search_pets()

    assert len(results_empty) == 3
    assert len(results_whitespace) == 3
    assert all(pet.status == "available" for pet in results_empty)
    assert all(pet.status == "available" for pet in results_whitespace)
    assert [pet.id for pet in results_empty] == [pet.id for pet in results_default]
