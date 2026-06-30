# Tested Demo Flow

Last updated: 2026-06-30 UTC.

## Local Validation

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
python3 skills/sdlc-story/scripts/validate_open_spec.py skills/sdlc-story/references/openspec-change-template
python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
NODE_PATH=/path/to/node_modules PLAYWRIGHT_BROWSER_CHANNEL=chrome python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/run_playwright_ui_demo.py --url http://localhost:4173 --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search
```

The build fixture now represents the bug-first demo path: a sparse issue reports that customers are seeing pets that are not available, with `PENDING_PET_VISIBLE` as the log clue.

## Historical Successful Build Result

Repository:

- `https://github.com/rajshah4/sdlc-automation-github-demo`

Issue:

- `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1`

Result:

- Rajistics OpenHands automation run `f84671ac-33b7-43d8-a0e4-3532fb180263` completed at `2026-06-23T02:29:45Z`.
- Rajistics OpenHands conversation: `https://app.replicated.rajistics.com/conversations/060aa6399eae4e77b2fcd630646fbe56`
- OpenHands posted the result comment: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4775062401`
- OpenHands opened PR #2: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/2`
- Issue #1 now has `openhands:done`.

Note: this successful build result used the earlier max-adoption-fee feature story before the demo assets were pivoted to bug-first examples. The active automation set is label-only and should use the current bug fixture for new dry runs.

## Registered OpenHands Automations

Prompt-preset automations are registered with the Rajistics Enterprise Org API key. The current Jira demo path uses the Rajistics instance, not app.all-hands Cloud:

| Work cell | Automation ID | Model profile | Trigger |
| --- | --- | --- | --- |
| `jira-to-story` | `a22f4cfd-d194-4566-b773-89fc903fd9d6` | `Bedrock-Claude-Sonnet-4-5-fast` | `jira:issue_created` from `jira-direct` |
| `jira-to-story-sidekick-v2` | `3ed7bd14-e35a-4fb4-b111-2efc0c739f1d` | `Bedrock-Claude-Sonnet-4-5-fast` | `jira:issue_created` from `jira-direct`, label `sidekick-v2` |
| `openhands-build` | `1d97b79d-7bb6-4b67-969d-7f0182c416a5` | `Bedrock-Claude-Sonnet-4-5` | `issues.labeled` |
| `openhands-incident` | `bbff1a54-fe12-43fd-85b6-b1add7f6ca84` | `Bedrock-Claude-Sonnet-4-5` | `issues.labeled` |
| `openhands-qa` | `b3192e16-171a-4ec3-8028-9514a7f372fe` | `Bedrock-Claude-Sonnet-4-5-fast` | `pull_request.labeled`, `issues.labeled` |
| `openhands-review` | `912cfa7e-2390-4a5c-bd27-5f6d75861030` | `Bedrock-Claude-Haiku-4-5` | `pull_request.labeled` |

Run-list check:

```bash
python3 scripts/list_openhands_automation_runs.py \
  --env-file /path/to/local/.env \
  --automation-id a22f4cfd-d194-4566-b773-89fc903fd9d6 \
  --limit 5
```

The Jira automation opens or updates a draft PR and adds `openhands-qa`. That label intentionally starts a second QA conversation. Humans still approve review, merge, deployment, and production-facing changes.

For the visible multi-agent customer demo, create the Jira Task with label
`sidekick-v2`. The normal Jira automation excludes that label and the
sidekick-v2 automation starts visible docs/logs/repo scout conversations before
the main implementation conversation.

The Rajistics API was checked after registration and returned the active set as enabled. The Jira custom webhook source is `jira-direct`.

Enterprise Org Jira webhook source:

- Webhook ID: `27073b98-289c-440f-bcc4-7de63f8c31fc`
- Webhook URL: `https://app.replicated.rajistics.com/api/automation/v1/events/b35383f5-00e0-4f4d-99c5-df8943fa2355/jira-direct`
- Event key expression: `webhookEvent`
- Signature header: `X-Hub-Signature`

