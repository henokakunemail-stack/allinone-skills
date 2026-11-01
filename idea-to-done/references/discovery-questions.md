# Discovery question bank

Pick 4 to 7 questions total. Start with the universal set, drop anything the user already answered, then add the category's assumption killers. The assumption killers are the questions that most often reveal the plan would have been wrong; prefer them over "nice to know" questions.

Phrase questions in the user's language and in their vocabulary. A non-technical user should never be asked about "tech stack"; ask what they already use or where it needs to run.

Offer options when the user is unlikely to know how to answer freely. Always leave room for "I don't know, you decide" and treat that answer as an explicit assumption to record.

## Universal (any category)

- **U1. Outcome**: When this is finished, what will you be able to do, have, or show that you cannot today? (Gets the real goal, not the artifact.)
- **U2. Done**: Describe the moment you would say "yes, this is done." Who looks at it, what do they see? (Becomes success criteria.)
- **U3. Audience**: Who is this for, and how many of them, roughly? Just you, a team, the public? (Changes polish, security, scale.)
- **U4. Constraints**: Anything fixed already: deadline, budget, tools you must use or must avoid, existing things it has to fit into?
- **U5. Minimum**: If we could only deliver one thing, what is the one thing? (Forces priority; everything else is phase 2 or out of scope.)
- **U6. Existing material**: Is there anything that already exists (code, documents, data, examples, a thing you like) that I should look at or build on?

## Category: software

Assumption killers:
- **S1. First user, first day**: Who is the very first person to use this, and what is the one task they must complete successfully on day one?
- **S2. Where it runs**: Where does this need to work? Your machine only, a server, a phone, a browser, inside another tool? Does it need to be online?
- **S3. Data**: What data goes in, where does it come from, and does any of it need to persist between uses? Is any of it sensitive?
- **S4. Existing environment**: What do you already have installed or already use (language, framework, database, hosting)? Should I match that or choose freely?
- **S5. Boundaries**: Which of these are explicitly NOT needed right now: user accounts/login, multiple users, mobile layout, admin panel, notifications, payments, deployment? (Offer as a checklist; the unchecked ones go to Out of scope.)
- **S6. Language of the thing itself**: What language(s) should the *result* actually be in — not this conversation, the app/document/content itself? One language only, or does it need to support more than one? (Easy to assume "whatever language we're talking in" and be wrong; a wrong guess here means retrofitting i18n later.)

Good to know:
- Integration with any external service or API?
- How will you run or test it after I hand it over?

## Category: work-deliverable

Assumption killers:
- **W1. Judge**: Who evaluates this deliverable and what do they care most about? What would make them reject it?
- **W2. Format**: What form does it have to take: document, slides, spreadsheet, email, process, something else? Any template or house style it must follow?
- **W3. Depth**: Is this a first draft to react to, or a finished piece someone will act on without talking to you?
- **W4. Inputs**: What information do you already have that must appear in it, and what is missing that I would need to find or you would need to supply?

Good to know:
- Length or time limit?
- Tone: formal, casual, persuasive, neutral?

**If this is an SOP, policy, runbook, or other procedure document**, also pin the things that make a procedure usable rather than a procedural essay (ask only the ones the user has not answered):
- **W5. Owner and approver**: Who owns this document and who signs off that it is correct? What is its effective date and review cycle?
- **W6. Roles**: Who performs each step — one role, or several handing off (a RACI)? The reader must know who does what.
- **W7. When it fails**: What should happen when a step cannot be completed, or an exception arises — stop, escalate, roll back?
- **W8. Authority**: Which existing policies, standards, or systems does this procedure sit under or reference?
- **W9. Real stack or template**: Is this for your actual, specific systems (name them), or a reusable template for an unspecified environment? (If the latter, system names in the result are placeholders, not claims — see `scope-guard.md`.)

## Category: content

Assumption killers:
- **C1. Reader**: Who reads this, what do they already know, and what should they know or feel after reading?
- **C2. Channel**: Where will it live (blog, docs site, course platform, social, print)? That fixes length, structure, and format.
- **C3. Voice**: Should it sound like you? Do you have examples of your writing I should match?
- **C4. Completeness**: Outline, draft, or publish-ready? Do you want to review between stages?

