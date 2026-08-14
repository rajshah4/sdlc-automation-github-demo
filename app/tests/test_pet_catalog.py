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


def test_search_pets_excludes_pending_pets_by_default() -> None:
    """Regression test for KAN-66: pending pets must not appear in default search."""
    results = search_pets()
    pet_ids = [pet.id for pet in results]
    
    assert "pet-103" not in pet_ids, "Nova (pet-103) is pending and should not appear in default search"
    assert "pet-100" in pet_ids
    assert "pet-101" in pet_ids
    assert "pet-102" in pet_ids


def test_search_pets_excludes_pending_pets_when_status_is_empty_string() -> None:
    """Regression test for KAN-66: empty status string should default to 'available'."""
    results = search_pets(status="")
    pet_ids = [pet.id for pet in results]
    
    assert "pet-103" not in pet_ids, "Nova (pet-103) should not appear when status is empty string"
    assert len(pet_ids) == 3
