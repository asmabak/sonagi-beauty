#!/usr/bin/env python3
"""Measure tokens and cache hit rate per session (v4 token-efficiency playbook).

Summary: reads Claude Code transcript files for this project and reports input,
output, cache-read and cache-write tokens, plus the CACHE HIT RATE, which v4
calls the single most important production metric. Until this script existed
the metric was unmeasured. Output is a plain table; no dashboards, no deps.

Usage:
  python scripts/session_cost.py            # newest session for this project
  python scripts/session_cost.py --all      # every session, plus a total
  python scripts/session_cost.py --rate     # also print a rough cost estimate

Cache hit rate = cache_read / (cache_read + cache_write + uncached_input).
A high number means we are reusing paid-for context instead of resending it.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Rough Anthropic token multipliers from v4 (relative to one input token):
# a cache WRITE costs ~1.25x, a cache READ ~0.1x. Used only for the optional
# --rate "effective input-token-equivalents" figure, not a dollar bill.
W_WRITE, W_READ = 1.25, 0.10


def project_transcript_dir() -> Path:
    """Claude Code encodes the project path: C:\\Users\\marou\\sonagi-beauty
    becomes C--Users-marou-sonagi-beauty under ~/.claude/projects/."""
    repo = Path(__file__).resolve().parent.parent
    encoded = str(repo).replace(":", "-").replace("\\", "-").replace("/", "-")
    return Path(os.path.expanduser("~")) / ".claude" / "projects" / encoded


def sum_usage(jsonl: Path) -> dict:
    tot = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "msgs": 0}
    try:
        with jsonl.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line or '"usage"' not in line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                u = rec.get("message", {}).get("usage") if isinstance(rec.get("message"), dict) else None
                u = u or rec.get("usage")
                if not isinstance(u, dict):
                    continue
                tot["input"] += u.get("input_tokens", 0) or 0
                tot["output"] += u.get("output_tokens", 0) or 0
                tot["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
                tot["cache_write"] += u.get("cache_creation_input_tokens", 0) or 0
                tot["msgs"] += 1
    except OSError:
        pass
    return tot


def hit_rate(t: dict) -> float:
    denom = t["cache_read"] + t["cache_write"] + t["input"]
    return (t["cache_read"] / denom * 100) if denom else 0.0


def fmt(t: dict, label: str, show_rate: bool) -> str:
    total_in = t["input"] + t["cache_read"] + t["cache_write"]
    line = (f"{label:<28} msgs={t['msgs']:<5} in={t['input']:<9} "
            f"out={t['output']:<8} cache_read={t['cache_read']:<10} "
            f"cache_write={t['cache_write']:<10} hit_rate={hit_rate(t):5.1f}%")
    if show_rate:
        eff = t["input"] + W_WRITE * t["cache_write"] + W_READ * t["cache_read"]
        naive = total_in
        saved = (1 - eff / naive) * 100 if naive else 0
        line += f"  | effective_input_eq={eff:,.0f} (vs {naive:,} uncached, ~{saved:.0f}% saved)"
    return line


def main(argv: list[str]) -> int:
    show_all = "--all" in argv
    show_rate = "--rate" in argv
    tdir = project_transcript_dir()
    if not tdir.exists():
        print(f"no transcript dir found at {tdir}")
        return 1
    files = sorted(tdir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        print(f"no transcripts in {tdir}")
        return 1

    print(f"transcripts: {tdir}\n")
    if not show_all:
        t = sum_usage(files[0])
        print(fmt(t, f"latest ({files[0].stem[:8]})", show_rate))
        return 0

    grand = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "msgs": 0}
    for f in files:
        t = sum_usage(f)
        for k in grand:
            grand[k] += t[k]
        print(fmt(t, f.stem[:8], show_rate))
    print("-" * 80)
    print(fmt(grand, f"TOTAL ({len(files)} sessions)", show_rate))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
