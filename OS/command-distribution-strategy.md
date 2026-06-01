# Command & definition distribution: strategy brief (decide with Asma, build next session)

> Status: OPEN STRATEGY QUESTION, 2026-06-01. Not yet decided. This brief sets up the
> strategy session; it does NOT lock a design. Build only after Asma aligns on the approach.
> Raised because /lets-start-sonagi was "command unknown" on a phone session, which exposed
> a deeper infra question, not a small one.

## The real question
What is the single source of truth for executable, ownable definitions (slash commands first,
but the same logic covers agents and skills), such that EVERY surface Asma works from has the
same version, with no hand-maintained copies that drift? Surfaces today: the Windows laptop,
the incoming Mac, and cloud/phone sessions (Claude Code on claude.ai) against either repo.

This is the same drift problem that made Asma reject keeping things on the local drive. It must
be solved on principle, not patched per-file.

## Hard constraints (verified 2026-06-01, do not re-derive)
1. Claude Code has exactly two command locations:
   - USER level (`~/.claude/commands/`): every repo, but only on that one machine. The cloud/phone cannot see it.
   - PROJECT level (`<repo>/.claude/commands/`): travels to the cloud/phone, but only for that repo, on the branch the session opens.
   There is NO built-in account-level command store that syncs to the phone. So at least one copy per repo is unavoidable.
2. A cloud/phone session reads PROJECT commands from the repo it opens, on that repo's branch.
3. Default branches (what a phone opens by default) are non-obvious:
   - `asmabak/sonagi-beauty` default branch = `claude/extract-marketing-skills-z03eL` (NOT the working branch `claude/live-baseline-2026-05-14`).
   - `asmabak/sonagi-reference` default branch = `main` (working branch is `phase-0/init`, which already has the commands).
   So "the working branch has it" is not enough; the phone opens the default branch.
4. State at time of writing: the two commands (lets-start-sonagi, wrapup) exist on
   `~/.claude/commands/` (laptop), on sonagi-beauty `claude/live-baseline-2026-05-14`, and on
   sonagi-reference `phase-0/init`. They are NOT on either repo's default branch. This is drift already.

## Principles the solution must satisfy
- One canonical home per item; mirrors only FOLLOW a master, never hand-edited (Charter section 2; the no-mirror retirement of 2026-06-01 explicitly allows generated mirrors that follow a master).
- Optimise the cold start: a fresh session on any surface wakes up with the right commands.
- Portable, survives the Mac move (so the master cannot be a single machine's `~/.claude/`).
- Lean for a 2-person team: no cathedral. Automate only what drifts silently (Charter D4).
- Human gate on publish/spend/delete still applies; a private/public-backup push is saving, not the gate.

## Option space (evaluate, do not assume)
- A. Canonical in one repo (`sonagi-beauty/.claude/commands/`) + `scripts/sync_commands.py` wired to a SessionStart hook that regenerates the mirrors (into `~/.claude/commands/` and the other repo) from the master. Mirrors generated, never edited. Open issue: getting the mirror committed+pushed to each repo's DEFAULT branch for the cloud, a local hook cannot fully own a cross-repo push.
- B. A dedicated tiny "commands" git repo, pulled into each project (submodule or a sync script). Cleaner master, but submodules are fragile on cloud/mobile and add a repo to manage.
- C. Accept user-level as the laptop convenience, and treat each repo's `.claude/commands/` as the canonical for that repo, with a sync script keeping them identical. Simplest, but two masters in tension.
- D. Reconsider the default-branch situation entirely (sonagi-beauty's default being a `claude/...` branch is itself odd and may be the root cause to fix first).

## Open sub-questions for Asma (the alignment part)
1. What is the canonical home (a repo path, a dedicated repo, or user-level)?
2. Do we fix sonagi-beauty's default branch first (it points at `claude/extract-marketing-skills-z03eL`, not the working branch)?
3. How do cloud copies get updated "all the time" given a local hook cannot cleanly push to another repo's branch? (candidate: a single `sync_commands.py` run that writes + commits + pushes to every target, run on demand or by a hook, treated as a generated-mirror refresh.)
4. Does this rule extend to agents and skills (same two-brains logic), or commands only for now?

## Recommendation for the build session
Start from option A (canonical in the OS repo + a generated-mirror sync script), but only after Asma
answers the sub-questions above. Write `scripts/sync_commands.py` + decision-log the canonical home,
then place the generated copies on each repo's phone-facing (default) branch. Build with fresh context.
