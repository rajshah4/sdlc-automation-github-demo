# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search returns only available pets

The customer-facing catalog must exclude pending pets from the default available-pets experience.

#### Scenario: Customer views available pets page

- Given the petstore has pets with various status values (available, pending)
- When a customer requests the default available pets list
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded

#### Scenario: Pending pet (Nova) does not appear in default catalog

- Given Nova (pet-103) has `status="pending"`
- When a customer requests the available pets list
- Then Nova is not included in the results
- And available pets (Mochi, Scout, Pip) are included

#### Scenario: Explicit pending search still works for ops

- Given an operations user needs to investigate a pending pet
- When they explicitly request `status="pending"` in the search
- Then pending pets are returned
- And this supports operations workflows without affecting customer experience

## UNCHANGED Requirements

### Requirement: Search filters by species, tags, and status

The existing catalog search filtering by species, tags, and status parameters remains unchanged.

### Requirement: Explicit status searches work correctly

When a caller explicitly provides a status parameter (available, pending, adopted), the search respects that filter.
