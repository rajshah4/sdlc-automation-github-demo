# Setup Checklist

Use this checklist to configure the GitHub-native SDLC Automation Demo. Do not
paste secret values into this file.

## GitHub

- Demo repository is available to the self-hosted OpenHands GitHub App.
- Public OpenHands GitHub App is not also installed on the same repo during the
  Rajistics demo.
- Labels from `.github/labels.json` are present.
- GitHub App permissions allow reading issues/PRs, posting comments, creating
  branches, creating PRs, reading checks, and updating labels.
- Enterprise runtime secret `GITHUB_TOKEN` is set and valid for the demo repo.
  The automations do not use a secret named `GITHUB`.

## OpenHands / Rajistics

- `OPENHANDS_HOST_GITHUB` points at the self-hosted app URL, usually
  `https://app.<base_domain>`.
- `OPENHANDS_API_KEY_ORG` is available locally for registration and verification.
  GitHub- or Rajistics-specific keys are accepted fallbacks, but the scripts
  prefer the org-scoped key when present.
- Model profiles referenced by the automation JSON files exist in Rajistics.
- Repo search works in OpenHands for the demo repo.
- Automations are registered from `automations/github/*/automation.prompt-preset.json`
  and `automations/jira/*/automation.prompt-preset.json`.
- If automation IDs differ from the defaults in
  `scripts/validation/preflight_live_connections.py`, set `JIRA_MAIN_AUTOMATION_ID`,
  `JIRA_SIDEKICK_V2_AUTOMATION_ID`, and `GITHUB_QA_AUTOMATION_ID` locally.
- Before the fast Jira-to-PR demo, run:

  ```bash
  python3 scripts/validation/preflight_live_connections.py \
    --env-file /path/to/local/.env \
    --mode main
  ```

- Before the visible sidekick demo, disable the normal Jira automation, enable
  `jira-to-story-sidekick-v2`, then run:

  ```bash
  python3 scripts/validation/preflight_live_connections.py \
    --env-file /path/to/local/.env \
    --mode sidekick-v2
  ```

- The `sidekick-v2` preflight also checks that the app-conversation API and
  GitHub provider repo search are available for visible scout conversations.
- Auth is split by API family:
  - `/api/automation/v1` uses `Authorization: Bearer <OPENHANDS_API_KEY_ORG>`.
  - `/api/v1` app-server endpoints use `X-Access-Token: <OPENHANDS_API_KEY_ORG>`.
- For visible sidekick runs, prefer `sandbox_grouping_strategy=FEWEST_CONVERSATIONS`
  so scout and implementation conversations can start promptly.

## Jira

- Jira admin webhook points to the Rajistics `jira-direct` webhook URL:

  ```text
  https://<openhands-host>/api/automation/v1/events/<org-id>/jira-direct
  ```

- Jira webhook secret matches the Rajistics `jira-direct` signing secret.
- Jira webhook sends issue-created events with body included.
- Jira webhook JQL is limited to the demo project and `Task` issue type.
- Enterprise OpenHands runtime secrets include the Jira API credentials the agent
  uses after it wakes up, such as `JIRA_API_TOKEN`,
  `JIRA_SERVICE_ACCOUNT_EMAIL`, `JIRA_SITE_URL`, and `JIRA_API_BASE_URL`.
- Demo Jira tickets are sparse business-language reports. Do not include repo
  names, file paths, log codes, or implementation clues in the ticket.
- For the fast path, create a normal Jira Task.
- For the visible sidekick path, add Jira label `sidekick-v2`.

## Demo Operation

- Fast path: `jira-to-story` takes a sparse Jira bug to a PR, adds tests, and
  applies `openhands-qa`.
- Visible sidekick path: `jira-to-story-sidekick-v2` starts separate docs, logs,
  and repo scout conversations before starting the main implementation
  conversation.
- QA is a handoff check, not a stopwatch metric. The useful demo signal is that
  the PR receives `openhands-qa`, starts the separate QA automation, and keeps
  human review in place.
- For UI/browser evidence, use `docs/ui-playwright-example.md` or a prepared
  runtime with Playwright/BrowserToolSet already available. Do not install
  Playwright during the timed Jira demo.
- Old or alternate Jira webhook paths can be temporarily disabled instead of
  deleted, then re-enabled after the demo.

## Repo Skills

Repo-local skills are loaded from `skills/`:

- `skills/sdlc-story`
- `skills/sdlc-context-sidekick`
- `skills/sdlc-sidekick-launcher`
- `skills/sdlc-qa`
- `skills/sdlc-code-review`

The automation prompts should stay short. Demo-specific knowledge, evidence
waypoints, tests, and human boundaries live in these skills and references.
