/* Render the daily briefing as GitHub-flavored markdown for posting as an Issue.
   GitHub will email this rendered content to repo watchers automatically. */

function escapeMd(s) {
  return (s || "").replace(/\|/g, "\\|").replace(/\n+/g, " ");
}

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

function renderPostBlock(post, comments) {
  const handle = post.handle || post.author || "?";
  const platformIcon = post.platform === "youtube" ? "🎥"
    : post.platform === "tiktok" ? "🎵"
    : post.platform === "ig" ? "📷"
    : post.platform === "blog" ? "📝"
    : "📌";
  const sourceTag = post.via_subreddit ? "r/" + post.via_subreddit
    : post.via_hashtag ? "#" + post.via_hashtag
    : post.via_channel ? post.via_channel
    : post.source;

  const lines = [];
  lines.push("### " + platformIcon + " " + escapeMd(post.title || "(no title)"));
  lines.push("");
  lines.push("**" + handle + "** · " + relativeTime(post.pubDate) + " · `" + escapeMd(sourceTag) + "` · [Ouvrir →](" + post.link + ")");
  lines.push("");
  if (post.description && post.description.trim() && post.description.trim() !== post.title) {
    lines.push("> " + escapeMd(post.description.slice(0, 300)) + (post.description.length > 300 ? "…" : ""));
    lines.push("");
  }
  if (comments && comments.length) {
    lines.push("**Suggestions de commentaire** (clique pour copier sur ton téléphone) :");
    lines.push("");
    comments.forEach((c, i) => {
      const letter = String.fromCharCode(65 + i);
      lines.push("**" + letter + ".** " + c);
      lines.push("");
    });
  } else {
    lines.push("_Pas de suggestion (clé Gemini manquante ou erreur de génération)._");
    lines.push("");
  }
  lines.push("---");
  lines.push("");
  return lines.join("\n");
}

function renderBriefingMarkdown({ posts, comments, stats, config }) {
  const date = new Date();
  const dateStr = date.toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  const lines = [];

  lines.push("# 🌸 Sonagi Daily Engagement Briefing");
  lines.push("");
  lines.push("**" + dateStr + "** · " + stats.total_posts + " posts · " + stats.total_comments + " commentaires suggérés · objectif " + (config.briefing.target_actions || 25) + " comments / " + (config.briefing.target_minutes || 15) + " min");
  lines.push("");
  lines.push("---");
  lines.push("");

  if (posts.length === 0) {
    lines.push("⚠️ **Aucun post récupéré aujourd'hui.** YouTube/blog feeds ont peut-être eu un creux. Vérifie demain ou ajoute des URLs dans `engagement-urls.txt`.");
    return lines.join("\n");
  }

  // Group by source
  const groups = {};
  posts.forEach((p) => {
    const key = p.source || "other";
    (groups[key] = groups[key] || []).push(p);
  });
  const labels = {
    manual: "📌 Tes URLs prioritaires",
    youtube: "🎥 YouTube K-beauty creators",
    blog: "📝 Blogs K-beauty",
    rss: "📰 RSS divers",
  };
  const order = ["manual", "youtube", "blog", "rss"];
  order.forEach((key) => {
    if (!groups[key]) return;
    lines.push("## " + (labels[key] || key) + " (" + groups[key].length + ")");
    lines.push("");
    groups[key].forEach((p) => lines.push(renderPostBlock(p, comments.get(p.id))));
  });

  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("_Briefing généré automatiquement par GitHub Actions chaque jour à 07:30 Paris. Modifie `scripts/engagement-brief/config.js` pour changer les sources/voix/cadence._");

  return lines.join("\n");
}

module.exports = { renderBriefingMarkdown };
