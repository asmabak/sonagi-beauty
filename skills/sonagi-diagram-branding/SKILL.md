---
name: sonagi-diagram-branding
description: Exact visual branding for Sonagi explainer/infographic diagrams (the hand-drawn cream-and-pastel "WHY WE DO THIS" doodle style). Use whenever generating, regenerating, or critiquing a Sonagi concept diagram so every output matches the established brand exactly. Build the image prompt from the Locked Spec below; best tool is nano_banana_pro at 4:3.
---

# Sonagi Diagram Branding

Summary: the locked visual identity for Sonagi's hand-drawn explainer diagrams (architecture, concept, and how-it-works infographics for LinkedIn and decks). Apply this spec verbatim to every diagram so the set looks like one hand. When to touch: only Asma changes the brand; everyone else copies it.

## Index
- When to use
- Locked spec (paste into every prompt)
- Content rules
- Exact-match upgrade (reference image)

## When to use
Any time you generate, regenerate, or critique a Sonagi diagram or infographic. Build the prompt from the Locked Spec. Tool: `nano_banana_pro` (Gemini 3 Pro Image) for accurate text rendering. Aspect ratio: `4:3`.

## Locked spec (paste into every prompt)
- **Medium:** hand-drawn doodle / line-art editorial illustration. Thin, slightly sketchy charcoal-navy outlines with a warm hand-drawn quality (NOT crisp flat vector). Tiny decorative hand-drawn sparkle and swirl accents float near some icons.
- **Background:** warm cream / ivory (about #F6EFDF), uniform, no gradient.
- **Fill palette** (soft desaturated pastels, used as flat partial fills INSIDE the black linework, sparingly, with lots of cream negative space): sage / eucalyptus green (#A9C4A0), dusty rose / mauve (#C9A1A6), soft peach / apricot (#EFC39C), muted terracotta / clay (#D69A78).
- **Ink and text colour:** soft dark navy / charcoal (#2C2C44).
- **Typography:** ALL CAPS throughout. Title = bold rounded geometric sans, large, centered. Subtitle = smaller, regular weight, centered, may use small dot separators or an underline accent on key words. Labels and the numbered body = medium-weight caps. Always legible, spelled exactly as written.
- **Status checks (when a layout uses them):** a soft pastel CIRCLE (alternate green / pink / peach / green) behind a hand-drawn check mark, one above each item.
- **"WHY WE DO THIS" box:** a rounded-rectangle with a thin navy outline across the bottom, with a small centered PILL-shaped tab on its top edge reading `WHY WE DO THIS`. Numbered lines inside, caps, navy.
- **Icons:** simple but characterful line-art with pastel fills: cute smiling robots, a safe/vault with a dial, a floppy disk, labeled file folders, a shield, an ID badge on a lanyard, an open padlock joined to a plug, a NOW sticky note, a vault of CORE/RECALL/ARCHIVAL drawers, a cracked monitor, a disc with a calendar, a gauge with a dollar sign, stacked layers with a recycle arrow.
- **Layouts:** (a) a four-icon row with checks; (b) two columns CHALLENGE -> SOLUTION with arrows; (c) a descending staircase with a SAVINGS arrow down the left. Generous whitespace, calm, balanced.
- **Mood:** warm, friendly, premium but approachable, editorial. Never corporate-flat, never neon, never busy.

## Content rules
- No em dashes anywhere (Sonagi rule). Use commas, periods, colons, parentheses.
- Proper technical vocabulary, but every term carries enough plain context for a non-technical LinkedIn reader.
- When showing choices, separate `WE CHOSE` (full colour) from `WE SKIPPED (FOR NOW)` (greyed, dashed, small X). These are deliberate design choices, not a build-status tracker.

## Exact-match upgrade (reference image)
For a pixel-faithful match, pass an original Sonagi diagram to `nano_banana_pro` as a reference image (`medias` role=reference) alongside the prompt. Chat-attached images cannot be written to disk directly, so Asma drops the originals into `media/reference visuals/` first, then they are uploaded via `media_upload` and referenced.
