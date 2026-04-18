# THIS WEEK — Asma's Checklist
**Sonagi Beauty | Week 1 — Foundation**
**Total time: ~9.5 hours across 7 days (≈ 1.5 h/day)**
**Purpose:** install the plumbing. Two posts ship. Everything else is system-building.

Copy this entire file into a Notion page → toggle to "to-do list" view → check items off live.

---

## Monday — Tracking Layer (1.5 h, 09h00–10h30)

- [ ] Open GA4 → Admin → Events → create the 8 conversion events listed in `PLAYBOOK-ANALYTICS.md` § 6
  - [ ] `waitlist_signup_submit`
  - [ ] `waitlist_signup_confirm`
  - [ ] `quiz_start`
  - [ ] `quiz_complete`
  - [ ] `social_outbound_click`
  - [ ] `nav_click_curated_brands`
  - [ ] `time_on_page_60s`
  - [ ] `scroll_75`
- [ ] Mark `waitlist_signup_submit` and `waitlist_signup_confirm` as **conversions**
- [ ] Open GA4 DebugView → visit each tracked page on sonagibeauty.com → confirm events fire
- [ ] Create `social-media/UTM-LIBRARY.csv` Google Sheet with columns: `date | platform | format | asset-id | full-utm-url | short-url`
- [ ] Add 2 sample UTM rows so the format is locked in

## Tuesday — Email & waitlist (1.5 h, 09h00–10h30)

- [ ] Brevo — sign up at brevo.com (FR interface, OVH-France hosting confirmed)
- [ ] Brevo → Forms → create the waitlist form (name + email only, double opt-in ON)
- [ ] Add hidden field `signup_source` to the form
- [ ] Add JS to populate the hidden field from URL `?utm_source=` (default = `direct`)
- [ ] Embed the form on `sonagibeauty.com/waitlist`
- [ ] **Test end-to-end:** open `/waitlist?utm_source=test`, sign up with a real address, confirm via email, verify "test" appears in the Brevo contact record's `signup_source` field

## Wednesday — Scheduling + brand kit (1.5 h)

- [ ] Metricool — sign up free, connect Instagram, TikTok, Pinterest, YouTube accounts
- [ ] Buffer — sign up free, connect 3 channels (backup)
- [ ] Canva — open `brand-strategy/brand-identity/canva-specs.md`, build the brand kit manually (logo upload, hex codes, font choices)

## Thursday — Content production day (2 h, 09h00–11h00)

- [ ] Write the introduction Reel script in French (30 seconds):
  - [ ] Hook (s 0–3): "On t'a menti sur la K-beauty. Et je vais te le prouver."
  - [ ] Body (s 3–25): 3 myths + 3 truths
  - [ ] CTA (s 25–30): "Liste d'attente en bio. Tu reçois l'enquête en avant-première."
- [ ] Record the video (phone is fine, vertical 9:16, natural light)
- [ ] Edit in CapCut — add auto-captions in French
- [ ] **Verify all French accents are correct** (é è ê à ç ô û î — no shortcuts)
- [ ] Export 9:16 (for IG Reel + TikTok + YT Short) and 1:1 (for IG feed safety)

## Friday — Link-in-bio + first content drop (1.5 h)

- [ ] Build `links.sonagibeauty.com` — single static page, 5 links:
  1. Rejoindre la liste d'attente
  2. Quiz : Quelle routine K-beauty pour toi ?
  3. Marques curées (À venir)
  4. Le Magazine (blog)
  5. Contact / DM
- [ ] Deploy via Netlify, point CNAME `links.sonagibeauty.com`
- [ ] Update IG bio + TikTok bio + Pinterest bio + YouTube About → all point to `links.sonagibeauty.com`
- [ ] In Metricool, schedule:
  - [ ] **IG Reel:** Tuesday next week, 12h30 Paris
  - [ ] **TikTok:** Wednesday next week, 13h00 Paris
  - [ ] Both with proper UTM links (copy from UTM library sheet)

## Saturday — Engagement OS bootstrap (45 min)

- [ ] Create Notion DB: "Watch list — French K-beauty creators"
  - Columns: handle, platform, follower count, content style fit (1–5), last engaged date
- [ ] Add 30 French K-beauty / skincare creators (search TikTok + IG: "k-beauty france", "soin coréen", "routine glass skin", "@anua_official", "@beautyofjoseon")
- [ ] Follow all 30
- [ ] Comment thoughtfully on 5 of their recent posts (no self-promotion, just genuine engagement)

## Sunday — Weekly review + Week 2 planning (1 h)

- [ ] Run the weekly review template from `PLAYBOOK-ANALYTICS.md` § 3 (will be near-empty data — that's fine, the habit is what matters)
- [ ] Open Notion content calendar; populate Weeks 2, 3, 4 with placeholder cards:
  - [ ] 12 IG Reel slots
  - [ ] 12 TikTok slots
  - [ ] 8 Pinterest pin slots
  - [ ] 4 YouTube Short slots
- [ ] Block recurring calendar event: **every Sunday 19h00–19h30 = weekly review** (non-negotiable)

---

## End-of-week success criteria (check on Sunday evening)

- [ ] GA4 conversion events firing (verified in DebugView)
- [ ] UTM library sheet exists with template + 2 sample rows
- [ ] Brevo waitlist form live, tested with real address, source field captured
- [ ] Metricool + Buffer connected to all 4 platforms
- [ ] `links.sonagibeauty.com` live, 5 links, branded
- [ ] First IG Reel + TikTok scheduled for next week with UTMs
- [ ] Watch-list Notion DB populated with 30 creators, 5 thoughtfully engaged
- [ ] Notion content calendar populated through Week 4
- [ ] Sunday weekly review habit installed in calendar

If 8/9 of these are checked, **Week 1 was a success.** Don't wait until everything is perfect — ship the system, then iterate from real data starting Week 2.

---

## What you are NOT doing this week (by design)

- Not chasing followers. Not running paid. Not pitching influencers. Not shooting 10 Reels.
- All of those happen Weeks 2+. Week 1 is plumbing only.
