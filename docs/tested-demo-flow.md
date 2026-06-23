# Tested Demo Flow

Last updated: 2026-06-22.

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

