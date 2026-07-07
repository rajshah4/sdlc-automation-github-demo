# Delegated Conversation Blueprint

## Purpose

Use a delegated conversation workflow when one visible supervisor should
coordinate specialized Agent Canvas conversations. The pattern is useful when a
team wants reusable orchestration instead of a chain of label-triggered runs.

## Required Pieces

| Piece | Responsibility |
| --- | --- |
| Supervisor prompt | Names inputs, rules, work-cell order, gate logic, and final report requirements. |
| Delegate helper | Creates child conversations with encrypted settings passed in memory. |
| Work-cell prompts | Give each child complete context and a bounded output contract. |
| Run directory | Stores manifest, prompt snapshot, child metadata, final responses, and lifecycle report. |
| Gate model | Decides whether to continue, stop, or ask for humans. |

## Supervisor Checklist

The supervisor prompt should:

- say the human starts only the parent conversation
- forbid doing the full lifecycle inside the parent
- name the local repository path and system of record
- call the orchestrator script rather than hand-rolling Canvas API requests
- require every child conversation id and UI URL to be written to the run
  directory
- define the exact work-cell order
- define stop conditions and human gates
- require one final lifecycle report

## Artifact Layout

Use a stable run directory so the operator and future agents can inspect the
same evidence:

```text
factory_runs/<run-id>/
  parent.conversation.json
  manifest.md
  prompt-snapshot/
  children.json
  children-summary.md
  <work-cell>.conversation.json
  <work-cell>.wait.json
  <work-cell>.final.json
  <work-cell>.md
  lifecycle-report.md
```

## Gate Statuses

Prefer a small status vocabulary:

- `done` or `pass`: continue when the artifact exists and evidence is enough
- `findings`: continue only when findings are non-blocking
- `needs-human`: stop before unsafe or under-specified work
- `failed`: stop and report the failure

## Adaptation Notes

To adapt the pattern for another team, change the cells and prompts first, then
only change code if the sequencing model itself needs to differ. Keep the
delegate helper generic: settings transport, conversation creation, waiting,
and final-response retrieval are infrastructure, not business logic.
