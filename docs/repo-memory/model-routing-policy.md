# Model Routing Policy

This demo uses model routing as cost governance: cheap agents narrow context, stronger agents act only when the task requires it.

| Phase | Typical work | Recommended tier | Notes |
| --- | --- | --- | --- |
| Deterministic preflight | Parse labels, fixtures, repo files, test commands | No LLM | Scripts should run before model calls. |
| Context scout | Summarize `AGENTS.md`, skills, logs, search hits, prior runs | Low-cost model | Produces the handoff report. |
| Story implementation | Update code, tests, OpenSpec-style artifacts, PR body | Coding model | Use after the scout has narrowed files. |
| QA evidence | Run tests, summarize exact outputs, capture UI evidence | No LLM or low-cost model | Use command output as source of truth. |
| Code review | Risk review, bug finding, missing tests | Medium model by default | Escalate for security or broad architecture. |
| Incident triage | Cloud evidence, safe-remediation decision | Low-cost for evidence summary; strong for high-risk judgment | Never mutate production without human approval. |

## Demo Talk Track

The goal is not to make every model call cheap. The goal is to spend premium reasoning only after the harness has loaded reusable memory, searched narrowly, and removed irrelevant context.

For Terraform, the same policy maps to:

- low-cost scout: workspace inventory, module ownership, prior plan summary, previous conversation search
- coding model: module upgrade edits and moved blocks
- strong/risk model: scary plan failures, IAM/state changes, or uncertain migration decisions
- human gate: applies, broad workspace changes, secrets, and state operations
