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
    # Mochi=$75 (7500¢) and Pip=$45 (4500¢) are under $120; Scout=$125 (12500¢) is excluded.
    results = search_pets(max_fee_cents=12000)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_includes_pets_at_exact_fee_boundary() -> None:
    results = search_pets(max_fee_cents=7500)

    assert any(pet.name == "Mochi" for pet in results)


def test_search_pets_rejects_negative_max_fee() -> None:
    with pytest.raises(ValueError, match="max_fee_cents"):
        search_pets(max_fee_cents=-1)


def test_search_pets_no_fee_filter_when_max_fee_none() -> None:
    all_available = search_pets()
    with_none = search_pets(max_fee_cents=None)

    assert [pet.id for pet in all_available] == [pet.id for pet in with_none]
