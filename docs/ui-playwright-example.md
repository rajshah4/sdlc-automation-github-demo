# Prebuilt UI And Playwright Example

Use this page when you want to show the richer browser-QA path without making
the live Jira demo depend on Playwright being installed in the Rajistics
automation runtime.

## Recommended Demo Split

Run the live customer demo with the non-UI bug path:

1. Create a sparse Jira bug in project `KAN`.
2. Let Rajistics OpenHands find docs/logs, identify the repo, fix the bug, add
   backend tests, open a draft PR, and add `openhands-qa`.
3. Show the second QA conversation and the PR comment.
4. Keep human review and merge as the final control point.

Then, when you want to show UI/browser evidence, point to the prebuilt example
below instead of creating a live browser-tooling dependency.

## Canonical UI Example

The clearest UI/Playwright example is:

- PR: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/6`
- Title: `Add adoption fee filter to Petstore UI`
- Branch: `codex/ui-adoption-fee-filter`
- QA label path: `openhands-qa` -> `openhands:done`

What to show in the PR:

- UI files changed:
  - `app/web/index.html`
  - `app/web/app.js`
  - `app/web/styles.css`
- Browser test added:
  - `app/web/tests/adoption-fee-filter.playwright.mjs`
- Demo artifacts committed on the PR branch:
  - `docs/demo-artifacts/pr6/adoption-fee-filter.gif`
  - `docs/demo-artifacts/pr6/adoption-fee-filter.png`
  - `docs/demo-artifacts/pr6/qa-report.md`
- PR comment with the inline browser artifact:
  - `https://github.com/rajshah4/sdlc-automation-github-demo/pull/6#issuecomment-4775361230`
- QA report comment:
  - `https://github.com/rajshah4/sdlc-automation-github-demo/pull/6#issuecomment-4775349283`

## Talk Track

Use this simple explanation:

> The live Jira demo is intentionally boring and reliable: it proves sparse
> business-language bugs can become PRs with tests and QA without extra setup.
> When the change is UI-visible and browser tooling is available, the QA work
> cell can also add a Playwright spec, run the real web UI, capture screenshot
> and video evidence, convert that into a GIF, and post the evidence back on the
> PR. PR #6 is the prebuilt example of that richer path.

The important point is that UI evidence is a capability of the QA work cell, not
a requirement for every bug demo.

## What This Proves

The UI example shows that OpenHands can:

- infer a browser scenario from the diff and product rule
- add or update a Playwright smoke test
- serve the static Petstore UI
- interact with real controls in a browser
- capture screenshot/video/GIF artifacts
- write a concise QA report
- post the evidence back to the PR

## Why The Live Rajistics Demo Does Not Install Playwright

Playwright is heavier than a normal test dependency. Installing it live can
require registry access, browser downloads, native OS libraries, and extra
runtime permissions. That makes the demo slower and less deterministic.

For customer demos, use one of these paths:

- Preferred: preinstall Playwright or BrowserToolSet in the Rajistics runtime.
- Current live path: let QA report the missing browser capability and run
  deterministic fallback checks.
- Presentation path: point to PR #6 as the prebuilt browser-evidence example.

Do not make the timed Jira demo install Playwright live unless the goal is
specifically to test runtime provisioning.

## Local Browser Evidence Command

When Playwright is already installed in a prepared environment, use the same
artifact pattern locally:

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

The checked-in baseline script is `app/web/tests/catalog-search.playwright.mjs`.
For UI PRs, QA should generate feature-specific scripts beside it and include
lightweight PR-branch artifacts when useful.
