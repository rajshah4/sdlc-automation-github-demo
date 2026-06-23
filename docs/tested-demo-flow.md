# Tested Demo Flow

Last updated: 2026-06-23 UTC.

## Local Validation

The intended validation sequence is:

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture fixtures/github_issue_comment_build.json
python3 skills/sdlc-story/scripts/validate_open_spec.py <path-to-open-spec.md>
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
| `openhands-build` | `02ee14cd-d57d-44a5-a182-14a2bb46c22d` |
| `openhands-incident` | `c1af72a7-e625-43bf-907d-572452a3db05` |
| `openhands-qa` | `77343499-1f2e-4d10-bb04-9292f112046c` |
| `openhands-review` | `2cc7de0f-2d35-4024-866e-d1c6985c3d1d` |

Run-list check:

```bash
python3 scripts/list_openhands_automation_runs.py \
  --env-file /path/to/local/.env \
  --automation-id 02ee14cd-d57d-44a5-a182-14a2bb46c22d \
  --limit 5
```

Result after the post-registration issue comment: `[]`.

The earlier registrations that referenced the hidden skill path were disabled after the skills moved to the first-class `skills/` directory. The second set of lightweight prompt registrations was disabled after the richer four-skill prompts were added.

## Skill Baseline Validation

The current repo-local skills are designed to be inspected in GitHub:

- `skills/sdlc-story` includes the open specification template, acceptance extraction, event classification, and OpenSpec validation.
- `skills/sdlc-qa` includes API/UI QA references, static UI smoke checks, and a local server harness.
- `skills/sdlc-incident` includes Cloud Run incident runbook guidance plus observation-report helpers.
- `skills/sdlc-code-review` includes risk and supply-chain review references plus a deterministic Petstore checklist.

The four OpenHands automations were re-registered after the richer prompt wording was added, so the OpenHands UI should now show the open-spec, QA, SRE, and code-review prompt details.
