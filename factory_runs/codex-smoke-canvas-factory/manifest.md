# SDLC Factory Run Manifest

## Run ID
`codex-smoke-canvas-factory`

## Repository
- Slug: `rajshah4/sdlc-automation-github-demo`
- Local path: `/Users/rajiv.shah/Code/sdlc-automation-github-demo`

## Story Request
- Issue: `#101`
- Title: `Filter pets by max adoption fee`
- Body: `As an adoption coordinator, I want to filter available pets by maximum adoption fee so families can find pets that fit their budget.`

## Incident
- Title: `Pending pets are visible in the available-pets experience`
- Body: `Operators report that pending pets can appear in the available-pets path. Gather evidence and recommend the safest remediation without mutating production.`

## Planned Work Cells (in order)

| # | Cell | Purpose | Gate |
|---|------|---------|------|
| 1 | context-scout | Read-only recon: repo memory, skills, likely surfaces | story-to-pr unlocked when done |
| 2 | story-to-pr | Implement feature branch + draft PR for issue #101 | code-review + QA unlocked when PR/branch produced |
| 3 | code-review | Automated code review of the PR diff | human approval to merge |
| 4 | qa | Functional QA: run tests, validate UI/API behaviour | sign-off or block |
| 5 | incident | Read-only incident analysis + remediation recommendation | human action to apply fix |

## Child Conversation Links

| Cell | Conversation ID | UI URL | Status | Artifact |
|------|----------------|--------|--------|---------|
| context-scout | `fc1aa845-62fd-47fe-b240-f927efb7f454` | [open](http://localhost:8000/conversations/fc1aa845-62fd-47fe-b240-f927efb7f454) | ✅ done | context-scout.md |
| story-to-pr | `08328969-a702-499d-8a09-802f2856e2dc` | [open](http://localhost:8000/conversations/08328969-a702-499d-8a09-802f2856e2dc) | ✅ done | PR #86 |
| code-review | `d70df31e-1721-4a22-8617-27e67fab4f0a` | [open](http://localhost:8000/conversations/d70df31e-1721-4a22-8617-27e67fab4f0a) | ⚠️ findings (non-blocking) | code-review.md |
| qa | `7729ee3a-63b8-4d1d-ad38-b2fcbc9ded9d` | [open](http://localhost:8000/conversations/7729ee3a-63b8-4d1d-ad38-b2fcbc9ded9d) | ✅ pass | qa.md + ui-evidence/ |
| incident | `51112f28-9d54-4de1-abc2-beb7e56ce70b` | [open](http://localhost:8000/conversations/51112f28-9d54-4de1-abc2-beb7e56ce70b) | 🔴 needs-human | incident.md |

## Human Gates
- PR #86 review and merge require human approval
- Incident remediation (`petstore_config_fix.py`) requires operator with GCP credentials
- CI pipeline gap flagged by code-review — maintainer decision required

## Status
COMPLETE — lifecycle report at `lifecycle-report.md`
