# Demo Upgrade Backlog

Keep this list focused on improvements that make the demo easier to reproduce,
explain, or operate. Raw timing notes and exploratory worklogs stay local.

## Sidekick Launcher Packaging

- Move `scripts/launch_sidekick_v2.py` into
  `skills/sdlc-sidekick-launcher/scripts/`.
- Update `skills/sdlc-sidekick-launcher/SKILL.md`, the `sidekick-v2` automation
  prompt, tests, and setup docs to call the skill-local script.
- Keep a thin top-level compatibility wrapper only if existing live automations
  still reference `scripts/launch_sidekick_v2.py`.

Why: the launcher is part of the sidekick skill's implementation. Keeping the
script inside the skill folder would make the skill feel self-contained when a
customer browses the repo.

## OpenHands SDK / Conversation API Wrapper

- Evaluate replacing the raw `urllib` calls in the launcher with the official
  OpenHands SDK when the SDK covers app-conversation creation, start-task
  polling, conversation events, and model/profile selection.
- Keep the customer-visible behavior the same: Step 0 launcher, three read-only
  scout conversations, main implementation conversation, then QA handoff.
- If the SDK path is adopted, keep comments in the launcher explaining the API
  objects so customers can map the code to the conversation UI.

Why: this demo started from the idea of using side agents. Today it implements
that architecture directly with OpenHands conversation APIs; an SDK wrapper
could make that easier to read and maintain.

## OpenSpec Folder Placement

Current shape:

- `skills/sdlc-story/references/` owns the OpenSpec-style templates and
  validation guidance.
- `openspec/project.md` and `openspec/changes/` provide a repo-level place for
  generated request-to-PR artifacts.

Recommended direction:

- Keep generated `openspec/changes/...` artifacts at repo level. They are meant
  to be visible in PR diffs and reviewable by humans.
- Consider moving static project guidance from `openspec/project.md` into
  `skills/sdlc-story/references/` if it is only used as agent context.
- If the repo-level `openspec/` folder remains, document it explicitly as the
  review artifact output area, not as an extra toolchain requirement.

Why: skills should own reusable instructions and templates; repo-level folders
should hold artifacts that reviewers and customers are expected to inspect.

## Demo Mode Switching

- Add a small script or documented command that toggles between:
  - fast mode: `jira-to-story` enabled, `sidekick-v2` disabled
  - visible sidekick mode: `jira-to-story` disabled, `sidekick-v2` enabled
- Re-run `scripts/preflight_live_connections.py` after the toggle and print the
  active mode.

Why: the current manual toggle is understandable, but a single command would
reduce pre-demo mistakes.

## UI Evidence Path

- Keep PR #6 as the prepared browser-evidence example.
- Add a prepared runtime note for installing Playwright or BrowserToolSet before
  a demo, without making the timed Jira path install browsers live.

Why: UI evidence is compelling, but the core Jira-to-PR demo should stay fast
and deterministic.
