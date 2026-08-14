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


def test_default_search_excludes_pending_pets() -> None:
    """Regression test for KAN-62: pending pets must not appear in default search."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    pet_names = [pet.name for pet in results]
    
    # Nova (pet-103) has status="pending" and must not appear in default results
    assert "pet-103" not in pet_ids, "pet-103 (Nova, pending) should not appear in default search"
    assert "Nova" not in pet_names, "Nova (pending pet) should not appear in default search"
    
    # Only available pets should be returned
    for pet in results:
        assert pet.status == "available", f"{pet.name} has status={pet.status}, expected available"


def test_default_dog_search_excludes_pending_dogs() -> None:
    """Regression test for KAN-62: pending dogs must not appear in species=dog search."""
    results = search_pets(species="dog")

    pet_ids = [pet.id for pet in results]
    
    # Scout (pet-101) is an available dog - should appear
    assert "pet-101" in pet_ids, "Scout (available dog) should appear"
    
    # Nova (pet-103) is a pending dog - must not appear
    assert "pet-103" not in pet_ids, "Nova (pending dog) should not appear in dog search"
    assert len(results) == 1, "Only one available dog (Scout) should be returned"
