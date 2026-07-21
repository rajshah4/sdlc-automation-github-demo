---
name: sdlc-story
description: Turn sparse GitHub or Jira bug reports and requests into OpenSpec-style change artifacts, scoped Petstore implementation, tests, and a human-reviewable PR for the SDLC Automation Demo.
triggers:
  - openhands-build
  - open spec
  - open specification
  - bug to pr
  - story to pr
  - sparse issue
---

# SDLC Request To PR

Use this skill when OpenHands turns a GitHub or Jira issue into a small reviewable PR.

The customer-facing story is: a sparse business-language bug report becomes an OpenSpec-style change proposal, spec delta, design, and task list, then an implementation branch, then a PR that humans review and merge.

## OpenSpec Lineage

This skill intentionally follows the Fission-AI/OpenSpec project:

- Project: `https://github.com/Fission-AI/OpenSpec`
- Site: `https://openspec.pro`
- Upstream pattern: `openspec/changes/<change-id>/proposal.md`, `design.md`, `tasks.md`, and `specs/.../spec.md`

For live OpenHands Automations, do not run `npm install`, `npm install -g @fission-ai/openspec`, or `openspec init/update` inside the timed label-triggered run. Those steps add network and toolchain variance to a customer demo. Instead, create the OpenSpec-style artifacts directly from `references/open-spec-template.md` and validate them with `scripts/validate_open_spec.py`.

If the OpenSpec CLI is preinstalled and the operator explicitly asks to use it, it is acceptable to run read-only or already-installed CLI validation. Otherwise, keep the live automation deterministic and explain in the PR that the artifacts follow OpenSpec lineage without invoking the CLI during the run.

## Inputs

- GitHub or Jira issue title, body, labels, and comments
- repository default branch
- target source branch
- acceptance criteria when present
- linked PRs or previous automation comments when present

Sparse issues are the primary demo path. The ticket should not need repo names, file paths, log codes, or implementation clues. For bug-shaped issues, first identify the violated behavior, repo-local docs, and any fixture/log evidence before editing code. Infer the smallest safe implementation, but write the assumptions, spec delta, task list, and human gates into the OpenSpec-style change folder before editing code.

## GitHub Boundaries

