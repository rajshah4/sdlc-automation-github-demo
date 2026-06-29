# Petstore Implementation Map

Use this reference when a sparse GitHub request needs to be grounded in the demo app.

## Core Files

| Area | Files | Contract |
| --- | --- | --- |
| Catalog search | `app/petstore_app/catalog.py`, `app/tests/test_pet_catalog.py` | Default search returns available pets only. Pending pets appear only when status is explicit. |
| Adoption order | `app/petstore_app/adoptions.py`, `app/tests/test_adoptions.py` | Pending or adopted pets cannot be adopted. |
| Cloud Run surface | `app/petstore_app/cloud_run_app.py`, `app/tests/test_cloud_run_app.py` | Runtime incident mode can expose pending pets and emit structured logs. |
| Static UI | `app/web/index.html`, `app/web/app.js`, `app/web/styles.css` | UI should remain dependency-free and simple to smoke test. |
| Demo docs and logs | `docs/wiki/petstore-catalog-availability.md`, `docs/logs/pending-pet-visible.ndjson` | Sparse bug reports can point to business rules and log evidence without spelling out the code path. |

## Common Bug Slices

### Pending Pet Visible In Available Catalog

Implementation intent:

- Keep default catalog search limited to `status="available"`.
- Preserve explicit `status="pending"` support searches.
- Map Nova to `pet-103` and the `PENDING_PET_VISIBLE` evidence.
- Add regression tests that default and available-only searches exclude pending pets.

Non-goals:

- cloud remediation
- deployment changes
- auth, secrets, or IAM changes
- persistence changes
- unrelated UI redesign

## Common Feature Slices

### Max Adoption Fee

Implementation intent:

- Add optional max-fee filtering using integer cents.
- Reject negative values.
- Preserve default status filtering.
- Add tests for included pets, excluded pets, and invalid input.

Non-goals:

- payment processing
- persistence
- currency conversion
- billing or checkout UI
- new dependencies

### Age Range Filter

Implementation intent:

- Add optional minimum and maximum age filters.
- Reject negative values.
- Reject inverted ranges.
- Preserve `max_results` validation.

## Validation Commands

```bash
python3 -m pytest -q app/tests/test_pet_catalog.py
python3 -m pytest -q app/tests/test_adoptions.py
python3 -m pytest -q
```

For UI-visible changes:

```bash
python3 -m http.server 4173 --directory app/web
python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```
