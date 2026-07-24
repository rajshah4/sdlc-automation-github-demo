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
    """Regression test for KAN-127: default search must exclude pending pets."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103) with status=pending should not appear in default search"
    assert "pet-100" in pet_ids
    assert "pet-101" in pet_ids
    assert "pet-102" in pet_ids


def test_search_pets_empty_status_defaults_to_available() -> None:
    """Regression test for KAN-127: empty status string must default to available."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103) should not appear when status is empty string"
    assert len(pet_ids) == 3


def test_search_pets_none_status_defaults_to_available() -> None:
    """Regression test for KAN-127: None status must default to available."""
    results = search_pets(status=None)

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103) should not appear when status is None"
    assert len(pet_ids) == 3


def test_search_pets_species_filter_excludes_pending() -> None:
    """Regression test for KAN-127: species search must also respect default available status."""
    results = search_pets(species="dog")

    pet_names = [pet.name for pet in results]
    assert "Nova" not in pet_names, "Nova (pending dog) should not appear in default dog search"
    assert "Scout" in pet_names
