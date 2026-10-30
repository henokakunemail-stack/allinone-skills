# idea-to-done

An [Agent Skill](https://agentskills.io) (v1.1) that takes a raw idea through five disciplined phases:

0. **Orientation** — resume from `docs/PLAN.md` if the project already exists
1. **Discovery** — 4 to 7 targeted questions, one round, answers become numbered requirements
2. **Planning** — `PRD.md` with a Scope Contract, `PLAN.md` with traceable tasks, plus `ARCHITECTURE.md` / `DESIGN.md` / `OUTLINE.md` when the project needs them → **approval**
3. **Execution** — task by task, or in parallel waves of workers when the agent supports it; each task verified and recorded; out-of-scope ideas parked in `IDEAS.md`
4. **Verification** — whole-system testing by a fresh agent (or QA mode), issues become fix tasks → **approval**

The work is organized like a small office. Five core roles (Product Manager, Tech Lead, Engineering Manager, Engineer, QA Engineer) and five specialists activated only when the scope needs them (UI/UX Designer, Technical Writer, Researcher, Security Reviewer, DevOps). Each role is a mandate with refusals and an artifact, never a rubber stamp; roles talk only through `docs/`. A scale rule decides whether roles run as separate agents or as hats worn by one agent.

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
