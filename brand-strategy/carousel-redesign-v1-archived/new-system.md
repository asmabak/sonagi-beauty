# Sonagi Beauty Carousel Design System v2

**Supersedes:** ad-hoc execution in rejected May 2026 set.
**References:** `../brand-identity/canva-specs.md` (brand kit source of truth), published winners may01/may02/may03/may05, user QC feedback on week 3.
**Status:** Proposal — awaiting approval on prototype-may15-v2.png before batch rollout.

---

## 1. Canvas and Format

- **Dimensions:** 1080 x 1080 px (square). canva-specs.md originally specified 1080x1350 but production has shipped 1080x1080 consistently — keep what's working.
- **Slides per carousel:** 7 (unchanged).
- **Safe zone:** 80px padding on all 4 edges for text. Never place headline text or kicker within 80px of any edge.
- **Dot indicator row:** Top 40px — 7 small circles, peach for current slide, cream-outline for others. Keep as-is; it's the only consistent visual cue Sonagi owns.

---

## 2. Color Palette (from canva-specs.md)

| Token | Hex | Role |
|---|---|---|
| Navy | #1a2744 | Headlines, primary text, CTA pills |
| Cream | #faf8f5 | Primary background, text on dark photos |
| White | #ffffff | Reserved for text on full photo backgrounds only |
| Peach | #f5c4aa | Single accent (ONE word or number per slide MAX), kickers |
| Peach-L | #fdeee5 | Background gradients, soft bands |
| Rose | #8a6565 | Body text secondary, captions |
| Muted | #8a8a8a | Swipe cue, logo watermark |

**Text overlay opacity rule (photo backgrounds):**
When using a photo as background, apply a navy `rgba(26,39,68,0.55)` overlay across the full canvas so cream/white text hits 7:1 contrast. Published slides already do this — enforce a fixed 55% opacity (not arbitrary per-slide).

---

## 3. Typography System

Pairing locked per `carousel-format-v3` memory: **Georgia (serif) + Arial (sans)**. These are Windows/Mac/Google-safe substitutes for Cormorant Garamond + DM Sans when the generator runs on a local machine. Cormorant/DM Sans only if a designer is working in Canva directly.

| Role | Font | Weight | Size (px) | Color | Example |
|---|---|---|---|---|---|
| H1 — Headline | Georgia | Bold | 72 | Navy or White (on dark) | "La routine K-beauty en 7 étapes." |
| H1 accent word | Georgia | Bold | 72 | Peach | The numeral "7" |
| Kicker | Arial | Bold, letter-spacing 4px, UPPERCASE | 22 | Navy 100% | ROUTINE COMPLÈTE — 7 ÉTAPES |
| Sub-hook | Georgia | Italic | 28 | Rose | "Le squelette de toute routine coréenne." |
| Body | Arial | Regular | 26 | Navy | Regular paragraph text |
| CTA / Swipe | Arial | Medium | 22 | Navy 80% | "Fais défiler pour les 7 étapes →" |
| Logo watermark | Arial | Regular italic | 18 | Muted | "sonagi beauty" bottom-right |

**Rules:**
- H1 is ONE sentence on ONE or TWO lines MAX. Never 3+ line headline stacks. If headline won't fit in 2 lines at 72px, shorten the headline.
- Peach accent limited to ONE word or number per slide. Never 50% of the headline in peach — that creates two competing focal points.
- Line-length: 18–24 characters per line for H1 (optical optimum in serif at this size). Body: 55–65 characters per line.
- Letter-spacing: only on kicker (4px). Never on H1 or body.
- French quality: ALL accents required (é è ê à ç ô û î ï). Run a mandatory accent-check pass before render. Reject any output with franglais inventions like "peau prête pas trempée".

---

## 4. Composition Grid (1080x1080)

```
┌─────────────────────────────────┐ y=0
│ •  ·  ·  ·  ·  ·  ·             │ y=40  dot row
│                                 │
│      [KICKER SMALL CAPS]        │ y=100  kicker
│                                 │
│   Headline serif                │ y=200  H1 block (2 lines max)
│   fits in 18–24 chars wide      │ y=280
│                                 │
│          ─                      │ y=400  4px peach divider, 80px wide
│                                 │
│   Italic sub-hook, one line     │ y=450  sub-hook
│                                 │
│   [SLOT: face photo / texture / │ y=540  main visual OR solid
│        illustration]            │         up to y=860
│                                 │
│                                 │
│   Fais défiler → (swipe cue)    │ y=940
│                                 │
│                     sonagi bty  │ y=1020  logo
└─────────────────────────────────┘ y=1080
```

**Slots:**
- y=0–40: dots
- y=80–160: kicker block
- y=180–360: headline block (H1)
- y=400–420: peach divider
- y=440–500: sub-hook
- y=540–860: main visual zone (photo with 55% navy overlay, OR solid cream, OR peach-L gradient)
- y=900–980: swipe cue
- y=1000–1050: logo watermark

**Variant A (Photo cover, like may03, may05):** Main visual zone extends from y=0 to y=1080 (full-bleed) with navy 55% overlay. Kicker/H1/sub sit on top.
**Variant B (Solid cover, like prototype-may15-v2):** Cream background full-bleed. A peach-L gradient band from y=540 to y=860 holds an abstract shape or icon. No photo. Best when no safe photo exists (banned products).
**Variant C (Split, like canva-specs.md slide 2):** Upper half solid navy, lower half cream with peach divider. Use for contrast comparisons (peau mouillée vs peau sèche).

