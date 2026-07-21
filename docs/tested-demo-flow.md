# Tested Demo Flow

Last updated: 2026-06-30 UTC.

This document keeps the public validation story concise: what to run, what the
viewer should see, and which human gates remain in place. Exploratory notes stay
outside the repo.

## Local Validation

```bash
python3 -m pytest -q
python3 scripts/validation/preflight_github_demo.py --offline
python3 scripts/validation/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_context.json
python3 scripts/build_context_reuse_report.py --fixture tests/fixtures/github_issue_labeled_context.json --stdout
python3 scripts/validation/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
python3 skills/sdlc-story/scripts/validate_open_spec.py skills/sdlc-story/references/openspec-change-template
python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```

The build fixture represents the bug-first demo path: a sparse issue reports
that customers are seeing pets that are not available, with
`PENDING_PET_VISIBLE` as the log clue.

## Automation Packages

Prompt-preset automations are registered with the Rajistics OpenHands API. The
saved prompt files are intentionally version-controlled so customers can inspect
the workflow boundary.

| Work cell | Package | Trigger |
| --- | --- | --- |
| Jira bug to PR | `automations/jira/jira-to-story/` | `jira:issue_created` from `jira-direct` |
| Visible sidekick Jira bug to PR | `automations/jira/jira-to-story-sidekick-v2/` | `jira:issue_created` from `jira-direct`, label `sidekick-v2` |
| GitHub context scout | `automations/github/openhands-context/` | `issues.labeled` |
| GitHub build | `automations/github/openhands-build/` | `issues.labeled` |
| GitHub QA | `automations/github/openhands-qa/` | `pull_request.labeled` or `issues.labeled` |
| GitHub review | `automations/github/openhands-review/` | `pull_request.labeled` |

Register the packages with:

```bash
python3 scripts/automations/register_github_automations.py --apply
python3 scripts/automations/register_jira_automations.py --apply
```

Use the same explicit `--ref` with both registration scripts when validating a
demo branch before it is merged. Customer installations normally use `main`.

## Fast Jira-To-PR Demo

Use this when you want the most reliable live customer demo.

1. Keep `jira-to-story` enabled and `jira-to-story-sidekick-v2` disabled.
2. Run the live read-only preflight in `main` mode.
3. Create a sparse Jira Task in the demo project.
4. Show OpenHands finding docs/log evidence, locating the repo files, adding a
   focused regression test, opening a PR, and applying `openhands-review`.
5. Show review posting findings and applying `openhands-qa`.
6. Show QA posting test evidence, then stop at human review. The automation does not approve, merge, deploy, or
   bypass branch protection.

Viewer-facing story:

- Sparse Jira ticket arrives in business language.
- OpenHands uses repo-local docs and logs to understand the bug.
- OpenHands finds the implementation and test files.
- OpenHands creates a PR with tests and evidence.
- Code review and QA run as separate PR-label conversations.
- Humans keep merge authority.

## Visible Sidekick Demo

Use this when you want the multi-conversation “wow” moment.

1. Disable `jira-to-story` and enable `jira-to-story-sidekick-v2`.
2. Run the live read-only preflight in `sidekick-v2` mode.
3. Create the Jira Task with label `sidekick-v2`.
4. Show the Step 0 launcher conversation as the index.
5. Open the visible docs, logs, and repo scout conversations.
6. Open the main implementation conversation and PR.
7. Show review hand off to QA and keep human merge authority as the final gate.

Expected visible sequence:

- `DEMO_STEP 0`: Jira webhook launcher unwraps the event.
- `DEMO_STEP 2A`: docs scout finds product/wiki context.
- `DEMO_STEP 2B`: logs scout finds symptom evidence.
- `DEMO_STEP 2C`: repo scout finds likely implementation and test files.
- `DEMO_STEP 3`: main implementation fixes the bug, adds tests, opens the PR,
  and adds `openhands-review`.
- `DEMO_STEP 4`: review posts findings and adds `openhands-qa`.
- `DEMO_STEP 5`: QA posts test evidence.

The sidekick launcher command and operational guardrails live in
`skills/sdlc-sidekick-launcher/` so the automation prompt stays readable.

## UI And Playwright Evidence

The live Jira bug path does not require browser tooling. For a prepared UI proof,
use `docs/ui-playwright-example.md`, which points to a PR with:

- UI files changed
- Playwright spec added
- screenshot/GIF/video/report artifacts
- QA PR comments

Do not install Playwright during a timed live demo unless runtime provisioning is
itself the thing being tested.

## Human Control

OpenHands may open PRs, add tests, post comments, and apply status labels.
Humans still own:

- scope acceptance
- PR review
- merge
- deployment
- risky follow-up decisions

## Not Part Of The Public Demo

- Exploratory timing notes are kept locally.
- Experimental automation variants stay local until they are stable enough for
  customers to inspect.
