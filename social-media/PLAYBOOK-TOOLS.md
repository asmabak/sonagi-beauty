# PLAYBOOK — Tool Stack
**Sonagi Beauty | Pre-launch tooling**
**Principle:** free tier first. Paid only when free is the bottleneck.
**Total recommended monthly spend pre-launch:** **0€** for 60 days, then **~12–25€** if you upgrade Brevo.
**Last updated:** 2026-04-17

---

## How to read this doc

Every tool below is rated:
- **USE NOW** — set up this week
- **USE LATER** — set up at launch (T-30 days), not before
- **SKIP** — don't bother for Sonagi's stage / market

Every paid tier carries a **"skip until X"** flag — i.e., the milestone that justifies the upgrade.

---

## 1. Scheduling

### Recommendation: **Metricool free** as primary, **Buffer free** as backup

#### Metricool — **USE NOW**
- **Purpose:** schedule + analytics in one tool, multi-platform
- **Free tier:** 1 brand, 50 scheduled posts/month, basic analytics, competitor tracking included (rare on free)
- **Paid:** Starter 18€/mo (unlimited posts, 5 competitors, 1 user), Advanced 29€/mo
- **Why this for Sonagi:** the free analytics + competitor tracking is more generous than Buffer's; Pinterest scheduling is native; supports French interface.
- **Skip the upgrade until:** you exceed 50 posts/month (likely Month 2 of 90-day plan).

#### Buffer free — **USE NOW (backup / second account)**
- **Purpose:** simplest cross-platform scheduler
- **Free tier:** 3 channels, 10 scheduled posts per channel at any time
- **Paid:** Essentials 6$/mo per channel (≈ 18$/mo for 3)
- **Use case:** if Metricool's queue jams or you want a second-opinion best-time-to-post.
- **Skip the upgrade until:** never; if you outgrow Buffer free, jump straight to Metricool paid.

#### Later — **SKIP for now**
- Best-in-class IG visual planner, but the free tier was discontinued (only 14-day trial). Not worth the 25$/mo until launch.
- **Revisit at launch** if you want a true visual grid planner for IG.

#### Hootsuite, Sprout Social — **SKIP**
- Hootsuite ~99$/mo entry, Sprout 199$/mo+. Built for agencies and enterprise. Massive overkill for a solo pre-launch brand.

---

## 2. Link-in-bio

### Recommendation: **Custom subdomain `links.sonagibeauty.com`** (build this)

The brand positioning is "premium curator." A Linktree page with their branding under the URL `linktr.ee/sonagibeauty` is the equivalent of putting a generic price-gun sticker on a Hermès box. It works but it cheapens the perception. You already own the domain. Build a one-page React/HTML link page on Netlify, point a CNAME at it, and you have `links.sonagibeauty.com` for **0€**.

**What it should contain (5 links max):**
1. Rejoindre la liste d'attente (primary CTA, big)
2. Quiz : Quelle routine K-beauty pour toi ?
3. Marques curées (À venir)
4. Le Magazine (blog)
5. Contact / DM

**Build time:** 2–3 hours. Asset goes in `/netlify/links/` on the existing site repo.

#### Linktree — **SKIP** (free tier is fine but the branding is wrong for Sonagi)
- Free: unlimited links, basic themes. Paid Pro 5$/mo, Premium 24$/mo.
- Use only as a 48h fallback if the custom subdomain breaks.

#### Beacons — **SKIP**
- Better-looking than Linktree, monetization features for creators. But still has Beacons branding on free, custom domain only on Creator Pro 10$/mo.
- Designed for creators monetizing direct, not for curator-brands building a waitlist.

#### Later Linkin.bio — **SKIP**
- Bundled with Later paid plans. Mirrors IG feed shoppably. Useful post-launch with a catalog. **Skip until:** you have ≥ 30 SKUs and a live shop.

---

## 3. Analytics

### Recommendation: native dashboards + GA4 + Looker Studio (all free)

#### Native dashboards — **USE NOW**
- Instagram Insights, TikTok Analytics, Pinterest Analytics, YouTube Studio
- All free. All sufficient. Check weekly per the analytics playbook.
- **Limitation:** no cross-platform view, no historical export beyond ~ 90 days. That's what GA4 + Looker Studio fix.

#### Google Analytics 4 — **USE NOW (this week)**
- Free, unlimited.
- Purpose: site-side conversion tracking, attribution, audience building.
- See `PLAYBOOK-ANALYTICS.md` § 6 for setup.
- **Skip the upgrade:** GA4 has no paid tier you'd need. GA360 starts at ~ 50K€/yr. Not for you.

