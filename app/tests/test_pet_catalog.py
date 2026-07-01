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


def test_default_search_excludes_pending_nova() -> None:
    """Regression test for KAN-67: pending pet Nova must not appear in default search."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    pet_names = [pet.name for pet in results]

    assert "pet-103" not in pet_ids, "Nova (pet-103) should not appear in default available search"
    assert "Nova" not in pet_names, "Nova should not appear in default available search"
    assert "pet-100" in pet_ids, "Mochi should appear in default search"
    assert "pet-101" in pet_ids, "Scout should appear in default search"
    assert "pet-102" in pet_ids, "Pip should appear in default search"


def test_species_search_excludes_pending() -> None:
    """Regression test for KAN-67: species filter must exclude pending pets."""
    results = search_pets(species="dog")

    assert len(results) == 1, "Only one available dog should be returned"
    assert results[0].id == "pet-101", "Scout is the only available dog"
    assert results[0].name == "Scout"
    assert results[0].status == "available"

    for pet in results:
        assert pet.id != "pet-103", "Nova (pending dog) must not appear in species search"
        assert pet.name != "Nova", "Nova (pending dog) must not appear in species search"
