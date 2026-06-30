---
name: sdlc-context-sidekick
description: Read-only context scout for sparse Jira-to-PR demo tickets. Use before the SDLC story skill when Codex needs to find likely docs, logs, repo files, missing context, and confidence without editing code, opening PRs, or mutating Jira/GitHub.
---

# SDLC Context Sidekick

Use this skill as a bounded scout before `skills/sdlc-story/SKILL.md`.

The sidekick's job is to make the hard part of the demo visible: a sparse,
business-language Jira ticket becomes a small context brief that names the docs,
logs, likely files, confidence, and missing information.

## Hard Boundaries

- Read only. Do not edit files.
- Do not create branches, commits, PRs, Jira comments, GitHub comments, labels, or status changes.
- Do not read or print secrets, `.env` values, credentials, tokens, or private keys.
- Search only the minimum repo context needed for the ticket:
  `README.md`, `AGENTS.md`, `docs/wiki/`, `docs/logs/`, `app/`,
  `tests/`, and `openspec/project.md`.
- Do not load workflow skills such as `skills/sdlc-story/SKILL.md`,
  `skills/sdlc-qa/SKILL.md`, or implementation references. The main agent owns
  those after the context brief exists.
- Prefer deterministic search before broad reasoning.
- Stop with `NEEDS_HUMAN` when the ticket cannot be mapped to a repo area with at least medium confidence.

## Scout Roles

For the visible sidekick demo, make launches easy to identify by splitting context
search into three bounded lanes:

| Scout | Roots | Job | Budget |
| --- | --- | --- | --- |
| `docs-scout` | `README.md`, `AGENTS.md`, `docs/wiki/`, `openspec/project.md` | Find product wording, architecture hints, and acceptance clues. | At most four matching files. |
| `logs-scout` | `docs/logs/` | Find symptom evidence, error codes, and request traces. | At most four matching files. |
| `repo-scout` | `app/`, `tests/` | Find likely implementation and test files. | At most four matching files. |

Each scout is read-only and should return only file paths, short evidence
snippets, confidence, and missing information. Scouts should not sit idle waiting
for other scouts; launch them together when using an orchestration script or
custom automation runner.

## Workflow

1. Capture the Jira key, URL, summary, description, labels, and comments when available.
2. Run the fan-out helper for the lowest-cost baseline:

   ```bash
   python3 skills/sdlc-context-sidekick/scripts/fanout_context_scouts.py \
     --jira-key KAN-123 \
     --title "Sparse ticket summary" \
     --body-file /path/to/body.txt
   ```

   This prints `CONTEXT_SCOUT_FANOUT` plus the aggregate `CONTEXT_BRIEF`.

3. If the fan-out helper is unavailable, run the single-brief helper:

   ```bash
   python3 skills/sdlc-context-sidekick/scripts/build_context_brief.py \
     --jira-key KAN-123 \
     --title "Sparse ticket summary" \
     --body-file /path/to/body.txt
   ```

   If no body file exists, pass the description on stdin or omit it.

4. If the helper finds weak evidence, use at most two additional `rg`, `sed`, or
   `find` reads per scout within the allowed paths.
5. Return the brief in the format from `references/brief-format.md`.
6. Hand the brief to the main story workflow. The main workflow owns edits, tests, PRs, Jira comments, and human gates.

## Confidence Rules

- `high`: ticket, wiki/docs, logs, and likely code/test files all point to the same fix area.
- `medium`: likely code/test files are clear, but docs or logs are partial.
- `low`: symptom is understood but repo area, evidence, or acceptance criteria are unclear.
- `NEEDS_HUMAN`: multiple plausible repos/files, missing product decision, missing logs/docs that the ticket depends on, or any request involving secrets, auth, data migration, deployment, or production mutation.

## Output Contract

The brief must be compact enough for a customer to read in a conversation log.
Use concrete paths and short evidence snippets. Do not include implementation
diffs or patch plans beyond likely file targets.

Required sections:

- `CONTEXT_BRIEF`
- `LIKELY_REPO_AREA`
- `DOCS_CHECKED`
- `LOGS_CHECKED`
- `LIKELY_FILES`
- `MISSING_INFO`
- `CONFIDENCE`
- `RECOMMENDED_NEXT_STEP`

For the Petstore demo, `Customers are seeing pets that are not available` should
usually map to catalog availability, `docs/wiki/petstore-catalog-availability.md`,
`docs/logs/pending-pet-visible.ndjson`, `app/petstore_app/catalog.py`, and
`app/tests/test_pet_catalog.py`.
