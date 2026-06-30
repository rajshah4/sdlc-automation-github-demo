---
name: sdlc-context-reuse
description: Build cost-aware context reuse reports for the SDLC Automation Demo by loading AGENTS.md, skills, existing logs, GitHub repo search results, and prior OpenHands conversation memory before broad model work.
triggers:
  - openhands-context
  - context reuse
  - agent memory
  - token savings
  - lower cost model
---

# Cost-Aware Context Reuse

Use this skill when OpenHands needs to show how an agent avoids rediscovering the same repository, workflow, logs, and prior decisions on every run.

The customer-facing story is: a low-cost scout agent gathers reusable context first, writes a compact handoff report, and only then does the expensive coding or risk-review agent act.

## Context Source Order

1. `AGENTS.md` for durable repo rules, commands, product constraints, and human gates.
2. Repo-local skills for procedural memory: `sdlc-story`, `sdlc-qa`, `sdlc-code-review`, and `sdlc-incident`.
3. Existing logs and evidence, especially `docs/work-log.md`, `docs/tested-demo-flow.md`, QA reports, and incident references.
4. Targeted GitHub repo search for the files and tests relevant to the trigger.
5. Previous agent runs and conversation memory in `docs/repo-memory/previous-agent-runs.md` and linked OpenHands run records.

## Workflow

1. Read `AGENTS.md` and `docs/repo-memory/petstore-intelligence.md` before broad exploration.
2. Select only the skills relevant to the trigger label or issue type.
3. Run the deterministic context report builder when local tools are available:

```bash
python3 scripts/build_context_reuse_report.py \
  --fixture tests/fixtures/github_issue_labeled_context.json \
  --output docs/context-reuse/latest-context-reuse-report.md
```

4. Use the report as the handoff from the scout phase to build, QA, review, or incident work.
5. Update durable memory only when you learned a reusable fact. Keep issue-specific details in PRs, issue comments, or context reports.

## Model Routing Policy

- Use no LLM or the lowest-cost model for deterministic parsing, label classification, file search, and log summarization.
- Use a low-cost model for the scout report when summarization is needed.
- Use a coding-capable model only for implementation or plan repair.
- Escalate to a stronger model for high-risk production, security, broad architecture, or ambiguous remediation decisions.
- Prefer exact command output and checked-in evidence over generating a fresh explanation from scratch.

## Report Requirements

A context reuse report must include:

- which durable memory was loaded
- which skills were loaded
- which logs or reports were reused
- which files were found by targeted repo search
- which previous agent runs or conversations were reused
- what broad exploration was skipped
- what model tier should handle each phase
- a rough token/context estimate with a clear caveat that it is illustrative, not billing data

## Stop Conditions

Ask for human input if the trigger requires secrets, production mutation, billing/IAM changes, destructive actions, or broad scope that cannot be narrowed from repo-local memory and search.
