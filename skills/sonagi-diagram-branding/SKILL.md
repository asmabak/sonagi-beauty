---
name: sonagi-diagram-branding
description: Exact visual branding for Sonagi explainer/teaching diagrams (the warm-cream fine-liner "WHY WE DO THIS" editorial style). Use whenever generating, regenerating, or critiquing a Sonagi concept diagram so every output matches the established brand exactly. Build the image prompt from the Recipe below; best tool is nano_banana_pro at 4:3.
---

# Sonagi Diagram Branding

Summary: the locked visual identity for Sonagi's hand-lettered teaching diagrams (architecture, concept, how-it-works infographics for LinkedIn and decks). Apply this recipe verbatim so the set looks like one hand. When to touch: only Asma changes the brand; everyone else copies it.

## Index
- The look in one line
- Hard style rules (the negatives matter most)
- Prompt recipe (paste and fill)
- Content rules

## The look in one line
Delicate editorial line-art teaching diagram, fine-liner technical illustration on warm cream paper, drawn with warmth and friendly detail, very clear and very simple, easy enough for a child to follow at a glance. Thin precise DARK-INK line-drawing icons, each with a SUBTLE soft pastel accent. Crisp legible hand-lettered all-capitals, magazine quality.

## Hard style rules (the negatives matter most)
- **Ink:** thin precise DARK INK line drawing (charcoal/black). NOT navy.
- **Accents:** subtle soft pastel accents only, used SPARINGLY: sage green, dusty rose, peach.
- **Background:** warm cream paper ground.
- **Lettering:** hand-lettered ALL CAPITALS, crisp, legible, magazine quality, identical fine-liner sketchbook style.
- **Layout:** organised, airy, lots of cream space. A bottom thin rounded-rectangle box headed `WHY WE DO THIS` with short numbered lines.
- **NEVER:** no solid fills, no navy, no grey, no white anywhere, no flat-vector look, no busy clutter.
- Always end the prompt by enumerating the EXACT text strings ("The text in the image is exactly these strings, spelled exactly, and nothing else: ...") so nothing garbles or gets invented.
- Tool: `nano_banana_pro`. Aspect ratio `4:3`.

## Prompt recipe (paste and fill)
```
Delicate editorial line-art teaching diagram on a warm cream paper background, no white anywhere, fine-liner technical illustration style, drawn with warmth and friendly detail, very clear and very simple, easy enough for a child to follow at a glance. Thin precise dark-ink line-drawing icons, each with a subtle soft pastel accent (sage green, dusty rose, or peach). Short hand-lettered all-capitals labels. Crisp legible lettering, magazine quality, identical fine-liner sketchbook style.

At the very top, centered, a hand-lettered all-capitals title on one line: {TITLE}
Directly under the title, one smaller hand-lettered line: {SUBTITLE}

{BODY: a clean layout, e.g. a descending five-step staircase with a SAVINGS arrow, OR a four-icon row, OR two columns CHALLENGE -> SOLUTION with arrows. Each item = one small dark-ink line-art icon with a subtle pastel accent and a short hand-lettered caps label.}

At the bottom, inside one thin rounded rectangle box spanning the width, a small hand-lettered header WHY WE DO THIS, then {N} short numbered lines in small neat hand-lettering:
{NUMBERED LINES}

The text in the image is exactly these strings, spelled exactly, and nothing else: {ENUMERATE EVERY STRING}. No other words.

Soft sage-green, dusty-rose and peach accents used sparingly. Warm cream ground, organised airy layout, refined minimal fine-line editorial illustration, clean legible hand-lettered capitals. No solid fills, no navy, no grey background, no white.
```

## Content rules
- No em dashes anywhere (Sonagi rule). Use commas, periods, colons, parentheses.
- Proper technical vocabulary, but every term carries enough plain context for a non-technical LinkedIn reader.
- When showing intentional choices for our size, separate `WE CHOSE` (icons carry the pastel accent + a small check) from `WE SKIPPED (FOR NOW)` (same dark-ink fine-line, drawn with a dashed outline and a small hand-drawn X, NO pastel accent). These are deliberate choices, not a build-status tracker. Do NOT use grey to show "skipped" (grey is banned); use the dashed outline + X instead.
