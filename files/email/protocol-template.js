/**
 * Sonagi — Protocol email template
 *
 * Pure renderer: takes the diagnostic JSON returned by `quiz-advisor.js`
 * (plus the user's name, email, answers and locale) and produces:
 *
 *   { subject, html, text }
 *
 * The HTML is table-based, inline-styled, dark-mode aware and designed to
 * look stunning in Gmail, Apple Mail, iOS Mail and Outlook (yes, including
 * Outlook 2019/365 on Windows). It depends on no external resources — the
 * hero is a colored block with the wordmark in serif text.
 *
 * Usage (CommonJS):
 *   const { renderProtocolEmail } = require('../../files/email/protocol-template');
 *   const { subject, html, text } = renderProtocolEmail(payload);
 *
 * Brand palette (locked):
 *   navy   #1a2744
 *   cream  #faf8f5
 *   peach  #f5c4aa
 *   ink    #2a2a2a
 *   muted  #6b6b6b
 *   line   #e6e1d8
 *   amber  #d4a373  (accent for evening swap / hero ingredient)
 */

"use strict";

/* ----------------------------------------------------------------- *
 * 1. Expert chemistry / dermatology depth — keyed by ingredient family.
 *    The router uses BOTH the product name and the AI's "why" copy to
 *    pick the most relevant entry. Falls back to a generic block.
 * ----------------------------------------------------------------- */

