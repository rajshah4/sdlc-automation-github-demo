# Playwright QA Report: Petstore Catalog Count

Status: pass

## Target

- URL: http://localhost:4188
- App: static Petstore web UI
- Feature: Available pet count display (KAN-120)

## Browser Scenarios

- [x] Default catalog shows count of 3 available pets
- [x] Count updates to 1 pet (singular) when filtering by species
- [x] Count shows 1 available cat (Mochi)
- [x] Count updates correctly with name search
- [x] Count returns to 3 pets (plural) after clearing filters
- [x] Count shows 0 when searching for pending pet (Nova)
- [x] Count shows 0 for non-existent pet name
- [x] Final evidence view restores all 3 available pets

## Artifacts

- Screenshot: catalog-count.png
- Video: catalog-count.webm
- GIF preview: catalog-count.gif

## Commands

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4188 --directory app/web" \
  --port 4188 \
  -- node app/web/tests/catalog-count.playwright.mjs \
     --url http://localhost:4188 \
     --artifact-dir docs/qa-reports/catalog-count-playwright
```

## Notes

- Tests the count display added in PR #116 (KAN-120)
- Verifies count updates with filters and handles singular/plural correctly
- Confirms pending pets are excluded from available count
