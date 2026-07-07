---
name: delegated-conversation-factory
description: Build or adapt parent-child delegated conversation workflows for OpenHands Replicated, Agent Canvas, SDLC automation, reusable software-factory patterns, supervisor conversations, child work cells, lifecycle reports, and prompt/blueprint scaffolding. Use when replacing label-by-label automations with one orchestrating conversation that delegates bounded child conversations, or when creating a reusable delegated workflow for another repo or team.
---

# Delegated Conversation Factory

## Overview

Use this skill to turn a sequential automation demo into a delegated
conversation workflow for OpenHands Replicated or Agent Canvas:

- one supervisor conversation acts as the visible control plane
- child conversations perform bounded work cells
- every child gets a self-contained prompt
- artifacts, final responses, gates, and links are written to a run directory
- humans keep authority over scope, review, merge, deployment, secrets, and
  production changes

## Workflow

1. Identify the work cells and gates. Keep each child narrow enough that its
   final response can be judged by the supervisor.
2. Read `references/blueprint.md` before creating or changing the parent
   prompt, orchestration script, or work-cell list.
3. Read `references/work-cell-contract.md` before creating child prompts.
4. Prefer the repo helpers for child creation: `scripts/agent_canvas_delegate.py`
   for Agent Canvas and `scripts/openhands_v1_delegate.py` for OpenHands
   Replicated. Do not hand-roll settings payloads, print encrypted settings, or
   store API keys in files.
5. When bootstrapping a new repo, run
   `scripts/scaffold_delegated_factory.py --target <repo> --name <factory-name>`
   from this skill folder, then customize the generated prompts.
6. Preserve the legacy automation path unless the user explicitly wants it
   removed. The delegated workflow can reference GitHub labels as context, but
   labels should not control sequencing.

## Design Rules

- The parent conversation orchestrates; it should not silently do all child
  work itself.
- Child prompts must include all inputs they need. Do not rely on hidden parent
  context.
- Each child must write a durable artifact and return a small machine-readable
  final response contract.
- The supervisor advances only when the previous child returns an acceptable
  status and artifact.
- Use deterministic scripts and repo-local skills before broad exploration.
- Stop or mark `needs-human` for missing credentials, unsafe production access,
  unresolved product scope, security risk, or failed validation.

## Resources

- `references/blueprint.md`: parent conversation, run directory, sequencing,
  artifacts, and gate model.
- `references/work-cell-contract.md`: required sections and final response
  contract for child prompts.
- `assets/factory-blueprint.json`: editable starting point for another team's
  delegated workflow.
- `scripts/scaffold_delegated_factory.py`: creates a prompt and blueprint
  skeleton in a target repo.
