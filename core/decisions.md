# decisions.md: standing decisions (do not re-litigate)

> Append-only log of deliberate choices that a fresh session (or a reviewer) might
> otherwise question and accidentally reverse, causing a regression. NOT loaded into
> every session (that would bloat token zero); the kernel just carries a pointer here,
> and you read this file on demand, before questioning or changing a settled choice.
> Each entry: the
> decision, the reason (the background you need before flagging it), the implication,
> and the owner. If you think a decision is wrong, raise it with Asma; do NOT silently
> undo it. Canonical human-brain copy lives in the Notion decisions log; this is the
> machine-brain cache for cold-start.

## 2026-06-01: The sonagi-beauty GitHub repo is PUBLIC, on purpose
- **Decision:** `asmabak/sonagi-beauty` is a PUBLIC repository, intentionally. Keep it public.
- **Reason (background):** Asma made it public to get the website publishing through Netlify, a private repo blocked that path. It also backs GitHub Pages (`asmabak.github.io/sonagi-beauty`).
- **Implication:** the Stop-hook auto-push (`scripts/push_repo.py`) publishes committed work to a public repo every session. That is accepted, it is not a charter violation. The charter's older "private-backup push" wording is inaccurate and should be reworded in Notion (the push is a public-by-design backup).
- **Hard guard:** because it is public, NEVER commit secrets or credentials, and keep all working/strategy content gitignored (it lives in OneDrive). Do NOT flip the repo to private without first confirming Netlify publishing and GitHub Pages will not break.
- **Owner:** Asma.

## 2026-06-01: The em-dash ban is for content writing only, not code
- **Decision:** the no-em-dash rule applies to content (articles, copy, captions, prose), not to code or config files.
- **Reason:** em dashes in code comments/strings do not reach a reader and are not worth the time to strip.
- **Implication:** the pre-commit gate (`evals/em_dash_lint.py --staged`) scans prose file types only (.md, .mdx, .txt, .html) and skips code. Explicit-file linting still scans anything passed.
- **Owner:** Asma.

## 2026-06-01: The old no-mirror principle is RETIRED
- **Decision:** the 2026-05-12 "no-mirror" rule (Notion is the ONLY source; any on-disk file duplicating Notion content is stale by definition and gets deleted, not reconciled) is retired.
- **Reason:** superseded by the two-brains model. Notion is the human brain; Git (the repo plus `~/.claude/`) is the machine brain. A running agent loads executable definitions, indexes, and maps from files on disk, so those legitimately live in git, not only in Notion.
- **Implication:** version-controlled mirrors that FOLLOW A MASTER are allowed and expected (the `core/` caches, the laptop and cloud clones, the `~/.claude/agents` runtime cache of the Notion roster). Do NOT delete on-disk code/definitions just because related content exists in Notion.
- **Surviving rule:** one canonical home per item; mirrors only follow their master; never hand-edit a second copy. Recorded on the AI Ops page decision log + Charter section 2.
- **Owner:** Asma.

## 2026-06-01: Bias to skills over agents; a review standard is a skill
- **Decision:** default new capabilities to skills; create an agent only when it names a distinct look-decide-act loop an existing agent plus a skill cannot do. Do not create persona/celebrity-named agents.
- **Reason:** v4 "few agents, many shared skills" and "deprecate the dead"; the ownable artifact of a review is its rubric, not a persona.
- **Implication:** review work runs via the `engineering-review` skill in a fresh context, not a standing reviewer agent.
- **Owner:** Asma.

## 2026-06-02: Command/definition portability across devices, canonical home + v1 mechanism
- **Decision:** the canonical master for ownable definitions (commands first; agents + Sonagi skills to follow) is the `sonagi-beauty` repo under `.claude/`. Every other copy (`~/.claude/`, the other repo's branches) is a generated mirror that follows it, never hand-edited. v1 keeps the sync MANUAL (no `sync_defs.py` yet); build the script only when agents + skills join (~12+ files). Cloud/phone reachability solved by R2: commit the commands onto each repo's EXISTING default branch (no default-branch change, no Netlify deploy-source risk).
- **Reason (background):** a cloud/phone session sees only the repo it opens, on that repo's default branch, and Claude Code has no account-level command store. `/lets-start-sonagi` failed on a phone because neither repo's default branch carried it. Full analysis + a fresh-context Karpathy/Gate-1 review in `OS/device-portability-architecture.md`: the review cut the originally-proposed sync script as over-build for 2 monthly-changing files (Charter D4), and showed the phone is always a consumer, so the problem reduces to "from the laptop, put the files on the right branch."
- **Implication:** `lets-start-sonagi.md` is universal (byte-identical everywhere) and propagated verbatim. `wrapup.md` has DIVERGED between the two repos (sonagi-beauty 182 lines incl. Build Chart/Manifest/Charter ids; sonagi-reference 161 lines) and was NOT unified, each repo's own version sits on its own default branch. Whether wrapup should be one universal command or legitimately per-repo is an OPEN decision for Asma. The third-party skill packs (~200, junctioned from ~20 external repos) are explicitly deferred, not portable to cloud in v1.
- **Open follow-ups:** (1) reconcile or formally split `wrapup.md`. (2) R1 cleanup later: both repos' default branches are stray/near-empty (`claude/extract-marketing-skills-z03eL`; `main` is just an initial commit) and only safe to repoint after confirming Netlify's production branch in the dashboard. (3) wire the manual mirror-refresh step into `/wrapup` once wrapup is reconciled. (4) version-control `~/.claude/commands/` before the Mac move.
- **Owner:** Asma.
