# Sonagi — CTA & Friction Audit (2026-05-14)

Stated objective (founder): **the only purpose of this website is to trigger sales. Every section must either attract or direct, with the shortest possible purchase path and minimum friction.**

This audit measures every page against that single test. Findings are ranked by impact on the path to purchase.

---

## Site-wide counts (CTA-class elements per page)

| Page | CTA count | Note |
|---|---:|---|
| `index.html` | 37 | Homepage. Has the most justifiable spread (multiple sections). |
| `skincare.html` / `maquillage.html` / `haircare.html` | 25 each | Catalog pages — count is healthy if 1 per product card. |
| `produit.html` | **17** | ⚠️ Product detail page. **Should be 2–3, not 17.** |
| `panier.html` | **16** | ⚠️ Cart page. The user is already mid-purchase; should be **1 dominant CTA** + remove. |
| `rewards.html` | 15 | OK |
| `masterclasses.html` | 10 | OK |
| `marques.html` | 9 | OK |
| `glossaire.html` | 8 | OK — but most are nav, see below. |

**Pattern:** the two pages closest to a purchase (`produit`, `panier`) have the **most competing CTAs**. Inverted funnel. This is the highest-leverage fix on the site.

---

## P0 — High-impact, ship before launch

### 1. `produit.html` — collapse to a single "Add to basket"
**Symptom:** 17 CTA-class elements on a page whose only job is "convince + buy."
**Likely culprits:** quiz nav button x2 (nav + mobile menu), product thumbnails x4 (image switcher, not real CTAs but styled like them), tab buttons (description / reviews / ingredients), "is this product right for my skin?" → quiz, related-products carousel buttons, footer CTAs.

**Concrete changes:**
- Make "Ajouter au panier" the only `.btn-primary` on the page. Everything else demotes to text-link or `.btn-ghost`.
- Move "Ce produit est-il fait pour ma peau ? → Faire le quiz" (currently `.prod-quiz-cta` near line 377) **below** the add-to-basket fold. It's a secondary path, currently competing for attention with the buy button.
- Remove the "quiz-nav-btn" duplication in the desktop nav for this page only — visitor already lands on a product, they don't need the quiz primary CTA in the chrome.

### 2. `panier.html` — one button, one job
**Symptom:** 16 CTA-class elements on a checkout page. Visitor came here to pay, not to browse.
**Already fixed this session:** rendered the real cart from `sonagi_cart_v1` instead of placeholder rows, so the page now reflects the visitor's actual basket.

**Concrete changes still needed:**
- Hide the main nav's quiz CTA on this page (same logic as produit.html).
- Remove or hide the "Masterclasses" / "Journal" / "Rewards" links from the page chrome — pure distractions when the user is mid-checkout. Keep only "Logo → home" and the basket-summary aside.
- The "Notify me at launch" button currently lives below the form — until `SHOP_OPEN=true`, it should be the **single dominant CTA at the top** of the right rail, replacing the disabled checkout button visually.
- Add an explicit "← Modifier mon panier" link at the top so visitors can edit, then return.

### 3. Hero — one primary CTA per slide, no competing buttons
**Symptom:** every hero slide currently shows two equally-weighted buttons ("Diagnostique ma peau →" + "Ma routine") that route to the same place (`/consultation.html`). Visual noise; user has to read twice.

**Already fixed this session:** the hero CTA was upgraded from `href="#"` + `onclick` to a real `/consultation.html` link.

**Concrete change still needed:**
- Drop the second button. Slide 1 keeps "Diagnostique ma peau →" as the only CTA. Slide 2 ("Voir les SPF") and Slide 3 ("Peaux sensibles") keep one CTA each. The "Ma routine" duplicate everywhere comes out.

### 4. Concerns tiles — confirm they actually convert
**Status:** moved to a position **after** brand-belt this session (was gating products). Still need to verify each tile's destination is the right SERP.

**Concrete check:** every `.concern-tile` href is `skincare.html?concern=X`. Open each `skincare.html?concern=acne` etc. and confirm the listing actually filters. If filter is not implemented, tiles are decorative — top P0 fix.

---

## P1 — Tighten secondary CTAs

### 5. Newsletter strip ("Préviens-moi")
- Appears in three places on `index.html`: prelaunch banner (top), `#newsletter` section, footer. That's fine for pre-launch but **rephrase** them so they're not identical. Top banner = urgency ("Lancement bientôt"); newsletter section = value ("15% de bienvenue + accès anticipé aux drops"); footer = catch-all.

### 6. "Toutes nos marques →" in `brand-belt-section`
- Healthy single CTA, links to `/marques.html`. Keep as-is.

### 7. Masterclasses "Réserver" — pre-launch handling
- Each event card has a `.evt-reserve` button. Currently styled as primary but **what happens when you click it?** If nothing (placeholder), demote to "Bientôt disponible" badge. If a Calendly/Eventbrite link, keep primary. **Verify.**

### 8. "Voir tout" links on tabbed product grid
- The "Nouveautés" + "Best-Sellers" tabs each have a "Voir tout →" link to `/skincare`. Good. Just confirm the tabs themselves don't visually compete with the CTAs inside the cards.

### 9. Floating "Add to basket" on product cards
- Each `.prod-card` has a hover-state `.prod-add-btn` that says "Voir le produit." Misleading — it sounds like add-to-cart but routes to product page. **Rename to "Voir →"** so it doesn't compete with real cart actions.

---

## P2 — Friction smells worth fixing soon

### 10. Mobile menu noise
- `closeMobileMenu()` is called on every menu click. The mobile drawer has Skincare/Maquillage/Haircare nested categories, then Masterclasses/Journal/About/Glossaire/Rewards/FAQ/Mentions. **8+ destinations is too many** for mobile-first commerce.
- Pre-launch priority: keep La Boutique (with skincare/maquillage/haircare sub-items), Masterclasses, Mon compte, FAQ. Move Journal, Glossaire, Rewards under a "Plus" collapse.

### 11. Footer CTAs
- Footer has 30+ links. Acceptable for SEO juice but **no soft conversion CTAs** at the bottom of the footer (e.g., "Pas encore inscrite ? 15% de bienvenue"). Add one cream-card right above the legal links.

### 12. About page hero CTA
- `about.html:613` has "Trouver mon rituel" with a defensive `if(typeof openQuiz==='function')openQuiz()` handler — that's stale (we replaced the modal with a real page). Upgrade to a real `<a href="/consultation.html">` like the homepage hero CTAs.

### 13. Confirmation page (post-purchase)
- The confirmation page should be a **second sales pitch**: "votre commande est validée" + "tu pourrais aimer aussi" cross-sell + share-to-Instagram referral. Currently we have nav, basket icon, footer — no second-pitch upsell.

---

## P3 — Polish

- Every `<button>` with an inline `onclick="..."` should be re-checked for accessibility (`aria-label` on icon-only buttons, `type="button"` on non-form buttons).
- The hero slide 1 CTA was upgraded this session; sweep slides 2 + 3 for the same upgrade.
- "Bientôt disponible" used inconsistently. Pick one phrase for pre-launch and use it everywhere.

---

## Single most-leverage change

If only one thing ships from this audit before launch: **fix `produit.html` to have one primary CTA (Add to basket / Notify me) and demote everything else.** Product page → cart conversion rate compounds with every visitor.
