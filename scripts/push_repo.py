#!/usr/bin/env python3
"""Auto-push committed work on session end, so nothing is stranded local-only.

Summary: a Stop hook runs this. It pushes the CURRENT branch to its GitHub
remote, but only when there is already-committed work ahead of the remote, and
it never fails the session on a network or config hiccup. This enforces the
"always push after commit" rule mechanically (CLAUDE.md, charter), so a session
never ends with unpushed commits.

Safe by design: it ONLY pushes commits that already exist. It never runs
`git add` or `git commit`, so it cannot sweep in junk, untracked files, or
secrets. Note: this repo is PUBLIC on purpose (Netlify publishing, see
core/decisions.md), so the push publishes publicly. That is accepted; the hard
rule that follows is NEVER commit secrets and keep working content gitignored.

Path-agnostic: resolves the repo from this file's location, so it works on
Windows, macOS, or a cloud clone unchanged. Run manually: python3 scripts/push_repo.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)


def main() -> int:
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if not branch or branch == "HEAD":
        return 0  # detached HEAD, nothing to push to
    # An upstream is required to know where this branch pushes.
    if git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}").returncode != 0:
        print(f"push_repo: '{branch}' has no upstream, skipping. Push once by hand to set it.")
        return 0
    git("fetch", "--quiet")
    ahead = git("rev-list", "--count", "@{u}..HEAD").stdout.strip() or "0"
    if ahead == "0":
        print("push_repo: nothing to push")
        return 0
    r = git("push", "--quiet", "origin", branch)
    print(f"push_repo: pushed {ahead} commit(s) on {branch}" if r.returncode == 0
          else f"push_repo: push failed ({r.stderr.strip()[:120]})")
    return 0  # never block a session on a push hiccup


if __name__ == "__main__":
    raise SystemExit(main())