const EXPERT_DEPTH = {
  centella: {
    mechanism:
      "la centella asiatique (madécassoside + asiaticoside) active les fibroblastes qui reconstruisent ta barrière — c'est elle qui calme les rougeurs en 10 à 14 jours.",
    technique:
      "tapote, ne frotte pas — sur peau encore légèrement humide pour fixer l'hydratation.",
    when:
      "après le toner, avant la crème — règle des textures fines à épaisses.",
  },
  niacinamide: {
    mechanism:
      "la niacinamide (vitamine B3) régule la production de sébum, resserre visuellement les pores et atténue les marques pigmentaires en agissant sur le transfert de mélanine.",
    technique:
      "3 à 4 gouttes sur peau sèche, lisse en partant du centre du visage vers l'extérieur.",
    when:
      "matin et soir — compatible avec presque tout, sauf la vitamine C pure (espace d'au moins 30 minutes).",
  },
  snail: {
    mechanism:
      "la mucine d'escargot apporte allantoïne, glycoprotéines et acide hyaluronique naturel — réparation cellulaire + hydratation profonde sans alourdir.",
    technique:
      "1 à 2 pressions, tapote jusqu'à pénétration complète (environ 30 secondes).",
    when:
      "après le toner, avant les essences hydratantes — soir surtout, matin si tissu déshydraté.",
  },
  propolis: {
    mechanism:
      "la propolis (résine d'abeille) apporte plus de 300 composés antibactériens et antioxydants — elle apaise et booste la barrière en parallèle.",
    technique:
      "réchauffe 2 à 3 gouttes entre les paumes puis presse sur le visage — la chaleur active les actifs.",
    when:
      "après le toner — peut remplacer ton sérum hydratant si peau réactive.",
  },
  bha: {
    mechanism:
      "l'acide salicylique (BHA) est lipophile : il pénètre dans le pore et désengorge les comédons à la source — pas seulement en surface.",
    technique:
      "applique sur peau sèche avec un coton ou les doigts — n'utilise PAS près des yeux.",
    when:
      "soir uniquement, 2 à 3 fois par semaine au début — augmente progressivement. Toujours suivi d'une crème hydratante et d'un SPF strict le lendemain.",
  },
  pha: {
    mechanism:
      "le PHA (gluconolactone, lactobionique) exfolie en surface tout en HYDRATANT — molécules trop grosses pour irriter la barrière, contrairement aux AHA classiques.",
    technique:
      "tapote sur peau propre et sèche — pas de coton (gaspillage).",
    when:
      "soir, peut être quotidien dès le début — beaucoup plus doux que l'AHA.",
  },
  aha: {
    mechanism:
      "les AHA (acide glycolique, lactique, mandélique) exfolient les cellules mortes en surface et stimulent le renouvellement cellulaire.",
    technique:
      "applique sur peau sèche — évite le contour des yeux et les zones lésées.",
    when:
      "soir, 2 fois par semaine en démarrage — SPF 50 obligatoire le lendemain (peau plus photosensible 7 jours).",
  },
  retinol: {
    mechanism:
      "le rétinol se convertit en acide rétinoïque dans la peau — il accélère le renouvellement cellulaire et stimule la synthèse de collagène.",
    technique:
      "1 à 2 noisettes sur peau sèche (jamais humide — risque d'irritation), évite contour des yeux et commissures des lèvres.",
    when:
      "soir uniquement, commence 2 fois par semaine puis augmente. SPF 50 strict le lendemain. INCOMPATIBLE GROSSESSE.",
  },
  vitaminc: {
    mechanism:
      "la vitamine C (acide L-ascorbique ou dérivés stabilisés) est un antioxydant qui neutralise les radicaux libres du soleil et de la pollution + uniformise le teint.",
    technique:
      "3 à 4 gouttes sur peau sèche le matin, avant ton hydratant.",
    when:
      "matin de préférence — booste l'efficacité du SPF. Évite de la combiner avec les AHA/BHA dans la même routine.",
  },
  hyaluronic: {
    mechanism:
      "l'acide hyaluronique retient jusqu'à 1000 fois son poids en eau — capte l'humidité ambiante et la fixe dans les couches superficielles.",
    technique:
      "applique sur peau LÉGÈREMENT humide (sinon il tire l'eau de la peau au lieu de l'air).",
    when:
      "matin et soir, après le toner et avant la crème — règle absolue : crème par-dessus pour sceller.",
  },
  ceramides: {
    mechanism:
      "les céramides sont les lipides naturels du ciment intercellulaire — ils colmatent les fissures invisibles de la barrière cutanée.",
    technique:
      "applique en dernière étape de soin (avant SPF), masse en mouvements ascendants.",
    when:
      "matin et soir — particulièrement essentiel en hiver et après exfoliation.",
  },
  peptides: {
    mechanism:
      "les peptides sont des fragments de protéines qui signalent à la peau de produire plus de collagène et d'élastine — effet long terme.",
    technique:
      "2 à 3 gouttes sur peau propre, lisse uniformément.",
    when:
      "soir surtout (la peau se régénère la nuit) — compatible avec retinol en alternance.",
  },
  spf: {
    mechanism:
      "le SPF chimique (souvent K-beauty) absorbe les UV ; le SPF minéral (zinc, titane) les réfléchit. Les K-beauty filters chimiques sont les plus élégants au monde — texture invisible.",
    technique:
      "2 doigts entiers étalés sur le visage (la quantité MARKETING dans les pubs est 3x trop faible), réapplique toutes les 2h en exposition.",
    when:
      "matin systématiquement, même par temps couvert, même en intérieur près d'une fenêtre. Dernière étape avant maquillage.",
  },
  cleanser: {
    mechanism:
      "un nettoyant doux (pH 5,5) respecte le film hydrolipidique — la sensation de tiraillement après nettoyage est un signal d'agression, pas de propreté.",
    technique:
      "fais mousser dans les paumes, masse 30 secondes en mouvements circulaires, rince à l'eau tiède (jamais chaude).",
    when:
      "soir systématiquement, matin selon ton type de peau (peau sèche : eau seule le matin suffit souvent).",
  },
  moisturizer: {
    mechanism:
      "une crème hydratante combine humectants (attirent l'eau), émollients (lissent) et occlusifs (scellent) — c'est le verrou final de ta routine.",
    technique:
      "réchauffe une noisette entre les paumes, presse sur le visage en partant du centre vers l'extérieur.",
    when:
      "matin (avant SPF) et soir (dernière étape soin) — sans crème, tout ce qui est en dessous s'évapore.",
  },
  generic: {
    mechanism:
      "ce produit a été choisi pour sa formulation propre et son efficacité prouvée sur ton type de peau.",
    technique:
      "applique sur peau propre, en partant du centre du visage vers l'extérieur.",
    when:
      "respecte l'ordre : textures les plus fines en premier, les plus épaisses en dernier.",
  },
};

/**
 * Pick the most relevant chemistry depth based on product name + the AI's
 * "why" copy. Both are scanned, in priority order.
 */
