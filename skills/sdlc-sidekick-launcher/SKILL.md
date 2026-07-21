---
name: sdlc-sidekick-launcher
description: Launch the visible sidekick Jira-to-PR demo from a Jira webhook event. Use when an OpenHands automation receives a Jira issue labeled sidekick-v2 and needs to start the docs, logs, repo scout conversations plus the main implementation conversation without embedding launcher shell details in the automation prompt.
---

# SDLC Sidekick Launcher

## Overview

Use this skill only in the Step 0 Jira webhook launcher automation for the
visible sidekick demo. The launcher conversation should unwrap the Jira event,
start the sidekick orchestration, and print the resulting conversation index.

The launcher does not implement code changes. It starts read-only scouts and the
main Jira-to-PR implementation conversation through `scripts/sidekick/launch_sidekick_v2.py`.

## Start Marker

Begin the visible response with:

```text
DEMO_STEP 0: Jira Webhook Launcher
```

## Inputs

Use the Jira webhook payload as the source of truth:

- `ISSUE_KEY`: Jira issue key, such as `KAN-123`
- `ISSUE_SUMMARY`: Jira summary
- `ISSUE_DESCRIPTION_PLAIN_TEXT`: plain text Jira description, or an empty string
  when no description is present

Do not call Jira from Step 0 unless the payload is missing the issue key or
summary. Do not read or print secret values.

## Launcher Command

Run the launcher exactly once. Use one shell command, not a backslash-wrapped
multi-line command, so argument parsing is unambiguous:

```bash
OPENHANDS_API_KEY_ORG="${OPENHANDS_API_KEY_ORG:-${OPENHANDS_API_KEY:-}}" GITHUB_TOKEN="${GITHUB_TOKEN}" python3 scripts/sidekick/launch_sidekick_v2.py --jira-key "<ISSUE_KEY>" --title "<ISSUE_SUMMARY>" --body "<ISSUE_DESCRIPTION_PLAIN_TEXT>" --full
```

The script owns the default Rajistics host, scout model, main model, timeouts,
parallel scout launch, 90-second main-start barrier, GitHub token verification,
and final JSON summary. Runtime settings come from environment secrets. In fresh
sandboxes the launcher may wait up to two minutes for runtime-injected secrets
to become available before starting the side conversations.

The command intentionally references `OPENHANDS_API_KEY_ORG`,
`OPENHANDS_API_KEY`, and `GITHUB_TOKEN` so the runtime injects those secrets into
the Python process without printing them.

Run the terminal action with a timeout of at least 900 seconds. The launcher may
produce little or no output until the final JSON summary; that is expected. Do
not pipe the output to another command to make it look shorter.

Required runtime secrets/settings:

- OpenHands API key: `OPENHANDS_API_KEY_ORG` or another supported
  `OPENHANDS_API_KEY*` value
- GitHub runtime token: `GITHUB_TOKEN`

Use `GITHUB_TOKEN` for GitHub auth. Do not use `GITHUB` or `GH_TOKEN`; if auth
is missing or rejected, stop and report `GITHUB_TOKEN` is missing or invalid
without printing the value.

## Hard Rules

- Do not implement the code change yourself.
- Do not inspect the launcher script first.
- Do not run a dry run first.
- Do not pipe launcher output to `head`, `tail`, `tee`, or any truncating command.
- Do not rerun the launcher after partial output. Reruns create duplicate scout
  and implementation conversations.
- If a required setting is missing, print only the missing setting name and stop.
  Do not probe token lengths, environment inventories, or secret values.
- If the launcher command times out, stop and report that the launcher timeout
  was too short. Do not rerun it.

## Expected Demo Shape

The launcher creates top-level conversations:

- Step 0: Jira webhook launcher unwraps the event and prints the index.
- Step 2A: Docs scout finds product/wiki context.
- Step 2B: Logs scout finds symptom evidence.
- Step 2C: Repo scout finds likely implementation and test files.
- Step 3: Main implementation agent fixes the bug, adds tests, opens the PR,
  and adds `openhands-review`.
- Step 4: GitHub review automation posts findings and adds `openhands-qa`.
- Step 5: GitHub QA automation validates the PR and leaves the human merge gate
  intact.

The Step 0 response is the visible index for the demo. Make it easy for a viewer
to click into the scout and implementation conversations.

## Final Response

Print the complete launcher JSON summary. Include:

- `timing_summary`
- scout conversation links
- main implementation conversation link
- PR link when available in the main conversation summary
- review/QA trigger or label handoff status when available

Humans still approve PR review, merge, deployment, and risky follow-up.
