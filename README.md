# 📏 measure-twice

**measure twice, cut once.**
**your agent cuts once. without measuring. not even once.**

[Install](#install) • [Before/After](#beforeafter) • [Why](#why)

---

A Claude Code skill that forces your agent to **read files before editing them**.

Based on Anthropic's own session data: after the Feb 2026 model changes, **1 in 3 edits** were made to files the agent hadn't read. The result: broken code, duplicated logic, violated conventions. A `$0.001` Haiku hook catches what the main model's reasoning does not.

We made it a one-line install.

## Before / After

| | |
|---|---|
| 🔪 **Without measure-twice** | 📏 **With measure-twice** |
| Agent edits `auth/middleware.ts` — never read it. Breaks existing token validation. Duplicates a config key. Contradicts every convention in the file. | Agent lists files, reads each one, confirms, then edits. Sees the existing token validation. Extends the config key instead of duplicating it. |

**Same task. Zero blind edits. Carpenter-grade discipline.**

## Install

```bash
npx skills add measure-twice
```

One command. That's it.

## Usage

Activates automatically whenever you ask the agent to edit an existing file.

No trigger phrase needed — it just works.

To disable for a session: `"skip read checks"` or `"stop measure-twice"`

## What It Enforces

| Behavior | Enforced? |
|---|---|
| Read file before Edit | ✅ Always |
| Read file before Write | ✅ Always |
| Read file before MultiEdit | ✅ Always |
| New file creation | ➖ Exempt (nothing to read) |
| "I'm familiar with this codebase" | ❌ Not good enough |
| Silent skip | ❌ Never allowed |

## Why

```
┌─────────────────────────────────────────┐
│  BLIND EDITS PREVENTED      ████████    │
│  BROKEN CONVENTIONS         ████████ 0% │
│  DUPLICATED LOGIC           ████████ 0% │
│  CARPENTER APPROVAL RATING  ████████ ✓  │
└─────────────────────────────────────────┘
```

From [GitHub issue #27790](https://github.com/anthropics/claude-code/issues/27790) on the Claude Code repo:

> "Opus 4.6 with 1M context systematically edits files without reading them first.
> Our hook fires on a significant percentage of edit attempts —
> confirming this is a model-level behavior pattern, not user error."

The fix exists as a hook — but hooks require `settings.json` configuration.
measure-twice makes it a one-line install that works everywhere.

## License

MIT — measure twice, liability once.
