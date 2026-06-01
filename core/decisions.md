# decisions.md: standing decisions (do not re-litigate)

> Append-only log of deliberate choices that a fresh session (or a reviewer) might
> otherwise question and accidentally reverse, causing a regression. Loaded at token
> zero via the kernel, so the background travels with every session. Each entry: the
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

## 2026-06-01: Bias to skills over agents; a review standard is a skill
- **Decision:** default new capabilities to skills; create an agent only when it names a distinct look-decide-act loop an existing agent plus a skill cannot do. Do not create persona/celebrity-named agents.
- **Reason:** v4 "few agents, many shared skills" and "deprecate the dead"; the ownable artifact of a review is its rubric, not a persona.
- **Implication:** review work runs via the `engineering-review` skill in a fresh context, not a standing reviewer agent.
- **Owner:** Asma.