Stage-specific model profiles are tracked in the automation JSON files with the
`model` field. In the Rajistics automation API, `model` means the saved model
profile name for automation runs.

## Current Jira-To-QA Validation

The latest confirmed end-to-end path before the Enterprise Org migration is KAN-25:

- Jira automation run `811b03a5-6ff9-4aab-ad98-368ebfb8bdd6` completed on 2026-06-29.
- Jira/story conversation: `https://app.replicated.rajistics.com/conversations/210a1ebe-94e8-400b-8116-3f7aff802cd5`
- Draft PR: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/36`
- QA automation run `dd0aa558-92b3-4e56-a129-da06d78c928b` completed on 2026-06-29.
- QA conversation: `https://app.replicated.rajistics.com/conversations/35e8ad56-91ea-4fd0-a4ce-ebfab3c4dde9`
- QA PR comment: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/36#issuecomment-4836846019`

The PR is intentionally still human-reviewed. The QA conversation pushed a QA report and commented with PASS evidence, but it did not approve or merge.

## Enterprise Org Live Smoke: 2026-06-29

KAN-26 confirmed the Enterprise Org Jira automation and Jira-to-PR work cell when
the Rajistics `jira-direct` event endpoint received a correctly signed Jira-shaped
event:

- Jira issue: `https://rajiv-shah.atlassian.net/browse/KAN-26`
- Enterprise Org Jira run: `c499dcc1-8545-4e68-97cd-6b7a5a493318`
- Jira/story conversation: `https://app.replicated.rajistics.com/conversations/0bf7ca7b530449d0b37000de5a937b3c`
- Draft PR: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/37`
- Result: PR opened, regression tests added, OpenSpec-style artifacts added, `openhands-qa` label added, and Jira commented.

KAN-27 tested a fresh live Jira issue-created webhook after the Enterprise Org URL
was configured in Jira:

- Jira issue: `https://rajiv-shah.atlassian.net/browse/KAN-27`
- Poll result: no new Enterprise Org Jira automation run appeared after 18 polls
  over roughly three minutes.
- Interpretation: the Rajistics Enterprise Org `jira-direct` source and automation
  match correctly when an event arrives, but the Jira admin webhook delivery still
  needs to be checked in Jira webhook history/configuration.

The QA handoff for PR #37 did run automatically, but it was handled by the older
personal-scope Rajistics QA automation, not the new Enterprise Org QA automation:

- Personal QA automation: `dfd2bfe1-72f9-4ad2-8548-6b2aad64a037`
- Personal QA run: `ffa67162-d16d-4567-ba93-127e4295f14d`
- QA conversation: `https://app.replicated.rajistics.com/conversations/2b1b5b07-b75e-478c-a544-8715a57d2349`
- QA comment: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/37#issuecomment-4837839892`

The new Enterprise Org QA automation was manually dispatched as a smoke test:

- Enterprise QA run: `abab8704-3f59-4207-a74c-852f79ef2383`
- Enterprise QA conversation: `https://app.replicated.rajistics.com/conversations/c6f640ca-e815-4072-8c57-cfe512bfb504`
- Result: the automation launched on `Bedrock-Qwen3-Coder-30B` and completed, but
  the automatic GitHub label event still appears to be routed to the personal scope.

KAN-28 confirmed the live Jira admin webhook after the Enterprise Org URL and
signing secret were updated in Jira:

