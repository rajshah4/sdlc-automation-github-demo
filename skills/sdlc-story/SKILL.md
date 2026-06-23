---
name: sdlc-story
description: Turn sparse GitHub issues or issue comments into an open specification, scoped Petstore implementation, tests, and a human-reviewable PR for the SDLC Automation Demo.
triggers:
  - openhands-build
  - open spec
  - open specification
  - story to pr
  - sparse issue
---

# SDLC Request To PR

Use this skill when OpenHands turns a GitHub issue or issue comment into a small reviewable PR.

The customer-facing story is: a sparse GitHub request becomes an open specification, then an implementation branch, then a PR that humans review and merge.

## Inputs

- GitHub issue title, body, labels, and comments
- repository default branch
- target source branch
- acceptance criteria when present
- linked PRs or previous automation comments when present

Sparse issues are acceptable when the title maps to an existing Petstore behavior. Infer the smallest safe implementation, but write the assumptions and human gates into an open specification before editing code.

## GitHub Boundaries

- Trigger labels/comments: `openhands-build`
- Status labels: `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, `openhands:done`
- Use event context; do not poll GitHub.
- Avoid result comments that repeat the exact trigger text.
- Never merge, bypass review, change branch protection, or alter deployment settings.

## Workflow

1. Read `README.md`, `AGENTS.md`, and the issue context.
2. Run `python3 skills/sdlc-story/scripts/extract_acceptance_criteria.py "<issue title>"` with the issue body on stdin when useful.
3. Create or update an open spec at `specs/github-issue-<number>/open-spec.md`.
4. Validate the spec with `python3 skills/sdlc-story/scripts/validate_open_spec.py specs/github-issue-<number>/open-spec.md`.
5. Search existing app code and tests.
6. Implement a narrow change that satisfies the spec.
7. Add or update focused tests.
8. Run the narrowest useful validation first.
9. Open a draft PR with spec link, evidence, and human-review notes.

## Open Specification

Use `references/open-spec-template.md` for the required headings and demo-friendly language. The spec is not ceremony; it is the contract that connects the request, implementation, QA, review, and incident follow-up.

The spec must include:

- source issue/comment link
- assumptions and non-goals
- acceptance criteria
- human gates
- implementation plan
- validation plan
- evidence checklist

If a request has unresolved product, security, data, or environment questions, post the partial spec and label `openhands:needs-human` instead of guessing.

## Petstore Map

- Catalog behavior: `app/petstore_app/catalog.py`
- Adoption behavior: `app/petstore_app/adoptions.py`
- Static UI: `app/web/`
- Tests: `app/tests/`
- Open specs: `specs/github-issue-<number>/open-spec.md`

## Sparse Story Examples

`Filter pets by max adoption fee` means:

- add an optional max-fee filter to catalog search, using integer cents
- expose a simple static UI input only if the issue or PR scope includes UI
- add focused backend tests for match, exclusion, and invalid negative fees
- do not add payment processing, persistence, billing, auth, or dependencies

`Let adopters search by age range` means:

- add optional min/max age filters
- reject negative ages and inverted ranges
- keep default search limited to available pets
- add focused backend tests

## Stop Conditions

Ask for human input if the issue requires a product decision, schema migration, auth change, new dependency, environment change, secret access, or production mutation.

## PR Requirements

The PR body must show:

- open spec path
- assumptions and non-goals
- acceptance criteria status
- files changed
- tests run
- residual risks
- reminder that humans approve review and merge decisions
