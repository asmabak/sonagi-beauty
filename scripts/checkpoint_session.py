#!/usr/bin/env python3
"""Write a durable checkpoint of the live session so a crash resumes without hand-reading the transcript.

Summary: a Stop hook (every assistant turn) and a UserPromptSubmit hook (every new
ask) run this. It snapshots the smallest set of facts that let a FRESH session pick
up where a crashed one died: the current ask, what the agent was last doing, the git
branch/commit, and the path to the full transcript for detail. It writes BOTH a
machine file (latest.json) and a human-readable banner (latest.md) into
state/_checkpoint/. The 2026-05-31 crash forced a session to hand-read a raw
transcript dump (OS/crash session 3105.txt); this removes that.

Crash detection is by absence: a clean exit deletes the checkpoint (SessionEnd ->
clear_checkpoint.py). If the checkpoint still exists at the next SessionStart, the
prior session did NOT exit cleanly, so resume_check.py surfaces it. The current
session's first Stop overwrites latest.json with its own state, so the chain always
points at the last live turn.

Safe by design: reads only; the only writes are the two checkpoint files. It never
fails the session (any error -> exit 0). Reads the hook payload from stdin
(transcript_path, session_id, cwd, hook_event_name, and prompt on UserPromptSubmit).

Portable: repo resolved from this file's location; no absolute machine path.
Usage: invoked by the Stop and UserPromptSubmit hooks. Manual: echo '{}' | python3 scripts/checkpoint_session.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# The checkpoint dir is overridable so the eval can point at a tempdir and never
# touch real session state. Default is the per-machine, gitignored state dir.
CKPT_DIR = Path(os.environ.get("SONAGI_CKPT_DIR", REPO / "state" / "_checkpoint"))
RECENT_TOOLS = 10  # how many of the most recent tool calls to record


def git(*args: str) -> str:
    try:
        r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def read_stdin_payload() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def _text_from_content(content) -> str:
    """Pull plain text out of a message 'content' that may be a str or a block list."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                return block.get("text", "")
    return ""


def parse_transcript(path_str: str) -> dict:
    """Extract the current ask, recent tool calls, and the last assistant note."""
    out = {"last_prompt": "", "recent_tools": [], "last_assistant": ""}
    if not path_str:
        return out
    p = Path(path_str)
    if not p.exists():
        return out
    tools: list[str] = []
    lp_record = ""       # the authoritative 'last-prompt' value, if present
    last_user_text = ""  # most recent plain user message, as a fallback
    try:
        with p.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = rec.get("type")
                # Claude Code stores the verbatim latest user prompt in 'last-prompt'.
                if t == "last-prompt" and rec.get("lastPrompt"):
                    lp_record = str(rec["lastPrompt"])
                elif t == "user":
                    txt = _text_from_content(rec.get("message", {}).get("content"))
                    # Skip slash-command wrappers and empty tool-result turns; keep the LATEST.
                    if txt and not txt.lstrip().startswith("<command-"):
                        last_user_text = txt
                elif t == "assistant":
                    for block in rec.get("message", {}).get("content") or []:
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_use":
                            tools.append(block.get("name", "?"))
                        elif block.get("type") == "text" and block.get("text", "").strip():
                            out["last_assistant"] = block["text"].strip()
    except OSError:
        return out
    # Precedence: the explicit last-prompt record wins, else the latest user text.
    out["last_prompt"] = lp_record or last_user_text
    out["recent_tools"] = tools[-RECENT_TOOLS:]
    return out


def main() -> int:
    try:
        payload = read_stdin_payload()
        session_id = payload.get("session_id", "")
        transcript_path = payload.get("transcript_path", "")
        event = payload.get("hook_event_name", "")

        info = parse_transcript(transcript_path)
        # On UserPromptSubmit the just-typed prompt is handed in directly and is
        # fresher than anything yet written to the transcript file.
        if payload.get("prompt"):
            info["last_prompt"] = str(payload["prompt"])

        branch = git("rev-parse", "--abbrev-ref", "HEAD")
        head = git("log", "-1", "--format=%h %s")
        dirty = git("status", "--porcelain")
        dirty_count = len([ln for ln in dirty.splitlines() if ln.strip()]) if dirty else 0
        now = datetime.now().isoformat(timespec="seconds")

        snap = {
            "saved_at": now,
            "session_id": session_id,
            "hook_event": event,
            "transcript_path": transcript_path,
            "branch": branch,
            "head": head,
            "dirty_files": dirty_count,
            "current_ask": (info["last_prompt"] or "").strip()[:500],
            "recent_tools": info["recent_tools"],
            "last_assistant_note": info["last_assistant"][:600],
        }

        CKPT_DIR.mkdir(parents=True, exist_ok=True)
        # Atomic write: a kill mid-write must never leave a truncated latest.json
        # (that is the exact crash this feature exists to survive). Write a temp
        # file, then os.replace, which is atomic on both Windows and macOS.
        tmp = CKPT_DIR / "latest.json.tmp"
        tmp.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, CKPT_DIR / "latest.json")

        tools_line = ", ".join(snap["recent_tools"]) or "(none recorded)"
        md = (
            f"# Session checkpoint (last live turn)\n\n"
            f"> Written by checkpoint_session.py on every turn. If you are reading this in a\n"
            f"> resume banner, the previous session ended WITHOUT a clean exit (likely a crash).\n\n"
            f"- Saved at: {now}\n"
            f"- Session id: {session_id or '(unknown)'}\n"
            f"- Branch: {branch or '(unknown)'}\n"
            f"- HEAD: {head or '(unknown)'}\n"
            f"- Uncommitted files: {dirty_count}\n\n"
            f"## What the session was asked to do\n{snap['current_ask'] or '(not captured)'}\n\n"
            f"## What it was last doing\nRecent tool calls: {tools_line}\n\n"
            f"Last assistant note:\n{snap['last_assistant_note'] or '(none)'}\n\n"
            f"## Full detail\nReplay the transcript if you need step-by-step history:\n{transcript_path or '(unknown)'}\n"
        )
        (CKPT_DIR / "latest.md").write_text(md, encoding="utf-8")
    except Exception:
        # A checkpoint must never break a turn.
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
