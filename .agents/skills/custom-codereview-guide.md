---
name: custom-codereview-guide
description: Override rules for @openhands review on PRs. Force COMMENT status, never APPROVE, and suppress the separate summary comment.
triggers:
  - "@openhands review"
  - "@OpenHands review"
  - review
  - code review
  - pr review
  - /codereview
---

# Custom Code Review Guide (TEST)

These rules OVERRIDE the default review and summary behavior for any PR review
triggered by an `@openhands review` (or equivalent) comment on this repository.

## Review Status — ALWAYS COMMENT, NEVER APPROVE

When posting a GitHub pull request review, you MUST set the review `event` to
`COMMENT`. You must NEVER submit a review with `event: APPROVE` and NEVER submit
a review with `event: REQUEST_CHANGES`.

Even if the PR is flawless and has no findings, still submit the review with
`event: COMMENT` and include a brief note in the review body that the change
looks good. Do not use the APPROVE event under any circumstances.

Example of the correct review payload:

```json
{
  "commit_id": "<head sha>",
  "event": "COMMENT",
  "body": "Review summary...",
  "comments": []
}
```

## Summary Comment — DO NOT POST A SEPARATE SUMMARY

Do not post a separate "summary of what was done" PR comment after the review.
The GitHub pull request review itself is the complete output. Posting an
additional summary comment is duplicative and should be avoided.

Concretely, after you submit the PR review (with `event: COMMENT`), you are
done. Do not call the issue-comment API to post a follow-up summary. If the
runtime asks you to "send a final message summarizing your work", keep that
final message empty or respond that the review is the summary, and do not post
it as a separate GitHub comment.

## Acknowledgment

These rules apply to the review output only. They do not change the "I'm on
it!" acknowledgment, which is posted by the OpenHands platform.
