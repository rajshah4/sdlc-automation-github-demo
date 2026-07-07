# SDLC Factory Lifecycle Report

**Run ID:** `codex-smoke-canvas-factory`  
**Repository:** `rajshah4/sdlc-automation-github-demo`  
**Generated:** 2026-06-30  
**Parent conversation purpose:** Orchestrate a full SDLC lifecycle—context recon, implementation, code review, QA, and incident triage—for story issue #101 (filter pets by max adoption fee) and an active petstore incident, delegating each gate to an isolated Agent Canvas child conversation without merging PRs, mutating production, or bypassing human approvals.

---

## Child Conversation Table

| Work Cell | Status | Conversation ID | UI URL | Artifact |
|-----------|--------|----------------|--------|---------|
| context-scout | ✅ done | `fc1aa845-62fd-47fe-b240-f927efb7f454` | [open](http://localhost:8000/conversations/fc1aa845-62fd-47fe-b240-f927efb7f454) | `factory_runs/codex-smoke-canvas-factory/context-scout.md` |
| story-to-pr | ✅ done | `08328969-a702-499d-8a09-802f2856e2dc` | [open](http://localhost:8000/conversations/08328969-a702-499d-8a09-802f2856e2dc) | `factory_runs/codex-smoke-canvas-factory/story-to-pr.md` |
| code-review | ⚠️ findings (non-blocking) | `d70df31e-1721-4a22-8617-27e67fab4f0a` | [open](http://localhost:8000/conversations/d70df31e-1721-4a22-8617-27e67fab4f0a) | `factory_runs/codex-smoke-canvas-factory/code-review.md` |
| qa | ✅ pass | `7729ee3a-63b8-4d1d-ad38-b2fcbc9ded9d` | [open](http://localhost:8000/conversations/7729ee3a-63b8-4d1d-ad38-b2fcbc9ded9d) | `factory_runs/codex-smoke-canvas-factory/qa.md` |
| incident | 🔴 needs-human | `51112f28-9d54-4de1-abc2-beb7e56ce70b` | [open](http://localhost:8000/conversations/51112f28-9d54-4de1-abc2-beb7e56ce70b) | `factory_runs/codex-smoke-canvas-factory/incident.md` |

---

## Story Request

**Issue:** #101  
**Title:** Filter pets by max adoption fee  
**Body:** As an adoption coordinator, I want to filter available pets by maximum adoption fee so families can find pets that fit their budget.

**Assumptions made by story-to-pr:**
- Fee amounts are expressed in integer cents throughout the backend; the UI converts a dollar string via `feeToCents()` before calling the filter.
- Filter is inclusive of the boundary: a pet with `adoption_fee_cents == max_fee_cents` is included.
- Negative max fee values are rejected with a `ValueError` (fail-fast, per repo conventions).
- The filter applies only to available pets; pending pets remain hidden regardless.

---

## Spec / Change Artifact

Folder created by story-to-pr: `openspec/changes/canvas-issue-101-max-adoption-fee-filter/`

Contents:
- `proposal.md` — one-paragraph feature summary
- `design.md` — API surface, UI interaction, feeToCents() convention, edge cases
- `tasks.md` — implementation checklist
- `spec-delta.md` — what changed versus the baseline openspec

---

## Branch and PR

| Key | Value |
|-----|-------|
| Branch | `feature/canvas-issue-101-max-adoption-fee-filter` |
| Pull Request | [#86 — Filter pets by max adoption fee](https://github.com/rajshah4/sdlc-automation-github-demo/pull/86) |
| Status | Draft — awaiting human review and approval before merge |

**Changes in the PR:**
- `app/petstore_app/catalog.py` — added optional `max_fee_cents` param to `search_pets()` with validation and filter predicate.
- `app/tests/test_pet_catalog.py` — 4 new tests: filter, boundary, negative guard, `None` passthrough.
- `app/web/index.html` — Max fee ($) input added to toolbar.
- `app/web/app.js` — `feeToCents()` helper + live `input` event listener for real-time filtering.
- `app/web/styles.css` — minimal styling for the new input.
- `openspec/changes/canvas-issue-101-max-adoption-fee-filter/` — OpenSpec-style change artefacts.

---

## Code Review Findings

**Blocking:** No  
**Full report:** `factory_runs/codex-smoke-canvas-factory/code-review.md`

| Severity | Finding |
|----------|---------|
| Important | One pre-existing unrelated test failure on `main` ships in the same PR — not introduced by this PR, but makes CI signal ambiguous. |
| Important | No CI pipeline; there is no automated safety net for future PRs against this repo. |
| Medium | `feeToCents` logic is inlined in `app.js` twice instead of calling the helper from a shared module. |
| Medium | The design doc says `change` event but the correct implementation uses `input` — doc should be updated to match. |
| Low | No screenshot or Playwright evidence is attached directly to the PR description; evidence exists locally in `ui-evidence/`. |

**Recommended pre-merge actions for the operator:**
1. Attach or link the `ui-evidence/` screenshots to PR #86.
2. Note the pre-existing test failure in the PR description so reviewers know it is not a regression.
3. Optionally deduplicate the inline `feeToCents` into a module-level function before merge.

---

## QA Evidence

**Status:** PASS  
**Full report:** `factory_runs/codex-smoke-canvas-factory/qa.md`

| Check | Result |
|-------|--------|
| Backend tests (focused) | 9/9 pass — includes all 4 new `max_fee_cents` tests |
| Backend tests (full suite) | 28/29 pass — 1 failure is pre-existing on `main`, unrelated to this PR |
| HTML static smoke | ✅ `max-fee` input, label, `type=number`, `min=0` confirmed |
| Browser: default view | ✅ All 3 available pets shown + Max fee ($) control visible |
| Browser: `$100` filter | ✅ Scout ($125) hidden; Mochi ($75) and Pip ($45) remain |
| Pending pets with filter | ✅ Nova (pending, $150) stays hidden regardless of filter value |
| Adoption / telemetry modules | ✅ No regressions |

**Screenshot artefacts:**
- `factory_runs/codex-smoke-canvas-factory/ui-evidence/ui-default-all-pets.png`
- `factory_runs/codex-smoke-canvas-factory/ui-evidence/ui-fee-filter-100.png`

---

## Incident: Pending Pets Visible in Available-Pets Experience

**Status:** needs-human (read-only triage complete; no production mutation performed)  
**Full report:** `factory_runs/codex-smoke-canvas-factory/incident.md`

### Root Cause
`visible_pets()` in `app/petstore_app/cloud_run_app.py` returns all pets including `pending` when `current_mode()` equals `"bad_catalog_filter"`. That mode is activated by either:
- The `INCIDENT_MODE` environment variable set to `bad_catalog_filter` on the Cloud Run service, or
- The runtime config file at `RUNTIME_CONFIG_PATH` (`/tmp/sdlc-automation-petstore-runtime-config.json`) containing `{"mode": "bad_catalog_filter"}`.

### Evidence
- Local code analysis confirms the filter bypass is deliberate (controlled incident class `petstore_website_catalog_regression`).
- All three local tests covering this scenario pass deterministically.
- `/api/status` returns HTTP 500 with `status: "degraded"` and `error_code: "PENDING_PET_VISIBLE"` when incident mode is active.
- GCP authentication was unavailable in this child; Cloud Logging and the live Cloud Run service were not queried.

### Remediation Recommendation (human-executed)
1. **Observe (safe, read-only):** `python3 scripts/petstore_gcp_observe.py` — confirm `safe_to_remediate: true`.
2. **Fix (human-approved):** `python3 scripts/petstore_config_fix.py` — restores the catalog filter to `healthy` mode.
3. **Verify:** Re-run `python3 scripts/petstore_gcp_observe.py` and confirm `/api/status` returns `200 OK`.

No PR was opened for the incident. The fix is a config restoration, not a code change.

---

## Human Gates Still Required

| Gate | Who | Why |
|------|-----|-----|
| Review PR #86 | Repo maintainer | Standard code review; do not merge without approval. |
| Merge PR #86 to `main` | Repo maintainer | Factory agents never merge. |
| Attach UI evidence to PR | Developer | Screenshots are local only; attach to PR #86 description before review. |
| Incident `petstore_gcp_observe.py` | Operator with GCP access | Verify `safe_to_remediate: true` before running the fix. |
| Incident `petstore_config_fix.py` | Operator with GCP access | Requires GCP credentials; no agent will run this. |
| CI pipeline setup | Maintainer | Currently missing; adds automated safety net for future work. |

---

## Exact Next Action for the Operator

```
1. Open PR #86 in your browser:
   https://github.com/rajshah4/sdlc-automation-github-demo/pull/86

2. Attach the UI screenshots from:
   factory_runs/codex-smoke-canvas-factory/ui-evidence/

3. Review the code-review findings in:
   factory_runs/codex-smoke-canvas-factory/code-review.md

4. Approve and merge PR #86 when satisfied.

5. For the incident — from a terminal with GCP credentials:
   python3 scripts/petstore_gcp_observe.py     # confirm safe_to_remediate
   python3 scripts/petstore_config_fix.py       # apply fix
   python3 scripts/petstore_gcp_observe.py     # verify healthy
```
