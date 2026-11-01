# idea-to-done

An [Agent Skill](https://agentskills.io) (v1.1) that takes a raw idea through five disciplined phases:

0. **Orientation** — resume from `docs/PLAN.md` if the project already exists
1. **Discovery** — 4 to 7 targeted questions, one round, answers become numbered requirements
2. **Planning** — `PRD.md` with a Scope Contract, `PLAN.md` with traceable tasks, plus `ARCHITECTURE.md` / `DESIGN.md` / `OUTLINE.md` when the project needs them → **approval**
3. **Execution** — task by task, or in parallel waves of workers when the agent supports it; each task verified and recorded; out-of-scope ideas parked in `IDEAS.md`
4. **Verification** — whole-system testing by a fresh agent (or QA mode), issues become fix tasks → **approval**

The work is organized like a small office. Five core roles (Product Manager, Tech Lead, Engineering Manager, Engineer, QA Engineer) and six specialists activated only when the scope needs them (UI/UX Designer, Technical Writer, Researcher, Security Reviewer, DevOps, Editor/Craft Reviewer). Each role is a mandate with refusals and an artifact, never a rubber stamp; roles talk only through `docs/`. A scale rule decides whether roles run as separate agents or as hats worn by one agent.

Its distinguishing rule: the office builds only what the approved Scope Contract says and states only what it has verified. Every task traces to a requirement; every acceptance criterion can be checked by a stranger; every shipped feature traces back to a task; every scope change goes through a logged revision.

Works with any agent that reads the Agent Skills standard. Only `SKILL.md` is required; `references/` are read when a phase needs them, `assets/` are document templates, `scripts/status.py` prints progress.

## Install

The folder is the same everywhere; only the location changes. Copy (or symlink) the `idea-to-done/` folder into one of these:

| Agent | Project-level | Global |
|---|---|---|
| Claude Code | `.claude/skills/idea-to-done/` | `~/.claude/skills/idea-to-done/` |
| Claude app / claude.ai | — | Settings → Capabilities → Skills → upload the `.skill` or `.zip` file |
| OpenAI Codex | `.agents/skills/idea-to-done/` | `~/.codex/skills/idea-to-done/` or `~/.agents/skills/idea-to-done/` |
| Google Antigravity (IDE) | `.agents/skills/idea-to-done/` | `~/.gemini/config/skills/idea-to-done/` |
| Google Antigravity (CLI) | `.agents/skills/idea-to-done/` | `~/.gemini/antigravity-cli/skills/idea-to-done/` |
| Cursor | `.cursor/skills/idea-to-done/` (also reads `.claude/skills/` and `.codex/skills/`) | `~/.cursor/skills/idea-to-done/` |
| Gemini CLI, Copilot, others | `.agents/skills/idea-to-done/` | `~/.agents/skills/idea-to-done/` |

`.agents/skills/` is the shared location most tools read, so for a project that is opened in several agents, put it there once.

With the Skills CLI (where available): `npx skills add <repo-or-path> --skill idea-to-done`.

Paths were checked in October 2026 against each tool's documentation. Check the tool's docs if a path has moved.

### Upgrading

The install is just a folder copy, so upgrading is the same copy, again. Pull the latest version of this repo (`git pull`, or re-download it) and re-copy or re-symlink `idea-to-done/` over the old one at the same path from the table above — or, if you installed with the Skills CLI, run the same `npx skills add ...` command again; it overwrites the existing copy. Your own project's `docs/` folder is untouched either way, since the skill and the projects it produced are separate.

### Uninstalling

Delete the `idea-to-done/` folder from wherever you installed it (the same path from the table above). There is nothing else to clean up — no background process, no registry entry, no state outside that folder and your own projects' `docs/`.

## Use

Say what you want to make:

> I want to build a small tool that turns my bank CSV exports into a monthly spending summary.

The agent will ask a handful of questions, write `docs/PRD.md` and `docs/PLAN.md` (and `ARCHITECTURE.md` if warranted), and wait for your approval. Then it executes, then it verifies, then it asks you to sign off.

To resume, open the project and say "continue", or invoke the skill by name (`/idea-to-done` in Claude Code, `$idea-to-done` in Codex, or by describing the project).

To check progress from a terminal:

```
python path/to/idea-to-done/scripts/status.py            # looks for ./docs/PLAN.md
python path/to/idea-to-done/scripts/status.py other/dir  # project root as argument
```

## Documents the skill produces

In the project's `docs/` folder:

| File | Always? | Purpose |
|---|---|---|
| `PRD.md` / `BRIEF.md` | yes | What and why; requirements, success criteria, Scope Contract |
| `PLAN.md` | yes | How and when; tasks with traces and status; document index; also the roadmap |
| `DECISIONS.md` | yes | Choices and reasons |
| `IDEAS.md` | yes | Out-of-scope ideas, parked |
| `VERIFICATION.md` | yes | What was tested and found |
| `ARCHITECTURE.md` | software, multi-component | Components, data flow, stack |
| `STRUCTURE.md` | software | File map, kept in sync with the tree |
| `DESIGN.md` | has a UI | Screens, flows, visual direction |
| `OUTLINE.md` | non-software | Section-by-section structure |

## Structure of this skill

```
idea-to-done/
├── SKILL.md                      phases, hard rules
├── README.md                     this file
├── references/
│   ├── discovery-questions.md    question bank by category
│   ├── document-set.md           what each document contains and who reads it
│   ├── scope-guard.md            anti-creep and anti-fabrication rules
│   ├── execution-rules.md        the per-task loop and stop-and-ask triggers
│   ├── parallel-execution.md     orchestrator/worker mode: waves, briefs, integration checks
│   ├── revision-protocol.md      how scope changes are logged and re-approved
│   └── roles/                    role cards: README (roster, activation, scale) + one card per role
│   ├── verification-checklist.md the four verification layers
├── assets/                       templates for every document
└── scripts/
    └── status.py                 progress summary from docs/PLAN.md
```

## Changelog

**v1.7.0** — turns capability honesty from a dead end into a provisioning decision. v1.5's rule stopped the skill from implying media output it couldn't produce — correct, but it left the user at a wall ("can't make it smooth") with no way forward. v1.7 keeps the honesty and adds a path:
- New reference **`references/media-capability.md`**: a three-tier capability ladder (A local rendering / B local models / C hosted connectors) and a provisioning procedure — the Media/Visual Producer names the target quality tier the request really asks for, the Tech Lead detects what the environment can actually reach (local tools, local models, and **any configured media-generation / voice / music connector**), routes to the best available, and where the target needs something absent, records the gap and tells the user the **one thing to enable** to close it while delivering the best achievable tier as a provisional fallback.
- **Capability blocked-assumptions must now be actionable**: a missing-capability gap (`scope-guard.md`) has to name how to lift it — which connector, key, or tool — not just state that it exists.
- **`DESIGN.md` gains a Capability ladder block** (target tier / available / gap / how to close), surfaced at **gate 2** so the shortfall is actionable, not just noted. Template and `document-set.md` updated.
- **Roles wired for provisioning**: Tech Lead does media capability provisioning (not just skill-routing); Media/Visual Producer sets the target tier; Video Editor and Audio/Sound Designer route to a configured generation connector when one exists, not only local tools. Discovery's media M0 points to the ladder.
- **Guardrails held**: honesty is not a quality cap — capability is lifted by adding tools, never by dropping the no-fabrication/source-read-only rules; generated output is still verified (probed/watched); and a hosted connector call is an external, usually paid action, so it is not incurred unattended without standing authorization.

**v1.6.0** — splits media production into a creative sub-team instead of one catch-all producer. v1.5 gave media work a single Media/Visual Producer; real video/image jobs want distinct hands. Four new specialist roles, each with its own mandate, refuses, and artifact (activated only when the Scope Contract gives them work, like every specialist):
- **Scriptwriter** (`references/roles/scriptwriter.md`) — the words and their timing for video/voiceover/ads/podcasts; refuses inventing claims the brief doesn't supply, and refuses writing lines a beat has no time to show.
- **Video Editor** (`references/roles/video-editor.md`) — assembling/cutting/sequencing/captioning video; refuses asserting a "highlight"/"best take" it can't justify from observed content (ties into the blocked-assumption rule), overwriting source footage, and quality-degrading re-encodes.
- **Image Editor** (`references/roles/image-editor.md`) — editing/retouching/batch-processing existing images; refuses overwriting originals (source-read-only hard rule), "enhancing" beyond the task, and verifying one image while declaring a batch done.
- **Audio / Sound Designer** (`references/roles/audio-designer.md`) — voiceover, music, sound, mixing, transcription/captioning; gated on capability honesty (no TTS/music model → say so and fall back to a silent/captioned default rather than imply audio it can't render).
- The **Media/Visual Producer** is repositioned as the **creative lead** that holds the direction and storyboard and directs these four, mirroring how the Tech Lead leads the Engineers. On a small job one agent still wears all the hats in turn. (Optional roles considered but not added as standing cards — Motion/Animation Designer, dedicated Narrator/Voice, Thumbnail/Cover Designer — are folded into these four unless a project needs them often enough to promote.)

**v1.5.0** — extends the skill from software/prose work to media, batch, and schedule deliverables, after stress-testing it against video, image, SOP and content-calendar requests exposed that its governance spine transferred but its document/verification/role shape was software- and prose-only. Ten changes:
- **New `media` category** (video, audio, images, graphics, motion) in discovery, with its own assumption-killers — exact spec (dimensions/duration), count and an "identical vs varies" consistency contract, narration-vs-captions, visual style, on-screen language — plus a capability-honesty check so the skill never implies photographic/illustrated/voiced output it can't actually render.
- **New Media/Visual Producer role** (`references/roles/media-producer.md`): owns visual and temporal direction for non-UI visual artifacts, and is explicitly accountable to *refuse* a selection it can't justify from observed content rather than fake one.
- **`DESIGN.md` now covers any deliberate visual/temporal artifact**, not just UIs, with three template variants: UI, visual-system (palette/type/grid + the identical-vs-varies table), and a time-coded storyboard whose scene durations must sum to the target length.
- **Verification branches for the new shapes** (`references/verification-checklist.md`): video/audio (ffprobe + frame-sampling + watch), batch/collection (count in==out, invariant over *all* items, deliberate worst-case, originals-untouched by checksum), set-consistency (diff each item vs item 1), schedule/calendar (cadence counts, date continuity, weekday-correctness computed not eyeballed), and SOP (walk each step as the executor). The "check every fact against its source" rule is now scoped to where the document asserts real facts, so placeholder-driven templates aren't flagged.
- **Blocked assumptions**: a gap that needs information, judgment, or a capability the agent lacks (which clip is a "highlight", what's "background" in a photo it can't see) is no longer dressed up as an ordinary decision. It's named as blocked, given an honest fallback, and when it sits under a core requirement the deliverable is flagged *provisional* and raised first at gate 2.
- **Source inputs are read-only (new hard rule)**: the user's photos/footage/data/drafts are never overwritten; derivatives go to a new location, and verification confirms originals are untouched.
- **Future/recurring deliverables**: for a plan/calendar/schedule, "done" means the plan is complete and verified, *not* that the future work happened — said plainly at gate 2 so "all tasks done" isn't mistaken for "it shipped", with an offer to hand dated items to the environment's scheduled tasks.
- **Medium-skill routing**: the Tech Lead now searches for and delegates to a specialized environment skill (e.g. `video-making`) for a non-text medium instead of hand-rolling.
- **Unattended approval gates**: when the user has pre-authorized autonomy and is unreachable, a gate becomes a recorded *provisional approval* to ratify later — not a silently-skipped stop (irreversible/external actions still wait regardless).
- **Doc-set fit for non-prose deliverables**: the finished artifact lives in its own named file (listed in PLAN's index, seen by status.py), a plan/schedule deliverable is never conflated with the skill's own PLAN.md or given task-checkboxes, Phases 2–3 may merge for schedule-shaped work, the Craft Reviewer loads a design skill *appropriate to the medium* rather than `frontend-design` for everything, and OUTLINE.md carries SOP structure (doc control, RACI, exception path, revision history) when the deliverable is a procedure.

**v1.4.0** — fixes for six issues found by stress-testing v1.3 itself.
- **`scripts/status.py` now supports a split plan.** v1.3 told you to split a large plan into `docs/plan/phase-<n>.md` but shipped a status script that still only read a single `docs/PLAN.md`, so a split plan reported nothing. The script now follows the phase-file links from an index `PLAN.md` automatically (`status.py .` just works), and also accepts an explicit plan file as a second argument. Flat single-file plans behave exactly as before.
- **Revert-before-retry now actually has something to revert to.** `references/parallel-execution.md` said to revert a failed worker's Files before redispatch, but in a project without version control there was no pre-task version to revert to. It now says to snapshot each task's Files *before dispatch*, so the clean version still exists when an attempt fails.
- **Scale-tier tie-breaker for a tiny UI.** "A UI makes it medium" and "≤5 tasks is small" contradicted each other for a trivial one-screen page. `references/roles/README.md` and `SKILL.md` now resolve it: a single static screen with no real flow stays small; "a UI makes it medium" means more than one screen or a real flow. The Editor/Craft Reviewer still activates regardless of tier.
- **`status.py` no longer miscounts placeholder ideas.** The template's example bullet (and parenthetical placeholders like `- (none yet)`) were counted as real parked ideas. Bullets whose content starts with `<` or `(` are now skipped.
- **`status.py` wave calculation no longer over-locks.** A *done* task's Files were treated as "in flight" and blocked otherwise-parallelizable tasks that touched the same file. Only *in-progress* (`[~]`) tasks hold their Files now; finished work doesn't lock a wave.
- **Resume guidance: `status.py` is a summary, not the source of truth.** `SKILL.md` Phase 0 now says plainly that the script only reads checkboxes — it can't see that a `[ ]` task is actually built on disk or that a `[x]` task's files are gone — so on resume you read the real files and trust disk over the checkbox when they disagree.
- **Revert-before-retry now applies in every mode.** The revert/snapshot rule had been stated only in `parallel-execution.md` (read only in parallel mode), but a broken half-written file needing a clean revert happens just as readily in a small sequential run. `references/execution-rules.md` (read in every mode) now carries a "Retrying a failed task" rule: start a retry from the task's pre-attempt state, reverting its Files first — checking out the pre-task version under VCS, or restoring from a copy made before starting otherwise.

**v1.3.0**
- Added a new specialist role, **Editor / Craft Reviewer** (`references/roles/editor-craft-reviewer.md`), activated when the result is a UI, a document, or other content a person reads or looks at directly. It judges craft — does this read or look like it was actually finished with care, not just whether it satisfies its requirements — separately from fidelity (Phase 4 Layer 1) and function (Layer 2). For UI work it loads a dedicated visual-design skill where the environment has one rather than inventing design judgment from scratch. Wired into `SKILL.md` Phase 4 as a new Layer 3b and into `references/verification-checklist.md` and `references/roles/README.md`.
- **Security Reviewer now activates retroactively.** Previously it only turned on when the PRD mentioned sensitive data/auth/payments up front. Now, if Phase 4's fidelity check turns up password/token/secret/auth-handling code the PRD never named, the Tech Lead activates Security Reviewer then, rather than letting it stay dormant because nobody flagged it in advance.
- **Local git commits are now part of the per-task loop** (`references/execution-rules.md`): a local commit (never a push) for a task's `Files`, named with the task ID, may happen automatically as part of recording a task — distinct from the existing stop-and-ask rule for `push` and other external actions, which is unchanged.
- **Large plans can be split.** `references/document-set.md` now says when and how: past roughly 60 tasks or more than three Phases, keep `PLAN.md` as a short index and move each phase's tasks into `docs/plan/phase-<n>.md`.
- **Approval gates now record how long they've been waiting.** A `Waiting since:` line on PLAN.md's status (added to `assets/PLAN.template.md`) is set whenever Status is `awaiting-approval` or otherwise stopped on the user, and a resuming agent that finds it old says so explicitly rather than silently re-presenting the same gate as if no time had passed.
- **Failed parallel workers are redispatched onto a clean slate.** `references/parallel-execution.md` now says explicitly: revert a failed worker's `Files` before giving the task to a second attempt, rather than building on top of a half-finished first one.
- Clarified that the **"single writer" rule has a real limit**: it protects against one orchestrator's own workers colliding, not against two independent sessions a person opens against the same project from outside the skill's control. `references/parallel-execution.md` now says what to do if you notice a document doesn't match what you last wrote to it. New stress case `evals/s10-concurrent-agents-same-plan/` exercises this.
- Discovery now asks what language the **deliverable itself** needs to be in (not the conversation) — a new assumption-killer question (S6) in `references/discovery-questions.md`, since this is easy to assume wrong and expensive to retrofit.
- `scripts/status.py` no longer silently drops a malformed task line. A `- [...]` line that looks like a task but fails to parse now prints a `WARNING` (text output) and appears under a new `unparsed_lines` key (`--json`), the same treatment the v1.2 `unknown_deps` fix gave to dangling dependencies.
- `references/document-set.md` and `assets/STRUCTURE.template.md` gained an optional **Module relationships** section for existing-codebase projects: the Tech Lead records which modules call which and what would break the most if changed carelessly, as plain markdown written once while reading the repo — the same kind of thing a generated code-relationship graph gives an agent, without adding any external tool or dependency.
- README gained short **Upgrading** and **Uninstalling** sections.

**v1.2.0**
- Fixed three `scripts/status.py` bugs found by manual stress-testing: a task with no `Files` listed could still be placed in a parallel wave with another task (now always runs alone, since its scope is unknown); an in-progress (`[~]`) task's `Files` were not locked, so a colliding task could still show as "parallelizable now" (now `[~]` files are claimed exactly like `[x]` files); a `Deps` entry naming a task ID that does not exist anywhere in the plan produced no warning, so that task would wait forever (now reported as `WARNING dependency to unknown task` in text output and under `unknown_deps` in `--json`).
- The "stranger test" for acceptance criteria — could someone who has never seen this project verify it without asking the author? — previously ran only once, by the Tech Lead before gate 1, against the tasks as planned. It now also applies to anything an Engineer is tempted to add during execution that the task or its `Accept` line did not name, however small it looks (a `--help` flag, a usage message, an extra validation check). Reinforced in `SKILL.md` Phase 3 and 4, `references/execution-rules.md`, `references/roles/engineer.md`'s Refuses list, and `references/verification-checklist.md`'s result→task trace.
- Phase 1 (Discovery) now checks first whether the target directory already holds a substantial existing project. If so, the Tech Lead reads the repo (stack, how to run it, existing tests, structure, rough size) before the Product Manager picks any question, and discovery asks only what the code cannot answer — intent, scope of touch, done, no-touch zones, and above all whether a bug found along the way may be fixed directly or only reported. See "Working on an existing codebase" in `references/discovery-questions.md` and the updated Inputs in `references/roles/tech-lead.md`.
