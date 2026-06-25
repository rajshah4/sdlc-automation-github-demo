# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Search pets by maximum adoption fee

Adopters can filter the catalog by specifying a maximum adoption fee in cents.

#### Scenario: Return pets within budget

- Given a catalog containing pets with varying adoption fees
- When an adopter searches with a maximum fee of 10000 cents ($100)
- Then only pets with adoption fees at or below 10000 cents are returned

#### Scenario: Exclude pets above budget

- Given a catalog containing pets with varying adoption fees
- When an adopter searches with a maximum fee of 5000 cents ($50)
- Then pets with adoption fees above 5000 cents are excluded from results

#### Scenario: Reject negative maximum fee

- Given an adopter attempts to search with a negative maximum fee
- When the search is executed
- Then a ValueError is raised indicating invalid fee constraint

#### Scenario: No maximum fee specified

- Given an adopter searches without specifying a maximum fee
- When the search is executed
- Then all pets matching other criteria are returned regardless of adoption fee
