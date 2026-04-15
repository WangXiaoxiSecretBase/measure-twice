#!/usr/bin/env python3
"""
measure-twice benchmark — results analyser
------------------------------------------
Reads /tmp/measure-twice-benchmark.jsonl and prints a summary.

Usage:
    python3 benchmark/analyse.py
    python3 benchmark/analyse.py --clear   # clear log and start fresh
"""

import json
import sys
from pathlib import Path
from collections import Counter

LOG_FILE = Path("/tmp/measure-twice-benchmark.jsonl")


def load_records():
    if not LOG_FILE.exists():
        return []
    records = []
    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def print_summary(records, label=""):
    total = len(records)
    if total == 0:
        print("  No edits recorded.")
        return

    blind = sum(1 for r in records if r["blind_edit"])
    read_first = total - blind
    blind_pct = blind / total * 100

    print(f"  Total edits  : {total}")
    print(f"  Read first   : {read_first}  ({100 - blind_pct:.0f}%)")
    print(f"  Blind edits  : {blind}  ({blind_pct:.0f}%)")

    if blind > 0:
        print("\n  Blind edit targets:")
        blind_files = Counter(r["file"] for r in records if r["blind_edit"])
        for path, count in blind_files.most_common():
            short = path.split("/")[-1]
            print(f"    {short}: {count}x")


def main():
    if "--clear" in sys.argv:
        LOG_FILE.unlink(missing_ok=True)
        print(f"Cleared {LOG_FILE}")
        return

    records = load_records()

    if not records:
        print(f"No data yet. Run the benchmark first.")
        print(f"Log file: {LOG_FILE}")
        return

    # Split by run label if present, otherwise show all
    labelled = [r for r in records if r.get("label")]
    unlabelled = [r for r in records if not r.get("label")]

    print("=" * 50)
    print("  measure-twice benchmark results")
    print("=" * 50)

    if labelled:
        runs = {}
        for r in labelled:
            runs.setdefault(r["label"], []).append(r)
        for label, run_records in runs.items():
            print(f"\n[{label}]")
            print_summary(run_records)
    else:
        print()
        print_summary(records)

    print()
    print(f"Log file: {LOG_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()
