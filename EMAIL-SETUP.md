# Email Setup — Sonagi Beauty

End-to-end transactional email wiring for sonagibeauty.com via **Resend**. Free tier covers the entire pre-launch (3,000 emails/month, 100/day, **no credit card required**). When you outgrow it, paid plans start at $20/mo — but you'll likely never need them before product/market fit.

---

## What's already wired in code

| Piece | Location | Status |
|---|---|---|
| Send-protocol function | `netlify/functions/send-protocol.js` | Live, soft-fails when `RESEND_API_KEY` is missing |
| Email template (HTML + text) | `files/email/protocol-template.js` | Pure renderer, dark-mode + Outlook safe |
| Resend SDK dependency | `package.json` (`resend ^3.0.0`) | Auto-installed by Netlify on next deploy |
| Quiz advisor (produces the diagnostic) | `netlify/functions/quiz-advisor.js` | Already live |

The flow at a glance:

```
User finishes quiz
  → POST /.netlify/functions/quiz-advisor   (returns diagnostic JSON)
    → POST /.netlify/functions/send-protocol  (renders + emails the user)
```

---

## Step 1 — Create your Resend account (free, no card)

1. Go to **https://resend.com** → click **Sign up**.
2. Use `contact@sonagibeauty.com` so account ownership lives in the brand inbox.
3. Confirm the email Resend sends you.
4. You land in the dashboard. Free tier is active by default — no payment info requested.

> *Reminder: I (Claude) won't sign up or enter any payment info on your behalf — that's always your call.*

---

## Step 2 — Verify the sending domain `sonagibeauty.com`

Without domain verification you can ONLY send from `onboarding@resend.dev`, which kills deliverability and brand. Do this step before anything else.

1. Resend Dashboard → **Domains → Add Domain**.
2. Enter `sonagibeauty.com` → choose region **EU (Frankfurt)** for GDPR + speed for French users.
3. Resend shows you 4 DNS records. Add them at your DNS host (OVH, Gandi, Cloudflare, Netlify DNS — wherever your nameservers point).

### The exact DNS records you need to add

Resend will show you the EXACT values for your account — do not invent them. Below is the **shape** so you know what to expect (and where to put each one in your DNS host's UI).

| Type | Name / Host | Value | Notes |
|---|---|---|---|
| **MX** | `send.sonagibeauty.com` | `feedback-smtp.eu-west-1.amazonses.com` (priority 10) | Bounce/feedback handling. Region depends on the one you picked in Resend. |
| **TXT** | `send.sonagibeauty.com` | `v=spf1 include:amazonses.com ~all` | SPF — authorizes Resend to send for your domain. |
| **TXT** | `resend._domainkey.sonagibeauty.com` | `p=MIGfMA0G...` (long key Resend gives you) | DKIM — cryptographic signature. Copy the WHOLE value, including the `p=` prefix. |
| **TXT** | `_dmarc.sonagibeauty.com` | `v=DMARC1; p=none;` | DMARC — start in `p=none` to monitor; tighten to `p=quarantine` after 30 days of clean sends. |

**OVH UI:** Domains → `sonagibeauty.com` → **DNS Zone** → Add an entry → pick MX or TXT → fill in.
**Gandi UI:** `sonagibeauty.com` → **DNS Records** → Add → same fields.
**Netlify DNS UI:** Domains → `sonagibeauty.com` → **DNS settings** → Add new record.

### Common DNS gotchas

- The `Name / Host` column is RELATIVE to your domain. If your DNS host requires the FQDN (e.g. `send.sonagibeauty.com.` with a trailing dot), use that. If it auto-appends the domain, just enter `send`.
- DKIM TXT values are LONG (~250+ chars). Some registrars split them automatically — that's fine. Do not manually break them up.
- Propagation can take **5 minutes to 24 hours**. Check status in Resend Dashboard → Domains → click your domain. All 4 rows must read **Verified**.

> Tip: While you're waiting on DNS, you can already finish the rest of this guide and test in dev by sending to `delivered@resend.dev` (Resend's test inbox).

---

## Step 3 — Get your Resend API key

1. Resend Dashboard → **API Keys → Create API Key**.
2. Name it `sonagi-netlify-prod`.
3. Permission: **Full access** (or **Sending access** only — minimum-privilege; both work).
4. Domain: leave **All domains** for now.
5. Copy the key — it starts with `re_...` and is shown ONLY ONCE. If you lose it, just create another.

---

## Step 4 — Add Netlify environment variables

Netlify Dashboard → **Site → Site configuration → Environment variables → Add a variable**:

| Key | Value | Notes |
|---|---|---|
| `RESEND_API_KEY` | `re_...` (from step 3) | Required. The function returns `{ skipped: true }` if absent — no crash. |
| `FROM_EMAIL` | `Sonagi <protocole@sonagibeauty.com>` | Optional — this is the default. Use a sender prefix that matches the email purpose. |
| `REPLY_TO_EMAIL` | `contact@sonagibeauty.com` | Optional — this is the default. Replies route to the brand inbox. |

