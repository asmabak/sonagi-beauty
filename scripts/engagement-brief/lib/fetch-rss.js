/* Fetch RSS feeds (Atom or RSS 2.0) — pure Node, no deps. */

const https = require("https");

function getWithTimeout(url, timeoutMs) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { "User-Agent": "Mozilla/5.0 (compatible; SonagiBriefing/1.0)" } }, (res) => {
      // Follow one redirect
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return getWithTimeout(res.headers.location, timeoutMs).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode} on ${url}`));
      let data = "";
      res.setEncoding("utf8");
      res.on("data", (c) => (data += c));
      res.on("end", () => resolve(data));
    });
    req.setTimeout(timeoutMs, () => { req.destroy(new Error(`Timeout ${timeoutMs}ms on ${url}`)); });
    req.on("error", reject);
  });
}

function decodeEntities(s) {
  return (s || "")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/&nbsp;/g, " ");
}

function stripHtml(s) {
  return (s || "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<[^>]+>/g, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function extractFirstImg(html) {
  if (!html) return null;
  const m = html.match(/<img[^>]+src=["']([^"']+)["']/i);
  return m ? m[1] : null;
}

function pickBetween(s, start, end) {
  const i = s.indexOf(start);
  if (i < 0) return null;
  const j = s.indexOf(end, i + start.length);
  if (j < 0) return null;
  return s.slice(i + start.length, j);
}

/**
 * Parse RSS 2.0 / Atom feed. Returns array of items.
 * Each item: { id, title, link, pubDate (Date), description, image, author }
 */
function parseFeed(xml) {
  if (!xml) return [];
  const items = [];

  // RSS 2.0 — <item>...</item>
  const itemRe = /<item[\s\S]*?<\/item>/gi;
  // Atom — <entry>...</entry>
  const entryRe = /<entry[\s\S]*?<\/entry>/gi;

  const blocks = (xml.match(itemRe) || []).concat(xml.match(entryRe) || []);

  for (const block of blocks) {
    const title = decodeEntities(stripHtml(pickBetween(block, "<title>", "</title>") || pickBetween(block, "<title><![CDATA[", "]]></title>") || ""));
    const link = (pickBetween(block, "<link>", "</link>") || (block.match(/<link[^>]+href=["']([^"']+)["']/) || [])[1] || "").trim();
    const pubDateStr = pickBetween(block, "<pubDate>", "</pubDate>") || pickBetween(block, "<published>", "</published>") || pickBetween(block, "<updated>", "</updated>") || "";
    const descRaw = pickBetween(block, "<description>", "</description>") || pickBetween(block, "<content type=\"html\">", "</content>") || pickBetween(block, "<content>", "</content>") || pickBetween(block, "<summary>", "</summary>") || "";
    const descHtml = decodeEntities(descRaw.replace(/^<!\[CDATA\[/, "").replace(/\]\]>$/, ""));
    const image = extractFirstImg(descHtml) || (block.match(/<media:content[^>]+url=["']([^"']+)["']/) || [])[1] || (block.match(/<enclosure[^>]+url=["']([^"']+)["']/) || [])[1] || null;
    const author = decodeEntities(stripHtml(pickBetween(block, "<author>", "</author>") || pickBetween(block, "<dc:creator>", "</dc:creator>") || ""));
    const guid = pickBetween(block, "<guid", "</guid>") || pickBetween(block, "<id>", "</id>") || link;

    items.push({
      id: (guid || link).trim(),
      title: title.trim(),
      link: link.trim(),
      pubDate: pubDateStr ? new Date(pubDateStr) : null,
      description: stripHtml(descHtml).slice(0, 1200),
      image: image,
      author: author.trim(),
      raw_html: descHtml.slice(0, 4000),
    });
  }
  return items;
}

/**
 * Try a list of RSSHub instances until one succeeds.
 */
async function fetchRsshub(path, instances, timeoutMs) {
  let lastErr = null;
  for (const base of instances) {
    try {
      const xml = await getWithTimeout(base.replace(/\/$/, "") + path, timeoutMs);
      return parseFeed(xml);
    } catch (e) {
      lastErr = e;
      continue;
    }
  }
  throw lastErr || new Error("All RSSHub instances failed");
}

/**
 * Fetch posts for a single Instagram user.
 */
async function fetchIgUser(handle, instances, timeoutMs) {
  return fetchRsshub("/instagram/user/" + encodeURIComponent(handle), instances, timeoutMs);
}

/**
 * Fetch posts for an Instagram hashtag.
 */
async function fetchIgTag(tag, instances, timeoutMs) {
  return fetchRsshub("/instagram/tag/" + encodeURIComponent(tag), instances, timeoutMs);
}

/**
 * Fetch posts for a TikTok user.
 */
async function fetchTiktokUser(handle, instances, timeoutMs) {
  return fetchRsshub("/tiktok/user/" + encodeURIComponent(handle), instances, timeoutMs);
}

/**
 * Fetch posts for a TikTok hashtag.
 */
async function fetchTiktokTag(tag, instances, timeoutMs) {
  return fetchRsshub("/tiktok/tag/" + encodeURIComponent(tag), instances, timeoutMs);
}

function delay(ms) { return new Promise((r) => setTimeout(r, ms)); }

module.exports = {
  fetchIgUser,
  fetchIgTag,
  fetchTiktokUser,
  fetchTiktokTag,
  delay,
  parseFeed,
};
