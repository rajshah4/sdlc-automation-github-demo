# Story-to-PR Report

**Run ID:** `canvas-tmp-stability-20260707-110100`
**Issue:** #101 — Filter pets by max adoption fee
**Timestamp:** 2026-07-07

---

## Branch

`feature/canvas-issue-101-max-adoption-fee-filter`

---

## OpenSpec Change Path

`openspec/changes/canvas-issue-101-max-adoption-fee-filter/`

Files:
- `proposal.md` — why, assumptions, non-goals, what changes, human gates
- `design.md` — backend/frontend design decisions and risks
- `tasks.md` — implementation checklist (all items checked)
- `specs/catalog-filter/spec.md` — spec delta for `search_pets()` signature

---

## Changed Files

| File | Change |
|------|--------|
| `app/petstore_app/catalog.py` | Added `max_fee_cents: int | None = None` parameter to `search_pets()` with `>= 0` validation and per-pet filter predicate |
| `app/tests/test_pet_catalog.py` | Added 4 focused tests: fee filter match, boundary inclusive, negative raises `ValueError`, `None` means no bound |
| `app/web/index.html` | Added `<input id="max-fee" type="number" min="0" step="1" placeholder="Any">` to toolbar |
| `app/web/app.js` | Added `feeToCents()` helper, max-fee filter predicate in `renderResults()`, and `input` event listener on `#max-fee` |

---

## Tests Run and Results

### Focused: `app/tests/test_pet_catalog.py`

```
9 passed in 0.01s
```

Tests cover:
- `test_search_pets_filters_by_max_fee` — Mochi ($75) and Pip ($45) returned when max is $120; Scout ($125) excluded
- `test_search_pets_includes_pets_at_exact_fee_boundary` — pet at exact threshold is included
- `test_search_pets_rejects_negative_max_fee` — `ValueError` raised for `max_fee_cents=-1`
- `test_search_pets_no_fee_filter_when_max_fee_none` — omitting the param returns all available pets

### Full suite regression

```
32 passed in 0.06s
```

No regressions.

---

## PR Link

**Draft PR #86:** https://github.com/rajshah4/sdlc-automation-github-demo/pull/86

Title: `feat: filter pets by max adoption fee (closes #101)`
State: open, draft

---

## Assumptions from the Sparse Story

1. **Available pets only** — the max-fee filter compounds with the existing `status="available"` default; pending pets are never shown (per product rule).
2. **Inclusive boundary** — a pet whose fee equals the max is included.
3. **Integer cents** — the backend stores and filters in integer cents; UI input is whole dollars converted locally with `feeToCents()`.
4. **Optional filter** — no input / empty field means no upper bound (`max_fee_cents=None`).
5. **No persistence** — filter state is per-session only (per sprint scope).
6. **No new services** — purely additive change to existing `search_pets()` function and static UI.
7. **Negative fee is invalid** — `ValueError` raised; HTML `min="0"` prevents browser-side negatives.

---

## Human Review Next Steps

1. **Scope approval** — confirm the implementation matches the intent of issue #101.
2. **Code review** — review the diff on PR #86; focus on `catalog.py` validation logic and `app.js` fee conversion.
3. **QA** — open `app/web/index.html` locally; verify the max-fee input filters the pet list in real-time.
4. **Mark ready for review** — when satisfied, remove draft status on PR #86.
5. **Merge** — merge after review approval (human gate).
6. **Deploy** — human deploys to production (human gate).
