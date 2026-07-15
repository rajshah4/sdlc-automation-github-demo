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


def test_search_pets_filters_by_max_age() -> None:
    results = search_pets(max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_excludes_pets_older_than_max_age() -> None:
    results = search_pets(max_age_months=15)

    assert [pet.name for pet in results] == ["Pip"]
    assert "Mochi" not in [pet.name for pet in results]
    assert "Scout" not in [pet.name for pet in results]


def test_search_pets_max_age_is_optional() -> None:
    results_with_age = search_pets(max_age_months=20)
    results_without_age = search_pets()

    assert len(results_without_age) >= len(results_with_age)


def test_search_pets_rejects_negative_age() -> None:
    with pytest.raises(ValueError, match="max_age_months cannot be negative"):
        search_pets(max_age_months=-5)


def test_search_pets_age_filter_preserves_status_filtering() -> None:
    results = search_pets(max_age_months=30)

    pet_names = [pet.name for pet in results]
    assert "Nova" not in pet_names  # pending pet excluded by default status


def test_search_pets_zero_age_is_valid() -> None:
    results = search_pets(max_age_months=0)

    assert results == []  # no pets aged exactly 0 months in test data

