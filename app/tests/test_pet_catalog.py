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
    results = search_pets(min_age_months=18)

    assert [pet.name for pet in results] == ["Mochi", "Scout"]


def test_search_pets_filters_by_maximum_age() -> None:
    results = search_pets(max_age_months=10)

    assert [pet.name for pet in results] == ["Pip"]


def test_search_pets_filters_by_age_range() -> None:
    results = search_pets(min_age_months=10, max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_filters_by_wider_age_range() -> None:
    results = search_pets(min_age_months=8, max_age_months=19)

    assert sorted([pet.name for pet in results]) == ["Mochi", "Pip"]


def test_search_pets_age_range_with_species() -> None:
    results = search_pets(species="dog", min_age_months=20)

    assert [pet.name for pet in results] == ["Scout"]


def test_search_pets_age_filter_respects_default_status() -> None:
    results = search_pets(min_age_months=10, max_age_months=20)

    pet_names = [pet.name for pet in results]
    assert "Nova" not in pet_names


def test_search_pets_age_range_exact_boundary() -> None:
    results = search_pets(min_age_months=18, max_age_months=18)

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_min_age_zero_returns_all() -> None:
    results = search_pets(min_age_months=0)

    assert len(results) == 3


def test_search_pets_rejects_negative_min_age() -> None:
    with pytest.raises(ValueError, match="min_age_months cannot be negative"):
        search_pets(min_age_months=-1)


def test_search_pets_rejects_negative_max_age() -> None:
    with pytest.raises(ValueError, match="max_age_months cannot be negative"):
        search_pets(max_age_months=-5)


def test_search_pets_rejects_inverted_age_range() -> None:
    with pytest.raises(ValueError, match="min_age_months cannot exceed max_age_months"):
        search_pets(min_age_months=24, max_age_months=12)
