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


def test_search_pets_filters_by_max_fee() -> None:
    results = search_pets(max_fee_cents=10000)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_excludes_pets_above_max_fee() -> None:
    results = search_pets(max_fee_cents=5000)

    assert [pet.name for pet in results] == ["Pip"]


def test_search_pets_without_max_fee_returns_all_available() -> None:
    results = search_pets()

    assert len(results) == 3
    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


def test_search_pets_rejects_negative_max_fee() -> None:
    with pytest.raises(ValueError, match="max_fee_cents must be non-negative"):
        search_pets(max_fee_cents=-100)


def test_search_pets_max_fee_zero_excludes_all_pets_with_fees() -> None:
    results = search_pets(max_fee_cents=0)

    assert len(results) == 0
