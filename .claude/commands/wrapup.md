---
name: wrapup
description: Wrap up the current session for a clean handover. Writes the local daily snapshot, mirrors the full handover to the Notion 🤝 Session Handoffs database, marks prior handovers for this stream as Superseded, and prints the link the user can hand to /lets-start-sonagi next time.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, TodoWrite, mcp__58be3a19-e5a3-469b-be1a-bef8e58dd948__notion-search, mcp__58be3a19-e5a3-469b-be1a-bef8e58dd948__notion-fetch, mcp__58be3a19-e5a3-469b-be1a-bef8e58dd948__notion-update-page, mcp__58be3a19-e5a3-469b-be1a-bef8e58dd948__notion-create-pages, AskUserQuestion
---

# `/wrapup` — session handover protocol

You are wrapping the current session. Asma will close the chat after you finish. The next session opens with ZERO context and will run `/lets-start-sonagi` to pick the handover up. Your job is to leave the next session everything it needs.

Follow the steps below in order. Do not skip steps. Do not parallelise — the order matters because step N reads what step N-1 wrote.

## Canonical identifiers (do not invent, do not change)

- **Notion handover database (data source):** `d97e5d4f-d188-4998-8480-e579a80544f0`
- **Notion handover database (page URL):** https://www.notion.so/b6cd589c158d4b7095666bc88632933f
- **soul.md page id:** `36878492-123f-81fe-b75b-c9040cae1d7f`
- **Stream values (Select, EXACT strings):** `Sonagi Reference`, `Social Content`, `LinkedIn Agent`, `Brand Strategy & Sonagi OS`, `Site & E-commerce`, `Newsletter (Le Petit Rituel)`, `Paid Ads`, `Visual Production`, `Other`
- **Status values (Select, EXACT strings):** `Open — next session picks up`, `Picked up — in flight`, `Completed`, `Superseded`
- **Sonagi OS Build Chart (data source):** `d50113dc-b969-47e7-ae0a-a92841ece1e0`
- **Sonagi OS Manifest (data source):** `4c9a8b5b-f88f-415d-b0bb-ffb04ca6f00b`
- **Sonagi OS Charter (page):** `37178492-123f-8101-b440-e2aeb2abc568`

## 0. Pre-flight

- `git status` — note any uncommitted changes.
- `git log --oneline --since="<today's date> 00:00"` — remember what shipped this session.
- `gh pr view --json url,state,headRefName 2>/dev/null` if a PR exists.
- Read `state/_protocol.md` once (defines when state files get written).
- Read `CLAUDE.md` "Workflow rules" + `EDITORIAL-BIBLE.md` "Entry structural protocol" so you can quote the latest binding rules in the handover.

## 0b. Branch lock check (Sonagi Reference only)

Before any commit, run `git branch --show-current`. If the result is anything other than `phase-0/init` (e.g. `main`, `claude/sonagi-reference-onboarding-XXXX`), STOP. The work belongs on `phase-0/init`. Switch with `git switch phase-0/init`, cherry-pick this session's commits onto it if needed, then continue wrapup. Per CLAUDE.md branch-lock rule (Asma 2026-05-28). Do NOT push to a `claude/...` worktree branch or to `main`.

## 1. Commit any loose work

If `git status` shows modified files that belong to the session's work (not noise in `state/`, not `.cache/`, not `node_modules/`), commit them with a self-contained message. Do not bundle unrelated changes. If anything is in a half-shipped state (validation failing, hero not viewed, etc.), STOP and surface to Asma — do not paper over with a wrapup commit.

## 2. Build + validate (skip if no content/template changes this session)

```bash
python scripts/validate-schema.py 2>&1 | tail -3
python scripts/generate-html.py 2>&1 | tail -3
```

Both must succeed if you touched anything that affects the build. If either fails, fix the failure before continuing.

## 3. Determine the stream

Infer the stream from the working directory and the session's commits:

- `sonagi-reference` repo → almost always `Sonagi Reference`
- `sonagi-beauty` repo → could be any of `Social Content`, `LinkedIn Agent`, `Brand Strategy & Sonagi OS`, `Newsletter (Le Petit Rituel)`, `Paid Ads`, `Visual Production`. Read the commit subjects to infer.
- Mixed sessions → use the dominant stream OR ask the user with AskUserQuestion.

If unambiguous from cwd + commits, set the stream and move on. If ambiguous, use AskUserQuestion to ask "Which stream did this session cover?" with the 9 stream values as options.

## 4. Get the live preview URL

The current working branch deploys to a Netlify deploy-preview URL.

```bash
git rev-parse --abbrev-ref HEAD
gh pr view --json url,number 2>/dev/null
```

Build the preview URL: `https://deploy-preview-<PR_NUMBER>--<site-slug>.netlify.app/`. Verify it 200s with `curl -sI`. If preview is unreachable, fall back to production. Note both in the handover.

## 5. Write the local daily handoff snapshot

Append or create `state/_daily-handoff/YYYY-MM-DD.md`. Use prior handoffs (e.g. `state/_daily-handoff/2026-05-28.md`) as the template. Required sections:

- Frontmatter line: Outgoing from / For / Branch / Launch gate state
- **What this session shipped** — every commit grouped logically (infra / content / fix / process), with SHA + one-line summary
- **Open follow-ups carried in** — anything flagged that did NOT get done this session, with verbatim user words if available
- **Next session queue** — priority-ordered, with enough detail to start without re-asking
- **Sources already verified** — PMID / ISBN / URL for any content work queued
- **Standing rules / locks landed this session** — quote any new CLAUDE.md or EDITORIAL-BIBLE.md rule with date stamp + verbatim directive
- **Branch / preview / production state at session close**

## 6. Mark prior open handovers for this stream as Superseded

Query the Session Handoffs database for entries where Stream = <this stream> AND Status = "Open — next session picks up". For each, update Status to "Superseded". Only ONE handover per stream should be Open at any time — that's the one `/lets-start-sonagi` will read.

Use `notion-search` with `data_source_url: "collection://d97e5d4f-d188-4998-8480-e579a80544f0"` and a query that matches the stream name. Filter results to status=Open. Update each via `notion-update-page` with `command: "update_properties"` setting `Status: "Superseded"`.

## 6b. Update the Sonagi OS Build Chart + Manifest (OS-build sessions only)

If this session advanced the OS build (usually the `Brand Strategy & Sonagi OS` stream):

- **Build Chart** (`d50113dc-b969-47e7-ae0a-a92841ece1e0`): set the rows you advanced to `Done` and paste the proof (commit SHA, Notion URL). Add rows for new planned work with a concrete `Next action`.
- **Manifest** (`4c9a8b5b-f88f-415d-b0bb-ffb04ca6f00b`): if you created, changed, cached, or retired an agent or skill, add or update its row (name, type, one-line purpose, trigger, pointer, freshness). This is register-on-creation / deprecate-the-dead per the Charter.

Skip this section entirely for non-OS sessions.

## 7. Create the new Notion handover page

Use `notion-create-pages` with `parent: {type: "data_source_id", data_source_id: "d97e5d4f-d188-4998-8480-e579a80544f0"}`.

Page properties (REQUIRED — set ALL of these):
- `Title`: `YYYY-MM-DD — <stream> — <one-line scope>` (under 120 chars)
- `date:Date:start`: `YYYY-MM-DD` today
- `Stream`: exact stream string from §3
- `Status`: `Open — next session picks up`
- `Branch`: current branch name
- `Preview URL`: the verified preview URL
- `Production URL`: production URL (note 503 status if applicable)
- `PR URL`: PR URL if open
- `Last commit`: `<sha> <subject>` of the latest commit on this branch
- `Open follow-ups`: 1-3 sentence summary
- `Created by`: `Claude Code session <session_id prefix> (<model>), <date>`

