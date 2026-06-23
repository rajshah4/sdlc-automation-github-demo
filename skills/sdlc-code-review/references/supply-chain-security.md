# Supply Chain Security

Use this reference when a PR adds or changes dependencies, package metadata, GitHub Actions, installation scripts, Dockerfiles, or build images.

## Demo Default

The SDLC Automation Demo should avoid new dependencies unless the open specification explicitly requires them. Most Petstore changes can use the Python standard library and existing pytest setup.

## Review Checks

- Is this a new dependency? If yes, ask why the standard library or existing repo code is insufficient.
- Was the target version released very recently? Recent releases have less community review.
- Are there install-time hooks, postinstall scripts, `.pth` files, curl-to-shell patterns, or unpinned images?
- Did GitHub Actions permissions broaden beyond the workflow's needs?
- Did a Dockerfile start copying secrets, tokens, local dotfiles, or credentials?
- Does the PR introduce `pip install`, `npm install`, or registry access inside demo automation prompts?

## Escalation

Treat these as high risk:

- new dependency without clear need
- yanked/deprecated package or version
- install-time code execution
- broad workflow permissions such as write-all
- unpinned privileged container image
- secret exposure in scripts, logs, docs, or screenshots

## Output Snippet

```markdown
Supply-chain check:
- Dependency changes: none | reviewed | needs human follow-up
- Workflow/build permission changes: none | reviewed | needs human follow-up
- Notes:
```
