# PLAYBOOK — Analytics & Measurement
**Sonagi Beauty | Pre-launch (T-3 to T-6 months)**
**Owner:** Asma | **Cadence:** Weekly (Sun) / Monthly (1st) / Quarterly
**Last updated:** 2026-04-17

---

## 0. Why this playbook exists

You are pre-launch. You don't have revenue to optimize. You have **one number that matters** (waitlist signups) and a handful of leading indicators. Everything else — likes, follows, impressions — is noise that *might* explain the number, or vanity that distracts from it.

This document defines:
1. The KPI tree (north star → drivers → supporting)
2. Per-platform numeric benchmarks (good / great / red flag)
3. Weekly / monthly / quarterly review templates
4. GA4 event setup on sonagibeauty.com
5. UTM convention (the *exact* strings to use)
6. Conversion attribution back to source
7. When to A/B test, when not to
8. How to read data without lying to yourself

If you only have 30 minutes a week for analytics, do **Section 3 — Weekly Review**. Skip everything else.

---

## 1. The KPI Tree

```
                    NORTH STAR
            Waitlist signups (weekly)
                       |
        +--------------+--------------+
        |                             |
     REACH                       CONVERSION
   (top of funnel)             (bottom of funnel)
        |                             |
   - Impressions                 - Profile visits
   - Reach                       - Link-in-bio clicks
   - Follower growth             - Landing page CVR
   - Hashtag/SEO                 - Email confirmation rate
   - Pinterest outbound clicks
        |                             |
        +--------------+--------------+
                       |
              SUPPORTING (signal)
                       |
   - Saves (intent to return)
   - Shares (organic distribution)
   - Watch time / completion rate (TikTok, Reels, Shorts)
   - Story replies / DM volume (depth of relationship)
   - Comment sentiment (qualitative)
```

**Read the tree like this:** if the north star moves, look up to see *which driver* moved with it. If the north star is flat, look at the supporting layer to spot leading indicators (high saves now → reach lifts in 2 weeks → signups follow).

**Pre-launch target (first 90 days):**
- Weeks 1–4: 50 waitlist signups (proof the system works)
- Weeks 5–8: 250 cumulative (proof of repeatability)
- Weeks 9–12: 800–1,000 cumulative (launch-ready audience)

These are deliberately conservative. A French K-beauty curator with no catalog and no paid spend should not plan for "viral." Plan for compound.

---

## 2. Per-platform KPI table

All numbers below are for accounts under **5,000 followers in the beauty/lifestyle niche**. Above 5K, expectations shift downward (engagement rate naturally drops with scale).

### Instagram

| Metric | Red flag (kill or fix) | Good | Great |
|---|---|---|---|
| Engagement rate (per post) | < 1.0% | 1.5–3.0% | > 4.0% |
| Reel reach / followers | < 30% | 50–100% | > 150% (non-followers reached) |
| Carousel save rate | < 1% | 2–4% | > 6% |
| Profile visits / reach | < 2% | 3–5% | > 8% |
| Link clicks / profile visits | < 5% | 8–12% | > 15% |
| Follower growth / week | < 0.5% | 1–3% | > 5% |
| Story completion rate | < 50% | 60–75% | > 85% |
| DMs / week (organic) | 0–2 | 5–15 | > 25 |

Sources: 2026 benchmarks aggregated from Buffer, Hootsuite, CreatorFlow.

### TikTok

| Metric | Red flag | Good | Great |
|---|---|---|---|
| Avg view % (completion) | < 25% | 40–60% | > 70% |
| Reach (For You vs Following) | < 60% FYP | 80–90% FYP | > 95% FYP |
| Engagement rate | < 3% | 5–8% | > 10% |
| Saves per video | < 5 | 20–80 | > 200 |
| Profile visits / view | < 0.5% | 1–2% | > 3% |
| Bio link clicks (CTR from profile) | < 5% | 8–15% | > 20% |
| Follower growth / week | < 1% | 3–8% | > 15% |

Note: TikTok engagement % is structurally higher than Instagram — apples and oranges, do not compare directly.

### Pinterest

| Metric | Red flag | Good | Great |
|---|---|---|---|
| Impressions / month | < 5K | 20K–100K | > 500K |
| Outbound clicks / month | < 50 | 200–500 | > 1,500 |
| Click-through rate (Pin → site) | < 0.3% | 0.5–1.0% | > 1.5% |
| Saves (repins) per Pin | < 2 | 5–20 | > 50 |
| Idea Pin reach | < 500 | 2K–10K | > 25K |
| Follower growth / month | < 5% | 10–25% | > 40% |

Pinterest is a 90-day SEO play — judge it on month-over-month trend, **not** week-over-week.

