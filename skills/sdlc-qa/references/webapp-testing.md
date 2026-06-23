# Web App Testing Reference

Use this reference when a PR changes `app/web/` or a backend change affects user-visible UI behavior.

## Decision Tree

1. If the app is static HTML/JS/CSS, serve `app/web` with Python's built-in HTTP server.
2. If Playwright is already available in the environment, use it to inspect the page, interact with controls, and capture screenshots.
3. If Playwright is not available, use dependency-free checks:
   - `skills/sdlc-qa/scripts/static_ui_smoke.py`
   - targeted HTML/JS inspection
   - `urllib` checks against the served app
4. If the UI depends on a live backend not available in the test environment, document the missing service and test the boundary that is available.

Do not install browsers or Python packages during the demo.

## Server Harness

Use the bundled harness to start and clean up local servers:

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```

## UI Evidence Expectations

For UI-visible changes, collect at least one of:

- screenshot path
- DOM assertion output
- static smoke output
- browser interaction notes with selectors used

Do not report "UI passed" unless you opened or served the UI surface.

## Static Petstore Checks

The static UI should continue to show:

- Petstore identity
- search controls and available-pets wording
- stable controls for the changed behavior
- no trigger phrases in automation result text

When the PR adds a UI control, assert that the control exists and that its label/value maps to the open specification.
