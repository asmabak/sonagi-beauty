/* ══════════════════════════════════════════════════════
   SONAGI ENGAGEMENT BRIEFING — config v2 (zero-friction)
   ──────────────────────────────────────────────────────
   Output: GitHub Issue → auto-emails you (no SMTP setup).
   Sources: YouTube RSS + blog RSS + your manual URL queue.
            All free, all work from GitHub Actions IPs.
   Required secret: just GEMINI_API_KEY (1 minute setup).
   ══════════════════════════════════════════════════════ */

module.exports = {
  briefing: {
    title: "Sonagi Daily Engagement Briefing",
    target_minutes: 15,
    target_actions: 25,
    timezone: "Europe/Paris",
    locale: "fr-FR",
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

  // ── YouTube channels (FREE, works from any IP) ───────
  // Find the channel_id by visiting any of their videos and clicking the channel name.
  youtube: {
    enabled: true,
    channels: [
      { channel_id: "UCFpb7dQ-Wl5wCsHfxnTQpZA", name: "James Welsh",        priority: 1, note: "UK K-beauty male creator, weekly" },
      { channel_id: "UC0LMlVDdEUW8Imzaqi6vsAA", name: "Liah Yoo",           priority: 1, note: "Korean-American educator, KraveBeauty founder" },
      { channel_id: "UCKrtdyiQ7XSiHBO3-vsxo7w", name: "Edward Zo",          priority: 1, note: "English K-beauty male, Minjun voice template" },
      { channel_id: "UCvIxUJVwXp3Q5kDc9H1PdHA", name: "WishtrendTV",        priority: 2, note: "Wishtrend brand channel, K-beauty deep dives" },
      { channel_id: "UC7AJpFf6Lm2DjOXkM8ahDcg", name: "Hyram",              priority: 2, note: "Mass-market skincare, K-beauty heavy" },
      { channel_id: "UCsf0GnUcHi9hTqI_9ksyeXw", name: "DariaB Skincare",    priority: 3, note: "Cosmetic chemist + K-beauty reviews" },
      { channel_id: "UCwEsBLLukBHOBN1A-XR8X4w", name: "Caroline Receveur",  priority: 3, note: "Top FR beauty creator (occasional K-beauty)" },
      { channel_id: "UCC1tRfBRLrYIUqHcVqJjE9w", name: "Lucile Woodward",    priority: 3, note: "FR skincare science, dermatology angle" },
    ],
    limit_per_channel: 3,
  },

  // ── Blog / Substack RSS (FREE, works from any IP) ────
  blogs: {
    enabled: true,
    feeds: [
      { url: "https://theklog.co/feed/",            name: "The Klog (Soko Glam)", priority: 1 },
      { url: "https://www.glowrecipe.com/blogs/recipes.atom", name: "Glow Recipe Recipes", priority: 2 },
      { url: "https://www.allure.com/feed/category/skin/rss", name: "Allure Skin",         priority: 2 },
      { url: "https://miin-cosmetics.fr/blog/feed/",          name: "MiiN Cosmetics FR",   priority: 1 },
    ],
    limit_per_feed: 3,
  },

  // ── Manual URL queue — paste IG/TikTok/blog URLs here ────────────────────
  manual_urls: {
    enabled: true,
    file: "engagement-urls.txt",
  },

  // ── Limits ───────────────────────────────────────────
  limits: {
    max_posts_in_briefing: 50,
    max_post_age_hours:    96,
    request_delay_ms:      400,
    fetch_timeout_ms:      15000,
  },

  // ── GEMINI API (FREE — 1M tokens/day, no card) ───────
  gemini: {
    model:            "gemini-2.5-flash",
    max_tokens:       800,
    options_per_post: 4,
    temperature:      0.85,
    batch_size:       8,
  },

  // ── GitHub Issue delivery ────────────────────────────
  github: {
    owner: "asmabak",
    repo:  "sonagi-beauty",
    label: "engagement-brief",
  },
};
