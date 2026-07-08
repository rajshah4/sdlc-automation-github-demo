# Tasks: Filter pets by maximum adoption fee

## Checklist

- [x] Proposal and design written (`proposal.md`, `design.md`)
- [x] Spec delta created (`specs/pet-catalog/spec.md`)
- [x] `catalog.py` — add `max_fee_cents` param, guard, and filter step
- [x] `test_pet_catalog.py` — add match, exclusion, and negative-fee tests
- [x] `index.html` — add max adoption fee number input to toolbar
- [x] `app.js` — add `feeCents` to pet data; apply max-fee filter in `renderResults`
- [x] `catalog-search.playwright.mjs` — add browser scenario for fee filter
- [x] Backend tests pass (`pytest app/tests/test_pet_catalog.py`)
- [x] Draft PR opened from this workcell
- [x] `factory_runs/canvas-verify-full/story-to-pr.md` written

## Human Gates

- [ ] Scope approval (story issue review by coordinator)
- [ ] Code review (GitHub PR review)
- [ ] QA sign-off (Playwright + pytest)
- [ ] Merge (repository maintainer)
