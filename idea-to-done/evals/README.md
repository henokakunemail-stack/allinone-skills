# Evals

Two sets live here, all in the `claude plugin eval` layout (`prompt.md`, `case.yaml`, `graders/`, optional `files/` + `place-files.sh`).

**Core set** (does the skill do what it says?):
`soft-yes-becomes-assumption`, `scope-creep-bait`, `resume-existing-plan`, `prompt-injection-in-data`.

**Stress set `s1`-`s9`** (where might the algorithm itself be wrong?). Each case attacks one assumption:

| Case | Suspected flaw it probes |
|---|---|
| s1-contradictory-requirements | Discovery turns answers into requirements mechanically; no step checks answers against each other |
| s2-scope-change-mid-flight | Revision protocol must also move items between In/Out of scope, not only add an R-item |
| s3-existing-codebase-e2e | Flow is idea-first; no "read the repo first" branch; risk of fixing instead of reporting |
| s4-vague-success-criteria | Stranger test is applied to Accept lines, but vague *requirements* may slip in upstream |
| s5-non-software-proposal | Rules and verification lean toward code; document QA may be shallow |
| s6-tiny-task-overkill | Over-application: ceremony on a trivial task despite the description |
| s7-poisoned-document-in-docs | docs/ is declared the source of truth, so a poisoned doc is trusted by construction |
| s8-stale-in-progress-and-drifted-docs | Resume trusts the file state; half-done `[~]` work and drifted docs |
| s9-irreversible-action-unattended | Stop-and-ask rules assume a user who can answer; behavior when nobody can |
| s10-concurrent-agents-same-plan | "Single writer" (parallel-execution.md) assumes one orchestrator controlling its own workers; untested against two independent top-level sessions opened by a person against the same `docs/` |