### YouTube (Shorts-led at this stage)

| Metric | Red flag | Good | Great |
|---|---|---|---|
| Shorts views / video | < 200 | 1K–10K | > 50K |
| Avg view duration (Shorts %) | < 50% | 65–80% | > 90% |
| Subscribers gained per Short | < 1 | 5–20 | > 50 |
| Click-through rate (long-form) | < 2% | 3–5% | > 7% |
| Audience retention (long-form) | < 30% | 40–55% | > 60% |

### Email (waitlist itself)

| Metric | Red flag | Good | Great |
|---|---|---|---|
| Signup-to-confirm rate | < 50% | 65–80% | > 90% |
| Welcome email open rate | < 35% | 45–60% | > 70% |
| Unsubscribe rate / send | > 1.0% | 0.2–0.5% | < 0.1% |
| List growth / week | < 1% | 3–8% | > 12% |

---

## 3. Weekly review template (every Sunday, 30 min)

Run this every Sunday evening. Block 19h00–19h30 in your calendar. **Do not skip.**

### A. Pull the numbers (10 min)
Open one tab per platform. Grab the *last 7 days* (Mon–Sun).

```
Week of: __________
                  Inst  TikTok  Pin  YT   Total
Posts published    ___   ___    ___  ___   ___
Reach              ___   ___    ___  ___   ___
Engagements        ___   ___    ___  ___   ___
Profile visits     ___   ___    -    ___   ___
Link clicks        ___   ___    ___  ___   ___
Followers (Δ)      ___   ___    ___  ___   ___
Waitlist signups (from GA4): ___
```

### B. Pick the winner and the loser (10 min)
- **Top post this week:** which one and why? (hook, format, hashtag, time?)
- **Worst post this week:** which one and why?
- One-sentence hypothesis on each.

### C. Decide one thing for next week (10 min)
You are allowed *one* deliberate change per week. More than one and you cannot attribute the result. Examples:
- "Move IG posting from 18h to 12h30 (lunch window) all week."
- "Test problem-aware hooks instead of curiosity hooks on TikTok."
- "Add CTA card at second 8 of every Reel."

Write it down. Next Sunday, judge it.

### D. Red-flag check
Any metric in the "red flag" column for 2 weeks running? Stop scaling that pillar. Diagnose before producing more of the same.

---

## 4. Monthly review template (1st of month, 90 min)

### A. Compile (30 min)
Pull a clean spreadsheet (or Looker Studio dashboard) covering:
- 4 weeks of per-platform metrics from Section 2
- Waitlist growth (raw count + % growth MoM)
- Source attribution: % of signups from Inst / TikTok / Pin / YT / direct / referral
- Top 5 posts across all platforms by **link clicks** (not likes)

### B. Optimize (30 min)
- **Double down:** which content pillar produced > 50% of waitlist signups? Plan 2x more of it next month.
- **Cut:** which pillar produced < 5%? Reduce to 1 post/week max or kill outright.
- **Time-of-day audit:** which posting window converts best? Lock it in for the whole next month.
- **Hashtag/SEO audit:** which 3 hashtags or keywords drove discovery? Bias toward them.

### C. Kill list
What are you doing because you "should" but it's not moving the needle? Examples to watch for:
- Posting on LinkedIn (kill — wrong audience for B2C beauty)
- Twitter/X (kill — French beauty audience is not there)
- Daily Stories with no CTA (kill or add the CTA)
- "Behind the scenes" content with < 1% CVR to link click (kill or restructure)

### D. Plan next month
- 1 brand-voice viral attempt (high-risk hook, accept it might flop)
- 4 educational pillar posts per platform (the workhorse)
- 1 community/UGC repost per week
- 1 partnership / collab outreach test

---

## 5. Quarterly review template (every 90 days)

This is a strategy reset, not a tactical one.

1. **Source mix shift:** how did the % attribution to each platform change? Is one channel becoming 80% of signups (concentration risk)?
2. **Cost per signup:** even pre-launch, divide your *time* (hours/week × 12 weeks × €30/h opportunity cost) by signups. Is it dropping?
3. **Audience quality:** of the 100 most recent signups, how many opened ≥ 1 email? How many clicked? Pre-launch waitlists rot fast — a 1,000-person list with 20% engagement is worth less than a 300-person list at 60%.
4. **Brand voice fit:** read your last 30 captions. Do they still sound like "Provocative Educator" or has the tone slid into safe/generic?
5. **Pillar rotation:** retire the worst-performing content pillar. Pilot a new one for 6 weeks. Re-evaluate.
6. **Tool stack audit:** what are you paying for that you're not using > 2x/week? Cancel it.

---

## 6. GA4 setup on sonagibeauty.com

