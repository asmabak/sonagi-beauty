# Sonagi — Site Taxonomy + SEO Strategy (2026-05-14)

Three problems this doc solves:
1. URL params (`?cat=`, `?concern=`, `?brand=`) currently use inconsistent vocabularies across pages.
2. SEO metadata varies per page — some have rich Open Graph + JSON-LD, some have minimal.
3. There is no single source of truth for "what categories exist on the site."

This is a **strategy doc**. The concrete changes at the bottom are prioritized for implementation in subsequent sessions.

---

## 1. The taxonomy (single source of truth)

Every piece of content (product, blog post, masterclass, glossary entry, concern, ingredient) gets tagged on these six dimensions. **Tag values are locked** — do not invent new ones outside this list without updating this doc.

### A. Product Category (`?cat=`)
The shelf the product sits on. **One value per product.**

| Slug | French label | English label |
|---|---|---|
| `nettoyant` | Nettoyant | Cleanser |
| `toner` | Toner | Toner |
| `exfoliant` | Exfoliant / Gommage | Exfoliant / Scrub |
| `essence` | Essence | Essence |
| `serum` | Ampoule / Sérum | Ampoule / Serum |
| `contour-yeux` | Contour des Yeux | Eye care |
| `creme` | Crème Hydratante | Moisturiser |
| `spf` | Crème Solaire | Sun care |
| `masque` | Masque à Rincer | Rinse-off mask |
| `masque-tissu` | Masque en Tissu | Sheet mask |
| `levres` | Lèvres | Lips |
| `teint` | Teint | Complexion |
| `yeux-maquillage` | Yeux | Eyes (makeup) |
| `cheveux-soin` | Soin cheveux | Hair care |
| `corps` | Corps | Body |

### B. Skin Type (`?type=`)
**Multi-value allowed** (a product can suit oily + sensitive).

| Slug | French | English |
|---|---|---|
| `peau-grasse` | Peau Grasse | Oily |
| `peau-seche` | Peau Sèche | Dry |
| `peau-mixte` | Peau Mixte | Combination |
| `peau-normale` | Peau Normale | Normal |
| `peau-sensible` | Peau Sensible | Sensitive |

### C. Concern (`?concern=`)
What the visitor came to solve. **Multi-value allowed.**

| Slug | French | English | Korean |
|---|---|---|---|
| `acne` | Acné active | Active acne | 트러블 |
| `pores` | Pores dilatés / Points noirs | Large pores / blackheads | 모공 |
| `eclat` | Teint terne / Hyperpigmentation | Dull skin / hyperpigmentation | 광채 |
| `taches` | Taches & post-acné | Spots & post-acne | 잡티 |
| `hydratation` | Déshydratation | Dehydration | 수분 |
| `anti-age` | Rides & Élasticité | Wrinkles & elasticity | 탄력 |
| `anti-rougeurs` | Rougeurs & Inflammations | Redness & inflammation | 진정 |
| `barriere` | Barrière endommagée | Damaged barrier | — |
| `sebum` | Excès de sébum | Excess sebum | 피지 |
| `sensibilite` | Sensibilité & rougeurs | Sensitivity & redness | 진정 |

### D. Brand (`?brand=`)
Single-value, slug = lowercased brand name with dashes.

`cosrx`, `beauty-of-joseon`, `mixsoon`, `skin1004`, `glow-recipe`, `huxley`, `iunik`, `anua`, `round-lab`, `laneige`.

### E. Korean Concept (tag, no URL param)
Editorial tag for content (blog / glossary / masterclass), not for product filtering.

`glass-skin`, `7-skin-method`, `slugging`, `double-cleansing`, `essence-layering`, `chok-chok`, `mool-gwang`, `K-beauty-10-step`, `hanbang` (traditional herbal).

### F. Ritual Step (no URL param, used in routine builder)
Maps to the consultation slot keys. Read-only for the buy flow.

`cleanser`, `toner`, `essence`, `serum`, `eye`, `moisturiser`, `spf`, `mask`, `treatment`.

---

## 2. URL pattern rules

### Catalog pages (skincare / maquillage / haircare)
- Single filter: `?cat=serum`
- Combined filters: `?cat=serum&concern=acne` (always alphabetical key order)
- Brand filter: `?brand=cosrx` (no `?cat=` needed)
- Always lowercase, always dash-separated, **never accents or special chars**.

### Product pages
- `/produit.html?sku=cosrx-snail-96-mucin-essence` — locked SKU per product.
- All slug-style, no IDs. SEO-friendly + shareable.
- Future migration: `/produit/cosrx-snail-96-mucin-essence` (pretty URL via Netlify redirect rule).

### Concern landing pages
- `/skincare.html?concern=acne` — should redirect/canonical to a real landing page once authored: `/concerns/acne` (future).

### Korean-concept landing pages
- `/journal.html?tag=glass-skin` — same future migration: `/concepts/glass-skin`.

---

## 3. SEO baseline — what every page must have

### A. Mandatory meta (currently missing or inconsistent on some pages)
- `<title>` — formula: `{page-specific topic} · Sonagi Beauty`. Max 60 chars.
- `<meta name="description">` — 150–160 chars, French-first, includes one primary keyword + one secondary.
- `<link rel="canonical">` — every page needs an absolute https URL.
- `<meta property="og:type">` — `website` for home/landing, `product` for `/produit`, `article` for journal posts.
- `<meta property="og:image">` — 1200x630, branded, NOT a stock photo. **Most pages currently inherit a generic image; needs per-page art.**
- `<meta name="theme-color">` — locked to `#FF3E9D` (done this session).

