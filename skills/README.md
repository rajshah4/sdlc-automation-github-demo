# SDLC Automation Demo Skills

These skills are intentionally version-controlled in a first-class `skills/` directory so other teams can read, copy, and adapt them without knowing about hidden agent folders.

| Skill | Purpose |
| --- | --- |
| `delegated-conversation-factory` | Builds parent/child delegated conversation workflows for Replicated OpenHands, Agent Canvas, and customer software-factory patterns. |
| `sdlc-story` | Turns sparse GitHub issues into OpenSpec-style change artifacts, scoped Petstore changes, tests, and PRs. |
| `sdlc-qa` | Builds out automated QA evidence, including API tests and UI smoke/browser evidence where applicable. |
| `sdlc-incident` | Performs SRE incident triage with Cloud Run/Cloud Logging evidence and bounded remediation rules. |
| `sdlc-code-review` | Layers Petstore-specific correctness, risk, and supply-chain checks onto OpenHands `/codereview`. |

Each skill keeps its own `SKILL.md` plus optional `references/` and `scripts/`. The scripts avoid unnecessary LLM calls and make the demo easier to inspect in customer conversations.

The GitHub labels in `.github/labels.json` are the human-controlled automation boundaries for the existing label-driven demo. The delegated factory skill supports the opt-in parent/child conversation flow without changing those automations.
