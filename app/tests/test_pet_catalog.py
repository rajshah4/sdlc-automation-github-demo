import pytest

from petstore_app.catalog import count_available, search_pets


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


def test_count_available_returns_all_available_pets_by_default() -> None:
    count = count_available()

    assert count == 3


def test_count_available_filters_by_species() -> None:
    count = count_available(species="dog")

    assert count == 1


def test_count_available_filters_by_query() -> None:
    count = count_available(query="Mochi")

    assert count == 1


def test_count_available_filters_by_tag() -> None:
    count = count_available(tag="indoor")

    assert count == 2


def test_count_available_excludes_pending_pets() -> None:
    count = count_available(species="dog", status="available")

    assert count == 1


def test_count_available_can_count_pending_pets_when_requested() -> None:
    count = count_available(status="pending")

    assert count == 1


def test_count_available_returns_zero_when_no_matches() -> None:
    count = count_available(query="nonexistent")

    assert count == 0


def test_count_available_with_multiple_filters() -> None:
    count = count_available(species="cat", tag="indoor")

    assert count == 1
