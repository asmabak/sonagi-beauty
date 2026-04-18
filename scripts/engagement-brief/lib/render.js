/* Render the daily briefing as a self-contained HTML page. */

const fs = require("fs");
const path = require("path");

function escapeHtml(s) {
  return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function escapeAttr(s) { return escapeHtml(s); }

function escapeJs(s) { return (s || "").replace(/\\/g, "\\\\").replace(/'/g, "\\'").replace(/\n/g, "\\n"); }

function relativeTime(date) {
  if (!date) return "";
  const d = new Date(date);
  if (isNaN(d.getTime())) return "";
  const diffMs = Date.now() - d.getTime();
  const m = Math.round(diffMs / 60000);
  if (m < 60) return "il y a " + m + " min";
  const h = Math.round(m / 60);
  if (h < 24) return "il y a " + h + "h";
  const dd = Math.round(h / 24);
  return "il y a " + dd + "j";
}

function renderPostCard(post, comments, idx) {
  const handle = post.handle || post.author || "?";
  const platformIcon = post.platform === "tiktok"
    ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5.8 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1.84-.1z"/></svg>'
    : '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></svg>';
  const link = post.link || "#";
  const caption = (post.title || post.description || "").slice(0, 280);
  const tag = post.via_hashtag ? '<span class="badge">#' + escapeHtml(post.via_hashtag) + '</span>' : '<span class="badge badge-watch">watchlist</span>';
  const priorityBadge = post.priority === 1 ? '<span class="badge badge-pri">★</span>' : "";
  const commentsList = (comments || []).map((c, i) => {
    const letter = String.fromCharCode(65 + i);
    return '<div class="comment-row">' +
      '<button class="copy-btn" data-comment="' + escapeAttr(c) + '" onclick="copyComment(this)">' + letter + ' · copy</button>' +
      '<p class="comment-text">' + escapeHtml(c) + '</p>' +
      '</div>';
  }).join("");

  return '<article class="post-card" data-id="' + escapeAttr(post.id) + '">' +
    '<header class="post-head">' +
      '<div class="post-meta">' +
        platformIcon +
        '<span class="handle">@' + escapeHtml(handle) + '</span>' +
        '<span class="when">' + relativeTime(post.pubDate) + '</span>' +
        tag + priorityBadge +
      '</div>' +
      '<button class="open-btn" onclick="markDone(this);window.open(\'' + escapeJs(link) + '\', \'_blank\')">Ouvrir →</button>' +
    '</header>' +
    (caption ? '<p class="caption">' + escapeHtml(caption) + (caption.length >= 280 ? '…' : '') + '</p>' : '') +
    (commentsList ? '<div class="comments">' + commentsList + '</div>' : '<p class="no-comments">Pas de suggestion (ré-essaie demain).</p>') +
    '<button class="done-btn" onclick="markDone(this)">✓ Commenté</button>' +
  '</article>';
}

function renderBriefing({ date, posts, comments, stats, config }) {
  const dateStr = new Date(date).toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  const watchlistPosts = posts.filter((p) => p.source === "watchlist");
  const hashtagPosts = posts.filter((p) => p.source === "hashtag");

  const cards = (group) => group.map((p, i) => renderPostCard(p, comments.get(p.id), i)).join("\n");

  return `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>${escapeHtml(config.briefing.title)} — ${escapeHtml(dateStr)}</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root { --navy:#1a2744; --cream:#faf8f5; --peach:#f5c4aa; --peach-l:#fdeee5; --rose:#8a6565; --muted:#8a8a8a; --border:#ede8e2; --text:#2c2c2c; --green:#2d8659; }
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }
html { background: var(--cream); color: var(--text); -webkit-text-size-adjust:100%; }
body { font-family: 'DM Sans', system-ui, sans-serif; line-height: 1.55; padding-bottom: 80px; }
header.page-head { background: var(--navy); color: #fff; padding: 28px 20px 32px; }
.page-head h1 { font-family: 'Fraunces', Georgia, serif; font-weight: 300; font-size: 26px; letter-spacing: -.01em; margin-bottom: 4px; }
.page-head .date { font-size: 12px; opacity: .8; letter-spacing: 1px; text-transform: uppercase; }
.page-head .stats { display: flex; gap: 20px; margin-top: 18px; flex-wrap: wrap; font-size: 13px; }
.page-head .stat strong { color: var(--peach); font-family: 'Fraunces', serif; font-size: 18px; display: block; line-height: 1.1; }
main { max-width: 920px; margin: 0 auto; padding: 0 16px; }
section.group { margin: 32px 0; }
section.group > h2 { font-family: 'Fraunces', serif; font-weight: 300; font-size: 22px; color: var(--navy); margin-bottom: 4px; letter-spacing:-.01em; }
section.group > p.sub { font-size: 13px; color: var(--muted); margin-bottom: 18px; }
.post-card { background:#fff; border:1px solid var(--border); border-radius: 12px; padding: 18px 18px 14px; margin-bottom: 14px; transition: opacity .25s, transform .25s; }
.post-card.done { opacity: .35; transform: scale(.99); }
.post-head { display:flex; align-items:flex-start; justify-content:space-between; gap: 12px; margin-bottom: 10px; }
.post-meta { display:flex; align-items:center; gap: 10px; flex-wrap: wrap; font-size: 12px; color: var(--muted); }
.post-meta .handle { color: var(--navy); font-weight: 500; font-size: 14px; }
.post-meta .when { font-size: 11px; }
.badge { display:inline-block; padding: 2px 8px; border-radius: 999px; background: var(--peach-l); color: var(--rose); font-size: 10px; letter-spacing: .5px; }
.badge-watch { background: var(--navy); color: #fff; }
.badge-pri { background: var(--peach); color: var(--navy); font-weight: 600; }
.open-btn { background: none; border: 1px solid var(--navy); color: var(--navy); padding: 6px 14px; border-radius: 999px; font-size: 11px; letter-spacing: .5px; text-transform: uppercase; cursor: pointer; flex-shrink: 0; min-height: 32px; transition: all .2s; }
.open-btn:hover { background: var(--navy); color: #fff; }
.caption { font-size: 14px; line-height: 1.6; color: var(--text); margin: 6px 0 14px; padding: 10px 12px; background: var(--cream); border-radius: 8px; border-left: 3px solid var(--peach); }
.comments { display: grid; gap: 8px; margin-bottom: 12px; }
.comment-row { display: grid; grid-template-columns: 70px 1fr; gap: 10px; align-items: start; padding: 10px; border: 1px solid var(--border); border-radius: 8px; background: #fff; transition: background .15s; }
.comment-row:hover { background: var(--peach-l); }
.copy-btn { background: var(--navy); color: #fff; border: 0; padding: 6px 8px; font-size: 10px; font-family: ui-monospace, monospace; letter-spacing: .5px; cursor: pointer; border-radius: 6px; min-height: 32px; }
.copy-btn.copied { background: var(--green); }
.copy-btn.copied::before { content: "✓ "; }
.comment-text { font-size: 13.5px; line-height: 1.5; color: var(--text); }
.no-comments { font-size: 12px; color: var(--muted); font-style: italic; padding: 8px 0; }
.done-btn { display: inline-block; background: none; border: 1px solid var(--border); color: var(--muted); font-size: 11px; padding: 6px 12px; border-radius: 999px; cursor: pointer; min-height: 32px; transition: all .2s; }
.done-btn:hover { background: var(--green); border-color: var(--green); color: #fff; }
.done-btn.done { background: var(--green); border-color: var(--green); color: #fff; }
@media (min-width: 768px) {
  .page-head h1 { font-size: 36px; }
  main { padding: 0 24px; }
  .post-card { padding: 22px 24px 18px; }
  .comment-row { grid-template-columns: 80px 1fr; }
}
.empty-state { text-align: center; padding: 60px 20px; color: var(--muted); }
.empty-state h3 { font-family: 'Fraunces', serif; font-weight: 300; color: var(--navy); margin-bottom: 8px; }
footer.page-foot { text-align: center; padding: 30px 20px; font-size: 11px; color: var(--muted); border-top: 1px solid var(--border); margin-top: 40px; }
footer.page-foot a { color: var(--navy); }
</style>
</head>
<body>
<header class="page-head">
  <p class="date">${escapeHtml(dateStr)}</p>
  <h1>${escapeHtml(config.briefing.title)}</h1>
  <div class="stats">
    <div class="stat"><strong>${stats.total_posts}</strong>posts à commenter</div>
    <div class="stat"><strong>${stats.total_comments}</strong>commentaires suggérés</div>
    <div class="stat"><strong>${config.briefing.target_minutes} min</strong>objectif quotidien</div>
    <div class="stat"><strong>${config.briefing.target_actions}</strong>cible commentaires/jour</div>
  </div>
</header>
<main>
${watchlistPosts.length ? `
<section class="group">
  <h2>Watchlist · creators à entretenir</h2>
  <p class="sub">Tes ${config.watchlist.length} comptes prioritaires — comment-engage pour rester top-of-mind avant les DMs.</p>
  ${cards(watchlistPosts)}
</section>` : ""}
${hashtagPosts.length ? `
<section class="group">
  <h2>Découverte · hashtags chauds</h2>
  <p class="sub">Posts récents sur les hashtags K-beauty / beauté FR. Engage pour atteindre des nouvelles audiences.</p>
  ${cards(hashtagPosts)}
</section>` : ""}
${posts.length === 0 ? `
<div class="empty-state">
  <h3>Aucun post récupéré aujourd'hui</h3>
  <p>RSSHub a probablement été rate-limité. Réessaie dans quelques heures, ou vérifie les logs GitHub Actions.</p>
</div>` : ""}
</main>
<footer class="page-foot">
  Généré ${new Date().toLocaleString("fr-FR")} · <a href="https://sonagibeauty.com">sonagibeauty.com</a> · Briefing privé — ne pas partager
</footer>
<script>
function copyComment(btn) {
  const text = btn.getAttribute("data-comment");
  navigator.clipboard.writeText(text).then(() => {
    btn.classList.add("copied");
    const orig = btn.textContent;
    btn.textContent = "copié";
    setTimeout(() => { btn.classList.remove("copied"); btn.textContent = orig; }, 1500);
  });
}
function markDone(btn) {
  const card = btn.closest(".post-card");
  card.classList.toggle("done");
  const id = card.getAttribute("data-id");
  const done = JSON.parse(localStorage.getItem("sonagi_brief_done") || "{}");
  if (card.classList.contains("done")) done[id] = Date.now(); else delete done[id];
  localStorage.setItem("sonagi_brief_done", JSON.stringify(done));
}
// Restore done-state on load
document.addEventListener("DOMContentLoaded", () => {
  const done = JSON.parse(localStorage.getItem("sonagi_brief_done") || "{}");
  document.querySelectorAll(".post-card").forEach((c) => {
    if (done[c.getAttribute("data-id")]) c.classList.add("done");
  });
});
</script>
</body>
</html>`;
}

function writeBriefing(rendered, outDir) {
  fs.mkdirSync(outDir, { recursive: true });
  const today = new Date().toISOString().slice(0, 10);
  const dated = path.join(outDir, "briefing-" + today + ".html");
  const index = path.join(outDir, "index.html");
  fs.writeFileSync(dated, rendered, "utf8");
  fs.writeFileSync(index, rendered, "utf8");
  return { dated, index };
}

module.exports = { renderBriefing, writeBriefing };
