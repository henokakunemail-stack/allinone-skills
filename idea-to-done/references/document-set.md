# The document set

Each document has one job. This file says what goes in each, who reads it, and how to keep it honest. Templates are in `assets/`; copy the template, keep its headings, fill the sections.

Rule of thumb before creating any file: name the phase that will read it. If no later phase reads it, do not create it.

## Core documents

### PRD.md (software) / BRIEF.md (everything else)

**Answers:** What are we making and why, and where does it stop?
**Written:** Phase 2, from discovery answers. **Read by:** Phase 2 planning, every Phase 3 scope guard, Phase 4 layer 1.
**Changes only** through an agreed plan revision. If execution reveals the PRD is wrong, stop and propose the change; do not edit it quietly.

Sections:
- **Idea summary**: one paragraph in your words. If the user reads it and says "yes, exactly", you understood.
- **Requirements**: `R1`, `R2`, ... Each one derived from something the user said. Keep their words next to it in parentheses. A requirement with no source is an invention.
- **Success criteria**: observable, checkable statements. "The user can upload a CSV and see a chart within 5 seconds", not "it works well". Each criterion references the requirements it proves.
- **Scope Contract**:
  - *In scope*: only items that map to a requirement.
  - *Out of scope*: explicit list. Always consider the usual AI additions (authentication, multi-user, dark mode, logging, analytics, CI/CD, deployment, extra docs, refactoring of existing code, mobile layout, i18n, admin panel, notifications, tests beyond what verification needs) and list every one the user did not ask for.
  - *Assumptions*: `A1`, `A2`, ... Everything you decided without being told, with the reason. These are the user's chance to catch a wrong guess before it becomes code.
- **Open questions** (optional): things that could not be resolved and are parked, with the fallback you will use.
- **Version and change log**: `Version: 1.0` at the top; every post-approval change appends a line (version, date, what changed, source, affected tasks) per `revision-protocol.md`. Requirement IDs are never reused; a replaced requirement is marked `(superseded in vX by Rn)`, not deleted.

Owner: Product Manager. Nobody else edits this file.

### PLAN.md

**Answers:** How will we get there, in what order, and where are we now? This is also the roadmap; do not create a separate ROADMAP.md.
**Written:** Phase 2. **Updated:** every task in Phase 3, every round in Phase 4. **Read by:** every phase, every resuming agent, `scripts/status.py`. **Owner:** Engineering Manager, the sole writer; other roles report and it records.

Sections:
- **Status line** at the top: `Status: planning | awaiting-approval | executing | executing (parallel) | verifying | fixing | done`, plus the current phase. The first thing a resuming agent reads. Add a `Waiting since: <date>` line whenever Status is `awaiting-approval` or otherwise stopped on the user (a stop-and-ask trigger); remove it once they answer. A resuming agent that finds this line old — weeks, not hours — does not silently proceed on the agent's own authority: it says plainly how long the gate has been waiting and, if anything in the project or the world plausibly changed since then (dependencies, the user's own stated deadline, files that look edited by someone else), surfaces that before re-presenting the same gate.
- **Document index**: which documents exist in `docs/`, one line each on what it is for. A resuming agent uses this to know what to read.
- **Approach**: the method in a paragraph. For software, name the stack and point to ARCHITECTURE.md for detail.
- **Phases and tasks**. Task format (keep it exact; the status script parses it):
  ```
  - [ ] T1.1 Short imperative title → R2, R5
    - Deps: T0.1, T0.2   (or — if none; tasks that must be [x] first)
    - Files: src/x/, tests/test_x.py   (what this task owns; nothing else may be edited)
    - Accept: how this task is verified, concretely — must pass the stranger test (one command or action, checkable by someone who never saw the project)
    - Risk: (optional) why this is uncertain
    - Note: (filled on completion) one-line result with evidence
  ```
  Status markers: `[ ]` pending, `[~]` in progress, `[x]` done, `[!]` blocked (say why in Note). `Deps` and `Files` are what make parallel execution safe (see `parallel-execution.md`); write them even in sequential mode so a later session can switch.
