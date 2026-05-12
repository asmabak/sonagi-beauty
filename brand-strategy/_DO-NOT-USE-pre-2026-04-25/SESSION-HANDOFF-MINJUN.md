# Session Handoff — Minjun AI Influencer Project
## Read this ENTIRE document before doing anything

---

## WHAT THIS PROJECT IS

We're building **Minjun (@minjun.skin)** — an AI-generated Korean-American male skincare influencer for TikTok/Reels/Shorts. He's early-to-mid 20s, lives in Paris, speaks English (not French — French voice was tested and sounds terrible). He reviews K-beauty products in short-form video content.

His on-camera energy is inspired by **Edward Zo** — playful, witty, talks to camera like FaceTiming his best friend. Reference screenshots saved in the project files.

---

## WHAT WE DID SO FAR

### 1. Character & Scripts (previous session)
- Created full character sheet, 5 video scripts, image prompts
- Generated reference images on Higgsfield (hero portrait, expressions, hair variants)
- Tested voice options — final pick was Higgsfield's built-in English voice

### 2. Higgsfield Testing (this session)
- Tested Script 05 on Higgsfield Seedance 2.0
- **Problems discovered:**
  - Max 15s per generation — had to split into 3 clips
  - Character changes between clips (different face, different background)
  - Background never stays consistent across separate generations
  - French voice was dull and unnatural — switched to English
  - First attempts used wrong prompt format (labeled blocks). Seedance needs flowing paragraphs with time segments (0-5s, 5-10s, 10-15s), 60-100 words max
- **What worked:** Final Clip A prompt produced a great video with good voice, good expressions, correct skin damage visible. This video is saved as the reference.

### 3. Production Bible & Skills
- Created `MINJUN-PRODUCTION-BIBLE.md` — universal rules for camera, interaction, product rendering, settings
- Created reusable video scripting skills (Seedance prompt guide, character bible template, script writing template)
- All pushed to GitHub at `asmabak/sonagi-beauty`

### 4. Decision: Migrate to Creatify
- Higgsfield can't maintain consistency across clips → switching to **Creatify** (creatify.ai)
- Creatify supports: up to 10-minute videos, custom avatar from photo, consistent character, API + MCP automation, 75+ language lip-sync
- User created a Creatify account (email: asma.bakhtar@gmail.com)
- Extracted Minjun's voice from the best Higgsfield video for voice cloning

---

## WHAT NEEDS TO HAPPEN NOW

### Step 0: Search for skills and knowledge FIRST

Before starting any work, search for and install relevant skills:

1. **Search GitHub for Creatify skills/MCP tools:**
   - `@tsavo/creatify-mcp` — MCP server for Creatify API (npm package, ready to install)
   - Search for any other Creatify Claude Code skills, prompt templates, or automation tools
   - Search: `creatify MCP claude`, `creatify API automation`, `creatify avatar creation guide`

2. **Search for AI avatar creation skills:**
   - Search GitHub for: `AI avatar creation`, `AI influencer automation`, `virtual influencer tools`, `AI UGC generator`
   - Look for Claude Code skills or MCP servers related to AI video generation, avatar management, content pipelines
   - Check if there are skills for voice cloning, lip-sync automation, or batch video generation

