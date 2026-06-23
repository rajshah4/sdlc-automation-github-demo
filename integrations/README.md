# Integrations

Integrations connect the SDLC automation to systems outside source control.

GitHub is the SDLC surface. Integrations such as Slack and Google Cloud are notification, observability, runtime, and evidence surfaces.

## Initial Integrations

- Slack: automation notifications and human handoff
- Google Cloud: Cloud Run runtime, Cloud Logging evidence, synthetic incident signals

## Out Of Scope For This Demo

- Email and personal Gmail dependencies
- destructive cloud remediation
- secret rotation
- data deletion
- IAM mutation

## Demo Flow

```text
GitHub issue, PR, label, or comment
  -> OpenHands automation
  -> Slack notification
  -> Google Cloud evidence when operational context is needed
  -> PR or issue evidence
```
