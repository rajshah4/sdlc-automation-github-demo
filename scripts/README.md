# Scripts

Scripts are grouped by the demo path they support. Foldered paths are the
canonical paths for new docs, tests, and local commands.

The existing step-by-step demo should continue to call repo-local skills from
its automation prompts. These folders organize helper scripts; they do not move
SDLC policy out of skills or change the automation boundaries.

| Folder | Use |
| --- | --- |
| `scripts/automations/` | Register, list, disable, and label OpenHands automations. |
| `scripts/build_context_reuse_report.py` | Build deterministic context-reuse reports before expensive agent work. This remains top-level because live GitHub automation prompts call it directly. |
| `scripts/validation/` | Run local preflight checks and fixture simulations. |
| `scripts/openhands/` | Inspect or summarize OpenHands conversations. |
| `scripts/sidekick/` | Legacy sidekick launch helpers for the visible multi-conversation Jira demo. |
| `agent-canvas/scripts/` | Parent-child Agent Canvas factory launcher, orchestrator, delegate helper, and QA helpers. |

## Common Commands

Register step-by-step GitHub automations:

```bash
python3 scripts/automations/register_github_automations.py --dry-run
python3 scripts/automations/register_github_automations.py --apply
```

Register Jira automations:

```bash
python3 scripts/automations/register_jira_automations.py --dry-run
python3 scripts/automations/register_jira_automations.py --apply
```

Validate the local demo shape:

```bash
python3 scripts/validation/preflight_github_demo.py --offline
python3 scripts/validation/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
```

Run the Agent Canvas parent-child factory:

```bash
python3 agent-canvas/scripts/start_agent_canvas_factory.py --help
```

## Path Policy

New helper scripts should live in one of the folders above. Keep
`scripts/build_context_reuse_report.py` at the top level until the live GitHub
automation prompts are deliberately migrated and re-registered.
