# Work-Cell Prompt Contract

Each delegated child conversation needs a prompt that stands on its own.

## Required Sections

Use these sections for every work-cell prompt:

```text
# <Name> Work Cell

## Inputs
## What You Do
## Human Control
## Output Contract
```

## Inputs

Include concrete values for:

- run id
- repository or workspace path
- source request, ticket, PR, incident, or dataset
- artifact paths from earlier cells when relevant
- special runtime requirements such as browser evidence or model profile

## What You Do

Define the bounded job. Name repo-local skills, deterministic scripts, and
source files the child should prefer. Include any legacy context the child may
see, such as GitHub labels from an older workflow, and explain how to interpret
it.

## Human Control

State what the child must not do. Common boundaries:

- do not merge
- do not approve your own work
- do not bypass branch protection
- do not mutate production
- do not reveal secrets
- do not continue when product, security, or credential questions are blocking

## Output Contract

Require both a durable artifact and a compact final response. Example:

```text
status: done | needs-human | failed
artifact: factory_runs/{{run_id}}/<work-cell>.md
summary: <five or fewer bullets>
next_gate: <next-cell-or-stop>
```

Specialized cells can add fields such as `branch`, `pr`, `blocking`,
`tests`, or `evidence`, but keep the first four fields stable.

## Quality Bar

The supervisor must be able to decide the next gate from the final response and
artifact without reading the entire child event log. If that is not true, make
the work-cell contract narrower.
