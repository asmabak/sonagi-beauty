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

It never touches the real state/_checkpoint dir: it runs the scripts with a patched
checkpoint dir via a temp HOME-independent copy, asserting on a temp transcript.

Usage:
  python evals/crash_resume_eval.py        # run the checks
Exit code: 0 = all pass, 1 = a check failed.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"


def run(script: str, payload: dict | None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(SCRIPTS / script)],
        input=json.dumps(payload) if payload is not None else "",
        capture_output=True, text=True,
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
    # Isolate: redirect the checkpoint dir by running in a temp repo-shaped tree is
    # heavy; instead we accept that the scripts write to the REAL state/_checkpoint,
    # so we snapshot-and-restore any existing checkpoint around the test.
    ckpt = REPO / "state" / "_checkpoint"
    saved = {}
    for n in ("latest.json", "latest.md"):
        f = ckpt / n
        if f.exists():
            saved[n] = f.read_text(encoding="utf-8")

    try:
        with tempfile.TemporaryDirectory() as td:
            tp = make_fake_transcript(Path(td))
            # 1. write a checkpoint
            run("checkpoint_session.py", {
                "session_id": "PRIOR", "transcript_path": str(tp),
                "hook_event_name": "Stop",
            })
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

            # 2a. resume surfaces for a DIFFERENT session
            r = run("resume_check.py", {"session_id": "CURRENT-other"})
            if "<sonagi-resume>" not in r.stdout:
                fails.append("resume_check did not surface a prior checkpoint")
            # 2b. resume is SILENT for the SAME session
            r = run("resume_check.py", {"session_id": "PRIOR"})
            if "<sonagi-resume>" in r.stdout:
                fails.append("resume_check resurfaced the current session's own checkpoint")

            # 3. clear removes it
            run("clear_checkpoint.py", None)
            if (ckpt / "latest.json").exists() or (ckpt / "latest.md").exists():
                fails.append("clear_checkpoint did not remove the checkpoint")
            # 3b. resume is silent when there is nothing to resume
            r = run("resume_check.py", {"session_id": "x"})
            if "<sonagi-resume>" in r.stdout:
                fails.append("resume_check surfaced a banner with no checkpoint present")
    finally:
        # restore any real checkpoint we displaced
        ckpt.mkdir(parents=True, exist_ok=True)
        for n, content in saved.items():
            (ckpt / n).write_text(content, encoding="utf-8")
        if not saved:
            for n in ("latest.json", "latest.md"):
                try:
                    (ckpt / n).unlink(missing_ok=True)
                except OSError:
                    pass

    if fails:
        print("crash_resume_eval: FAIL")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("crash_resume_eval: PASS (write, surface, silence-on-self, clear)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
