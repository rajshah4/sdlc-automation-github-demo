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
    """Regression test for KAN-64: pending pets must not appear in default available catalog."""
    results = search_pets()
    
    pet_ids = [pet.id for pet in results]
    pet_names = [pet.name for pet in results]
    
    assert "pet-103" not in pet_ids, "Nova (pet-103) should not appear in default search"
    assert "Nova" not in pet_names, "Pending pet Nova should not appear in available catalog"
    assert all(pet.status == "available" for pet in results), "All default results must have status='available'"