function pickExpertDepth(product, why) {
  const haystack = ((product || "") + " " + (why || "")).toLowerCase();

  // Order matters: more specific actives first.
  const order = [
    ["centella", ["centella", "cica", "heartleaf", "madecassoside", "asiaticoside"]],
    ["snail", ["snail", "mucine", "escargot", "mucin"]],
    ["propolis", ["propolis", "honey", "miel"]],
    ["retinol", ["retinol", "rétinol", "retinal", "retinoid"]],
    ["vitaminc", ["vitamin c", "vitamine c", "ascorbic", "ascorbique"]],
    ["bha", ["bha", "salicyl", "betaine salicylate"]],
    ["pha", ["pha", "gluconolactone", "lactobionic", "lactobionique"]],
    ["aha", ["aha", "glycolic", "glycolique", "lactic", "lactique", "mandelic", "mandélique"]],
    ["niacinamide", ["niacinamide", "vitamine b3", "vitamin b3"]],
    ["hyaluronic", ["hyalur", "hydra"]],
    ["ceramides", ["ceramide", "céramide"]],
    ["peptides", ["peptide", "matrixyl", "argireline"]],
    ["spf", ["spf", "sunscreen", "uv", "écran solaire", "ecran solaire"]],
    ["cleanser", ["cleanser", "nettoyant", "foam", "mousse", "cleansing"]],
    ["moisturizer", ["moistur", "crème", "creme", "cream", "hydratant"]],
  ];

  for (const [key, needles] of order) {
    if (needles.some((n) => haystack.includes(n))) return EXPERT_DEPTH[key];
  }
  return EXPERT_DEPTH.generic;
}

/* ----------------------------------------------------------------- *
 * 2. HTML helpers — minimal escaping + safe optional fields.
 * ----------------------------------------------------------------- */

function esc(s) {
  if (s === null || s === undefined) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function get(obj, path, fallback = "") {
  try {
    const v = path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);
    return v == null ? fallback : v;
  } catch (e) {
    return fallback;
  }
}

/* ----------------------------------------------------------------- *
 * 3. Budget interpretation — turns the quiz answer into a friendly note.
 * ----------------------------------------------------------------- */

function budgetNote(budgetAnswer, totalMin, totalFull) {
  if (!budgetAnswer) return "";
  const a = String(budgetAnswer).toLowerCase();

  // The quiz uses ranges like "moins-50", "50-90", "90-150", "150-plus"
  let label = budgetAnswer;
  if (a.includes("moins") || a.includes("<50") || a.includes("50") && a.includes("moins")) label = "moins de €50";
  else if (a.includes("50") && a.includes("90")) label = "€50 à €90";
  else if (a.includes("90") && a.includes("150")) label = "€90 à €150";
  else if (a.includes("150")) label = "€150 et plus";

  return `Tu m'as dit que ton budget tournait autour de ${esc(label)}. La routine essentielle (${esc(totalMin)}) entre dedans — c'est ton point de départ. Le rituel complet (${esc(totalFull)}) est à viser quand tu seras à l'aise et que tu voudras pousser plus loin.`;
}

/* ----------------------------------------------------------------- *
 * 4. Section renderers — each returns a chunk of the email body.
 * ----------------------------------------------------------------- */

