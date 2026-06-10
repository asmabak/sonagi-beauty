# Sonagi Carousel Automation Rules

These rules exist because V1-V4 exposed recurring mistakes: weak visual judgment, unsafe crops, repeated images, diagrams used as decorative backgrounds, and slides that looked assembled rather than editorial.

## Non-Negotiables

1. No card behind the main text.
2. Main photo must be visible and contextually relevant.
3. Do not crop a photo so hard that the subject becomes random or unclear.
4. Do not repeat the same background photo inside one carousel.
5. Use diagrams in the carousel language only: French diagrams for French carousels, English diagrams for English carousels. If no English diagram exists, do not use the French diagram as a substitute.
6. Every slide must be understandable without guessing.
7. Every final slide must have a direct product CTA when the carousel is product-led.
8. Never use a diagram, chart, mechanism image, or product packshot as a background photo.
9. Background photos must be crop-safe for 4:5 full bleed. If the image would need an inset, letterbox, or blurred duplicate to work, reject it and ask Iris for a better owned image.
10. Do not paste a second lifestyle/photo image on top of the slide. The only allowed overlay image is a small explanatory diagram, centered in the lower space.

## Topic Selection

Good Sonagi carousel topics must have one of these tensions:

- A trendy behavior the audience already sees: skin flooding, Sephora Kids, glass skin, double cleansing.
- A counter-intuitive correction: oily skin is not dirty, more products can make sensitivity worse.
- A clear skin mechanism: barrier leakage, sebum regulation, hydration layering.
- A product-selection payoff: which toner, balm, ampoule, SPF, or serum solves the clarified need.

Avoid topics that are educational but not emotionally charged.

## Article Mining Rule

One Sonagi Reference article should produce several carousel angles before moving to another source.

Do not treat an article as one carousel. Treat it as a bank of:

- Trend angle: what people are already talking about.
- Mistake angle: what the audience is doing wrong.
- Mechanism angle: what the skin is actually doing.
- Routine angle: what sequence or gesture should change.
- Product angle: which product/category solves the clarified need.
- Audience angle: who this applies to and who should avoid it.
- Myth angle: the counter-intuitive soundbite that makes the article saveable.

For each article, first extract at least 5 possible carousel hooks. Then choose the strongest 2-4 angles based on:

- Does the hook create tension in the first sentence?
- Can the article support 7 fully understandable slides?
- Are there enough owned/contextual images for the topic?
- Is there a direct CTA: quiz, product page, routine, or article?

Example from one double-cleansing article:

- "Ta mousse seule ne retire pas vraiment ton SPF."
- "Double nettoyage ne veut pas dire double agression."
- "Le soir, ta peau porte deux familles de résidus."
- "Le baume se met sur peau sèche, pas sous la douche."
- "Si ta peau tire après, le problème est l'étape 2."

Example from one skin-barrier article:

- "Si tout pique, ce n'est pas que ta peau est capricieuse."
- "Ta barrière n'a pas besoin de courage, elle a besoin de silence."
- "Acides + rétinol + gommage : le mur prend tout."
- "Deux semaines simples valent mieux qu'un placard plein."
- "La peau qui tire demande moins, pas plus."

## Hook Rules

Good hooks:

- Start from an existing belief and reverse it.
- Are concrete, not decorative.
- Contain a visible tension in the first line.
- Do not sound like a blog title.

Examples:

- "Ta mousse seule ne retire pas vraiment ton SPF."
- "Plus tu assèches ta peau grasse, plus elle négocie."
- "Une fille de douze ans n'a pas besoin d'anti-âge."

Weak hooks:

- "Tout savoir sur..."
- "Guide complet de..."
- "Pourquoi utiliser..."

## Visual Selection Rules

Image priority:

1. Images from the exact Sonagi Reference article. This is mandatory, not optional. If the exact article has a usable photo, it must be tried before any adjacent archive image.
2. Crop-safe Iris-produced / Image Lab Sonagi-owned photos already available in `sonagi-reference/assets/images/_prompt-library/outputs/`.
3. Adjacent Sonagi Reference image from the same skin state, ingredient family, or routine moment.
4. Existing Sonagi archive/social image if it clarifies the same emotional or physical state.
5. Product image from the exact product CTA only when the slide is explicitly about product selection.
6. If no good image exists, mark `iris_needed: true` and ask Iris/image lab for a new photo.

Image rejection criteria:

- The image only matches the product, not the slide idea.
- The subject would be destroyed by a 4:5 crop.
- The image is an Iris horizontal output that needs a vertical variant before full-bleed use.
- The slide needs intimacy but the image is just a product packshot.
- The slide needs education but the image is decorative lifestyle filler.
- The same background appears elsewhere in the same carousel.
- The photo has been rejected by Asma in review. Add it to the carousel blocklist and do not reuse it for the same topic.

## Crop Rules

Default crop mode is `full_bleed_safe_crop`.

This means:

- The selected image fills the entire 1080x1350 slide.
- The subject remains recognizable after the crop.
- The source aspect ratio must be close enough to 4:5 to avoid a destroyed subject.
- Never crop a face at the mouth, eyes, or forehead unless intentionally editorial and still readable.
- Never crop a product so the label/shape becomes unrecognizable.

Reject the image and ask Iris/image lab when:

- The source photo is too wide or too tall for full bleed.
- The only way to use it is to place the full image as a rectangle over a blurred background.
- The resulting slide starts to feel like a card or collage instead of an Auteur-style full-bleed editorial image.

## Diagram Rules

- Do not use diagrams as backgrounds.
- Diagrams may be used as small educational inserts only.
- Diagram inserts must be centered in the lower space, below the main text and above the CTA.
- Diagram inserts must come from the Sonagi Reference diagram set in the same language as the carousel.
- Do not use product packshots as diagram substitutes.
- If the diagram makes the slide feel crowded, remove words before removing the photo.

## Real Estate Rules

- Keep the main text in a consistent upper-left editorial zone.
- Keep the image as one centered full-bleed background.
- If a diagram is needed, center it in the lower visual space.
- Keep CTA bars thin. They should close the slide, not dominate it.
- Do not use a large opaque text panel. Readability comes from gradient/filter, shadow, and strong image selection.
- Prefer fewer, better words. If the title and body compete for space, rewrite the body first.

## CTA Rules

- Final slide must include three paths:
  - Shop route: Instagram Shop product tag or TikTok Shop tag when available.
  - Quiz route: `sonagibeauty.com/consultation.html`.
  - Article route: the full Sonagi Reference article URL.
- If Instagram Shop or TikTok Shop is not connected yet, write "via le tag boutique IG/TikTok Shop" as the operational placeholder.
- Normal slides must not say "next slide", "dernière slide", or push people out of the platform repeatedly.
- Normal-slide footer should be native and light: save/profile/link-in-bio/reference language.
- Final slide is the only slide that should carry the full quiz/article URL pattern unless a specific platform format supports clickable links.

## Slide Structure

For Kbeauty Gems-style Sonagi carousels:

1. Trend/tension hook.
2. What the skin is doing.
3. What the skin needs.
4. What people get wrong.
5. What to choose.
6. Why this product/category fits.
7. Direct CTA.

For each slide, ask:

- Is the slide fully understandable alone?
- Does the image support the sentence on the slide?
- Would someone save this because it teaches one useful thing?
- Is the CTA clear and direct?

## Iris Escalation

Ask Iris/image lab when:

- The article has fewer than 4 usable photos.
- The only available image is a product packshot and the slide needs a skin/emotional state.
- The crop-safe version of the image looks generic.
- The carousel would reuse the same visual language more than twice.

Prompt Iris with:

- Slide topic.
- Exact sentence on the slide.
- Needed skin state, object, gesture, or product context.
- Sonagi visual mood: high-end, intimate, editorial, MoMA/typewriter, Auteur-like image under filter.
- Ownership requirement: only Sonagi-owned or newly generated image lab output.
