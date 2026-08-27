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


def test_pet_has_fee_breakdown_fields() -> None:
    results = search_pets(query="Mochi")

    assert len(results) == 1
    pet = results[0]
    assert pet.base_fee_cents == 5000
    assert pet.vaccination_fee_cents == 1500
    assert pet.microchip_fee_cents == 1000
    assert pet.adoption_fee_cents == 7500


def test_pet_fee_breakdown_sums_to_total() -> None:
    results = search_pets()

    for pet in results:
        expected_total = pet.base_fee_cents + pet.vaccination_fee_cents + pet.microchip_fee_cents
        assert pet.adoption_fee_cents == expected_total, f"Pet {pet.name} fee breakdown doesn't sum to total"

