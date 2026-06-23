# Work Log

## 2026-06-22

- Created a fresh GitHub-native SDLC Automation Demo repo instead of modifying the Azure DevOps demo in place.
- Copied safe Petstore app, tests, GitHub provider adapter, GCP helper scripts, and integration docs from the existing demo.
- Did not copy `.env`, `.git`, Azure automation tarballs, or secret-bearing material.
- Renamed runtime service references from the old internal service name to `sdlc-automation-petstore`.
- Added GitHub labels, issue templates, prompt-preset automation packages, setup docs, and deterministic preflight scripts.
- Added repo-local OpenHands skills under `.agents/skills/` so automation behavior is version controlled and visible in the OpenHands UI.
- Created and pushed the private GitHub repo `rajshah4/sdlc-automation-github-demo` for safe GitHub-native validation.
