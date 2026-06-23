# Web App Testing Reference

Use this reference when a PR changes `app/web/` or a backend change affects user-visible UI behavior.

## Decision Tree

1. If the app is static HTML/JS/CSS, serve `app/web` with Python's built-in HTTP server.
2. Infer browser scenarios from the diff. Do not depend on PR text listing exact test steps.
3. If Playwright is already available in the environment, use it to inspect the page, interact with controls, record video, capture screenshots, and produce a GIF preview when possible.
4. If Playwright is not available, use dependency-free checks:
   - `skills/sdlc-qa/scripts/static_ui_smoke.py`
   - targeted HTML/JS inspection
   - `urllib` checks against the served app
5. If the UI depends on a live backend not available in the test environment, document the missing service and test the boundary that is available.

Do not install browsers or Python packages during the demo.

## Scenario Inference

For static Petstore UI changes, infer scenarios from the changed surface:

- New input/select/button: test default state, one successful interaction, and one boundary or validation path.
- New validation text or aria-live region: trigger the invalid state and assert the message appears.
- New filtering/sorting behavior: assert included and excluded pet names, including pending-pet exclusion where relevant.
- Fee or money changes: assert integer-cent data paths and user-facing formatted values.
- Empty-state changes: trigger the no-results state and assert the displayed message.

The PR body may be intentionally short. It is acceptable to read it for intent,
but the browser test plan should come from the diff plus existing product rules.

## Server Harness

Use the bundled harness to start and clean up local servers:

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```

## UI Evidence Expectations

For UI-visible changes, prefer the full browser evidence bundle:

- Playwright/spec file committed to the PR branch
- screenshot path or committed screenshot
- `.webm` video path when available
- GIF preview converted from the browser video when `ffmpeg` is available
- `qa-report.md` summary
- PR comment with inline GIF or artifact links
- browser interaction notes with selectors/roles used

Do not report "UI passed" unless you opened or served the UI surface. Do not
present DOM/static checks as equivalent to browser interaction; label them as
fallback evidence.

## Playwright Artifact Pattern

When generating a Playwright smoke for a static UI PR:

1. Put the script near the UI, for example `app/web/tests/<feature>.playwright.mjs`.
2. Use accessible selectors such as labels and roles before brittle CSS selectors.
3. Record video with Playwright `recordVideo`.
4. Capture a full-page screenshot.
5. If `ffmpeg` exists, convert the video to a small GIF:

```bash
ffmpeg -y -i input.webm -vf "fps=8,scale=960:-1:flags=lanczos" output.gif
```

6. Write a short `qa-report.md` with scenarios, pass/fail status, and artifact paths.
7. Commit lightweight artifacts under a demo artifact folder such as
   `docs/demo-artifacts/pr<NUMBER>/` when they help the customer see the result
   in GitHub.
8. Link the report and embed the GIF in the PR comment.

## Static Petstore Checks

The static UI should continue to show:

- Petstore identity
- search controls and available-pets wording
- stable controls for the changed behavior
- no trigger phrases in automation result text

When the PR adds a UI control, assert that the control exists and that its label/value maps to the open specification.
