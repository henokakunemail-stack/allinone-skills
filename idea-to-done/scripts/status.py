#!/usr/bin/env python3
"""Print a progress summary of an idea-to-done project from docs/PLAN.md.

Usage:
    python status.py                      # uses ./docs/PLAN.md
    python status.py path/to/project      # uses path/to/project/docs/PLAN.md
    python status.py path/to/project FILE # scan one explicit plan file (e.g. a split phase file)
    python status.py --json               # machine-readable output

Standard library only. The parser relies on the task format from
assets/PLAN.template.md:

    - [ ] T1.1 Title → R1
      - Deps: T0.1, T0.2
      - Files: src/x/
      - Accept: ...
      - Note: ...

A large plan may be split (see references/document-set.md "Splitting a large plan"):
PLAN.md becomes a short index and each phase's tasks move into docs/plan/phase-<n>.md.
When PLAN.md holds no task lines of its own but links to such phase files, this script
follows those links and scans them in order, so `python status.py .` keeps working
against a split plan. A second argument points it at one plan file explicitly instead.
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
        # Tolerate markdown bold around the ID/title (e.g. `- [x] **T1.1** Title` or
        # `- [x] **T1.1 Title**`): bold markers carry no meaning for parsing, so probe a
        # copy with them stripped. The original line is kept for field extraction below.
        probe = line.replace("**", "") if "**" in line else line
        m = TASK_RE.match(probe)
        if not m and TASK_LOOKS_LIKE_RE.match(probe):
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


# Markdown links to split phase files, e.g. [Phase 2](plan/phase-2.md) or a bare
# docs/plan/phase-2.md written inline. Matches a relative path ending in .md inside a
# plan/ directory. Used only when PLAN.md itself holds no task lines.
PHASE_LINK_RE = re.compile(r"\(?\b((?:docs/)?plan/[^()\s]+\.md)\)?")


def phase_files_from_index(plan_path, text):
    """Ordered, de-duplicated list of existing split phase files linked from an index PLAN.md.

    Link paths may be written relative to docs/ (plan/phase-1.md) or to the project root
    (docs/plan/phase-1.md); both resolve to the same file under the plan's own docs/ dir.
    """
    docs_dir = plan_path.parent
    seen, found = set(), []
    for m in PHASE_LINK_RE.finditer(text):
        rel = m.group(1)
        rel = rel[len("docs/"):] if rel.startswith("docs/") else rel
        cand = (docs_dir / rel).resolve()
        if cand == plan_path.resolve() or cand in seen:
            continue
        if cand.exists():
            seen.add(cand)
            found.append(cand)
    return found


def load_plan_text(plan_path):
    """Return (combined_text, sources).

    If PLAN.md has task lines of its own, use it unchanged (flat plan, original behaviour).
    Otherwise, if it is an index linking to split phase files, concatenate the index's own
    header (for its Status line) with each phase file's body, in link order, so the rest of
    the parser is unaffected.
    """
    text = plan_path.read_text(encoding="utf-8")
    if any(TASK_RE.match(line.replace("**", "")) for line in text.splitlines()):
        return text, [plan_path]
    phase_files = phase_files_from_index(plan_path, text)
    if not phase_files:
        return text, [plan_path]
    parts = [text] + [pf.read_text(encoding="utf-8") for pf in phase_files]
    return "\n".join(parts), [plan_path] + phase_files


def count_ideas(ideas_path):
    """Count real parked ideas in IDEAS.md, skipping template placeholder bullets.

    The shipped template seeds an example bullet (`- <idea>. Came up in T<n>...`), and
    agents sometimes leave a parenthetical placeholder like `- (none yet)`. Neither is a
    real idea, so a bullet whose content starts with `<` or `(` is not counted.
    """
    if not ideas_path.exists():
        return 0
    n = 0
    for l in ideas_path.read_text(encoding="utf-8").splitlines():
        if not l.startswith("- "):
            continue
        content = l[2:].lstrip()
        if content.startswith("<") or content.startswith("("):
            continue
        n += 1
    return n


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
    """Files owned by work actually in flight right now: only in-progress (`[~]`) tasks.

    A done (`[x]`) task is finished and nobody is writing its Files any more, so those
    files should not lock a new wave — holding them only under-reports what can run in
    parallel. Only `[~]` work genuinely conflicts with a fresh task that shares its Files.
    """
    claimed = []
    for t in tasks:
        if t["status"] == "in_progress":
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
    # Convenience: if the first argument is itself a plan file (ends in .md and exists,
    # e.g. `status.py docs/PLAN.md` or a split phase file), treat it as the explicit plan
    # rather than a project dir — otherwise it was read as a root and looked for
    # <file>/docs/PLAN.md, a confusing papercut on resume.
    if args and args[0].endswith(".md") and Path(args[0]).is_file():
        args = [str(Path(args[0]).parent.parent), args[0]]
    root = Path(args[0]) if args else Path(".")
    explicit = Path(args[1]) if len(args) > 1 else None

    if explicit is not None:
        # Point at one plan file directly (e.g. a single split phase file). Accept an
        # absolute/cwd-relative path, or one relative to the project root.
        plan = explicit if explicit.is_absolute() or explicit.exists() else (root / explicit)
        if not plan.exists():
            print(f"No plan file at {plan}.", file=sys.stderr)
            return 1
        plan_text, sources = plan.read_text(encoding="utf-8"), [plan]
    else:
        plan = root / "docs" / "PLAN.md"
        if not plan.exists():
            print(f"No plan found at {plan}. Not an idea-to-done project, or docs live elsewhere.", file=sys.stderr)
            return 1
        plan_text, sources = load_plan_text(plan)

    status_line, tasks, unparsed = parse_plan(plan_text)
    counts = {k: 0 for k in STATUS_NAMES.values()}
    for t in tasks:
        counts[t["status"]] += 1
    ready = ready_tasks(tasks)
    wave = first_wave(ready, in_flight_files=claimed_files(tasks))
    untraced = [t for t in tasks if not t["trace"]]
    bad_deps = unknown_deps(tasks)
    docs = sorted(p.name for p in (root / "docs").glob("*.md"))
    ideas = root / "docs" / "IDEAS.md"
    n_ideas = count_ideas(ideas)

    if as_json:
        print(json.dumps({
            "status": status_line, "counts": counts, "total": len(tasks),
            "ready": [t["id"] for t in ready], "first_wave": [t["id"] for t in wave],
            "blocked": [t["id"] for t in tasks if t["status"] == "blocked"],
            "in_progress": [t["id"] for t in tasks if t["status"] == "in_progress"],
            "untraced": [t["id"] for t in untraced], "docs": docs, "ideas_parked": n_ideas,
            "unknown_deps": [{"task": tid, "missing_dep": d} for tid, d in bad_deps],
            "unparsed_lines": [{"line": n, "text": t} for n, t in unparsed],
            "sources": [str(s) for s in sources],
        }, indent=2, ensure_ascii=False))
        return 0

    total = len(tasks)
    if len(sources) > 1:
        print(f"Plan: {plan} (index) + {len(sources) - 1} phase files")
    else:
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