- **Integration** phase: created in parallel mode when a wave breaks the build; tasks `I1`, `I2`, ...
- **Fixes** phase: created in Phase 4 if issues are found; tasks `F1`, `F2`, ... with the same format, each tracing to the VERIFICATION.md issue it fixes (`→ V3`).
- **Verification plan**: written in Phase 2, before anything is built, so that Phase 4 is not designed by someone who already knows what was built. Lists what will be run and what will be inspected.

**Splitting a large plan.** Once the plan holds more than roughly 60 tasks, or more than three Phases, a single `PLAN.md` stops being something a resuming agent (or the user) can actually read. At that point, split it: keep `PLAN.md` itself as a short index — status line, document index, approach, and a one-line-per-phase table pointing to where each phase's tasks live — and move each phase's task list into `docs/plan/phase-<n>-<slug>.md` (same task format, same rules, same single-writer ownership). `scripts/status.py` still needs one file to scan; either keep it reading `docs/PLAN.md` and teach it to follow the phase links, or point it at the phase file explicitly as a second argument. This is a structural change, not a scope change — it does not need a new approval, but note the split itself as a line in `DECISIONS.md` so a resuming agent knows to look for `docs/plan/`.

### DECISIONS.md

**Answers:** Why is it the way it is?
**Written:** Phase 2 (initial choices) and Phase 3 (as they happen). **Read by:** resuming agents, Phase 4, the user when they wonder "why did it do that".

One entry per decision: `D1`, date, the decision, the alternatives considered, the reason, which task triggered it. Short. The point is that nobody has to re-derive or second-guess the choice later.

### IDEAS.md

**Answers:** What did we think of and deliberately not do?
**Written:** any phase. **Read by:** the user at approval gate 2, and whenever they plan the next version.

One line per idea: what it is, why it came up, why it is out of scope (usually "not in the Scope Contract"). No design, no elaboration. This file is the pressure valve that makes "do not add features" sustainable: the idea is captured, so there is no urge to build it.

### VERIFICATION.md

**Answers:** Has it actually been proven to work, and what was found?
**Written:** Phase 4. **Read by:** the user at approval gate 2, the next verification round.

Sections: scope of the round (what was verified, by whom, fresh-eyes or not), the requirement-to-evidence table, the result-to-task trace (with untraceable items flagged as scope creep), functional tests run with their actual output, edge cases tried, document accuracy check, issues `V1`, `V2`, ... each with severity, repro, and the fix task it became, and finally accepted limitations.

## Conditional documents

### ARCHITECTURE.md

**Create when:** software with more than one component (a frontend and a backend, a CLI and a library, a service and a database, a pipeline with stages). A single-file script does not need one.
**Written:** Phase 2, before approval. **Read by:** Phase 3 tasks, Phase 4 layer 1.

Sections: components and their responsibilities, data flow between them (a simple text diagram is fine), stack with one-line reasons, external dependencies and why each is needed, constraints inherited from requirements (offline, single-user, etc.), and what is explicitly not part of the architecture. Every library or service named must be verified to exist and fit; mark anything not yet verified as `(unverified)` and verify before the task that uses it.

### STRUCTURE.md

**Create when:** software. **Written:** the first execution task that creates files. **Updated:** in the same step as any task that adds, moves, or removes files. **Read by:** every later task, Phase 4.

A tree of the project with one line per folder and per significant file saying what it is responsible for. This is the document that rots fastest; the rule "update it in the same step" exists because "I will update it at the end" never happens. Phase 4 compares it to the real tree.

