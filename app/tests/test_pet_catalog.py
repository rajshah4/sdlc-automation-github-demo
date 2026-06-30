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


def test_search_pets_empty_status_excludes_pending() -> None:
    """Regression test for KAN-29: empty status string must not bypass availability filter."""
    results = search_pets(status="")

    assert all(pet.status == "available" for pet in results)
    assert "Nova" not in [pet.name for pet in results]


def test_search_pets_default_status_excludes_pending_from_species_search() -> None:
    """Regression test for KAN-29: species filter with default status must exclude pending pets."""
    results = search_pets(species="dog")

    assert len(results) == 1
    assert results[0].name == "Scout"
    assert results[0].status == "available"
