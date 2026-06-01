/* Post the briefing as a GitHub Issue on the repo.
   GitHub auto-emails the repo owner about new issues (no SMTP needed).
   Uses the built-in GITHUB_TOKEN that every GitHub Action receives free. */

const https = require("https");

function postIssue({ owner, repo, token, title, body, labels = [] }) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({ title, body, labels });
    const req = https.request({
      hostname: "api.github.com",
      path: "/repos/" + owner + "/" + repo + "/issues",
      method: "POST",
      headers: {
        "Authorization": "token " + token,
        "User-Agent": "SonagiBriefing/1.0",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(payload),
      },
    }, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) resolve(json);
          else reject(new Error("GitHub API " + res.statusCode + ": " + (json.message || data.slice(0, 300))));
        } catch (e) { reject(e); }
      });
    });
    req.on("error", reject);
    req.setTimeout(20000, () => req.destroy(new Error("GitHub API timeout")));
    req.write(payload);
    req.end();
  });
}

module.exports = { postIssue };
