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
- Rebuilt the Rajistics Jira demo path after the instance reset:
  - Jira admin webhook sends KAN Task creation events to Rajistics custom source `jira-direct`.
  - Personal-org Jira automation `1ae30b64-85ba-4713-bd39-b82892dcdc9a` turned sparse Jira bugs into draft PRs before the Enterprise Org migration.
  - Personal-org QA automation `dfd2bfe1-72f9-4ad2-8548-6b2aad64a037` ran when `openhands-qa` was added to a PR before the Enterprise Org migration.
- Updated the Jira story prompt and `sdlc-story` skill so the first Jira conversation adds `openhands-qa` after opening or updating the PR. This intentionally spawns a second QA conversation while preserving human PR review and merge approval.
- Validated the end-to-end Jira-to-QA handoff with KAN-25:
  - Jira/story run `811b03a5-6ff9-4aab-ad98-368ebfb8bdd6`
  - Jira/story conversation `https://app.replicated.rajistics.com/conversations/210a1ebe-94e8-400b-8116-3f7aff802cd5`
  - PR #36 `https://github.com/rajshah4/sdlc-automation-github-demo/pull/36`
  - QA run `dd0aa558-92b3-4e56-a129-da06d78c928b`
  - QA conversation `https://app.replicated.rajistics.com/conversations/35e8ad56-91ea-4fd0-a4ce-ebfab3c4dde9`
- Confirmed PR #36 did not produce Playwright browser artifacts because the automation runtime did not have Playwright available. QA correctly used backend/API checks and static UI validation, and reported the browser-tooling gap instead of claiming full browser coverage.
- Added `docs/ui-playwright-example.md` as the stable pointer for showing the older UI/Playwright PR while keeping the live Jira demo on the reliable non-UI bug path.
- Migrated the demo registration to Rajistics `Enterprise Org` using `OPENHANDS_API_KEY_ORG`:
  - Recreated Jira custom webhook source `jira-direct` as `27073b98-289c-440f-bcc4-7de63f8c31fc`.
  - New Jira webhook URL is `https://app.replicated.rajistics.com/api/automation/v1/events/b35383f5-00e0-4f4d-99c5-df8943fa2355/jira-direct`.
  - Registered Jira automation `a22f4cfd-d194-4566-b773-89fc903fd9d6` on `Bedrock-Claude-Sonnet-4-5`.
  - Registered build automation `1d97b79d-7bb6-4b67-969d-7f0182c416a5` on `Bedrock-Claude-Sonnet-4-5`.
  - Registered QA automation `b3192e16-171a-4ec3-8028-9514a7f372fe` on `Bedrock-Qwen3-Coder-30B`.
  - Registered review automation `912cfa7e-2390-4a5c-bd27-5f6d75861030` on `Bedrock-Claude-Haiku-4-5`.
  - Registered incident automation `bbff1a54-fe12-43fd-85b6-b1add7f6ca84` on `Bedrock-Claude-Sonnet-4-5`.
- Ran an Enterprise Org live smoke after the migration:
  - Created KAN-26 and triggered the Enterprise Org Jira automation with a correctly signed Rajistics `jira-direct` event after live Jira delivery did not appear.
  - Enterprise Jira run `c499dcc1-8545-4e68-97cd-6b7a5a493318` completed and opened PR #37: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/37`.
  - The Jira/story conversation was `https://app.replicated.rajistics.com/conversations/0bf7ca7b530449d0b37000de5a937b3c`.
  - Created KAN-27 as a fresh Jira issue-created webhook smoke; no new Enterprise Org Jira run appeared after roughly three minutes of polling.
  - Automatic QA for PR #37 was handled by the older personal-scope QA automation `dfd2bfe1-72f9-4ad2-8548-6b2aad64a037`, run `ffa67162-d16d-4567-ba93-127e4295f14d`, conversation `https://app.replicated.rajistics.com/conversations/2b1b5b07-b75e-478c-a544-8715a57d2349`.
  - Updated the Enterprise Org QA automation to accept both `pull_request.labeled` and `issues.labeled`, then manually dispatched it as run `abab8704-3f59-4207-a74c-852f79ef2383` to verify the `Bedrock-Qwen3-Coder-30B` work-cell path.
  - Remaining integration gaps: Jira admin webhook delivery to the Enterprise Org URL, and GitHub App/event routing from the personal automation scope to Enterprise Org automations.
- Re-tested after the Jira admin webhook URL and signing secret were updated:
  - Created KAN-28 from Jira and confirmed the Enterprise Org Jira automation run `b0ce5754-a388-4c1a-967f-8aaf41b8461a`.
  - Jira/story conversation `https://app.replicated.rajistics.com/conversations/37175c6c-0445-4729-bdd4-519842f855b3` opened PR #38: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/38`.
  - PR #38 received the `openhands-qa` label, but GitHub still routed the label event to the older personal-scope QA automation before it was disabled.
  - Disabled the older personal-scope demo automations: Jira `1ae30b64-85ba-4713-bd39-b82892dcdc9a`, build `c0e77dc6-af1b-48eb-bb88-6673093a8ea5`, incident `fc5bd894-3571-4375-b27f-4719061bb45a`, QA `dfd2bfe1-72f9-4ad2-8548-6b2aad64a037`, and review `50c7b188-a2f8-4ac7-bc27-85cd3cb2cc0c`.
  - Verified the Enterprise Org automations remain enabled with the intended model profiles.
- Confirmed the GitHub label routing fix:
  - Enterprise Org QA automation `b3192e16-171a-4ec3-8028-9514a7f372fe` received a live `openhands-qa` event.
  - Run `c96832d5-f706-4989-97be-8a9efaf9370c` completed with conversation `https://app.replicated.rajistics.com/conversations/c3d75104-9f1f-44d5-8fd6-08d388a99d98`.
- Created branch `sidekick-context-experiment` to test a context-sidekick architecture:
  - Added read-only skill `skills/sdlc-context-sidekick/`.
  - Added label-gated Jira experiment packages `jira-to-story-control` and `jira-to-story-sidekick`.
  - Added `docs/experiments/sidekick-context-experiment.md` and `scripts/compare_sidekick_experiment.py` to compare time to PR, token/model cost, success rate, and conversation readability.
