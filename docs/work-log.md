# Work Log

## 2026-06-22

- Created a fresh GitHub-native SDLC Automation Demo repo instead of modifying the Azure DevOps demo in place.
- Copied safe Petstore app, tests, GitHub provider adapter, GCP helper scripts, and integration docs from the existing demo.
- Did not copy `.env`, `.git`, Azure automation tarballs, or secret-bearing material.
- Renamed runtime service references from the old internal service name to `sdlc-automation-petstore`.
- Added GitHub labels, issue templates, prompt-preset automation packages, setup docs, and deterministic preflight scripts.
- Added repo-local OpenHands skills under `skills/` so automation behavior is version controlled, easy to browse, and visible in the OpenHands UI.
- Created and pushed the private GitHub repo `rajshah4/sdlc-automation-github-demo` for safe GitHub-native validation.
- Created labels from `config/github-labels.json` and opened safe test issue #1.
- Validated the GitHub label path with the deterministic `OpenHands Label Demo` workflow. Two work-cell/status label events initially ran, which exposed an important retrigger risk before OpenHands automation registration.
- Fixed the GitHub Actions and OpenHands preset filters so only the four work-cell labels (`openhands-build`, `openhands-review`, `openhands-qa`, `openhands-incident`) trigger work. Status labels such as `openhands:ready` no longer retrigger automations.
- Re-tested the issue-comment path after the guard fix; run `27996297265` completed successfully and posted a single acknowledgement comment.
- Registered the four GitHub prompt-preset OpenHands automations against the configured OpenHands instance.
- Posted a post-registration `openhands-build` comment on issue #1. GitHub Actions run `27996464141` passed, but the OpenHands build automation run list remained empty. Next required setup is to install or refresh the self-hosted OpenHands GitHub App for this new private repo.
- Moved repo-local skills from the hidden agent folder to first-class `skills/` so customers and teammates can browse and reuse them directly.
- Disabled the earlier OpenHands automation registrations whose prompts referenced the hidden skill path.
- Registered fresh OpenHands automations whose prompts reference `skills/`:
  - build: `843a19a5-25c5-493e-b253-746678362dc8`
  - incident: `6875f016-92c6-4d71-bcb6-c65805f5e858`
  - QA: `6be9edc4-8ef1-4d5f-a5ad-4e26ff278a13`
  - review: `311d2a61-9eee-4d32-93a6-ee7c6f49c9a4`

## 2026-06-23

- Reworked the repo-local skills into four broad automation skills:
  - `sdlc-story`: sparse GitHub comment/issue to open specification to PR.
  - `sdlc-qa`: automated test-suite buildout and UI evidence.
  - `sdlc-incident`: SRE incident triage with Cloud Run/Cloud Logging evidence and bounded remediation.
  - `sdlc-code-review`: OpenHands `/codereview` with Petstore risk and supply-chain checks.
- Folded the earlier standalone GitHub/GCP helper skills into references and scripts under those four primary skills.
- Added OpenSpec template and validation tooling so the request-to-PR flow has a versioned specification artifact.
- Added QA references and a local server harness adapted from the automated QA demo pattern.
- Added SRE references and observation-summary tooling adapted from the Cloud Run incident demo pattern.
- Added code-review risk and supply-chain references based on the OpenHands code-review guidance.
- Updated OpenHands prompt-preset prompts to point at the four richer skill workflows.
- Disabled the previous prompt-preset registrations with the earlier lightweight prompts.
- Registered fresh OpenHands automations with the updated four-skill prompt wording:
  - build: `02ee14cd-d57d-44a5-a182-14a2bb46c22d`
  - incident: `c1af72a7-e625-43bf-907d-572452a3db05`
  - QA: `77343499-1f2e-4d10-bb04-9292f112046c`
  - review: `2cc7de0f-2d35-4024-866e-d1c6985c3d1d`
