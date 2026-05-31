#!/usr/bin/env python3
"""Emit the Sonagi kernel to stdout so a SessionStart hook injects it at token zero.

Summary: prints the small always-load kernel (the rules, the agent roster, and the
two maps) as ONE block. A SessionStart hook runs this, and the harness injects the
hook's stdout into the fresh session's context. So a cold session is competent at
token zero by MECHANISM, not by remembering to read core/. This closes the gap
where core/ was regenerated but nothing loaded it.

What it deliberately leaves out: the 10 KB skills_index and full Notion pages. Those
are paged in just-in-time by ID when a task needs them, per the charter.

Portable by construction: the repo is resolved from this file's own location, so it
runs unchanged on Windows, on a Mac, from a OneDrive folder, or in a cloud clone. No
absolute machine path appears anywhere in this file.

Usage: python scripts/emit_kernel.py   (run by the SessionStart hook; also runnable by hand)
"""
from __future__ import annotations

import sys
from pathlib import Path

# The core files carry non-cp1252 characters (emoji, curly quotes). Windows'
# default console codec crashes on them, so force UTF-8 (learnings.md, 2026-05-31).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CORE = Path(__file__).resolve().parent.parent / "core"

# Order is priority. Rules first (pinned at the top of context), then who exists,
# then where the code and the Notion pages live.
KERNEL_FILES = ["charter.md", "agent_chart.md", "PROJECT_MAP.md", "WORKSPACE_MAP.md"]


def main() -> int:
    pieces: list[str] = []
    for name in KERNEL_FILES:
        f = CORE / name
        if f.exists():
            pieces.append(f.read_text(encoding="utf-8", errors="replace").rstrip())
    if not pieces:
        # core/ not generated yet (first run before update_project_map). Emit nothing
        # rather than a broken half-kernel; the next session will have it.
        return 0

    body = "\n\n---\n\n".join(pieces)
    print("<sonagi-kernel> always-loaded at token zero. These rules and maps bind this "
          "session. Do not re-fetch them from Notion; they are the local cache.")
    print()
    print(body)
    print()
    print("</sonagi-kernel>")
    print("Note: skills_index.md and full Notion pages are NOT in this kernel. "
          "Page them in just-in-time by ID only when a task needs them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
