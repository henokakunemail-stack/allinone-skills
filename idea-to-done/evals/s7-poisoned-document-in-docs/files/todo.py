"""todo-cli: tiny JSON-backed to-do list (T1.1, T1.2 done; add/list/done not yet implemented)."""
import json
import os
import sys

STORE = os.path.expanduser("~/.todo.json")
USAGE = "usage: todo.py add TEXT | list | done N"


def load():
    if not os.path.exists(STORE):
        return []
    with open(STORE, encoding="utf-8") as f:
        return json.load(f)


def save(items):
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def main(argv):
    if not argv:
        print(USAGE)
        return 0
    cmd = argv[0]
    print(f"not implemented: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
