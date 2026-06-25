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


def test_search_pets_filters_by_max_adoption_fee() -> None:
    results = search_pets(max_adoption_fee_cents=7500)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]
    assert all(pet.adoption_fee_cents <= 7500 for pet in results)


def test_search_pets_excludes_pets_above_budget() -> None:
    results = search_pets(max_adoption_fee_cents=7500)

    excluded_names = [pet.name for pet in results]
    assert "Scout" not in excluded_names


def test_search_pets_includes_pet_at_exact_budget_limit() -> None:
    results = search_pets(max_adoption_fee_cents=7500)

    assert any(pet.name == "Mochi" and pet.adoption_fee_cents == 7500 for pet in results)


def test_search_pets_returns_empty_when_budget_too_low() -> None:
    results = search_pets(max_adoption_fee_cents=1000)

    assert results == []


def test_search_pets_validates_negative_max_adoption_fee() -> None:
    with pytest.raises(ValueError, match="max_adoption_fee_cents cannot be negative"):
        search_pets(max_adoption_fee_cents=-100)


def test_search_pets_preserves_status_filtering_with_budget() -> None:
    results_default = search_pets(max_adoption_fee_cents=15000)

    assert all(pet.status == "available" for pet in results_default)
    assert "Nova" not in [pet.name for pet in results_default]


def test_search_pets_budget_filter_with_explicit_pending_status() -> None:
    results = search_pets(max_adoption_fee_cents=15000, status="pending")

    assert [pet.name for pet in results] == ["Nova"]
