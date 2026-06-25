# Tested Demo Flow

Last updated: 2026-06-24 UTC.

## Local Validation

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
python3 scripts/simulate_jira_event.py --fixture tests/fixtures/jira_comment_created_build.json
python3 scripts/simulate_jira_event.py --fixture tests/fixtures/jira_issue_created_budget_story.json
python3 skills/sdlc-story/scripts/validate_open_spec.py skills/sdlc-story/references/openspec-change-template
python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
NODE_PATH=/path/to/node_modules PLAYWRIGHT_BROWSER_CHANNEL=chrome python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/run_playwright_ui_demo.py --url http://localhost:4173 --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search
```

Focused Jira validation run on 2026-06-24:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_automation_packages.py tests/test_github_label_fixtures.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider
python3 scripts/register_jira_automations.py --dry-run --project-key KAN --repo-url https://github.com/rajshah4/sdlc-automation-github-demo
python3 scripts/simulate_jira_event.py --fixture tests/fixtures/jira_comment_created_build.json
```

Results:

- focused Jira/package tests: `7 passed`
- full test suite: `21 passed`
- Jira dry-run payload used source `jira`, event `comment_created`, and filter `projectKey == 'KAN'`
- Jira fixture matched `openhands-build`

## Successful Build Result

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

Note: this successful build result happened before the final label-only cleanup. The active automation set is now label-only and was not re-triggered on issue #1 to avoid creating duplicate work from a completed issue.

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

## Registered Jira OpenHands Automation

The Jira build path was registered with the Rajistics Replicated API key through the OpenHands prompt preset API:

| Work cell | Automation ID | Trigger |
| --- | --- | --- |
| `openhands-build` | `f21a7ebb-9a20-4c22-8517-b13b717512f6` | custom source `jira`, `comment_created`, `projectKey == 'KAN'` |

Jira event path:

```text
Jira Automation rule
  -> https://app.replicated.rajistics.com/jira-shim
  -> OpenHands custom webhook source jira
  -> SDLC Demo - Jira OpenHands Build
  -> OpenHands conversation / PR
```

Validated pieces:

- Jira service-account token works with Bearer auth through `JIRA_API_BASE_URL`.
- `GET $JIRA_API_BASE_URL/rest/api/3/myself` returned the `OpenHands Agent` app account in a runtime smoke conversation.
- The custom OpenHands webhook source `jira` exists.
- The Jira shim accepted both signed shim smoke requests and token-header smoke requests.
- The Jira prompt-preset automation is enabled in Rajistics.
- Local fixture simulation matches the Jira build automation.

## Not Tested Live

- SRE incident remediation was not run; cloud mutation remains report-only unless `scripts/petstore_gcp_observe.py` reports `diagnosis.safe_to_remediate=true`.
- QA and review automations are registered but were not live-triggered in this pass.
- The fresh label-only build automation was registered and preflight-validated, but not live-triggered after cleanup to avoid opening a duplicate PR for issue #1.
- The Jira Automation rule in project `KAN` has not yet been live-tested from Jira by commenting with `@openhands`.

## Planned Jira Direct Webhook Demo

Preferred customer path:

```text
Jira Task created in KAN
  -> signed Jira admin webhook
  -> OpenHands custom webhook source jira-direct
  -> SDLC Demo - Jira Direct OpenHands Build
  -> docs/wiki + logs context gathering
  -> repo/file discovery
  -> code fix, tests, draft PR
  -> Jira summary and optional Teams escalation
```

Primary sparse Jira ticket:

```text
Families need to find pets in their budget
```

The expected agent interpretation is:

```text
budget / afford
  -> adoption affordability
  -> maximum adoption fee filter
  -> Petstore Catalog Search
  -> app/petstore_app/catalog.py and app/tests/test_pet_catalog.py
```

Local demo fixtures:

- `tests/fixtures/jira_issue_created_budget_story.json`
- `tests/fixtures/jira_issue_created_needs_human.json`
- `docs/wiki/pet-discovery-affordability.md`
- `docs/logs/pet-search-budget-limit.ndjson`
