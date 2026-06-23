# Petstore UI Browser Checks

This folder contains browser-level checks for UI-visible Petstore changes.

Run the adoption fee filter smoke test with a local static server:

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- node app/web/tests/adoption-fee-filter.playwright.mjs
```

The script uses Playwright directly, interacts with the page through labels and
roles, and writes a screenshot to `/tmp/sdlc-petstore-playwright/`.

For local machines that have the Playwright package but not its browser cache,
set an installed browser channel:

```bash
PLAYWRIGHT_BROWSER_CHANNEL=chrome node app/web/tests/adoption-fee-filter.playwright.mjs
```

If Playwright is unavailable in the runtime, the QA automation should say so and
fall back to the dependency-free checks under `skills/sdlc-qa/scripts/`.
