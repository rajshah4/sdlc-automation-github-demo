# Provider Adapters

Provider adapters isolate GitHub event shapes from the SDLC work cells.

The expected flow is:

```text
provider payload -> normalized event -> OpenHands automation -> provider action
```

Work cells should depend on the normalized event and helper methods, not raw provider payloads.

## Runtime Sides

Provider adapters also need a runtime context. This GitHub-native demo uses the GitHub OpenHands login side and GitHub-specific automation IDs.

The runtime contract lives in:

```text
providers/runtime-manifest.json
```

Use it before launching a work cell so the automation reads credentials from the correct GitHub secret namespace.
