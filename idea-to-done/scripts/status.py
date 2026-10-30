#!/usr/bin/env python3
"""Print a progress summary of an idea-to-done project from docs/PLAN.md.

Usage:
    python status.py                 # uses ./docs/PLAN.md
    python status.py path/to/project # uses path/to/project/docs/PLAN.md
    python status.py --json          # machine-readable output

Standard library only. The parser relies on the task format from
assets/PLAN.template.md:

    - [ ] T1.1 Title → R1
      - Deps: T0.1, T0.2
      - Files: src/x/
      - Accept: ...
      - Note: ...
"""
import json
import re
import sys
from pathlib import Path

TASK_RE = re.compile(
    r"^- \[(?P<st>[ x~!])\]\s+(?P<id>[A-Z]+\d+(?:\.\d+)?[a-z]?)\s+(?P<title>.*?)(?:\s+(?:→|->)\s*(?P<trace>.*))?$"
)
# Looks like the start of a task line (any checkbox marker) but failed TASK_RE: a malformed
# task that would otherwise vanish from the count with no warning, same failure shape as an
# unknown Deps entry. Checked whenever a `- [...]` line does not match TASK_RE.
TASK_LOOKS_LIKE_RE = re.compile(r"^- \[.\]")
FIELD_RE = re.compile(r"^\s+- (?P<key>Deps|Files|Accept|Risk|Note):\s*(?P<val>.*)$")
PHASE_RE = re.compile(r"^###\s+(?P<name>.+)$")
STATUS_RE = re.compile(r"^Status:\s*(?P<val>.+)$")

STATUS_NAMES = {" ": "pending", "~": "in_progress", "x": "done", "!": "blocked"}
NO_DEPS = {"—", "-", "none", "None", "n/a"}


def parse_plan(text):
    tasks, phase, status_line, cur = [], None, None, None
    unparsed = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = STATUS_RE.match(line)
        if m and status_line is None:
            status_line = m.group("val").strip()
            continue
        m = PHASE_RE.match(line)
        if m:
            phase, cur = m.group("name").strip(), None
            continue
        m = TASK_RE.match(line)
        if not m and TASK_LOOKS_LIKE_RE.match(line):
            unparsed.append((lineno, line.strip()))
        if m:
            cur = {
                "id": m.group("id"),
                "title": m.group("title").strip(),
                "status": STATUS_NAMES[m.group("st")],
                "trace": [t.strip() for t in (m.group("trace") or "").split(",") if t.strip()],
                "phase": phase,
                "deps": [],
                "files": [],
                "note": "",
            }
            tasks.append(cur)
            continue
        m = FIELD_RE.match(line)
        if m and cur is not None:
            key, val = m.group("key"), m.group("val").strip()
            if key == "Deps":
                cur["deps"] = [d.strip() for d in val.split(",") if d.strip() and d.strip() not in NO_DEPS]
            elif key == "Files":
                cur["files"] = [f.strip() for f in val.split(",") if f.strip()]
            elif key == "Note":
                cur["note"] = val
    return status_line, tasks, unparsed


def known_task_ids(tasks):
    return {t["id"] for t in tasks}


def unknown_deps(tasks):
    """Deps that name a task ID absent from the whole plan: these would wait forever."""
    known = known_task_ids(tasks)
    out = []
    for t in tasks:
        for d in t["deps"]:
            if d not in known:
                out.append((t["id"], d))
    return out


def ready_tasks(tasks):
    """Pending tasks whose deps are all done, in plan order."""
    done = {t["id"] for t in tasks if t["status"] == "done"}
    return [t for t in tasks if t["status"] == "pending" and all(d in done for d in t["deps"])]


def _overlap(a, b):
    a, b = a.rstrip("/"), b.rstrip("/")
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def claimed_files(tasks):
    """Files already owned by work in flight: done and in-progress tasks both hold their Files."""
    claimed = []
    for t in tasks:
        if t["status"] in ("done", "in_progress"):
            claimed.extend(t["files"])
    return claimed


