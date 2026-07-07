# Cost-Aware Context Reuse Report

This report is generated before broad model exploration. It shows which existing context a low-cost scout agent can load, summarize, and hand off to a stronger coding or review agent.

## Trigger

- Event: `manual.demo`
- Title: Filter pets by max adoption fee
- Labels: `openhands-context`

## Context Sources Used

### 1. Durable Repo Memory
- `AGENTS.md` (~630 tokens): repo rules, product constraints, commands, and reusable architecture notes.
- `docs/repo-memory/petstore-intelligence.md` (~544 tokens): repo rules, product constraints, commands, and reusable architecture notes.
- `docs/repo-memory/model-routing-policy.md` (~416 tokens): repo rules, product constraints, commands, and reusable architecture notes.

### 2. Skills As Procedural Memory
- `skills/sdlc-context-reuse/SKILL.md` (~763 tokens): task-specific workflow and stop conditions.
- `skills/sdlc-story/SKILL.md` (~1333 tokens): task-specific workflow and stop conditions.
- `skills/sdlc-qa/SKILL.md` (~1406 tokens): task-specific workflow and stop conditions.
- `skills/sdlc-code-review/SKILL.md` (~873 tokens): task-specific workflow and stop conditions.
- `skills/sdlc-incident/SKILL.md` (~1362 tokens): task-specific workflow and stop conditions.

### 3. Existing Logs And Evidence
- `docs/qa-reports/family-friendly-filter.md` (~1401 tokens): prior validation, QA, incident, or operator evidence.
- `docs/qa-reports/family-friendly-filter-playwright/qa-report.md` (~212 tokens): prior validation, QA, incident, or operator evidence.
- `skills/sdlc-incident/references/cloud-run-petstore-incident.md` (~870 tokens): prior validation, QA, incident, or operator evidence.

### 4. Targeted GitHub Repo Search

Search terms: `filter`, `max`, `adoption`, `fee`, `openhands-context`, `catalog`, `search`, `adoption_fee_cents`, `max_results`, `status`, `available`, `pending`

- `app/petstore_app/cloud_run_app.py` (score 108)
  - L11: from http import HTTPStatus
  - L17: from .adoptions import create_adoption_order
- `app/web/tests/family_friendly_filter_smoke.py` (score 42)
  - L3: Smoke test for the family-friendly filter feature.
  - L4: Tests the filter checkbox control and data filtering logic.
- `app/web/tests/catalog-search.playwright.mjs` (score 40)
  - L16: "/tmp/sdlc-petstore-playwright/catalog-search",
  - L37: console.error("Playwright is not available in this runtime.");
- `app/tests/test_pet_catalog.py` (score 35)
  - L1: import pytest
  - L3: from petstore_app.catalog import search_pets
- `app/petstore_app/catalog.py` (score 30)
  - L1: """Pet catalog behavior used by review and QA scenarios."""
  - L13: status: str
- `app/web/tests/family-friendly-filter.playwright.mjs` (score 28)
  - L16: "/tmp/sdlc-petstore-playwright/family-friendly-filter",
  - L37: console.error("Playwright is not available in this runtime.");
- `app/petstore_app/adoptions.py` (score 24)
  - L1: """Adoption order behavior used by validation and incident scenarios."""
  - L7: from .catalog import PETS, Pet
- `app/tests/test_adoptions.py` (score 23)
  - L1: import pytest
  - L3: from petstore_app.adoptions import create_adoption_order
- `app/tests/test_telemetry.py` (score 22)
  - L1: from petstore_app.telemetry import adoption_validation_error_event, search_latency_event
  - L4: def test_adoption_validation_error_event_matches_gcp_schema() -> None:
- `app/petstore_app/telemetry.py` (score 21)
  - L8: def adoption_validation_error_event(
  - L11: pet_status: str,

### 5. Previous Agent Runs / Conversation Memory
- `docs/repo-memory/previous-agent-runs.md` (~307 tokens): durable lessons and reusable file-path hints from prior agent runs.

## Cost-Aware Model Routing

| Phase | Work | Recommended tier | Why |
| --- | --- | --- | --- |
| Preflight | Parse event, labels, repo memory, deterministic search | No LLM or lowest-cost model | Fixed inputs and scripts do most of the work. |
| Scout | Summarize AGENTS.md, skills, logs, repo hits, prior runs | Low-cost model | Narrow context before expensive reasoning. |
| Implement | Edit code, update tests, create PR | Coding model | Requires coherent code changes. |
| Verify | Run tests and summarize evidence | Low-cost or deterministic | Prefer commands and exact output over reasoning. |
| Risk review | Security, production, or broad-change judgment | Medium/strong model | Escalate only when risk warrants it. |

## Reuse Decisions

- Reuse `AGENTS.md` and repo-memory docs before asking the model to rediscover product rules.
- Reuse skill procedures instead of restating task workflows in every prompt.
- Reuse prior QA reports, incident notes, and OpenHands run links before creating new evidence.
- Search focused code paths first; avoid loading unrelated app, Jira, GCP, and automation files unless the trigger requires them.
- Preserve durable findings in `docs/repo-memory/`; keep issue-specific details in reports or PRs.

## Token Reuse Estimate

- Text files in repo scan: 118
- Rough full-repo text estimate: ~78965 tokens
- Focused context estimate for this run: ~10362 tokens
- Illustrative context avoided before coding: ~68603 tokens

These are rough character-based estimates for live-demo comparison, not billing records. The point is the harness policy: load the known context first, then spend stronger model calls only where they change the outcome.

## Terraform Analogy For The Customer

- `AGENTS.md` becomes Terraform workspace rules, risk policy, module ownership, and approved commands.
- Skills become module-upgrade, moved-block, and plan-triage procedures.
- Existing logs become Terraform Cloud plans, previous apply errors, and validation output.
- GitHub search finds module usage and workspace-specific code paths without reading every repo.
- Old conversation memory captures what prior agents already learned about a workspace or module family.

