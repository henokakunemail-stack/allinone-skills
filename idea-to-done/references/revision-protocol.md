# Revision protocol: changing the plan in the open

The PRD and the plan are a contract with the user. Contracts change; what must never happen is the contract changing without anyone noticing. This protocol makes every change visible, traceable and reversible in thought.

## When this applies

- The user asks for something new, different or removed, at any phase after gate 1.
- Execution or verification reveals a requirement is wrong, impossible, or ambiguous in a way that changes the result.
- An assumption (A-item) turns out to be false.
- A worker's blocked question, once answered, changes what gets built.

It does **not** apply to: adding `Deps`/`Files` to tasks, splitting a task into sub-tasks, renaming a task, fixing a typo. Those are plan maintenance; the Engineering Manager does them and notes them in the task.

## The steps (Product Manager leads; Engineering Manager records)

1. **State the change in one sentence** and its source: the user's words, or the evidence that forced it.
2. **Bump the PRD version** (`1.0` → `1.1` for additions or clarifications; `1.0` → `2.0` if a requirement is removed or reversed) and append a line to its **Change log**:
   ```
   - v1.1 (2026-10-30): R5 added — skip PENDING transactions. Source: user, "abaikan PENDING". Requested after T2.2 blocked. Affects: T2.2.
   ```
3. **Update the requirements** in the PRD: add `R<n>` with the quote, or mark an existing one `(superseded in v1.1 by R<n>)` rather than deleting it. IDs are never reused.
4. **Update the Scope Contract** if the change moves something between in / out / assumptions.
5. **Update the plan**: new tasks with traces to the new R-item, `Deps`, `Files`, stranger-checkable `Accept`; existing tasks adjusted with a note; tasks made obsolete marked `[x]` with `Note: superseded by v1.1, not built` (not deleted, so the history reads).
6. **Record in `DECISIONS.md`**: `D<n>: Plan revision to v1.1`, what changed, why, what it affects.
7. **Re-approval**: a change that adds or removes scope goes back to the user as a short gate-1-style summary ("v1.1 adds R5 and one task; nothing else changes. OK?"). A change the user themselves requested in plain terms counts as approved when they said it; still show them the change-log line so they see it landed as they meant.
8. **Verification plan**: if the change adds behavior, add how Phase 4 will check it.

## What the change log is for

Three months later someone asks "why does this ignore PENDING rows?" The answer should be findable in three places that point at each other: the change-log line in the PRD, the R-item with the user's words, the DECISIONS entry. If any of the three is missing, the protocol was not followed.

## Anti-patterns

- Editing `R3` in place to mean something else. The old meaning vanishes and tasks that traced to it now trace to a different requirement.
- "Small" changes applied directly in code because they seemed obvious. Obvious to whom, and will the verifier know to test it?
- Re-running discovery because of one new requirement. One question, one R-item, one change-log line.
- Deleting obsolete tasks. Mark them superseded; the plan is also the project's history.
