# Agent Instructions

This is the GitHub-native SDLC Automation Demo. Customer-facing language should say "SDLC Automation Demo" and should not use "software factory."

## Repository Shape

- Petstore app: `app/petstore_app/`
- Backend tests: `app/tests/`
- Static UI: `app/web/`
- GitHub automations: `automations/github/`
- Repo-local OpenHands skills: `.agents/skills/`
- Setup and registration scripts: `scripts/`
- Demo docs: `docs/`

## Automation Rules

- Humans approve scope, reviews, PRs, merges, deployments, and production changes.
- OpenHands may create branches, tests, comments, reports, and draft PRs when the relevant GitHub label or comment asks it to.
- Do not push directly to `main`.
- Do not print or commit secrets.
- Prefer deterministic scripts and preflight checks before spending LLM calls.
- Use event-driven GitHub triggers instead of polling.
- Avoid dependency installation in automation helper scripts unless a prompt explicitly authorizes it.

## Petstore Product Rules

- Default pet search returns only available pets.
- Pending pets can be shown only when explicitly requested and cannot be adopted.
- Money is represented as integer cents.
- UI-visible changes need UI evidence, not only unit tests.

