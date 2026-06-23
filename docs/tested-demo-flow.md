# Tested Demo Flow

Last updated: 2026-06-23 UTC.

## Local Validation

The intended validation sequence is:

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture fixtures/github_issue_comment_build.json
```

## Safe GitHub Validation

Use a disposable private GitHub repo for the first live test:

1. Push this repo.
2. Install only the self-hosted Rajistics OpenHands GitHub App.
3. Create labels with `python3 scripts/create_github_labels.py --repo OWNER/REPO --apply`.
4. Register automations with `python3 scripts/register_github_automations.py --apply`.
5. Create a fresh issue and comment `openhands-build`.
6. Confirm an OpenHands conversation appears and a result comment or PR is posted.

Cloud-mutating incident remediation is not required for the safe test. Use dry-run or report-only mode unless `scripts/petstore_gcp_observe.py` reports `diagnosis.safe_to_remediate=true`.

## Latest Safe Test

Repository:

- `https://github.com/rajshah4/sdlc-automation-github-demo`

Issue:

- `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1`

Validated:

- Labels were created from `config/github-labels.json`.
- Issue #1 was labeled with `type:story`, `openhands-build`, and `openhands:ready`.
- The deterministic GitHub Actions workflow ran successfully for work-cell label events.
- The test exposed a duplicate-trigger risk from status labels; filters were tightened so status labels no longer trigger work cells.
- After the guard fix, an `issue_comment` retest using `openhands-build` produced one successful deterministic workflow run.
- After OpenHands automation registration, a second `openhands-build` issue comment produced another successful GitHub Actions run, but the OpenHands build automation still showed no runs after the event.

Evidence:

- Successful run `27996217965`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996217965`
- Successful run `27996217942`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996217942`
- Successful comment-trigger retest run `27996297265`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996297265`
- Comment-trigger acknowledgement: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4774842490`
- Post-registration GitHub trigger run `27996464141`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996464141`
- A skipped non-matching event confirmed the workflow boundary also skips events outside the trigger guard.

Not tested live:

- GCP incident remediation was not run; cloud mutation remains report-only unless the safe-remediation script reports `safe_to_remediate=true`.
- GitHub-to-OpenHands event delivery for the new private repo did not produce an OpenHands run yet. The likely missing setup step is installing or refreshing the self-hosted OpenHands GitHub App on `rajshah4/sdlc-automation-github-demo`.

## Registered OpenHands Automations

Prompt-preset automations were registered through `scripts/register_github_automations.py --apply` using the configured OpenHands API credentials:

| Work cell | Automation ID |
| --- | --- |
| `openhands-build` | `843a19a5-25c5-493e-b253-746678362dc8` |
| `openhands-incident` | `6875f016-92c6-4d71-bcb6-c65805f5e858` |
| `openhands-qa` | `6be9edc4-8ef1-4d5f-a5ad-4e26ff278a13` |
| `openhands-review` | `311d2a61-9eee-4d32-93a6-ee7c6f49c9a4` |

Run-list check:

```bash
python3 scripts/list_openhands_automation_runs.py \
  --env-file /Users/rajiv.shah/Code/software-factory-demo/.env \
  --automation-id 843a19a5-25c5-493e-b253-746678362dc8 \
  --limit 5
```

Result after the post-registration issue comment: `[]`.

The earlier registrations that referenced the hidden skill path were disabled after the skills moved to the first-class `skills/` directory.
