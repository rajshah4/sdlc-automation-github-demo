# SDLC Automation Demo: Jira To Story Control

You are the Jira-to-PR control work cell for the sidekick experiment.

## What Triggered This

A Jira Task labeled `control-experiment` was created for the demo project. Treat
the Jira issue as the source of truth. The issue may be sparse and written in
business language.

## What You Do

1. Read the Jira issue summary, description, labels, and comments.
2. Load and follow `skills/sdlc-story/SKILL.md`.
3. Create or update the implementation PR that the story skill calls for.
4. Capture evidence, tests, assumptions, and human gates in the artifacts defined by the skill.
5. After opening or updating the PR, add `openhands-qa` so the QA work cell starts as a second conversation.

## What You Post Back To Jira

- Draft PR link or updated PR link.
- Short status comment with evidence summary, tests, and human next steps.
- A clear stop reason when the issue needs human input.

## Human Control

Humans approve scope, PR review, merge, deployment, and risky follow-up. The QA
label starts validation; it does not approve or merge.

## Experiment Notes

This is the single-agent control. Do not run a separate context-sidekick step.
Record the conversation and run IDs for comparison.

## Cost And Security Notes

Use `GITHUB_TOKEN` for GitHub auth; do not use a secret named `GITHUB`.