- Jira issue: `https://rajiv-shah.atlassian.net/browse/KAN-28`
- Enterprise Org Jira run: `b0ce5754-a388-4c1a-967f-8aaf41b8461a`
- Jira/story conversation: `https://app.replicated.rajistics.com/conversations/37175c6c-0445-4729-bdd4-519842f855b3`
- Draft PR: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/38`
- Result: PR opened, regression tests added, OpenSpec-style artifacts added, `openhands-qa` label added, and Jira commented.

The first `openhands-qa` label on PR #38 still routed to the older personal-scope
QA automation. The older personal-scope demo automations were then disabled:

- Jira: `1ae30b64-85ba-4713-bd39-b82892dcdc9a`
- Build: `c0e77dc6-af1b-48eb-bb88-6673093a8ea5`
- Incident: `fc5bd894-3571-4375-b27f-4719061bb45a`
- QA: `dfd2bfe1-72f9-4ad2-8548-6b2aad64a037`
- Review: `50c7b188-a2f8-4ac7-bc27-85cd3cb2cc0c`

After the GitHub event routing fix, the Enterprise Org QA automation received a
live `openhands-qa` label event:

- Enterprise QA automation: `b3192e16-171a-4ec3-8028-9514a7f372fe`
- Enterprise QA run: `c96832d5-f706-4989-97be-8a9efaf9370c`
- QA conversation: `https://app.replicated.rajistics.com/conversations/c3d75104-9f1f-44d5-8fd6-08d388a99d98`
- Result: run completed successfully on 2026-06-30 UTC. The PR already had a QA
  report from the older run, so the validation evidence should be checked in the
  Enterprise conversation as well as the PR comment history.

At this point, both delivery paths are proven separately: live Jira issue-created
events reach Enterprise `jira-to-story`, and live GitHub label events reach
Enterprise `openhands-qa`.

## Sidekick Context Experiment

The sidekick experiment lives on branch `sidekick-context-experiment`.

- Read-only sidekick skill: `skills/sdlc-context-sidekick/`
- Single-agent control package: `automations/jira/jira-to-story-control/`
- Sidekick-assisted package: `automations/jira/jira-to-story-sidekick/`
- Visible child-conversation package:
  `automations/jira/jira-to-story-sidekick-v2/`
- Experiment plan: `docs/experiments/sidekick-context-experiment.md`
- Comparison helper: `scripts/compare_sidekick_experiment.py`

The experiment packages are label-gated with `control-experiment` and
`sidekick-experiment` so the normal Jira demo can stay separate.

First live A/B result on 2026-06-30 UTC:

- Control: Jira `KAN-29`, run `09bf9e2a-26a7-4b9f-a1ec-0d59cd30cb55`, conversation
  `https://app.replicated.rajistics.com/conversations/2bfaf1bb-2ce7-4fa9-8b6a-14bad473f807`,
  PR `https://github.com/rajshah4/sdlc-automation-github-demo/pull/39`, time to PR
  4.88 minutes, run completion 6.26 minutes.
- Sidekick: Jira `KAN-30`, run `cbaa0fc7-a671-4676-be23-3294e01c888d`, conversation
  `https://app.replicated.rajistics.com/conversations/9b361dd2-f2ac-4f24-afdb-b48b2d5f8b10`,
  PR `https://github.com/rajshah4/sdlc-automation-github-demo/pull/40`, time to PR
  6.19 minutes, run completion 7.84 minutes.
- Interpretation: sidekick assistance improves the architecture story and evidence
  readability, but the first run missed the five-minute target. Keep the
  single-agent Jira-to-PR path for the main live demo.

Visible Sidekick V2 live result on 2026-06-30 UTC:

- Jira: `https://rajiv-shah.atlassian.net/browse/KAN-41`
- Sidekick-v2 automation run:
  `0b60432b-5065-445c-b731-d494af8f60c7`
- Launcher automation conversation:
  `https://app.replicated.rajistics.com/conversations/34bfd883-8520-4276-9891-87ab9c679bf8`
- Parent sidekick conversation:
  `https://app.replicated.rajistics.com/conversations/4a96f19d97354f2f9acaf12f82341a1c`
- Scout conversations:
  `logs-scout` `https://app.replicated.rajistics.com/conversations/0b1436fec56a4411b011477d57c537ad`,
  `docs-scout` `https://app.replicated.rajistics.com/conversations/5813c3c4970f4c4f9d62264791e43022`,
  `repo-scout` `https://app.replicated.rajistics.com/conversations/897a9a5c6cb14765982d381fa4a7551d`
- Main implementation conversation:
  `https://app.replicated.rajistics.com/conversations/f5f758a453a247cb9146f088d61548d0`
