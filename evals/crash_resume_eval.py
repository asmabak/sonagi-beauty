#!/usr/bin/env python3
"""Machine eval (D6): prove the crash-resume checkpoint round-trips correctly.

Summary: drives the three crash-resume scripts against a temporary fake transcript
and asserts the contract that item A promises:
  1. checkpoint_session.py writes latest.json + latest.md from a hook payload, and
     extracts the current ask + recent tool calls from the transcript.
  2. resume_check.py SURFACES a checkpoint from a different session, and stays
     SILENT for the same session (never resurfaces the current session's own state).
  3. clear_checkpoint.py removes the checkpoint (the clean-exit path).
A regression here means a crash would not resume, so this blocks the ship.

True isolation: every script honours the SONAGI_CKPT_DIR env var, so this eval
points all three at a tempdir and never reads or writes the real
state/_checkpoint. No snapshot/restore, no race with a live session.

Usage:
  python evals/crash_resume_eval.py        # run the checks
Exit code: 0 = all pass, 1 = a check failed.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"


def run(script: str, payload: dict | None, ckpt_dir: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, SONAGI_CKPT_DIR=str(ckpt_dir))
    return subprocess.run(
        ["python3", str(SCRIPTS / script)],
        input=json.dumps(payload) if payload is not None else "",
        capture_output=True, text=True, env=env,
    )


def make_fake_transcript(d: Path) -> Path:
    """A minimal transcript with a last-prompt, an assistant tool_use, and a note."""
    tp = d / "fake.jsonl"
    lines = [
        {"type": "last-prompt", "lastPrompt": "ship the crash-resume eval", "sessionId": "PRIOR"},
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "text", "text": "Writing the eval now."},
            {"type": "tool_use", "name": "Write"},
        ]}},
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "name": "Bash"},
        ]}},
    ]
    tp.write_text("\n".join(json.dumps(x) for x in lines), encoding="utf-8")
    return tp


def main() -> int:
    fails: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        ckpt = td / "_checkpoint"
        tp = make_fake_transcript(td)

        # 1. write a checkpoint
        run("checkpoint_session.py",
            {"session_id": "PRIOR", "transcript_path": str(tp), "hook_event_name": "Stop"},
            ckpt)
        j = ckpt / "latest.json"
        if not j.exists():
            fails.append("checkpoint_session.py did not write latest.json")
        else:
            snap = json.loads(j.read_text(encoding="utf-8"))
            if snap.get("current_ask") != "ship the crash-resume eval":
                fails.append(f"current_ask not extracted: {snap.get('current_ask')!r}")
            if "Write" not in (snap.get("recent_tools") or []):
                fails.append(f"recent_tools missing tool calls: {snap.get('recent_tools')}")
            if not (ckpt / "latest.md").exists():
                fails.append("latest.md not written")
            if (ckpt / "latest.json.tmp").exists():
                fails.append("temp file left behind (atomic write did not os.replace)")

        # 2a. resume surfaces for a DIFFERENT session
        r = run("resume_check.py", {"session_id": "CURRENT-other"}, ckpt)
        if "<sonagi-resume>" not in r.stdout:
            fails.append("resume_check did not surface a prior checkpoint")
        # 2b. resume is SILENT for the SAME session
        r = run("resume_check.py", {"session_id": "PRIOR"}, ckpt)
        if "<sonagi-resume>" in r.stdout:
            fails.append("resume_check resurfaced the current session's own checkpoint")

        # 3. clear removes it
        run("clear_checkpoint.py", None, ckpt)
        if (ckpt / "latest.json").exists() or (ckpt / "latest.md").exists():
            fails.append("clear_checkpoint did not remove the checkpoint")
        # 3b. resume is silent when there is nothing to resume
        r = run("resume_check.py", {"session_id": "x"}, ckpt)
        if "<sonagi-resume>" in r.stdout:
            fails.append("resume_check surfaced a banner with no checkpoint present")

    if fails:
        print("crash_resume_eval: FAIL")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("crash_resume_eval: PASS (write, surface, silence-on-self, clear, atomic)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
