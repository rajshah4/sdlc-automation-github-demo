# Work Log

## 2026-06-22

- Created a fresh GitHub-native SDLC Automation Demo repo instead of modifying the Azure DevOps demo in place.
- Copied safe Petstore app, tests, GitHub provider adapter, GCP helper scripts, and integration docs from the existing demo.
- Did not copy `.env`, `.git`, Azure automation tarballs, or secret-bearing material.
- Added GitHub labels, issue templates, prompt-preset automation packages, setup docs, and deterministic preflight scripts.
- Added repo-local OpenHands skills under `skills/` so automation behavior is version controlled, easy to browse, and visible in GitHub.
- Created and pushed the private GitHub repo `rajshah4/sdlc-automation-github-demo`.

## 2026-06-23

- Reworked the repo-local skills into four broad automation skills:
  - `sdlc-story`: sparse GitHub issue to OpenSpec-style change artifacts to PR.
  - `sdlc-qa`: automated test-suite buildout and UI evidence.
  - `sdlc-incident`: SRE incident triage with Cloud Run/Cloud Logging evidence and bounded remediation.
  - `sdlc-code-review`: OpenHands `/codereview` with Petstore risk and supply-chain checks.
- Folded earlier helper skills into references and scripts under the four primary skills.
- Added a lightweight OpenSpec-inspired template and validation tooling so the request-to-PR flow has a versioned specification artifact.
- Added QA references and a local server harness adapted from the automated QA demo pattern.
- Added SRE references and observation-summary tooling adapted from the Cloud Run incident demo pattern.
- Added code-review risk and supply-chain references based on OpenHands code-review guidance.
- Reworked the story-to-PR specification layer to show clear Fission-AI/OpenSpec lineage: `openspec/changes/<change-id>/proposal.md`, `design.md`, `tasks.md`, and `specs/.../spec.md`. The skill explains why the timed automation writes artifacts directly instead of installing or invoking the OpenSpec CLI live.
- Added a checked-in Playwright UI evidence example for the Petstore web app, including screenshot/GIF/report generation for PR evidence and fallback guidance for remote runtimes without browser tooling.
- Registered the four OpenHands prompt-preset automations with the Rajistics Replicated API key:
  - build: `0ce7add1-fbba-40ef-bc0d-bef77f1bd108`
  - incident: `31c15181-2c7a-446e-8156-232808e6d1fc`
  - QA: `d6f6e6f9-202c-45cc-afcc-69cf5379fb16`
  - review: `a8605df3-d80a-487c-bf11-1932f81a2c0c`
- Validated the Rajistics build automation path: issue #1 produced conversation `https://app.replicated.rajistics.com/conversations/060aa6399eae4e77b2fcd630646fbe56`, completed automation run `f84671ac-33b7-43d8-a0e4-3532fb180263`, moved issue #1 to `openhands:done`, posted an implementation summary, and opened PR #2 for the max adoption fee filter.
- Removed the temporary GitHub workflow path from the active demo. The live demo now uses GitHub labels and OpenHands Automations only.
- Disabled the comment-capable automation set and registered the active label-only set:
  - build: `efc16fdb-04da-4140-963a-5e693bbc8bb4`
  - incident: `4c9ebc42-eb96-4cc5-a4a7-13089bdd6506`
  - QA: `fe3ea75f-dfbb-4779-a73f-a287380fdb27`
  - review: `854dcbb9-0320-40f2-a8a7-e70d15cb737c`
- Did not re-trigger issue #1 after label-only registration because it is already complete and should not create duplicate work.
- Simplified issue #1 so it reads like a normal product request and pruned the old test/acknowledgement comments, leaving the OpenHands completion summary and PR link.
- Verified through the Rajistics API that the active automation set is enabled, label-only, and guarded against items already marked `openhands:done`.
- Simplified the tracked repo layout for customer-facing use by removing the temporary provider abstraction, top-level event fixtures, and duplicate integrations samples. Test fixtures now live under `tests/fixtures`.

## 2026-06-29

- Pivoted the build/demo assets from a feature-request hero story to a bug-first path: customers are seeing pets that are not available.
- Added repo-local wiki and log evidence for the pending-pet visibility bug:
  - `docs/wiki/petstore-catalog-availability.md`
  - `docs/logs/pending-pet-visible.ndjson`
- Updated the build automation prompt, story skill, OpenSpec-style templates, simulation fixture, and walkthrough so sparse incoming work looks like a bug/regression rather than a new feature.
