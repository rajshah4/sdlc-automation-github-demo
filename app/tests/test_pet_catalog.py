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


def test_search_pets_filters_by_min_age() -> None:
    # Pets: Mochi=18mo, Scout=28mo, Pip=9mo (available), Nova=14mo (pending)
    results = search_pets(min_age_months=15)

    assert [pet.name for pet in results] == ["Mochi", "Scout"]


def test_search_pets_filters_by_max_age() -> None:
    results = search_pets(max_age_months=15)

    assert [pet.name for pet in results] == ["Pip"]


def test_search_pets_filters_by_age_range() -> None:
    results = search_pets(min_age_months=10, max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_includes_pets_at_min_age_boundary() -> None:
    results = search_pets(min_age_months=18)

    assert any(pet.name == "Mochi" for pet in results)


def test_search_pets_includes_pets_at_max_age_boundary() -> None:
    results = search_pets(max_age_months=18)

    assert any(pet.name == "Mochi" for pet in results)


def test_search_pets_rejects_negative_min_age() -> None:
    with pytest.raises(ValueError, match="min_age_months"):
        search_pets(min_age_months=-1)


def test_search_pets_rejects_negative_max_age() -> None:
    with pytest.raises(ValueError, match="max_age_months"):
        search_pets(max_age_months=-1)


def test_search_pets_rejects_inverted_age_range() -> None:
    with pytest.raises(ValueError, match="min_age_months must be <= max_age_months"):
        search_pets(min_age_months=20, max_age_months=10)


def test_search_pets_no_age_filter_when_both_none() -> None:
    all_available = search_pets()
    with_none_ages = search_pets(min_age_months=None, max_age_months=None)

    assert [pet.id for pet in all_available] == [pet.id for pet in with_none_ages]
