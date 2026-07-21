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


def test_search_pets_filters_by_basic_training_level() -> None:
    results = search_pets(training_level="basic")

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_filters_by_intermediate_training_level() -> None:
    results = search_pets(training_level="intermediate")

    assert [pet.name for pet in results] == ["Scout"]


def test_search_pets_filters_by_advanced_training_level() -> None:
    results = search_pets(training_level="advanced", status="pending")

    assert [pet.name for pet in results] == ["Nova"]


def test_search_pets_default_behavior_without_training_level() -> None:
    results = search_pets()

    assert [pet.name for pet in results] == ["Mochi", "Scout", "Pip"]


def test_search_pets_training_level_respects_status_filter() -> None:
    results = search_pets(training_level="advanced")

    assert results == []


def test_search_pets_combines_training_level_with_species() -> None:
    results = search_pets(species="dog", training_level="intermediate")

    assert [pet.name for pet in results] == ["Scout"]


def test_search_pets_training_level_case_insensitive() -> None:
    results = search_pets(training_level="BASIC")

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_training_level_with_whitespace() -> None:
    results = search_pets(training_level="  basic  ")

    assert [pet.name for pet in results] == ["Mochi", "Pip"]

