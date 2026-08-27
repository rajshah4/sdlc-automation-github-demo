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


def test_search_pets_empty_status_should_not_bypass_filter() -> None:
    results = search_pets(status="")

    assert len(results) == 0, "Empty status should not match any pets"


def test_search_pets_default_excludes_pending_pets() -> None:
    results = search_pets()

    pet_names = [pet.name for pet in results]
    assert "Nova" not in pet_names, "Default search should exclude pending pets"
    assert "Mochi" in pet_names, "Default search should include available pets"
