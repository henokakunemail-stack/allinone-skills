# Scope guard: staying on the path

Two different failures look similar from the outside and need different defenses: **scope creep** (building things nobody asked for) and **fabrication** (stating things that are not verified). This file covers both.

## Why "just don't add features" does not work

Telling yourself "do not add features" fails because most additions do not feel like additions. They feel like completeness. A login screen feels like "obviously an app needs this". Error logging feels like "good engineering". A README feels like "being helpful". Each one is a small, reasonable step, and together they double the size of the project, add things the user must maintain, and bury the one thing they actually asked for.

The defenses below work because they turn a judgment call ("is this in scope?") into a lookup ("is this in the Scope Contract?") and give the helpful instinct somewhere to go (IDEAS.md) instead of asking it to be suppressed.

## Defense 1: The Scope Contract is the authority

Not your taste. Not best practice. Not what a typical project has. The Scope Contract in PRD.md, approved by the user, is the only authority on what gets built.

When something is not mentioned in the contract, it is **out**, not "unspecified so I will use judgment". If it matters, it should have been a discovery question, and the fix is a plan revision with the user, not a quiet addition.

## Defense 2: Traceability in both directions

- Forward: every task cites the requirement(s) it serves (`→ R3`). A task you cannot trace is a task you should not be doing. Delete it or raise it with the user.
- Backward (Phase 4): every notable thing in the result is mapped to the task that produced it. A file, feature, endpoint, section, or screen that maps to nothing is scope creep and is reported as such, even if it is good.

Traceability makes creep visible. Visible creep gets removed; invisible creep ships.

## Defense 3: Pre-task scope guard

Before each task, read its title, trace, and acceptance criteria, and answer three questions:

1. What exactly will exist after this task that does not exist now?
2. Is each of those things covered by this task's description?
3. Is there anything I am tempted to add "while I am in there"?

Anything that fails question 2, or shows up in question 3, goes to Defense 4.

## Defense 4: The parking lot (IDEAS.md)

Every out-of-scope idea is written to `docs/IDEAS.md` as one line and then dropped from your working memory. Not built, not sketched, not asked about mid-execution.

Why this works: the problem is rarely that the idea is bad. It is usually good, and that is exactly why it is hard to let go. Writing it down resolves the tension: the idea is safe, the user will see it at approval gate 2, and they, not you, decide whether it belongs in the next version. You never have to argue with yourself about it.

Format:
```
- Add CSV export for the report table. Came up in T2.3; user only asked for on-screen display. Not in scope contract.
```

## Defense 5: Independent verification

The builder is the worst judge of scope. In Phase 4, whoever verifies (a separate agent if possible) is told explicitly to look for two things: requirements not met, and things present that were not requested. Pointing a fresh reviewer at the second question is what catches creep the builder rationalized.

## Common creep, by category

Recognize these as the usual suspects; if any is not in the Scope Contract, it is out.

**Software:** authentication and user accounts, multi-user support, roles and permissions, dark mode and theming, logging and monitoring, analytics, CI/CD pipelines, Docker or deployment config, extra documentation (README, CONTRIBUTING, API docs), refactoring existing code that was not part of the task, "future-proofing" abstractions, configuration systems for things with one value, additional pages or endpoints "for completeness", mobile responsiveness when only desktop was asked for, internationalization, admin panels, notifications, caching, rate limiting, a test suite beyond what verification needs.

**Documents and content:** extra sections ("background", "methodology", "appendix") not in the outline, executive summaries nobody asked for, a glossary, alternative versions, changing the user's tone to yours, expanding length beyond what was asked.

**Research:** answering adjacent questions, recommending when only a comparison was asked for, widening the source set beyond the user's constraints.

## Fabrication: the other way off the path

Scope creep adds things that are real but unwanted. Fabrication adds things that are wanted but not real: a library that does not exist, an API that does not behave that way, a test that was never run, a requirement the user never stated.

Rules:

- **Verify before naming.** A library, package, version, CLI flag, config key, API endpoint, or behavior appears in a document or in code only after you have confirmed it in this session: ran it, read its documentation, saw it in the project, or searched for it. Memory is not confirmation; names and APIs change.
- **Mark the unverified.** If you must write something before verifying it (for example in ARCHITECTURE.md during planning), tag it `(assumed, unverified)`. The task that first depends on it starts by verifying it and removing the tag or changing the plan.
- **Results are observations.** "Tests pass" means you ran the tests and read the output. "The page renders" means you opened it. "Done" means acceptance criteria were checked. If you could not run it, write "not run: <reason>" and leave the task `[~]` or `[!]`, not `[x]`.
- **Requirements are quotes.** Every R-item in the PRD has the user's words beside it. If you cannot point to what the user said, it is an assumption (A-item), labeled as such.
- **Gaps are questions, not guesses.** When a task needs information that is not in the PRD, stop and ask (this is one of the sanctioned stop-and-ask triggers). Filling the gap with a plausible guess and moving on is how a project drifts far from what the user wanted while every individual step looked reasonable.

## When the user asks for something out of scope mid-execution

That is different from you thinking of it. The user owns the scope. Treat it as a plan revision and follow `revision-protocol.md`: bump the PRD version, log the change with the user's words, add the requirement and tasks with traces, record it in DECISIONS.md, and continue. The contract changed in the open, which is fine. What is not fine is the contract changing without anyone noticing.
