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
    results = search_pets(max_age_months=15)

    assert [pet.name for pet in results] == ["Pip"]


def test_search_pets_filters_by_age_range() -> None:
    results = search_pets(min_age_months=10, max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_minimum_age_zero_returns_all() -> None:
    results = search_pets(min_age_months=0)

    assert len(results) == 3
    assert "Nova" not in [pet.name for pet in results]


def test_search_pets_age_filter_combines_with_status() -> None:
    results = search_pets(status="available", min_age_months=15)

    assert [pet.name for pet in results] == ["Mochi", "Scout"]
    assert "Nova" not in [pet.name for pet in results]


def test_search_pets_age_filter_combines_with_species() -> None:
    results = search_pets(species="dog", status="pending", max_age_months=20)

    assert [pet.name for pet in results] == ["Nova"]


def test_search_pets_rejects_negative_minimum_age() -> None:
    with pytest.raises(ValueError, match="min_age_months must be non-negative"):
        search_pets(min_age_months=-1)


def test_search_pets_rejects_negative_maximum_age() -> None:
    with pytest.raises(ValueError, match="max_age_months must be non-negative"):
        search_pets(max_age_months=-1)


def test_search_pets_rejects_inverted_age_range() -> None:
    with pytest.raises(ValueError, match="min_age_months must not exceed max_age_months"):
        search_pets(min_age_months=20, max_age_months=10)
