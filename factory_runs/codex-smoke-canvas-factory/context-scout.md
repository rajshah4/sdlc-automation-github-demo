# Context Scout Report

**Run ID:** `codex-smoke-canvas-factory`
**Story:** Issue #101 — Filter pets by max adoption fee
**Scout date:** 2026-06-30
**Status:** done

---

## 1. Durable Repo Memory Loaded

| File | Tokens (est.) | Key takeaways |
|------|--------------|---------------|
| `AGENTS.md` | ~630 | Money is integer cents; default search returns available pets only; UI-visible changes need UI evidence; do not push to main |
| `docs/repo-memory/petstore-intelligence.md` | ~544 | App map confirmed; key surfaces are `catalog.py`, `test_pet_catalog.py`, `app/web/`; start here before exploring broadly |
| `docs/repo-memory/model-routing-policy.md` | ~416 | Scout → low-cost; implementation → coding model; QA → deterministic or low-cost |
| `docs/repo-memory/previous-agent-runs.md` | ~307 | **Prior run on Issue #1 produced PR #2 for max adoption fee filter.** Feature never merged to main. QA report template is `docs/qa-reports/family-friendly-filter.md`. |

---

## 2. Skills Loaded

| Skill | Role for this story |
|-------|---------------------|
| `skills/sdlc-context-reuse/SKILL.md` | Guides this scout pass; model routing policy |
| `skills/sdlc-story/SKILL.md` + `references/petstore-implementation-map.md` | Has a pre-written **Max Adoption Fee** implementation intent section — use it verbatim |
| `skills/sdlc-qa/SKILL.md` | QA smoke-test pattern and `with_server.py` wrapper |
| `skills/sdlc-code-review/SKILL.md` | Risk review guidance for the follow-on code-review cell |

Skills NOT loaded (not relevant to this feature): `sdlc-incident`.

---

## 3. Targeted Files Searched

| File | Why searched | Key finding |
|------|-------------|-------------|
| `app/petstore_app/catalog.py` | Core implementation target | `search_pets()` has NO `max_fee_cents` param; `Pet` dataclass has `adoption_fee_cents: int` field — feature is absent from main |
| `app/tests/test_pet_catalog.py` | Test baseline | 4 existing tests; no fee-filter test exists; pattern is straightforward `search_pets()` assertions |
| `app/web/app.js` | UI implementation target | Pet data uses `fee: "$75"` formatted string; family-friendly filter already present as implementation template |
| `app/web/index.html` | UI markup target | Checkbox control pattern from family-friendly filter is reusable for a number input |
| `app/web/tests/family_friendly_filter_smoke.py` | QA pattern reference | Static smoke pattern: fetch HTML and JS, assert on control presence and filter logic |
| `skills/sdlc-story/references/petstore-implementation-map.md` | Implementation guide | **Max Adoption Fee section already written** with implementation intent, non-goals, and validation commands |
| `docs/qa-reports/family-friendly-filter.md` | QA report template | Full QA report style example; six scenarios, each with expected/actual/result |
| `openspec/changes/` | Prior change artifacts | **Empty** — no existing folder for issue #101; story-to-pr must create one |

---

## 4. Likely Implementation Surfaces

### 4a. Backend — `app/petstore_app/catalog.py`

```python
def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",
    tag: str | None = None,
    max_fee_cents: int | None = None,   # ADD THIS
    max_results: int = 10,
) -> list[Pet]:
```

- Validate `max_fee_cents >= 0` (raise `ValueError` on negative).
- Add filter: `if max_fee_cents is not None and pet.adoption_fee_cents > max_fee_cents: continue`.
- Position the fee check before the `max_results` slice.

### 4b. Backend Tests — `app/tests/test_pet_catalog.py`

Add four tests following existing style:
1. `test_search_pets_filters_by_max_fee` — all pets under $120 (Mochi $75, Pip $45; Scout $125 excluded).
2. `test_search_pets_includes_pets_at_exact_fee_boundary` — max_fee_cents=7500 includes Mochi.
3. `test_search_pets_rejects_negative_max_fee` — `pytest.raises(ValueError)`.
4. `test_search_pets_no_fee_filter_when_max_fee_none` — default returns all available pets.

Data for reference:
- Mochi: `adoption_fee_cents=7500` (available)
- Scout: `adoption_fee_cents=12500` (available)
- Pip: `adoption_fee_cents=4500` (available)
- Nova: `adoption_fee_cents=11000` (pending — excluded by default status filter)

### 4c. UI — `app/web/app.js`

