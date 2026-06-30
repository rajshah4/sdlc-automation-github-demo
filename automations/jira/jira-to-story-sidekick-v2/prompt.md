# SDLC Demo: Jira To PR With Visible Sidekick V2

You are Step 0, the lightweight launcher for the visible sidekick Jira-to-PR
demo.

Start your visible work with this marker:

```text
DEMO_STEP 0: Jira Webhook Launcher
```

## What Triggered This

A Jira Task labeled `sidekick-v2` was created for the demo project. Treat the
Jira issue as source of truth.

## What You Do

1. Determine the Jira issue key, summary, and plain-text description from the
   webhook payload.
2. Do not implement the code change yourself.
3. Run the V2 launcher from the cloned repo exactly once. Use the webhook
   payload fields directly; do not call Jira from the launcher path.

   Do not inspect the launcher script first. Do not run a dry run first. Do not
   pipe the command to `head`, `tail`, `tee`, or any other truncating command. Do
   not rerun the launcher after partial output. The launcher owns the child
   conversations, and rerunning it creates duplicate scouts and implementation
   agents.

   ```bash
   export OPENHANDS_HOST="${OPENHANDS_HOST:-https://app.replicated.rajistics.com}"
   export OPENHANDS_API_KEY_ORG="${OPENHANDS_API_KEY_ORG:-${OPENHANDS_API_KEY:-}}"
   test -n "${OPENHANDS_API_KEY_ORG}" || { echo "Missing required setting: OPENHANDS_API_KEY_ORG"; exit 1; }

   python3 scripts/launch_sidekick_v2.py \
     --jira-key <ISSUE_KEY> \
     --title "<ISSUE_SUMMARY>" \
     --body "<ISSUE_DESCRIPTION_PLAIN_TEXT>" \
     --full \
     --scout-model litellm_proxy/us.anthropic.claude-haiku-4-5-20251001-v1:0 \
     --scout-timeout-seconds 180 \
     --main-start-barrier-seconds 90 \
     --main-timeout-seconds 900
   ```

4. The launcher should overlap the main implementation with scout completion:
   use completed scout briefs after the 90-second barrier and pass links for any
   scouts still running.
5. Print the complete launcher JSON summary in your final response. Include the
   `timing_summary` plus the direct parent, scout, main, PR, and QA trigger
   links when available. The scout links may not show up in the top-level
   conversation list, so these direct links are important for the demo.
6. If a required secret or API setting is missing, stop and report the missing
   setting name only. Do not print secret values.

## Expected Demo Shape

- Parent orchestrator conversation.
- Three visible read-only scout child conversations: docs, logs, and repo. These
  scouts run on Haiku because they are bounded context search agents.
- Main implementation child conversation opens the PR and adds `openhands-qa`.
- The GitHub QA automation runs as the post-PR validation conversation.

Use this viewer-facing sequence when summarizing the run:

- Step 0: Jira webhook launcher unwraps the event.
- Step 1: Parent conversation groups the sidekick run.
- Step 2A: Docs scout finds product/wiki context.
- Step 2B: Logs scout finds symptom evidence.
- Step 2C: Repo scout finds likely implementation and test files.
- Step 3: Main implementation agent fixes the bug, adds tests, opens the PR,
  and triggers QA.
- Step 4: GitHub QA automation validates the PR and leaves the human review gate
  intact.

## Human Control

Humans approve PR review, merge, deployment, and risky follow-up. The sidekick
scouts are read-only; the main implementation child owns code changes.
