# Setup Checklist

Use this checklist to configure the GitHub-native SDLC Automation Demo. Do not paste secret values into this file.

## GitHub

- Repository created for this demo.
- Self-hosted OpenHands GitHub App from the Rajistics Replicated instance is installed on the demo repo.
- If the repo was created after the app was first installed, refresh the GitHub App installation and explicitly include this repo.
- Public OpenHands GitHub App is not also installed on the same repo.
- Labels from `.github/labels.json` are present.
- GitHub App permissions allow reading issues/PRs, posting comments, creating branches, creating PRs, reading checks, and updating labels.
## OpenHands / Rajistics

- `OPENHANDS_HOST_GITHUB` points at the self-hosted app URL, usually `https://app.<base_domain>`.
- `OPENHANDS_API_KEY_ORG` is available locally for registration and verification. GitHub- or Rajistics-specific keys are accepted fallbacks, but the demo scripts prefer the org-scoped key when it is present.
- Before a live demo, run the non-mutating connection gate:
  `python3 scripts/preflight_live_connections.py --env-file /Users/rajiv.shah/Code/install_replicate/.env --mode main`
- Before the sidekick A/B timing demo, switch automation state intentionally and
  run: `python3 scripts/preflight_live_connections.py --env-file /Users/rajiv.shah/Code/install_replicate/.env --mode sidekick-experiment`
- Before the visible sidekick customer demo, keep the normal Jira automation and
  `sidekick-v2` automation enabled, then run:
  `python3 scripts/preflight_live_connections.py --env-file /Users/rajiv.shah/Code/install_replicate/.env --mode sidekick-v2`
  This mode now also checks `/api/v1/app-conversations/search`; the visible
  sidekick demo is not ready if that endpoint returns `BearerTokenError`, even
  when the automation list endpoint passes.
- The read-only preflight does not prove that `selected_repository` child
  conversations can start. If the sidekick launcher fails with `Git provider
  authentication issue when getting remote URL`, fix the Rajistics GitHub
  provider/app authorization before testing Haiku scout timing.
- Auth is split by API family. Automation endpoints under `/api/automation/v1`
  use `Authorization: Bearer <OPENHANDS_API_KEY_ORG>`. App-server endpoints
  under `/api/v1`, including app conversations and Git provider repo search, use
  `X-Access-Token: <OPENHANDS_API_KEY_ORG>`. Do not send both headers together;
  app auth may prioritize a stale `Authorization` header.
- For visible sidekick runs, keep `sandbox_grouping_strategy` at
  `FEWEST_CONVERSATIONS`; with `NO_GROUPING`, KAN-42 failed before useful work
  with `Timed out: Sandbox not available`.
- For timed customer demos, measure the Jira-to-PR path. QA only needs to kick
  off through the `openhands-qa` label and show a separate Enterprise QA
  run/conversation. Use `docs/ui-playwright-example.md` as the prebuilt UI and
  Playwright evidence path.
- For the Rajistics Replicated instance, verify the app URL, GitHub App slug, client ID, app ID, webhook secret, and private key are configured in the Replicated admin console.
- GitHub sign-in works in OpenHands.
- Repo search works in OpenHands.
- Adding the `openhands-build` label to a clean issue creates a conversation in the self-hosted instance.
- Automations are registered from `automations/github/*/automation.prompt-preset.json`.
- After moving to an org-scoped API key, verify GitHub label events create runs in
  the same org scope. After the latest refreshed install, the active Enterprise
  Org QA automation is `96b8ad90-bdb4-42ba-81f8-0cabf059bd6a`.
- The older personal-scope demo automations were disabled on 2026-06-29 so GitHub
  labels no longer take the old path. Keep the Enterprise Org automations enabled.
- After the GitHub event routing fix, PR #38's `openhands-qa` label reached the
  Enterprise Org QA automation as run `c96832d5-f706-4989-97be-8a9efaf9370c`.
- Jira demo automation is defined in `automations/jira/jira-to-story/`; it uses the `jira-direct` webhook source and keeps implementation details in `skills/sdlc-story/`.
- The sidekick A/B experiment is isolated on branch `sidekick-context-experiment`
  with label-gated Jira packages under `automations/jira/jira-to-story-control/`
  and `automations/jira/jira-to-story-sidekick/`.
- The visible sidekick V2 customer path is label-gated under
  `automations/jira/jira-to-story-sidekick-v2/`. Add Jira label `sidekick-v2`
  when you want separate docs/logs/repo scout conversations before the main
  Jira-to-PR implementation conversation.
