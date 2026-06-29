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


def test_search_pets_excludes_pending_with_empty_status() -> None:
    """Regression test for KAN-28: empty status should default to available."""
    results_empty = search_pets(status="")
    results_whitespace = search_pets(status="   ")

    assert all(pet.status == "available" for pet in results_empty)
    assert all(pet.status == "available" for pet in results_whitespace)
    assert "Nova" not in [pet.name for pet in results_empty]
    assert "Nova" not in [pet.name for pet in results_whitespace]
