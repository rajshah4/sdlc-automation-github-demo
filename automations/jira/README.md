# Jira OpenHands Automation

This folder contains the Jira-triggered automation packages for the SDLC Automation Demo.

The Jira webhook should send `jira:issue_created` events from the `KAN` project into the Rajistics custom webhook source named `jira-direct`.

## Work Cell

| Work cell | Jira trigger | Human boundary |
| --- | --- | --- |
| `jira-to-story` | KAN Task created | OpenHands opens or updates a PR; humans review and merge |
| `jira-to-story-control` | KAN Task created with `control-experiment` label | Single-agent control for the sidekick experiment. |
| `jira-to-story-sidekick` | KAN Task created with `sidekick-experiment` label | Runs the read-only context sidekick before the story skill. |

## Registration Notes

The visible automation prompt should stay short. Jira-specific implementation details, OpenSpec-style artifacts, evidence waypoints, and handoff behavior live in `skills/sdlc-story/`. Sidekick experiment context scouting lives in `skills/sdlc-context-sidekick/`.

Use the existing Rajistics webhook source:

- Source: `jira-direct`
- Event: `jira:issue_created`
- Filter: `issue.fields.project.key == 'KAN' && issue.fields.issuetype.name == 'Task'`

Do not include repo names, file paths, log codes, or implementation clues in demo Jira tickets.

For sidekick A/B tests, pause the normal `jira-to-story` automation or keep the
experiment labels out of normal tickets so one Jira issue wakes only one work
cell.
