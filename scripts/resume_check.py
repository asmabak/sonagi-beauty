#!/usr/bin/env python3
"""Surface a crash checkpoint at SessionStart so a fresh session resumes a dead one.

Summary: a SessionStart hook runs this. If state/_checkpoint/latest.json exists, the
PREVIOUS session did not exit cleanly (a clean exit deletes it via
clear_checkpoint.py on SessionEnd). So this prints a <sonagi-resume> banner with
where that session was: its ask, what it was last doing, the git branch/commit, and
the transcript path for full detail. The banner is injected at the END of the
SessionStart output so the current goal sits at the bottom of context (v4: pin the
goal at top or bottom, never the middle).

It does NOT delete the checkpoint: the current session's first Stop hook overwrites
latest.json with its own state, so nothing is lost and the chain stays correct.

Safe by design: read-only, never fails the session (any error -> exit 0).
Portable: repo resolved from this file's location. Reads the hook payload (session_id)
from stdin to avoid ever surfacing the current session's own checkpoint.
Usage: invoked by the SessionStart hook. Manual: echo '{}' | python3 scripts/resume_check.py
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CKPT_DIR = Path(os.environ.get("SONAGI_CKPT_DIR", REPO / "state" / "_checkpoint"))
LATEST = CKPT_DIR / "latest.json"


def _age_hint(saved_at: str) -> str:
    """A human age like '3h ago' so a stale checkpoint is obviously stale."""
    try:
        delta = datetime.now() - datetime.fromisoformat(saved_at)
        secs = int(delta.total_seconds())
        if secs < 3600:
            return f"{secs // 60}m ago"
        if secs < 86400:
            return f"{secs // 3600}h ago"
        return f"{secs // 86400}d ago"
    except Exception:
        return "unknown age"


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}
    current_session = payload.get("session_id", "")

    try:
        if not LATEST.exists():
            return 0
        snap = json.loads(LATEST.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return 0

    # Belt and suspenders: never resurface the current session's own checkpoint.
    if snap.get("session_id") and snap.get("session_id") == current_session:
        return 0

    tools = ", ".join(snap.get("recent_tools") or []) or "(none recorded)"
    print("<sonagi-resume> The previous session did not exit cleanly (no clean "
          "SessionEnd), so its checkpoint survived. This is where it was. Confirm with "
          "Asma before assuming the work is still wanted; do not blindly redo committed work.")
    print()
    print(f"- Saved at: {snap.get('saved_at', '(unknown)')} ({_age_hint(snap.get('saved_at', ''))})")
    print(f"- Branch: {snap.get('branch', '(unknown)')}")
    print(f"- HEAD: {snap.get('head', '(unknown)')}")
    print(f"- Uncommitted files at crash: {snap.get('dirty_files', '?')}")
    print(f"- Was asked to: {snap.get('current_ask') or '(not captured)'}")
    print(f"- Was last doing (recent tools): {tools}")
    note = (snap.get("last_assistant_note") or "").strip()
    if note:
        print(f"- Last note: {note[:400]}")
    print(f"- Full transcript for replay: {snap.get('transcript_path', '(unknown)')}")
    print("</sonagi-resume>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
