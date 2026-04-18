/* Fetch Reddit RSS feeds — Reddit still serves clean RSS without auth.
   Subreddits like r/AsianBeauty are goldmines for K-beauty discussion. */

const { parseFeed } = require("./fetch-rss");
const https = require("https");

function getJson(url, timeoutMs) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { "User-Agent": "SonagiBriefing/1.0 (https://sonagibeauty.com)" } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return getJson(res.headers.location, timeoutMs).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error("HTTP " + res.statusCode + " on " + url));
      let data = "";
      res.setEncoding("utf8");
      res.on("data", (c) => (data += c));
      res.on("end", () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error("Timeout")));
    req.on("error", reject);
  });
}

/**
 * Fetch top posts from a subreddit in the last 24h via JSON API.
 * Returns normalized post objects.
 */
async function fetchSubreddit(name, { limit = 10, timeoutMs = 15000 } = {}) {
  const url = "https://www.reddit.com/r/" + encodeURIComponent(name) + "/top.json?t=day&limit=" + limit;
  try {
    const json = await getJson(url, timeoutMs);
    const children = (json && json.data && json.data.children) || [];
    return children
      .map((c) => c.data)
      .filter((p) => p && !p.over_18 && !p.stickied)
      .map((p) => ({
        id: "reddit_" + p.id,
        title: p.title,
        link: "https://www.reddit.com" + p.permalink,
        pubDate: new Date(p.created_utc * 1000),
        description: (p.selftext || "").slice(0, 1500),
        author: p.author,
        image: p.thumbnail && p.thumbnail.startsWith("http") ? p.thumbnail : null,
        score: p.score,
        comments_count: p.num_comments,
      }));
  } catch (e) {
    console.warn("[reddit] r/" + name + " ERROR " + e.message);
    return [];
  }
}

module.exports = { fetchSubreddit };
