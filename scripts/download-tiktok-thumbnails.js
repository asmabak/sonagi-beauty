// Downloads TikTok thumbnails locally for the homepage influencer grid.
// Run: node scripts/download-tiktok-thumbnails.js
// Re-run anytime a video is swapped on the homepage.

const https = require('https');
const fs = require('fs');
const path = require('path');

const VIDEOS = [
  { user: 'mikaylanogueira',         id: '7490607555937422635', file: 'tiktok-pdrn.jpg' },
  { user: 'bambidoesbeauty',         id: '7302121489170468128', file: 'tiktok-snail.jpg' },
  { user: 'bewareofpity',            id: '7393718267111607553', file: 'tiktok-anua.jpg' },
  { user: 'beautyofjoseon_official', id: '7556048499373133076', file: 'tiktok-boj.jpg' },
];

const OUT_DIR = path.join(__dirname, '..', 'files', 'images', 'social');
fs.mkdirSync(OUT_DIR, { recursive: true });

function getJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

function downloadBinary(url, outPath) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.tiktok.com/' } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadBinary(res.headers.location, outPath).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      const file = fs.createWriteStream(outPath);
      res.pipe(file);
      file.on('finish', () => file.close(() => resolve(outPath)));
      file.on('error', reject);
    }).on('error', reject);
  });
}

(async () => {
  for (const v of VIDEOS) {
    try {
      const oembedUrl = `https://www.tiktok.com/oembed?url=https://www.tiktok.com/@${v.user}/video/${v.id}`;
      const meta = await getJSON(oembedUrl);
      if (!meta.thumbnail_url) {
        console.error(`${v.file}: no thumbnail_url in oEmbed response`);
        continue;
      }
      const out = path.join(OUT_DIR, v.file);
      await downloadBinary(meta.thumbnail_url, out);
      const size = fs.statSync(out).size;
      console.log(`${v.file}: ${size} bytes — "${meta.title?.slice(0, 60) || ''}"`);
    } catch (e) {
      console.error(`${v.file}: ${e.message}`);
    }
  }
})();
