# QA Report: PR #159 — Fix: Enable Enter key for pet search (KAN-162)

**Verdict: PASS ✅**

Date: 2026-08-27  
Branch: `jira-kan-162-enter-key-search` → `main`  
PR: https://github.com/rajshah4/sdlc-automation-github-demo/pull/159  
Conversation: https://app.replicated.rajistics.com/conversations/2309fc15-bf10-430b-9999-0b5c43d61545

---

## Browser Environment

| Component | Version |
|---|---|
| Runtime | Real Chromium (Playwright-managed headless) |
| Browser | Google Chrome for Testing 151.0.7922.34 |
| Playwright | v1.62.1 (npm, installed to /tmp/playwright-qa outside repo) |
| Node.js | v22.23.2 |
| Browser binary | /tmp/playwright-browsers/chromium-1234/chrome-linux64/chrome |
| Platform | Linux amd64 (headless) |

> All tests used real Chromium executing full DOM interaction — not static checks, not mocks.

---

## Change Summary

`app/web/app.js` gained two `keydown` listeners: one on `#query` (Pet name) and one on `#species` (Species dropdown). Each fires `renderResults()` when `Enter` is pressed. No other behavior was changed.

`app/web/tests/catalog-search.playwright.mjs` was extended with two new browser scenarios:
- Enter key in Pet name input → filters pets
- Enter key in Species dropdown → filters pets

---

## BEFORE Baseline (origin/main)

**Worktree:** `/tmp/petstore-main-baseline` (detached HEAD at `e2e96b1`, `origin/main`)  
**Server:** `python3 -m http.server 4174 --directory /tmp/petstore-main-baseline/app/web`  
**Script:** `/tmp/playwright-qa-before.mjs` (ad-hoc, run outside repo)

### Commands Run

```bash
# Create worktree for main (does not mutate main)
git worktree add /tmp/petstore-main-baseline origin/main

# Start baseline server
python3 -m http.server 4174 --directory /tmp/petstore-main-baseline/app/web &

# Run BEFORE test
PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers \
NODE_PATH=/tmp/playwright-qa/node_modules \
node /tmp/playwright-qa-before.mjs
```

### Observed Behavior (main — no Enter key fix)

| Step | Action | Observed Result |
|---|---|---|
| Initial load | Navigate to `http://localhost:4174` | Shows Mochi, Scout, Pip (all available) |
| Enter key | Fill "mochi" in Pet name, press Enter | Shows **Mochi, Scout, Pip** (unchanged — Enter did nothing) |
| Button click | Fill "mochi" in Pet name, click "Find Pets" | Shows **Mochi** only (button search works) |

**Key finding:** After pressing Enter in the Pet name field with "mochi" typed, all three available pets remained visible. The list was NOT filtered. This proves the BEFORE state lacks Enter key support.

**Screenshot:** `before-enter-key-no-filter.png` — shows all three pets still listed after Enter  
**GIF:** `before-baseline.gif` — records the full BEFORE session including no-op Enter key

---

## AFTER: PR Branch (jira-kan-162-enter-key-search)

**Server:** `python3 -m http.server 4173 --directory app/web` (PR branch checkout)  
**Script:** `app/web/tests/catalog-search.playwright.mjs` (checked-in, unmodified by QA)

### Commands Run

```bash
# Start PR branch server
python3 -m http.server 4173 --directory app/web &

# Run checked-in Playwright test
PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers \
NODE_PATH=/tmp/playwright-qa/node_modules \
PLAYWRIGHT_ARTIFACT_DIR=/tmp/playwright-evidence/after \
node app/web/tests/catalog-search.playwright.mjs \
  --url http://localhost:4173 \
  --artifact-dir /tmp/playwright-evidence/after

# Create GIF from video
ffmpeg -y -i /tmp/playwright-evidence/after/catalog-search.webm \
  -vf "fps=8,scale=960:-1:flags=lanczos" \
  /tmp/playwright-evidence/after/catalog-search.gif
```

### Scenarios Run and Outcomes

| # | Scenario | Selector / Action | Expected | Observed | Result |
|---|---|---|---|---|---|
| 1 | Default catalog shows available pets, excludes pending | Load page | Mochi, Scout, Pip | Mochi, Scout, Pip | ✅ PASS |
| 2 | Species filter narrows results | `getByLabel("Species").selectOption("dog")` + button | Scout | Scout | ✅ PASS |
| 3 | Name search via button | `getByLabel("Pet name").fill("pip")` + button | Pip | Pip | ✅ PASS |
| 4 | **Enter key in Pet name triggers search** | `getByLabel("Pet name").fill("mochi")` + `.press("Enter")` | Mochi | Mochi | ✅ PASS |
| 5 | **Enter key in Species dropdown triggers search** | `getByLabel("Species").selectOption("dog")` + `.press("Enter")` | Scout | Scout | ✅ PASS |
| 6 | Pending pet (Nova) remains hidden | `getByLabel("Pet name").fill("nova")` + button | empty-state message | "No available pets match this search." | ✅ PASS |

All 6 scenarios passed.

**Screenshot:** `catalog-search.png` — full-page screenshot after all scenarios  
**GIF:** `catalog-search.gif` — animated record of complete Playwright session (88 KB)

---

## Before / After Comparison

| Behavior | BEFORE (main) | AFTER (PR branch) |
|---|---|---|
| Enter key in Pet name | ❌ No-op — all pets remain | ✅ Filters to matching pets |
| Enter key in Species | ❌ Not present | ✅ Filters to matching species |
| Button search | ✅ Works | ✅ Still works |
| Pending pet exclusion | ✅ Hidden | ✅ Still hidden |

---

## Artifacts

| File | Description |
|---|---|
| `before-enter-key-no-filter.png` | Screenshot: main branch — Enter key did not filter |
| `before-baseline.gif` | GIF: full BEFORE Playwright session (61 KB) |
| `catalog-search.png` | Screenshot: PR branch — full page after all scenarios pass |
| `catalog-search.gif` | GIF: full AFTER Playwright session (88 KB) |
| `qa-report.md` | This report |

Raw video files (`.webm`) and temporary Playwright/browser files were not committed to the repository.

---

## Petstore Contract Checks

| Contract | Status |
|---|---|
| Default search returns only available pets | ✅ Verified (Nova absent by default) |
| Pending pet cannot be found by search | ✅ Verified (Nova → empty state) |
| Button search still works | ✅ Verified |
| Enter key now works in Pet name field | ✅ Verified (PR adds this) |
| Enter key now works in Species dropdown | ✅ Verified (PR adds this) |

---

## Residual Risk

- Low. The change adds keyboard shortcuts as aliases to the existing button; no filtering logic was changed.
- The Enter key listener on `#species` uses a `keydown` event on a `<select>` element. Most browsers fire `keydown` for Enter on a focused select after a value has been chosen. This was confirmed in Chromium 151. Other browsers (Safari, Firefox) were not tested.
- No accessibility attributes (e.g., `aria-keyshortcuts`) were added; this is an enhancement for keyboard users but not a formal a11y regression.
