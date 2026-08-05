# Automation Conversation-Link Gap (Self-Hosted / Replicated)

## TL;DR

On cloud (`app.all-hands.dev`), prompt-preset automations inject an
`AUTOMATION_SESSION_URL` secret so the agent can link to its own conversation
in PR descriptions and Jira comments. On self-hosted Replicated deployments
(Local mode), this injection is skipped, so the agent has no way to discover
its own conversation URL. This is a known product gap tracked in
[OHE-2554](https://linear.app/all-hands-ai/issue/OHE-2554) (Linear) and
[OpenHands/automation#221](https://github.com/OpenHands/automation/issues/221)
(GitHub).

**Status:** Worked around in this demo with custom automation scripts (Option B
below). All three work cells — Jira→PR, Review, and QA — now embed their
conversation URL directly in the prompt text and post it back to GitHub.

## What We Want

When the Jira → PR automation creates a draft PR and posts a Jira comment, it
should include a clickable link to the OpenHands conversation that did the
work, e.g.:

> OpenHands conversation: https://app.replicated.rajistics.com/conversations/3b0faacb-...

The same applies to the review and QA work cells — their GitHub review
comments and QA reports should link back to their own conversations.

## The Exact Code That Causes the Gap

The preset endpoint generates a `main.py` from a template. That template
lives in the `OpenHands/automation` repository at
`openhands/automation/presets/prompt/sdk_main.py` (and a mirror at
`presets/plugin/sdk_main.py`). Here is the relevant block (lines 371–376 as
of commit `85ed3cc`, 2026-07-24):

```python
# Build session URL from conversation ID and inject as a secret so
# the agent can use $AUTOMATION_SESSION_URL in bash commands.
if not IS_LOCAL_MODE and api_url:
    session_url = f"{api_url}/conversations/{conversation.id}"
    conversation.update_secrets({"AUTOMATION_SESSION_URL": session_url})
    print(f"  session URL: {session_url}")
```

Two variables gate this block:

| Variable | Cloud mode | Local mode (Replicated) |
|---|---|---|
| `IS_LOCAL_MODE` | `False` (no `AGENT_SERVER_URL`) | `True` (set at line 79) |
| `api_url` | `https://app.all-hands.dev` (from `OPENHANDS_CLOUD_API_URL`) | empty string (env var not set) |

In Local mode **both** conditions fail: `IS_LOCAL_MODE` is `True`, and
`api_url` is empty. The block is skipped entirely. The agent never receives
`AUTOMATION_SESSION_URL`, so any prompt instruction to use it produces an
empty value.

## Why the Guard Exists (Root Cause)

This is not a bug — it's an incomplete feature. The guard exists because in
Local mode there is no reliable way to build the **public UI URL** from
inside the sandbox.

### The Cloud-mode assumption

In Cloud mode, `OPENHANDS_CLOUD_API_URL` (e.g. `https://app.all-hands.dev`)
serves **both** the API and the web UI. So `{api_url}/conversations/{id}`
is a valid, clickable link a human can open.

### The Local-mode problem

In a self-hosted Replicated deployment, these are **different URLs**:

| Purpose | URL | Available to the script? |
|---|---|---|
| Agent server API (internal) | `http://openhands-agent-server.svc:18000` or `http://127.0.0.1:18000` | ✅ via `AGENT_SERVER_URL` |
| Web UI (public) | `https://app.replicated.rajistics.com` | ❌ not passed to the runtime |

The automation script can see `AGENT_SERVER_URL` (the internal API), but
building `{agent_server_url}/conversations/{id}` would produce an internal
URL that a human outside the cluster cannot open. So the original authors
skipped injection rather than emit a broken link.

### Git history confirms this

The session-URL injection was introduced in
[PR #142](https://github.com/OpenHands/automation/pull/142) (commit
`2ca55c1807`, 2026-05-27) as a **Cloud-only** feature. The commit message
explicitly says: *"Adds `AUTOMATION_SESSION_URL` to the sandbox env vars
when `SANDBOX_ID` is available (Cloud mode)."* At that time, Local mode
did not exist yet.

Local mode was added later via
[issue #62](https://github.com/OpenHands/automation/issues/62) / Linear
[OHE-1388](https://linear.app/all-hands-ai/issue/OHE-1388) ("Support
open-source self-hosted deployments"). The preset script was made dual-mode,
but session-URL injection was guarded with `if not IS_LOCAL_MODE` rather
than extended — because the public-UI-URL problem had no solution yet.

## Upstream Tracking

This gap is tracked in two places:

1. **Linear:** [OHE-2554](https://linear.app/all-hands-ai/issue/OHE-2554) —
   "Reviewer agent and QA Agent: add LLM, trajectories" (Priority 0, state:
   GitHub Backlog, unassigned). This is the internal ticket. Its description
   explicitly calls out: *"preset scripts inject `AUTOMATION_SESSION_URL`
   as a secret in cloud mode"* and *"`AUTOMATION_SESSION_URL` is not
   automatically added to GitHub review or QA comments."*

2. **GitHub:** [OpenHands/automation#221](https://github.com/OpenHands/automation/issues/221) —
   the public mirror of OHE-2554. It proposes adding a footer to automation
   comments with the LLM profile, conversation link, and run link.

Both are still open. No fix has been shipped upstream.

## Options

### Option A — Product fix (the right long-term fix)

Change the generated `sdk_main.py` to inject `AUTOMATION_SESSION_URL` in
Local mode too, using a new deployment-config value for the public UI URL.

The missing piece is a way to pass the **public UI base URL** into the
automation runtime. Options the product team could pursue:

- Add a new env var like `OPENHANDS_PUBLIC_URL` or
  `AUTOMATION_UI_BASE_URL`, set by the deployment (Replicated chart /
  Helm values / docker-compose), and read it in `sdk_main.py`.
- Derive it from `AUTOMATION_CALLBACK_URL` (the callback URL already
  points to the automation service, which is on the same host as the UI
  in most deployments).
- Add it to the `RemoteWorkspace` / agent-server settings so the preset
  script can fetch it via `workspace.get_ui_url()` or similar.

```python
# Proposed change to sdk_main.py:
ui_base_url = os.environ.get("OPENHANDS_PUBLIC_URL", "").rstrip("/")
if IS_LOCAL_MODE and ui_base_url:
    session_url = f"{ui_base_url}/conversations/{conversation.id}"
    conversation.update_secrets({"AUTOMATION_SESSION_URL": session_url})
elif not IS_LOCAL_MODE and api_url:
    session_url = f"{api_url}/conversations/{conversation.id}"
    conversation.update_secrets({"AUTOMATION_SESSION_URL": session_url})
```

**Pros:** Fixes it for all self-hosted customers, not just this demo. No
per-automation maintenance. Survives SDK/service upgrades. Aligns with the
upstream design proposed in OHE-2554 / issue #221.

**Cons:** Requires a product change in the automation service or SDK. Needs
a reliable way to know the public-facing UI URL from inside the sandbox.
The Replicated chart would need to expose this value to the automation pod
environment.

### Option B — Custom automation script (workaround, NOW IMPLEMENTED)

Replace the prompt-preset with a custom-script automation whose `main.py`
is modeled on the preset output but adds Local-mode injection with a
deployment-specific host.

The custom `main.py` is a copy of the preset `sdk_main.py` with one change:
after the conversation is created, it builds the session URL from a
hardcoded (or `OPENHANDS_PUBLIC_URL`-env-var) UI base and the conversation
ID, then:

1. Injects it as the `AUTOMATION_SESSION_URL` secret (for bash use), and
2. **Appends the resolved URL directly to the prompt text** so the agent
   sees the literal URL and can paste it without expanding a shell variable.

```python
# In the custom main.py, after conversation creation:
if IS_LOCAL_MODE:
    ui_base = (
        os.environ.get("OPENHANDS_PUBLIC_URL", "").rstrip("/")
        or "https://app.replicated.rajistics.com"
    )
    session_url = f"{ui_base}/conversations/{conversation.id}"
    conversation.update_secrets({"AUTOMATION_SESSION_URL": session_url})

    # Append the literal URL to the prompt so the agent doesn't need
    # to expand a shell variable — it can copy-paste the URL directly.
    USER_PROMPT += (
        f"\n\n---\n## Conversation Link\n\nThe URL for this OpenHands "
        f"conversation is:\n\n{session_url}\n\nInclude this URL in the PR "
        f"description and any GitHub comments you post, formatted as:\n\n"
        f"OpenHands conversation: {session_url}\n"
    )
```

**Why embed the URL in the prompt text (not just the secret)?** Early
testing showed that when the URL is only available as a bash environment
variable, the LLM occasionally writes the literal `${AUTOMATION_SESSION_URL}`
placeholder into the PR body instead of resolving it. Embedding the resolved
URL directly in the prompt text eliminates that failure mode — the agent
sees the actual URL and can copy it verbatim.

**Pros:** Works today, no product change needed. Full control over the
script. Can also add the provenance footer proposed in issue #221.

**Cons:** We maintain the SDK boilerplate ourselves. Must track SDK
upgrades manually (the preset's `setup.sh` auto-fetches the SDK version; a
custom script would use the same `setup.sh` but the `main.py` is frozen).
Hardcoded host URL is not portable across environments (mitigated by the
`OPENHANDS_PUBLIC_URL` env-var fallback). The custom-script path requires
explicit user agreement per the automation skill's rules.

### Option C — Agent self-discovery (not recommended)

Instruct the agent in the prompt to call the agent-server API
(`GET $AGENT_SERVER_URL/api/conversations`) to find its own conversation
ID, then construct the URL.

**Pros:** No script changes. Works with the preset endpoint.

**Cons:** Fragile — the agent doesn't know which conversation is its own.
Concurrent automation runs could pick the wrong conversation. Relies on
"most recent" heuristics. Also, `AGENT_SERVER_URL` is internal, so the
agent would still need the public UI URL to build a clickable link.

## Recommendation

**Option A** is the right durable fix and aligns with OHE-2554. Until it
ships upstream, **Option B** (custom script) is the pragmatic workaround
used by this demo.

## How To Apply This To An Automation (Option B)

Each of the three SDLC demo automations (Jira→PR, Review, QA) was converted
from a prompt-preset to a custom-script automation using the same pattern.
The steps are:

1. **Start from the preset `sdk_main.py`.** The preset endpoint generates
   this file when you create a prompt-preset automation. Download or copy
   the generated `main.py` and `setup.sh`.

2. **Add the Local-mode session-URL block** shown in Option B above, after
   the conversation is created and before `conversation.send_message()`.

3. **Add a "Conversation Link" section to the prompt** instructing the
   agent to include the URL in its GitHub output. The section in each
   prompt (`automations/*/prompt.md`) reads:

   ```markdown
   ## Conversation Link

   This automation's OpenHands conversation URL is appended to the end of
   this prompt by the runtime. Include it in the [PR description / review
   comment / QA report] so reviewers can trace the work back to the agent
   session. Add it as a concise line near the end:

   `OpenHands conversation: <url>`

   Copy the URL exactly as provided — do not write a shell variable or
   placeholder.
   ```

4. **Package as a tarball** (`main.py`, `setup.sh`, `repos_config.json`,
   and `prompt.txt`) and upload via the automation API:

   ```bash
   curl -X POST "${OPENHANDS_HOST}/api/automation/v1/uploads" \
     -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
     -H "Content-Type: application/gzip" \
     --data-binary @automation.tar.gz
   ```

5. **PATCH the existing automation** with the new `tarball_path` (do not
   create a duplicate automation):

   ```bash
   curl -X PATCH "${OPENHANDS_HOST}/api/automation/v1/${AUTOMATION_ID}" \
     -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{"tarball_path": "oh-internal://uploads/<upload-id>"}'
   ```

6. **Test end-to-end.** Create a Jira story (or manually add the trigger
   label to a PR) and verify the conversation link appears in the PR body
   and/or review/QA comments.

## Current State (2026-07-09)

All three SDLC demo work cells use the custom-script workaround (Option B):

| Work cell | Automation ID | Status |
|---|---|---|
| Jira → PR | `0d28716a-71c5-4d2f-a7db-64b9f9cec833` | ✅ Live, conversation links in PR body |
| Code Review | `27c02f29-bab7-47ab-93e5-dc5f8aaccd06` | ✅ Live, conversation links in review comments |
| QA | `30c42c03-8b76-4d45-8237-79db173e1ab6` | ✅ Live, conversation links in QA reports |

The original Jira → PR prompt-preset automation (`0ff815fd`) remains
disabled as a backup.

Verified end-to-end on PR #139 (KAN-144): Jira → PR → Review → QA → Done,
with conversation links in the review comment and QA report. The PR body
link depends on LLM reliability (the agent occasionally writes the literal
placeholder instead of the resolved URL; embedding the URL in the prompt
text minimizes this).

### Caveats

- The custom `main.py` is frozen at the SDK version it was generated from.
  When the automation service or SDK is upgraded, re-generate the preset
  `main.py` and re-apply the Local-mode injection block.
- The hardcoded UI host (`https://app.replicated.rajistics.com`) is
  deployment-specific. Set `OPENHANDS_PUBLIC_URL` in the automation pod
  environment to make the script portable.
- The Kubernetes patch that sets `FILE_STORE=s3` (MinIO) for package
  storage may be overwritten by a future Replicated redeployment. See
  [OHE-3033](https://linear.app/all-hands-ai/issue/OHE-3033) and the
  incident note in `install_replicate/incident-notes/`.