- PR:
  `https://github.com/rajshah4/sdlc-automation-github-demo/pull/48`
- QA run:
  `361bb50f-1f5b-47ca-b442-b842448eff84`
- QA conversation:
  `https://app.replicated.rajistics.com/conversations/3fa9264a-fab9-4381-a37a-fc5e0f7bee1a`
- QA comment:
  `https://github.com/rajshah4/sdlc-automation-github-demo/pull/48#issuecomment-4839894899`

Timing: Jira automation run to PR opened was about 7.3 minutes. The visible
sidekick tree to PR opened was about 5.4 minutes. The main implementation child
to PR opened was about 4.5 minutes. QA label to QA comment was about 4.0
minutes. This proves the customer-visible architecture, but the prompt-preset
launcher still adds enough overhead that a strict five-minute Jira-to-PR demo
should use the normal path or a future deterministic custom launcher.

Follow-up sidekick-v2 checks on 2026-06-30 UTC:

- KAN-42 run `ce41b5b4-2d67-4874-99e1-411b274f9b13` failed after timeout with
  `Timed out: Sandbox not available` while sandbox grouping was
  `NO_GROUPING`. No PR was opened.
- The org setting `sandbox_grouping_strategy` was changed to
  `FEWEST_CONVERSATIONS`.
- KAN-43 run `e43e01c1-85ee-41f8-8627-2b82b3295612` then got a sandbox and
  completed quickly, but the old registered v2 prompt still called
  `--fetch-jira` and stopped because `JIRA_API_BASE_URL` was not available in
  the automation runtime.
- The v2 prompt was corrected to use the Jira webhook payload summary and
  description directly, avoiding the extra Jira API env dependency. The old v2
  automation `ca0ddf76-bafe-4c3e-803a-1612eaed74de` was disabled and the
  corrected v2 automation `3ed7bd14-e35a-4fb4-b111-2efc0c739f1d` is now the
  expected label-gated path.
- KAN-44 was created against the corrected v2 automation as run
  `5c5c528d-882e-400d-8cf2-57748443a6e1`, but by 05:22 UTC the automation runs
  endpoint was returning HTTP 503 `Service Unavailable` / `no available server`
  and no KAN-44 PR had appeared. Treat that as an automation service
  availability blocker, not a successful timing run.

## Playwright Status

PR #36 is mostly a backend/catalog-filter fix. It has user-visible impact, but it does not add a new UI control. The QA conversation therefore ran backend/API checks plus static UI validation.

The automation runtime did not have Playwright available, so QA correctly reported fallback evidence instead of claiming browser coverage. To show the full Playwright artifact path, use one of these options:

- Point to the prebuilt UI example in `docs/ui-playwright-example.md`, especially PR #6.
- Preinstall Playwright or expose BrowserToolSet in the Rajistics automation runtime before the demo.
- Run the checked-in Playwright example locally or in a prepared runtime with `NODE_PATH` pointing at an existing Playwright install.

Do not let the timed automation install Playwright live; the demo guidance is to use preinstalled browser tooling or report the gap clearly.

## Disabling The Old app.all-hands Path

For a clean Rajistics demo, disable the old app.all-hands Cloud Jira path without deleting it:

1. In Jira admin, open **System -> Webhooks**.
2. Disable the webhook or rule named like `OpenHands Cloud Integration`.
3. Leave `OpenHands KAN Task Created` enabled because it points at Rajistics `jira-direct`.
4. To reverse, re-enable the Cloud webhook or rule.

If the Cloud path is an OpenHands automation instead of a Jira webhook, toggle that automation's `enabled` setting off in app.all-hands and toggle it back on after the demo. Do not delete secrets or credentials for a temporary pause.

## Not Tested Live

- SRE incident remediation was not run; cloud mutation remains report-only unless `scripts/petstore_gcp_observe.py` reports `diagnosis.safe_to_remediate=true`.
- Review automation was not part of the latest Jira-to-QA pass.
