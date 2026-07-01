# Enterprise Memory And Cost Demo

## One-Sentence Story

OpenHands reduces repeated SDLC and infrastructure automation cost by loading existing memory first, routing discovery to cheaper agents, and reserving stronger models for code edits and risk decisions.

## Live Demo Path

1. Open a sparse GitHub issue, for example:

```text
Filter pets by max adoption fee
```

2. Add `openhands-context` first for the scout pass.

What to show:

- `AGENTS.md` durable repo rules
- `skills/sdlc-context-reuse/SKILL.md` procedural memory
- `docs/repo-memory/petstore-intelligence.md` durable app map
- `docs/repo-memory/previous-agent-runs.md` prior OpenHands run memory
- generated `docs/context-reuse/latest-context-reuse-report.md`

3. Add `openhands-build` when ready to show the existing build work cell using the same memory path before implementation.

4. On the resulting PR, add `openhands-review` and `openhands-qa` to show reuse across separate agents/work cells.

## Live Trigger Mechanics

The context scout is triggered by a GitHub issue label, not GitHub Actions and not a comment command.

1. Create or reopen an issue in `rajshah4/sdlc-automation-github-demo`.
2. Add the `openhands-context` label.
3. The GitHub integration sends an `issues.labeled` event to OpenHands.
4. The automation filter matches only issues in the configured repo where `label.name == 'openhands-context'`.
5. The automation clones the configured repo/ref, loads `AGENTS.md`, `skills/`, `docs/repo-memory/`, and deterministic scripts, then posts a concise issue comment.

To rerun the same issue, remove `openhands-context`, remove any terminal status label such as `openhands:done`, and add `openhands-context` again. For the cleanest live demo, create a fresh sparse issue and apply the label once.

## What Is Stored Vs Pulled

- Stored in OpenHands automation: trigger, filter, model profile, timeout, and prompt text.
- Pulled from GitHub on each run: `AGENTS.md`, repo-local skills, repo memory docs, scripts, fixtures, and app code from the configured ref.
- Local only: operator notes, raw validation breadcrumbs, run IDs, and environment-specific proof.

## Presenter Language

Use this framing:

```text
The first agent is not trying to solve the whole task. It is a low-cost scout.
It loads durable memory, searches narrowly, summarizes prior logs and prior
agent runs, and hands a compact report to the coding or review agent.
```

Then connect it to Terraform:

```text
For Terraform, this is how you avoid paying every agent to rediscover the same
workspace topology, module ownership, Terraform Cloud plan quirks, and previous
migration failures. Cheap agents classify and summarize; stronger agents edit
or reason through risky plans only after the context has been narrowed.
```

## Local Rehearsal

```bash
python3 scripts/build_context_reuse_report.py \
  --fixture tests/fixtures/github_issue_labeled_context.json \
  --stdout

python3 scripts/simulate_github_event.py \
  --fixture tests/fixtures/github_issue_labeled_context.json

python3 scripts/preflight_github_demo.py --offline
```

## Live Validation Checklist

For a customer-facing live run, keep environment-specific proof in local notes and show only the polished artifacts in GitHub:

- The OpenHands automation is registered from `automations/github/openhands-context/`.
- The automation clones the branch that contains `AGENTS.md`, `skills/sdlc-context-reuse/`, `docs/repo-memory/`, and `scripts/build_context_reuse_report.py`.
- The scout automation uses a lower-cost model profile when available.
- The runtime has a `GITHUB_TOKEN` secret with permission to comment on issues.
- Applying `openhands-context` to a sparse issue creates a context report and posts a concise issue comment.

## What This Proves

- Agents can use `AGENTS.md` as durable memory.
- Skills externalize procedure so prompts stay smaller.
- Existing logs and QA reports become operational memory.
- GitHub repo search narrows the file set before code work.
- Previous OpenHands runs become episodic memory.
- Lower-cost models can perform scout/summarization work before stronger models are invoked.
