# Verification

## Round 1 — <date>

Verifier: fresh agent | QA mode (checklist written before reading implementation)
Scope: <what was verified>

### Requirement → evidence

| Item | How checked | Observed | Result |
|---|---|---|---|
| R1 | <command / action> | <output / observation> | pass / fail (V<n>) |
| SC1 | <command / action> | <output / observation> | pass / fail |

### Result → task trace

| Thing in the result | Produced by | Note |
|---|---|---|
| <file / feature / section> | T<n> | |
| <file / feature / section> | — | **Scope creep**: not traceable to any task |

### Document accuracy

- STRUCTURE.md vs tree: match | mismatch (V<n>)
- ARCHITECTURE.md vs code: match | mismatch (V<n>)
- DESIGN.md vs screens: match | mismatch | n/a
- DECISIONS.md vs what was built: match | mismatch

### Functional tests

- <test>: ran `<command>` → <output>. pass / fail
- <flow>: <steps taken> → <observed>. pass / fail

### Edge cases

- Empty input: <what was done> → <what happened>. pass / fail
- Malformed input: ...
- Second run: ...
- Dependency unavailable: ...
- Security hygiene: ...
- Not applicable: <items skipped and why>

### Issues

#### V1. <title>
- Severity: high | medium | low
- Found in: Layer <n>, <item>
- Repro: <exact steps / command and observed result>
- Expected: <what should happen> (R<n>)
- Fix: F1

### Capability ladder (media deliverables — surfaced at gate 2)

<Only when the deliverable's quality depended on a generation capability (see media-capability.md). Lead gate 2 with this when the target tier wasn't reached.>

- Target tier: <A composed / A+ motion-graphics / B local model / C hosted generative>
- Delivered tier: <what was actually produced>
- Gap: <none / capability gap / authorization gap (available but not authorized)>
- One thing to enable to reach target: <connector / install / authorization + est. cost & cap>
- Provisional? <yes/no>

### Accepted limitations

- <limitation> — reason: <why not fixing now; user agreed on <date>>

## Round 2 — <date>
<Re-verification after fixes. Only the affected parts.>
