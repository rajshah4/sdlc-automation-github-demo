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


# --- max_fee_cents filter (issue #101) ---

def test_search_pets_max_fee_returns_affordable_pets() -> None:
    # Pip ($45 = 4500 cents) fits; Mochi ($75) and Scout ($125) do not.
    results = search_pets(max_fee_cents=5000)
    assert [pet.id for pet in results] == ["pet-102"]


def test_search_pets_max_fee_includes_exact_boundary() -> None:
    # max_fee_cents=7500 includes Mochi ($75) and Pip ($45).
    results = search_pets(max_fee_cents=7500)
    assert {pet.id for pet in results} == {"pet-100", "pet-102"}


def test_search_pets_max_fee_excludes_all_when_below_minimum() -> None:
    results = search_pets(max_fee_cents=4000)
    assert results == []


def test_search_pets_max_fee_none_returns_all_available() -> None:
    results = search_pets(max_fee_cents=None)
    assert {pet.id for pet in results} == {"pet-100", "pet-101", "pet-102"}


def test_search_pets_max_fee_pending_pets_remain_hidden() -> None:
    # Nova is pending; even a generous cap must not surface it in default search.
    results = search_pets(max_fee_cents=20000)
    assert all(pet.status == "available" for pet in results)
    assert "pet-103" not in [pet.id for pet in results]


def test_search_pets_max_fee_negative_raises() -> None:
    with pytest.raises(ValueError, match="max_fee_cents"):
        search_pets(max_fee_cents=-1)
