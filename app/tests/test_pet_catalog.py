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


def test_search_pets_default_excludes_pending_pets() -> None:
    """
    Regression test for KAN-173 / PENDING_PET_VISIBLE.
    
    Default search with no parameters must exclude pending pets.
    Nova (pet-103) has status="pending" and must not appear in default results.
    """
    results = search_pets()
    
    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103) must not appear in default available search"
    assert len(results) == 3, "Default search should return exactly 3 available pets"
    assert pet_ids == ["pet-100", "pet-101", "pet-102"]


def test_search_pets_by_name_excludes_pending_pets() -> None:
    """
    Regression test for KAN-173 / PENDING_PET_VISIBLE.
    
    Searching for a pending pet by name with default status filter must return no results.
    Customers must not be able to discover pending pets through name search.
    """
    results = search_pets(query="nova")
    
    assert len(results) == 0, "Searching for 'nova' with default status must return empty results"
    
    results_upper = search_pets(query="Nova")
    assert len(results_upper) == 0, "Search must be case-insensitive and still exclude pending pets"
