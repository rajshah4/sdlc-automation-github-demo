# SDLC Automation Demo Skills

These four broad skills are intentionally version-controlled in a first-class `skills/` directory so other teams can read, copy, and adapt them without knowing about hidden agent folders.

| Skill | Purpose |
| --- | --- |
| `sdlc-story` | Turns sparse GitHub issues/comments into open specifications, scoped Petstore changes, tests, and PRs. |
| `sdlc-qa` | Builds out automated QA evidence, including API tests and UI smoke/browser evidence where applicable. |
| `sdlc-incident` | Performs SRE incident triage with Cloud Run/Cloud Logging evidence and bounded remediation rules. |
| `sdlc-code-review` | Layers Petstore-specific correctness, risk, and supply-chain checks onto OpenHands `/codereview`. |

Each skill keeps its own `SKILL.md` plus optional `references/` and `scripts/`. The scripts avoid unnecessary LLM calls and make the demo easier to inspect in customer conversations.

The GitHub labels in `config/github-labels.json` work for both OpenHands Automations and the deterministic GitHub Actions demo path.
