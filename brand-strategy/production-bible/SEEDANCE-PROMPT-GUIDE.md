# Seedance 2.0 — Prompt Writing Guide
## Everything learned from testing, failing, and iterating on Higgsfield

---

## THE GOLDEN RULE

Seedance wants **60-100 words**, written like a **film director's brief**, not a creative writing essay. One subject, one action, one camera per segment. Put the most important thing first.

---

## PROMPT STRUCTURE THAT WORKS

### The 6-Step Formula

```
[Subject], [Action], in [Environment], camera [Camera Movement], style [Style], avoid [Constraints]
```

### For 10-15 Second Clips — Use Time Segments

This is the format Seedance actually follows:

```
A 15-second vertical video of [subject description] doing [main action] in [setting]. [Voice/language direction].

0-5s: [What happens visually]. [Camera/framing]. [Lighting].
He says: "[Dialogue]"

5-10s: [What happens visually]. [Expression/gesture].
He says: "[Dialogue]"

10-15s: [What happens visually]. [Emotional shift].
He says: "[Dialogue]"

Camera [one instruction]. [Lighting]. [Music/audio direction].
```

### What does NOT work

- Labeled block format (CHARACTER:, CAMERA RULES:, SETTING:, INTERACTION STYLE:) — Seedance ignores structured headers
- 300+ word prompts — Seedance loses coherence after ~100 words
- Multiple camera instructions in one segment
- Describing what NOT to do (negative prompts have limited effect)
- Asking for captions/text overlays — Seedance can't render dynamic text

---

## CAMERA LANGUAGE SEEDANCE UNDERSTANDS

Use exactly these terms:

| Keyword | What it does |
|---------|-------------|
| `push-in` / `dolly in` | Moves toward subject |
| `pull-out` / `dolly out` | Reveals wider shot |
| `pan left/right` | Horizontal sweep |
| `tracking shot` / `follow` | Pursues subject |
| `orbit` / `arc` | Rotates around subject |
| `aerial` / `drone shot` | Bird's eye |
| `handheld` | Natural slight shake (UGC feel) |
| `fixed` / `locked-off` | Completely still |

**CRITICAL: Use only ONE camera instruction per clip.** Combining movements causes jitter and artifacts.

### Shot Sizes

`extreme close-up` → `close-up` → `medium close-up` → `medium shot` → `full shot` → `wide shot`

### Pacing Words (instead of technical specs)

- **Extremely slow**: imperceptible, barely
- **Slow**: slow, gentle, gradual
- **Medium**: smooth, controlled
- **Fast**: dynamic, swift (use cautiously — degrades quality)

---

## THE @ REFERENCE SYSTEM

When uploading images/videos/audio as references:

```
@Image1 as the first frame
@Image1's character as the subject
reference @Video1's camera movement
BGM references @Audio1
wearing the outfit from @Image2
scene references @Image3
```

Always explicitly state WHAT each reference contributes.

---

## LIGHTING — THE HIGHEST LEVERAGE ELEMENT

Adding one lighting description improves quality more than adding ten adjectives.

**Keywords that work well:**
- `golden hour` / `warm golden lighting`
- `rim light` / `backlit`
- `natural light` / `soft window light`
- `neon` / `fluorescent`
- `overcast` / `diffused`
- `vanity light from left` (for bathroom content)

---

## WHAT KILLS QUALITY

| Mistake | Why | Fix |
|---------|-----|-----|
| Using "fast" | Causes jitter when combined with complex scenes | Make only ONE element fast |
| Multiple camera moves | Conflicting instructions = artifacts | One camera per segment |
| Vague adjectives ("cinematic", "epic", "beautiful") | No actionable guidance for the model | Describe specifically |
| 200+ word prompts | Model loses coherence | Stay under 100 words |
| Negative-only instructions ("don't do X") | Model responds better to affirmative | Say what TO do |
| Asking for text/captions | Seedance can't render readable text | Add text in post-production |
| Combining fast camera + fast subject + busy scene | Triple-jitter | Keep one element fast, others slow |

---

## COMMON NEGATIVE PROMPTS (append when needed)

```
avoid jitter, avoid bent limbs, avoid temporal flicker, 
avoid identity drift, avoid chaotic composition
```

---

## UGC / INFLUENCER STYLE — SPECIFIC TIPS

Getting Seedance to produce authentic-looking influencer content (not ads):