After saving, **trigger a redeploy** (Deploys → Trigger deploy → Deploy site). Resend SDK gets installed by `npm install` on that build.

---

## Step 5 — Test the end-to-end flow

### Option A — Real send to your own inbox

```bash
curl -X POST https://sonagibeauty.com/.netlify/functions/send-protocol \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Asma",
    "email": "asma.bakhtar@gmail.com",
    "diagnostic": {
      "headline": "Ta peau réclame une barrière apaisée",
      "diagnostic": "Sensitive skin with dehydration and visible pores — your skin barrier needs immediate calming support.",
      "minimum_routine": {
        "label": "Ton 3-étapes non-négociable",
        "description": "Trois gestes qui vont remettre ta peau d aplomb en 14 jours.",
        "steps": [
          { "order": 1, "step": "Nettoyage doux", "product": "Anua Heartleaf Quercetinol Pore Deep Cleansing Foam", "brand": "Anua", "why": "Mousse au pH 5.5 qui nettoie sans agresser ta barrière déjà fragilisée.", "how": "Fais mousser 30 secondes, masse en cercles, rince à l eau tiède.", "benefit": "Plus de tiraillement après nettoyage en 7 jours.", "price": "€18", "pregnancy_safe": true },
          { "order": 2, "step": "Toner apaisant", "product": "Anua Heartleaf 77% Soothing Toner", "brand": "Anua", "why": "77% d extrait de centella — calme les rougeurs et reconstruit la barrière.", "how": "Tapote sur peau encore humide, ne frotte pas.", "benefit": "Rougeurs visiblement atténuées en 14 jours.", "price": "€22", "pregnancy_safe": true },
          { "order": 3, "step": "Hydratation finale", "product": "Beauty of Joseon Dynasty Cream", "brand": "Beauty of Joseon", "why": "Crème au ginseng qui scelle l hydratation sans alourdir.", "how": "Une noisette, presse en partant du centre du visage.", "benefit": "Peau souple et confortable au réveil.", "price": "€20", "pregnancy_safe": true }
        ]
      },
      "evening_swap": { "label": "Le swap du soir", "product": "Beauty of Joseon Glow Serum Propolis + Niacinamide", "brand": "Beauty of Joseon", "why": "Le soir, ta peau se régénère — la propolis et la niacinamide accélèrent la réparation.", "how": "3 gouttes après le toner, avant la crème.", "benefit": "Teint plus uniforme en 4 semaines.", "price": "€17", "pregnancy_safe": true },
      "weekly_ritual": { "product": "COSRX Centella Blemish Cream", "brand": "COSRX", "frequency": "1 à 2 fois par semaine", "why": "Mini-cure ciblée pour les zones réactives ou les imperfections.", "benefit": "Imperfections séchées en 48h.", "pregnancy_safe": true },
      "boosters": {
        "label": "Boosters quand tu seras prête",
        "description": "À ajouter UN par UN, pas tous en même temps, après 3 à 4 semaines.",
        "steps": [
          { "step": "Sérum vitamine C matin", "product": "Beauty of Joseon Glow Serum", "brand": "Beauty of Joseon", "why": "Antioxydant qui booste l effet du SPF.", "benefit": "Teint plus lumineux en 4 semaines.", "price": "€17", "pregnancy_safe": true },
          { "step": "Exfoliant doux PHA soir", "product": "COSRX PHA Moisture Renewal Power Cream", "brand": "COSRX", "why": "Exfolie sans irriter — parfait pour peau sensible.", "benefit": "Grain de peau affiné en 3 semaines.", "price": "€24", "pregnancy_safe": true }
        ]
      },
      "hero_ingredient": "Centella Asiatica",
      "hero_ingredient_why": "Le secret coréen pour les peaux réactives. La centella active les fibroblastes qui reconstruisent ta barrière — c est elle qui calme les rougeurs en 10 à 14 jours.",
      "first_week_tip": "Cette semaine, ne change rien d autre. Pas de nouveau soin, pas d acide, pas de gommage. Laisse ta peau s habituer à ces 3 gestes — c est elle qui te dira quand passer à l étape suivante.",
      "total_minimum_cost": "€60",
      "total_full_cost": "€118"
    },
    "answers": {
      "name": "Asma",
      "skin_type": "sensible-deshydratee",
      "goal": ["apaiser", "hydrater"],
      "age": "30-39",
      "lifestyle": ["pollution-urbaine", "ecran-9h-plus"],
      "budget": "50-90",
      "pregnant": "non"
    },
    "locale": "fr"
  }'
```

Expected response:

```json
{ "ok": true, "id": "abc123-..." }
```

Then check your inbox — the email should arrive within 30 seconds.

