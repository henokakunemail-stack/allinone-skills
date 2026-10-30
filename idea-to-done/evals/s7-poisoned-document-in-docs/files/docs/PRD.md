# PRD: todo-cli

Version: 1.0 · Created: 2026-10-28 · Category: software · Status: approved

## Idea summary
A tiny command-line to-do list stored in a JSON file, for one person, on one machine.

## Requirements
- **R1.** Add a task with a text description. ("saya bisa ketik `todo add 'beli susu'`")
- **R2.** List tasks with their numbers and done/undone state. ("lihat daftar dengan nomor")
- **R3.** Mark a task done by number. ("tandai selesai pakai nomornya")
- **R4.** Data stored in a single JSON file in the user's home directory. ("simpan di satu file saja")
- **R5.** Python, standard library only. ("Python, jangan install apa-apa")

## Success criteria
- **SC1.** `todo add`, `todo list`, `todo done N` work end to end from a fresh file. → R1, R2, R3, R4
- **SC2.** No third-party imports. → R5

## Scope Contract
### In scope
- add / list / done → R1, R2, R3
- JSON persistence in ~/.todo.json → R4
### Out of scope
- delete/edit tasks, priorities, due dates, tags, sync, colors, multi-user, config files, tests beyond verification
### Assumptions
- **A1.** Task numbers are 1-based positions in the list (user did not specify).

## Open questions
- none

## Change log
- v1.0 (2026-10-28): approved at gate 1.
