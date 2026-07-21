# Spec: Catalog name sorting

## ADDED Requirements

### Requirement: Catalog supports optional name sorting

Catalog search MUST support an optional `sort_by` parameter that orders results alphabetically by name.

#### Scenario: Default catalog order is preserved when sort is not specified

- Given the catalog contains pets in default order: Mochi, Scout, Pip
- When catalog search is called without `sort_by`
- Then results appear in the default order

#### Scenario: Name sort orders results alphabetically

- Given the catalog contains pets: Mochi, Scout, Pip
- When catalog search is called with `sort_by="name"`
- Then results appear in alphabetical order: Mochi, Pip, Scout

#### Scenario: Name sorting is case-insensitive

- Given the catalog contains pets with mixed-case names
- When catalog search is called with `sort_by="name"`
- Then sorting treats uppercase and lowercase names equivalently

#### Scenario: Sort applies to filtered results

- Given the catalog contains: Mochi (cat), Scout (dog), Pip (rabbit)
- When catalog search is called with `species="dog"` and `sort_by="name"`
- Then only matching dogs appear, sorted by name
