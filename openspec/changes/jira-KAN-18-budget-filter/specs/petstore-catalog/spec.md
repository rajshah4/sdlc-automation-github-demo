# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: UI exposes budget-based pet filtering

Families using the static petstore UI can filter available pets by maximum adoption fee.

#### Scenario: Family searches with budget constraint

- Given the petstore catalog UI is loaded
- When a family enters "100" in the "Max Budget" field and searches
- Then only pets with adoption fees ≤ $100 are displayed

#### Scenario: Budget filter combines with species filter

- Given the petstore catalog UI is loaded
- When a family selects species "dog" and enters "100" in the "Max Budget" field
- Then only available dogs with adoption fees ≤ $100 are displayed

#### Scenario: Empty budget field shows all pets

- Given the petstore catalog UI is loaded
- When the "Max Budget" field is empty or zero
- Then all available pets are displayed regardless of adoption fee

#### Scenario: Budget filter displays fees for comparison

- Given the petstore catalog UI shows search results
- When pets are displayed
- Then each pet card shows its adoption fee for family comparison

## EXISTING Requirements (Backend)

These requirements are already implemented and tested in `app/petstore_app/catalog.py`:

### Requirement: Catalog search supports optional maximum adoption fee

The backend `search_pets` function accepts `max_adoption_fee_cents` parameter.

#### Scenario: Search excludes pets above fee cap (EXISTING)

- Given pets with fees: Mochi ($75), Scout ($125), Pip ($45)
- When searching with `max_adoption_fee_cents=7500`
- Then results include Mochi and Pip, exclude Scout

#### Scenario: Negative fee cap is rejected (EXISTING)

- Given a catalog search request
- When `max_adoption_fee_cents=-1`
- Then ValueError is raised with message containing "max_adoption_fee_cents"

## Validation

- Backend: `pytest app/tests/test_pet_catalog.py::test_search_pets_filters_by_max_adoption_fee`
- UI: Manual verification that budget input filters displayed pets correctly
- Integration: Confirm dollar amounts in UI convert to cents matching backend expectations
