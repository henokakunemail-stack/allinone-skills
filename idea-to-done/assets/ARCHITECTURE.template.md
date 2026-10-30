# Architecture: <project name>

Status: draft | approved · Updated: <date>

## Components

| Component | Responsibility | Talks to |
|---|---|---|
| <name> | <one line> | <components> |

## Data flow

<Simple text diagram or numbered steps for the main flow(s) from the PRD.>

```
user → [frontend] → HTTP → [api] → [db]
```

## Stack

Every item verified to exist and fit, or marked (assumed, unverified) until the task that uses it confirms it.

| Layer | Choice | Reason | Status |
|---|---|---|---|
| Language | <...> | <one line; cite the requirement or assumption> | verified |
| <...> | <...> | <...> | (assumed, unverified) |

## External dependencies

| Dependency | Why needed | Requirement |
|---|---|---|
| <library / service> | <...> | R<n> |

## Constraints inherited from requirements

- <offline, single user, must run on X, data must stay local, ...> → R<n>

## Explicitly not part of this architecture

- <authentication, scaling, multi-tenant, ...> (out of scope per PRD)
