# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search must exclude pending pets

Product rule: Default customer-facing catalog search must show only pets with `status="available"`.

#### Scenario: Default search without filters

- Given a catalog with available pets (Mochi, Scout, Pip) and a pending pet (Nova/pet-103)
- When a customer performs a default search with no status filter
- Then only available pets are returned
- And Nova (pet-103) does not appear in results
- And all returned pets have status="available"

#### Scenario: Species filter with default status

- Given a catalog with available dogs (Scout/pet-101) and pending dogs (Nova/pet-103)
- When a customer searches for species="dog" with default status
- Then only Scout (pet-101) is returned
- And Nova (pet-103) does not appear in results

#### Scenario: Explicit pending pet search for support workflows

- Given a catalog with pending pets (Nova/pet-103)
- When support explicitly searches with status="pending"
- Then pending pets are returned
- And Nova appears in results
- This confirms that pending pets are accessible when explicitly requested

## UNCHANGED Requirements

- Explicit `status="pending"` searches must continue to work for support and operations workflows
- Pet search filtering by name, species, tag, and max_results remains unchanged
- Frontend Playwright tests already verify UI-visible behavior
