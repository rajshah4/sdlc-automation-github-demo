import pytest

from petstore_app.catalog import PETS, search_pets


def test_default_search_excludes_pending_pets() -> None:
    """Regression test for KAN-60: Default search must exclude pending pets."""
    results = search_pets()

    result_ids = [pet.id for pet in results]
    assert "pet-103" not in result_ids, "Nova (pet-103, pending) should not appear in default search"
    assert all(pet.status == "available" for pet in results), "All results must have status='available'"


def test_nova_excluded_from_default_search() -> None:
    """Regression test for KAN-60: Nova (pet-103) must not appear in default available pet list."""
    results = search_pets()

    nova_in_results = any(pet.name == "Nova" for pet in results)
    assert not nova_in_results, "Nova should not appear in default search (she has status='pending')"


def test_all_available_pets_included_by_default() -> None:
    """Regression test for KAN-60: Verify all available pets appear in default search."""
    results = search_pets()

    result_ids = {pet.id for pet in results}
    expected_available = {pet.id for pet in PETS if pet.status == "available"}
    assert result_ids == expected_available, "Default search should return all available pets"


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
