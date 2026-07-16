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


def test_search_pets_indoor_filter_excludes_non_indoor_pets() -> None:
    results = search_pets(tag="indoor")

    assert len(results) == 2
    assert all("indoor" in pet.tags for pet in results)
    assert "Scout" not in [pet.name for pet in results]


def test_search_pets_indoor_filter_with_species() -> None:
    results = search_pets(species="cat", tag="indoor")

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_indoor_filter_with_name_query() -> None:
    results = search_pets("Pip", tag="indoor")

    assert [pet.name for pet in results] == ["Pip"]


def test_search_pets_indoor_filter_excludes_pending_pets() -> None:
    results = search_pets(tag="indoor", status="available")

    assert "Nova" not in [pet.name for pet in results]
    assert all(pet.status == "available" for pet in results)


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)
