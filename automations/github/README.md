# GitHub OpenHands Automations

This folder contains the GitHub-native automation package set for the SDLC Automation Demo.

The packages use the OpenHands Automations prompt preset API instead of custom SDK tarballs. That keeps registration simple, avoids ad hoc dependency installation, and makes the prompt visible in the OpenHands UI. Each package sets `keep_alive: true` so a completed sandbox remains available until the normal runtime cleanup policy removes it.

## Work Cells

| Work cell | GitHub trigger | Human boundary |
| --- | --- | --- |
| `openhands-context` | issue label | OpenHands posts a cost-aware context reuse report; humans decide which work cell to trigger next |
| `openhands-build` | issue label | OpenHands opens or updates a PR, then adds `openhands-review`; humans review and merge |
| `openhands-review` | PR label | OpenHands posts findings, then adds `openhands-qa`; humans decide what blocks |
| `openhands-qa` | PR label | OpenHands adds/runs QA evidence and marks the automation chain done; humans judge readiness |

The labels form a durable chain: Jira or a GitHub issue creates the PR, the PR
event starts review, and review's PR event starts QA. Each stage can also be
started manually by applying its label.

## Registration

Dry-run:

```bash
python3 scripts/automations/register_github_automations.py --dry-run
```

Apply:

```bash
python3 scripts/automations/register_github_automations.py --apply
```

By default, registration clones `main` for each run. For a live demo branch, pass an explicit ref:

```bash
python3 scripts/automations/register_github_automations.py \
  --apply \
  --repository rajshah4/sdlc-automation-github-demo \
  --repo-url https://github.com/rajshah4/sdlc-automation-github-demo \
  --ref codex/memory-cost-overlay
```

After rebuilding or replacing an OpenHands installation, run the registration
command again. Automation metadata and generated package storage may have
different lifecycles, so successful registration is part of the deployment
process rather than a one-time setup step.

Before a live demo, confirm that the GitHub organization is claimed by the
intended OpenHands organization, the GitHub App can access this repository, and
the installed automation runner is compatible with the runtime version.
