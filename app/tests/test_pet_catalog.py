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


def test_search_pets_sorts_by_adoption_fee() -> None:
    results = search_pets(sort_by="adoption_fee")

    assert [pet.name for pet in results] == ["Pip", "Mochi", "Scout"]
    assert [pet.adoption_fee_cents for pet in results] == [4500, 7500, 12500]


def test_search_pets_default_behavior_unchanged_without_sorting() -> None:
    results = search_pets()

    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


def test_search_pets_sorts_with_species_filter() -> None:
    results = search_pets(species="dog", status="available", sort_by="adoption_fee")

    assert [pet.name for pet in results] == ["Scout"]


def test_search_pets_sorts_with_tag_filter() -> None:
    results = search_pets(tag="indoor", sort_by="adoption_fee")

    assert [pet.name for pet in results] == ["Pip", "Mochi"]
    assert [pet.adoption_fee_cents for pet in results] == [4500, 7500]
