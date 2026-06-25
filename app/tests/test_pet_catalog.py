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


def test_search_pets_filters_by_max_adoption_fee() -> None:
    results = search_pets(max_adoption_fee_cents=7500)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_combines_fee_cap_with_existing_filters() -> None:
    results = search_pets(tag="family", max_adoption_fee_cents=10000)

    assert results == []


def test_search_pets_rejects_negative_max_adoption_fee() -> None:
    with pytest.raises(ValueError, match="max_adoption_fee_cents"):
        search_pets(max_adoption_fee_cents=-1)


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)
