# Plan: <project name>

Status: planning | awaiting-approval | executing | executing (parallel) | verifying | fixing | done
Phase: 2 · Updated: <date>

## Document index

- `PRD.md` — what and why; requirements, success criteria, Scope Contract
- `PLAN.md` — this file; approach, tasks, status
- `DECISIONS.md` — choices made and reasons
- `IDEAS.md` — out-of-scope ideas, parked
- `VERIFICATION.md` — created in Phase 4
- `ARCHITECTURE.md` — <present only if created> components and data flow
- `STRUCTURE.md` — <present only if created> file map, kept in sync with the tree
- `DESIGN.md` — <present only if created> screens and flows

## Approach

Scale tier: small | medium | large · Execution mode: sequential | parallel (see DECISIONS)

<One paragraph: the method. For software, name the stack and point to ARCHITECTURE.md. Say what is built first and why.>

## Phases and tasks

Status: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked
Every `Accept:` must pass the stranger test: one command or action, checkable without asking the author.

### Phase 1: <name>

- [ ] T1.1 <Imperative title> → R1
  - Deps: —
  - Files: <files or folders this task owns>
  - Accept: <concrete check>
  - Note:
- [ ] T1.2 <Imperative title> → R1, R3
  - Deps: T1.1
  - Files: <...>
  - Accept: <concrete check>
  - Risk: <why uncertain, if it is>
  - Note:

### Phase 2: <name>

- [ ] T2.1 <Imperative title> → R2
  - Deps: T1.1
  - Files: <...>
  - Accept: <concrete check>
  - Note:

### Integration
<Created in parallel mode if a wave breaks the build. Tasks I1, I2, ...>

### Fixes
<Created in Phase 4 if needed. Tasks F1, F2, ... each tracing to a V issue.>

## Verification plan

Written before building. What Phase 4 will run and inspect:

- Fidelity: map R1..Rn and SC1..SCn to evidence; trace result back to tasks
- Functional: <what will be run, from scratch, following the docs>
- Edge cases: <which of the checklist items apply to this project>
- Documents: STRUCTURE.md vs tree; ARCHITECTURE.md vs code; <...>
- Verifier: fresh agent if available, else QA mode
