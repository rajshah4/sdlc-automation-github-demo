# Petstore Web UI Tests

This folder contains browser-oriented QA examples for the static Petstore UI.

For the customer-facing prebuilt UI/Playwright demo pointer, see
`docs/ui-playwright-example.md`.

## Playwright Example

`catalog-search.playwright.mjs` drives the real browser UI and produces the
artifact shape used in the automated QA demo:

- screenshot
- browser video
- GIF preview when `ffmpeg` is available
- markdown QA report

Run it with the repo-local server harness:

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- node app/web/tests/catalog-search.playwright.mjs \
     --url http://localhost:4173 \
     --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search
```

If Playwright is installed outside this repo, set `NODE_PATH` to that
`node_modules` directory. For example:

```bash
NODE_PATH=/path/to/node_modules \
PLAYWRIGHT_BROWSER_CHANNEL=chrome \
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- node app/web/tests/catalog-search.playwright.mjs \
     --url http://localhost:4173 \
     --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search
```

Live OpenHands automations should not install Playwright during the timed demo.
If the runtime does not already have Playwright or BrowserToolSet available,
fall back to dependency-free checks and report that browser evidence was not
collected.
