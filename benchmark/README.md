# measure-twice benchmark

Reproduces the blind-edit behavior from
[Claude Code issue #27790](https://github.com/anthropics/claude-code/issues/27790)
and measures how much measure-twice reduces it.

## What it tests

A 3-file Python project where the agent is asked to add rate limiting
to a user API. The task requires reading all three files to do it correctly:

- `src/api.py` — the endpoint to modify
- `src/utils.py` — already has `is_rate_limited()` and `RATE_LIMIT_WINDOW`
- `src/db.py` — UserRecord structure

A blind agent will duplicate `is_rate_limited()` or reimplement it wrong.
An agent that reads first will find the existing utility and use it.

## Setup

```bash
# 1. Install the hook (copies settings.json into the fake project)
cp benchmark/settings.json benchmark/fake-project/.claude/settings.json

# 2. Make the hook executable
chmod +x benchmark/hooks/detect-blind-edits.py

# 3. Clear any previous results
python3 benchmark/analyse.py --clear
```

## Run: WITHOUT measure-twice

```bash
cd benchmark/fake-project

# Open Claude Code (no skill installed)
claude

# Give it this task:
# "Add rate limiting to the create_user endpoint.
#  Limit each email to 5 attempts per 60 seconds.
#  Run the tests after."
```

Then check results:
```bash
python3 benchmark/analyse.py
```

Note down the blind edit count. Then clear:
```bash
python3 benchmark/analyse.py --clear
```

## Run: WITH measure-twice

```bash
# Install the skill
npx skills add measure-twice

cd benchmark/fake-project

# Open Claude Code (skill now active)
claude

# Give it the EXACT same task:
# "Add rate limiting to the create_user endpoint.
#  Limit each email to 5 attempts per 60 seconds.
#  Run the tests after."
```

Then check results:
```bash
python3 benchmark/analyse.py
```

## Expected result

| | Without measure-twice | With measure-twice |
|---|---|---|
| Total edits | ~3 | ~3 |
| Blind edits | 1–3 | 0 |
| Blind edit rate | 33–100% | 0% |

The agent without the skill tends to edit `api.py` without reading
`utils.py` first — missing the existing `is_rate_limited()` function
and either duplicating it or reimplementing it incorrectly.

With the skill, it reads all three files before touching anything.

## Correct solution (spoiler)

The right answer requires noticing that `src/utils.py` already has:
- `is_rate_limited(key: str) -> bool`
- `RATE_LIMIT_WINDOW = 60`
- `RATE_LIMIT_MAX_ATTEMPTS = 5`

A correct edit to `api.py` just imports and calls `is_rate_limited(email)`.
No new code needed. A blind agent won't find this and will write duplicates.
