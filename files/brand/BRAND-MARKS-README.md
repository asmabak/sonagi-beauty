# Sonagi Beauty — Brand Marks

Editorial wordmark and monogram system. All assets are SVG, scale-independent, and use only the brand palette.

---

## Files in this folder

| File | viewBox | Use case |
|------|---------|----------|
| `sonagi-wordmark.svg` | 400×90 | Primary lockup — site header, email signature, light backgrounds |
| `sonagi-wordmark-reverse.svg` | 400×90 | Reverse lockup — announcement bar, footer, navy backgrounds |
| `sonagi-mark.svg` | 100×100 | Monogram (S + raindrop) for square contexts, social avatars, watermarks |
| `favicon.svg` | 32×32 | Browser tab icon — modern browsers prefer SVG favicons |
| `apple-touch-icon.svg` | 180×180 | iOS home-screen icon when user adds to home screen |

---

## Brand palette (single source of truth)

| Token | Hex | Use |
|-------|-----|-----|
| `--navy` | `#1a2744` | Primary — wordmark, monogram, body text |
| `--cream` | `#faf8f5` | Backgrounds, reverse type |
| `--peach` | `#f5c4aa` | Accent only — raindrop, 소나기 glyph, decorative dots |
| `--rose` | `#8a6565` | Rare warm secondary, NEVER as primary |

---

## When to use each variant

### Primary wordmark — `sonagi-wordmark.svg`
- Default lockup on cream / white / light photo backgrounds
- Site header, blog post headers, press kit, business cards
- The 소나기 Korean glyph is part of the lockup — do not strip it

### Reverse wordmark — `sonagi-wordmark-reverse.svg`
- Whenever the background is navy or a dark photo
- Announcement bar, footer, navy promo blocks, dark hero imagery
- 소나기 stays peach — it remains the brand accent

### Monogram — `sonagi-mark.svg`
- Square contexts only: Instagram avatar, watermark on UGC, sticker, app icon hero
- The raindrop above the italic S references 소나기 ("sudden summer rain")
- Always shows S in navy + drop in peach — never invert the raindrop color

### Favicon — `favicon.svg`
- Linked in `<head>`. Modern browsers (Chrome, Firefox, Safari, Edge) all support SVG favicons
- Path-drawn S (no font dependency) so it renders identically across all OSes

### Apple touch icon — `apple-touch-icon.svg`
- For iOS Safari "Add to Home Screen"
- Has a built-in navy background (iOS does not auto-fill)
- If you need PNG fallbacks for older iOS, export this at 180×180 and 192×192

---

## Minimum sizes (DO NOT go smaller)

| Asset | Minimum |
|-------|---------|
| Wordmark (primary or reverse) | 120 px wide |
| Monogram | 24 px square |
| Favicon | renders at 16 / 32 / 48 px — already optimized |

Below these sizes the tracked-out letterspacing and the 소나기 glyph become illegible.

---

## Clear space rule

Around any wordmark, leave clear space equal to **one cap-height of the "S" in SONAGI** on all four sides. No competing elements (icons, text, lines, photos) inside that buffer.

For the monogram, leave clear space equal to **half the canvas size** (so a 100 px monogram needs 50 px of breathing room around it).

---

## Color usage rules

1. **Default:** navy on cream — use this 80% of the time
2. **Reverse:** cream on navy — use for announcement bars, footers, dark hero overlays
3. **Peach is an ACCENT only.** Never set the full wordmark in peach. Never use peach for body text.
4. **Rose is reserved** for warm secondary moments (e.g., journal pull-quotes). Never as a primary mark color.
5. **Never put the wordmark on a colored background other than navy.** No peach background, no rose background, no off-brand color.

---

## File-format guidance

- **Web:** always use these SVGs. They scale infinitely and have zero font dependency on the client (the wordmark uses Fraunces from Google Fonts which the site already loads; the favicon and apple-touch-icon use path-drawn glyphs and need no font).
- **Raster export needed?** (Instagram bio photo, app store icon, print) Open the SVG in any browser at 4× the target pixel density and screenshot, or use a one-off CLI like `rsvg-convert -w 1024 sonagi-mark.svg -o sonagi-mark@1024.png`.
- **Never re-typeset the wordmark in another tool.** If you need a one-off layout (e.g., a partner ad), use the SVG as-is and resize.

---

## Embedding snippets

### In the site nav (Phase 3)

```html
<a href="/" class="nav-brand" aria-label="Sonagi Beauty — Accueil">
  <img src="/files/brand/sonagi-wordmark.svg"
       alt="Sonagi Beauty"
       width="200" height="45"
       loading="eager" decoding="async">
</a>
```

### In the announcement bar (reverse)

```html
<img src="/files/brand/sonagi-wordmark-reverse.svg"
     alt="Sonagi Beauty"
     width="140" height="32"
     loading="eager" decoding="async">
```

### In `<head>` for favicon + iOS

```html
<link rel="icon" type="image/svg+xml" href="/files/brand/favicon.svg">
<link rel="apple-touch-icon" href="/files/brand/apple-touch-icon.svg">
<link rel="mask-icon" href="/files/brand/sonagi-mark.svg" color="#1a2744">
<meta name="theme-color" content="#1a2744">
```

---

## V2 polish roadmap (future)

These v1 marks are production-ready but lean on Fraunces from Google Fonts for the wordmark. To level up:

1. **Commission a custom Fraunces variant** — pay Undercase Type to draw a one-off tracked SONAGI lockup with optical adjustments to the SO and AG kerning pairs and a custom "G" terminal. Outline the result and ship as `sonagi-wordmark-v2.svg` with zero font dependency. Budget: ~€800–1,500.
2. **Hand-letter the wordmark** — hire a French letterer (e.g., from Paris-based studios like Akatre or Atelier Müesli) to draw a true bespoke wordmark. This becomes the brand asset and is trademark-able. Budget: €2,500–6,000.
3. **Motion variants for the hero** — animated SVG of the raindrop falling and dispersing into the wordmark on first page load. ~5 KB Lottie or SMIL. Budget: 1 day of designer time.
4. **Korean monogram alternate** — a `소` mark for Korean-language touch points (international expansion). Same raindrop language, but the Korean glyph is the lockup.
5. **Embossed / foil print spec sheet** — once the wordmark is finalized, document the gold-foil and blind-emboss specs for press kits, packaging inserts, and unboxing experiences.
6. **Sound logo** — three-note signature (rain → silence → soft chime) for video content end-cards. ~€500 from a French sound designer.
