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

Evidence:

- Successful run `27996217965`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996217965`
- Successful run `27996217942`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996217942`
- Successful comment-trigger retest run `27996297265`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996297265`
- Comment-trigger acknowledgement: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4774842490`
- A skipped non-matching event confirmed the workflow boundary also skips events outside the trigger guard.

Not tested live:

- OpenHands prompt-preset registration was dry-run only because the live Rajistics/OpenHands automation API values were not set in this local environment.
- GCP incident remediation was not run; cloud mutation remains report-only unless the safe-remediation script reports `safe_to_remediate=true`.
