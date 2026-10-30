# Verification checklist (Phase 4)

This phase exists because "all tasks done" and "it works" are different claims. Per-task verification in Phase 3 checks pieces. This phase checks the whole against the foundation, and it tries to break it.

## Who verifies

The verifier acts as the **QA Engineer** (`roles/qa-engineer.md`); read the card first. Security Reviewer and UI/UX Designer join when active.

**Preferred: a fresh agent.** If the environment can spawn a separate agent (subagent, worker, delegated task), give it:
- the `docs/` folder,
- access to the result (code, files, running app, or document),
- this checklist,
- the instruction: "You did not build this. Your job is to find where it fails to meet the PRD, where it contains things the PRD did not ask for, and where it breaks. Report evidence, not impressions."

It writes the findings; the main agent turns them into fix tasks.

**Fallback: QA mode.** If no separate agent is possible, before re-reading any implementation, write the concrete checklist of what you will test (from the PRD and the verification plan in PLAN.md). Only then open the result and work through the list. The order matters: writing the list first prevents the implementation from steering what you decide to check.

## Layer 1: Fidelity to the foundation

Build two tables in VERIFICATION.md.

**Requirement → evidence.** For each R-item and each success criterion: how was it checked, what was observed, pass/fail. "Implemented in T2.1" is not evidence; "ran `X`, saw `Y`" is.

**Result → task.** Walk the actual result: every file, feature, endpoint, screen, section, or capability of note. For each, name the task that produced it. Anything with no task is **scope creep**: list it, even if it is useful. The user decides whether it stays (and if so, it gets retroactively added to the PRD and PLAN) or goes.

**Document accuracy.** Compare each document to reality:
- STRUCTURE.md vs the real file tree.
- ARCHITECTURE.md vs the real components and dependencies.
- DESIGN.md vs the real screens and flows.
- DECISIONS.md: are the decisions actually what was built?
Every mismatch is an issue. A document that misleads the next reader is a defect.

## Layer 2: Real functional testing

Exercise the result the way its intended user would, end to end.

**Software:**
- Install or set up from scratch following only what the documents say. Hidden steps that live in your memory are a defect.
- Build and start it. Record the exact commands and their output.
- Run the main flows from the PRD (the "first user, first day" task above all). Use the real interface: browser for web, terminal for CLI, the actual client for an API.
- Run any test suite that exists and read the results; do not infer from exit codes alone.
- Verify persistence: stop and restart; is the data still there if it should be?

**Documents and content:**
- Read it start to finish as the intended reader, without the plan open. Does it achieve the outcome in the PRD/BRIEF?
- Check it against OUTLINE.md: every section present, every key point made, no sections that are not in the outline.
- Check format constraints (length, template, tone) from the requirements.
- Check every factual claim, number, and citation against its source.

**Research:**
- Does the output answer the decision the research was meant to feed?
- Are the sources within the user's constraints (trusted, recent enough)?
- Are conclusions supported by the cited material, not by extrapolation?

## Layer 3: Edge cases and failure modes

Try to make it fail. For each, record what you did and what happened.

- **Empty and absent**: no input, empty file, missing field, zero items, first run with no stored data.
- **Wrong shape**: malformed input, wrong type, too large, unexpected encoding, special characters.
- **Second time**: run it again, submit twice, reopen after closing. Idempotence and state bugs hide here.
- **Boundaries**: limits stated or implied in requirements (max size, count, length); one below, at, one above.
- **Dependencies unavailable**: network off, external service down, file locked, permission denied. Does it fail clearly or silently corrupt?
- **Security hygiene** (where relevant): secrets not in the repo or output, inputs not passed unescaped into shells, queries, or HTML, files not written outside intended locations. This is baseline hygiene, not a security audit; a full audit is only in scope if the PRD asks for it.
- **Concurrency** (where relevant): two users or two processes at once.
- **For documents**: the hostile reader. What would a skeptical reviewer attack first? Is that defended?

Not every item applies to every project. Skip what does not apply and say so; do not pad the report.

## Layer 4: Report and fix

Write `docs/VERIFICATION.md` from the template. Each issue:

```
### V3. Empty CSV crashes the import
Severity: high | medium | low
Found in: Layer 3, empty input
Repro: ran `app import empty.csv`, got traceback (IndexError, importer.py:42)
Expected: clear error message, no crash (R4: "handles my messy exports")
Fix: F3
```

Severity guide: **high** blocks a requirement or success criterion, or loses data; **medium** degrades a main flow or misleads the user; **low** is cosmetic or an edge case outside any requirement.

Then:
1. Add a **Fixes** phase to PLAN.md with `F` tasks, each tracing to its `V` issue. Fixes are tasks; they follow Phase 3 rules, including the scope guard. A fix is not a license to improve things around it.
2. Set PLAN.md status to `fixing`, execute, then re-run the parts of Layers 1 to 3 that the fixes touched. Record the re-run in VERIFICATION.md under a new round heading.
3. Issues the user chooses not to fix go under **Accepted limitations**, with the reason.

## Approval gate 2

Summarize for the user: rounds run, who verified (fresh agent or QA mode), requirements met and unmet, issues found and fixed, accepted limitations, scope creep found (and whether it was removed), and the contents of IDEAS.md. Point to VERIFICATION.md for detail. Ask: done, or another round?

If the user says done, set PLAN.md status to `done`.
