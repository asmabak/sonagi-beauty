# 90-DAY LAUNCH PLAN
**Sonagi Beauty | Pre-launch roadmap (Weeks 1–12)**
**Goal:** 800–1,000 confirmed waitlist signups by end of Week 12, ready for launch
**Time budget:** ~10–12 hours/week (Asma solo)
**Time zone:** Europe/Paris
**Last updated:** 2026-04-17

---

## How this plan is structured

- **Month 1 — Foundation (Weeks 1–4):** build the operational system. Cadence > virality. The system you build this month determines what's possible Month 3.
- **Month 2 — Acceleration (Weeks 5–8):** scale content output, plant Pinterest + YouTube seeds (long-tail SEO), open micro-influencer conversations.
- **Month 3 — Pre-launch sprint (Weeks 9–12):** waitlist density push, partner activations, press, the 15%-welcome teaser, content density spike.

Each week has:
- **Theme** (one sentence)
- **Content output** (per platform, with numbers)
- **Engagement budget** (minutes/day)
- **Specific named actions** (you can copy these into a task manager)
- **Success criteria** (how you know the week worked)

Brand voice across all weeks: **Provocative Educator**. French audience 18–35. No catalog yet — every CTA points to waitlist or quiz. No fake products in any AI/visual content (memory: feedback_no_fake_products.md).

---

# MONTH 1 — FOUNDATION (Weeks 1–4)

## Week 1: Build the system (this week is the most important)

**Theme:** "Plumbing week." If the plumbing leaks, every later week leaks.

**Content output:** **2 posts** total (bare minimum — system-building takes priority).
- Instagram: 1 introduction Reel (founder POV, 30s, French)
- TikTok: 1 short hook video (15s, French) — same script, repurposed

