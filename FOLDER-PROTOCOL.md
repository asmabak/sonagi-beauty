# Sonagi Beauty — Folder Organization Protocol
## READ THIS when creating, moving, or finding any content
## Last Updated: 2026-04-16

---

## MASTER STRUCTURE

```
sonagi-beauty/
├── website/
│   ├── html-css-js/              # Website source code
│   ├── product-images/           # Product photos for site
│   ├── blog/                     # Blog articles
│   └── seo/                      # SEO assets, schema, sitemap
│
├── brand-strategy/
│   ├── brand-identity/           # Logo, profile photo, color palette, fonts
│   ├── voice-guide/              # Brand Voice Guide (PPTX), tone rules
│   ├── campaign-plans/           # Monthly plans, orchestration workflow
│   ├── competitor-research/      # Soko Glam, Glow Recipe, Seoul Beauty Club analysis
│   └── production-bible/         # Minjun character sheet, Seedance guide, templates
│
├── social-media/
│   ├── instagram/
│   │   ├── french/               # @sonagi.beauty
│   │   │   ├── to-be-approved/   # Claude generates → user reviews
│   │   │   │   └── 2026/may/week1/  # Organized by year/month/week
│   │   │   ├── approved/         # User approved → ready to post
│   │   │   ├── published/        # Posted → with date records
│   │   │   └── rejected/         # User rejected → needs revision
│   │   ├── english/              # @sonagi.beauty.int
│   │   │   └── (same structure)
│   │   ├── italian/              # Future
│   │   ├── spanish/              # Future
│   │   └── (same for each language)
│   │
│   ├── tiktok/
│   │   └── (same structure: french/english/italian/spanish)
│   │
│   ├── youtube/
│   │   └── (same structure)
│   │
│   ├── linkedin/
│   │   └── (same structure)
│   │
│   ├── pinterest/
│   │   └── (same structure)
│   │
│   ├── facebook/
│   │   └── (same structure)
│   │
│   ├── twitter-x/
│   │   └── (same structure)
│   │
│   └── minjun/                   # Minjun's own section (independent creator)
│       ├── assets/               # hero-v4.jpg, voice clip, reference images
│       ├── scripts/              # Video scripts and prompts
│       └── videos/
│           ├── to-be-approved/
│           ├── approved/
│           └── published/
│
├── scheduler/                    # Automated posting system
│   ├── schedule.json             # What to post and when
│   ├── post.js                   # Posting script
│   ├── review.js                 # Preview upcoming posts
│   └── README.md                 # Documentation
│
├── SESSION-STATE.md              # Full project state for session continuity
├── ORCHESTRATION-WORKFLOW.md     # Production pipelines
├── FOLDER-PROTOCOL.md            # THIS FILE — folder rules
└── CLAUDE.md                     # Claude Code instructions
```

---

## CONTENT LIFECYCLE

### Stage 1: TO-BE-APPROVED
Claude generates content → saves here.
```
social-media/{platform}/{language}/to-be-approved/{year}/{month}/{week}/
```
Example: `social-media/instagram/french/to-be-approved/2026/may/week1/may01-7secondes/`

### Stage 2: APPROVED
User reviews and approves → Claude moves here.
```
social-media/{platform}/{language}/approved/{year}/{month}/
```

### Stage 3: PUBLISHED
Claude posts it → moves here with timestamp.
```
social-media/{platform}/{language}/published/{year}/{month}/
```

### Stage 4: REJECTED
User rejects → moves here with reason.
```
social-media/{platform}/{language}/rejected/{year}/{month}/
```

---

## RULES FOR FUTURE SESSIONS

1. **NEVER delete files** — always copy first, then move. Keep originals until user confirms.
2. **New content goes to to-be-approved/** — always. Never straight to published.
3. **Organize by year/month/week** — `2026/may/week1/`
4. **Each carousel gets its own subfolder** — `may01-7secondes/slide-1.png` through `slide-7.png`
5. **Captions go in a captions/ subfolder** — one .md file per week
6. **Stories go in a stories/ subfolder** — one .md file per month
7. **Reels go in a reels/ subfolder** — one folder per reel with video + caption
8. **English translations mirror French structure** — same filenames, same organization
9. **When user approves**, move from to-be-approved → approved
10. **When posted**, move from approved → published, add date to filename or log
11. **Minjun content stays in social-media/minjun/** — never mix with Sonagi brand content
12. **Brand strategy files are reference docs** — don't move them, link to them
13. **Scheduler reads from approved/** — only posts content that's been approved
14. **Archive old versions** in images/YYYY-MM-DD/archive/ — never in the main structure

---

## LANGUAGE EXPANSION WORKFLOW

When creating content for a new language:
1. Copy the French carousel slides folder → to the target language's to-be-approved/
2. Regenerate slides with translated text (same design system, same images)
3. Write translated captions
4. User approves
5. Post to the language-specific account

Language accounts:
- French: @sonagi.beauty
- English: @sonagi.beauty.int
- Italian: TBD
- Spanish: TBD

---

## FINDING THINGS QUICKLY

| What you need | Where to look |
|---|---|
| Latest carousel slides | social-media/instagram/french/to-be-approved/2026/may/ |
| Published posts | social-media/instagram/french/published/ |
| Captions | social-media/instagram/french/to-be-approved/2026/may/captions/ |
| Stories | social-media/instagram/french/to-be-approved/2026/may/stories/ |
| Minjun videos | social-media/minjun/videos/ |
| Minjun face reference | social-media/minjun/assets/hero-v4.jpg |
| Brand voice guide | brand-strategy/voice-guide/ |
| Posting schedule | scheduler/schedule.json |
| Website code | website/html-css-js/ |
| Product images | website/product-images/ |
| Campaign plan | brand-strategy/campaign-plans/ |
| Session state | SESSION-STATE.md |
| This protocol | FOLDER-PROTOCOL.md |
