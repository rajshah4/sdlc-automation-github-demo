# Petstore API Spec Delta

## MODIFIED Requirements

### Requirement: /api/pets endpoint uses catalog search logic

The `/api/pets` API endpoint MUST use the `search_pets()` function from `catalog.py` to ensure consistent filtering logic across the application.

#### Scenario: /api/pets excludes pending pets by default

- Given Nova has status `pending`
- And Scout has status `available`
- When a GET request is made to `/api/pets`
- Then the response includes Scout
- And the response does not include Nova

#### Scenario: catalog search logic is consistent

- Given the `search_pets()` function has default status="available"
- When `/api/pets` endpoint is called
- Then it uses `search_pets()` for filtering
- And the filtering behavior matches catalog search expectations

## UNCHANGED Requirements

### Requirement: HTML home page can show incident simulation

The home page rendering (`/` path) continues to use `visible_pets()` to support demo incident mode simulation (INCIDENT_MODE).

#### Scenario: incident mode simulation preserved

- Given the system is in INCIDENT_MODE (for demo purposes)
- When the home page is rendered
- Then `visible_pets()` is used to show the incident banner
- And the incident detection logic remains functional

### Requirement: Explicit pending searches still work

Support and operations workflows can still explicitly search for pending pets.

#### Scenario: search_pets with status="pending" works

- Given Nova has status `pending`
- When catalog search is called with `status="pending"`
- Then Nova is included in the results
