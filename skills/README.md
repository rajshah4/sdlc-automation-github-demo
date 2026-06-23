# SDLC Automation Demo Skills

These skills are intentionally version-controlled in a first-class `skills/` directory so other teams can read, copy, and adapt them without knowing about hidden agent folders.

| Skill | Purpose |
| --- | --- |
| `sdlc-story` | Turns sparse GitHub issues into scoped Petstore PRs. |
| `sdlc-code-review` | Adds Petstore-specific review rules for OpenHands PR review. |
| `sdlc-qa` | Guides QA/test generation and UI evidence collection. |
| `sdlc-incident` | Defines incident triage and safe-remediation rules. |
| `gcp-observability` | Captures read-only Cloud Run and Cloud Logging guidance. |
| `github-automation` | Encodes GitHub label/comment/status boundaries. |

Each skill keeps its own `SKILL.md` and may include small deterministic scripts in `scripts/`. The scripts avoid LLM calls and make the demo easier to inspect in customer conversations.

