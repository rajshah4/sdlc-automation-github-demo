# Jira OpenHands Automation

This folder contains the Jira-triggered automation packages for the SDLC Automation Demo.

The Jira webhook should send `jira:issue_created` events from the `KAN` project into the Rajistics custom webhook source named `jira-direct`.

## Work Cell

| Work cell | Jira trigger | Human boundary |
| --- | --- | --- |
| `jira-to-story` | KAN Task created | OpenHands opens or updates a PR; humans review and merge |
| `jira-to-story-sidekick-v2` | KAN Task created with `sidekick-v2` label | OpenHands starts visible read-only docs/logs/repo scout conversations, then the main implementation conversation. |

## Registration Notes

The visible automation prompts should stay short. Jira-specific implementation
details, OpenSpec-style artifacts, evidence waypoints, and handoff behavior live
in `skills/sdlc-story/`. The visible sidekick launcher contract lives in
`skills/sdlc-sidekick-launcher/`; context-scout output conventions live in
`skills/sdlc-context-sidekick/`.

Use the existing Rajistics webhook source:

- Source: `jira-direct`
- Event: `jira:issue_created`
- Filter: `issue.fields.project.key == 'KAN' && issue.fields.issuetype.name == 'Task'`

Do not include repo names, file paths, log codes, or implementation clues in demo Jira tickets.

For the visible sidekick demo, disable the normal `jira-to-story` automation and
enable `jira-to-story-sidekick-v2` so one Jira issue wakes only one work cell.
