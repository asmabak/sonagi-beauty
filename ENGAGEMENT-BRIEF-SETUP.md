# Daily Engagement Briefing — Setup

A daily email landing in your inbox at **07:30 Paris** with 25-50 social posts to comment on. Each post comes with **4 ready-to-paste comment options** in Sonagi voice. You comment manually (no automation = no ban risk). Goal: 25 comments in 15 minutes.

## Cost: €0/month

| Layer | Tool | Free? |
|---|---|---|
| Discovery (Reddit) | Reddit JSON API | ✅ Yes — public, no auth |
| Discovery (IG/TikTok URLs you queue) | TikTok oEmbed + IG meta scrape | ✅ Yes — official, no auth |
| Comment generation | **Google Gemini 2.5 Flash** — free tier 1M tokens/day | ✅ Yes — no credit card |
| Cron + compute | GitHub Actions | ✅ Yes — 2,000 free min/mo, this uses ~3 min/day |
| Email delivery | Gmail SMTP | ✅ Yes — your own Gmail account |

## One-time setup (~10 minutes total)

### Step 1 — Get your free Gemini API key (~2 min)
1. https://aistudio.google.com/app/apikey
2. Sign in with your Gmail
3. **Create API key** → copy it (starts with `AIza...`)
4. **No credit card required**, 1M tokens/day free (we use ~13k/day)

### Step 2 — Generate a Gmail app password (~3 min)
1. Make sure 2FA is on: https://myaccount.google.com/security → "2-Step Verification"
2. Go to https://myaccount.google.com/apppasswords
3. App name: `Sonagi Briefing` → **Create**
4. Copy the **16-character password** that pops up (looks like `abcd efgh ijkl mnop`) — Google shows it once

### Step 3 — Add 4 GitHub Secrets (~3 min)
https://github.com/asmabak/sonagi-beauty/settings/secrets/actions → **New repository secret** for each:

| Name | Value |
|---|---|
| `GEMINI_API_KEY` | the `AIza...` key from Step 1 |
| `SMTP_USER` | `asma.bakhtar@gmail.com` (your Gmail) |
| `SMTP_PASS` | the 16-char app password from Step 2 (no spaces) |
| `EMAIL_TO` | where the briefing lands — recommend `asma.bakhtar@gmail.com` (or `contact@sonagibeauty.com` if you want it forwarded there) |

### Step 4 — Run it once to test (~30 sec)
1. https://github.com/asmabak/sonagi-beauty/actions/workflows/daily-engagement-brief.yml
2. **Run workflow** → **Run workflow** (uses `main` branch)
3. Wait ~3 minutes → check your inbox

That's it. From then on the briefing arrives every morning at 07:30 Paris.

---

## Your daily ritual (~15 min)

Each morning at coffee:
1. Open the **Sonagi Briefing** email (Gmail → search `from:Sonagi Briefing`)
2. Scroll through the posts (manual queue at top, then Reddit by priority)
3. For each post you want to comment on:
   - Read the caption
   - Pick the comment option that fits (A/B/C/D)
   - **Tap "copy"** → comment is on your clipboard
   - **Tap "Ouvrir →"** → opens the Reddit/IG/TikTok post in a new tab
   - Paste, post, done
4. Tap **"✓ Commenté"** on each one as you go (just a UI toggle, helps you track)

Target: **25 comments/day** in **15 minutes**.

---

## Adding posts manually (the "I saw this on IG" queue)

When you scroll IG/TikTok and see a post you want to comment on later with a Sonagi-voice draft, paste the URL into:

📁 `scripts/engagement-brief/engagement-urls.txt`

One URL per line. Lines starting with `#` are comments. Save, commit, push. Next morning's briefing has 4 comment options for each URL at the top.

**Pro tip:** keep that file open in a tab on your phone (GitHub mobile lets you edit). Anytime you see a creator post, paste the URL. By 07:30 the briefing has comments ready.

---

## How to change the voice / cadence / sources

Edit `scripts/engagement-brief/config.js`:

- **Add subreddits** in `reddit.subreddits` array
- **Tweak voice rules** in `voice.rules` (sent to Gemini verbatim)
- **Change cadence target** in `briefing.target_actions` (default: 25 comments/day)

To change the cron time → edit `.github/workflows/daily-engagement-brief.yml` (default: `30 6 * * *` = 06:30 UTC = 07:30 Paris CET / 08:30 CEST).

Commit + push → next morning's briefing reflects the changes.

---

## Why no Instagram/TikTok hashtag scraping?

**Meta and ByteDance kill scrapers in 2026.** I tested public RSSHub instances during build — `rsshub.app` returns HTTP 403 on every Instagram route. Other public instances either don't exist or return zero results. The only honest paths are:

1. **What we use today** — Reddit (free, stable) + your manual URL queue (free, official APIs)
2. **Self-host RSSHub** on Vercel free tier — ~1 hour setup, gives you IG/TikTok hashtag feeds (until Meta blocks the IP, then it stops working)
3. **Pay for Apify/ScrapingBee** (€30-100/mo) — works reliably, but you said no paid tools

For the volume you need (25 comments/day), Reddit + manual queue is plenty. K-beauty Reddit is a goldmine — r/AsianBeauty alone has 2.2M subscribers and 30+ daily posts.

---

## Privacy + ban safety

- **Zero automation touches IG/TikTok APIs** — comments are posted manually by you. No ban risk.
- **GitHub Secrets are encrypted** — your Gemini key + Gmail password never appear in logs
- **The briefing is in your inbox only** — not on the public website
- All Reddit content is public; using TikTok oEmbed + IG public meta is officially allowed

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| No email at 07:30 | GitHub Actions failed | https://github.com/asmabak/sonagi-beauty/actions — click latest run, read the red step |
| Email empty (no posts) | Reddit hit a temporary 429 rate limit | Re-run manually in 1 hour |
| Posts have no comments | `GEMINI_API_KEY` missing or wrong | Step 1 + Step 3 above |
| Email doesn't arrive | `SMTP_PASS` wrong (most common) | Re-generate app password (Step 2), update secret |
| Briefing in spam folder | First send from new domain | Move once to inbox + mark "Not spam" — Gmail learns |

## When to upgrade

After ~1 month of running, evaluate:
- Comments quality good? → keep Gemini Flash, stays free
- Want sharper / more nuanced comments? → switch to `gemini-2.5-pro` in config (still free tier, slower but better)
- Outgrown Reddit + manual? → self-host RSSHub for IG/TikTok hashtag feeds (Vercel free tier, 1 hr setup)
- Outgrown free Gemini limits? → never going to happen at this volume (we use ~1.3% of daily quota)
