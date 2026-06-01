/* Fetch YouTube channel RSS feeds, Google still serves these freely
   from anywhere (no auth, no rate limit at our volume).
   Format: https://www.youtube.com/feeds/videos.xml?channel_id=UCxxx
   To find a channel ID: visit any video, click the channel name, the URL is
   /channel/UCxxx, the UCxxx part is the channel_id. */

const https = require("https");
const { parseFeed } = require("./fetch-rss");

function getText(url, timeoutMs = 15000) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { "User-Agent": "Mozilla/5.0 SonagiBriefing" } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return getText(res.headers.location, timeoutMs).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error("HTTP " + res.statusCode));
      let data = "";
      res.setEncoding("utf8");
      res.on("data", (c) => (data += c));
      res.on("end", () => resolve(data));
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error("Timeout")));
    req.on("error", reject);
  });
}

async function fetchYoutubeChannel(channel_id, { limit = 5, timeoutMs = 15000 } = {}) {
  try {
    const xml = await getText("https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id, timeoutMs);
    const items = parseFeed(xml).slice(0, limit);
    return items.map((it) => ({
      ...it,
      id: "yt_" + (it.id || it.link),
      author: it.author || "",
    }));
  } catch (e) {
    console.warn("[youtube] " + channel_id + " ERROR " + e.message);
    return [];
  }
}

/** Generic RSS feed fetcher (for Substack, WordPress, blog feeds). */
async function fetchRssUrl(url, { limit = 5, timeoutMs = 15000 } = {}) {
  try {
    const xml = await getText(url, timeoutMs);
    return parseFeed(xml).slice(0, limit);
  } catch (e) {
    console.warn("[rss] " + url + " ERROR " + e.message);
    return [];
  }
}

module.exports = { fetchYoutubeChannel, fetchRssUrl };
