# Sonagi Beauty — Influencer & Press CRM (Notion-style template)

**How to use:** Copy this file into Notion as a database (or keep as markdown if Notion isn't set up yet). Each row = one creator or one journalist. Update the `Status` column every time you act.

---

## Database 1 — Influencer Outreach CRM

### Properties (columns)

| Property | Type | Options / Notes |
|---|---|---|
| Handle | Title | @username |
| Platform | Select | Instagram, TikTok, YouTube, Pinterest |
| Real name | Text | If known |
| Followers | Number | Approx, update quarterly |
| Engagement rate (%) | Number | (likes + comments) ÷ followers × 100, average of last 6 posts |
| Tier | Select | Nano (1-10k), Micro (10-50k), Mid (50-200k), Retailer, Press |
| Niche | Multi-select | K-beauty, Skincare, Makeup, Lifestyle, Wellness, Mom, Curly hair, Sensitive skin, Acne, Anti-aging, Vegan |
| Location | Text | City + country (Paris, France) |
| Language | Select | French, English, Bilingual |
| K-beauty verified | Checkbox | TRUE only if last 10 posts include K-beauty content |
| Email | Email | If publicly available |
| DM URL | URL | direct link to their IG/TikTok DM |
| Status | Select | (see status list below) |
| Date 1st contact | Date | |
| Date last follow-up | Date | |
| Reply received | Checkbox | |
| PR shipped date | Date | |
| Tracking number | Text | |
| PR received confirmed | Checkbox | |
| Posted date | Date | |
| Post URL | URL | |
| Code shared (Y/N) | Checkbox | |
| Code | Text | e.g., ARALE15 |
| Sales generated (€) | Number | track post-launch via affiliate |
| Quality rating (1-5) | Select | 1=fake/low-quality, 5=dream creator |
| Recurring? | Checkbox | TRUE if posted 2+ times |
| Notes | Text | Long-form |

### Status options (Select)

- 🔍 `prospect` — In research, not contacted
- 👀 `engaging` — Commenting on their content, no DM yet
- 📨 `cold-sent` — DM sent, awaiting reply
- ↗️ `follow-up-1` — D+7 follow-up sent
- ↗️ `follow-up-2` — D+14 follow-up sent
- 💬 `warm-replied` — They replied positively, awaiting address
- 📦 `pr-shipped` — Kit en route
- ✅ `pr-received` — Confirmed received
- 🌟 `posted-organic` — Posted without prompting
- 📣 `posted-prompted` — We asked, they posted
- 💛 `recurring` — Posted 2+ times — VIP
- ❌ `declined` — Politely said no
- 🪦 `silent` — No reply after 2 follow-ups, archive
- 🚫 `do-not-contact` — Bad fit, off-brand, or burned bridge

### Views to create in Notion

1. **All Active** — filter `Status` ≠ silent / declined / do-not-contact
2. **Pipeline by Status** — Board view, grouped by Status
3. **This Week's Outreach** — filter `Date 1st contact` is empty AND `Status` = prospect, sorted by `Engagement rate` descending
4. **Awaiting Reply** — `Status` = cold-sent OR follow-up-1 OR follow-up-2
5. **PR Tracker** — `Status` = pr-shipped OR pr-received, sorted by `PR shipped date`
6. **VIP Recurring** — `Recurring` = TRUE
7. **K-beauty verified only** — filter `K-beauty verified` = TRUE

---

## Database 2 — Press / Journalist CRM

### Properties

| Property | Type | Notes |
|---|---|---|
| Outlet | Title | e.g., Vogue.fr, Jung Magazine |
| Journalist name | Text | |
| Beat | Select | Beauty editor, Beauty director, Trade, Lifestyle, Health, Freelance |
| Email | Email | |
| Twitter/X | URL | |
| LinkedIn | URL | |
| Tier | Select | Tier 1 (Jung, Premium Beauty News, Doctissimo), Tier 2 (Vogue Glamour Elle Marie Claire Cosmo), Tier 3 (regional / niche) |
| Pitch sent date | Date | |
| Angle pitched | Text | |
| Reply | Select | No reply, Replied positive, Replied no, Published |
| Article URL | URL | If they published |
| Coverage rating | Select | 1-5 stars based on coverage quality |
| Notes | Text | Personal interests, prior coverage style, dietary restrictions if meeting in person |

### Initial seed data (Tier 1 priority for Sonagi launch)

| Outlet | Tier | Status |
|---|---|---|
| Jung Magazine | 1 | To pitch week 1 |
| Premium Beauty News | 1 | To pitch week 1 |
| Doctissimo Beauté | 1 | To pitch week 2 |
| Beauty Decoded | 1 | To pitch week 2 |
| Holizy Magazine | 2 | To pitch week 3 |
| Vogue.fr Beauté | 2 | To pitch week 4 |
| Glamour.fr | 2 | To pitch week 4 |
| Marie Claire France | 2 | To pitch week 5 |
| Elle.fr Beauté | 2 | To pitch week 5 |
| Cosmopolitan FR | 2 | To pitch week 6 |

---

## Database 3 — UGC log

### Properties

| Property | Type | Notes |
|---|---|---|
| Customer handle | Title | |
| Platform | Select | Instagram, TikTok, Story, Reel, Post |
| Original post URL | URL | |
| Date tagged | Date | |
| Permission requested? | Checkbox | |
| Permission granted? | Checkbox | |
| Permission DM screenshot path | Text | local file path |
| Reposted to | Multi-select | Feed, Story, Highlight, Reel compilation |
| Repost URL | URL | |
| Sent thank-you gift? | Checkbox | |
| Notes | Text | |

---

## Database 4 — Comment templates library

Store the 22 comment templates from Section 2 of the playbook here, tagged by intent (educational, affirmation, intimate, expert, provocative). Add new ones as you discover what works. Track which templates have the highest reply-back rate from creators.

| Template ID | Intent | French text | Times used | Times replied to | Reply rate (%) |
|---|---|---|---|---|---|
| E-01 | Educational | Petit ajout : la mucine d'escargot fonctionne mieux... | | | |
| E-02 | Educational | Le centella asiatica calme l'inflammation, mais... | | | |
| ... | ... | ... | | | |

---

## Setup time

- Build all 4 databases in Notion: ~45 min one-time
- Import the 14 seed handles from `influencer-hit-list.csv`: ~15 min
- Initial weekly maintenance: ~30 min

## Free Notion templates worth importing as starting points

- "Influencer Outreach Tracker" (Notion Marketplace, free)
- "Outreach Tracker" (Notion Marketplace, free)
- "Talent Manager CRM" (Notion Marketplace, free) — overkill but useful for the field structure

---

**END OF CRM TEMPLATE**
