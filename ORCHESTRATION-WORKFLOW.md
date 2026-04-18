# Sonagi Beauty -- Content Production Orchestration Workflow
## Master Playbook for All Content Types

**Last updated:** 2026-04-16
**Open this document at the start of every work session.**

---

## Table of Contents

1. [Master Workflow Map](#1-master-workflow-map)
2. [Workflow: New Minjun Video (End-to-End)](#2-workflow-new-minjun-video-end-to-end)
3. [Workflow: Instagram Carousel (End-to-End)](#3-workflow-instagram-carousel-end-to-end)
4. [Workflow: Weekly Content Batch](#4-workflow-weekly-content-batch)
5. [Workflow: New Product Launch](#5-workflow-new-product-launch)
6. [Workflow: Monthly Strategy Review](#6-workflow-monthly-strategy-review)
7. [Skill Reference Map](#7-skill-reference-map)
8. [Quick-Start Commands](#8-quick-start-commands)

---

## 1. MASTER WORKFLOW MAP

```
 IDEA          RESEARCH        SCRIPT         PRODUCTION      POST-PROD       PUBLISH        ANALYZE
  |               |               |               |               |              |              |
  v               v               v               v               v              v              v
+----------+ +----------+  +------------+  +------------+  +-----------+  +----------+  +-----------+
| Campaign | | Customer |  | Script     |  | Creatify   |  | Captions  |  | Social   |  | Analytics |
| Calendar | | Research |  | Writing    |  | Avatar     |  | + Music   |  | Caption  |  | Tracking  |
| + Content| | + Market |  | Template   |  | Generation |  | + Overlay |  | + Hash-  |  | + Metrics |
| Strategy | | Psych    |  | + Hook     |  | OR         |  | (CapCut)  |  | tags     |  | Review    |
|          | |          |  | Formulas   |  | Canva      |  |           |  |          |  |           |
+----------+ +----------+  +------------+  +------------+  +-----------+  +----------+  +-----------+

SKILLS USED AT EACH STAGE:

IDEA            content-strategy, marketing-ideas, full-campaign-plan.md
RESEARCH        customer-research, marketing-psychology, competitor-alternatives
SCRIPT          copywriting, social-content, SCRIPT-WRITING-TEMPLATE.md
PRODUCTION      UGC-CHARACTER-BIBLE-TEMPLATE.md, SEEDANCE-PROMPT-GUIDE.md, Creatify, Canva
POST-PROD       Dynamic caption color system (UGC-CHARACTER-BIBLE-TEMPLATE.md)
PUBLISH         social-content, community-marketing, copy-editing
ANALYZE         analytics-tracking, ab-test-setup
```

### Content Pillar Quick Reference

| Pillar | French | Goal | Primary Formats | Days |
|--------|--------|------|-----------------|------|
| EDUQUER | Eduquer | Build trust | Carousels, infographics | Mon, Wed |
| MONTRER | Montrer | Prove it works | Reels, demos, before/after | Tue, Thu |
| INSPIRER | Inspirer | Create desire | ASMR, flat lays, aesthetics | Fri, Sun |
| VENDRE | Vendre | Convert | Product spotlights, CTAs | Woven into all |

### Posting Schedule (France Time)

| Day | Format | Pillar | Time |
|-----|--------|--------|------|
| Monday | Carousel (8-10 slides) | Eduquer | 12h00 |
| Tuesday | Reel (15-30s) | Montrer | 18h00 |
| Wednesday | Carousel (7-8 slides) | Eduquer | 12h00 |
| Thursday | Reel (15-30s) | Montrer | 18h00 |
| Friday | Reel (30-60s) | Inspirer | 19h00 |
| Saturday | Stories (3-5 stories) | Engager | 10h00 |
| Sunday | Static post | Inspirer | 11h00 |

---

## 2. WORKFLOW: New Minjun Video (End-to-End)

**Time estimate:** 2-3 hours from concept to ready-to-publish
**Output:** One 45-second vertical video (9:16) for TikTok/Reels/Shorts

### Prerequisites

- Creatify account logged in (asma.bakhtar@gmail.com)
- hero-v4.jpg uploaded as Minjun avatar in Creatify
- Voice clone from minjun-voice-clip.mp3 active in Creatify
- CapCut or equivalent editor for post-production

### Step 1: Pick Script Topic

**Skill:** `content-strategy` + `full-campaign-plan.md`

- [ ] Open `content/full-campaign-plan.md` and check what is scheduled for this week
- [ ] Identify the pillar (Eduquer/Montrer/Inspirer/Vendre) for the day
- [ ] Pick the product to feature from the campaign calendar
- [ ] Confirm the hook type has not been used in the last 3 videos (rotate: macro, celebrity, clinic, stranger, before/after)

```
Claude prompt:
"Check the campaign calendar in content/full-campaign-plan.md. What Minjun video
is scheduled for [Tuesday/Thursday/Friday] of week [N]? Give me the topic,
product, and suggested hook type."
```

### Step 2: Research Product/Ingredient

**Skill:** `customer-research` + `marketing-psychology`

- [ ] Research the featured product: key ingredients, claims, price point
- [ ] Identify the target skin concern it solves
- [ ] Find the emotional angle: what pain does the audience feel about this concern?
- [ ] Check competitor content: what has performed well for this product on TikTok?

```
Claude prompt:
"Research [product name] for a Minjun video script. I need: key ingredients
and what they do, the skin concern it solves, the emotional pain point for
French women 18-35, and what competitor content about this product has gone
viral on TikTok."
```

### Step 3: Write the Hook

**Skill:** `social-content` (social hook patterns) + `SCRIPT-WRITING-TEMPLATE.md`

Choose from these proven hook formulas:

| Formula | Example |
|---------|---------|
| Vulnerable confession | "My skin was DESTROYED" |
| Stranger compliment | "A girl stopped me to ask THIS" |
| Celebrity reference | "Jungkook made me try it" |
| Reaction/shock | "Korean stars use THIS for their pores" |
| Challenge/provocative | "Don't even try this" |
| Before/after tease | "One product changed EVERYTHING" |
| Clinic authority | "I got my skin analyzed in Korea" |
| Counter-intuitive | "The WORST beauty trend from Korea" |
| Pain point | "Most people do this wrong -- it's ruining their skin" |
| Curiosity gap | "Dermatologists in Korea do this. French ones don't." |
| FOMO | "Everyone in Seoul uses this. Nobody in Paris knows about it." |

- [ ] Pick a hook formula that matches the product and emotional angle
- [ ] Write the hook line: 10-15 words maximum, mid-thought start
- [ ] Write the text overlay version: 3-5 words, bold, for top of frame

```
Claude prompt:
"Write 5 hook options for a Minjun video about [product]. Use the [hook type]
formula. Each hook should be 10-15 words, start mid-thought (no 'Hey guys'),
and feel like a friend sharing a secret. Also write the text overlay version
(3-5 words) for each."
```

### Step 4: Write Full Script

**Skill:** `copywriting` + `SCRIPT-WRITING-TEMPLATE.md`

Follow the 3x15s formula (30-40 words per clip):

| Clip | Duration | Purpose | Camera Angle | Energy |
|------|----------|---------|-------------|--------|
| A -- Hook | 15s | Grab attention | Counter Low or Shelf High | Vulnerable or Shocked |
| B -- Product | 15s | Show the product | Side Three-Quarter | Conspiratorial or Ritualistic |
| C -- Payoff | 15s | Result + sign-off | Counter Low | Amazed or Sincere |

**Dialogue rules:**
- 30-40 words per 15-second clip (in English)
- Start mid-thought -- never "Hey guys" or "So today..."
- Short punchy sentences, no complex grammar
- ONE product name mention per clip (natural, not forced)
- End Clip C with a warm personal sign-off, never a sales CTA
- Tone: friend sharing a secret, never salesperson

- [ ] Write Clip A dialogue (hook + problem + tease)
- [ ] Write Clip B dialogue (product reveal + application + technique)
- [ ] Write Clip C dialogue (result + advice + sign-off)
- [ ] Check word count per clip (30-40 words)
- [ ] Read aloud -- does it sound like Minjun (Edward Zo energy)?

```
Claude prompt:
"Write a complete Minjun video script for [product] using the [hook type] hook.
Follow the SCRIPT-WRITING-TEMPLATE: 3 clips x 15 seconds, 30-40 words per clip.
Use the hook: '[chosen hook line]'. Edward Zo energy -- playful, witty, talks to
camera like FaceTiming his best friend. End with a warm sign-off, not a sales CTA."
```

### Step 5: Generate Minjun Behaviour Prompt

**Skill:** `UGC-CHARACTER-BIBLE-TEMPLATE.md` + `SEEDANCE-PROMPT-GUIDE.md`

For each clip, write a Creatify-ready prompt using this structure:

```
A 15-second vertical video of [character description from hero-v4.jpg]
[main action] in [warm beige-grey tile bathroom]. He speaks English
with natural lip-sync, young warm voice with slight Korean accent.

0-5s: [Visual + framing + lighting]. [Expression/action].
He says: "[dialogue]"

5-10s: [Visual development]. [Gesture/expression change].
He says: "[dialogue]"

10-15s: [Energy shift]. [Transition gesture].
He says: "[dialogue]"

Camera [one instruction only]. [Lighting]. [Music direction].
```

**Critical rules from SEEDANCE-PROMPT-GUIDE:**
- 60-100 words maximum per prompt
- ONE camera instruction per clip
- Flowing paragraphs with time segments, NOT labeled blocks
- Describe what TO do, not what NOT to do
- Different camera angle per clip
- Describe lighting specifically (e.g., "warm golden vanity light from left")

- [ ] Write prompt for Clip A
- [ ] Write prompt for Clip B (different angle from A)
- [ ] Write prompt for Clip C (different angle from A and B)
- [ ] Check each prompt is under 100 words
- [ ] Save prompts to `images/YYYY-MM-DD/` folder

```
Claude prompt:
"Convert this Minjun script into 3 Creatify-ready prompts. Follow the
SEEDANCE-PROMPT-GUIDE format: time-segmented, 60-100 words each, one camera
instruction per clip, different angle per clip. Character reference is hero-v4.jpg.
Setting is the warm beige-grey tile bathroom from UGC-CHARACTER-BIBLE-TEMPLATE."
```

### Step 6: Create Avatar Video in Creatify

**Tool:** Creatify (browser-based at creatify.ai)

- [ ] Log in to Creatify (asma.bakhtar@gmail.com)
- [ ] Select the Minjun avatar (created from hero-v4.jpg)
- [ ] Select the cloned voice (from minjun-voice-clip.mp3)
- [ ] Paste the full script (all 3 clips as one continuous ~45s video)
- [ ] Set format: 9:16 vertical, 1080x1920
- [ ] Generate the video
- [ ] Review: does Minjun look consistent? Is lip-sync good? Is the energy right?
- [ ] If not satisfactory, adjust prompt and regenerate (append version number to filename)
- [ ] Download the approved video
- [ ] Save to `images/YYYY-MM-DD/` with descriptive filename

**Quality checklist:**
- [ ] Face matches hero-v4.jpg throughout
- [ ] Lip-sync matches English dialogue
- [ ] Expressions match the scripted energy per clip
- [ ] Bathroom setting is warm and consistent
- [ ] No identity drift between clips

### Step 7: Post-Production

**Tool:** CapCut, Opus Clip, or equivalent video editor
**Reference:** Dynamic Caption Color System from `UGC-CHARACTER-BIBLE-TEMPLATE.md`

- [ ] Import the Creatify video
- [ ] Add text hook overlay at top of frame (first 3-4 seconds of Clip A)
- [ ] Add dynamic word-by-word captions using the color system:

| Word Type | Color | Size | Animation |
|-----------|-------|------|-----------|
| Normal filler (the, a, is) | White #FFFFFF | 18-22pt | fade |
| Product names | Coral Pink #FF6B6B | 28-34pt | slam |
| Action words (try, apply) | Cyan #00E5FF | 24-28pt | pop-in |
| Emphasis (INSANE, NEVER) | Bright Yellow #FFD700 | 36-44pt | slam+shake |
| Negative (don't, stop) | Red #FF3333 | 30-36pt | slam |
| Korean/foreign terms | Lavender #B388FF | 28-32pt | bounce |
| Numbers/stats | Green #00FF88 | 30-34pt | slam |

- [ ] Add before/after overlay photos (if applicable) at top of frame during result section
- [ ] Add trending TikTok music at 15-20% volume
- [ ] Check transitions between clips (simple cuts work best -- angle changes are natural transitions)
- [ ] Export at 1080x1920, 30fps minimum
- [ ] Save final version to `images/YYYY-MM-DD/`

### Step 8: Write Social Caption

**Skill:** `copywriting` + `social-content` + `copy-editing`

Brand voice rules for captions:
- Intimate, educating, provocative, honest, sensory, warm
- Mix French and English naturally (audience is French women 18-35)
- Include a question or CTA to drive comments
- Keep under 2200 characters for Instagram

- [ ] Write the caption in the Sonagi brand voice
- [ ] Include a hook in the first line (visible before "...more")
- [ ] Add a clear CTA (save, share, comment, link in bio)
- [ ] Proofread with `copy-editing` skill

```
Claude prompt:
"Write an Instagram/TikTok caption for this Minjun video about [product].
Sonagi brand voice: intimate, educating, provocative, honest, sensory, warm.
Mix French and English. Start with a hook visible before the fold. End with
a CTA that drives saves or comments. Target: French women 18-35."
```

### Step 9: Publish with Hashtags and Optimal Timing

- [ ] Select hashtag set based on content type:

**Primary (every post):**
```
#sonagibeauty #kbeauty #beautecoreeenne #kbeautyfrance #skincareroutine
```

**Educational posts:**
```
#skincaretips #conseilsbeaute #routinecoreeenne #glasskin #skincareaddict #soinsvisage
```

**Product posts:**
```
#cosrx #beautyofjoseon #anua #laneige #innisfree #kbeautyeurope
```

**Engagement posts:**
```
#MonRituelSonagi #skincarecommunity #beauteasiatique #peauparfaite
```

- [ ] Schedule or post at optimal time (Reels: Tue/Thu 18h00, Fri 19h00 France time)
- [ ] Cross-post to TikTok and YouTube Shorts
- [ ] Add to Instagram Stories with a poll or question sticker for engagement

### Step 10: Track Metrics

**Skill:** `analytics-tracking`

Track these metrics 24h and 7d after posting:

| Metric | Target | Signal |
|--------|--------|--------|
| Saves | 50+ | Algorithm gold -- content has lasting value |
| Shares/DMs | 20+ | Highest weight in 2026 algorithm |
| Reel watch time | 80%+ completion | Hook is working |
| Profile visits | 100+/week | Converting viewers to followers |
| Link clicks | 50+/week | Converting followers to shoppers |

- [ ] Record metrics in tracking sheet at 24h
- [ ] Record metrics again at 7d
- [ ] Note which hook type and product drove best performance
- [ ] Flag any video with >80% watch time as a format to repeat

---

## 3. WORKFLOW: Instagram Carousel (End-to-End)

**Time estimate:** 1-1.5 hours from concept to ready-to-publish
**Output:** One 7-10 slide carousel for Instagram
**Schedule:** Monday 12h00 and Wednesday 12h00 (France time)

### Step 1: Pick Topic from Campaign Calendar

**Skill:** `content-strategy`

- [ ] Check `content/full-campaign-plan.md` for this week's carousel topics
- [ ] Confirm the pillar: Eduquer carousels are educational/instructional
- [ ] Identify the core takeaway: what should someone SAVE this carousel for?

```
Claude prompt:
"Check the campaign calendar. What carousel is scheduled for [Monday/Wednesday]
of week [N]? Give me the topic, target slide count, and the save-worthy
takeaway."
```

### Step 2: Research Angle

**Skill:** `marketing-psychology` + `customer-research`

- [ ] Research the persuasion angle: what makes this topic shareable?
- [ ] Identify the knowledge gap: what does the audience think they know vs. what is true?
- [ ] Find 3-5 data points or facts to support each slide
- [ ] Determine the emotional arc: curiosity -> revelation -> value

```
Claude prompt:
"Research the persuasion angle for a carousel about [topic]. Target audience:
French women 18-35 interested in K-beauty. What knowledge gaps exist?
What surprising facts will drive saves? Use marketing-psychology principles
to structure the emotional arc."
```

### Step 3: Write Carousel Copy

**Skill:** `copywriting` + `copy-editing`

Carousel structure:

| Slide | Purpose | Copy Length |
|-------|---------|------------|
| 1 -- Cover | Hook + promise | 5-10 words, bold |
| 2-6 -- Content | One point per slide | 15-30 words each |
| 7 -- Cheat sheet | Saveable summary | Scannable list |
| 8 -- CTA | Save + follow + link | 10-15 words |

- [ ] Write cover slide hook (must work as a standalone image in the feed)
- [ ] Write one clear point per content slide
- [ ] Create a save-worthy cheat sheet slide
- [ ] Write the CTA slide
- [ ] Run through `copy-editing` for clarity and conciseness

```
Claude prompt:
"Write carousel copy for [topic]. 7-8 slides. Sonagi brand voice: intimate,
educating, provocative, honest. Slide 1 is a bold hook. Slides 2-6 are one
insight per slide (15-30 words). Slide 7 is a saveable cheat sheet.
Slide 8 is a CTA. French audience, mix French/English naturally."
```

### Step 4: Design in Canva

**Tool:** Canva (MCP tools available for automation)

**Design system:**
- Fonts: Cormorant Garamond (headings) + DM Sans (body)
- Colors: Cream background, Navy text (#1B2A4A), Peach accents (#FFCBA4)
- Style: Clean, minimal, editorial K-beauty aesthetic
- Format: 1080x1350 (4:5 portrait)

- [ ] Create or duplicate a Sonagi carousel template in Canva
- [ ] Apply the copy to each slide
- [ ] Add product images or ingredient visuals where relevant
- [ ] Ensure brand consistency: fonts, colors, spacing
- [ ] Export all slides as PNG

```
Claude prompt (if using Canva MCP):
"Create an Instagram carousel design in Canva for [topic]. Use the Sonagi
design system: Cormorant Garamond headings, DM Sans body, cream/navy/peach
palette. 1080x1350 format. [Paste slide copy here]."
```

### Step 5: Write Caption + Hashtags

**Skill:** `copywriting` + `social-content`

- [ ] Write caption following the same rules as Step 8 of the video workflow
- [ ] First line must hook (visible before "...more")
- [ ] Include a save CTA ("Sauvegarde pour ta prochaine routine")
- [ ] Select Educational hashtag set + Primary hashtags
- [ ] Total: 15-20 hashtags

### Step 6: Publish at Optimal Time

- [ ] Post on Monday or Wednesday at 12h00 France time
- [ ] Add to Stories with a swipe prompt ("Nouvelle publication -- swipe!")
- [ ] Engage in comments for first 30 minutes after posting

### Step 7: Track Saves and Completion Rate

| Metric | Target | Signal |
|--------|--------|--------|
| Saves | 50+ | High value content |
| Carousel completion rate | 60%+ | People swiping through all slides |
| Shares | 20+ | Shareable insight |
| Comments | 10+ | Engagement hook worked |

- [ ] Record at 24h and 7d
- [ ] Note which slide types drive highest completion

---

## 4. WORKFLOW: Weekly Content Batch

**Time estimate:** 4-6 hours (one focused session)
**Output:** 7 pieces of content scheduled for the week
**Best day:** Sunday evening or Monday morning

### Phase 1: Monday Planning (45 min)

**Skill:** `content-strategy`

- [ ] Open `content/full-campaign-plan.md`
- [ ] Identify the week number and theme
- [ ] List all 7 content pieces for the week:

| Day | Format | Topic | Product | Pillar | Status |
|-----|--------|-------|---------|--------|--------|
| Mon | Carousel | | | Eduquer | [ ] |
| Tue | Reel | | | Montrer | [ ] |
| Wed | Carousel | | | Eduquer | [ ] |
| Thu | Reel | | | Montrer | [ ] |
| Fri | Reel | | | Inspirer | [ ] |
| Sat | Stories | | | Engager | [ ] |
| Sun | Static | | | Inspirer | [ ] |

- [ ] Confirm no hook type is repeated from last week
- [ ] Gather all product images and references needed

```
Claude prompt:
"Plan this week's content from the campaign calendar (week [N]).
List all 7 pieces with format, topic, product, pillar, and hook type.
Make sure no hook type repeats from last week."
```

### Phase 2: Batch-Write All Copy (1.5 hours)

**Skill:** `copywriting` + `social-content` + `copy-editing`

Write all text content in one session:

- [ ] 2x carousel scripts (Monday + Wednesday)
- [ ] 3x Minjun video scripts (Tuesday + Thursday + Friday)
- [ ] 1x Stories plan (Saturday -- polls, quizzes, Q&A)
- [ ] 1x static post caption (Sunday)
- [ ] 7x social captions with hashtags
- [ ] Save all copy to a weekly content file

```
Claude prompt:
"Batch-write all copy for week [N]. I need: 2 carousel scripts (Mon/Wed),
3 Minjun video scripts (Tue/Thu/Fri), Saturday Stories plan, Sunday static
post caption, and all 7 social captions with hashtags. Follow Sonagi brand
voice and the SCRIPT-WRITING-TEMPLATE for videos."
```

### Phase 3: Batch-Design Carousels (1 hour)

**Tool:** Canva

- [ ] Design Monday's carousel (follow Step 4 from Carousel workflow)
- [ ] Design Wednesday's carousel
- [ ] Design Sunday's static post
- [ ] Design Saturday's Stories templates
- [ ] Export all assets

### Phase 4: Batch-Generate Videos (1-2 hours)

**Tool:** Creatify

- [ ] Generate Tuesday's Minjun Reel
- [ ] Generate Thursday's Minjun Reel
- [ ] Generate Friday's Minjun Reel
- [ ] Post-produce all 3 videos (captions, music, overlays)
- [ ] Save all final versions to `images/YYYY-MM-DD/`

### Phase 5: Schedule Everything (30 min)

- [ ] Schedule Monday carousel at 12h00
- [ ] Schedule Tuesday Reel at 18h00
- [ ] Schedule Wednesday carousel at 12h00
- [ ] Schedule Thursday Reel at 18h00
- [ ] Schedule Friday Reel at 19h00
- [ ] Prepare Saturday Stories (post manually at 10h00)
- [ ] Schedule Sunday static post at 11h00
- [ ] Cross-post Reels to TikTok and YouTube Shorts

### Phase 6: Daily Engagement (30 min/day)

**Skill:** `community-marketing`

- [ ] Reply to all comments within 1 hour of posting
- [ ] Engage with 10 accounts in the K-beauty niche
- [ ] Respond to all DMs
- [ ] Repost relevant UGC or tagged content to Stories
- [ ] Track daily metrics in a simple spreadsheet

```
Claude prompt:
"Give me today's community engagement checklist using the community-marketing
skill. What accounts should I engage with? What comment reply strategies
drive the most conversation?"
```

---

## 5. WORKFLOW: New Product Launch

**Time estimate:** 1 week of preparation + 1 week of launch content
**Output:** Full launch sequence across all channels

### Phase 1: Product Research (Day 1)

**Skill:** `customer-research` + `marketing-psychology` + `competitor-alternatives`

- [ ] Research the product: ingredients, claims, price, differentiators
- [ ] Analyze competitor products and their positioning
- [ ] Identify the target customer's pain point this product solves
- [ ] Map the emotional journey: problem awareness -> solution desire -> purchase intent
- [ ] Determine the unique angle for Sonagi (K-beauty expertise, Minjun's personal testing)

```
Claude prompt:
"Research [new product] for a Sonagi Beauty launch. Use customer-research to
identify the target pain point, marketing-psychology for the emotional angle,
and competitor-alternatives to find our unique positioning. Target: French
women 18-35 interested in K-beauty."
```

### Phase 2: Product Page Copy (Day 1-2)

**Skill:** `copywriting` + `page-cro`

- [ ] Write product page headline and subhead
- [ ] Write product description (benefits-first, ingredients-second)
- [ ] Write 3-5 bullet points for key claims
- [ ] Write usage instructions
- [ ] Optimize for conversions using `page-cro` skill
- [ ] Add to sonagibeauty.com product page

```
Claude prompt:
"Write product page copy for [product] on sonagibeauty.com. Use the Sonagi brand
voice: intimate, educating, sensory. Benefits first, ingredients second.
Then optimize the page layout for conversions using page-cro principles."
```

### Phase 3: Launch Carousel (Day 2-3)

Follow the full [Carousel Workflow](#3-workflow-instagram-carousel-end-to-end) with this specific angle:

- [ ] Slide 1: "On a trouve [product category] parfait"
- [ ] Slides 2-5: What it does, key ingredients, how to use, who it is for
- [ ] Slide 6: Before/after or texture close-up
- [ ] Slide 7: Price + "dispo maintenant sur sonagibeauty.com"

### Phase 4: Minjun Review Video (Day 3-4)

Follow the full [Minjun Video Workflow](#2-workflow-new-minjun-video-end-to-end) with this structure:

- [ ] Hook: "I've been testing [product] for 2 weeks. Here's the truth."
- [ ] Product: Show application, texture, feel
- [ ] Payoff: Honest review with genuine result
- [ ] Sign-off: "If [skin concern], this is the one."

### Phase 5: Email Announcement (Day 4-5)

**Skill:** `email-sequence`

- [ ] Write announcement email (subject line, preview text, body)
- [ ] Include: product hero image, 3 key benefits, CTA button
- [ ] Write follow-up email for 48h later (social proof angle)
- [ ] Write abandoned-cart reminder if applicable

```
Claude prompt:
"Write a 2-email launch sequence for [product] using the email-sequence skill.
Email 1: announcement (day of launch). Email 2: social proof follow-up (48h later).
Sonagi brand voice. Include subject lines, preview text, and full body copy."
```

### Phase 6: Social Launch Sequence (Day 5-7)

3 posts across 1 week:

| Post | Day | Format | Angle |
|------|-----|--------|-------|
| Teaser | Day -2 | Story + Static | "Something new is coming..." |
| Launch | Day 0 | Carousel + Reel | Full reveal + Minjun review |
| Social proof | Day +3 | Reel | Results, reactions, testimonials |

### Phase 7: Paid Promotion (Day 7+)

**Skill:** `paid-ads` + `ad-creative`

- [ ] Create 3 ad variations (different hooks, same product)
- [ ] Set up targeting: French women 18-35, K-beauty interests, skincare interests
- [ ] Budget: start with EUR 10/day per variation for testing
- [ ] Platform: Instagram Reels ads + TikTok In-Feed
- [ ] Run for 7 days, then analyze and scale winners

```
Claude prompt:
"Create 3 ad variations for [product] using paid-ads and ad-creative skills.
Target: French women 18-35 interested in K-beauty/skincare. Each variation
should use a different hook. Include copy, targeting, and budget recommendations."
```

---

## 6. WORKFLOW: Monthly Strategy Review

**Time estimate:** 2-3 hours
**Schedule:** Last Sunday of each month
**Output:** Updated content calendar + performance insights

### Step 1: Analyze Last Month's Metrics

**Skill:** `analytics-tracking`

- [ ] Pull all post metrics from Instagram and TikTok analytics
- [ ] Fill in the performance table:

| Week | Best Post | Saves | Shares | Watch Time | Why It Worked |
|------|-----------|-------|--------|------------|---------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |

```
Claude prompt:
"Help me analyze this month's content performance. Here are the metrics:
[paste metrics]. Identify the top 3 performers, the bottom 3, and patterns
in what drove saves, shares, and watch time."
```

### Step 2: Review What Content Performed

- [ ] Identify top 3 posts by saves (signal: lasting value)
- [ ] Identify top 3 posts by shares (signal: word-of-mouth)
- [ ] Identify top 3 Reels by watch time (signal: hook strength)
- [ ] Identify which hook types performed best
- [ ] Identify which products generated most interest
- [ ] Note any viral or breakout content and what made it work

### Step 3: Adjust Next Month's Calendar

**Skill:** `content-strategy` + `marketing-ideas`

- [ ] Double down on formats/topics that performed well
- [ ] Cut or modify formats/topics that underperformed
- [ ] Introduce 1-2 new content experiments
- [ ] Update `content/full-campaign-plan.md` for next month
- [ ] Ensure content pillar balance is maintained

```
Claude prompt:
"Based on this month's performance analysis, update the content strategy for
next month. Use content-strategy and marketing-ideas skills. Keep what works,
cut what doesn't, and suggest 2 new experiments. Update the campaign plan."
```

### Step 4: Refresh Ad Creatives (If Running Paid)

**Skill:** `ad-creative` + `ab-test-setup`

- [ ] Review ad performance: CTR, CPC, ROAS
- [ ] Pause underperforming ads (CTR < 1%)
- [ ] Create new variations based on top organic content
- [ ] Set up A/B tests for new creatives

### Step 5: Community Health Check

**Skill:** `community-marketing`

- [ ] Review follower growth rate
- [ ] Check DM volume and response time
- [ ] Review comment sentiment
- [ ] Identify top community members / potential ambassadors
- [ ] Check hashtag #MonRituelSonagi usage
- [ ] Plan community engagement initiatives for next month

```
Claude prompt:
"Run a community health check for Sonagi Beauty using the community-marketing
skill. Assess: follower growth, engagement quality, DM patterns, comment
sentiment, and ambassador potential. Recommend actions for next month."
```

---

## 7. SKILL REFERENCE MAP

### Brand and Strategy

| Skill | When to Use | Workflows |
|-------|-------------|-----------|
| `content-strategy` | Planning content calendars, choosing topics, content pillar balance | Weekly Batch (Phase 1), Monthly Review (Step 3) |
| `marketing-ideas` | Brainstorming new content angles, experiments | Monthly Review (Step 3) |
| `marketing-psychology` | Persuasion hooks, emotional triggers, carousel angles | Video (Step 2), Carousel (Step 2), Product Launch (Phase 1) |
| `customer-research` | Understanding audience pain points, product research | Video (Step 2), Product Launch (Phase 1) |
| `pricing-strategy` | Setting product prices, bundle offers, promotions | Product Launch (Phase 2) |
| `launch-strategy` | Planning product or campaign launches | Product Launch (all phases) |
| `product-marketing-context` | Foundation context read by all other skills | Always (auto-referenced) |
| `competitor-alternatives` | Analyzing competitor content and positioning | Product Launch (Phase 1) |

### Content and Copy

| Skill | When to Use | Workflows |
|-------|-------------|-----------|
| `copywriting` | Writing all marketing copy (captions, scripts, product pages) | Video (Steps 4, 8), Carousel (Step 3), Product Launch (Phase 2) |
| `copy-editing` | Proofreading and tightening copy | Video (Step 8), Carousel (Step 3), Weekly Batch (Phase 2) |
| `social-content` | Social media posts, platform-specific optimization | Video (Steps 3, 8), Carousel (Step 5), Weekly Batch (Phase 2) |
| `email-sequence` | Welcome emails, launch announcements, nurture sequences | Product Launch (Phase 5) |
| `cold-email` | Outreach to influencers, press, potential partners | Product Launch (outreach) |

### Video Production

| Template/Tool | When to Use | Workflows |
|---------------|-------------|-----------|
| `SCRIPT-WRITING-TEMPLATE.md` | Writing 3x15s video scripts | Video (Steps 3, 4) |
| `UGC-CHARACTER-BIBLE-TEMPLATE.md` | Character behaviour, camera angles, caption system | Video (Step 5, 7) |
| `SEEDANCE-PROMPT-GUIDE.md` | Structuring video generation prompts | Video (Step 5) |
| `SESSION-HANDOFF-MINJUN.md` | Full context on Minjun project, files, decisions | Start of any Minjun session |
| Creatify (browser) | Generating avatar videos | Video (Step 6) |
| CapCut (editor) | Post-production: captions, music, overlays | Video (Step 7) |

### Seedance Video Skills (15 styles in `higgsfield-seedance2-skills/skills/`)

| Skill | When to Use |
|-------|-------------|
| `01-cinematic` | Aspirational brand content, high-production feel |
| `07-ecommerce-ad` | Product-focused paid ad creatives |
| `09-product-360` | 360-degree product showcase |
| `11-social-hook` | Short-form social hooks (TikTok/Reels openers) |
| `12-brand-story` | About-us or brand narrative videos |
| `13-fashion-lookbook` | Aesthetic product styling sequences |
| `14-food-beverage` | Texture/sensory content (adapt for skincare textures) |

(Other styles -- 02-3d-cgi, 03-cartoon, 04-comic-to-video, 05-fight-scenes, 06-motion-design-ad, 08-anime-action, 10-music-video, 15-real-estate -- are available but less relevant to skincare content.)

### Growth and Conversion

| Skill | When to Use | Workflows |
|-------|-------------|-----------|
| `paid-ads` | Setting up and managing paid campaigns | Product Launch (Phase 7) |
| `ad-creative` | Creating ad copy and visuals | Product Launch (Phase 7), Monthly Review (Step 4) |
| `ab-test-setup` | Testing ad variations, landing pages, email subjects | Monthly Review (Step 4) |
| `referral-program` | Building word-of-mouth referral mechanics | Growth initiatives |
| `community-marketing` | Community engagement, ambassador programs | Weekly Batch (Phase 6), Monthly Review (Step 5) |
| `lead-magnets` | Creating free resources to capture emails | List building |
| `popup-cro` | Optimizing website popups for email capture | Conversion optimization |
| `page-cro` | Optimizing product pages for purchases | Product Launch (Phase 2) |

### SEO and Technical

| Skill | When to Use | Workflows |
|-------|-------------|-----------|
| `seo-audit` | Auditing sonagibeauty.com for search visibility | Quarterly |
| `ai-seo` | Optimizing for AI-powered search (Google SGE, Perplexity) | Quarterly |
| `schema-markup` | Adding structured data to product pages | Site updates |
| `site-architecture` | Optimizing site navigation and URL structure | Site redesigns |
| `programmatic-seo` | Creating ingredient/product template pages at scale | Growth initiative |
| `analytics-tracking` | Setting up GA4, events, conversion tracking | Monthly Review (Step 1), Video (Step 10) |

### Less Frequently Used (Available When Needed)

| Skill | Purpose |
|-------|---------|
| `signup-flow-cro` | Optimizing account creation flow |
| `onboarding-cro` | Optimizing first-purchase experience |
| `form-cro` | Optimizing checkout and contact forms |
| `paywall-upgrade-cro` | Subscription/membership upsells |
| `churn-prevention` | Reducing customer churn |
| `free-tool-strategy` | Creating free skincare tools (quiz, routine builder) |
| `revops` | Revenue operations and sales process |
| `sales-enablement` | Sales collateral and training |
| `aso-audit` | App store optimization (if Sonagi launches an app) |

---

## 8. QUICK-START COMMANDS

Copy-paste these prompts to kick off any workflow instantly.

### Minjun Video Commands

```
Write a Minjun script for [product] using the [hook type] hook.
Follow SCRIPT-WRITING-TEMPLATE: 3x15s clips, 30-40 words each.
Edward Zo energy. End with warm sign-off, not sales CTA.
```

```
Convert this Minjun script into Creatify-ready prompts.
Follow SEEDANCE-PROMPT-GUIDE: time-segmented, 60-100 words each,
one camera instruction per clip, different angle per clip.
Character: hero-v4.jpg. Setting: warm beige-grey tile bathroom.
```

```
Write a Minjun video script about barrier repair using the
before/after tease hook. Product: Anua Heartleaf 77% Toner.
```

```
Write a Minjun video script about SPF using the curiosity gap
hook. Product: Beauty of Joseon Relief Sun SPF50+.
```

```
Write a Minjun video script about snail mucin using the
celebrity reaction hook. Product: COSRX Advanced Snail 96 Mucin.
```

### Carousel Commands

```
Create an Instagram carousel about [ingredient/topic] following
the Sonagi voice. 7-8 slides, educational pillar. Cormorant
Garamond + DM Sans, cream/navy/peach. Include a save-worthy
cheat sheet on the second-to-last slide.
```

```
Write a "sur peau mouillee ou seche" style educational carousel
about [skincare technique]. Make it save-worthy.
```

```
Create a product comparison carousel: [Product A] vs [Product B].
Target: French women deciding between French pharmacy and K-beauty.
```

### Weekly Planning Commands

```
Plan next week's content from the campaign calendar (week [N]
of full-campaign-plan.md). List all 7 pieces with format, topic,
product, pillar, and hook type.
```

```
Batch-write all captions for this week's 7 posts. Use Sonagi
brand voice, mix French and English. Include hashtags for each.
```

```
Write 3 Minjun video scripts for this week (Tue/Thu/Fri).
Different products, different hook types. Follow the campaign
calendar.
```

### Product Launch Commands

```
Plan a full product launch for [product name]. Include: product
page copy, launch carousel, Minjun review video script, 2-email
sequence, and 3-post social launch sequence. Use customer-research
for the pain point and marketing-psychology for the emotional angle.
```

```
Write product page copy for [product] on sonagibeauty.com.
Benefits-first, ingredients-second. Sonagi brand voice. Then
optimize for conversions using page-cro.
```

```
Create 3 ad variations for [product]. Target: French women 18-35,
K-beauty interests. Different hooks per variation. Include copy,
targeting, and budget.
```

### Monthly Review Commands

```
Help me analyze this month's content performance.
[Paste metrics here.]
Identify top 3 and bottom 3 performers. Find patterns in saves,
shares, and watch time. Recommend what to keep, cut, and test.
```

```
Run a community health check for Sonagi Beauty. Assess follower
growth, engagement quality, comment sentiment, and ambassador
potential. Recommend actions for next month.
```

```
Update the content strategy for next month based on this performance
data. Keep what works, cut what doesn't, suggest 2 experiments.
Update content/full-campaign-plan.md.
```

### Brand Voice Quick Reference

```
Rewrite this copy in the Sonagi brand voice: intimate, educating,
provocative, honest, sensory, warm. Target: French women 18-35.
Mix French and English naturally. "[paste copy here]"
```

### Utility Commands

```
Read SESSION-HANDOFF-MINJUN.md and bring yourself up to speed
on the Minjun project. Then tell me what the next priority is.
```

```
Check all files in images/YYYY-MM-DD/ and tell me what assets
we have for today's production session.
```

```
Search the campaign calendar for all posts featuring [product name]
and list them with dates, formats, and hooks.
```

---

## KEY FILES REFERENCE

| File | Location | Purpose |
|------|----------|---------|
| Campaign plan | `content/full-campaign-plan.md` | 4-week content calendar |
| Script template | `SCRIPT-WRITING-TEMPLATE.md` | 3x15s video script formula |
| Prompt guide | `SEEDANCE-PROMPT-GUIDE.md` | Video generation prompt rules |
| Character bible | `UGC-CHARACTER-BIBLE-TEMPLATE.md` | Minjun behaviour, angles, captions |
| Session handoff | `SESSION-HANDOFF-MINJUN.md` | Full project context and file locations |
| Character sheet | `higgsfield-seedance2-skills/MINJUN-CHARACTER-SHEET.md` | Minjun's identity and look |
| Production bible | `higgsfield-seedance2-skills/MINJUN-PRODUCTION-BIBLE.md` | Universal production rules |
| Hero image | `images/2026-04-15/minjun-reference/hero-v4.jpg` | Minjun anchor face |
| Voice clip | `images/2026-04-16/Minjun_script5/minjun-voice-clip.mp3` | Voice clone source |
| Best video | `images/2026-04-16/Minjun_script5/Minjun best.mp4` | Gold standard reference |
| Marketing skills | `.agents/skills/` | 36 marketing skills |
| Seedance skills | `higgsfield-seedance2-skills/skills/` | 15 video style skills |

---

## RULES (never break these)

1. **Minjun speaks ENGLISH**, not French. French voice was tested and dropped.
2. **Save all outputs** to `images/YYYY-MM-DD/` folders. Never lose an asset. Append version numbers if regenerating.
3. **Edward Zo is the #1 energy reference** for Minjun. Playful, witty, FaceTime energy.
4. **30-40 words per 15-second clip**. No more.
5. **One camera instruction per clip**. Multiple instructions cause jitter.
6. **Different camera angle per clip**. Creates visual dynamism.
7. **60-100 words max per video generation prompt**. Flowing paragraphs, not labeled blocks.
8. **Text overlays, captions, and music are post-production**. Never ask the AI video generator to create them.
9. **Before/after photos** are overlaid in the editor at top of frame, not generated by AI.
10. **Brand voice**: intimate, educating, provocative, honest, sensory, warm. Never salesy or corporate.
11. **Use Playwright with Edge browser**, not Chrome. Chrome locks between sessions.
12. **Search for existing work before creating new**. The user loses trust when assets are recreated unnecessarily.
