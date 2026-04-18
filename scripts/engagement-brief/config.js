/* ══════════════════════════════════════════════════════
   SONAGI ENGAGEMENT BRIEFING — config (free-only stack)
   ──────────────────────────────────────────────────────
   Edit, commit, push — next morning's email reflects it.
   Cost target: €0/month forever.
   ══════════════════════════════════════════════════════ */

module.exports = {
  briefing: {
    title: "Sonagi Daily Engagement Briefing",
    target_minutes: 15,
    target_actions: 25,
    timezone: "Europe/Paris",
    locale: "fr-FR",
    email_to: "asma.bakhtar@gmail.com",          // where the briefing lands
    email_from_name: "Sonagi Engagement Bot",
  },

  voice: {
    brand: "Sonagi Beauty",
    positioning: "Provocative Educator — French K-beauty curator, more edge than Soko Glam, more intimate than Glow Recipe",
    tu_or_vous: "tu",
    language: "fr",
    rules: [
      "Always 1-2 sentences max",
      "Reference SOMETHING SPECIFIC from the post (proves you actually read/watched it)",
      "Mix tones across the 4 options: question, expert add-on, intimate reaction, gentle counter-take",
      "Never use empty hype ('trop beau!', 'love this!', 'goals!')",
      "Never lead with a product mention",
      "Always proper French accents (é è ê à ç ô û î) when writing in French",
      "Use 'tu' never 'vous' in French",
      "Sonagi doesn't sell yet — never say 'achète chez nous' or push the brand",
      "OK to drop niche K-beauty knowledge naturally (e.g. ingredient mechanism, Korean technique)",
      "Match the post's language — if the post is English, comment in English. If French, French.",
    ],
  },

  // ── REDDIT subreddits — daily auto-discovery (FREE, RELIABLE) ────────────
  reddit: {
    enabled: true,
    subreddits: [
      { name: "AsianBeauty",          limit: 10, priority: 1, note: "K-beauty mecca, 2.2M subs" },
      { name: "SkincareAddiction",    limit: 8,  priority: 2, note: "General skincare, 2M subs — drop K-beauty wisdom" },
      { name: "Skincareaddictionuk",  limit: 5,  priority: 3, note: "UK editorial-leaning" },
      { name: "30PlusSkinCare",       limit: 5,  priority: 3, note: "Aging-skin focused" },
      { name: "FrenchSkincare",       limit: 5,  priority: 1, note: "Smaller but PERFECT FR audience" },
      { name: "Frenchcareaddiction",  limit: 5,  priority: 1, note: "FR skincare crowd" },
    ],
  },

  // ── MANUAL URL QUEUE — paste IG/TikTok URLs into engagement-urls.txt ─────
  manual_urls: {
    enabled: true,
    file: "engagement-urls.txt",
    note: "Paste any IG/TikTok URL — script fetches caption + drafts comments.",
  },

  // ── LIMITS ───────────────────────────────────────────
  limits: {
    max_posts_in_briefing: 50,
    max_post_age_hours:    72,
    request_delay_ms:      400,
    fetch_timeout_ms:      15000,
  },

  // ── GEMINI API (FREE — 1M tokens/day, no card) ───────
  gemini: {
    model:            "gemini-2.5-flash",        // fast, free tier covers way more than we need
    max_tokens:       800,
    options_per_post: 4,
    temperature:      0.85,
    batch_size:       8,
    free_tier_note:   "Get key at https://aistudio.google.com/app/apikey — no credit card required",
  },
};
