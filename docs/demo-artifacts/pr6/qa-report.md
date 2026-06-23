# Petstore UI QA Report

## Status

PASS

## Browser Scenarios

- Default catalog shows Mochi, Scout, and Pip.
- Pending pet Nova is not visible by default.
- Max adoption fee `80` hides Scout and leaves Mochi/Pip visible.
- Max adoption fee `40` shows the empty-state message.
- Negative fee `-1` shows inline validation.

## Artifacts

- GIF preview: [adoption-fee-filter.gif](adoption-fee-filter.gif)
- Screenshot: [adoption-fee-filter.png](adoption-fee-filter.png)

The local Playwright run also produced a `.webm` video in
`/tmp/sdlc-petstore-playwright/videos/`; the GIF above is the committed preview
for GitHub PR review.
