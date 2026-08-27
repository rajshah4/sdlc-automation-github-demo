# Pet Detail Display Spec Delta

## ADDED Requirements

### Requirement: Pet detail page displays adoption fee breakdown

The pet detail page must show a breakdown of adoption fees to provide transparency to adopters about the cost components.

#### Scenario: Adopter views pet with fee breakdown

- Given a pet is available for adoption with base fee $50, vaccination fee $15, and microchip fee $10
- When the adopter views the pet detail page
- Then the page displays "Base Fee: $50.00"
- And the page displays "Vaccination Fee: $15.00"
- And the page displays "Microchip Fee: $10.00"
- And the page displays "Total Adoption Fee: $75.00"

#### Scenario: Fee breakdown components sum to total

- Given a pet has base_fee_cents = 5000, vaccination_fee_cents = 1500, microchip_fee_cents = 1000
- When the system computes the total
- Then adoption_fee_cents equals 7500 (the sum of all components)

#### Scenario: All pets display fee breakdowns

- Given multiple pets are available with different fee structures
- When an adopter browses the pet catalog
- Then each pet detail shows its specific fee breakdown
- And the breakdown values differ based on each pet's needs

### Requirement: Backend provides fee breakdown data

The Pet dataclass must include fields for each fee component to support transparent fee display.

#### Scenario: Pet data includes breakdown fields

- Given the Pet dataclass is used to represent pet information
- When a Pet instance is created
- Then it includes base_fee_cents as an integer
- And it includes vaccination_fee_cents as an integer
- And it includes microchip_fee_cents as an integer
- And it includes adoption_fee_cents as the total (existing field)
