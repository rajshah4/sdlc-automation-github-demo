# Context Brief Format

Use this exact shape so sidekick-assisted runs are easy to compare with the
single-agent control.

When using split scouts, print this short fan-out header before the aggregate
brief:

```markdown
CONTEXT_SCOUT_FANOUT
Ticket: <Jira key or URL>
Summary: <one sentence>
Launch: docs-scout, logs-scout, and repo-scout started together
Total elapsed seconds: <number>

LAUNCHES
- docs-scout: <purpose>; read-only; no edits; no other skills
- logs-scout: <purpose>; read-only; no edits; no other skills
- repo-scout: <purpose>; read-only; no edits; no other skills

SCOUT_RESULT docs-scout
- purpose: <short purpose>
- files_checked: <number>
- elapsed_seconds: <number>
- findings:
  - <path>: `<term>` -> <short snippet>

SCOUT_RESULT logs-scout
- purpose: <short purpose>
- files_checked: <number>
- elapsed_seconds: <number>
- findings:
  - <path>: `<term>` -> <short snippet>

SCOUT_RESULT repo-scout
- purpose: <short purpose>
- files_checked: <number>
- elapsed_seconds: <number>
- findings:
  - <path>: `<term>` -> <short snippet>
```

```markdown
CONTEXT_BRIEF
Ticket: <Jira key or URL>
Summary: <one sentence>

LIKELY_REPO_AREA
- <area>: <why this area fits>

DOCS_CHECKED
- <path>: <short finding>

LOGS_CHECKED
- <path or source>: <short finding>

LIKELY_FILES
- <path>: <why the main agent should inspect it>

MISSING_INFO
- <none, or concrete question for a human>

CONFIDENCE
- <high|medium|low|NEEDS_HUMAN>: <one sentence rationale>

RECOMMENDED_NEXT_STEP
- <handoff instruction for the main Jira-to-PR agent>
```

## Readability Scoring

Use this rubric when comparing conversation logs:

| Score | Meaning |
| --- | --- |
| 5 | Customer can clearly see ticket, docs, logs, repo files, confidence, and next step in under 30 seconds. |
| 4 | Clear and demo-ready, with only minor noise or missing detail. |
| 3 | Understandable, but the context path takes work to follow. |
| 2 | Some useful findings, but the agent appears to wander or over-explain. |
| 1 | The context path is unclear, misleading, or not customer-demo friendly. |
