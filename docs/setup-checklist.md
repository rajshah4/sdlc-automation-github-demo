# Setup Checklist

Use this checklist to configure the GitHub-native SDLC Automation Demo. Do not paste secret values into this file.

## GitHub

- Repository created for this demo.
- Self-hosted OpenHands GitHub App from the Rajistics Replicated instance is installed on the demo repo.
- Public OpenHands GitHub App is not also installed on the same repo.
- Labels from `config/github-labels.json` are present.
- GitHub App permissions allow reading issues/PRs, posting comments, creating branches, creating PRs, and updating labels.
- Optional GitHub Actions secrets are configured if you want to show the Actions path:
  - `OPENHANDS_API_KEY`
  - `OPENHANDS_HOST`

## OpenHands / Rajistics

- `OPENHANDS_HOST_GITHUB` points at the self-hosted app URL, usually `https://app.<base_domain>`.
- `OPENHANDS_API_KEY_GITHUB` is available locally for registration and in the OpenHands secret store for automations.
- GitHub sign-in works in OpenHands.
- Repo search works in OpenHands.
- A clean `@openhands` or `openhands-build` issue comment creates a conversation in the self-hosted instance.
- Automations are registered from `automations/github/*/automation.prompt-preset.json`.

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
- Store only secret/config names here:
  - `GCP_PROJECT`
  - `GCP_REGION`
  - `GCP_SERVICE`
  - `GCP_LOG_NAME`
  - `GOOGLE_APPLICATION_CREDENTIALS_JSON_B64`

## Cost And Security

- Event-driven triggers avoid unnecessary LLM calls.
- `scripts/preflight_github_demo.py` and label setup are deterministic and do not call an LLM.
- Different LLM profiles can be mapped by stage: review, QA, build, incident, and critic.
- Secrets stay in OpenHands secret store, GitHub Actions secrets, or local `.env`.
- Humans approve PRs, reviews, merges, deployments, and production-facing fixes.

