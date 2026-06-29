# Petstore Catalog Availability Rules

Default customer-facing catalog search must show only pets with `status="available"`.

Support and operations workflows may explicitly request `status="pending"` when investigating a case, but pending pets must not appear in the default available-pets experience or an available-only species search.

Known demo mapping:

- Nova is `pet-103`.
- Nova has `status="pending"`.
- A `PENDING_PET_VISIBLE` log means a pending pet appeared in the available-pets experience and should be treated as a catalog regression.
