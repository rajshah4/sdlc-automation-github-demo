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


def test_search_pets_max_fee_returns_pets_within_budget() -> None:
    # Mochi=7500, Pip=4500 are <= 8000; Scout=12500 is excluded
    results = search_pets(max_fee_cents=8000)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_max_fee_exact_match_is_inclusive() -> None:
    # Pip's fee is exactly 4500
    results = search_pets(max_fee_cents=4500)

    assert any(pet.name == "Pip" for pet in results)


def test_search_pets_max_fee_below_all_returns_empty() -> None:
    results = search_pets(max_fee_cents=100)

    assert results == []


def test_search_pets_max_fee_negative_raises_value_error() -> None:
    with pytest.raises(ValueError, match="max_fee_cents"):
        search_pets(max_fee_cents=-1)
