# Petstore Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog must exclude pending pets

The customer-facing available-pets catalog must show only pets with `status="available"` and must never show pending pets, regardless of internal system state or runtime configuration.

#### Scenario: Customer views available pets on the website

- **Given** the petstore has multiple pets including Nova (pet-103) with `status="pending"`
- **When** a customer requests the available-pets catalog via the home page or `/api/pets` endpoint
- **Then** the response must include only pets with `status="available"`
- **And** Nova (pet-103) must not appear in the results

#### Scenario: Customer searches for dogs (species filter with default status)

- **Given** the petstore has Scout (pet-101, dog, available) and Nova (pet-103, dog, pending)
- **When** a customer searches for dogs without specifying status
- **Then** the response must include Scout but not Nova
- **And** only available dogs must be returned

#### Scenario: Support explicitly requests pending pets

- **Given** the petstore has pending pets like Nova (pet-103)
- **When** support or operations explicitly request `status="pending"` in the search
- **Then** the response may include pending pets
- **And** this is the only scenario where pending pets are visible

## UNCHANGED Requirements

### Requirement: Explicit pending pet search for support workflows

Support and operations workflows may explicitly request `status="pending"` to investigate cases. This capability must remain unchanged.

## Acceptance Criteria

- [ ] The `/api/pets` endpoint returns only available pets
- [ ] The home page (`/`) shows only available pets
- [ ] Nova (pet-103) does not appear in default catalog results
- [ ] Explicit `status="pending"` searches still work for support workflows
- [ ] Focused regression test proves pending pets stay out of default results