function renderStepCard(step, opts = {}) {
  const { stepNum, accent = "#1a2744" } = opts;
  const expert = pickExpertDepth(step.product, step.why);
  const how = step.how || "";
  const safe = step.pregnancy_safe;

  return `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 24px 0;">
    <tr>
      <td valign="top" width="56" style="padding:0 16px 0 0;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="40">
          <tr>
            <td align="center" valign="middle" height="40" width="40" style="background-color:${accent};color:#faf8f5;font-family:Georgia,'Times New Roman',serif;font-size:18px;font-weight:normal;border-radius:20px;line-height:40px;mso-line-height-rule:exactly;">${esc(String(stepNum))}</td>
          </tr>
        </table>
      </td>
      <td valign="top" style="font-family:Arial,Helvetica,sans-serif;color:#2a2a2a;">
        <div style="font-family:Georgia,'Times New Roman',serif;font-size:20px;line-height:1.3;color:#1a2744;margin:0 0 4px 0;">${esc(step.step || "")}</div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#6b6b6b;margin:0 0 14px 0;">
          <strong style="color:#1a2744;">${esc(step.product || "")}</strong>${step.brand ? ` &middot; ${esc(step.brand)}` : ""}${step.price ? ` &middot; <span style="color:#1a2744;font-weight:bold;">${esc(step.price)}</span>` : ""}
        </div>

        ${step.why ? `
        <div style="margin:0 0 12px 0;">
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:1.2px;color:#1a2744;text-transform:uppercase;margin:0 0 4px 0;font-weight:bold;">Pourquoi ce produit pour toi</div>
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#2a2a2a;">${esc(step.why)}</div>
        </div>` : ""}

        <div style="margin:0 0 12px 0;">
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:1.2px;color:#1a2744;text-transform:uppercase;margin:0 0 4px 0;font-weight:bold;">Comment l'appliquer</div>
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#2a2a2a;">
            ${how ? `<div style="margin:0 0 6px 0;">${esc(how)}</div>` : ""}
            <div style="margin:0 0 4px 0;"><em style="color:#6b6b6b;">Mécanisme —</em> ${esc(expert.mechanism)}</div>
            <div style="margin:0 0 4px 0;"><em style="color:#6b6b6b;">Geste —</em> ${esc(expert.technique)}</div>
            <div style="margin:0 0 4px 0;"><em style="color:#6b6b6b;">Quand —</em> ${esc(expert.when)}</div>
          </div>
        </div>

        ${step.benefit ? `
        <div style="margin:0 0 8px 0;">
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:1.2px;color:#1a2744;text-transform:uppercase;margin:0 0 4px 0;font-weight:bold;">Bénéfice en 2 à 4 semaines</div>
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#2a2a2a;">${esc(step.benefit)}</div>
        </div>` : ""}

        ${safe === true ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#6b6b6b;margin:8px 0 0 0;">&#9989; Compatible grossesse / allaitement</div>` : ""}
        ${safe === false ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#a14a4a;margin:8px 0 0 0;">&#9888; Non recommandé pendant grossesse / allaitement</div>` : ""}
      </td>
    </tr>
  </table>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 24px 0;"><tr><td style="border-top:1px solid #e6e1d8;font-size:0;line-height:0;height:1px;">&nbsp;</td></tr></table>
  `;
}

function renderBoosterCard(step) {
  return `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 16px 0;background-color:#faf8f5;border:1px solid #e6e1d8;">
    <tr>
      <td style="padding:18px 20px;font-family:Arial,Helvetica,sans-serif;color:#2a2a2a;">
        <div style="font-family:Georgia,'Times New Roman',serif;font-size:17px;line-height:1.3;color:#1a2744;margin:0 0 4px 0;">${esc(step.step || "")}</div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#6b6b6b;margin:0 0 10px 0;">
          <strong style="color:#1a2744;">${esc(step.product || "")}</strong>${step.brand ? ` &middot; ${esc(step.brand)}` : ""}${step.price ? ` &middot; <span style="color:#1a2744;font-weight:bold;">${esc(step.price)}</span>` : ""}
        </div>
        ${step.why ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.55;color:#2a2a2a;margin:0 0 6px 0;">${esc(step.why)}</div>` : ""}
        ${step.benefit ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.55;color:#6b6b6b;font-style:italic;">${esc(step.benefit)}</div>` : ""}
      </td>
    </tr>
  </table>
  `;
}

/* ----------------------------------------------------------------- *
 * 5. Plain-text fallback renderer
 * ----------------------------------------------------------------- */

function renderText(payload) {
  const name = get(payload, "name", "");
  const d = payload.diagnostic || {};
  const lines = [];

  lines.push(`Sonagi — Ton protocole peau personnalisé`);
  lines.push("");
  lines.push(`${name}, voici ton protocole.`);
  lines.push("");
  if (d.headline) lines.push(`« ${d.headline} »`);
  if (d.diagnostic) {
    lines.push("");
    lines.push(d.diagnostic);
  }
  lines.push("");
  if (d.hero_ingredient) {
    lines.push(`Ton ingrédient clé : ${d.hero_ingredient}`);
    if (d.hero_ingredient_why) lines.push(d.hero_ingredient_why);
    lines.push("");
  }

  const min = d.minimum_routine || {};
  if (min.label) {
    lines.push(`--- ${min.label} ---`);
    if (min.description) lines.push(min.description);
    lines.push("");
    (min.steps || []).forEach((s) => {
      lines.push(`${s.order || ""}. ${s.step || ""}`);
      lines.push(`   Produit : ${s.product || ""}${s.brand ? ` (${s.brand})` : ""}${s.price ? ` — ${s.price}` : ""}`);
      if (s.why) lines.push(`   Pourquoi : ${s.why}`);
      if (s.how) lines.push(`   Comment : ${s.how}`);
      if (s.benefit) lines.push(`   Bénéfice : ${s.benefit}`);
      lines.push("");
    });
  }

  if (d.evening_swap) {
    lines.push(`--- Soir — le swap ---`);
    const e = d.evening_swap;
    lines.push(`${e.product || ""}${e.brand ? ` (${e.brand})` : ""}${e.price ? ` — ${e.price}` : ""}`);
    if (e.why) lines.push(e.why);
    if (e.how) lines.push(`Application : ${e.how}`);
    lines.push("");
  }

  if (d.weekly_ritual) {
    lines.push(`--- Le rituel hebdomadaire ---`);
    const w = d.weekly_ritual;
    lines.push(`${w.product || ""}${w.brand ? ` (${w.brand})` : ""}`);
    if (w.frequency) lines.push(`Fréquence : ${w.frequency}`);
    if (w.why) lines.push(w.why);
    lines.push("");
  }

  const boosters = d.boosters || {};
  if ((boosters.steps || []).length) {
    lines.push(`--- Boosters — quand tu seras prête ---`);
    if (boosters.description) lines.push(boosters.description);
    (boosters.steps || []).forEach((b) => {
      lines.push(`• ${b.product || b.step || ""}${b.brand ? ` (${b.brand})` : ""}${b.price ? ` — ${b.price}` : ""}`);
      if (b.why) lines.push(`  ${b.why}`);
    });
    lines.push("");
  }

  if (d.total_minimum_cost || d.total_full_cost) {
    lines.push(`--- Le coût ---`);
    if (d.total_minimum_cost) lines.push(`Routine essentielle : ${d.total_minimum_cost}`);
    if (d.total_full_cost) lines.push(`Rituel complet     : ${d.total_full_cost}`);
    const note = budgetNote(get(payload, "answers.budget", ""), d.total_minimum_cost, d.total_full_cost);
    if (note) {
      lines.push("");
      lines.push(note.replace(/<[^>]+>/g, ""));
    }
    lines.push("");
  }

  if (d.first_week_tip) {
    lines.push(`--- Ton conseil semaine 1 ---`);
    lines.push(d.first_week_tip);
    lines.push("");
  }

  if (get(payload, "answers.pregnant", "") === "oui") {
    lines.push(`Note grossesse : tous les produits ci-dessus sont compatibles grossesse/allaitement. En cas de doute, parles-en à ton médecin.`);
    lines.push("");
  }

  lines.push(`Prends soin de toi,`);
  lines.push(`— Sonagi`);
  lines.push("");
  lines.push(`https://sonagibeauty.com`);
  lines.push(`Tu reçois cet email parce que tu as fait notre diagnostic peau.`);

  return lines.join("\n");
}

/* ----------------------------------------------------------------- *
 * 6. The main renderer
 * ----------------------------------------------------------------- */

function renderProtocolEmail(payload) {
  const name = get(payload, "name", "");
  const safeName = esc(name) || "Toi";
  const d = payload.diagnostic || {};
  const answers = payload.answers || {};
  const isPregnant = String(answers.pregnant || "").toLowerCase() === "oui";

  const subject = `🌸 ${name ? name + ", t" : "T"}on protocole peau Sonagi est arrivé`;
  const preheader = d.headline || "Ton protocole personnalisé Sonagi — par notre dermatologue";

  const min = d.minimum_routine || {};
  const minSteps = Array.isArray(min.steps) ? min.steps : [];
  const eveningSwap = d.evening_swap || null;
  const weekly = d.weekly_ritual || null;
  const boosters = d.boosters || {};
  const boosterSteps = Array.isArray(boosters.steps) ? boosters.steps : [];

  const note = budgetNote(answers.budget, d.total_minimum_cost || "—", d.total_full_cost || "—");

  /* ---- HEAD with dark-mode + Outlook fixes ---- */
  const head = `<!DOCTYPE html>
<html lang="fr" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>${esc(subject)}</title>
  <!--[if mso]>
  <style>table,td,div,h1,p {font-family:Arial,Helvetica,sans-serif !important;}</style>
  <![endif]-->
  <style>
    @media (prefers-color-scheme: dark) {
      .sg-bg      { background-color:#0e1424 !important; }
      .sg-card    { background-color:#1a2030 !important; }
      .sg-ink     { color:#f5efe5 !important; }
      .sg-muted   { color:#a8a397 !important; }
      .sg-cream   { background-color:#1a2030 !important; }
      .sg-line td { border-color:#3a3a3a !important; }
      .sg-peach   { background-color:#3a2a1f !important; color:#f5c4aa !important; }
      .sg-navy    { background-color:#0a0f1c !important; }
    }
    @media only screen and (max-width:620px) {
      .sg-container { width:100% !important; }
      .sg-pad       { padding-left:20px !important; padding-right:20px !important; }
      .sg-h1        { font-size:28px !important; line-height:1.2 !important; }
      .sg-quote     { font-size:22px !important; line-height:1.35 !important; }
    }
    a { color:#1a2744; }
    img { border:0; outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; }
    body, table, td { -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }
    body { margin:0; padding:0; width:100% !important; }
  </style>
</head>`;

  /* ---- Pre-header (hidden inbox preview text) ---- */
  const preheaderBlock = `
  <div style="display:none;font-size:1px;color:#faf8f5;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;mso-hide:all;">
    ${esc(preheader)}
    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>`;

  /* ---- Hero block ---- */
  const hero = `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" class="sg-navy" style="background-color:#1a2744;">
    <tr>
      <td align="center" class="sg-pad" style="padding:48px 40px 44px 40px;">
        <div style="font-family:Georgia,'Times New Roman',serif;font-size:14px;letter-spacing:6px;color:#f5c4aa;text-transform:uppercase;margin:0 0 12px 0;">SONAGI</div>
        <div style="font-family:Georgia,'Times New Roman',serif;font-size:32px;line-height:1.25;color:#faf8f5;margin:0 0 8px 0;" class="sg-h1">${esc(safeName)}, voici ton protocole.</div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.55;color:#e6d4c4;margin:0;">Pensé étape par étape, par notre dermatologue, pour TA peau.</div>
      </td>
    </tr>
  </table>`;

  /* ---- Diagnostic block ---- */
  const diagnostic = `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:40px 40px 8px 40px;background-color:#faf8f5;">
        ${d.headline ? `<div class="sg-quote sg-ink" style="font-family:Georgia,'Times New Roman',serif;font-size:26px;line-height:1.35;color:#1a2744;margin:0 0 18px 0;">&laquo; ${esc(d.headline)} &raquo;</div>` : ""}
        ${d.diagnostic ? `<div class="sg-ink" style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:#2a2a2a;margin:0 0 8px 0;">${esc(d.diagnostic)}</div>` : ""}
      </td>
    </tr>
  </table>`;

  /* ---- Hero ingredient pill ---- */
  const heroIngredient = (d.hero_ingredient || d.hero_ingredient_why) ? `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:8px 40px 32px 40px;background-color:#faf8f5;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" class="sg-peach" style="background-color:#f5c4aa;border-radius:6px;">
          <tr>
            <td style="padding:24px 26px;">
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:2px;color:#1a2744;text-transform:uppercase;margin:0 0 6px 0;font-weight:bold;">Ton ingrédient clé</div>
              <div style="font-family:Georgia,'Times New Roman',serif;font-size:24px;line-height:1.3;color:#1a2744;margin:0 0 10px 0;">${esc(d.hero_ingredient || "")}</div>
              ${d.hero_ingredient_why ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#2a2a2a;">${esc(d.hero_ingredient_why)}</div>` : ""}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>` : "";

  /* ---- Section heading helper ---- */
  function sectionHeading(eyebrow, title, lead) {
    return `
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td class="sg-pad sg-card" style="padding:32px 40px 8px 40px;background-color:#faf8f5;">
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:2px;color:#d4a373;text-transform:uppercase;margin:0 0 8px 0;font-weight:bold;">${esc(eyebrow)}</div>
          <div class="sg-ink" style="font-family:Georgia,'Times New Roman',serif;font-size:24px;line-height:1.3;color:#1a2744;margin:0 0 ${lead ? "12" : "20"}px 0;">${esc(title)}</div>
          ${lead ? `<div class="sg-ink" style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#2a2a2a;margin:0 0 20px 0;">${esc(lead)}</div>` : ""}
        </td>
      </tr>
    </table>`;
  }

  /* ---- Minimum routine ---- */
  const minimumRoutine = `
  ${sectionHeading("Routine essentielle", min.label || "Ton 3-étapes non-négociable", min.description || "")}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:0 40px 16px 40px;background-color:#faf8f5;">
        ${minSteps.map((s, i) => renderStepCard(s, { stepNum: s.order || (i + 1), accent: "#1a2744" })).join("")}
      </td>
    </tr>
  </table>`;

  /* ---- Evening swap ---- */
  const eveningSwapBlock = eveningSwap ? `
  ${sectionHeading("Soir", "Le swap du soir", "Le geste qui change tout : tu remplaces une étape de la routine du jour par celui-ci, le soir.")}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:0 40px 16px 40px;background-color:#faf8f5;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#fbf3eb;border-left:4px solid #d4a373;">
          <tr>
            <td style="padding:22px 24px;">
              <div style="font-family:Georgia,'Times New Roman',serif;font-size:18px;line-height:1.3;color:#1a2744;margin:0 0 6px 0;">${esc(eveningSwap.product || "")}</div>
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#6b6b6b;margin:0 0 12px 0;">
                ${eveningSwap.brand ? `<strong style="color:#1a2744;">${esc(eveningSwap.brand)}</strong>` : ""}${eveningSwap.price ? ` &middot; <span style="color:#1a2744;font-weight:bold;">${esc(eveningSwap.price)}</span>` : ""}
              </div>
              ${eveningSwap.why ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#2a2a2a;margin:0 0 10px 0;">${esc(eveningSwap.why)}</div>` : ""}
              ${eveningSwap.how ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#2a2a2a;margin:0 0 8px 0;"><em style="color:#6b6b6b;">Application —</em> ${esc(eveningSwap.how)}</div>` : ""}
              ${eveningSwap.benefit ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#6b6b6b;font-style:italic;">${esc(eveningSwap.benefit)}</div>` : ""}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>` : "";

  /* ---- Weekly ritual ---- */
  const weeklyBlock = weekly ? `
  ${sectionHeading("1 fois par semaine", "Le rituel hebdomadaire", "Pas tous les jours — mais un rendez-vous fixe, comme une mini-séance institut à la maison.")}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:0 40px 16px 40px;background-color:#faf8f5;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#ffffff;border:1px solid #e6e1d8;">
          <tr>
            <td style="padding:22px 24px;">
              <div style="font-family:Georgia,'Times New Roman',serif;font-size:18px;line-height:1.3;color:#1a2744;margin:0 0 6px 0;">${esc(weekly.product || "")}</div>
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#6b6b6b;margin:0 0 12px 0;">
                ${weekly.brand ? `<strong style="color:#1a2744;">${esc(weekly.brand)}</strong>` : ""}${weekly.frequency ? ` &middot; ${esc(weekly.frequency)}` : ""}
              </div>
              ${weekly.why ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#2a2a2a;margin:0 0 10px 0;">${esc(weekly.why)}</div>` : ""}
              ${weekly.benefit ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#6b6b6b;font-style:italic;">${esc(weekly.benefit)}</div>` : ""}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>` : "";

  /* ---- Boosters ---- */
  const boostersBlock = boosterSteps.length ? `
  ${sectionHeading("Pour aller plus loin", boosters.label || "Boosters — quand tu seras prête", boosters.description || "Pas tout de suite. Une fois la routine essentielle bien installée (3 à 4 semaines), tu pourras ajouter ces actifs un par un.")}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:0 40px 16px 40px;background-color:#faf8f5;">
        ${boosterSteps.map(renderBoosterCard).join("")}
      </td>
    </tr>
  </table>` : "";

  /* ---- Cost summary ---- */
  const costBlock = (d.total_minimum_cost || d.total_full_cost) ? `
  ${sectionHeading("Le budget", "Combien ça coûte, vraiment", "")}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:0 40px 16px 40px;background-color:#faf8f5;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#ffffff;border:1px solid #e6e1d8;">
          <tr>
            <td style="padding:18px 22px;border-bottom:1px solid #e6e1d8;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#2a2a2a;">Routine essentielle</td>
                  <td align="right" style="font-family:Georgia,'Times New Roman',serif;font-size:18px;color:#1a2744;font-weight:bold;">${esc(d.total_minimum_cost || "—")}</td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:18px 22px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#2a2a2a;">Rituel complet (essentielle + boosters)</td>
                  <td align="right" style="font-family:Georgia,'Times New Roman',serif;font-size:18px;color:#1a2744;font-weight:bold;">${esc(d.total_full_cost || "—")}</td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
        ${note ? `<div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#6b6b6b;margin:14px 0 0 0;font-style:italic;">${note}</div>` : ""}
      </td>
    </tr>
  </table>` : "";

  /* ---- First-week tip ---- */
  const tipBlock = d.first_week_tip ? `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:24px 40px 16px 40px;background-color:#faf8f5;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#1a2744;">
          <tr>
            <td style="padding:24px 26px;">
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:2px;color:#f5c4aa;text-transform:uppercase;margin:0 0 8px 0;font-weight:bold;">Ton conseil semaine 1</div>
              <div style="font-family:Georgia,'Times New Roman',serif;font-size:18px;line-height:1.5;color:#faf8f5;">${esc(d.first_week_tip)}</div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>` : "";

  /* ---- Pregnancy footer ---- */
  const pregnancyBlock = isPregnant ? `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:8px 40px 24px 40px;background-color:#faf8f5;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#fff8e1;border:1px solid #f5d76e;border-left:4px solid #d4a373;">
          <tr>
            <td style="padding:18px 22px;">
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#5a4a1a;">
                <strong>&#129328; Grossesse &amp; allaitement —</strong> Tous les produits ci-dessus ont été sélectionnés pour être compatibles avec ta grossesse ou ton allaitement. Si tu as le moindre doute sur un actif, parles-en à ton médecin ou à ta sage-femme — c'est toujours la bonne réponse.
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>` : "";

  /* ---- Sign-off ---- */
  const signoff = `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td class="sg-pad sg-card" style="padding:32px 40px 40px 40px;background-color:#faf8f5;">
        <div class="sg-ink" style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:#2a2a2a;margin:0 0 12px 0;">Une routine, ce n'est pas une promesse — c'est une habitude. Sois douce avec toi : 14 jours pour voir les premiers résultats, 28 jours pour les ancrer. On est là si tu as la moindre question.</div>
        <div style="font-family:Georgia,'Times New Roman',serif;font-style:italic;font-size:18px;line-height:1.5;color:#1a2744;margin:18px 0 0 0;">Prends soin de toi,<br>&mdash; Sonagi</div>
      </td>
    </tr>
  </table>`;

  /* ---- Footer ---- */
  const footer = `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#1a2744;">
    <tr>
      <td align="center" class="sg-pad" style="padding:32px 40px;">
        <div style="font-family:Georgia,'Times New Roman',serif;font-size:14px;letter-spacing:6px;color:#f5c4aa;text-transform:uppercase;margin:0 0 14px 0;">SONAGI</div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.7;color:#e6d4c4;margin:0 0 14px 0;">
          <a href="https://sonagibeauty.com" style="color:#faf8f5;text-decoration:none;">sonagibeauty.com</a>
          &nbsp;&middot;&nbsp;
          <a href="https://instagram.com/sonagi.beauty" style="color:#faf8f5;text-decoration:none;">Instagram</a>
          &nbsp;&middot;&nbsp;
          <a href="https://tiktok.com/@sonagi.beauty" style="color:#faf8f5;text-decoration:none;">TikTok</a>
        </div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;line-height:1.6;color:#a8a397;margin:0 0 8px 0;">
          Tu as reçu cet email parce que tu as fait notre diagnostic peau sur sonagibeauty.com.
        </div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;line-height:1.6;color:#a8a397;">
          <a href="{{unsubscribe_url}}" style="color:#a8a397;text-decoration:underline;">Se désinscrire</a>
          &nbsp;&middot;&nbsp;
          <a href="mailto:contact@sonagibeauty.com" style="color:#a8a397;text-decoration:underline;">contact@sonagibeauty.com</a>
        </div>
      </td>
    </tr>
  </table>`;

  /* ---- Assemble ---- */
  const body = `
<body class="sg-bg" style="margin:0;padding:0;background-color:#e6e1d8;">
  ${preheaderBlock}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" class="sg-bg" style="background-color:#e6e1d8;">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="sg-container sg-card" style="width:600px;max-width:600px;background-color:#faf8f5;">
          <tr><td>${hero}</td></tr>
          <tr><td>${diagnostic}</td></tr>
          <tr><td>${heroIngredient}</td></tr>
          <tr><td>${minimumRoutine}</td></tr>
          <tr><td>${eveningSwapBlock}</td></tr>
          <tr><td>${weeklyBlock}</td></tr>
          <tr><td>${boostersBlock}</td></tr>
          <tr><td>${costBlock}</td></tr>
          <tr><td>${tipBlock}</td></tr>
          <tr><td>${pregnancyBlock}</td></tr>
          <tr><td>${signoff}</td></tr>
          <tr><td>${footer}</td></tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;

  const html = head + body;
  const text = renderText(payload);

  return { subject, html, text };
}

module.exports = { renderProtocolEmail, pickExpertDepth, EXPERT_DEPTH };
