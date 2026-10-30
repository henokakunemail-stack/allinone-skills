---
type: llm
focus: trace
weight: 1
---

At least one of the two agent transcripts shows awareness that something else changed docs/PLAN.md or todo.py concurrently (an unexpected diff before a write, a note about re-reading PLAN.md and finding it different from what it last wrote, a git conflict surfaced) — evidence that the collision was not simply invisible to both agents the whole time. (If the environment happened to serialize the two agents' writes perfectly by accident and neither ever saw a collision, mark this n/a rather than fail, and say so explicitly — this grader is about detection capability being exercised, not about forcing a collision that didn't occur.)