Page content (Notion-flavored Markdown — the full handover prompt the next session will ingest):

```
> 🟡 OPEN — next /lets-start-sonagi for the <Stream> stream picks this up. Created <YYYY-MM-DD> at end-of-session by Claude.

## How to use this entry
This handoff page IS the prompt for the next session. /lets-start-sonagi reads it in full when the user picks <Stream>, then follows the protocol below.

## Mandatory reads BEFORE touching any work
1. soul.md — Notion page id 36878492-123f-81fe-b75b-c9040cae1d7f. Read in FULL.
2. <local daily-handoff path you just wrote>
3. <repo>/CLAUDE.md
4. <repo>/EDITORIAL-BIBLE.md (if Sonagi Reference stream)
5. <repo>/schemas/<category>.schema.json (if working on a typed content category)

## Standing skills the next session must use
<list relevant skills for this stream — humanizer, branded-ai-design, medical-fact-checker, copywriting, seo-content, etc.>

## Protocol — binding rules
<paste / summarize the binding rules from CLAUDE.md + EDITORIAL-BIBLE.md that apply to this stream. 10-14 numbered rules.>

## Next session queue (priority order)
<paste from the local daily handoff — items A, B, C, ... with full briefs>

## Sources already verified
<paste from the local daily handoff>

## Branch / preview / production state at session close
<paste from the local daily handoff>

## End of handover
Next session: confirm scope with Asma, then start work.
```

The page body must be COPY-PASTE READY — the next session reads it and acts. Don't reference "see the local file" for content the next session can't reach without context.

## 8. Print the deliverable in chat

After steps 0-7 succeed, output a single chat message with:

1. One-line status: `Session wrapped. Handover at <Notion URL>.`
2. The Notion page URL (clickable).
3. The preview URL.
4. One short paragraph naming the open follow-ups so Asma sees them.
5. Reminder: `Next session: type /lets-start-sonagi → pick <Stream> when asked.`

DO NOT print the full handover prompt block in chat anymore. The Notion page IS the prompt. Asma doesn't have to copy-paste anything — the next session pulls it directly.

## 9. Clear the crash checkpoint, then stop

This session ended cleanly, so its continuity lives in the daily handoff and the Notion row above, NOT in the emergency crash banner. Clear the checkpoint so the next session does not falsely think this one crashed:

```bash
python3 scripts/clear_checkpoint.py
```

(SessionEnd also does this automatically; running it here guarantees a wrapped session never nags the next one with a stale resume banner.)

Do not start new work. Do not run "one more thing." The session ends here.

## Failure modes to avoid

- **Skipping the live-page view.** If you committed CSS/template/content changes this session and never loaded the rendered page, that's the same bug pattern Asma has bounced back repeatedly. View it before wrapping.
- **Forgetting to mark prior handovers Superseded.** Two Open handovers for the same stream confuses /lets-start-sonagi. Only one Open per stream at a time.
- **Writing the handover from memory.** Read `git log`, read the actual files. Memory hallucinates.
- **Burying open issues.** Name them in "Open follow-ups" with the specific blocker. Do not pretend they are done.
- **Generic next-session queue.** If the queue could apply to any session, it is useless. Cite specific files, URLs, Asma directives from this session.
- **Wrong stream.** Picking `Other` when one of the 8 named streams fits causes the next session to load the wrong context. Use `Other` only when the work genuinely doesn't fit elsewhere.
- **Handover as a standalone page.** Every handover is a ROW in the Session Handoffs DB with a `Stream`, never a loose Notion page. A standalone handover is invisible to `/lets-start-sonagi` (it filters the DB by Stream + Status=Open). If you find a loose handover page, migrate it into the DB as a row. This is the "current state vs history" rule: exactly one `Open` row per stream is the live state; everything else is `Superseded` history, hidden by the "Current — one per stream" view.
