# Wiki: Pet Discovery Affordability

This page represents the Confluence-style context used in the Jira-to-OpenHands demo.

## Business Language

Adoption counselors and support teams often describe adoption-fee search in everyday language:

- "families need to find pets in their budget"
- "show pets people can afford"
- "filter by fee cap"
- "cost range"
- "budget limit"

When a Jira ticket uses those phrases, map the request to the Petstore Catalog capability.

## Product Requirement

Pet discovery search should support an optional maximum adoption fee so counselors can help families narrow results before they visit.

Acceptance expectations:

- Search accepts an optional maximum adoption fee.
- Adoption fees are represented in integer cents.
- Pets above the maximum fee are excluded.
- Default search still returns only available pets.
- Pending pets remain hidden unless status is explicitly requested.
- Invalid negative fee caps are rejected.

## Ownership

Capability:

```text
Petstore Catalog Search
```

Repository:

```text
rajshah4/sdlc-automation-github-demo
```

Likely files:

```text
app/petstore_app/catalog.py
app/tests/test_pet_catalog.py
```

Non-goals:

- payment processing
- checkout
- persistence
- currency conversion
- authentication
- new dependencies
