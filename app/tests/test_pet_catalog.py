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


def test_search_pets_preserves_default_order_when_sort_is_not_specified() -> None:
    results = search_pets()

    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


def test_search_pets_sorts_by_name_alphabetically() -> None:
    results = search_pets(sort_by="name")

    assert [pet.name for pet in results] == ["Mochi", "Pip", "Scout"]


def test_search_pets_sorts_by_name_case_insensitively() -> None:
    results = search_pets(sort_by="name")

    names = [pet.name for pet in results]
    assert names == sorted(names, key=str.lower)


def test_search_pets_applies_sort_to_filtered_results() -> None:
    results = search_pets(species="dog", sort_by="name")

    assert [pet.name for pet in results] == ["Scout"]
