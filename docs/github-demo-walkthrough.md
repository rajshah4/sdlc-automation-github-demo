# GitHub Demo Walkthrough

This is the live flow for the GitHub-native SDLC Automation Demo.

## 1. Create Or Comment On An Issue

Create a GitHub issue with a sparse title such as:

```text
Filter pets by max adoption fee
```

Add the label `openhands-build`, or comment:

```text
openhands-build
```

OpenHands should clarify the request inside the conversation, infer the smallest safe Petstore change, create a feature branch, run focused tests, and open a draft PR. The PR should document assumptions, acceptance criteria, evidence, and human review notes.

## 2. Automation Creates A PR

Show the generated PR and call out the human controls:

- PR is draft or reviewable, not auto-merged.
- Reviewers decide whether the implementation is acceptable.
- CI and branch protections still apply.
- Humans choose whether to merge.

## 3. Trigger PR Review

On the PR, add the label `openhands-review`, or comment:

```text
openhands-review
```

OpenHands should inspect the diff, apply repo-local Petstore review rules, and post a structured code review comment. It should not claim tests passed unless it ran them or verified evidence.

## 4. Trigger QA And Test Generation

On the PR, add the label `openhands-qa`, or comment:

```text
openhands-qa
```

OpenHands should run or add focused tests, exercise the changed behavior, and include UI evidence when the static web app changed.

## 5. Human Review And Merge

Show the normal GitHub review path:

- humans inspect OpenHands comments and code diffs
- humans resolve findings or ask follow-up questions
- humans approve and merge only when ready

## 6. Optional SRE Incident Flow

Create an incident issue with label `openhands-incident`, or comment:

```text
openhands-incident
```

Use the sample symptom:

```text
The Petstore website is showing pending pets in the available-pets experience.
Please inspect GCP logs and propose the safest fix.
```

OpenHands should collect GCP evidence, summarize impact, identify whether remediation is safe, and either post an operator report or open a small fix PR. It must not mutate cloud resources unless the bounded safe-remediation check passes.

