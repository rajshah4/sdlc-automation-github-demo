"""Adoption order behavior used by validation scenarios."""

from __future__ import annotations

from dataclasses import dataclass

from .catalog import PETS, Pet


@dataclass(frozen=True)
class AdoptionOrder:
    pet_id: str
    adopter_email: str
    adoption_fee_cents: int
    donation_cents: int
    total_cents: int


def _find_pet(pet_id: str) -> Pet:
    normalized_pet_id = pet_id.strip()
    for pet in PETS:
        if pet.id == normalized_pet_id:
            return pet
    raise ValueError("pet_id was not found")


def create_adoption_order(
    pet_id: str,
    adopter_email: str,
    *,
    donation_cents: int = 0,
) -> AdoptionOrder:
    """Create a reviewable adoption order summary."""
    pet = _find_pet(pet_id)
    if pet.status != "available":
        raise ValueError("pet is not available for adoption")
    if "@" not in adopter_email:
        raise ValueError("adopter_email must be a valid email address")
    if donation_cents < 0:
        raise ValueError("donation_cents cannot be negative")

    return AdoptionOrder(
        pet_id=pet.id,
        adopter_email=adopter_email,
        adoption_fee_cents=pet.adoption_fee_cents,
        donation_cents=donation_cents,
        total_cents=pet.adoption_fee_cents + donation_cents,
    )
