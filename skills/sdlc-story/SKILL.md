---
name: sdlc-story
description: GitHub issue to PR implementation guidance for the SDLC Automation Demo Petstore app.
triggers:
  - openhands-build
  - story to pr
  - sparse issue
---

# SDLC Story To PR

Use this skill when OpenHands turns a GitHub issue into a small reviewable PR.

## Inputs

- GitHub issue title, body, labels, and comments
- repository default branch
- target source branch
- acceptance criteria when present
- linked PRs or previous automation comments when present

Sparse issues are acceptable when the title maps to an existing Petstore behavior. Infer the smallest safe implementation and document assumptions before editing.

## Workflow

1. Read `README.md`, `AGENTS.md`, and the issue context.
2. Run `python3 skills/sdlc-story/scripts/extract_acceptance_criteria.py` on the issue body when useful.
3. Write assumptions, non-goals, acceptance criteria, and validation plan before editing.
4. Search existing app code and tests.
5. Implement a narrow change.
6. Add or update focused tests.
7. Run the narrowest useful validation first.
8. Open a draft PR with evidence and human-review notes.

## Petstore Map

- Catalog behavior: `app/petstore_app/catalog.py`
- Adoption behavior: `app/petstore_app/adoptions.py`
- Static UI: `app/web/`
- Tests: `app/tests/`

## Sparse Story Examples

`Filter pets by max adoption fee` means:

- add an optional max-fee filter to catalog search
- expose a simple static UI input if the PR includes UI
- add focused backend tests
- do not add payment processing, persistence, billing, or dependencies

## Stop Conditions

Ask for human input if the issue requires a product decision, schema migration, auth change, new dependency, environment change, secret access, or production mutation.
