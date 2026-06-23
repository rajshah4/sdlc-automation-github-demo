# Risk Evaluation

Use this reference when reviewing a PR or deciding whether automation should request human follow-up.

## Low Risk

Low-risk changes are narrow, well tested, and reversible.

Examples:

- small Petstore filter behavior with focused tests
- docs or prompt wording with no trigger/filter change
- deterministic script output improvements
- UI copy/layout changes with smoke evidence

Review expectation:

- normal review
- focused test check
- note residual risk only if evidence is thin

## Medium Risk

Medium-risk changes touch shared behavior or automation boundaries.

Examples:

- catalog behavior that changes defaults
- adoption validation changes
- GitHub label/comment trigger filters
- OpenHands prompt changes that could create loops
- incident scripts that alter eligibility checks

Review expectation:

- require clear acceptance criteria
- require tests for old and new behavior
- check status-label loop guards
- ask for human follow-up if evidence is incomplete

## High Risk

High-risk changes can affect production, secrets, identity, billing, or broad automation behavior.

Examples:

- secret handling
- GitHub App permissions
- cloud remediation, deployment, IAM, or billing
- new dependencies or package-manager changes
- workflow permissions broadening
- scripts that mutate cloud resources without a deterministic safety gate

Review expectation:

- do not approve automatically
- require explicit human approval
- require rollback or report-only plan
- require supply-chain review for dependency changes

## Output

Include one line in the review:

```markdown
Risk: low | medium | high - <why>
```

Escalate to `needs human follow-up` when risk is high or when evidence is missing for a medium-risk behavior change.
