# Tasks

- [x] Create OpenSpec-style change folder with proposal, spec delta, design, and tasks.
- [x] Validate change folder shape with `scripts/validate_open_spec.py`.
- [x] Add `max_fee_cents: int | None = None` to `search_pets()` in `catalog.py` with validation and filter predicate.
- [x] Add four focused tests in `test_pet_catalog.py`: filter match, boundary inclusive, negative raises, None means no bound.
- [x] Add `<input id="max-fee" ...>` to toolbar in `index.html`.
- [x] Add `feeToCents()` helper and max fee filter predicate in `app.js`.
- [x] Wire `change` listener on `#max-fee` input.
- [x] Run `python3 -m pytest -q app/tests/test_pet_catalog.py` — all pass.
- [x] Run `python3 -m pytest -q` — full suite clean.
- [x] Open draft PR with OpenSpec change link and human-review notes.

## Human Gates

- [ ] Scope approval: human confirms this implementation matches intent of issue #88.
- [ ] Code review: human reviews the PR diff.
- [ ] Merge approval: human merges after review.
- [ ] Deployment: human deploys to production.