def first_wave(ready, in_flight_files=()):
    """Greedy: ready tasks whose Files do not overlap each other or files already in flight.

    A task with no Files listed has unknown scope and can corrupt any wave it joins
    (nothing says what it might touch), so it never shares a wave with another task;
    it is always alone in its own wave of one.
    """
    wave, claimed = [], list(in_flight_files)
    for t in ready:
        if not t["files"]:
            if not wave:
                wave.append(t)
            break
        if any(_overlap(f, c) for f in t["files"] for c in claimed):
            continue
        wave.append(t)
        claimed.extend(t["files"])
    return wave


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if not a.startswith("--")]
    root = Path(args[0]) if args else Path(".")
    plan = root / "docs" / "PLAN.md"
    if not plan.exists():
        print(f"No plan found at {plan}. Not an idea-to-done project, or docs live elsewhere.", file=sys.stderr)
        return 1

    status_line, tasks, unparsed = parse_plan(plan.read_text(encoding="utf-8"))
    counts = {k: 0 for k in STATUS_NAMES.values()}
    for t in tasks:
        counts[t["status"]] += 1
    ready = ready_tasks(tasks)
    wave = first_wave(ready, in_flight_files=claimed_files(tasks))
    untraced = [t for t in tasks if not t["trace"]]
    bad_deps = unknown_deps(tasks)
    docs = sorted(p.name for p in (root / "docs").glob("*.md"))
    ideas = root / "docs" / "IDEAS.md"
    n_ideas = (
        sum(1 for l in ideas.read_text(encoding="utf-8").splitlines() if l.startswith("- ") and "<idea>" not in l)
        if ideas.exists() else 0
    )

    if as_json:
        print(json.dumps({
            "status": status_line, "counts": counts, "total": len(tasks),
            "ready": [t["id"] for t in ready], "first_wave": [t["id"] for t in wave],
            "blocked": [t["id"] for t in tasks if t["status"] == "blocked"],
            "in_progress": [t["id"] for t in tasks if t["status"] == "in_progress"],
            "untraced": [t["id"] for t in untraced], "docs": docs, "ideas_parked": n_ideas,
            "unknown_deps": [{"task": tid, "missing_dep": d} for tid, d in bad_deps],
            "unparsed_lines": [{"line": n, "text": t} for n, t in unparsed],
        }, indent=2, ensure_ascii=False))
        return 0

    total = len(tasks)
    print(f"Plan: {plan}")
    print(f"Status: {status_line or '(no status line)'}")
    print(f"Tasks: {counts['done']}/{total} done · {counts['in_progress']} in progress · "
          f"{counts['blocked']} blocked · {counts['pending']} pending")
    for t in tasks:
        if t["status"] == "in_progress":
            print(f"In progress: {t['id']} {t['title']}")
    for t in tasks:
        if t["status"] == "blocked":
            print(f"Blocked: {t['id']} {t['title']}" + (f" — {t['note']}" if t["note"] else ""))
    if ready:
        print("Ready (deps satisfied): " + ", ".join(t["id"] for t in ready))
        if len(wave) > 1:
            print("Parallelizable now (no file overlap): " + ", ".join(t["id"] for t in wave))
        nxt = ready[0]
        print(f"Next: {nxt['id']} {nxt['title']}" + (f" → {', '.join(nxt['trace'])}" if nxt["trace"] else ""))
    elif counts["pending"]:
        print("No task is ready: every pending task waits on a dependency that is not done.")
    elif total and counts["done"] == total:
        print("All tasks done. Next: Phase 4 verification (or approval gate 2 if VERIFICATION.md is complete).")
    if untraced:
        print("WARNING untraced tasks (no → R-item): " + ", ".join(t["id"] for t in untraced))
    for tid, dep in bad_deps:
        print(f"WARNING dependency to unknown task: {tid} depends on {dep} (does not exist)")
    for lineno, text in unparsed:
        print(f"WARNING line {lineno} looks like a task but did not parse, and is not counted: {text}")
    print(f"Docs: {', '.join(docs) if docs else '(none)'} · Ideas parked: {n_ideas}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
