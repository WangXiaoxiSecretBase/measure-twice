#!/usr/bin/env python3
"""
measure-twice benchmark hook
----------------------------
PreToolUse hook on Edit|Write|MultiEdit.

Reads the Claude Code transcript to check whether the agent
called Read on the target file before attempting this edit.

Exit 0  → allow (and log result)
Exit 0  → also allow if blind edit detected (we only LOG, not block)
          This lets the benchmark run naturally without interfering.

Logs every result to: /tmp/measure-twice-benchmark.jsonl
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("/tmp/measure-twice-benchmark.jsonl")


def main():
    raw = sys.stdin.read()
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})
    transcript_path = event.get("transcript_path", "")

    # Get the target file path from the tool input
    target_file = (
        tool_input.get("file_path")          # Write
        or tool_input.get("path")            # Edit
        or tool_input.get("new_path")        # MultiEdit
        or ""
    )

    if not target_file:
        sys.exit(0)

    target_file = str(Path(target_file).resolve())

    # Check transcript for prior Read on this file
    did_read = False
    if transcript_path and Path(transcript_path).exists():
        try:
            with open(transcript_path) as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Look for Read tool calls in assistant messages
                    if entry.get("role") != "assistant":
                        continue

                    for block in entry.get("content", []):
                        if block.get("type") != "tool_use":
                            continue
                        if block.get("name") != "Read":
                            continue
                        read_path = str(Path(
                            block.get("input", {}).get("file_path", "")
                        ).resolve())
                        if read_path == target_file:
                            did_read = True
                            break
                    if did_read:
                        break
        except Exception:
            pass

    # Log result
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "tool": tool_name,
        "file": target_file,
        "did_read_first": did_read,
        "blind_edit": not did_read,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

    # Always allow — we are observing, not blocking
    sys.exit(0)


if __name__ == "__main__":
    main()
