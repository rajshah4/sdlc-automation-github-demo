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


def test_search_pets_excludes_pending_by_default() -> None:
    """Regression test for KAN-55: default search must exclude pending pets."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103) should not appear in default search"
    assert set(pet_ids) == {"pet-100", "pet-101", "pet-102"}


def test_search_pets_with_empty_status_excludes_pending() -> None:
    """Edge case: empty status string should still exclude pending pets."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert len(pet_ids) == 0, "Empty status should match no pets"


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)
