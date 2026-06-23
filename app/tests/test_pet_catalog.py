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


def test_search_pets_filters_by_weekend_available() -> None:
    results = search_pets(weekend_available=True)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_excludes_weekend_unavailable() -> None:
    results = search_pets(weekend_available=False)

    assert [pet.name for pet in results] == ["Scout"]


def test_search_pets_default_includes_all_weekend_availability() -> None:
    results = search_pets()

    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


def test_search_pets_combines_weekend_filter_with_species() -> None:
    results = search_pets(species="dog", weekend_available=True)

    assert [pet.name for pet in results] == []


def test_search_pets_combines_weekend_filter_with_tag() -> None:
    results = search_pets(tag="indoor", weekend_available=True)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]