#### Looker Studio — **USE LATER (Month 2)**
- Free, unlimited dashboards.
- Connect GA4 directly (free). For Inst/TikTok/Pin, you need a paid connector (Porter Metrics 14$/mo, Supermetrics 39$/mo+).
- **Skip the upgrade until:** you're spending > 30 min/week pulling numbers by hand. The connector pays for itself when it saves > 2h/month.
- Free workaround: build a GA4-only dashboard now (covers source attribution + waitlist conversion). Add native social later via manual CSV upload to Sheets → Looker Studio (clunky but free).

---

## 4. Content design

### Recommendation: **Canva free** as primary, **Figma free** for anything brand-systemic

#### Canva free — **USE NOW**
- Free: 250K+ templates, basic photo editing, 5GB cloud
- Paid: Pro 12.99€/mo, includes background remover, brand kit, 100GB
- **Skip the upgrade until:** the brand kit limitation actually slows you down (Month 2–3). You can manually re-apply colors/fonts in free.
- **Warning:** Canva's AI generation is bad with French (memory: feedback_canva_generate.md). Use Canva for layout, not for AI text/image generation.

#### Figma free — **USE NOW for brand systems**
- Free: 3 active design files, unlimited personal drafts
- Use it to maintain the master brand asset library, social templates, and post mockups.
- **Skip the upgrade until:** you have a collaborator or > 3 active projects. Then 15$/mo.

