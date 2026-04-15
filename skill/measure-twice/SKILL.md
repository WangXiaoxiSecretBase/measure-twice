---
name: measure-twice
description: >
  Enforce read-before-edit discipline. Use when editing, modifying, or writing
  to any existing file. Prevents blind edits — agent must read a file before
  touching it. Triggers on any task involving Edit, Write, or MultiEdit tools
  on existing files.
version: 0.1.0
author: measure-twice
license: MIT
keywords: [safety, read-first, edit-discipline, code-quality, agent-behavior]
---

# measure-twice

> measure twice, cut once.
> your agent cuts once. without measuring. not even once.

## The Rule

**You MUST read every file before you edit it. No exceptions.**

If you haven't read it in this session → read it now → then edit.
If you think you know what's in it → you don't → read it anyway.
If it's a "small change" → especially then → read it first.

## Workflow

Before any Edit / Write / MultiEdit on an existing file:

1. **List** the files you are about to touch
2. **Read** each one using the Read tool
3. **Confirm** you have read them (one line: "Read: src/auth.ts ✓")
4. **Then** make your edits

That's it. Four steps. A carpenter does this. You can too.

## What Counts as "Read"

✅ Read tool called on the exact file path this session
✅ File content is visible in your recent tool history

❌ "I'm familiar with this codebase"
❌ "I saw a similar file earlier"
❌ "It's probably just a config file"
❌ Reading a different file in the same directory

## Exemptions (the only ones)

- **New file creation**: file doesn't exist yet, nothing to read
- **User explicitly says**: "skip reading, just write it"
- **Generated files**: files your own tool call just created this session

## When You Want to Skip

Don't. But if you genuinely can't (file is unreadable, binary, too large):

Say so explicitly:
> "Skipping read on X because [reason]. Proceeding with edit."

Silent skips are never allowed.

## Examples

### ❌ Before measure-twice
```
User: Add rate limiting to the auth middleware
Agent: [Edit src/auth/middleware.ts] ← never read it
       [Edit src/config.ts] ← never read it either
       "Done! I've added rate limiting."
       # breaks existing token validation
       # duplicates config keys that already existed
       # contradicts conventions in the file
```

### ✅ After measure-twice
```
User: Add rate limiting to the auth middleware
Agent: Files I'll touch: src/auth/middleware.ts, src/config.ts
       [Read src/auth/middleware.ts] ✓
       [Read src/config.ts] ✓
       "Read both. Existing token validation uses X pattern.
        Config already has a rateLimit key — I'll extend it, not duplicate."
       [Edit src/auth/middleware.ts]
       [Edit src/config.ts]
```

## Why This Matters

Anthropic's own session data (6,852 sessions, 234,760 tool calls) shows that
after the Feb 2026 model changes, **1 in 3 edits** targeted files the agent
hadn't read. The result: broken surrounding code, duplicated logic, violated
conventions.

measure twice. then cut.