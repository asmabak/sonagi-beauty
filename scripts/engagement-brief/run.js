#!/usr/bin/env node
/* ══════════════════════════════════════════════════════
   SONAGI ENGAGEMENT BRIEFING — daily runner (free stack)
   ──────────────────────────────────────────────────────
   Sources:  Reddit (auto) + manual URL queue (your paste)
   LLM:      Google Gemini 2.5 Flash (free tier)
   Output:   HTML file written to ./brief-{date}.html
             — emailed by the GitHub Action that calls this
   Cost:     €0/month
   ══════════════════════════════════════════════════════ */

const fs = require("fs");
const path = require("path");
const config = require("./config");
const { fetchSubreddit } = require("./lib/fetch-reddit");
const { fetchByUrl } = require("./lib/fetch-by-url");
const { generateForPosts } = require("./lib/generate-comments");
const { renderBriefing } = require("./lib/render");

const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "";
const OUT_DIR = process.env.OUT_DIR || __dirname;

function ageHours(date) {
  if (!date) return Infinity;
  return (Date.now() - new Date(date).getTime()) / 3600000;
}

function readManualUrls() {
  const filePath = path.join(__dirname, config.manual_urls.file);
  if (!fs.existsSync(filePath)) return [];
  return fs.readFileSync(filePath, "utf8")
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"));
}

async function fetchReddit() {
  if (!config.reddit.enabled) return [];
  const out = [];
  const seen = new Set();
  for (const sub of config.reddit.subreddits) {
    try {
      const items = await fetchSubreddit(sub.name, { limit: sub.limit, timeoutMs: config.limits.fetch_timeout_ms });
      const fresh = items
        .filter((it) => ageHours(it.pubDate) <= config.limits.max_post_age_hours)
        .filter((it) => !seen.has(it.id));
      for (const it of fresh) {
        seen.add(it.id);
        out.push(Object.assign({}, it, {
          source: "reddit",
          platform: "reddit",
          via_subreddit: sub.name,
          handle: "r/" + sub.name + " · u/" + it.author,
          priority: sub.priority,
        }));
      }
      console.log("[reddit] r/" + sub.name + " → " + fresh.length + " fresh");
    } catch (e) {
      console.warn("[reddit] r/" + sub.name + " ERROR " + e.message);
    }
  }
  return out;
}

async function fetchManual() {
  if (!config.manual_urls.enabled) return [];
  const urls = readManualUrls();
  if (!urls.length) {
    console.log("[manual] no URLs in queue");
    return [];
  }
  const out = [];
  for (const url of urls) {
    try {
      const post = await fetchByUrl(url);
      if (post && !post.error) {
        post.source = "manual";
        post.priority = 1;
        out.push(post);
        console.log("[manual] ✓ " + post.platform + " · " + (post.handle || post.author || "?"));
      } else {
        console.warn("[manual] ✗ " + url + " · " + (post && post.error));
      }
    } catch (e) {
      console.warn("[manual] ERROR on " + url + ": " + e.message);
    }
  }
  return out;
}

(async () => {
  console.log("=== Sonagi Engagement Briefing — " + new Date().toISOString() + " ===");

  const [redditPosts, manualPosts] = await Promise.all([
    fetchReddit(),
    fetchManual(),
  ]);

  console.log("Sources: Reddit=" + redditPosts.length + " · Manual=" + manualPosts.length);

  let posts = manualPosts.concat(redditPosts);

  posts.sort((a, b) => {
    const srcOrder = { manual: 0, reddit: 1, hashtag: 2 };
    if (srcOrder[a.source] !== srcOrder[b.source]) return (srcOrder[a.source] || 9) - (srcOrder[b.source] || 9);
    if ((a.priority || 9) !== (b.priority || 9)) return (a.priority || 9) - (b.priority || 9);
    return (b.pubDate ? +new Date(b.pubDate) : 0) - (a.pubDate ? +new Date(a.pubDate) : 0);
  });

  if (posts.length > config.limits.max_posts_in_briefing) posts = posts.slice(0, config.limits.max_posts_in_briefing);
  console.log("Total posts after sort+cap: " + posts.length);

  const comments = await generateForPosts(posts, {
    apiKey: GEMINI_API_KEY,
    model: config.gemini.model,
    max_tokens: config.gemini.max_tokens,
    temperature: config.gemini.temperature,
    voice: Object.assign({}, config.voice, { options_per_post: config.gemini.options_per_post }),
    batch_size: config.gemini.batch_size,
  });

  const stats = {
    total_posts: posts.length,
    total_comments: Array.from(comments.values()).reduce((s, arr) => s + arr.length, 0),
  };
  const html = renderBriefing({ date: new Date(), posts, comments, stats, config });

  const today = new Date().toISOString().slice(0, 10);
  const outFile = path.join(OUT_DIR, "brief-" + today + ".html");
  fs.writeFileSync(outFile, html, "utf8");
  console.log("Wrote: " + outFile);
  console.log("Stats: " + JSON.stringify(stats));

  // Echo subject line for the email step
  const subject = "Sonagi Briefing · " + new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" }) + " · " + stats.total_posts + " posts à commenter";
  console.log("EMAIL_SUBJECT=" + subject);
  // Save metadata for the workflow to read
  fs.writeFileSync(path.join(OUT_DIR, "brief-meta.json"), JSON.stringify({ subject, stats, file: outFile }), "utf8");
})().catch((e) => {
  console.error("FATAL: " + e.message);
  console.error(e.stack);
  process.exit(1);
});
