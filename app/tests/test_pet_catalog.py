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


def test_search_pets_filters_by_size_small() -> None:
    results = search_pets(size="small")

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_filters_by_size_medium() -> None:
    results = search_pets(size="medium")

    assert [pet.name for pet in results] == ["Scout"]


def test_search_pets_filters_by_size_large() -> None:
    results = search_pets(size="large")

    assert len(results) == 0


def test_search_pets_without_size_filter_returns_all_available() -> None:
    results = search_pets()

    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


def test_search_pets_combines_size_and_species_filters() -> None:
    results = search_pets(size="small", species="cat")

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_size_filter_excludes_non_matching() -> None:
    results = search_pets(size="small")

    pet_names = [pet.name for pet in results]
    assert "Scout" not in pet_names
    assert "Mochi" in pet_names
    assert "Pip" in pet_names


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)