- Add `maxFee` state read from a number input (dollar amount).
- Convert user input to cents: `const maxFeeCents = maxFee ? Math.round(parseFloat(maxFee) * 100) : null`.
- Add filter predicate: `&& (maxFeeCents === null || feeToCents(pet.fee) <= maxFeeCents)`.
- Add helper `feeToCents(feeStr)` that strips `$` and multiplies by 100.
- Wire a `change` event listener on the new input (same pattern as `#family-friendly`).

### 4d. UI — `app/web/index.html`

Add a number input inside the `.toolbar` section:

```html
<label>
  Max fee ($)
  <input id="max-fee" type="number" min="0" step="1" placeholder="Any">
</label>
```

### 4e. UI — `app/web/styles.css`

Minor: ensure the new input is visually consistent with the existing search controls. Copy the pattern used for `#query`.

### 4f. OpenSpec Artifacts — `openspec/changes/github-issue-101-max-adoption-fee-filter/`

Create:
- `proposal.md` — why, what changes, impact, assumptions, non-goals
- `design.md` — smallest safe implementation (no persistence, no currency conversion, integer cents backend, dollar-input UI)
- `tasks.md` — checklist of backend param, validation, tests, UI input, UI filter, UI smoke test, PR
- `specs/catalog-filter/spec.md` — acceptance criteria as requirements and scenarios

Use `skills/sdlc-story/references/open-spec-template.md` for the heading shape.

---

## 5. Test and Browser Evidence Surfaces

| Surface | Command | Evidence type |
|---------|---------|--------------|
| Backend unit tests | `python3 -m pytest -q app/tests/test_pet_catalog.py` | Pass/fail output |
| Full suite | `python3 -m pytest -q` | Regression guard |
| UI smoke (static) | `python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173` | HTML/JS assertions |
| UI smoke (with server) | `python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173` | Integrated server + smoke |
| Playwright (optional) | `app/web/tests/catalog-search.playwright.mjs` | Screenshot / video evidence (requires Playwright) |

QA report template: `docs/qa-reports/family-friendly-filter.md`.

---

## 6. Risks, Assumptions, and Human Questions

### Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Fee representation mismatch: backend uses integer cents (`adoption_fee_cents`), UI uses formatted string (`fee: "$75"`). | Medium | Story-to-PR agent must add `feeToCents()` helper in JS and document the convention. Do not change the backend data format. |
| Multiple prior remote branches exist (`feature/add-max-adoption-fee-filter`, `feature/filter-pets-by-max-adoption-fee`, `remotes/origin/codex/ui-adoption-fee-filter`, etc.). None merged to main. | Low | Start fresh from main; optionally inspect a prior branch for reference patterns but do not rebase or carry over stale decisions. |
| GitHub issue #101 returned 404 (may not exist yet or token gap). | Low | Story text is provided via factory run input; proceed on that basis. GitHub label gates are not needed for the factory run. |

### Assumptions

- Max fee filter applies to available pets only (product rule enforced by existing `status` default).
- UI input is in whole dollars; the filter converts to cents before comparison.
- Negative max_fee_cents raises `ValueError` (consistent with `max_results` guard pattern).
- A missing or empty max fee input means no upper bound (optional parameter).
- No new dependencies; UI remains a single-file static app.

### Human Questions

None blocking. The story is well-defined, maps directly to the `petstore-implementation-map.md` Max Adoption Fee section, and prior QA evidence patterns are available.

---

## 7. Context Reuse Report

The deterministic context script was run successfully:

```
python3 scripts/build_context_reuse_report.py \
  --output factory_runs/codex-smoke-canvas-factory/context-reuse-report.md
```

Output: `factory_runs/codex-smoke-canvas-factory/context-reuse-report.md`

Illustrative token savings: ~68,603 tokens of broad repo exploration avoided by loading focused context first.

---

## 8. Model Routing Recommendation

| Phase | Cell | Recommended tier |
|-------|------|-----------------|
| This scout | context-scout | Low-cost / no LLM (deterministic scripts + this summary) |
| Implementation | story-to-pr | Coding model |
| Test evidence | qa | Low-cost or deterministic (pytest output is the source of truth) |
| Diff risk review | code-review | Medium model; escalate only if security or broad-architecture concerns surface |

---

## 9. Recommendation

**The story-to-pr child can proceed.**

All implementation surfaces are identified, test patterns are available, OpenSpec artifact structure is documented in the skill, and prior QA report style is in `docs/qa-reports/`. No human clarification is needed before implementation begins.
