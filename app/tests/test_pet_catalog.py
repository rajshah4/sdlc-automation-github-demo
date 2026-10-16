import pytest

from petstore_app.catalog import search_pets


def test_search_pets_filters_by_species_and_status() -> None:
    results = search_pets(species="dog")

    assert [pet.id for pet in results] == ["pet-101"]


def test_default_search_excludes_pending_pets() -> None:
    """Regression test: pending pets must not appear in default available-only search.
    
    Addresses KAN-241: Customers seeing pets that are not available.
    Evidence: PENDING_PET_VISIBLE error log showed pet-103 (Nova, pending) was visible.
    """
    results = search_pets()
    result_ids = [pet.id for pet in results]
    
    # Explicitly verify Nova (pet-103, pending) is excluded
    assert "pet-103" not in result_ids, "Pending pet Nova (pet-103) must not appear in default search"
    
    # Verify only available pets are returned
    assert set(result_ids) == {"pet-100", "pet-101", "pet-102"}, \
        "Default search must return only available pets"


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
