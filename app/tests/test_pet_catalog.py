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
    """Regression test: default available search must exclude pending pets like Nova."""
    results = search_pets()  # Default status="available"

    pet_ids = [pet.id for pet in results]
    pet_names = [pet.name for pet in results]

    # Nova (pet-103) has status="pending" and must not appear in default results
    assert "pet-103" not in pet_ids
    assert "Nova" not in pet_names

    # Available pets should be present
    assert "pet-100" in pet_ids  # Mochi
    assert "pet-101" in pet_ids  # Scout
    assert "pet-102" in pet_ids  # Pip
