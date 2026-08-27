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


def test_search_pets_defaults_to_available_status() -> None:
    """Verify default search excludes pending pets (KAN-161 regression test)."""
    results = search_pets()
    
    result_ids = [pet.id for pet in results]
    assert "pet-103" not in result_ids, "Pending pet Nova (pet-103) should not appear in default search"
    assert "pet-100" in result_ids, "Available pet Mochi should appear"
    assert "pet-101" in result_ids, "Available pet Scout should appear"
    assert "pet-102" in result_ids, "Available pet Pip should appear"


def test_search_pets_excludes_pending_when_searching_by_name() -> None:
    """Verify searching for Nova by name doesn't return her when using default status."""
    results = search_pets(query="nova")
    
    assert len(results) == 0, "Pending pet Nova should not appear in default available-only search"


def test_search_pets_can_search_all_dogs_available_only() -> None:
    """Verify dog search excludes pending dog Nova by default."""
    results = search_pets(species="dog")
    
    result_names = [pet.name for pet in results]
    assert result_names == ["Scout"], "Only available dog Scout should be returned, not pending Nova"


def test_search_pets_explicit_available_status() -> None:
    """Verify explicitly passing status='available' works correctly."""
    results = search_pets(species="dog", status="available")
    
    assert [pet.name for pet in results] == ["Scout"]
    assert len(results) == 1
