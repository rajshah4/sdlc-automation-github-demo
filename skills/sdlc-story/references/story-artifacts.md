# Story-To-PR Artifacts

Use this reference after loading `skills/sdlc-story/SKILL.md`.

## Sparse Ticket Rule

The source issue should read like a real business report, not an automation prompt.

Do not expect the ticket to include:

- repository names
- file paths
- log file paths
- error codes
- test names
- implementation instructions

If the issue is too ambiguous to identify a product behavior, stop and ask a human. If it maps to a known Petstore behavior, proceed by gathering evidence from docs, logs, code, and tests.

## Evidence Waypoints

Make the reasoning path visible in the conversation, PR body, and source issue comment:

- `Stop 1 - Ticket`: summarize the sparse issue and business-language clues.
- `Stop 2 - Wiki/Docs`: cite docs checked, especially `docs/wiki/`; say explicitly when no relevant docs exist.
- `Stop 3 - Logs`: cite log attachments or fixtures checked, especially `docs/logs/`; include discovered error codes only after finding them.
- `Stop 4 - Repo/Files`: name the repo and files that explain the bug and fix.
- `Stop 5 - Tests/PR`: summarize tests added or run, validation result, and the draft PR link.

## OpenSpec Artifacts

Create a change folder before editing code:

```text
openspec/changes/github-issue-<number>-<slug>/
openspec/changes/jira-<issue-key>-<slug>/
```

Required files:

- `proposal.md`
- `design.md`
- `tasks.md`
- `specs/<capability>/spec.md`

Use `references/open-spec-template.md` for headings and examples. Validate with:

```bash
python3 skills/sdlc-story/scripts/validate_open_spec.py <change-folder>
```

## PR Body Contract

The draft PR body must include:

- source issue link
- Jira issue URL or GitHub issue URL, depending on the trigger source
- OpenSpec change path
- assumptions and non-goals
- acceptance criteria or spec status
- evidence waypoints
- files changed
- tests run
- residual risks
- AI assistance disclosure
- note that humans approve review, merge, and deployment decisions

## Source Issue Comment Contract

Post a concise result comment to the source issue. For Jira-triggered work, post to Jira. For GitHub-triggered work, post to GitHub.

Include:

- draft PR link
- validation summary
- evidence waypoints
- any human questions or stop reason

Avoid:

- repeating the exact trigger text
- implementation walls of text
- secrets, tokens, or environment values
- retrigger phrases such as `@openhands`

## Handoff Contract

When a draft PR is ready:

- Add `openhands-review` when the repo supports the chained review automation. This starts a separate review conversation.
- Do not add `openhands-qa` from story-to-PR. The review work cell adds it only after posting its review result.
- A parent-child supervisor may suppress both labels when it explicitly owns downstream orchestration.
- Do not add labels that can cause loops or duplicate runs.
- If labels cannot be changed, mention the recommended next work cell in the PR or issue comment.
- Keep the human gate explicit: review and QA evidence inform humans, but humans still approve, merge, and deploy.

## Human-In-The-Loop Stop Conditions

Stop and ask for human input instead of guessing when the work requires:

- product decision
- schema migration
- auth or identity change
- new dependency
- environment change
- secret access
- production mutation
- broad refactor outside the issue scope
