/* ══════════════════════════════════════════════════════
   SONAGI ADVISOR QUIZ — v3 (5 questions, basket hand-off)
   ──────────────────────────────────────────────────────
   Replaces the inline quiz logic that used to live in every
   HTML page. Mounts into the existing #quiz-modal shell and
   rebuilds the body with 5 streamlined questions.

   Public API (window.SonagiQuiz):
     init()   — wires the modal + global aliases
     open()   — opens the modal, resets state, shows step 1
     close()  — closes the modal
     state()  — returns current QA snapshot (for debugging)

   Backwards-compat globals (so existing onclick="openQuiz()"
   buttons in HTML keep working):
     window.openQuiz, window.closeQuiz
   ══════════════════════════════════════════════════════ */
(function () {
  "use strict";

  // ── CONFIG ─────────────────────────────────────────────
  const QT = 5; // total questions — must match banner copy
  const ENDPOINT_ADVISOR = "/.netlify/functions/quiz-advisor";
  const ENDPOINT_EMAIL   = "/.netlify/functions/send-protocol";
  const EMAIL_RX = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  // ── STATE ──────────────────────────────────────────────
  let QS = 1;
  const FRESH_QA = () => ({
    name: "",
    email: "",
    skin_type: "",       // grasse | seche | mixte | normale
    sensitive: false,
    pregnant: "non",     // non | oui  (kept for advisor prompt contract)
    concerns: [],        // max 2
    age: "",             // 18-25 | 26-32 | 33-40 | 40+
    lifestyle: "",       // sport-actif | écran-toute-la-journée | soleil-souvent | nuits-courtes
    budget: "",          // 30-50 | 50-90 | 90-150 | 150+
    routine_goal: ""     // minimum-efficace | rituel-complet
  });
  let QA = FRESH_QA();
  let LAST_DIAGNOSTIC = null; // last AI response, used by basket CTAs

  // ── HELPERS ────────────────────────────────────────────
  const $  = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  const escapeHtml = (s) => String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");

  const slugify = (s) => String(s || "")
    .toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "") // strip accents
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  // Build a stable SKU from brand + product name. When the catalog
  // fills with real Stripe price IDs, the SKUs must match this slug.
  const skuFor = (brand, product) => slugify(brand + "-" + product);

  const parsePrice = (str) => {
    const m = String(str || "").match(/(\d+(?:[.,]\d+)?)/);
    return m ? parseFloat(m[1].replace(",", ".")) : 0;
  };

  // ── MODAL SHELL ────────────────────────────────────────
  // We reuse the page's existing #quiz-modal overlay but replace
  // its .modal-body content with our own dynamic panels.
  function ensureModal() {
    const modal = document.getElementById("quiz-modal");
    if (!modal) return null;
    return modal;
  }

  function buildBody() {
    const modal = ensureModal();
    if (!modal) return;
    const body = modal.querySelector(".modal-body");
    if (!body) return;
    body.innerHTML = `
      <div class="disclaimer">⚕ Questionnaire cosmétique. Consultez votre médecin en cas de condition particulière.</div>
      <div class="qprog"><div class="qprog-bar" id="qpbar" style="width:${(1/QT)*100}%"></div></div>

      <!-- Q1 — Name + email -->
      <div class="quiz-step active" data-step="1">
        <span class="step-ctr">1 / ${QT} — Toi</span>
        <h3 class="quiz-q">On commence par toi</h3>
        <p class="quiz-sub">Pour t'envoyer ton protocole personnalisé, signé Sonagi Advisor.</p>
        <input type="text" class="quiz-input" id="sq-name" placeholder="Ton prénom" maxlength="40" autocomplete="given-name">
        <input type="email" class="quiz-input" id="sq-email" placeholder="ton.email@exemple.com" maxlength="120" autocomplete="email" style="margin-top:10px">
        <p class="quiz-err" id="sq-err-1" style="display:none;color:#c0392b;font-size:12px;margin-top:8px"></p>
        <p class="quiz-fineprint" style="margin-top:10px;font-size:11px;color:var(--muted,#888)">On t'envoie uniquement ton protocole et quelques rituels K-beauty. Désinscription en un clic.</p>
      </div>

      <!-- Q2 — Skin type + sensitivity + pregnancy -->
      <div class="quiz-step" data-step="2">
        <span class="step-ctr">2 / ${QT} — Ta peau</span>
        <h3 class="quiz-q">Quel est ton type de peau ?</h3>
        <div class="quiz-opts" data-group="skin_type">
          <button type="button" class="q-opt" data-val="grasse">Grasse — brillances, pores</button>
          <button type="button" class="q-opt" data-val="seche">Sèche — tiraillements</button>
          <button type="button" class="q-opt" data-val="mixte">Mixte — zone T grasse</button>
          <button type="button" class="q-opt" data-val="normale">Normale — équilibrée</button>
        </div>
        <div class="quiz-toggle-row" style="margin-top:18px;display:flex;flex-direction:column;gap:10px">
          <label class="quiz-toggle" style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:13px">
            <input type="checkbox" id="sq-sensitive"> Ma peau est sensible / réactive
          </label>
          <label class="quiz-toggle" style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:13px">
            <input type="checkbox" id="sq-pregnant"> Je suis enceinte ou allaitante
          </label>
        </div>
        <p class="quiz-err" id="sq-err-2" style="display:none;color:#c0392b;font-size:12px;margin-top:8px"></p>
      </div>

      <!-- Q3 — Top 2 concerns -->
      <div class="quiz-step" data-step="3">
        <span class="step-ctr">3 / ${QT} — Priorités</span>
        <h3 class="quiz-q">Tes 2 priorités peau ?</h3>
        <p class="quiz-sub">Choisis-en deux maximum — on construit ton protocole autour.</p>
        <div class="quiz-opts multi" data-group="concerns" data-max="2">
          <button type="button" class="q-opt" data-val="pores">Pores dilatés</button>
          <button type="button" class="q-opt" data-val="deshydratation">Déshydratation</button>
          <button type="button" class="q-opt" data-val="teint-terne">Teint terne</button>
          <button type="button" class="q-opt" data-val="taches">Taches pigmentaires</button>
          <button type="button" class="q-opt" data-val="acne">Acné &amp; imperfections</button>
          <button type="button" class="q-opt" data-val="rides">Ridules &amp; fermeté</button>
          <button type="button" class="q-opt" data-val="rougeurs">Rougeurs</button>
          <button type="button" class="q-opt" data-val="zone-t-grasse">Zone T grasse</button>
        </div>
        <p class="quiz-note" id="sq-note-3" style="display:none;font-size:12px;color:var(--muted,#888);margin-top:8px">Maximum 2 — on a remplacé ta plus ancienne sélection.</p>
        <p class="quiz-err" id="sq-err-3" style="display:none;color:#c0392b;font-size:12px;margin-top:8px"></p>
      </div>

      <!-- Q4 — Age + lifestyle -->
      <div class="quiz-step" data-step="4">
        <span class="step-ctr">4 / ${QT} — Ton quotidien</span>
        <h3 class="quiz-q">Ta tranche d'âge ?</h3>
        <div class="quiz-opts" data-group="age">
          <button type="button" class="q-opt" data-val="18-25">18–25</button>
          <button type="button" class="q-opt" data-val="26-32">26–32</button>
          <button type="button" class="q-opt" data-val="33-40">33–40</button>
          <button type="button" class="q-opt" data-val="40+">40+</button>
        </div>
        <h3 class="quiz-q" style="margin-top:20px">Ce qui décrit le mieux ton mode de vie ?</h3>
        <div class="quiz-opts" data-group="lifestyle">
          <button type="button" class="q-opt" data-val="sport-actif">Sport &amp; vie active</button>
          <button type="button" class="q-opt" data-val="ecran-toute-la-journee">Écrans toute la journée</button>
          <button type="button" class="q-opt" data-val="soleil-souvent">Souvent au soleil</button>
          <button type="button" class="q-opt" data-val="nuits-courtes">Nuits courtes / stress</button>
        </div>
        <p class="quiz-err" id="sq-err-4" style="display:none;color:#c0392b;font-size:12px;margin-top:8px"></p>
      </div>

      <!-- Q5 — Budget + ambition -->
      <div class="quiz-step" data-step="5">
        <span class="step-ctr">5 / ${QT} — Budget &amp; rituel</span>
        <h3 class="quiz-q">Ton budget pour cette routine ?</h3>
        <div class="quiz-opts" data-group="budget">
          <button type="button" class="q-opt" data-val="30-50">30–50 €</button>
          <button type="button" class="q-opt" data-val="50-90">50–90 €</button>
          <button type="button" class="q-opt" data-val="90-150">90–150 €</button>
          <button type="button" class="q-opt" data-val="150+">150 € et +</button>
        </div>
        <h3 class="quiz-q" style="margin-top:20px">Ton ambition ?</h3>
        <div class="quiz-opts" data-group="routine_goal">
          <button type="button" class="q-opt" data-val="minimum-efficace">Minimum efficace — 3 produits</button>
          <button type="button" class="q-opt" data-val="rituel-complet">Rituel complet — 5 à 7 produits</button>
        </div>
        <p class="quiz-err" id="sq-err-5" style="display:none;color:#c0392b;font-size:12px;margin-top:8px"></p>
      </div>

      <!-- Result -->
      <div class="quiz-step" data-step="result" id="quiz-result-step">
        <div id="quiz-loading" style="text-align:center;padding:40px 0">
          <div class="quiz-spinner"></div>
          <p style="margin-top:16px;font-size:14px;color:var(--muted,#888)">Sonagi Advisor analyse ton profil…</p>
        </div>
        <div id="quiz-results" style="display:none"></div>
      </div>

      <div class="quiz-nav-btns" id="qnav">
        <button type="button" class="q-back" id="q-back-btn" style="visibility:hidden">Retour</button>
        <button type="button" class="q-next" id="q-next-btn">Continuer</button>
      </div>
    `;
    bindBody();
  }

  // ── EVENT BINDING ──────────────────────────────────────
  function bindBody() {
    const modal = ensureModal();
    if (!modal) return;

    // Single-select option groups (Q2 skin_type, Q4 age + lifestyle, Q5 budget + routine_goal)
    $$('.quiz-opts:not(.multi)', modal).forEach((group) => {
      const key = group.getAttribute("data-group");
      $$(".q-opt", group).forEach((btn) => {
        btn.addEventListener("click", () => {
          $$(".q-opt", group).forEach((o) => o.classList.remove("sel"));
          btn.classList.add("sel");
          QA[key] = btn.getAttribute("data-val");
        });
      });
    });

    // Multi-select with max (Q3 concerns, max 2 — drop oldest when exceeding)
    $$(".quiz-opts.multi", modal).forEach((group) => {
      const key = group.getAttribute("data-group");
      const max = parseInt(group.getAttribute("data-max") || "0", 10) || 0;
      $$(".q-opt", group).forEach((btn) => {
        btn.addEventListener("click", () => {
          if (!Array.isArray(QA[key])) QA[key] = [];
          const val = btn.getAttribute("data-val");
          const idx = QA[key].indexOf(val);
          if (idx !== -1) {
            // Deselect
            QA[key].splice(idx, 1);
            btn.classList.remove("sel");
            return;
          }
          QA[key].push(val);
          btn.classList.add("sel");
          // Enforce max — drop oldest
          if (max > 0 && QA[key].length > max) {
            const dropped = QA[key].shift();
            const oldBtn = $$(".q-opt", group).find((b) => b.getAttribute("data-val") === dropped);
            if (oldBtn) oldBtn.classList.remove("sel");
            const note = $("#sq-note-3");
            if (note) {
              note.style.display = "block";
              clearTimeout(note._t);
              note._t = setTimeout(() => { note.style.display = "none"; }, 2400);
            }
          }
        });
      });
    });

    // Toggles in Q2
    const sens = $("#sq-sensitive");
    if (sens) sens.addEventListener("change", () => { QA.sensitive = !!sens.checked; });
    const preg = $("#sq-pregnant");
    if (preg) preg.addEventListener("change", () => { QA.pregnant = preg.checked ? "oui" : "non"; });

    // Nav buttons
    const back = $("#q-back-btn");
    if (back) back.addEventListener("click", qBack);
    const next = $("#q-next-btn");
    if (next) next.addEventListener("click", qNext);

    // Live email/name capture (also captured on Next)
    const ni = $("#sq-name");  if (ni) ni.addEventListener("input", () => { QA.name  = ni.value.trim(); });
    const ei = $("#sq-email"); if (ei) ei.addEventListener("input", () => { QA.email = ei.value.trim(); });
  }

  // ── NAV / VALIDATION ───────────────────────────────────
  function showQS(s) {
    const modal = ensureModal(); if (!modal) return;
    $$(".quiz-step", modal).forEach((x) => x.classList.remove("active"));
    const sel = (s === "result") ? '[data-step="result"]' : '[data-step="' + s + '"]';
    const t = modal.querySelector(sel);
    if (t) t.classList.add("active");
    const pct = (s === "result") ? 100 : (s / QT) * 100;
    const bar = $("#qpbar"); if (bar) bar.style.width = pct + "%";

    const nav = $("#qnav");
    if (!nav) return;
    if (s === "result") { nav.style.display = "none"; return; }
    nav.style.display = "flex";
    const back = $("#q-back-btn"); if (back) back.style.visibility = (s > 1) ? "visible" : "hidden";
    const isLast = (s === QT);
    const nb = $("#q-next-btn"); if (nb) nb.textContent = isLast ? "Voir mon protocole →" : "Continuer";
  }

  function setErr(step, msg) {
    const e = document.getElementById("sq-err-" + step);
    if (!e) return;
    if (!msg) { e.style.display = "none"; e.textContent = ""; return; }
    e.style.display = "block"; e.textContent = msg;
  }

  function validateStep(s) {
    setErr(s, "");
    if (s === 1) {
      const name = (QA.name || "").trim();
      const email = (QA.email || "").trim();
      if (!name) { setErr(1, "Indique ton prénom pour personnaliser ton protocole."); return false; }
      if (!EMAIL_RX.test(email)) { setErr(1, "Adresse email invalide. Vérifie le format."); return false; }
      return true;
    }
    if (s === 2) {
      if (!QA.skin_type) { setErr(2, "Choisis ton type de peau pour continuer."); return false; }
      return true;
    }
    if (s === 3) {
      if (!QA.concerns || !QA.concerns.length) { setErr(3, "Choisis au moins une priorité."); return false; }
      return true;
    }
    if (s === 4) {
      if (!QA.age)        { setErr(4, "Sélectionne ta tranche d'âge."); return false; }
      if (!QA.lifestyle)  { setErr(4, "Sélectionne ce qui décrit ton quotidien."); return false; }
      return true;
    }
    if (s === 5) {
      if (!QA.budget)        { setErr(5, "Choisis ton budget."); return false; }
      if (!QA.routine_goal)  { setErr(5, "Choisis ton ambition de routine."); return false; }
      return true;
    }
    return true;
  }

  function qNext() {
    // capture inputs for step 1
    if (QS === 1) {
      const ni = $("#sq-name");  if (ni) QA.name  = ni.value.trim();
      const ei = $("#sq-email"); if (ei) QA.email = ei.value.trim();
    }
    if (!validateStep(QS)) return;
    if (QS < QT) { QS++; showQS(QS); }
    else { showQS("result"); runAdvisor(); }
  }
  function qBack() { if (QS > 1) { QS--; showQS(QS); } }

  // ── ADVISOR PROMPT (preserves netlify function contract) ──
  // The netlify function reads a single `prompt` string and forwards
  // it to Claude. We mirror the exact JSON-shape contract from the
  // original inline advisor (same field names, same structure) so the
  // existing function deploy keeps working unchanged.
  function buildPrompt() {
    const isP = QA.pregnant === "oui";
    // Translate our 5-question answers to the legacy field names the
    // original prompt uses, so Claude receives the same context shape.
    const skin_type = QA.sensitive ? (QA.skin_type + " (sensible)") : QA.skin_type;
    const skin_feel = inferSkinFeel(QA);
    const goal = QA.concerns.join(", ");
    const lifestyle = QA.lifestyle;
    const current_routine = "(non demandé — supposer routine basique)";
    const routine_goal = QA.routine_goal === "minimum-efficace"
      ? "minimaliste 3 étapes"
      : "complète 5-7 étapes";
    const budget_label = ({
      "30-50":  "30-50€",
      "50-90":  "50-90€",
      "90-150": "90-150€",
      "150+":   "150€ et plus"
    })[QA.budget] || QA.budget;

    return [
      "You are Sonagi's expert K-beauty skin advisor and a trained dermatologist + cosmetic chemist.",
      "Your job is to give a protocol that feels like advice from a knowledgeable friend, not a marketing leaflet.",
      "STRICTLY respect the budget given — total_minimum_cost MUST fit inside the budget range.",
      "",
      "SKIN PROFILE:",
      "- Name: " + QA.name,
      "- Goals: " + goal,
      "- Skin type: " + skin_type,
      "- Skin feel end of day: " + skin_feel,
      "- Age: " + QA.age,
      "- Lifestyle: " + lifestyle,
      "- Current routine: " + current_routine,
      "- Routine length preference: " + routine_goal,
      "- Budget: " + budget_label,
      "- Pregnant/breastfeeding: " + QA.pregnant,
      "",
      isP
        ? "PREGNANCY SAFETY — NEVER recommend: retinol, retinoids, salicylic acid >2%, chemical sunscreens (oxybenzone), hydroquinone, TXA in 3rd trimester/breastfeeding, essential oils (mugwort, rosemary, tea tree, cinnamon, ylang ylang).\nSAFE: niacinamide, hyaluronic acid, centella, ceramides, vitamin C, azelaic acid, panthenol, bakuchiol, peptides.\n"
        : "",
      "RESPONSE RULES:",
      "- Be direct and specific. No generic advice.",
      "- Never say \"consult a dermatologist\" unless medically necessary.",
      "- Product names must be real K-beauty products that exist and are available in Europe.",
      "- Brands: COSRX, Beauty of Joseon, Anua, Some By Mi, Laneige, Innisfree, Mixsoon, Purito, Skin1004, Numbuzin, Round Lab, Axis-Y, Torriden, Thank You Farmer, Klairs.",
      "- Price ranges in EUR.",
      "",
      "Respond ONLY with valid JSON, no markdown, no backticks:",
      "",
      '{"headline":"One punchy 6-8 word line that captures their skin story","diagnostic":"One sharp insightful sentence that diagnoses their skin like a professional","minimum_routine":{"label":"Your 3-step non-negotiable","description":"One sentence on why these 3 steps are enough","steps":[{"order":1,"step":"Step name","product":"Exact product name","brand":"Brand","why":"One sentence for THEIR skin","how":"One punchy K-beauty application tip","benefit":"What they will notice in 2-4 weeks","price":"€X","pregnancy_safe":true}]},"boosters":{"label":"Level up when ready","description":"One sentence framing these as upgrades","steps":[{"order":1,"step":"Step name","product":"Exact product name","brand":"Brand","why":"What this adds","how":"Application tip","benefit":"The visible result","price":"€X","pregnancy_safe":true}]},"evening_swap":{"label":"At night one change","product":"Exact product name","brand":"Brand","why":"Why nighttime works best","how":"How to use","benefit":"What they will wake up with","price":"€X","pregnancy_safe":true},"weekly_ritual":{"product":"One weekly treatment","brand":"Brand","frequency":"1-2x per week","why":"Why this weekly step amplifies everything","benefit":"Cumulative result after 1 month","pregnancy_safe":true},"hero_ingredient":"Single most powerful ingredient","hero_ingredient_why":"One sentence why","first_week_tip":"One specific practical tip for the first 7 days","total_minimum_cost":"€X-€Y","total_full_cost":"€X-€Y"}'
    ].join("\n");
  }

  // Heuristic fallback: derive a plausible "skin_feel" from skin_type,
  // since the new 5-question flow doesn't ask it directly.
  function inferSkinFeel(a) {
    if (a.sensitive) return "irritee ou reactive";
    switch (a.skin_type) {
      case "grasse":  return "grasse et brillante";
      case "seche":   return "seche et qui tire";
      case "mixte":   return "grasse sur la zone T, seche sur les joues";
      default:        return "bien globalement";
    }
  }

  // ── ADVISOR CALL ───────────────────────────────────────
  function runAdvisor() {
    LAST_DIAGNOSTIC = null;
    const loading = $("#quiz-loading"); if (loading) loading.style.display = "block";
    const rr = $("#quiz-results"); if (rr) { rr.style.display = "none"; rr.innerHTML = ""; }

    const prompt = buildPrompt();
    fetch(ENDPOINT_ADVISOR, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: prompt })
    })
      .then((r) => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then((data) => {
        if (!data || !data.minimum_routine) throw new Error("Bad payload");
        LAST_DIAGNOSTIC = data;
        renderResults(data);
        sendProtocolEmail(data); // fire-and-forget
      })
      .catch((err) => {
        console.error("[SonagiQuiz] Advisor error:", err);
        renderError();
      });
  }

  function renderError() {
    const loading = $("#quiz-loading"); if (loading) loading.style.display = "none";
    const rr = $("#quiz-results"); if (!rr) return;
    rr.style.display = "block";
    rr.innerHTML = `
      <div style="text-align:center;padding:30px">
        <p style="font-size:18px;margin-bottom:12px">Le service est temporairement indisponible</p>
        <p style="font-size:13px;color:var(--muted,#888);margin-bottom:18px">Réessaie dans quelques instants — ou écris-nous à contact@sonagibeauty.com.</p>
        <button type="button" class="btn-primary" id="sq-retry">Réessayer</button>
      </div>`;
    const btn = document.getElementById("sq-retry");
    if (btn) btn.addEventListener("click", runAdvisor);
  }

  // ── RESULT RENDERING ───────────────────────────────────
  function renderStep(s) {
    if (!s) return "";
    return `
      <div class="adv-step">
        <div class="adv-step-head">
          <span class="adv-step-num">${escapeHtml(s.order)}</span>
          <span class="adv-step-name">${escapeHtml(s.step)}</span>
        </div>
        <p class="adv-product"><strong>${escapeHtml(s.brand)}</strong> — ${escapeHtml(s.product)}</p>
        <p class="adv-why">${escapeHtml(s.why)}</p>
        <p class="adv-how"><em>💡 ${escapeHtml(s.how)}</em></p>
        <p class="adv-benefit">→ ${escapeHtml(s.benefit)}</p>
        <span class="adv-price">${escapeHtml(s.price)}</span>
        ${s.pregnancy_safe ? '<span class="adv-safe">✓ Safe</span>' : ''}
      </div>`;
  }

  function renderResults(d) {
    const loading = $("#quiz-loading"); if (loading) loading.style.display = "none";
    const rr = $("#quiz-results"); if (!rr) return;
    rr.style.display = "block";

    const minSteps  = (d.minimum_routine && d.minimum_routine.steps) || [];
    const boostSteps = (d.boosters && d.boosters.steps) || [];

    let h = "";
    h += `<h2 class="adv-headline">${escapeHtml(d.headline)}</h2>`;
    h += `<p class="adv-diagnostic">${escapeHtml(d.diagnostic)}</p>`;

    // Essential routine
    h += `<div class="adv-card essential"><span class="adv-badge essential">ESSENTIEL</span>`;
    h += `<h3>Ta routine essentielle · ${minSteps.length || 3} étapes</h3>`;
    h += `<p class="adv-card-desc">${escapeHtml(d.minimum_routine && d.minimum_routine.description)}</p>`;
    minSteps.forEach((s) => { h += renderStep(s); });
    h += `</div>`;

    // Boosters
    if (boostSteps.length) {
      h += `<div class="adv-card booster"><span class="adv-badge booster">BOOSTER</span>`;
      h += `<h3>Quand tu veux aller plus loin</h3>`;
      h += `<p class="adv-card-desc">${escapeHtml(d.boosters.description)}</p>`;
      boostSteps.forEach((s) => { h += renderStep(s); });
      h += `</div>`;
    }

    // Evening swap
    if (d.evening_swap) {
      h += `<div class="adv-card small"><h4>🌙 Le soir, ajoute juste ça</h4>`;
      h += `<p class="adv-product"><strong>${escapeHtml(d.evening_swap.brand)}</strong> — ${escapeHtml(d.evening_swap.product)}</p>`;
      h += `<p class="adv-why">${escapeHtml(d.evening_swap.why)}</p>`;
      h += `<p class="adv-how"><em>💡 ${escapeHtml(d.evening_swap.how)}</em></p>`;
      h += `<p class="adv-benefit">→ ${escapeHtml(d.evening_swap.benefit)}</p>`;
      h += `<span class="adv-price">${escapeHtml(d.evening_swap.price)}</span></div>`;
    }

    // Weekly ritual
    if (d.weekly_ritual) {
      h += `<div class="adv-card small"><h4>📅 Une fois par semaine</h4>`;
      h += `<p class="adv-product"><strong>${escapeHtml(d.weekly_ritual.brand)}</strong> — ${escapeHtml(d.weekly_ritual.product)}</p>`;
      h += `<p class="adv-why">${escapeHtml(d.weekly_ritual.why)}</p>`;
      h += `<p class="adv-benefit">→ ${escapeHtml(d.weekly_ritual.benefit)}</p></div>`;
    }

    // Hero ingredient + week-1 tip
    h += `<div class="adv-hero-pill">Ton ingrédient clé : <strong>${escapeHtml(d.hero_ingredient)}</strong><br><span>${escapeHtml(d.hero_ingredient_why)}</span></div>`;
    h += `<div class="adv-tip-box"><strong>💡 Conseil semaine 1</strong><p>${escapeHtml(d.first_week_tip)}</p></div>`;

    // ── BASKETS ──
    h += `
      <div class="adv-baskets" style="margin-top:24px;display:grid;gap:14px">
        <div class="adv-basket adv-basket--min" style="border:1px solid var(--border,#e5e0d8);border-radius:14px;padding:18px;background:#fffaf3">
          <p style="font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:var(--navy,#1f2a44);font-weight:600">Panier prêt</p>
          <h3 style="margin:6px 0 4px;font-size:18px">Ton panier minimum efficace</h3>
          <p style="font-size:13px;color:var(--muted,#888);margin-bottom:10px">3 produits — l'essentiel de ton protocole.</p>
          <p style="font-size:14px;color:var(--navy,#1f2a44);font-weight:500;margin-bottom:14px">Total estimé : ${escapeHtml(d.total_minimum_cost || '—')}</p>
          <button type="button" class="btn-primary" id="sq-add-min" style="width:100%">Ajouter mon panier minimum</button>
        </div>
        <div class="adv-basket adv-basket--full" style="border:1px solid var(--border,#e5e0d8);border-radius:14px;padding:18px;background:#fff">
          <p style="font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:var(--navy,#1f2a44);font-weight:600">Aller plus loin</p>
          <h3 style="margin:6px 0 4px;font-size:18px">Rituel complet</h3>
          <p style="font-size:13px;color:var(--muted,#888);margin-bottom:10px">5 à 7 produits — essentiel + boosters + soir + hebdo.</p>
          <p style="font-size:14px;color:var(--navy,#1f2a44);font-weight:500;margin-bottom:14px">Total estimé : ${escapeHtml(d.total_full_cost || '—')}</p>
          <button type="button" class="btn-outline" id="sq-add-full" style="width:100%">Ajouter le rituel complet</button>
        </div>
      </div>`;

    h += `<div class="adv-costs" style="margin-top:14px"><span>Routine essentielle : ${escapeHtml(d.total_minimum_cost || '—')}</span><span>Routine complète : ${escapeHtml(d.total_full_cost || '—')}</span></div>`;
    h += `<p style="margin-top:16px;font-size:12px;color:var(--muted,#888);text-align:center">Ton protocole détaillé et le mode d'emploi sont en route vers ${escapeHtml(QA.email)}.</p>`;

    rr.innerHTML = h;

    // Wire basket CTAs
    const addMin = document.getElementById("sq-add-min");
    if (addMin) addMin.addEventListener("click", () => addBasket("min"));
    const addFull = document.getElementById("sq-add-full");
    if (addFull) addFull.addEventListener("click", () => addBasket("full"));
  }

  // ── BASKET HAND-OFF ────────────────────────────────────
  // Build cart items from the AI diagnostic and push to SonagiCart.
  function collectBasketItems(mode) {
    const d = LAST_DIAGNOSTIC;
    if (!d) return [];
    const items = [];
    const push = (s) => {
      if (!s || !s.brand || !s.product) return;
      items.push({
        sku:   skuFor(s.brand, s.product),
        brand: s.brand,
        name:  s.product,
        price: s.price || "",
        qty:   1
      });
    };
    (d.minimum_routine && d.minimum_routine.steps || []).forEach(push);
    if (mode === "full") {
      (d.boosters && d.boosters.steps || []).forEach(push);
      push(d.evening_swap);
      push(d.weekly_ritual && {
        brand:   d.weekly_ritual.brand,
        product: d.weekly_ritual.product,
        price:   d.weekly_ritual.price || ""
      });
    }
    // De-dupe by SKU (in case evening_swap repeats a step product)
    const seen = {};
    return items.filter((it) => {
      if (seen[it.sku]) return false;
      seen[it.sku] = true;
      return true;
    });
  }

  function addBasket(mode) {
    const items = collectBasketItems(mode);
    if (!items.length) return;
    const cart = window.SonagiCart;
    if (cart && typeof cart.add === "function") {
      items.forEach((it) => cart.add(it));
    } else {
      // Legacy fallback — push into in-memory array if SonagiCart isn't loaded
      window.cartItems = window.cartItems || [];
      items.forEach((it) => window.cartItems.push(it));
      if (typeof window.renderCart === "function") { try { window.renderCart(); } catch (e) {} }
    }
    close();
    setTimeout(() => {
      if (typeof window.toggleCart === "function") window.toggleCart();
    }, 250);
  }

  // ── EMAIL HAND-OFF (fire-and-forget) ───────────────────
  function sendProtocolEmail(diagnostic) {
    try {
      fetch(ENDPOINT_EMAIL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: QA.name,
          email: QA.email,
          diagnostic: diagnostic,
          answers: snapshotAnswers(),
          locale: "fr"
        })
      }).then((r) => {
        if (!r.ok) console.warn("[SonagiQuiz] send-protocol returned", r.status);
      }).catch((err) => {
        console.warn("[SonagiQuiz] send-protocol failed:", err && err.message);
      });
    } catch (e) {
      console.warn("[SonagiQuiz] send-protocol threw:", e && e.message);
    }
  }

  function snapshotAnswers() {
    return {
      name: QA.name,
      email: QA.email,
      skin_type: QA.skin_type,
      sensitive: QA.sensitive,
      pregnant: QA.pregnant,
      concerns: QA.concerns.slice(),
      age: QA.age,
      lifestyle: QA.lifestyle,
      budget: QA.budget,
      routine_goal: QA.routine_goal
    };
  }

  // ── PUBLIC API ─────────────────────────────────────────
  function open() {
    const modal = ensureModal();
    if (!modal) { console.warn("[SonagiQuiz] #quiz-modal not found in DOM"); return; }
    QA = FRESH_QA();
    QS = 1;
    LAST_DIAGNOSTIC = null;
    buildBody();
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
    showQS(1);
    // Focus first input
    setTimeout(() => { const ni = $("#sq-name"); if (ni) ni.focus(); }, 50);
  }

  function close() {
    const modal = ensureModal();
    if (modal) modal.classList.remove("open");
    document.body.style.overflow = "";
  }

  function init() {
    // Click on overlay backdrop closes modal (matches old behavior)
    document.addEventListener("click", (e) => {
      const modal = ensureModal();
      if (modal && e.target === modal) close();
    });
    // Keyboard: Esc closes, Enter on step 1 advances
    document.addEventListener("keydown", (e) => {
      const modal = ensureModal();
      if (!modal || !modal.classList.contains("open")) return;
      if (e.key === "Escape") { close(); return; }
      if (e.key === "Enter" && QS === 1) {
        // Avoid double-submit if focus is already on a button
        if (e.target && (e.target.tagName === "BUTTON")) return;
        e.preventDefault();
        qNext();
      }
    });
    // Backwards-compat globals so existing inline onclick="openQuiz()" works
    window.openQuiz  = open;
    window.closeQuiz = close;
  }

  window.SonagiQuiz = { init, open, close, state: () => Object.assign({}, QA) };

  // Auto-init on DOM ready (idempotent)
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