#### Adobe Express — **SKIP**
- Free tier exists but workflow is fragmented vs Canva. Only worth it if Asma already lives in the Adobe ecosystem (she doesn't — confirmed via session state).

---

## 5. Video editing

### Recommendation: **CapCut free** for short-form, **Descript free** for talking-head / cleanup

#### CapCut — **USE NOW**
- Free: 1080p export, auto-captions (multiple languages incl. French), templates, no watermark on basic exports
- Paid: Pro 7.99$/mo
- Best free short-form editor on the market. Owned by ByteDance (TikTok's parent), so optimization for TikTok formats is baked in.
- **Skip the upgrade until:** you specifically need 4K export or commercial-licensed effects (pre-launch you don't).

#### Descript — **USE NOW (when relevant)**
- Free: 1 hour transcription/month, basic editing, watermark on exports
- Paid: Creator 12$/mo (10h transcription, no watermark), Pro 24$/mo
- Best for: cleaning up voiceovers, removing filler words, quickly editing talking-head Reels via transcript.
- **Skip the upgrade until:** you publish > 1 talking-head video per week (likely Month 2).

#### Veed — **SKIP**
- Browser-based, decent free tier but watermark on free exports and weaker than CapCut for vertical short-form. Use only if CapCut fails on a specific OS.

#### Premiere Pro / Final Cut — **SKIP** (overkill pre-launch)

---

## 6. UGC discovery & monitoring

### Recommendation: **TikTok native search + Instagram Reels search + Google Alerts** (all free)

#### TikTok native search — **USE NOW**
- Search: "k-beauty france", "soin coréen", "routine glass skin français", "anua", "beauty of joseon avis", + each curated brand name
- Save creators to a "watchlist" Notion page
- Engage authentically (comment, save, share)

#### Instagram Reels search — **USE NOW**
- Same brand + niche keywords. Use the Reels tab specifically, not Posts.
- Plus hashtags: #kbeautyfrance #soincoréen #routinekbeauty

#### Google Alerts — **USE NOW**
- Free. Set alerts for: "Sonagi Beauty", "Sonagi", "@sonagibeauty", + each top curated brand.
- Daily digest to contact@sonagibeauty.com.
- Catches blog mentions, press, forum chatter that platform-native search misses.

#### Brand24, Mention, Brandwatch — **SKIP for now**
- Brand24: 149$/mo entry. Mention: 79$/mo. Brandwatch: enterprise (4-figure /mo).
- **Skip until:** you cross 5K followers across platforms AND you're actively running press outreach (likely Month 3+).
- Free alternative until then: F5Bot (free, monitors Reddit + Hacker News + Lobsters — useful if Sonagi gets discussed in r/AsianBeauty or r/SkincareAddictionEU).

---

## 7. Influencer discovery

### Recommendation: **Modash free trial (when ready)** + **manual TikTok/IG search** until then

#### Modash — **USE LATER (Month 2, week 6 outreach push)**
- Free trial: 14 days, 20 profile views, 6 email unlocks, 10 tracked creators
- Paid: from 199$/mo (Lite tier)
- Database: 350M+ creators across IG/TikTok/YT
- **How to use the trial:** save it for the week you've decided to do outreach to 6–10 micro-influencers. Don't burn it browsing.
- **Skip the paid plan until:** you have > 20 active influencer relationships to track or are running > 3 paid collabs/month (post-launch territory).

#### Heepsy — **USE LATER (free plan, lighter)**
- Free plan exists, smaller database (14M vs 350M)
- Use as supplemental to Modash trial.

#### Manual search — **USE NOW**
- Spend 30 min/week on TikTok + IG searching: French micro-influencers in K-beauty / skincare / lifestyle.
- Build a Notion table with: handle, follower count, engagement rate (manually calc on last 9 posts), avg views, content style fit, contact.
- Target: 50 prospects identified by end of Month 2. From those, 8–12 outreach in Month 3.

---

## 8. Mention monitoring (already covered above)

See section 6. **Google Alerts + native platform search is enough until 5K total followers.**

---

## 9. Email / waitlist capture

### Recommendation: **Brevo free** (RGPD-native, France-hosted, no contact cap)

#### Brevo (ex-Sendinblue) — **USE NOW**
- Free: 300 emails/day (~9,000/month), unlimited contacts, basic automation, drag-drop editor, double opt-in, RGPD tools native, French interface, French support
- Paid: Starter 9€/mo (5K sends, no Brevo logo), Business 18€/mo (multi-step automation, A/B test, send-time optimization)
- **Why this over Mailchimp:** Brevo data is hosted at OVH in France. Mailchimp transfers to US (Intuit). For a French brand collecting French consumer emails, Brevo removes the entire CLOUD-Act / Privacy-Shield headache. Plus pricing model is by sends not contacts — better for a growing waitlist.
- **Skip the upgrade until:** you hit 200 confirmed contacts AND you want to remove the Brevo logo (~ Month 2). Then jump straight to Business 18€/mo (skip Starter — A/B testing is what you actually want for the welcome sequence).

#### Mailchimp — **SKIP**
- Free tier capped at 250 contacts / 500 sends. You will hit the cap fast. Worse RGPD posture. Marketing emails feel inferior.

#### Resend — **DO NOT USE FOR MARKETING**
- Already wired into sonagibeauty.com for transactional (form confirmations, etc.). It is a developer-grade transactional API, not a marketing/newsletter platform. Do not send marketing campaigns through Resend — wrong tool, no compliance UI, no list management.

---

## 10. Optional / edge tools

### Notion — **USE NOW** (free)
- Personal plan: free, unlimited pages, 7-day version history
- Use for: content calendar (see Notion's free Social Media Calendar template), influencer prospect database, weekly review log, idea capture
- **Skip the upgrade until:** you collaborate with > 1 person.

### Google Sheets — **USE NOW** (free)
- For UTM library, KPI tracker, manual analytics export.

### Trello / Asana — **SKIP**
- Notion does the same job. Don't fragment your workflow.

### Hootsuite Insights, Sprinklr, Talkwalker — **SKIP** (enterprise)

### ChatGPT Plus / Claude Pro — **OPTIONAL, USER ALREADY HAS**
- For content drafting, not for replacing strategy. User already has access. No new spend.

---

## 11. Decision matrix — what to set up THIS WEEK

```
Tool                     Action this week               Time budget
─────────────────────────────────────────────────────────────────────
GA4                      Configure conversion events    90 min
UTM library (Sheet)      Build template                 30 min
Brevo                    Sign up, build waitlist form   60 min
Metricool                Sign up, connect 4 accounts    30 min
Buffer                   Sign up as backup              15 min
Canva                    Build brand kit (manual)       60 min
Notion content calendar  Duplicate template + customize 45 min
Google Alerts            Set 8–10 alerts                10 min
links.sonagibeauty.com   Build + deploy                 3 h
─────────────────────────────────────────────────────────────────────
TOTAL (one-time setup)                                   ~7 hours
```

After this one-time setup, ongoing tool maintenance is < 30 min/week.

---

## 12. Total cost summary

| Phase | Required spend | Optional spend |
|---|---|---|
| Month 1 (Foundation) | 0€ | 0€ |
| Month 2 (Acceleration) | 0€ | Brevo Business 18€/mo when > 200 contacts |
| Month 3 (Pre-launch sprint) | 0€ | Modash trial (free), Brevo (18€) |
| Launch (T-0) | ~ 18€/mo Brevo | Canva Pro 13€, CapCut Pro 8€ → total ~ 39€/mo |

**The single tool worth paying for first:** Brevo Business at 18€/mo. It unlocks A/B subject lines, send-time optimization, and removes the Brevo logo — all of which materially affect the waitlist's conversion to launch-day buyers.

**The trap to avoid:** signing up for Hootsuite, Sprout, or any enterprise scheduler "to be ready for launch." You will spend 100€+/mo on features you never use. Stay free until a free tool is *actively* the bottleneck.