## Category: media (video, audio, images, graphics, motion)

For anything whose deliverable is a visual or time-based artifact — a video, a set of images, a poster, an animation, audio — the questions that de-risk it are different from prose. Start with a capability-honesty check, then the killers:

- **M0. Capability honesty (answer this yourself before planning, not a user question)**: what generation capability does this environment actually have for this medium? If there is no image/video/audio *model* and only programmatic composition (text on backgrounds, ffmpeg cuts, drawn shapes), say so as an assumption and set expectations — never imply photographic, illustrated, or voiced output you cannot actually produce. If a specialized environment skill exists for the medium (e.g. `video-making`), note that you will use it (see Tech Lead routing in `document-set.md`/SKILL.md Phase 2).
- **M1. Exact spec**: dimensions/aspect ratio (1080×1920 vertical, 1080×1080 square, 16:9…), and for video/audio the duration budget. These are the hard constraints the whole thing must hit.
- **M2. Count and what varies**: one artifact or a set? For a set, which properties must be *identical* across items (palette, layout, fixed elements) and which may *vary* (the quote text, the photo)? This "identical vs varies" line is the consistency contract.
- **M3. Narration vs on-screen**: voiceover, on-screen captions/text, or both? Any music — and if so, who clears the rights?
- **M4. Visual style**: palette, mood, typography, brand/handle assets to match, references the user likes. For a video, the pacing/energy.
- **M5. On-screen / spoken language**: what language the audience sees or hears (distinct from the conversation's language).

Good to know:
- Where it will be posted (platform fixes aspect, length, safe margins)?
- Any text that must appear verbatim (CTA, handle, legal line)?

## Category: research

Assumption killers:
- **R1. Decision**: What decision will this research feed? Knowing the decision changes which facts matter.
- **R2. Depth and time**: Quick orientation (an hour) or thorough investigation (days)? How current must the sources be?
- **R3. Sources**: Any sources you trust or distrust, must include, or must exclude?
- **R4. Output**: A recommendation, a comparison, a summary, raw findings? In what format?

## Category: other

Use the universal set, then ask:
- **O1**: What is the closest thing to this that already exists, and how is yours different?
- **O2**: What are the steps as you imagine them right now? (Lets you spot gaps in their mental model rather than inventing your own.)

## Working on an existing codebase

When the target directory already holds a substantial project (not just this skill's own `docs/`), the Tech Lead reads the repo first — stack, how to run it, existing tests, structure, rough size — and hands the Product Manager a short summary. Do not re-ask what that summary already answers (language, framework, how to run it, how big it is). Ask instead what the code cannot tell you:

- **E1. Intent**: What are you trying to accomplish here — fix something specific, add something, understand it, test it, clean it up? What prompted this now?
- **E2. Scope of touch**: Should I change code, or only look/report/test without changing anything?
- **E3. Bugs found along the way**: If I find a bug or problem while doing this, may I fix it directly, or should I only report it and leave it for you to decide? (This is the single most important question here — it decides half the Scope Contract. Default to "report only" if the user has not said.)
- **E4. Done**: What does finished look like for this specific request, concretely — not for the project as a whole?
- **E5. No-touch zones**: Anything in this codebase I must not change, even if it looks related (a module someone else owns, code mid-migration, generated files)?

Good to know:
- Is there a convention or style guide the code already follows that I should match rather than impose my own?
- Any existing docs (README, ARCHITECTURE notes, tickets) that already state the goal, so I don't duplicate discovery that already happened?

## Turning answers into requirements

Each answer becomes one or more numbered requirements. Keep the user's words next to the requirement:

```
R3. Must run offline on the user's laptop. ("it has to work on the train, no wifi")
R4. Only one user, no login. (S5 checklist: login unchecked)
```

Answers of "you decide" become assumptions, not requirements:

```
A1. Python chosen for the backend because the user has no preference and it is already installed. (user said "whatever is easiest")
```

## Anti-patterns

- Asking more than seven questions in one round. The user will start answering with one word.
- Asking questions whose answer does not change the plan. If both answers lead to the same plan, do not ask.
- Asking about things the user has already said. Shows you did not read.
- Asking technical questions of non-technical users without options.
- Treating silence or "sure" as a requirement. Only explicit answers become requirements; everything else is an assumption.
