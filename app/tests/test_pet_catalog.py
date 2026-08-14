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


def test_search_pets_enforces_available_filter_when_status_empty() -> None:
    """Regression test for KAN-68: empty status should default to 'available'."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Pending pet should not appear when status is empty string"
    assert "pet-101" in pet_ids, "Available pets should still appear"


def test_search_pets_enforces_available_filter_by_default() -> None:
    """Pending pets should not appear in default search."""
    results = search_pets(species="dog")

    pet_ids = [pet.id for pet in results]
    assert pet_ids == ["pet-101"], "Only available dog should appear by default"
    assert "pet-103" not in pet_ids, "Pending dog should not appear"