- Story-to-PR artifacts follow Fission-AI/OpenSpec lineage, with change folders under `openspec/changes/`.
- The live automation does not install or run the OpenSpec CLI during the timed label-triggered flow; use preinstalled CLI setup/archive commands outside the demo run when needed.
- Only one OpenHands GitHub App should respond on this repo; duplicate public/self-hosted installs can create confusing duplicate runs.
- The four repo-local skills are loaded from `skills/`, not from a hidden `.agents` directory:
  - `skills/sdlc-story`
  - `skills/sdlc-qa`
  - `skills/sdlc-incident`
  - `skills/sdlc-code-review`

## Jira

- Jira admin webhook points to the Rajistics `jira-direct` webhook URL.
  - Enterprise Org URL: `https://app.replicated.rajistics.com/api/automation/v1/events/9a0d7385-6478-45d5-9764-122d1b980341/jira-direct`
- Jira webhook secret matches the Rajistics `jira-direct` signing secret.
- The Jira webhook signing secret is stored in the Rajistics automation webhook
  registration and in Jira's webhook configuration. It does not need to be
  duplicated as an OpenHands runtime secret unless a custom script explicitly
  reads `JIRA_WEBHOOK_SECRET`.
- Enterprise OpenHands runtime secrets still need the Jira API credentials the
  agent uses after it wakes up, such as `JIRA_API_TOKEN`, `JIRA_SERVICE_ACCOUNT_EMAIL`,
  `JIRA_SITE_URL`, and `JIRA_API_BASE_URL`.
- The visible sidekick-v2 launcher does not fetch Jira directly. It uses the
  Jira webhook payload key, summary, and description so it does not require
  `JIRA_API_BASE_URL` in the launcher runtime.
- Jira webhook sends issue-created events with body included.
- Jira webhook JQL is limited to `project = KAN AND issuetype = Task`.
- After updating the webhook URL, create a fresh `KAN` Task and confirm the
  Enterprise Org automation run list gains a new `jira-to-story` run. KAN-27 did
  not create a run after roughly three minutes of polling, so Jira webhook
  delivery history/configuration still needs review.
- Old app.all-hands Cloud Jira webhooks or Jira automation rules are disabled, not deleted, during the Rajistics demo.
- Demo Jira tickets are sparse business-language reports. Do not include repo names, file paths, log codes, or implementation clues in the ticket.
- Suggested labels for the normal path are `bug`, `jira-to-story-demo`, and
  `openhands-demo`; labels are for operator search, not the trigger boundary.
- For the visible sidekick customer demo, add `sidekick-v2` to the Jira Task.

## Slack

- Slack app is created and linked in OpenHands if Slack is shown.
- OpenHands UI `Install Slack` linking flow is complete.
- Store only secret names here:
  - `SLACK_WEBHOOK_URL`
  - `SLACK_BOT_TOKEN`
  - `SLACK_CHANNEL_ID`

## Google Cloud

- GCP project has Cloud Run and Cloud Logging evidence for the Petstore incident flow.
- OpenHands has read-only observability credentials.
- `DEMO_ADMIN_TOKEN` is available only when showing the bounded runtime remediation path.
- Store only secret/config names here:
  - `GCP_PROJECT`
  - `GCP_REGION`
  - `GCP_SERVICE`
  - `GCP_LOG_NAME`
  - `GOOGLE_APPLICATION_CREDENTIALS_JSON_B64`
  - `DEMO_ADMIN_TOKEN`

## Cost And Security

- Event-driven triggers avoid unnecessary LLM calls.
- `scripts/preflight_github_demo.py`, OpenSpec-style validation, label setup, and Petstore SRE observation scripts are deterministic and do not call an LLM.
- Desired LLM profiles are documented in the automation JSON files with the `model` field. In the Rajistics automation API, `model` means the saved model profile name for automation runs.
- Current Enterprise Org model split: Jira launcher, main implementation, and QA
  use `Bedrock-Claude-Sonnet-4-5-fast`; visible sidekick scouts use the concrete
  Haiku child-conversation model
  `litellm_proxy/us.anthropic.claude-haiku-4-5-20251001-v1:0`; build/incident
  use `Bedrock-Claude-Sonnet-4-5`; review uses `Bedrock-Claude-Haiku-4-5`.
- Secrets stay in OpenHands secret store or local `.env`.
- Humans approve PRs, reviews, merges, deployments, and production-facing fixes.
