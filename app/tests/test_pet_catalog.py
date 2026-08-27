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


def test_search_pets_filters_by_minimum_age() -> None:
    results = search_pets(min_age_months=15)

    assert [pet.name for pet in results] == ["Mochi", "Scout"]


def test_search_pets_filters_by_maximum_age() -> None:
    results = search_pets(max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_filters_by_age_range() -> None:
    results = search_pets(min_age_months=10, max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_age_filter_with_species() -> None:
    results = search_pets(species="dog", min_age_months=20)

    assert [pet.name for pet in results] == ["Scout"]


@pytest.mark.parametrize("min_age", [-1, -10])
def test_search_pets_validates_negative_min_age(min_age: int) -> None:
    with pytest.raises(ValueError, match="min_age_months must be non-negative"):
        search_pets(min_age_months=min_age)


@pytest.mark.parametrize("max_age", [-1, -10])
def test_search_pets_validates_negative_max_age(max_age: int) -> None:
    with pytest.raises(ValueError, match="max_age_months must be non-negative"):
        search_pets(max_age_months=max_age)


def test_search_pets_validates_inverted_range() -> None:
    with pytest.raises(ValueError, match="min_age_months cannot be greater than max_age_months"):
        search_pets(min_age_months=20, max_age_months=10)
