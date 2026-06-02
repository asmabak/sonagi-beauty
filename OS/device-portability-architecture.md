# Device portability architecture: full structure on any device, never blocked

> Status: ANALYSIS for alignment, 2026-06-01. Supersedes the framing of
> `OS/command-distribution-strategy.md` (which scoped to commands only). This doc reframes
> to Asma's actual goal and does the first-principles analysis she asked for before any build.
> It recommends; it does NOT lock a design. Build only after Asma aligns on the open decisions
> at the end, and after a fresh-context critical review.

## The real goal (Asma's words, 2026-06-01)

> "It's not just a question of command. Being able to start a job from any device means having
> access to the full structure from all devices I use and never being blocked because I start a
> session on my phone."

So the problem is not "sync two command files." It is: **a session started on any device wakes
up with the capability it needs, and is never dead-ended because that device is missing a piece
of the structure.** Commands are the first and smallest slice of that.

## First principle: what can each device actually see?

A Claude Code session can only load what is physically reachable from where it runs. Three surfaces:

| Surface | Can see user-level `~/.claude/` (commands, agents, skill junctions)? | Can see a repo? |
|---|---|---|
| Windows laptop | ✅ yes (full) | ✅ any local clone |
| Incoming Mac | ✅ yes, after `~/.claude/` is reconstructed by the migration scripts | ✅ any local clone |
| Cloud / phone (claude.ai Claude Code) | ❌ NO user-level anything | ✅ ONLY the one repo it opens, on the branch it opens |

The binding constraint is the **cloud/phone** surface. It has no `~/.claude/`. It sees only a repo,
on a branch. Everything that must work there has to be **committed into a repo, on the branch the
cloud session opens.** Claude Code has no account-level store that syncs to the phone (verified
2026-06-01). This single fact drives the entire design.

## Second principle: "full structure" is four layers, not one

Treating "structure" as one uniform thing is the mistake that makes this feel like a cathedral.
It is four layers with different portability profiles:

1. **Commands**: 2 markdown files (`lets-start-sonagi`, `wrapup`). Tiny, owned, edited ~monthly.
2. **Agents**: ~10 markdown files in `~/.claude/agents/`, already mastered in `asmabak/sonagi-agents`.
   Portable text Claude edits.
3. **Sonagi-owned skills**: the marketing pack (already in-repo under `.agents/skills/`),
   `engineering-review`, `sonagi-diagram-branding`. Owned, portable.
4. **Third-party skill packs**: ~200 skills junctioned from ~20 external repos
   (`claude-ads`, `anthropic-skills`, `claude-scientific-skills`, `claude-seo`, ...). These do NOT
   exist on cloud/phone and porting them is a separate, much larger project.

Layers 1-3 are small, owned, daily-edited, and genuinely belong on every device. Layer 4 is large,
vendored, and you would almost never invoke it from a phone (you are not running `biopython` or
`scientific/astropy` on mobile). **Lean answer (Gate 1): make layers 1-3 portable now; explicitly
defer layer 4 until a real need to run a specific third-party skill on mobile appears.** Pulling 20
external repos onto the cloud surface to satisfy a need that does not exist is exactly the
over-build the scope gate is meant to catch.

## Third principle: one master, generated mirrors (never two hand-edited copies)

The drift we are killing comes from editing the same definition in two places. On the laptop you
naturally edit `~/.claude/commands/`; the cloud needs the repo copy. If both are hand-edited, they
diverge (this already happened: the laptop and working branch have the real commands, both repos'
DEFAULT branches do not). So exactly one location is the **master** that a human/Claude edits, and
every other copy is a **generated mirror** carrying a "generated, do not edit" header, written by a
sync script. (Charter §2; the no-mirror retirement of 2026-06-01 explicitly allows generated
mirrors that follow a master.)

## The canonical-home question (the one Asma flagged for real analysis)

Candidates, judged on first principles, not preference:

