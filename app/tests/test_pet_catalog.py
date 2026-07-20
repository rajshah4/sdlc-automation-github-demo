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


def test_search_pets_filters_by_temperament() -> None:
    results = search_pets(temperament="calm")

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_filters_by_temperament_excludes_non_matching() -> None:
    results = search_pets(temperament="calm")

    assert "Scout" not in [pet.name for pet in results]
    assert "Pip" not in [pet.name for pet in results]


def test_search_pets_temperament_none_returns_all_available() -> None:
    results = search_pets(temperament=None)

    assert len(results) == 3
    assert [pet.id for pet in results] == ["pet-100", "pet-101", "pet-102"]


def test_search_pets_temperament_with_species_filter() -> None:
    results = search_pets(species="cat", temperament="calm")

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_temperament_respects_status_default() -> None:
    results = search_pets(temperament="active")

    assert [pet.name for pet in results] == ["Scout"]
    assert "Nova" not in [pet.name for pet in results]


def test_search_pets_temperament_case_insensitive() -> None:
    results = search_pets(temperament="Calm")

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_temperament_with_whitespace() -> None:
    results = search_pets(temperament="  calm  ")

    assert [pet.name for pet in results] == ["Mochi"]