### B. Structured data (JSON-LD)
- **Site-wide:** `Organization` + `WebSite` (currently on home only; should be on every page).
- **Product pages:** `Product` schema with `offers`, `aggregateRating`, `brand`, `category`, `image`. Currently missing entirely.
- **Catalog pages:** `CollectionPage` + `ItemList` referencing each product.
- **Journal posts:** `Article` with `author`, `datePublished`, `image`.
- **Masterclasses:** `Event` with `startDate`, `location` (Online vs in-person), `offers`.
- **Glossary entries:** `DefinedTerm` inside a `DefinedTermSet`.
- **Breadcrumbs:** `BreadcrumbList` (added on 18 pages by commit `8da8de0` on the abandoned site-corrections-v2 branch — needs porting forward to the live baseline).

### C. Hreflang (FR/EN)
The site uses inline `data-fr` / `data-en` for live language switching, so it doesn't have separate URLs per language. This is **not SEO-optimal** for English — Google sees only the French text.

**Decision needed:**
- (a) Keep single URL, single page, inline switch — fastest, weakest English SEO.
- (b) Add `?lang=en` param + render English server-side via Netlify edge function — middle ground.
- (c) Migrate to `/en/` URL subtree — strongest SEO but requires building all English pages.

Recommend **(b)** for v2: the Netlify edge function can serve the same HTML but pre-swap `data-fr` → text content based on `?lang=en` so crawlers see English text. Low effort, big SEO win.

### D. Sitemap.xml
- Currently: not checked. **Action: verify exists at `/sitemap.xml`**. If missing, add one listing every public HTML page with priority + changefreq.
- Add `<lastmod>` so search engines re-crawl after updates.

### E. robots.txt
- **Action:** verify the live `/robots.txt` exists and does NOT block `/consultation.html` (the new diagnostic page must be indexable for SEO).

---

## 4. Site-wide design-system performance contract

The "fastest possible mobile load" target the founder asked for. Use these as acceptance criteria for any new component.

### Page weight budgets (first-visit, gzip)
| Asset class | Budget per page | Current (~) | Status |
|---|---:|---:|---|
| HTML | < 50 KB | 35–65 KB | ✅ |
| CSS (sonagi.css shared) | < 80 KB | ~60 KB | ✅ |
| Above-the-fold JS | < 30 KB | ~13 KB (sonagi-app.js) | ✅ |
| Below-the-fold JS (deferred) | n/a | ~33 KB (quiz) + ~515 KB (quiz imgs) | ⚠️ quiz-imgs is huge — needs splitting |
| Hero image | < 200 KB | varies | ⚠️ some are 100–200 KB, ok |
| Hero video poster | < 200 KB | 70–150 KB | ✅ |
| Hero video (first slide) | < 5 MB | 3.3 MB (marshmallow-web.mp4) | ✅ (this session) |
| Hero videos (slides 2+) | preload="none" + poster | ✅ | (this session) |

### Quick wins (do in next session)
1. **Split `sonagi-quiz-imgs.js` (515 KB)** — currently bundles all quiz placeholder product images as base64. Since the consultation page is now the real quiz, this file is mostly dead weight. Either delete it or strip down to only the placeholders that `produit.html` + `panier.html` still reference.
2. **Convert PNG → WebP** for `files/images/visuals/*.png` — current heaviest is `sonagi-blog_men2.png` at 92 KB; WebP would be ~30 KB.
3. **Preconnect to fonts.gstatic.com** is already there. Add `<link rel="preload" as="font" ...>` for the Fraunces weight that's used in the hero (`weight: 300`) to shave first-paint by 100–200ms.
4. **Inline critical CSS for the hero** — first ~5 KB of `sonagi.css` (.carousel-wrap, .c-slide, .trust-row) inlined in `<head>` means hero paints before the rest of `sonagi.css` arrives.

### Long-term wins
- Move from raster product images to art-directed `<picture>` + `srcset` (mobile 320w / 640w / desktop 1280w).
- Service worker for offline / repeat-visit cache.
- Drop the global font fallback chain to a single web font (currently uses 3 — Fraunces, DM Sans, Noto Sans KR).

---

## 5. Concrete changes — prioritized for next session

### P0 (ship before launch)
1. Add `BreadcrumbList` JSON-LD to all 19 pages (port from the abandoned `claude/site-corrections-v2` branch commit `8da8de0`).
2. Add `Product` schema to `produit.html`.
3. Verify `/sitemap.xml` and `/robots.txt` exist + are valid.
4. Strip or split `sonagi-quiz-imgs.js` (515 KB → likely < 50 KB after audit).
5. Replace the empty `og:image` defaults on every page that lacks one.

### P1 (within 2 weeks of launch)
6. Wire English `?lang=en` server-side via a Netlify edge function (so crawlers see English text).
7. Convert top 10 product placeholder PNGs to WebP.
8. Add `CollectionPage` + `ItemList` schema to catalog pages.
9. Migrate `?concern=X` → `/concerns/X` real landing pages (better SEO, dedicated content).

### P2 (post-launch optimization)
10. Service worker for offline support + repeat-visit caching.
11. Migrate `/produit.html?sku=X` → `/produit/X` pretty URLs.
12. Author Korean-concept landing pages at `/concepts/glass-skin`, `/concepts/7-skin-method`, etc.

---

## 6. One-time housekeeping

- Decide canonical case for category slugs: lowercase only (current behavior on most links, but a few use mixed case). Lock as **lowercase-only, dash-separated**.
- Audit all internal anchors for trailing `.html` consistency. Netlify pretty-URLs already serve both, but pick one and stick to it for canonical/sitemap clarity.
- Add a `LAST-UPDATED` marker per page (in `<meta>` or via build) so the sitemap `<lastmod>` is accurate.
