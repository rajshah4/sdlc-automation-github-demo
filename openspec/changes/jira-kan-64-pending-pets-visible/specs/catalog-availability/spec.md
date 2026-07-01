# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet catalog search returns only available pets

The default customer-facing catalog search MUST return only pets with `status="available"`. Pending pets MUST NOT appear unless explicitly requested with `status="pending"`.

#### Scenario: Default catalog view excludes pending pets

- Given Nova (pet-103) has `status="pending"`
- When a customer views the default available pets catalog
- Then Nova MUST NOT appear in the results
- And only pets with `status="available"` are shown (Mochi, Scout, Pip)

#### Scenario: Species filter on available pets excludes pending pets

- Given Nova is a dog with `status="pending"`
- And Scout is a dog with `status="available"`
- When a customer filters by species="dog"
- Then only Scout appears in the results
- And Nova does not appear

#### Scenario: Name search for pending pet shows empty state

- Given Nova has `status="pending"`
- When a customer searches for "nova" by name
- Then the empty state message "No available pets match this search." is displayed
- And Nova is not shown in the results

## MODIFIED Requirements

### Requirement: Support workflows can explicitly query pending pets

Support and operations workflows may explicitly request `status="pending"` when investigating a case.

#### Scenario: Explicit pending search returns only pending pets

- Given Nova has `status="pending"`
- When a support agent explicitly searches with `status="pending"`
- Then Nova appears in the results
- And available pets are excluded
