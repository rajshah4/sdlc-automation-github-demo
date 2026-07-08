# Playwright QA Report: Max Adoption Fee Filter

Status: pass

## Target

- URL: http://127.0.0.1:57563
- Feature: issue #88 — filter pets by max adoption fee

## Scenarios

- [x] Baseline shows all three available pets before fee filter
- [x] Below-threshold $80 filter: Mochi and Pip shown, Scout hidden
- [x] Exact-boundary $75: Mochi ($75 === limit, inclusive) and Pip ($45) shown; Scout ($125) excluded
- [x] Budget below all pets ($10) shows empty-state message
- [x] Clearing max fee input restores all three available pets

## Screenshots

- fee-below-threshold.png
- fee-exact-boundary.png
- fee-cleared.png

## Video

- max-adoption-fee-filter.webm
- GIF preview: max-adoption-fee-filter.gif
