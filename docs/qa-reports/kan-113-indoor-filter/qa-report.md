# Playwright QA Report: Indoor-Friendly Pet Filter

Status: pass

## Target

- URL: http://localhost:43113
- App: static Petstore web UI
- Feature: Indoor-only filter control

## Browser Scenarios

- [x] Filter disabled shows all available pets (Mochi, Scout, Pip)
- [x] Filter enabled shows only indoor-friendly pets (Mochi, Pip)
- [x] Filter unchecked restores all available pets
- [x] Indoor filter works with species filter (indoor cats)
- [x] Indoor filter works with name search (pip + indoor)

## Validation

- Playwright UI QA: pass
- Repository tests: 76 passed
- Browser: preinstalled Google Chrome, headless
- Dependencies: preprovisioned Playwright runtime; no package installation

## Artifacts

- Screenshot: indoor-filter.png
- Video: indoor-filter.webm
- GIF preview: indoor-filter.gif

## Commands

```bash
NODE_PATH=<preprovisioned-node-modules> PLAYWRIGHT_BROWSER_CHANNEL=chrome \
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 43113 --directory app/web" \
  --port 43113 \
  -- node app/web/tests/indoor-filter.playwright.mjs \
     --url http://localhost:43113 \
     --artifact-dir docs/qa-reports/kan-113-indoor-filter
```

## Notes

- This test validates the indoor-friendly pet filter feature added in PR #110
- Evidence was generated from commit `afc6cc0` plus the checkbox presentation fix in this PR
- OpenSpec scenarios: openspec/changes/jira-KAN-113-indoor-filter/specs/indoor-catalog-filter/spec.md
