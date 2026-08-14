"""Pet catalog behavior used by review and QA scenarios."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Pet:
    id: str
    name: str
    species: str
    status: str
    tags: tuple[str, ...]
    age_months: int
    adoption_fee_cents: int


PETS: tuple[Pet, ...] = (
    Pet("pet-100", "Mochi", "cat", "available", ("calm", "indoor"), 18, 7500),
    Pet("pet-101", "Scout", "dog", "available", ("active", "family"), 28, 12500),
    Pet("pet-102", "Pip", "rabbit", "available", ("quiet", "indoor"), 9, 4500),
    Pet("pet-103", "Nova", "dog", "pending", ("active", "training"), 14, 11000),
)


def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",
    tag: str | None = None,
    min_age_months: int | None = None,
    max_age_months: int | None = None,
    max_results: int = 10,
) -> list[Pet]:
    """Search pets by name, species, status, tag, and age range."""
    if min_age_months is not None and min_age_months < 0:
        raise ValueError("min_age_months must be non-negative")
    if max_age_months is not None and max_age_months < 0:
        raise ValueError("max_age_months must be non-negative")
    if (
        min_age_months is not None
        and max_age_months is not None
        and min_age_months > max_age_months
    ):
        raise ValueError("min_age_months must not exceed max_age_months")
    if max_results < 1 or max_results > 50:
        raise ValueError("max_results must be between 1 and 50")

    normalized_query = query.strip().lower()
    normalized_species = species.strip().lower() if species else None
    normalized_status = status.strip().lower()
    normalized_tag = tag.strip().lower() if tag else None

    matches: list[Pet] = []
    for pet in PETS:
        if normalized_query and normalized_query not in pet.name.lower():
            continue
        if normalized_species and normalized_species != pet.species:
            continue
        if normalized_status and normalized_status != pet.status:
            continue
        if normalized_tag and normalized_tag not in pet.tags:
            continue
        if min_age_months is not None and pet.age_months < min_age_months:
            continue
        if max_age_months is not None and pet.age_months > max_age_months:
            continue
        matches.append(pet)

    return matches[:max_results]
