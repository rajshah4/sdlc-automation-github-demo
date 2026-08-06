# SDLC Automation Demo: Jira Request To PR

## What Triggered This

A new Jira request started this automation. The request may be brief and written
entirely in business language.

## What You Do

1. Understand the request, its context, and any acceptance criteria.
2. Follow the repository's SDLC story skill to turn the request into an
   OpenSpec-style proposal, design, task list, and test plan.
3. Implement the smallest safe change and create a draft pull request.
4. Record assumptions, evidence, and validation results in the pull request.
5. After the draft pull request is open, add the `openhands-review` label to it
   so the code-review work cell starts as a separate conversation. Do this label
   handoff before finishing so the next stage does not depend on conversation
   shutdown. Do not add `openhands-qa` or `openhands:done` here; those are owned
   by the review and QA work cells.

## Conversation Link

This automation's OpenHands conversation URL is appended to the end of this
prompt by the runtime. Include it in the pull-request description so reviewers
can trace the work back to the agent session that produced it. Add it as a
concise line near the end of the PR body:

`OpenHands conversation: <url>`

Copy the URL exactly as provided — do not write a shell variable or
placeholder. On self-hosted deployments the URL is injected by a custom
automation script; see `docs/automation-conversation-link-gap.md` for the
background and the workaround.

## What You Post Back To Jira

- A concise status update and link to the draft pull request.
- The validation performed and any assumptions that need confirmation.
- A clear question when a product or engineering decision requires human input.

## Human Control

People remain responsible for scope, pull-request review, merge, deployment, and
any risky follow-up. Automated QA validates the change; it never approves or
merges it.

## Operating Boundaries

Use the configured Jira and GitHub integrations and follow the repository-local
skills. Keep the workflow event-driven, protect credentials, and do not change
production resources, deployment settings, or branch protection.
