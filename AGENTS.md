# Agent Instructions

This is the GitHub-native SDLC Automation Demo. Customer-facing language should say "SDLC Automation Demo" and should not use "software factory."

## Repository Shape

- Petstore app: `app/petstore_app/`
- Backend tests: `app/tests/`
- Static UI: `app/web/`
- GitHub automations: `automations/github/`
- Repo-local OpenHands skills: `skills/`
- Setup and registration scripts: `scripts/`
- Demo docs: `docs/`

## Automation Rules

- Before creating, registering, or debugging OpenHands automations, read the OpenHands automation skill. In this environment it lives at `/Users/rajiv.shah/.openhands/cache/skills/public-skills/skills/openhands-automation/SKILL.md`, and it is also installed for Codex at `/Users/rajiv.shah/.codex/skills/openhands-automation/SKILL.md`.
- For automation smoke tests, start with the skill's basic path: create or inspect a simple automation, dispatch it manually with `/api/automation/v1/{id}/dispatch`, and verify `/api/automation/v1/{id}/runs` before adding GitHub, repo cloning, labels, or customer demo prompts.
- Humans approve scope, reviews, PRs, merges, deployments, and production changes.
- OpenHands may create branches, tests, comments, reports, and draft PRs when the relevant GitHub label or comment asks it to.
- Do not push directly to `main`.
- Do not print or commit secrets.
- Prefer deterministic scripts and preflight checks before spending LLM calls.
- Use event-driven GitHub triggers instead of polling.
- Verify prompt-preset `repos` uses a concrete repo URL before live registration. Do not register unresolved placeholders such as `${GITHUB_DEMO_REPO_URL}`.
- Avoid dependency installation in automation helper scripts unless a prompt explicitly authorizes it. Do not rely on `pip install` during timed customer demos; use existing dependencies or report the missing capability.
- Visible automation prompts should be demo-friendly: say what triggered the automation, what it does, what it posts back, where humans stay in control, and why the flow is cost/security-aware.

## Petstore Product Rules

- Default pet search returns only available pets.
- Pending pets can be shown only when explicitly requested and cannot be adopted.
- Money is represented as integer cents.
- UI-visible changes need UI evidence, not only unit tests.