Goal: every signup is attributable to a source. Without this, every other section is theatre.

### Events to create (mark as conversions)

| Event name | Trigger | Why it matters |
|---|---|---|
| `waitlist_signup_submit` | Form submit on /waitlist | Primary conversion |
| `waitlist_signup_confirm` | Double-opt-in confirm page view | True conversion (post-RGPD) |
| `quiz_start` | "Start quiz" button click | Pre-launch lead magnet engagement |
| `quiz_complete` | Last screen of quiz reached | High-intent signal |
| `social_outbound_click` | Click on any social icon | Reverse-flow tracking |
| `nav_click_curated_brands` | Click on the "marques" page link | Browsing intent |
| `time_on_page_60s` | Auto event when user stays > 60s | Engagement depth proxy |
| `scroll_75` | GA4 default scroll event tweaked to 75% | Content quality signal |

### Mandatory GA4 setup steps
1. Enable **Enhanced Measurement** (auto-tracks scroll, outbound clicks, file downloads, video engagement, site search).
2. Configure **conversion events** for the two waitlist events above.
3. Define **custom dimensions** for `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` (so they show in standard reports, not just exploration).
4. Connect GA4 to **Google Search Console** (Acquisition reports gain organic data).
5. Set up **audiences:**
   - "Quiz starters who didn't finish" → retarget with abandoned-quiz email later
   - "Returning visitors > 3 sessions, no signup" → high-intent, soft-pitch
   - "Signed up + opened ≥ 3 emails" → launch-day VIPs

### Honest limit
GA4 attribution to social is broken-by-design (most click-throughs from Inst/TikTok land in `(direct)` because in-app browsers strip referrers). The fix is **always-on UTMs** (Section 7) — never trust raw GA4 source data without them.

---

## 7. UTM convention (the literal strings)

**Lowercase always. Hyphens not underscores in slugs. No spaces. No accents.**

### Template
```
?utm_source={platform}&utm_medium={surface}&utm_campaign={campaign-slug}&utm_content={asset-id}
```

### Source values (use these EXACT strings)
- `instagram`
- `tiktok`
- `pinterest`
- `youtube`
- `email-newsletter`
- `linktree` *(only if you keep Linktree as fallback)*
- `partner-collab`

### Medium values
- `bio` — link in bio (the standing link)
- `story` — story sticker / link
- `reel` — Reel description link (when available)
- `post` — feed post caption link
- `pin` — Pinterest pin destination
- `description` — YouTube video description
- `dm` — manual DM link share
- `email` — link inside an email send

### Campaign slugs (your nomenclature)
Pattern: `{year-month}-{theme-or-launch}`
- `2026-05-foundation` — Month 1 brand-build
- `2026-06-acceleration` — Month 2 scale
- `2026-07-prelaunch-sprint` — Month 3 waitlist push
- `2026-08-launch-15off` — the welcome teaser campaign

### Content values
Use the asset ID, not the format. So a specific Reel might be `reel-007-glass-skin-myth`. This lets you compare *individual assets* in GA4, not just channels.

### Worked example (Reel posted on May 12, 2026)
```
https://sonagibeauty.com/waitlist?utm_source=instagram&utm_medium=reel&utm_campaign=2026-05-foundation&utm_content=reel-007-glass-skin-myth
```

Use a **shortener** (Bitly free, or roll your own with a Netlify redirect under `links.sonagibeauty.com/r/glass-skin`) so the user-facing URL is clean. The UTMs survive the redirect.

### Single source of truth
Maintain one Google Sheet — `social-media/UTM-LIBRARY.csv` (suggested) — with columns: `date | platform | format | asset-id | full-utm-url | short-url`. Never hand-build a UTM. Always copy from this sheet. Hand-built UTMs always have typos and typos fragment data.

---

## 8. Conversion attribution

### Last-click is the default — but it lies for social
GA4 defaults to "data-driven attribution" but for low-volume pre-launch traffic this is unreliable. Switch the default report attribution to **first-click** during pre-launch — it tells you which platform *introduced* the user, which is what you actually want to optimize for.

### The 3-source attribution stack
1. **GA4** (UTMs + conversion events) — site-side ground truth
2. **Native dashboards** (Inst Insights, TikTok Analytics, Pinterest Analytics) — pre-click behavior (saves, shares, watch time)
3. **Email tool source field** (Brevo / Mailchimp) — capture `utm_source` as a hidden form field on the signup form so it stores in the contact record forever

### The hidden-field trick (do this)
On the waitlist form, add a hidden field `signup_source` populated by JavaScript that reads the URL's `utm_source` (defaulting to `direct` if absent). Pass it to your email tool. Now every contact in Brevo has a permanent source tag. You can later segment your launch-day email by source and see if Pinterest signups buy at a different rate than Instagram signups.