3. **Read the skills we already created and saved:**
   - `C:\Users\marou\higgsfield-seedance2-skills\SEEDANCE-PROMPT-GUIDE.md` — complete video prompt writing guide (format, camera language, what works/doesn't, UGC tips). Useful even for non-Seedance platforms.
   - `C:\Users\marou\higgsfield-seedance2-skills\UGC-CHARACTER-BIBLE-TEMPLATE.md` — reusable template for building any AI influencer character (identity, camera angles, interaction energy, settings, product interaction, caption system)
   - `C:\Users\marou\higgsfield-seedance2-skills\SCRIPT-WRITING-TEMPLATE.md` — fill-in-the-blank template for 45-second social media videos, hook formulas, dialogue rules, series planning
   - `C:\Users\marou\higgsfield-seedance2-skills\MINJUN-PRODUCTION-BIBLE.md` — Minjun-specific production rules (Edward Zo energy, camera angles A-D, product/texture rendering, bathroom setting, anti-patterns from Higgsfield v1)
   - These are also on GitHub at `asmabak/sonagi-beauty` (branch: `claude/extract-marketing-skills-z03eL`)

4. **Read the Creatify API docs:**
   - Main API page: `https://creatify.ai/api`
   - Full docs: `https://docs.creatify.ai/api-documentation/`
   - Personas endpoint: `https://api.creatify.ai/api/personas_v2/` (for creating custom avatars)
   - Understand how to: create a persona, upload face image, clone voice, generate video with custom avatar

### Step 1: Set up Playwright with EDGE (not Chrome)

Chrome Playwright is broken in this environment — it locks between sessions. Use Edge instead:

```
npx @playwright/mcp@latest --browser msedge
```

Or configure the Playwright MCP server to use Edge in settings. This is critical — Chrome will fail.

### Step 2: Help user find Creatify API credentials

Navigate to creatify.ai with Playwright, help user log in (Google account: asma.bakhtar@gmail.com), and find:
- **X-API-ID** — API identifier
- **X-API-KEY** — secret API key

These are in Settings/API/Developer section somewhere in the Creatify dashboard. User hasn't found them yet.

### Step 3: Install Creatify MCP server

```
npm install -g @tsavo/creatify-mcp
```

Configure with user's API credentials. This allows generating videos directly from Claude Code sessions.

### Step 4: Create Minjun avatar on Creatify

Using Creatify's persona/avatar system, create Minjun with:
- **Face:** Upload `hero-v4.jpg` as the anchor face
- **Voice:** Clone from `minjun-voice-clip.mp3` (extracted from the approved Higgsfield video the user loved)
- **Reference video:** `Minjun best.mp4` — the gold standard for how Minjun should look and sound
- **Character details:** See `MINJUN-CHARACTER-SHEET.md` and `MINJUN-PRODUCTION-BIBLE.md`

### Step 5: Generate Script 05 as a single continuous video

No more 3-clip stitching. Creatify can do up to 10 minutes. Generate the full 45-second video in one go. The complete English script is at the bottom of this document.

### Step 6: If Script 05 works, adapt and generate Scripts 01-04

All 5 scripts exist in the repo but are in French and formatted for Seedance. They need:
- Translation to English
- Reformatting for Creatify's system
- Same Minjun avatar and voice throughout

---

## WHERE ALL THE FILES ARE

### Main project repo (cloned from GitHub):
`C:\Users\marou\higgsfield-seedance2-skills\`
- `MINJUN-CHARACTER-SHEET.md` — full character description
- `MINJUN-PRODUCTION-BIBLE.md` — universal production rules (camera angles, interaction style, product rendering, anti-patterns)
- `MINJUN-NANOBANANA-PROMPTS.md` — image generation prompts
- `SCRIPT-01-MACRO-HOOK-GLASS-SKIN.md` — Mixsoon Bean Essence (French, needs English rewrite)
- `SCRIPT-02-CELEBRITY-REACTION-PORES.md` — COSRX Snail Mucin (French, needs English rewrite)
- `SCRIPT-03-CLINIC-VLOG-BRIGHTENING.md` — Anua Niacinamide Serum (French, needs English rewrite)
- `SCRIPT-04-STRANGER-STORY-SPF.md` — Beauty of Joseon SPF (French, needs English rewrite)
- `SCRIPT-05-BEFORE-AFTER-BARRIER.md` — Anua Heartleaf Toner (French, original)
- `SCRIPT-05-CLIPS-BARRIER-REPAIR.md` — Script 05 rewritten as 3x15s English clips for Seedance
- `SEEDANCE-PROMPT-GUIDE.md` — video prompt writing guide (reusable skill)
- `UGC-CHARACTER-BIBLE-TEMPLATE.md` — character bible template (reusable skill)
- `SCRIPT-WRITING-TEMPLATE.md` — script writing template (reusable skill)
- `GENERATE-NOW-SCRIPT05.md` — original Seedance generation instructions
- GitHub remote: `https://github.com/beshuaxian/higgsfield-seedance2-jineng.git` (READ ONLY — not user's repo, DO NOT push here)

### Reference images:
`C:\Users\marou\images\2026-04-15\minjun-reference\`
- `hero-v4.jpg` — **THE anchor face for Minjun** (use for avatar creation)
- `minjun bathroom.jpg` — approved bathroom from Clip A
- `expr-conspiracy.jpg`, `expr-disgusted.jpg`, `expr-smile.jpg` — expression refs
- `edwardzo-reel1.jpg`, `edwardzo-reel2.jpg`, `edwardzo-reel3.jpg` — Edward Zo style references
- `inspiration screen settings Minjun script5.jpg` — TikTok format inspiration (overlay photos at top)
- `anua-heartleaf-77-toner-padded.jpg` — product image (padded for aspect ratio)

### Script 05 working files:
`C:\Users\marou\images\2026-04-16\Minjun_script5\`
- `CLIP-A-HOOK.txt` — Clip A prompt (English, approved format)
- `CLIP-B-APPLICATION.txt` — Clip B prompt (English)
- `CLIP-C-RESULT.txt` — Clip C prompt (English)
- `minjun-voice-clip.mp3` — **extracted voice for cloning on Creatify**
- `Minjun best.mp4` — **THE approved video** (user loved this — gold standard)

### User's own GitHub repo (CAN push here):
`C:\Users\marou\sonagi-beauty\` — GitHub: `asmabak/sonagi-beauty`
- Skills files on branch `claude/extract-marketing-skills-z03eL`

### Memory files:
`C:\Users\marou\.claude\projects\C--Users-marou\memory\`
- `project_minjun_character.md` — character overview
- `project_production_bible.md` — production rules reference
- `project_creatify_migration.md` — why we moved to Creatify
- `user_creative_projects.md` — user background
- `feedback_save_work.md` — always save work, search thoroughly

---

## IMPORTANT RULES

1. **User gets frustrated when work is lost between sessions.** Always save important decisions to files AND memory. Search thoroughly before saying something doesn't exist.

2. **Minjun speaks ENGLISH, not French.** French was tested and dropped — the AI voice sounded dull and unnatural.

3. **Minjun is Korean-American living in Paris.** Updated backstory.

4. **The user's GitHub is `asmabak`**, not `beshuaxian`. Never push to beshuaxian — that's someone else's repo.

5. **Edward Zo is the #1 inspiration** for Minjun's on-camera energy. Playful eyes, witty, treats camera like a person.

6. **Before/after in videos:** Use overlay photos at top of frame (added in editor), NOT split-screen generated by AI. See `inspiration screen settings Minjun script5.jpg`.

7. **Save all outputs** to `/images/YYYY-MM-DD/` folders. Never lose an asset. Append version numbers if regenerating.

8. **Use Playwright with Edge browser**, not Chrome. Chrome Playwright locks/crashes between sessions.

9. **Search for skills BEFORE starting work.** Look for Creatify skills, AI avatar creation tools, and video automation MCP servers on GitHub and npm. Install anything useful.

10. **Creatify API uses TWO credentials:** `X-API-ID` and `X-API-KEY` in request headers. User hasn't found these yet.

11. **Don't write overly verbose prompts.** The Seedance lesson applies everywhere: concise, specific, director-style language beats walls of text. Read `SEEDANCE-PROMPT-GUIDE.md` for principles.

12. **The 5 video scripts each feature a different product:**

| Script | Product | Hook Type |
|--------|---------|-----------|
| 01 | Mixsoon Bean Essence | Macro skin hook |
| 02 | COSRX Snail 96 Mucin | Celebrity reaction |
| 03 | Anua Niacinamide 10% + TXA 4% | Korean clinic vlog |
| 04 | Beauty of Joseon Relief Sun SPF50+ | Stranger story |
| 05 | Anua Heartleaf 77% Toner | Before/after (CURRENT PRIORITY) |

---

## SCRIPT 05 — FULL ENGLISH VERSION (for Creatify, single video)

Generate as ONE continuous ~45 second video:

**Hook (0-5s):** Close-up, skin visibly damaged — red irritated patches on cheeks, dry flaky texture. He touches his cheek and winces.
"OK I'm gonna be real with you. My skin right now is a disaster."

**Problem (5-10s):** Gestures counting on fingers. Frustrated but amused.
"I went way too hard on the retinol, too many exfoliants, and my skin barrier is completely wrecked."

**Tease (10-15s):** Eyebrows lift with hope, glances at product.
"But I found something."

**Product (15-25s):** Picks up Anua Heartleaf 77% toner, pumps into palm, liquid visible and glistening. Taps onto cheeks with fingertips, skin becomes wet and dewy.
"Anua Heartleaf toner. Seventy-seven percent heartleaf extract. You press gently, you never rub. You layer it and let your skin drink."

**Result (25-35s):** Skin transformed — redness gone, smooth calm dewy luminous. Touches cheek with genuine smile.
"The redness is gone. My skin is hydrated and calm. If your skin is struggling right now, stop everything. Go back to basics."

**Close (35-45s):** Holds bottle casually, warm eye contact, small smile.
"Anua Heartleaf. Take care of yourself."

**Post-production (added in editor, NOT generated by AI):**
- Text hook at top of frame for first 3-4s: "my skin was DESTROYED." (white bold, DESTROYED in red)
- Before/After overlay photos at top during result section
- Dynamic word-by-word English captions (color system in Production Bible)
- Trending TikTok music at 15-20% volume

---

## FIRST THING TO DO

1. Read this document completely
2. Read the memory files in `C:\Users\marou\.claude\projects\C--Users-marou\memory\`
3. Search GitHub/npm for Creatify skills, AI avatar creation tools, and video automation MCP servers
4. Read `SEEDANCE-PROMPT-GUIDE.md` and `MINJUN-PRODUCTION-BIBLE.md` for context
5. Set up Playwright with Edge browser
6. Help user find Creatify API credentials and set up the Minjun avatar
