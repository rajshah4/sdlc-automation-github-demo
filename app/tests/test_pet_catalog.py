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
    results = search_pets(max_adoption_fee_cents=10000)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_includes_pets_at_exact_max_fee() -> None:
    results = search_pets(max_adoption_fee_cents=7500)

    pet_names = [pet.name for pet in results]
    assert "Mochi" in pet_names
    assert "Pip" in pet_names


def test_search_pets_excludes_pets_above_max_fee() -> None:
    results = search_pets(max_adoption_fee_cents=5000)

    pet_names = [pet.name for pet in results]
    assert "Mochi" not in pet_names
    assert "Scout" not in pet_names
    assert "Pip" in pet_names


def test_search_pets_returns_all_when_max_fee_not_provided() -> None:
    results = search_pets()

    assert len(results) == 3


def test_search_pets_rejects_negative_max_fee() -> None:
    with pytest.raises(ValueError, match="max_adoption_fee_cents"):
        search_pets(max_adoption_fee_cents=-100)