---

## 5. Product Photography Policy (ENFORCED)

> **Any product shown in a Sonagi carousel must be (a) in the confirmed resale catalog with supplier agreement signed, OR (b) visually unbranded — labels removed/flipped/blurred, or photographed as texture only. Competitor brand photography is BANNED until signed agreements exist.**

**Banned until resale agreements signed:**
The Ordinary, iUnik, COSRX, Mizon, Centella / SKIN1004, Cos De BAHA, Anua, Banila Co, Beauty of Joseon, Torriden, Laneige, Innisfree, Sulwhasoo, and any other third-party K-beauty / generic skincare brand whose packaging is identifiable on camera.

**Always safe (use these):**
- Skin/hand close-ups applying product
- Faces (eyes, lips, jaw) in natural light
- Ingredient shots: centella leaves, snail mucin swirls, rice grains, fermented tea, ginseng root, propolis amber
- Texture shots: serum drops on glass, cream swirls on palm, water beads on skin, oil ribbons
- Unbranded glass/amber bottle silhouettes (stock photography where label is removed or dropper is close-up only)
- AI-generated (Nano Banana, Seedance 2.0 refs) textures with explicit no-brand-label instruction

**Case-by-case (verify first):**
- Mint/green coordinated bottle sets (like may20). If ANY label is readable at 1080px, reject and regenerate.
- User's own photographed inventory once suppliers are on file.

---

## 6. Slide-to-Slide Consistency

**Cover (slide 1):** Variant A or B. One sentence headline. One peach accent. Kicker frames topic. Sub-hook sets up the payoff.

**Content slides (slides 2–6):** Switch to cream background (cleaner for dense info). Same H1 pattern (one-block headline) at top. Body uses numbered pills (1–4 max visible per slide) or side-by-side split comparisons. **Fill the grid — if bottom 30% is empty, content is under-designed.** Add an illustration, a gold tip box, or a Korean proverb in Noto Sans KR. Never leave y=700–y=1020 blank.

**CTA slide (slide 7):** Variant A photo cover with smiling face. Copy: "Retrouve la routine complète sur sonagibeauty.com" + "Lien en bio 🌸". Navy CTA pill at y=780 with peach border.

Consistency checks across a 7-slide set:
- Dot-row position identical on every slide (y=40).
- Logo watermark identical position (bottom-right, y=1020).
- Kicker letter-spacing identical on every slide.
- Peach accent used max once per slide; max twice across the full 7-slide set (otherwise peach fatigue).
- No slide has more than 50 total words.

---

## 7. "Do vs Don't" Reference (ASCII)

**DO — published may03 pattern (one-block headline):**
```
         K-BEAUTY ROUTINE               ← kicker, high contrast
                                        
    Frotter = rides.                    ← H1 one sentence
    Tapoter = glass skin.                 two lines, single color
                                        
              ─                         ← peach divider
                                        
    La différence entre une peau        ← sub-hook italic
    terne et une peau lumineuse.
```

**DON'T — rejected may12 pattern (fragmented headline):**
```
        SONAGI BEAUTY                   ← no topic kicker
                                        
     L'ingrédient                       ← H1 line 1, white medium
                                        
        secret.                         ← H1 line 2, peach HUGE
                                          (two competing focal points)
              ─                         
                                        
    Dont personne ne parle encore.      ← vague, unverifiable
```

**DO — prototype-may15-v2 pattern (solid cover, one accent):**
```
         ROUTINE COMPLÈTE — 7 ÉTAPES    ← kicker, letter-spaced
                                        
    La routine K-beauty en              ← H1 navy, one sentence
           7 étapes.                    ← "7" only in peach
                                        
              ─
                                        
    Le squelette de toute routine       ← sub-hook italic rose
         coréenne.
                                        
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░         ← peach-L gradient band
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░           (decorative, no brands)
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░
                                        
    Fais défiler pour les 7 étapes →
                                        
                         sonagi beauty
```

**DON'T — rejected may15 pattern (brand logo field + stacked peach):**
```
         SONAGI BEAUTY                  
         ROUTINE COMPLÈTE               ← muted peach, invisible
                                        
    Routine                             ← H1 line 1
    complète                            ← line 2
    7 étapes                            ← line 3 peach
              ─
    Moins de 80 euros. Chaque...        ← conflicts with may21 claim
                                        
    [The Ordinary | iUnik | Centella |  ← LEGAL RISK
     Mizon | Cos De BAHA — all visible]
```

---

## 8. Batch Regeneration Workflow (next session)

1. Load this new-system.md + diagnosis.md into context.
2. For each rejected carousel, regenerate slide 1 using Variant A (photo-safe) or Variant B (solid) depending on whether a safe background image exists.
3. Audit slides 2–6 for the real-estate waste rule (fill y=540–y=1020 or add visual weight).
4. Audit every caption for accent / franglais / jargon / unverifiable claims.
5. Replace any slide containing the banned serum shelf photo.
6. Export as `slide-1-v2.png`, `slide-2-v2.png`, etc. into the same rejected folder so git diff is reviewable.
7. Present a grid of old-vs-new to the user for final QC before moving to `/published/`.

Expected work: ~70 slides. Expect 2 Claude sessions, batched in parallel by day.
