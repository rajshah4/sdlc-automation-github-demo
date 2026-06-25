# Jira OpenHands Automations

This folder contains the Jira-native automation package set for the SDLC Automation Demo.

The preferred Jira demo uses the OpenHands Automations prompt preset API with a signed Jira admin webhook. Jira sends `jira:issue_created` events into the Rajistics OpenHands custom webhook source named `jira-direct`, and the prompt-preset automation starts for `KAN` Tasks.

The older Jira Automation comment path remains available as a fallback. In that path, Jira sends events to the Rajistics Jira shim, the shim forwards signed events into the custom OpenHands webhook source named `jira`, and the prompt-preset automation starts when Jira Automation sends a `comment_created` event for project `KAN`.

## Work Cells

| Work cell | Jira trigger | Human boundary |
| --- | --- | --- |
| `openhands-build-direct` | Jira admin webhook `jira:issue_created` for `KAN` Tasks | OpenHands opens or updates a PR; humans review and merge |
| `openhands-build` | fallback issue comment containing `@openhands` | OpenHands opens or updates a PR; humans review and merge |

## Runtime Configuration

Store these values in the Rajistics OpenHands secret store:

```text
JIRA_API_TOKEN
JIRA_API_BASE_URL
JIRA_SITE_URL
JIRA_AUTH_MODE
JIRA_SERVICE_ACCOUNT_EMAIL
```

For the current Rajistics demo, `JIRA_AUTH_MODE` is `bearer`, and Jira REST calls use:

```text
Authorization: Bearer $JIRA_API_TOKEN
```

The service-account API token works through the Atlassian API Gateway base URL in `JIRA_API_BASE_URL`, not through Basic auth against the Jira site URL.

## Registration

Dry-run:

```bash
python3 scripts/register_jira_automations.py --dry-run --project-key KAN --repo-url https://github.com/rajshah4/sdlc-automation-github-demo
```

Apply only after confirming the live automation target:

```bash
python3 scripts/register_jira_automations.py --apply
```

No secrets belong in this repo. Store OpenHands, Jira, GitHub, Teams, Slack, and GCP credentials in the OpenHands secret store or a local `.env` excluded by `.gitignore`.

## Direct Jira Admin Webhook

Configure a Jira admin webhook for:

```text
project = KAN AND issuetype = Task
```

Event:

```text
jira:issue_created
```

OpenHands custom webhook source:

```text
jira-direct
```

The direct demo ticket should be sparse business language, for example:

```text
Families need to find pets in their budget
```

The automation should use Jira details, wiki docs, logs, and repo-local context to infer the adoption-fee filtering requirement.

## Fallback Jira Automation Rule

Keep this path only as fallback:

1. Trigger: issue commented.
2. Condition: comment contains `@openhands`.
3. Action: send web request to `https://app.replicated.rajistics.com/jira-shim`.
4. Method: `POST`.
5. Headers:
   - `Content-Type: application/json`
   - `X-Jira-Shim-Token: <shim token>`
6. Body:

```json
{
  "webhookEvent": "comment_created",
  "source": "jira-automation",
  "site": "https://rajiv-shah.atlassian.net",
  "projectKey": "{{issue.project.key}}",
  "issueKey": "{{issue.key}}",
  "issueUrl": "{{issue.url}}",
  "trigger": "comment",
  "commentId": "{{comment.id}}"
}
```
