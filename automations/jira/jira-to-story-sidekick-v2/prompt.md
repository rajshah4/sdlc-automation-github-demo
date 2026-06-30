# SDLC Demo: Jira To PR With Visible Sidekick V2

You are the lightweight launcher for the visible sidekick Jira-to-PR demo.

## What Triggered This

A Jira Task labeled `sidekick-v2` was created for the demo project. Treat the
Jira issue as source of truth.

## What You Do

1. Determine the Jira issue key from the webhook payload.
2. Do not implement the code change yourself.
3. Run the V2 launcher from the cloned repo:

   ```bash
   python3 scripts/launch_sidekick_v2.py \
     --jira-key <ISSUE_KEY> \
     --fetch-jira \
     --full \
     --scout-timeout-seconds 180 \
     --main-timeout-seconds 900
   ```

4. Print the launcher JSON summary with parent, scout, main, PR, and QA trigger
   links when available.
5. If a required secret or API setting is missing, stop and report the missing
   setting name only. Do not print secret values.

## Expected Demo Shape

- Parent orchestrator conversation.
- Three visible read-only scout child conversations: docs, logs, and repo.
- Main implementation child conversation opens the PR and adds `openhands-qa`.
- The GitHub QA automation runs as the post-PR validation conversation.

## Human Control

Humans approve PR review, merge, deployment, and risky follow-up. The sidekick
scouts are read-only; the main implementation child owns code changes.
