# Structure: <project name>

Updated: <date> · Must match the real tree; updated in the same task that changes files.

```
<project>/
├── docs/            Project documents (this folder)
├── src/             <responsibility>
│   ├── <file>       <responsibility>
│   └── <folder>/    <responsibility>
├── tests/           <responsibility>
└── <file>           <responsibility>
```

## Conventions

- <naming, where new things go, anything a contributor must know to place a file correctly>

## Module relationships (existing codebase only)

<Only when this project started from an existing codebase. A handful of plain lines on which modules call which and what would break the most if changed carelessly — not a diagram, not a full call graph. Delete this section entirely on a from-scratch project.>

- <module A> calls <module B> for <reason>
- <module C> is depended on by <module D, module E> — changing its interface touches both