**Option A. Master = a folder in the OS repo (`sonagi-beauty`).** Mirrors generated into
`~/.claude/` and into the other repo.
- For: the OS brain already lives here (`OS/`, `core/`, the kernel, the skills). It is where Claude
  works every day. Zero new repos to maintain (Gate 1: a new repo is guilty until proven necessary).
- Against: the master copy sits on a working branch, but cloud opens the DEFAULT branch, so within
  this very repo the master is not what the phone sees. And pushing a mirror into the *other* repo
  (`sonagi-reference`) is a cross-repo commit+push that a local hook cannot own cleanly.

**Option B. Master = a dedicated definitions repo** (extend `sonagi-agents` into `sonagi-os-defs`
holding commands + agents + Sonagi skills). Every machine and project pulls from it.
- For: conceptually the cleanest single master; a phone can open THIS repo directly to get
  commands/agents.
- Against: it does NOT remove the per-repo copy. For a command to work while a cloud session is open
  on `sonagi-beauty` (not the defs repo), the defs still must be copied into
  `sonagi-beauty/.claude/commands/`. So B adds a second repo to maintain AND still needs the same
  mirror step. Submodules are fragile on cloud/mobile. Net: more machinery, same copy problem.
  `sonagi-agents` already shows the maintenance tax of a second definitions repo.

**Option C. Two masters (user-level + per-repo), a script keeps them identical.** Rejected: two
masters is the drift we are removing; "keep them identical" is a promise, not a mechanism.

**Recommendation: Option A.** One master folder in `sonagi-beauty`, because it adds no new repo and
sits where the OS and Claude's daily work already are. B's "clean dedicated master" is illusory: it
still requires the per-repo mirror, so it pays an extra repo for nothing. The cross-repo push that A
makes awkward is solved not by changing the master but by the sync script (below) and by fixing the
reachability question (next).

## Reachability: making it work on BOTH repos (Asma's requirement)

Asma: commands must be reachable on both `sonagi-beauty` and `sonagi-reference`. Cloud opens each
repo's DEFAULT branch. Today:
- `sonagi-beauty` default = `claude/extract-marketing-skills-z03eL` → carries the OLD claude-flow
  commands, not the real two. (This stray default is almost certainly an accident and is the direct
  cause of the "command unknown" phone failure.)
- `sonagi-reference` default = `main` → has no `.claude/commands/` at all.

Two ways to make both defaults carry the current definitions:

- **(R1) Fix the default branches** so cloud naturally opens a branch that has everything. Cleanest
  root cause: it also fixes the confusing "default is a stray `claude/...` branch" problem for clones
  and PRs. BLAST RADIUS: changing a repo's default branch can change what a fresh clone gets, what
  PRs target, and possibly what Netlify deploys. **Open unknown:** Netlify's production branch is set
  in the Netlify dashboard, not in `netlify.toml`; I cannot see it from the repo. This must be
  confirmed before touching the default, or the live site could change deploy source.
- **(R2) Leave defaults as-is; the sync script commits the definitions onto each repo's existing
  default branch.** Lower blast radius (no deploy-source change), but you keep an odd stray default
  branch on `sonagi-beauty` and you commit definitions onto branches you otherwise never work on.

R1 is better long-term and fixes a real wart; R2 is safer to ship today. The choice hinges on the
Netlify dashboard fact, which is the single thing I genuinely cannot resolve without Asma or the
dashboard.

## The sync mechanism

One script, `scripts/sync_defs.py` (commands first; structured so agents and Sonagi skills join the
same loop later). It:
1. Reads the master folder(s) in `sonagi-beauty`.
2. Writes generated mirrors, each with a "GENERATED: edit the master in sonagi-beauty, not this
   file" header, to: `~/.claude/commands/` (laptop/Mac), and the phone-facing branch of each target
   repo.
3. For the cross-repo / cross-branch targets, it operates on a local clone/worktree of the target on
   its phone-facing branch, commits, and pushes.

