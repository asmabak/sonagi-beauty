---
name: lets-start-sonagi
description: Start a new Sonagi session cleanly. Asks which stream to cover, then reads soul.md + the latest Open Notion handover for that stream + relevant standing files before touching any work.
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, mcp__58be3a19-e5a3-469b-be1a-bef8e58dd948__notion-search, mcp__58be3a19-e5a3-469b-be1a-bef8e58dd948__notion-fetch
---

# `/lets-start-sonagi` — session pickup protocol

You are starting a new Sonagi session. You have ZERO context. Do NOT touch any work, write any code, draft any content, or call any tool other than the ones in this protocol until step 5 finishes.

## Canonical identifiers

- **Notion handover database (data source):** `d97e5d4f-d188-4998-8480-e579a80544f0`
- **Notion handover database (page URL):** https://www.notion.so/b6cd589c158d4b7095666bc88632933f
- **soul.md page id:** `36878492-123f-81fe-b75b-c9040cae1d7f`
- **Stream values (EXACT strings):** `Sonagi Reference`, `Social Content`, `LinkedIn Agent`, `Brand Strategy & Sonagi OS`, `Site & E-commerce`, `Newsletter (Le Petit Rituel)`, `Paid Ads`, `Visual Production`, `Other`

## Step 1 — Ask the user which stream

This is the FIRST thing you do. No prior step, no other tool call. Use `AskUserQuestion` with this exact question:

> Which stream should I cover?

Single-select options (recommended order):
1. **Sonagi Reference** — encyclopedia + Édito, sonagi-reference repo
2. **Social Content** — TikTok / Instagram / Reels / Stories, sonagi-beauty repo
3. **LinkedIn Agent**
4. **Brand Strategy & Sonagi OS**
5. **Site & E-commerce** — sonagibeauty.com / Shopify
6. **Newsletter (Le Petit Rituel)**
7. **Paid Ads** — Meta / Google / TikTok / LinkedIn
8. **Visual Production** — Higgsfield / Seedance / Midjourney
9. **Other** — free text, ask the user to describe

Wait for the user's answer. Do not assume from cwd or recent git activity — the user's intent for THIS session is the source of truth.

## Step 2 — Read soul.md (LOCAL FIRST — Notion is the mirror)

Read `~/.claude/soul.md` with the Read tool (the canonical master, synced to every project repo by `~/.claude/sync-soul.sh`). Only if that file is missing, fall back to `notion-fetch` with `id: "36878492-123f-81fe-b75b-c9040cae1d7f"`. Never block a session on Notion being reachable. Read the FULL file. The "did I do the work, or did I do enough to look like I did the work?" doctrine governs every decision in this session. Internalize it before reading anything else.

## Step 3 — Find and read the latest Open handover for the chosen stream

Use `notion-search` with:
- `data_source_url: "collection://d97e5d4f-d188-4998-8480-e579a80544f0"`
- `query`: the chosen stream name (e.g. "Sonagi Reference")
- `page_size`: 5

From the results, identify the most recent page where Status = `Open — next session picks up` AND Stream = <chosen stream>. There should be exactly ONE (the `/wrapup` skill enforces this by marking older ones as `Superseded`).

- **Zero Open entries:** tell the user "No Open handover found for <Stream>. Please brief me on what to work on." STOP. Wait for the user.
- **Multiple Open entries:** read all of them, flag to the user that the /wrapup discipline slipped (older ones should have been marked Superseded), then proceed with the most recent.

Use `notion-fetch` with the page id of the chosen Open handover. Read the FULL body — that body IS your prompt for this session. Do not skim. Do not summarize before you read.

## Step 4 — Read the stream-specific standing files

If you have filesystem access (Read tool), also read these. If you don't, note them and ask the user to paste relevant excerpts if anything ambiguous comes up.

