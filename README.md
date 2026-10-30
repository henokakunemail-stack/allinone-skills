# allinone-skills

**Stop your AI coding agent from hallucinating features and APIs you never asked for.**

A growing collection of open, portable [Agent Skills](https://agentskills.io) — plain `SKILL.md` files that work in **Claude Code, Claude.ai, OpenAI Codex, Google Antigravity, Cursor**, and any other agent that reads the Agent Skills standard. No MCP server, no plugin install, no vendor lock-in: copy a folder, and your agent gets a new, disciplined way of working.

## Why this repo exists

Anyone who has used an AI coding agent for more than a day knows the pattern: you ask for one small thing, and the agent quietly adds a login screen, a config system, a README, dark mode, and three "future-proofing" abstractions nobody asked for — then tells you it's "done" without ever actually running the thing. Scope creep and hallucinated results are the two most common ways AI-assisted work goes wrong.

The skills in this repo exist to fix exactly that: they turn "vibe coding" into a repeatable, auditable, resumable process — one your agent follows the same way whether it's Claude, Codex, Gemini, or Cursor.

## Skills in this repo

### [`idea-to-done/`](idea-to-done/) — from a one-line idea to a verified, finished result

Give it a sentence like *"I want to build a tool that turns my bank CSV exports into a monthly spending summary"* and the skill runs your agent through four disciplined phases — Discovery → Planning → Execution → Verification — organized like a small software team (Product Manager, Tech Lead, Engineers, QA Engineer), all communicating through plain markdown files in `docs/` so the work can be paused, resumed, or handed to a different agent at any point.

What makes it different from just prompting your agent harder:

- **No scope creep.** Every feature must trace back to a requirement you actually asked for. Anything else gets parked in `IDEAS.md`, not silently built.
- **No hallucinated results.** "Done" means the agent ran it and showed you the output — not "should work."
- **Resumable and portable.** State lives in files, not in a chat thread, so a session that dies (or a different agent entirely) can pick up exactly where it left off.
- **Scales to the task.** A one-line fix stays a one-line fix; a real project gets the full office, with parallel workers when it helps.
- **Stress-tested, not just vibes.** Benchmarked with/without the skill (95% vs 63% pass rate across real failure-mode tests) and hardened against 9 adversarial cases — contradictory requirements, prompt injection hidden inside its own project files, mid-flight scope changes, stale/crashed sessions, and more. See `idea-to-done/README.md` for the full changelog.

Works today in Claude Code, Claude.ai, OpenAI Codex, Google Antigravity, and Cursor — see [`idea-to-done/README.md`](idea-to-done/README.md) for exact install paths per tool.

## Install

Each skill is just a folder. Copy or symlink it into your agent's skills directory (see each skill's own README for exact paths per tool), or with the Skills CLI:

```
npx skills add henokakunemail-stack/allinone-skills --skill idea-to-done
```

## Contributing / feedback

Found a case where a skill still drifts, hallucinates, or over-builds? Open an issue with the prompt that broke it — that's exactly how `idea-to-done` reached v1.2.