Run **explicitly** (a `/wrapup` step and on demand), NOT as a silent per-session hook, because:
- definitions change ~monthly, so D4 says hand-trigger, do not over-automate;
- a cross-repo commit+push is a publish-shaped action and deserves to be deliberate;
- a SessionStart hook that pushes to other repos on every cold start is fragile and noisy.

## What this is NOT (explicit scope cuts, so the build stays lean)

- NOT pulling the ~200 third-party skills onto cloud/phone (layer 4). Deferred until a specific
  skill is actually needed on mobile.
- NOT a submodule/dedicated-repo system (Option B) unless A proves insufficient.
- NOT a silent always-on sync daemon. Explicit trigger only.
- NOT a default-branch change made before the Netlify production-branch setting is confirmed.

## Open decisions for Asma (the alignment)

1. **Canonical home:** accept Option A (master in `sonagi-beauty`), or do you want B (dedicated defs
   repo) for a cleaner conceptual master despite the extra repo?
2. **Reachability:** R1 (fix the default branches, after I confirm Netlify's production branch) or R2
   (sync onto the existing defaults, no deploy-source risk)?
3. **Layer scope for this first build:** commands only now, with the script *designed* to take agents
   and Sonagi skills next (recommended), or include agents in this first pass too?
4. **The Netlify check:** do you want me to confirm the Netlify production-branch setting (you check
   the dashboard, or grant Netlify access) before R1 is even on the table?

## Recommendation in one line

Master in `sonagi-beauty` (A); one explicit `scripts/sync_defs.py` writing generated mirrors;
commands first with agents/Sonagi-skills designed to follow; reachability via R1 **only after** the
Netlify production-branch fact is confirmed, else R2. Third-party skill packs explicitly deferred.

## Review outcome (2026-06-01, fresh-context Karpathy/Gate-1 review): go LEANER (null-design v1)

A fresh-context review attacked this analysis and changed the recommendation. Verdict: fix-then-build.
The load-bearing facts above are accurate, but two corrections matter:

1. **The sync script is an over-build for v1 (Gate 1 / D4).** The payload is 2 markdown files that
   change ~monthly. A clone/worktree/commit/push script to move 2 files is machinery we do not need
   yet. Build `sync_defs.py` only when agents + Sonagi skills actually join (~12+ files across 3
   layers, the doc's own "designed to follow" trigger).
2. **The cloud/phone can never run the sync** (no `~/.claude/`, sees only the one repo it opened). So
   sync always runs from the laptop/Mac, and the phone is always a *consumer* of an
   already-pushed mirror. The whole problem collapses to: "from the laptop, make sure the right
   branch of each repo has the files." Much smaller than first framed.

**Revised v1 (the null-design the script had to beat, and did):**
- **R1 root-cause fix:** correct `sonagi-beauty`'s stray default branch so a phone opening it wakes
  up with the current commands. Do this ONLY after confirming Netlify's production branch (dashboard),
  so the live site's deploy source does not change underneath us.
- **Edit-in-place master:** keep the human-edited master at `~/.claude/commands/` on the laptop; the
  repo copy is the mirror, refreshed by a ~2-line manual step in `/wrapup`
  (`Copy-Item` then `git add/commit/push`). No Python, no cross-repo push machinery.
- **Both repos (Asma's requirement):** `sonagi-reference` is already cloned locally, so the same
  manual copy step places the commands on its phone-facing branch. No new mechanism.
- **Cross-repo push risk dissolves:** because sync runs only where the clones + auth already exist
  (laptop/Mac), the fragile "push to another repo's branch from a machine that may not have it
  cloned" path is avoided in v1.
- **Keep:** explicit-trigger over a hook (reviewer confirmed: a SessionStart hook pushing to other
  repos every cold start would be fragile and noisy). Add a decision-log line for the canonical home
  (register-on-creation).
- **Graduation trigger:** when agents + Sonagi skills join, revisit `sync_defs.py` as the real
  mechanism; v1 is deliberately manual.

Full review retained in session history (2026-06-01). Net: ship the analysis, build the null-design,
defer the script and the third-party skill packs.
