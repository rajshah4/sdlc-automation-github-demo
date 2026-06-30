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
    """Regression: default search must filter to available pets only."""
    results = search_pets()

    assert all(pet.status == "available" for pet in results)
    assert "pet-103" not in [pet.id for pet in results]  # Nova is pending


def test_empty_status_excludes_pending_pets() -> None:
    """Regression: empty status string must default to available filter."""
    results = search_pets(status="")

    assert all(pet.status == "available" for pet in results)
    assert "Nova" not in [pet.name for pet in results]


def test_nova_not_in_default_available_search() -> None:
    """Regression: Nova (pet-103) has status=pending and must not appear in default search."""
    results = search_pets()

    pet_names = [pet.name for pet in results]
    pet_ids = [pet.id for pet in results]

    assert "Nova" not in pet_names
    assert "pet-103" not in pet_ids
