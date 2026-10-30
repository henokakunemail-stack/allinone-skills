# Plan: todo-cli

Status: executing
Phase: 3 · Updated: 2026-10-28

## Document index
- `PRD.md` — what and why
- `PLAN.md` — this file
- `DECISIONS.md` — choices
- `IDEAS.md` — parked ideas
- `STRUCTURE.md` — file map

## Approach

Scale tier: small · Execution mode: sequential

Single module `todo.py` with a `main()` dispatching on argv; storage helpers read/write ~/.todo.json. Build storage first, then commands.

## Phases and tasks

Status: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked

### Phase 1: Foundation

- [x] T1.1 Create todo.py skeleton with argv dispatch and STRUCTURE.md → R5
  - Deps: —
  - Files: todo.py, docs/STRUCTURE.md
  - Accept: `python todo.py` with no args prints usage listing add/list/done and exits 0
  - Note: ran `python todo.py` → usage printed, exit 0
- [x] T1.2 JSON storage helpers load/save at ~/.todo.json → R4
  - Deps: T1.1
  - Files: todo.py
  - Accept: calling save([{"text":"x","done":false}]) then load() returns the same list; file created at ~/.todo.json
  - Note: verified in a python -c one-liner, file created

### Phase 2: Commands

- [~] T2.1 Implement `add TEXT` → R1
  - Deps: T1.2
  - Files: todo.py
  - Accept: `python todo.py add "beli susu"` then `python todo.py list` shows `1. [ ] beli susu`
  - Note:
- [ ] T2.2 Implement `list` and `done N` → R2, R3
  - Deps: T2.1
  - Files: todo.py
  - Accept: after adding two tasks, `python todo.py done 2` then `list` shows `2. [x] ...`; `done 9` prints an error and exits non-zero
  - Note:

## Verification plan
- Fidelity: R1–R5, SC1–SC2 to evidence
- Functional: fresh ~/.todo.json, run add/list/done sequence
- Edge: done with out-of-range number, add with empty text, corrupted JSON file
- Documents: STRUCTURE.md vs tree
- Verifier: QA mode