**On an existing codebase** (the Phase 1 read-repo-first branch), add a short **Module relationships** section before any task starts: which modules call which, and the few dependencies that would break the most if changed carelessly — a handful of plain lines (`parser.py reads from config.py; cli.py calls both; tests/ exercises cli.py only`), not a diagram, not an exhaustive call graph, and not a separate tool or generated artifact. The point is the same one a generated code-relationship graph serves — giving an agent (this session's or a later one) the shape of the codebase without re-deriving it from scratch each time — but written by the Tech Lead who actually read the code, kept as plain markdown next to the rest of `docs/`, and updated the same way STRUCTURE.md's tree is: in the same task that changes the relationship, not as a separate maintenance chore.

### DESIGN.md

**Create when:** the deliverable has a deliberate visual or temporal form — a user interface (web, mobile, desktop, CLI with meaningful interaction), **or** a visual/time-based artifact: a video, a set of images, a poster, a slide deck, an animation, a brand set. Do not create it for a backend-only or script project, or a pure prose document. Written by the UI/UX Designer for a UI, by the Media/Visual Producer for a media artifact.
**Written:** Phase 2. **Read by:** UI/media tasks in Phase 3, Phase 4 functional + craft testing.

Pick the variant that fits; only include what traces to a requirement:

- **UI variant:** screens or views (list, purpose of each), user flows for the main PRD tasks (step by step), visual direction (tone, typography, color, density; match any references the user supplied), reused components, and required states (empty, loading, error).
- **Visual-system variant** (a set of graphics, a poster, a brand set): palette, type scale, grid/margins, the fixed elements every piece shares, and — the piece most often missed — an explicit **"identical vs varies" table**: which properties must be byte-for-byte consistent across the set and which may change per item. That table is the consistency contract Phase 4 checks against.
- **Storyboard variant** (video, animation, audio): a time-coded table — `Scene | t_start–t_end (duration) | on-screen text | visual | audio/VO | transition` — plus the overall visual/pacing direction. The scene durations must sum to the target length; state that sum as a check.

### OUTLINE.md

**Create when:** the deliverable is prose — a document, report, proposal, article, course, or SOP. For a deliverable that is structured data rather than prose (a calendar, a schedule, a table, a dataset), OUTLINE.md describes the *structure* only (columns, row meaning, ordering) and the filled grid lives in the deliverable file itself (below), not inside OUTLINE.md.
**Written:** Phase 2. **Read by:** Phase 3 writing tasks, Phase 4 review.

The structure of the deliverable section by section: purpose of each section, key points it must make, source material it draws on, approximate length. Each section traces to a requirement or success criterion.

**For an SOP, policy, or runbook**, the outline should carry the sections that make a procedure usable rather than a procedural essay: a document-control header (owner, approver, effective date, revision history), purpose, scope, roles/responsibilities (a RACI where handoffs matter), definitions, prerequisites/trigger, the numbered procedure itself, an exception/rollback path, and references to the policies it sits under. An SOP that is just numbered prose with none of these is the common failure.

### The deliverable file itself (non-software)

For software the deliverable *is* the code tree (STRUCTURE.md maps it). For a non-software deliverable — a proposal, a calendar, a video, an image set — the finished artifact is a named file (or folder) that is **not** one of the `docs/` planning files: e.g. `proposal.md`, `content-calendar.md`, `output/quote-01.png … quote-05.png`, `electricity_tips.mp4`. Name it in `PLAN.md`'s document index and in a task's `Files`, so it is tracked and so `scripts/status.py` and Phase 4 can find it. Do not pour the actual deliverable into PLAN.md or OUTLINE.md because it happens to be text — those are planning documents, not the thing being delivered.

**When the deliverable is itself a plan or schedule** (a content calendar, a roadmap, a release schedule), it is NOT this skill's own `PLAN.md`. `PLAN.md` tracks the work of *building* the deliverable; the user's schedule is its own deliverable file. Do not give the deliverable's entries task checkboxes (`[ ]`/`[x]`) — those mean build-progress, and a reader (or `status.py`) will read "all tasks done" as "the month shipped" when nothing has been published. For such a deliverable, Phase 2 and Phase 3 may legitimately merge: designing the schedule in planning IS most of the build, and forcing a separate near-empty execution phase is ceremony, not structure (note the merge in DECISIONS.md).

## Keeping documents honest

- A document that disagrees with reality is deleted or fixed in Phase 4; it is never left standing.
- Facts appear in one document and are referenced from others. Requirements live in PRD; tasks reference them by ID rather than restating them.
- Documents are written for the next reader, who may be a different agent with no memory of this conversation. Write what they need to act, not a diary of what you did.
- Do not create additional documents (CHANGELOG, CONTRIBUTING, API.md, ...) unless a requirement asks for them. If you think one is needed, it goes in IDEAS.md.
