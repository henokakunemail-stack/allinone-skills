---
type: llm
focus: trace
weight: 1
---

docs/PLAN.md, after both agents finish or stop, parses cleanly as one plan: no duplicated task IDs (e.g. two different T2.1 blocks with different content), no half-written task block (a `- [ ]` line with no closing fields before the next task starts), and status.py run against it does not crash or report corruption.
