# Slack Integration

Slack is the human-facing notification layer for the SDLC automation.

## Recommended Channel

Create a dedicated channel such as:

```text
#openhands-petstore-sdlc
```

## What To Post

Post only concise operational updates:

- automation started
- automation needs human input
- automation completed with evidence
- Goal-Critic forced continuation
- incident triage report created

Do not post secrets, raw webhook payloads, full logs, or large test output.

## Message Types

| Type | When |
| --- | --- |
| `sdlc.run.started` | a work cell begins |
| `sdlc.run.needs_input` | automation is blocked or requires approval |
| `sdlc.run.completed` | work cell posts final evidence |
| `sdlc.goal_critic.continued` | critic verdict is incomplete and the agent continues |
| `sdlc.incident.triaged` | incident report or PR is ready |

## Required Secret

Use one of:

```text
SLACK_BOT_TOKEN
SLACK_CHANNEL_ID
```

or:

```text
SLACK_WEBHOOK_URL
```

For demos, an incoming webhook is usually enough.

## Example Message

```text
OpenHands SDLC Automation
Stage: QA
Petstore PR: <link>
Status: pass
Evidence: <PR comment link>
Goal-Critic: complete after 1 continuation
```
