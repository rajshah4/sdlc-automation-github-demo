# GitHub Provider

The GitHub provider supports the SDLC Automation Demo work cells:

- `openhands-review`
- `openhands-qa`
- `openhands-build`
- `openhands-incident`

Potential GitHub triggers:

- PR comment containing `openhands-review`
- `openhands-review` label
- `openhands-qa` label
- `openhands-build` issue label
- `openhands-incident` issue label
- requested reviewer

Where possible, use official OpenHands plugins and skills instead of custom provider code.

## Runtime

GitHub uses the GitHub OpenHands login side:

```text
OPENHANDS_API_KEY_GITHUB
GITHUB_TOKEN
GITHUB_OPENHANDS_<STAGE>_AUTOMATION_ID
```

GitHub chaining should use status labels such as `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, and `openhands:done`.
