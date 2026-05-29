#!/usr/bin/env node
/* ══════════════════════════════════════════════════════
   SONAGI ENGAGEMENT BRIEFING — runner v2 (GitHub Issue out)
   ──────────────────────────────────────────────────────
   Sources:  YouTube RSS + blog RSS + manual URL queue
   LLM:      Google Gemini 2.5 Flash (free)
   Output:   GitHub Issue created on asmabak/sonagi-beauty
             — GitHub auto-emails the repo owner
   ══════════════════════════════════════════════════════ */

const fs = require("fs");
const path = require("path");
const config = require("./config");
const { fetchYoutubeChannel, fetchRssUrl } = require("./lib/fetch-youtube-rss");
const { fetchByUrl } = require("./lib/fetch-by-url");
const { generateForPosts } = require("./lib/generate-comments");
const { renderBriefingMarkdown } = require("./lib/render-markdown");
const { postIssue } = require("./lib/post-issue");

const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "";
const GITHUB_TOKEN   = process.env.GITHUB_TOKEN   || "";

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

async function fetchYoutube() {
  if (!config.youtube.enabled) return [];
  const out = [];
  for (const ch of config.youtube.channels) {
    const items = await fetchYoutubeChannel(ch.channel_id, { limit: config.youtube.limit_per_channel, timeoutMs: config.limits.fetch_timeout_ms });
    items.forEach((it) => {
      if (ageHours(it.pubDate) > config.limits.max_post_age_hours) return;
      out.push(Object.assign({}, it, {
        source: "youtube",
        platform: "youtube",
        via_channel: ch.name,
        handle: ch.name,
        priority: ch.priority,
      }));
    });
    console.log("[youtube] " + ch.name + " → " + items.length + " items");
  }
  return out;
}

async function fetchBlogs() {
  if (!config.blogs.enabled) return [];
  const out = [];
  for (const feed of config.blogs.feeds) {
    const items = await fetchRssUrl(feed.url, { limit: config.blogs.limit_per_feed, timeoutMs: config.limits.fetch_timeout_ms });
    items.forEach((it) => {
      if (ageHours(it.pubDate) > config.limits.max_post_age_hours) return;
      out.push(Object.assign({}, it, {
        source: "blog",
        platform: "blog",
        via_channel: feed.name,
        handle: feed.name,
        priority: feed.priority,
      }));
    });
    console.log("[blog] " + feed.name + " → " + items.length + " items");
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
      }
    } catch (e) {
      console.warn("[manual] ERROR on " + url + ": " + e.message);
    }
  }
  return out;
}

(async () => {
  const startTime = new Date();
  console.log("=== Sonagi Engagement Briefing v2 — " + startTime.toISOString() + " ===");

  let posts = [];
  let comments = new Map();
  let errorMsg = null;

  try {
    // 1. Fetch from all sources in parallel
    const [ytPosts, blogPosts, manualPosts] = await Promise.all([
      fetchYoutube(),
      fetchBlogs(),
      fetchManual(),
    ]);
    console.log("Sources: YouTube=" + ytPosts.length + " · Blogs=" + blogPosts.length + " · Manual=" + manualPosts.length);

    posts = manualPosts.concat(ytPosts).concat(blogPosts);

    // 2. Sort
    posts.sort((a, b) => {
      const srcOrder = { manual: 0, youtube: 1, blog: 2 };
      if (srcOrder[a.source] !== srcOrder[b.source]) return (srcOrder[a.source] ?? 9) - (srcOrder[b.source] ?? 9);
      if ((a.priority || 9) !== (b.priority || 9)) return (a.priority || 9) - (b.priority || 9);
      return (b.pubDate ? +new Date(b.pubDate) : 0) - (a.pubDate ? +new Date(a.pubDate) : 0);
    });

    if (posts.length > config.limits.max_posts_in_briefing) posts = posts.slice(0, config.limits.max_posts_in_briefing);

    // 3. Generate comments
    if (GEMINI_API_KEY) {
      comments = await generateForPosts(posts, {
        apiKey: GEMINI_API_KEY,
        model: config.gemini.model,
        max_tokens: config.gemini.max_tokens,
        temperature: config.gemini.temperature,
        voice: Object.assign({}, config.voice, { options_per_post: config.gemini.options_per_post }),
        batch_size: config.gemini.batch_size,
      });
    }
  } catch (e) {
    errorMsg = e.message;
    console.error("FETCH/GEN ERROR: " + e.message);
  }

  // 4. Build the markdown body
  const stats = {
    total_posts: posts.length,
    total_comments: Array.from(comments.values()).reduce((s, arr) => s + arr.length, 0),
  };
  let body = renderBriefingMarkdown({ posts, comments, stats, config });

  if (errorMsg) {
    body = "> ⚠️ Erreur partielle pendant la génération : `" + errorMsg + "`\n\n" + body;
  }
  if (!GEMINI_API_KEY) {
    body = "> ⚠️ **GEMINI_API_KEY n'est pas défini dans GitHub Secrets** — les posts sont fetchés mais sans suggestions de commentaire.\n>\n> Fix : https://github.com/asmabak/sonagi-beauty/settings/secrets/actions → New secret → name `GEMINI_API_KEY` → value depuis https://aistudio.google.com/app/apikey (gratuit, 2 min)\n\n" + body;
  }

  // 5. Post as GitHub Issue (or write to file if not in GitHub Actions)
  const today = new Date().toISOString().slice(0, 10);
  const subject = "🌸 Briefing du " + new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" }) + " · " + stats.total_posts + " posts · " + stats.total_comments + " commentaires";

  if (GITHUB_TOKEN) {
    try {
      const issue = await postIssue({
        owner: config.github.owner,
        repo:  config.github.repo,
        token: GITHUB_TOKEN,
        title: subject,
        body,
        labels: [config.github.label],
      });
      console.log("✅ Posted as Issue #" + issue.number + " · " + issue.html_url);
    } catch (e) {
      console.error("❌ Failed to post Issue: " + e.message);
      // Fallback: write to file
      fs.writeFileSync(path.join(__dirname, "brief-" + today + ".md"), body, "utf8");
      throw e;
    }
  } else {
    const outFile = path.join(__dirname, "brief-" + today + ".md");
    fs.writeFileSync(outFile, body, "utf8");
    console.log("Wrote: " + outFile + " (no GITHUB_TOKEN — local mode)");
  }

  console.log("Stats: " + JSON.stringify(stats));
})().catch((e) => {
  console.error("FATAL: " + e.message);
  console.error(e.stack);
  process.exit(1);
});
