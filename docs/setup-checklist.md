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
- `OPENHANDS_API_KEY_GITHUB` is available locally for registration and in the OpenHands secret store for automations. For the Rajistics instance, `OPENHANDS_API_KEY_RAJISTICS` is an accepted fallback when the GitHub-specific key is intentionally blank.
- For the Rajistics Replicated instance, verify the app URL, GitHub App slug, client ID, app ID, webhook secret, and private key are configured in the Replicated admin console.
- GitHub sign-in works in OpenHands.
- Repo search works in OpenHands.
- Adding the `openhands-build` label to a clean issue creates a conversation in the self-hosted instance.
- Automations are registered from `automations/github/*/automation.prompt-preset.json`.
- Jira demo automation is defined in `automations/jira/jira-to-story/`; it uses the `jira-direct` webhook source and keeps implementation details in `skills/sdlc-story/`.
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
- Jira webhook secret matches the Rajistics `jira-direct` signing secret.
- Jira webhook sends issue-created events with body included.
- Jira webhook JQL is limited to `project = KAN AND issuetype = Task`.
- Demo Jira tickets are sparse business-language reports. Do not include repo names, file paths, log codes, or implementation clues in the ticket.
- Suggested labels are `bug`, `jira-to-story-demo`, and `openhands-demo`; labels are for operator search, not the trigger boundary.

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
- Different LLM profiles can be mapped by stage: review, QA, build, incident, and critic.
- Secrets stay in OpenHands secret store or local `.env`.
- Humans approve PRs, reviews, merges, deployments, and production-facing fixes.