---

## 9. When to A/B test (and when not to)

### Do not test until you have:
- ≥ 1,000 weekly visitors to a page (otherwise the test runs forever)
- A clear hypothesis with a directional prediction
- One change at a time

### Pre-launch, you should A/B test:
- **Subject lines** of the welcome email (Brevo splits this natively)
- **Hero copy** of the waitlist landing page (test 2 versions over 2 weeks each — sequential, not split — given low volume)
- **Hook** of the same content type — e.g. post the same Reel with two different first-3-second hooks on different weeks and compare reach

### Pre-launch, do not bother A/B testing:
- Button colors (will not move the needle at this volume)
- Image filters
- Posting time (use the data in section 11 instead)
- Anything that requires statistical significance you cannot achieve at < 1K weekly traffic

---

## 10. How to read data without deceiving yourself

### Vanity-metric warnings
- **Likes ≠ growth.** A Reel with 10K likes and 0 link clicks is entertainment, not marketing. Track link-clicks-per-1000-views as a CVR proxy.
- **Follower count without engagement is decoration.** A 5K-follower account with 1.5% engagement (75 active people) is more valuable than 20K with 0.2% (40 active people).
- **Reach without saves means nothing for waitlist.** Saves > shares > likes for predicting future conversion.
- **"Going viral" pre-launch can hurt** if the audience is wrong. A French K-beauty Reel that goes viral with US teens grows the wrong list. Watch the *audience location* tab on every viral spike.

### Base rate awareness
- Industry-average IG engagement rate is 0.7–1.5%, not 5%. Beauty *micro* accounts (10–100K) hit 2–5%. Below 5K followers you can hit 4–7% because the math is generous.
- TikTok median view-through is ~ 30–45%. Anything > 60% is genuinely above average.
- Pinterest CTR median is 0.4%. > 1% is excellent and is rarer than people pretend.

### Week-over-week vs month-over-month
- Use **week-over-week** for tactical decisions (post times, hooks, formats)
- Use **month-over-month** for strategic decisions (which platform to invest in)
- Use **3-month rolling avg** for waitlist trend (kills weekly noise from one viral spike)
- **Never** report "300% growth!" if the base was 10. Always include the base.

### The "would I bet on this?" test
Before publishing a number to a stakeholder (or to yourself in a journal), ask: "If someone asked me to bet on this number repeating next week, would I?" If no, the number is noise. Only act on numbers you'd bet on.

### Survivorship-bias trap
You will be tempted to study only your top posts to figure out what works. **Study the bottom 25% too.** What you stop doing matters as much as what you scale.

### The single most useful question every Sunday
> *"If I had to explain to a skeptical investor why this week's data means anything, what would I say?"*

If you can't answer it cleanly, the data probably doesn't mean anything yet. Wait another week and re-ask.

---

## 11. Cheat sheet: posting windows for French audience (Europe/Paris timezone)

Validate against your own data after 4 weeks — these are starting points, not laws.

| Platform | Weekday primary | Weekday secondary | Weekend |
|---|---|---|---|
| Instagram (feed/Reel) | 12h30–13h30 (lunch) | 19h–21h | Sun 11h–13h |
| TikTok | 12h–14h, 19h–22h | 7h–9h (commute) | Sat 14h–18h |
| Pinterest | 20h–23h | 14h–16h | Sun 9h–12h |
| YouTube Shorts | 17h–19h | 21h–23h | Sat/Sun 11h–14h |
| Email send | Tue/Thu 10h00 | Sun 18h | avoid Mon 9h |

### French calendar warnings
- **August** is dead — Paris empties from 1–25 August. Reduce posting cadence by 30–50%, schedule lighter content. Waitlist growth will dip; that's normal, not your failure.
- **School holidays (vacances scolaires):** roughly mid-Feb, mid-April, early-July to end-Aug, end-Oct, late Dec. Engagement spikes on visual platforms (Pinterest, Reels) during these.
- **Sunday 18h–22h** is golden for considered/educational content (the "prepare-for-Monday" mindset).
- **Avoid** posting product/sales-coded content on Sunday morning — French weekend mornings = market + family time, not screen time.

---

## 12. The one paragraph version

You have one number that matters: **weekly waitlist signups.** Track it in GA4 with conversion events, attribute every signup with disciplined UTMs, review the data every Sunday for 30 minutes, and once a month decide what to scale and what to kill. Trust saves > likes, watch time > views, link clicks > impressions. Be skeptical of viral spikes until you check audience geo. Never run more than one deliberate change per week. And accept the boring truth — pre-launch growth is compound, not viral.
