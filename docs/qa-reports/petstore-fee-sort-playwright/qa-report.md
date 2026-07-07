# Playwright QA Report: Petstore Fee Sort UI

Status: pass

## Target

- URL: http://127.0.0.1:4173
- App: static Petstore web UI

## Browser Scenarios

- [x] Default catalog shows available pets and excludes pending pets
- [x] Sort control orders available pets from lowest fee to highest fee
- [x] Sort control can reverse the fee order
- [x] Species filter still works while sorting is enabled
- [x] Name search finds a matching available pet
- [x] Pending pet remains hidden and shows the empty state

## Artifacts

- Screenshot: petstore-fee-sort.png
- Video: petstore-fee-sort.webm
- GIF preview: petstore-fee-sort.gif

## Commands

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --bind 127.0.0.1 --directory app/web" \
  --port 4173 \
  -- node app/web/tests/catalog-search.playwright.mjs \
     --url http://127.0.0.1:4173 \
     --artifact-dir docs/qa-reports/petstore-fee-sort-playwright
```

## Notes

- This is the preferred browser-evidence path for UI-visible changes.
- If Playwright is unavailable in a remote automation runtime, fall back to dependency-free checks and say so explicitly.
