# Jira OpenHands Automation

This folder contains the Jira-triggered automation package for the SDLC Automation Demo.

The Jira webhook should send `jira:issue_created` events from the `KAN` project into the Rajistics custom webhook source named `jira-direct`.

## Work Cell

| Work cell | Jira trigger | Human boundary |
| --- | --- | --- |
| `jira-to-story` | KAN Task created | OpenHands opens or updates a PR; humans review and merge |

## Registration Notes

The visible automation prompt should stay short. Jira-specific implementation details, OpenSpec-style artifacts, evidence waypoints, and handoff behavior live in `skills/sdlc-story/`.

Use the existing Rajistics webhook source:

- Source: `jira-direct`
- Event: `jira:issue_created`
- Filter: `issue.fields.project.key == 'KAN' && issue.fields.issuetype.name == 'Task'`

Do not include repo names, file paths, log codes, or implementation clues in demo Jira tickets.
