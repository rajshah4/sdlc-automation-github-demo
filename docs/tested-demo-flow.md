# Tested Demo Flow

Last updated: 2026-06-23 UTC.

## Local Validation

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
python3 skills/sdlc-story/scripts/validate_open_spec.py skills/sdlc-story/references/openspec-change-template
python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
NODE_PATH=/path/to/node_modules PLAYWRIGHT_BROWSER_CHANNEL=chrome python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/run_playwright_ui_demo.py --url http://localhost:4173 --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search
```

The build fixture now represents the bug-first demo path: a sparse issue reports that customers are seeing pets that are not available, with `PENDING_PET_VISIBLE` as the log clue.

## Historical Successful Build Result

Repository:

- `https://github.com/rajshah4/sdlc-automation-github-demo`

Issue:

- `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1`

Result:

- Rajistics OpenHands automation run `f84671ac-33b7-43d8-a0e4-3532fb180263` completed at `2026-06-23T02:29:45Z`.
- Rajistics OpenHands conversation: `https://app.replicated.rajistics.com/conversations/060aa6399eae4e77b2fcd630646fbe56`
- OpenHands posted the result comment: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4775062401`
- OpenHands opened PR #2: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/2`
- Issue #1 now has `openhands:done`.

Note: this successful build result used the earlier max-adoption-fee feature story before the demo assets were pivoted to bug-first examples. The active automation set is label-only and should use the current bug fixture for new dry runs.

## Registered OpenHands Automations

Prompt-preset automations were registered with the Rajistics Replicated API key:

| Work cell | Automation ID | Trigger |
| --- | --- | --- |
| `openhands-build` | `efc16fdb-04da-4140-963a-5e693bbc8bb4` | `issues.labeled` |
| `openhands-incident` | `4c9ebc42-eb96-4cc5-a4a7-13089bdd6506` | `issues.labeled` |
| `openhands-qa` | `fe3ea75f-dfbb-4779-a73f-a287380fdb27` | `pull_request.labeled` |
| `openhands-review` | `854dcbb9-0320-40f2-a8a7-e70d15cb737c` | `pull_request.labeled` |

Run-list check:

```bash
python3 scripts/list_openhands_automation_runs.py \
  --env-file /path/to/local/.env \
  --automation-id efc16fdb-04da-4140-963a-5e693bbc8bb4 \
  --limit 5
```

The previously registered comment-capable automation set was disabled. The active set above is label-only and skips items already marked `openhands:done`.

The Rajistics API was checked after registration and returned the active set as enabled with only `issues.labeled` or `pull_request.labeled` triggers.

## Not Tested Live

- SRE incident remediation was not run; cloud mutation remains report-only unless `scripts/petstore_gcp_observe.py` reports `diagnosis.safe_to_remediate=true`.
- QA and review automations are registered but were not live-triggered in this pass.
- The fresh label-only build automation was registered and preflight-validated, but not live-triggered after cleanup to avoid opening a duplicate PR for issue #1.
