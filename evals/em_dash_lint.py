#!/usr/bin/env python3
"""Machine eval (content layer, D6): the em-dash ban, enforced as a hard gate.

Summary: scans text for em dashes and their lookalikes, which are a banned
Claude writing tell across all Sonagi work. Prints every hit as file:line:col
with context and exits non-zero if any are found, so it can BLOCK a commit or
a ship. This is the lintable half of the content layer; taste still goes to a
human gate.

Note: this file contains NO literal em dash. The banned characters are built
from unicode escapes below, so the linter passes its own gate.

Usage:
  python evals/em_dash_lint.py FILE [FILE ...]   # scan given files
  python evals/em_dash_lint.py --staged          # scan git-staged text files
  python evals/em_dash_lint.py --selftest        # prove the gate catches/passes

Exit code: 0 = clean, 1 = banned characters found, 2 = selftest failed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Force UTF-8 output so printing an offending character never crashes on a
# Windows cp1252 console.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

# Built from code points, NOT typed literally, so this source file contains
# none of the banned characters and therefore passes its own gate.
EM = chr(0x2014)   # em dash, the primary banned character
BAR = chr(0x2015)  # horizontal bar, an em-dash lookalike, also banned

# Banned character -> plain reason (no literal em dash in the reason text).
BANNED = {
    EM: "em dash. Use a period, comma, colon, or parentheses instead.",
    BAR: "horizontal bar (em-dash lookalike). Banned, same rule.",
}

TEXT_SUFFIXES = {".md", ".txt", ".mdx", ".html", ".json", ".yml", ".yaml", ".py", ".js", ".ts"}


def scan_text(name: str, text: str) -> list[str]:
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for col, ch in enumerate(line, 1):
            if ch in BANNED:
                ctx = line.strip()
                if len(ctx) > 80:
                    ctx = ctx[:77] + "..."
                hits.append(f"{name}:{lineno}:{col}: {BANNED[ch]}  | {ctx}")
    return hits


def scan_file(path: Path) -> list[str]:
    try:
        return scan_text(str(path), path.read_text(encoding="utf-8", errors="replace"))
    except OSError as e:
        return [f"{path}: could not read ({e})"]


def staged_files() -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True,
    ).stdout.splitlines()
    return [Path(p) for p in out if Path(p).suffix.lower() in TEXT_SUFFIXES and Path(p).exists()]


def selftest() -> int:
    bad = "This sentence uses an em dash " + EM + " like so."
    good = "This sentence uses a colon: like so, and parentheses (like this)."
    bad_hits = scan_text("<bad>", bad)
    good_hits = scan_text("<good>", good)
    ok = len(bad_hits) == 1 and len(good_hits) == 0
    print("selftest:", "PASS" if ok else "FAIL",
          f"(caught {len(bad_hits)} in bad, {len(good_hits)} in good)")
    return 0 if ok else 2


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--selftest":
        return selftest()
    files = staged_files() if argv[0] == "--staged" else [Path(a) for a in argv]
    if not files:
        print("em-dash lint: no files to scan")
        return 0
    all_hits: list[str] = []
    for f in files:
        all_hits.extend(scan_file(f))
    if all_hits:
        print(f"em-dash lint: BLOCKED. {len(all_hits)} banned character(s) found:\n")
        print("\n".join(all_hits))
        return 1
    print(f"em-dash lint: clean ({len(files)} file(s) scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