**Engagement budget:** **20 min/day** (low — you're setting up).

**Success criteria end of week:** GA4 firing conversion events, UTM library populated, Brevo waitlist form live with hidden source field, 4 platform accounts scheduled in Metricool, Notion content calendar populated for Weeks 2–4.

### Day-by-day for Week 1 (the literal Mon→Sun)

#### **Monday — Foundation: Tracking layer (1.5h)**
- 09h00–09h45: GA4 — create the 8 conversion events listed in `PLAYBOOK-ANALYTICS.md` § 6
- 09h45–10h15: Test the events using GA4 DebugView (visit each tracked page, confirm events fire)
- 10h15–10h30: Build the UTM library Google Sheet (`social-media/UTM-LIBRARY.csv` template — see Analytics playbook § 7)

#### **Tuesday — Email & waitlist (1.5h)**
- 09h00–09h30: Brevo — create account, choose French interface, OVH-France hosting confirmed
- 09h30–10h15: Build the waitlist form in Brevo. **Critical:** add hidden field `signup_source` populated by JS reading `?utm_source=` from URL
- 10h15–10h30: Embed form on `/waitlist` page of sonagibeauty.com
- Test: open the page with `?utm_source=test`, sign up, confirm the source lands in Brevo contact record

#### **Wednesday — Scheduling + brand kit (1.5h)**
- 09h00–09h30: Metricool — sign up, connect Instagram, TikTok, Pinterest, YouTube
- 09h30–10h00: Buffer — sign up as backup, connect 3 channels
- 10h00–10h30: Canva — build brand kit manually (logo, hex codes, font choices) per `canva-specs.md`

#### **Thursday — Content production day (2h)**
- 09h00–10h30: Shoot/record the introduction Reel in French.
  - Hook (s 0–3): "On t'a menti sur la K-beauty. Et je vais te le prouver." (Provocative-Educator opener)
  - Body (s 3–25): 3 sharp myths + 3 sharp truths
  - CTA (s 25–30): "Liste d'attente en bio. Tu reçois l'enquête en avant-première."
- 10h30–11h00: Edit in CapCut — auto-captions in French (verify accents — memory: feedback_french_accents.md)
- 11h00–11h30: Export 2 versions (9:16 for IG/TikTok, 1:1 for IG feed safety)

#### **Friday — Link-in-bio + first content drop (1.5h)**
- 09h00–11h00: Build `links.sonagibeauty.com` — single page, 5 links, deploy via Netlify CNAME
- Schedule the Reel for **Tuesday next week, 12h30** (Instagram) and **Wednesday, 13h00** (TikTok) — staggered so analytics signals are clean

#### **Saturday — Engagement OS bootstrap (45 min)**
- Build a "watch list" Notion DB of 30 French K-beauty / skincare creators to engage with
- Follow them. Comment on 5 of their recent posts thoughtfully.

#### **Sunday — First weekly review + planning (1h)**
- Run the weekly review template (`PLAYBOOK-ANALYTICS.md` § 3) even though there's almost no data yet — the habit matters more than the numbers this week
- Populate Notion content calendar for Weeks 2, 3, 4 with: 12 IG Reels, 12 TikToks, 8 Pinterest pins, 4 YT Shorts (= the Month 1 production target)

**Week 1 total time investment:** ~9.5 hours.

---

## Week 2: First posting cadence

**Theme:** "Ship the cadence." Stop perfecting; start shipping at the cadence you can sustain.

**Content output:**
- Instagram: 3 Reels + 2 carousel educational posts + 5 Stories
- TikTok: 4 short videos (mix: 2 educational, 1 founder POV, 1 trend-rideable)
- Pinterest: 5 pins (each linking to a blog post or waitlist landing — UTMs!)
- YouTube: 1 Short (repurposed from a TikTok)

**Engagement budget:** **30 min/day, split:** 15 min on IG (replies, DMs, comments on watch-list creators), 15 min on TikTok (replies, comments, duets you save for later).

**Specific actions:**
- Mon: publish the IG Reel (delayed from W1 schedule); engage 30 min
- Tue 12h30: IG Reel #2 publishes
- Wed 13h00: TikTok #1 publishes; Pinterest 2 pins go live
- Thu: Brevo — write the welcome email (the one signups get on confirm). Subject line A/B test setup.
- Fri 18h: IG Reel #3 + TikTok #2
- Sat: 30 min creator engagement on TikTok (reply to comments, DM 2 micro-creators with genuine compliment + light intro)
- Sun: weekly review

**Success criteria:** First 10 waitlist signups attributed (via UTM) to a specific platform. If 0 signups, diagnose: is the form broken? Is the CTA buried? Re-test the funnel before producing more content.

---

## Week 3: First content pillar test

**Theme:** "Find what works." This week we test 3 distinct content pillars and watch which gets traction.

**The 3 pillars to test:**
1. **Myth-busting** ("Ce que les marques européennes ne te disent pas sur la K-beauty")
2. **Curated discovery** ("3 marques coréennes que tu ne trouveras jamais en Sephora")
3. **Ritual / texture / sensory** (visual-led, ASMR-adjacent — memory: feedback_no_exaggerated_claims.md)

**Content output:**
- Instagram: 4 Reels (2× pillar 1, 1× pillar 2, 1× pillar 3) + 2 carousels + 6 Stories
- TikTok: 5 short videos (one of each pillar twice)
- Pinterest: 8 pins (mix of all 3 pillars)
- YouTube: 1 Short

**Engagement budget:** 30 min/day, same split.

**Specific actions:**
- Activate Stories engagement: 1 question sticker per day on IG ("Quelle marque K-beauty tu rêves d'essayer ?" → DM responder)
- Cross-post the IG Reel that performs best to TikTok and YouTube Shorts on Friday
- Sat: review **per-pillar** save rate, share rate, link-click rate. Note the winner.

**Success criteria:** 25 cumulative waitlist signups. One pillar shows 2x the engagement of the other two — that's your wedge for Month 2.

---

## Week 4: Double down + Month 1 retrospective

**Theme:** "Lock the winner." Scale the winning pillar; cut or rework the laggard.

**Content output:**
- Instagram: 4 Reels (3 in winning pillar, 1 in second-best) + 2 carousels + Stories daily
- TikTok: 5 videos (4 in winning pillar)
- Pinterest: 8 pins (re-pin best blog content + 4 new)
- YouTube: 2 Shorts

**Engagement budget:** **40 min/day** (now scaling — more comments to reply to).

**Specific actions:**
- Mon: Pinterest — set up 5 boards properly (Routine matin, Routine soir, Glass skin, Marques découvertes, Ingrédients K-beauty). All boards keyword-optimized in French.
- Wed: Brevo — send first newsletter to existing signups. Theme: "Bienvenue dans le cercle Sonagi." Soft, no sell.
- Fri: post a "behind the scenes" on Stories (sourcing process, no products, just process) — humanize.
- Sun: **Month 1 retrospective** (use template in `PLAYBOOK-ANALYTICS.md` § 4).

**Success criteria end of Month 1:**
- ≥ 50 waitlist signups
- Posting cadence proven sustainable (no week missed)
- 1 winning pillar identified with data
- 4-week trend on follower growth visible

---

# MONTH 2 — ACCELERATION (Weeks 5–8)

## Week 5: Scale the winning pillar + Pinterest serious-mode

**Theme:** "Become the K-beauty curator on Pinterest."

Pinterest is a 90-day SEO compounding play. We start serious now so the traffic shows up in Month 3.

**Content output:**
- Instagram: 4 Reels + 3 carousels + daily Stories
- TikTok: 6 videos (cadence push from 5 → 6/week)
- **Pinterest: 15 pins/week** (big jump). Each pin = 1 blog post or 1 quiz / 1 waitlist landing
- YouTube: 2 Shorts

**Specific actions:**
- Mon: write 3 SEO-optimized blog posts on sonagibeauty.com (each → multiple Pinterest pins). Topics: "Routine K-beauty pour peau sensible", "Différence essence vs sérum", "10 ingrédients K-beauty incontournables".
- Tue–Fri: design 15 Pinterest pins (Canva, French keyword titles, vertical 1000×1500)
- Sun: review which pillar still wins. Don't switch yet.

**Success criteria:** 80 cumulative signups. Pinterest impressions cross 5K/week (baseline establishes).

---

## Week 6: Micro-influencer outreach (the soft kind)

**Theme:** "Open relationships, don't pitch yet."

**Content output:** keep Week 5 cadence. Don't add output — add depth.

**Specific actions:**
- Mon: activate the Modash 14-day trial. Use the 20 profile views to vet your top 20 prospects from Notion.
- Tue: build the outreach DB — 10 final targets. Criteria: French, 5K–25K followers, 2.5%+ engagement, K-beauty/skincare/lifestyle, *no* prior brand-deal saturation in feed.
- Wed–Fri: send 10 personalized DMs. **No pitch.** Format:
  > "Salut [prénom], on m'a parlé de ton contenu sur [specific post]. Je lance Sonagi Beauty, une curation K-beauty pour le marché français — pas encore de boutique mais on construit la communauté en avance. Aucune demande, juste : ton avis sur [specific question relevant to their content] m'intéresserait."
- Track responses in the same Notion DB.

**Success criteria:** 4 of 10 reply (40% reply rate is good for cold). 1 schedules a call/voice DM. **Do not** ask for content yet.

---

## Week 7: YouTube channel activation + first viral attempt

**Theme:** "Plant the YouTube seed + take one big swing."

**Content output:**
- Instagram: 5 Reels (cadence push) + 3 carousels
- TikTok: 6 videos
- Pinterest: 15 pins
- **YouTube: 1 long-form (8–12 min) + 3 Shorts**

**Specific actions:**
- The long-form: "J'ai testé 10 marques K-beauty pour 1 mois. Voilà ce qui vaut le coup (et ce qui est surfait)." Voice + B-roll, no on-camera required if Asma prefers.
- Mid-week: **the brand-voice viral attempt** — one Reel that takes a stronger position than usual. Example: "Pourquoi je ne vendrai jamais [popular K-beauty product] sur Sonagi" — provocative, defensible, brand-coherent. Accept it might flop. The point is to test the ceiling.
- Sun: weekly review — note if the viral attempt drove disproportionate signups vs reach.

**Success criteria:** 200 cumulative signups. YouTube channel published with first video + thumbnail proper.

---

## Week 8: Month 2 retrospective + influencer activation prep

**Theme:** "Lock relationships, prep Month 3."

**Content output:** maintain Week 7 cadence (5 IG Reels, 6 TikToks, 15 pins, 1 long YT, 3 Shorts).

**Specific actions:**
- Mon: of the 4 influencers who replied in Week 6, deepen 2 — voice DM, share something exclusive (early Sonagi visual? sample selection list?), no ask.
- Wed: from Brevo data, identify your 20 most-engaged email subscribers. Send them a personal email asking for input on the launch (real input, not theatre).
- Fri: build the **press list** — 30 French beauty journalists / bloggers. Sources: Madmoizelle, Marie Claire FR beauty, ELLE FR, Nuoo, Beauté Test, niche substacks. Save in Notion.
- Sun: **Month 2 retrospective** (`PLAYBOOK-ANALYTICS.md` § 4).

**Success criteria end of Month 2:**
- ≥ 250 cumulative waitlist signups
- 2 micro-influencers in active relationship (not transactional yet)
- Pinterest hitting 20K+ impressions/month
- One YouTube long-form published
- One brand-voice viral attempt completed (regardless of result)
- Press list of 30 ready

---

# MONTH 3 — PRE-LAUNCH SPRINT (Weeks 9–12)

## Week 9: Waitlist density push + 15% welcome teaser kickoff

**Theme:** "Tell people there's a reward for being early."

**Content output:**
- Instagram: 6 Reels (cadence push) + 4 carousels + Stories daily with waitlist sticker
- TikTok: 7 videos
- Pinterest: 18 pins
- YouTube: 1 long-form + 3 Shorts

**Specific actions:**
- Mon: announce the **"15% off launch + early access 48h before public"** waitlist incentive. Single asset across all platforms (Reel + carousel + pin + Short + email).
- Tue: in Brevo — build the **waitlist welcome sequence v2**:
  - Email 1 (instant): "Bienvenue. Voilà ton code, garde-le." (the 15% code, even though shop isn't live)
  - Email 2 (D+3): "Pourquoi la K-beauty européenne te ment" (the brand manifesto)
  - Email 3 (D+10): "3 marques que je curate pour toi" (anticipation)
  - Email 4 (D+21): "Quel est le rituel qui te ressemble ?" (quiz drive)
- Wed: pin the announcement Reel at top of IG profile.
- Sun: weekly review.

**Success criteria:** 350 cumulative signups (+ 100 in this week alone). Welcome sequence open rate > 50% on email 1.

---

## Week 10: Partner / influencer activations (paid + barter mix)

**Theme:** "Borrow audiences."

**Content output:** maintain Week 9 cadence.

**Specific actions:**
- Mon: from the 2 deepened influencer relationships, propose: "Tu partages la liste d'attente en story une fois, je te garantis [exclusive: first access to samples / collab on launch product / podcast guest spot]." No money exchanged yet.
- Wed: launch a **collab Reel** with one of the influencers (joint post if IG Collab feature; otherwise dual-publish).
- Fri: identify 3 French micro-creators with 2K–5K followers (true nano-influencers — easier to activate, often deeper engagement) and offer the same.
- Throughout week: Asma personally engages 10× per day in the comments of partner posts.

**Success criteria:** 500 cumulative signups. At least 30 attributed via `utm_source=partner-collab` or `utm_campaign=2026-07-influencer-week`.

---

## Week 11: Press outreach + content density spike

**Theme:** "Get on someone else's page."

**Content output:**
- Instagram: 7 Reels + 5 carousels + Stories twice daily
- TikTok: 8 videos
- Pinterest: 20 pins
- YouTube: 1 long-form + 4 Shorts

**Specific actions:**
- Mon–Tue: send personalized press emails (from the list of 30 built in Week 8). Subject pattern: "Sonagi Beauty — la curation K-beauty française qui assume" + personal hook per recipient. Not a press release. A 4-paragraph human email.
  - Para 1: why I'm writing to *this specific* journalist
  - Para 2: what Sonagi is in 2 sentences
  - Para 3: what's interesting/unique now (the curation philosophy, the pre-launch waitlist of 500, the brand voice positioning)
  - Para 4: ask (a 15-min call OR an exclusive on the brand-launch story — give them a choice)
- Wed: publish the **"manifesto" piece** — a long-form blog post + carousel + Reel + YT video, all the same idea. SEO-optimized for "K-beauty France 2026" and adjacent keywords.
- Fri: re-engage the 30 most-engaged email subscribers with a personal "Quand on lance, vous serez 48h en avance. Voilà ce qu'on prépare. Vous voulez voir un sneak peek ?"
- Sun: weekly review.

**Success criteria:** 700 cumulative signups. ≥ 1 press response (email reply, not necessarily article — yet).

---

## Week 12: Final density spike + launch-readiness audit

**Theme:** "All hands on deck. Get to 1,000."

**Content output:** Week 11 cadence + add 1 daily IG Story poll/question.

**Specific actions:**
- Mon: announce launch date publicly. "Le [date] on ouvre la boutique. Liste d'attente fermée à [N] inscrits = J-7."
- Tue–Fri: daily countdown content (1 Reel + 1 TikTok + 1 Story per day). Each day reveals a different curated brand on the launch list.
- Wed: send Brevo email: "On y est. Confirmez votre adresse en 1 clic pour garder votre 15% — sinon vous perdez la priorité." (re-engagement / cleanup pass).
- Thu: re-out to the 4 micro-influencers who never replied in Week 6 + the press list. Update them with the social proof: "On a passé les 800 inscrits. Si l'angle Sonagi t'intéresse maintenant, on peut parler."
- Fri: **the personal pre-launch livestream** — IG Live + TikTok Live, 20–30 min, "Ce que vous allez trouver lundi, en avant-première." Even with 50 viewers, generates 4–6 signups.
- Sat: rest. Yes, actually rest. Launch week is heavier than this and you can't deplete your runway now.
- Sun: **Month 3 retrospective + launch-readiness checklist:**
  - Waitlist count: ___ (target 800–1000)
  - Confirmed (double opt-in) %: ___
  - Source mix: % from each platform
  - Top 5 highest-converting pieces of content (replicate angle on launch week)
  - Tools: are Brevo automations live and tested with a real address? Is the 15% code working in Stripe (memory: STRIPE-SETUP.md)?
  - Email send-day decision: launch on a **Tuesday** at **10h00 Paris** for highest open rates.

**Success criteria end of Month 3:**
- 800–1,000 cumulative confirmed waitlist signups
- ≥ 50% have opened ≥ 1 email in the welcome sequence
- ≥ 5 micro-influencer relationships warm
- ≥ 1 press piece in motion (could be week 13 publication)
- All tracking + automation tested end-to-end with a real address

---

# Cross-cutting principles (apply every week)

1. **Engagement OS:** every day, Asma personally replies to every comment + DM within 12h. This is non-negotiable pre-launch — the 100 most engaged followers will become your 100 launch-day champions.
2. **One change per week:** never test more than one variable at a time (see Analytics playbook § 3). The point of weekly cadence is *attribution*, not output volume.
3. **No fake products in AI/visual content** (memory: feedback_no_fake_products.md). Use texture, faces, hands, botanicals, real curated products only.
4. **French accents always** (memory: feedback_french_accents.md).
5. **August dead zone:** if Month 2 lands on August, reduce cadence by 30–50% and bank content for September restart. Push the launch sprint to September if needed.
6. **TikTok policy risk:** France passed a minor-protection bill at first reading (Jan 2026). Watch but don't panic — it targets minors and platform design, not brand accounts. Diversify to Pinterest + IG + YouTube as insurance, which this plan already does.
7. **Engagement minutes/day budget across 12 weeks:**
   - Weeks 1–4: 20–40 min/day
   - Weeks 5–8: 40–50 min/day
   - Weeks 9–12: 60 min/day
   - Always at the same window (suggested: 19h–20h Paris) so it becomes habit not burden

# Time budget summary

| Phase | Hours/week | Content hours | Engagement hours | Analytics + ops |
|---|---|---|---|---|
| Month 1 | 9–11 | 5 | 2.5 | 1.5–3.5 |
| Month 2 | 11–13 | 7 | 3.5 | 0.5–2.5 |
| Month 3 | 13–15 | 8 | 5 | 1–2 |
| **Avg.** | **~12** | **~7** | **~3.5** | **~1.5** |

If you cannot consistently commit 10h/week, halve the content output but keep the cadence. Half the volume on time beats full volume sporadic.