- Trigger label: `openhands-build`
- Status labels: `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, `openhands:done`
- Use event context; do not poll GitHub.
- Avoid result comments that repeat the exact trigger text.
- Use runtime secret `GITHUB_TOKEN` for GitHub API calls, `gh`, pushes, PRs, labels, and comments. Do not use `GITHUB` or `GH_TOKEN`; if auth is missing or returns 401, stop and report `GITHUB_TOKEN` is missing or invalid without printing it.
- Do not run `git remote -v`, `gh auth status`, or any command that prints token-bearing remote URLs. Use GitHub tools or API calls for PR creation and label/comment updates, and never echo auth-bearing remotes, token previews, or authorization headers.
- Never merge, bypass review, change branch protection, or alter deployment settings.

## Jira Boundaries

- Treat Jira Tasks as source issues when the automation starts from a Jira webhook.
- Use the Jira issue key and URL in artifacts and comments.
- Keep Jira comments concise: status, evidence waypoints, PR link, tests, and any human questions.
- Do not require the Jira ticket to mention logs, docs, repository names, file paths, or error codes.

## Workflow

0. Use `skills/sdlc-context-reuse/SKILL.md` or `scripts/build_context_reuse_report.py` to reuse durable context before broad exploration.
1. Read `README.md`, `AGENTS.md`, and the issue context.
2. Read `references/story-artifacts.md`, `references/open-spec-template.md`, and `references/petstore-implementation-map.md`.
3. Run `python3 skills/sdlc-story/scripts/extract_acceptance_criteria.py "<issue title>"` with the issue body on stdin when useful.
4. Create or update an OpenSpec-style change folder at `openspec/changes/github-issue-<number>-<slug>/` or `openspec/changes/jira-<issue-key>-<slug>/`.
5. Include `proposal.md`, `design.md`, `tasks.md`, and at least one `specs/<capability>/spec.md` file.
6. Validate the change folder with `python3 skills/sdlc-story/scripts/validate_open_spec.py <change-folder>`.
7. Search docs, logs, app code, and tests to find the smallest safe code change.
8. Implement the narrow change that satisfies the spec delta.
9. Add or update focused tests.
10. Run the narrowest useful validation first.
11. Open a draft PR with OpenSpec change link, evidence, and human-review notes.
12. After opening or updating the PR, add `openhands-review` as the final GitHub mutation so code review starts as a separate conversation. Do not add `openhands-qa`; the review work cell owns that handoff. A parent-child supervisor may explicitly override this when it owns downstream orchestration itself.

## Evidence Waypoints

For bug-first demos, make the reasoning path visible. The conversation, PR body, and final issue comment should include these waypoints:

- `Stop 1 - Ticket`: the sparse issue and the business-language clues used.
- `Stop 2 - Wiki/Docs`: the wiki or docs checked, with paths such as `docs/wiki/petstore-catalog-availability.md`; if none are relevant or accessible, say so.
- `Stop 3 - Logs`: log attachments or fixtures checked, with paths such as `docs/logs/pending-pet-visible.ndjson` and error codes such as `PENDING_PET_VISIBLE`; if no logs are available, say so.
- `Stop 4 - Repo/Files`: the repo and files that explain the bug and fix.
- `Stop 5 - Tests/PR`: tests added or run, validation result, and draft PR link.

## OpenSpec-Style Change Artifacts

Use `references/open-spec-template.md` and `references/story-artifacts.md` for the required folder shape, headings, and demo-friendly language. The artifacts are not ceremony; they are the contract that connects the request, implementation, QA, review, and human follow-up.

The change folder must include:

- source issue/comment link
- proposal with why, what changes, impact, assumptions, and non-goals
- spec delta with acceptance criteria expressed as requirements and scenarios
- design notes for the smallest safe implementation
- task checklist
- human gates
- validation plan
- evidence checklist
- evidence waypoints for wiki/docs, logs, repo/files, tests, and PR

If a request has unresolved product, security, data, or environment questions, post the partial OpenSpec-style change and label `openhands:needs-human` instead of guessing.

## Petstore Map

- Catalog behavior: `app/petstore_app/catalog.py`
- Adoption behavior: `app/petstore_app/adoptions.py`
- Static UI: `app/web/`
- Tests: `app/tests/`
- OpenSpec-style changes: `openspec/changes/github-issue-<number>-<slug>/`
- Jira OpenSpec-style changes: `openspec/changes/jira-<issue-key>-<slug>/`

## Sparse Bug Examples

`Customers are seeing pets that are not available` means:

- default available-pets search must exclude pets with `status="pending"`
- correlate the symptom with `PENDING_PET_VISIBLE` evidence when logs or fixtures are present
- inspect `app/petstore_app/catalog.py` and existing tests before changing behavior
- add or repair focused tests proving pending pets stay out of default available results
- do not mutate deployment settings, secrets, auth, or unrelated UI behavior

`Nova is showing up as adoptable` means:

- map Nova to `pet-103` and confirm her status is `pending`
- preserve explicit pending searches when the caller asks for `status="pending"`
- keep the default catalog path available-only
- add focused regression coverage

## Sparse Feature Examples

`Filter pets by max adoption fee` means:

- add an optional max-fee filter to catalog search, using integer cents
- expose a simple static UI input only if the issue or PR scope includes UI
- add focused backend tests for match, exclusion, and invalid negative fees
- do not add payment processing, persistence, billing, auth, or dependencies

`Let adopters search by age range` means:

- add optional min/max age filters
- reject negative ages and inverted ranges
- keep default search limited to available pets
- add focused backend tests

## Stop Conditions

Ask for human input if the issue requires a product decision, schema migration, auth change, new dependency, environment change, secret access, or production mutation.

## PR Requirements

The PR body must show:

- OpenSpec change path
- evidence waypoints, including wiki/docs and logs checked
- assumptions and non-goals
- acceptance criteria status
- files changed
- tests run
- residual risks
- reminder that humans approve review and merge decisions

When the repo supports the chained automations, add `openhands-review` to the PR after it is created or updated. Code review then adds `openhands-qa` after posting its findings. These handoffs start bounded automation work only; they must not approve, merge, bypass branch protection, or remove human PR review.
