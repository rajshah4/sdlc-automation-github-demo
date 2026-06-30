# Petstore Intelligence Pack

This is durable repo memory for the SDLC Automation Demo. Agents should read this before rediscovering the app from scratch.

## Product Rules

- Default pet search returns only available pets.
- Pending pets can be shown only when explicitly requested and cannot be adopted.
- Money is represented as integer cents.
- UI-visible changes need UI evidence, not only backend tests.
- Humans approve scope, PRs, merges, deployments, and production-facing fixes.

## App Map

| Surface | Files | Notes |
| --- | --- | --- |
| Catalog behavior | `app/petstore_app/catalog.py`, `app/tests/test_pet_catalog.py` | Search filters, availability rules, fee and age fields. |
| Adoption behavior | `app/petstore_app/adoptions.py`, `app/tests/test_adoptions.py` | Adoption validation and pending-pet safety. |
| Cloud Run incident surface | `app/petstore_app/cloud_run_app.py`, `app/tests/test_cloud_run_app.py` | Runtime incident mode and `/api/status`. |
| Static UI | `app/web/`, `app/web/tests/` | Browser evidence path for UI-visible changes. |
| OpenSpec-style changes | `openspec/changes/` | Generated proposal/design/tasks/spec artifacts for story-to-PR work. |

## Commands To Prefer

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
python3 scripts/build_context_reuse_report.py --fixture tests/fixtures/github_issue_labeled_context.json
```

For UI smoke evidence when the runtime supports it:

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```

## Reuse Notes

- Start from this file and `AGENTS.md`; do not re-infer product rules from every source file.
- Use `skills/sdlc-story/references/petstore-implementation-map.md` when sparse stories need file targeting.
- Use `docs/qa-reports/` as prior QA evidence and report style examples.
- Use `docs/work-log.md` and `docs/tested-demo-flow.md` for previous OpenHands run IDs and validated automation state.
