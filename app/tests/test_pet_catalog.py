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


def test_search_pets_sort_by_fee_asc() -> None:
    results = search_pets(sort_by="fee_asc")

    # Available pets: Pip (4500), Mochi (7500), Scout (12500)
    assert [pet.name for pet in results] == ["Pip", "Mochi", "Scout"]
    assert [pet.adoption_fee_cents for pet in results] == [4500, 7500, 12500]


def test_search_pets_sort_by_fee_desc() -> None:
    results = search_pets(sort_by="fee_desc")

    # Available pets: Scout (12500), Mochi (7500), Pip (4500)
    assert [pet.name for pet in results] == ["Scout", "Mochi", "Pip"]
    assert [pet.adoption_fee_cents for pet in results] == [12500, 7500, 4500]


def test_search_pets_default_no_sort() -> None:
    results = search_pets()

    # Default order unchanged: Mochi, Scout, Pip (available pets in tuple order)
    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


def test_search_pets_sort_preserves_status_filter() -> None:
    # Only available pets should be sorted
    results = search_pets(status="available", sort_by="fee_asc")

    assert [pet.name for pet in results] == ["Pip", "Mochi", "Scout"]
    assert all(pet.status == "available" for pet in results)


def test_search_pets_sort_with_species_filter() -> None:
    # Add a test to ensure sorting works with other filters
    results = search_pets(species="dog", sort_by="fee_desc")

    # Only Scout is available dog
    assert [pet.name for pet in results] == ["Scout"]


@pytest.mark.parametrize("invalid_sort", ["name", "age", "invalid", "price"])
def test_search_pets_invalid_sort_by(invalid_sort: str) -> None:
    with pytest.raises(ValueError, match="sort_by"):
        search_pets(sort_by=invalid_sort)
