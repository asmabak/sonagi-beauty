/* Fetch metadata for individual Instagram + TikTok URLs.
   Asma pastes URLs into engagement-urls.txt; script enriches each.
   Free, no auth, ToS-friendly (we only read public metadata). */

const https = require("https");

function getText(url, timeoutMs = 15000, headers = {}) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: Object.assign({
        "User-Agent": "Mozilla/5.0 (compatible; SonagiBriefing/1.0)",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.5",
      }, headers),
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return getText(res.headers.location, timeoutMs, headers).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error("HTTP " + res.statusCode + " on " + url));
      let data = "";
      res.setEncoding("utf8");
      res.on("data", (c) => (data += c));
      res.on("end", () => resolve(data));
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error("Timeout")));
    req.on("error", reject);
  });
}

function decodeEntities(s) {
  return (s || "")
    .replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&").replace(/&nbsp;/g, " ");
}

function pickMeta(html, prop) {
  const re = new RegExp('<meta[^>]+(?:name|property)=["\']' + prop.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + '["\'][^>]*content=["\']([^"\']+)["\']', "i");
  const m = html.match(re);
  return m ? decodeEntities(m[1]) : null;
}

/**
 * TikTok — uses official oEmbed (no auth, free, stable).
 * Returns: { id, link, title, author, image, pubDate, platform: 'tiktok' }
 */
async function fetchTiktokByUrl(url) {
  const oembedUrl = "https://www.tiktok.com/oembed?url=" + encodeURIComponent(url);
  try {
    const text = await getText(oembedUrl);
    const json = JSON.parse(text);
    return {
      id: "tiktok_" + (url.match(/\/video\/(\d+)/) || [, "unknown"])[1],
      platform: "tiktok",
      link: url,
      title: json.title || "",
      author: (json.author_name || json.author_unique_id || "").replace(/^@?/, "@"),
      handle: (json.author_unique_id || "").replace(/^@?/, ""),
      image: json.thumbnail_url || null,
      pubDate: new Date(),  // TikTok oEmbed doesn't return date — assume "today"
      description: json.title || "",
    };
  } catch (e) {
    return { id: "err_" + Date.now(), link: url, error: e.message, platform: "tiktok" };
  }
}

/**
 * Instagram — scrape OG meta tags from the post URL.
 * Works on /p/, /reel/, /tv/ URLs. Public meta is served even unauthed.
 */
async function fetchInstagramByUrl(url) {
  const cleanUrl = url.split("?")[0].replace(/\/$/, "") + "/";
  try {
    const html = await getText(cleanUrl);
    const ogTitle = pickMeta(html, "og:title");
    const ogDesc = pickMeta(html, "og:description");
    const ogImg = pickMeta(html, "og:image");
    // Author handle — try multiple patterns Instagram uses
    let handle = null;
    const handleMatch = html.match(/"username"\s*:\s*"([^"]+)"/) || (cleanUrl.match(/instagram\.com\/([^\/]+)\//));
    if (handleMatch) handle = handleMatch[1].replace(/^@/, "").replace(/^p$|^reel$|^tv$/, "");
    const id = (cleanUrl.match(/\/(?:p|reel|tv)\/([^\/]+)/) || [])[1] || ("ig_" + Date.now());
    return {
      id: "ig_" + id,
      platform: "ig",
      link: cleanUrl,
      title: ogTitle || ogDesc || "",
      description: ogDesc || ogTitle || "",
      author: handle ? "@" + handle : (ogTitle || "").split(" on Instagram")[0],
      handle: handle || "",
      image: ogImg || null,
      pubDate: new Date(),  // unreliable from OG; assume "today"
    };
  } catch (e) {
    return { id: "err_" + Date.now(), link: url, error: e.message, platform: "ig" };
  }
}

/** Auto-detect platform from URL and route. */
async function fetchByUrl(url) {
  url = url.trim();
  if (!url || url.startsWith("#") || url.startsWith("//")) return null;
  if (/(?:tiktok\.com)/i.test(url)) return fetchTiktokByUrl(url);
  if (/(?:instagram\.com)/i.test(url)) return fetchInstagramByUrl(url);
  return { id: "unknown_" + Date.now(), link: url, error: "Unknown platform", platform: "other" };
}

module.exports = { fetchByUrl, fetchTiktokByUrl, fetchInstagramByUrl };
