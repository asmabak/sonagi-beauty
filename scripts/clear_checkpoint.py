#!/usr/bin/env python3
"""Delete the session checkpoint on a clean exit, so only a crash leaves one behind.

Summary: a SessionEnd hook runs this. SessionEnd fires on a normal exit (/clear,
logout, quit) but NOT on a hard crash (power loss, killed process, GPU lost). So
deleting the checkpoint here makes "a checkpoint still exists at next start" mean
exactly "the last session crashed", which is what resume_check.py keys off. A clean
session leaves nothing to resume; the daily handoff (wrapup) carries forward
intentional continuity instead.

Safe by design: only ever removes state/_checkpoint/latest.{json,md}; never fails the
session (any error -> exit 0). Portable: repo resolved from this file's location.
Usage: invoked by the SessionEnd hook. Manual: python3 scripts/clear_checkpoint.py
"""
from __future__ import annotations

import os
from pathlib import Path

CKPT_DIR = Path(os.environ.get(
    "SONAGI_CKPT_DIR", Path(__file__).resolve().parent.parent / "state" / "_checkpoint"))


def main() -> int:
    for name in ("latest.json", "latest.md", "latest.json.tmp"):
        try:
            (CKPT_DIR / name).unlink(missing_ok=True)
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