| Stream | Standing files to read |
|---|---|
| Sonagi Reference | `~/sonagi-reference/CLAUDE.md`, `~/sonagi-reference/EDITORIAL-BIBLE.md`, relevant `schemas/<category>.schema.json` |
| Social Content | `~/sonagi-beauty/CLAUDE.md`, `~/sonagi-beauty/SESSION-STATE.md`, `~/higgsfield-seedance2-skills/MINJUN-CHARACTER-SHEET.md`, `~/higgsfield-seedance2-skills/MINJUN-PRODUCTION-BIBLE.md` |
| LinkedIn Agent | LinkedIn Founder Carousel Guidelines (Notion `36d78492-123f-8151-877a-f59fb15b5509`), Asma's LinkedIn Founder Voice (Notion `36d78492-123f-8190-a4e8-c13ff0dcc61a`), The Asma File (Notion `36d78492-123f-816f-acac-ca06413c3dbf`), 09 — AI Operating Layer (Notion `35e78492-123f-8165-97c1-f824cef08601`), LinkedIn-EN Founder Strategy (Notion `36d78492-123f-8171-8868-cbed7bef005c`) |
| Brand Strategy & Sonagi OS | `~/sonagi-beauty/CLAUDE.md`, Sonagi root Notion page `35678492-123f-819e-bd07-e568cbd24049`, Sonagi OS — FR (Notion `35778492-123f-81e1-a082-dce9bec80e48`) |
| Site & E-commerce | sonagibeauty.com Shopify state (ask user), Returns & Dispute SLA (Notion `36478492-123f-81ea-a7a6-e810b0928c49`) |
| Newsletter (Le Petit Rituel) | Newsletter spec in Social Content Hub (Notion `36178492-123f-8144-9db1-cb7652d5835c`) |
| Paid Ads | ads skills at `~/.claude/skills/ads/`, ads-audit agents at `sonagi-beauty/.claude/agents/` |
| Visual Production | `~/sonagi-reference/EDITORIAL-BIBLE.md` section F (hero rules), `~/higgsfield-seedance2-skills/MINJUN-PRODUCTION-BIBLE.md`, branded-ai-design skill at `~/.claude/skills/anthropic/` |
| Other | Ask the user. |

## Step 4b — Branch lock (Sonagi Reference only)

If the chosen stream is `Sonagi Reference` AND you have Bash access, your VERY FIRST tool call before reading any local file is:

```bash
git branch --show-current
```

If the output is anything OTHER than `phase-0/init` (e.g. `main`, `claude/sonagi-reference-onboarding-XXXX`, any auto-generated worktree branch), immediately run:

```bash
git switch phase-0/init
```

If `phase-0/init` is not present locally, fetch it: `git fetch origin phase-0/init:phase-0/init && git switch phase-0/init`.

Do NOT ask the user "which branch should I use" — the answer is permanently `phase-0/init` until launch (per CLAUDE.md "Branch lock" rule, Asma 2026-05-28). The `claude/...-XXXX` worktree branches Claude Code spawns are based on `main` and are EMPTY of the actual build (no schemas, no scripts, no 66 articles). Working on them is broken by definition.

## Step 5 — Confirm scope with the user

After steps 1-4, output a single message:

1. One sentence: "I've read soul.md, the latest handover for <Stream> (created <date>, last commit <SHA>), and the standing files for this stream."
2. The "Next session queue" from the handover body, condensed to bullet points (A / B / C / ...).
3. ONE question: "Which queue item do you want me to start with? (Default: A, the highest priority.)"

Wait for the user's pick. Only after they answer do you start work.

## Failure modes to avoid

- **Skipping step 1.** Never start working without explicitly asking which stream. The user's intent for THIS session is the most important input.
- **Reading the handover from memory.** Always `notion-fetch` the actual page. Memory hallucinates dates, commits, and queue items.
- **Skipping soul.md.** The doctrine read happens every session, not just "the first time." It re-anchors discipline.
- **Starting work in step 5.** Confirm queue item with the user first. Skipping the confirmation is the same "look productive vs be productive" failure soul.md warns against.
- **Trusting Superseded entries.** Only the one entry with Status = `Open — next session picks up` for the chosen stream is the source of truth.
