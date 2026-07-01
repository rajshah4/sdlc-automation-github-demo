# GitHub OpenHands Automations

This folder contains the GitHub-native automation package set for the SDLC Automation Demo.

The packages use the OpenHands Automations prompt preset API instead of custom SDK tarballs. That keeps registration simple, avoids ad hoc dependency installation, and makes the prompt visible in the OpenHands UI.

## Work Cells

| Work cell | GitHub trigger | Human boundary |
| --- | --- | --- |
| `openhands-context` | issue label | OpenHands posts a cost-aware context reuse report; humans decide which work cell to trigger next |
| `openhands-build` | issue label | OpenHands opens or updates a PR; humans review and merge |
| `openhands-review` | PR label | OpenHands posts review findings; humans decide what blocks |
| `openhands-qa` | PR label | OpenHands adds/runs QA evidence; humans judge readiness |
| `openhands-incident` | issue label | OpenHands posts incident report or small fix PR; humans approve production actions |

## Registration

Dry-run:

```bash
python3 scripts/register_github_automations.py --dry-run
```

Apply:

```bash
python3 scripts/register_github_automations.py --apply
```

By default, registration clones `main` for each run. For a live demo branch, pass an explicit ref:

```bash
python3 scripts/register_github_automations.py \
  --apply \
  --repository rajshah4/sdlc-automation-github-demo \
  --repo-url https://github.com/rajshah4/sdlc-automation-github-demo \
  --ref codex/memory-cost-overlay
```
