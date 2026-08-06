# Design: Optional name sort for pet catalog

## Context

The Petstore catalog currently returns pets in their data source order (Mochi, Scout, Pip, Nova). Adopters need a way to scan the catalog alphabetically to find pets more easily.

## Decision

- Add an optional `sort_by` parameter to the `search_pets()` function.
- When `sort_by="name"`, sort results alphabetically by name (case-insensitive).
- When `sort_by` is `None` or not provided, preserve the current catalog order.
- Add a sort dropdown to the UI that applies name sorting.

## Implementation

### Backend Changes

**File**: `app/petstore_app/catalog.py`

Add an optional `sort_by` parameter to the `search_pets()` function:

```python
def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",
    tag: str | None = None,
    max_results: int = 10,
    sort_by: str | None = None,
) -> list[Pet]:
```

After filtering matches, apply sorting:

```python
if sort_by == "name":
    matches.sort(key=lambda pet: pet.name.lower())
```

### Frontend Changes

**File**: `app/web/index.html`

Add a sort dropdown in the toolbar section:

```html
<label>
  Sort by
  <select id="sort-by">
    <option value="">Default</option>
    <option value="name">Name</option>
  </select>
</label>
```

**File**: `app/web/app.js`

1. Read the sort selection:
   ```javascript
   const sortBy = document.querySelector("#sort-by").value;
   ```

2. Apply sorting to matches:
   ```javascript
   if (sortBy === "name") {
     matches.sort((a, b) => a.name.localeCompare(b.name));
   }
   ```

## Testing Strategy

- Test backend sorting with multiple pets (alphabetically out of order by default).
- Test that leaving `sort_by` unset preserves default order.
- Test that UI sort dropdown applies name sort correctly.

## Risks

- Low risk: The change is isolated to the search function and UI controls.
- No database or schema changes required.

## Validation Plan

1. Run focused backend tests: `pytest app/tests/test_pet_catalog.py -v`
2. Verify UI behavior manually or with existing Playwright tests if applicable.