### What works:
- `"smartphone filmed from slightly above"` or `"filmed from below face height"`
- `"handheld smartphone feel"` — triggers natural micro-shake
- `"camera fixed, no movement"` — for phone-propped-on-shelf look
- Describing the real environment (tiles, counter, mirror, products) in 1-2 sentences
- `"he talks directly to camera"` — triggers eye contact with lens
- `"eyes locked on camera like talking to a friend"`
- Time-segmented scene descriptions with dialogue inline

### What doesn't work:
- Asking for "off-center framing" (Seedance defaults to centered anyway)
- Long descriptions of facial micro-expressions (model can't control this precisely)
- Asking for product liquid/texture to be "visible and glistening" (hit or miss — sometimes produces dry skin)
- Describing wardrobe accessories in detail (earrings, necklaces — often ignored)

### The Ad vs UGC problem:
Seedance defaults to polished commercial aesthetics. To counter this:
- Use `"handheld"` camera keyword
- Describe a real room, not a studio
- Keep lighting description warm and natural, not "soft key light from upper-left"
- Use `"smartphone"` in the camera description
- Don't describe the character as "strikingly beautiful" or "perfectly symmetrical" — this triggers model/ad aesthetics

---

## MULTI-CLIP WORKFLOW (for videos longer than 15s)

Higgsfield max generation: **15 seconds**. For longer videos, generate separate clips and stitch in an editor.

### 3-Clip Template for a 45-second video:

| Clip | Seconds | Purpose | Camera |
|------|---------|---------|--------|
| A — Hook | 15s | Grab attention, establish topic | Angle 1 (e.g., from above) |
| B — Product/Action | 15s | Show the thing, the process | Angle 2 (e.g., three-quarter) |
| C — Payoff/Close | 15s | Result, reaction, sign-off | Angle 3 (e.g., from below) |

**Use a DIFFERENT camera angle per clip** — this creates visual dynamism when stitched together.

### What to add in post-production (NOT in Seedance):
- Text hook overlays at the top of frame
- Dynamic word-by-word captions
- Before/after comparison photos as overlays
- Trending music/sounds
- Transitions between clips (simple cuts work best)

### Overlap between clips:
End of Clip A should connect naturally to start of Clip B (e.g., A ends with reaching for product, B starts holding it).

---

## EXAMPLE: COMPLETE 15-SECOND UGC SKINCARE PROMPT

```
A 15-second vertical video of this exact young Korean male from 
the reference image talking directly to camera in a warm bathroom. 
He speaks French with natural lip-sync, young warm voice with 
slight Korean accent.

0-5s: Close-up of his face, smartphone filmed from slightly above, 
he looks up at camera. Warm beige tile bathroom, golden vanity 
light from left. His skin shows slight redness on cheeks. He 
touches his cheek with fingertips, winces, then gives camera a 
self-deprecating half-smile and small head shake.
He says: "Bon, je vais etre honnete. Ma peau en ce moment c'est 
la cata."

5-10s: Same framing. He gestures with one hand, counting on 
fingers. Frustrated but slightly amused expression. Eyes locked 
on camera like talking to a friend.
He says: "J'ai abuse du retinol, trop d'exfoliants, et ma 
barriere cutanee est foutue."

10-15s: His eyebrows lift, corner of mouth turns up. Hopeful 
energy. He glances down toward counter then back at camera with 
a knowing look.
He says: "Mais j'ai trouve un truc."

Camera fixed, no movement. Handheld smartphone feel. Warm golden 
lighting. Trending chill lo-fi beat at low volume.
```

---

## SOURCES

- [Seedance 2.0 Skill Guide (dexhunter)](https://github.com/dexhunter/seedance2-skill/blob/main/SKILL.md)
- [Apiyi — 6-Step Formula + Camera Guide](https://help.apiyi.com/en/seedance-2-0-prompt-guide-video-generation-camera-style-tips-en.html)
- [WaveSpeed AI — Prompt Template](https://wavespeed.ai/blog/posts/blog-seedance-2-0-prompt-template/)
- [500+ Curated Prompts (YouMind-OpenLab)](https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts)
- [Higgsfield Official — Seedance 2.0](https://higgsfield.ai/seedance/2.0)
- Our own testing: MINJUN-PRODUCTION-BIBLE.md + Script 05 v1/v2/v3 iterations