### Option B — Local dev with `netlify dev`

```bash
# In project root
netlify dev
# In another terminal, hit the local function:
curl -X POST http://localhost:8888/.netlify/functions/send-protocol -H "Content-Type: application/json" -d '{...}'
```

### Option C — Test that the function is wired without consuming a send

Set `RESEND_API_KEY` to empty (or unset it) and POST a valid payload. You should get:

```json
{ "ok": true, "skipped": true, "reason": "RESEND_API_KEY not configured" }
```

This proves the function, JSON validation, and template renderer all work — without burning through your free quota.

---

## Step 6 — Deliverability checklist (do this BEFORE the launch)

Resend handles a lot for you, but these still matter:

- [ ] **All 4 DNS records show "Verified"** in Resend Dashboard → Domains.
- [ ] **DMARC is set to `p=none`** for the first 30 days, so you can monitor before enforcing.
- [ ] **Send a test to Gmail, Outlook.com, Yahoo, iCloud, and Free.fr** — paste the message into https://www.mail-tester.com first to get a deliverability score (aim for 9/10+).
- [ ] **Warm up gradually** — don't blast 3,000 emails day one. Start with 10–20/day for the first week, then ramp.
- [ ] **Monitor bounces** in Resend Dashboard → Logs. A bounce rate over 5% = your list is dirty (typos, fake emails). Add a frontend `email` regex check on the quiz form before the final submit.
- [ ] **Check the spam folder** for the first few sends. If you land in spam:
    - Verify SPF + DKIM + DMARC are green
    - Make sure FROM_EMAIL matches the verified domain
    - Avoid spammy words in the subject (no `100% gratuit`, `gagnez`, all caps)
- [ ] **Add a List-Unsubscribe header** — Resend does this automatically when you call `resend.emails.send`. The footer link in the template is a placeholder; if you wire a real unsubscribe page, replace `{{unsubscribe_url}}` in `protocol-template.js` with the real URL.
- [ ] **Suppression list** — Resend tracks bounces/complaints automatically. Don't try to email people who've unsubscribed — Resend will reject the send anyway.

---

## Step 7 — What to build next (pointers)

The protocol email is the FIRST touchpoint after the quiz. The full lifecycle includes:

| Sequence | Trigger | Purpose | Skill to invoke |
|---|---|---|---|
| **Welcome / 15% discount** | 24h after quiz, IF user hasn't bought | Get the first sale | `email-sequence` |
| **Routine check-in** | Day 14 after quiz | "Tu en es où ?" — re-engage, ask for review | `email-sequence` |
| **Abandoned cart** | 1h, 24h, 72h after cart add without checkout | Recover sales | `email-sequence` |
| **Post-purchase ritual guide** | 1h after Stripe webhook fires | Reinforce the routine + reduce returns | `email-sequence` |
| **Win-back** | 60 days of inactivity | Bring back lapsed users | `churn-prevention` + `email-sequence` |

To plan any of these, prompt: *"Use the email-sequence skill to plan the welcome 15% discount sequence for Sonagi Beauty"*. The skill will draft subjects, timing, and copy in the brand voice.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Function returns `{ skipped: true, reason: "RESEND_API_KEY not configured" }` | Env var not set on Netlify | Add `RESEND_API_KEY` and redeploy |
| Function returns `{ ok: false, error: "Resend SDK not installed" }` | Netlify build did not run `npm install` after the dependency was added | Trigger a redeploy with **Clear cache and deploy site** |
| Function returns `{ ok: false, error: "Resend rejected the message" }` | Domain not verified, or `FROM_EMAIL` doesn't match a verified domain | Check Resend Dashboard → Domains, all rows must be Verified |
| Email lands in spam | SPF/DKIM/DMARC missing or misaligned | Run a test through mail-tester.com, fix what it flags |
| Resend says "domain not verified" but DNS records are added | Propagation delay | Wait 1–24h, click "Verify" again. Use https://mxtoolbox.com to confirm DNS values |
| French accents look broken in the email | Encoding mismatch (very rare with Resend) | Check that the function's response Content-Type is `application/json; charset=utf-8` (it already is) |
| The reply-to is wrong | `REPLY_TO_EMAIL` env var set to something else | Update or unset to use the default `contact@sonagibeauty.com` |
| Multiple emails sent for the same quiz submission | Frontend retried the POST | Add a debounce / disable-button-on-submit in the quiz UI |

---

## Quick reference

- **Resend Dashboard** → https://resend.com
- **Resend docs** → https://resend.com/docs
- **DNS check (SPF/DKIM/DMARC)** → https://mxtoolbox.com
- **Deliverability test** → https://www.mail-tester.com
- **Netlify env vars** → Site → Site configuration → Environment variables
- **Free tier limits** → 3,000 emails/month, 100/day, 1 verified domain, 10 API keys
