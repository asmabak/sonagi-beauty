# Article Angle Mining

Date: 2026-06-10

Use this before generating any Sonagi carousel bank from Sonagi Reference.

## Principle

One article is not one carousel. One article should become a cluster of carousel concepts.

The carousel generator should first mine the article for angles, then create separate carousels from the strongest angles. This avoids shallow summaries and creates repeatable content from the same editorial asset.

## Required Extraction

For each article, extract:

- 5-10 hook candidates.
- 3-5 skin/routine mechanisms.
- 3 common mistakes.
- 3 counter-intuitive soundbites.
- 2-4 audience segments.
- 2-4 CTA routes: product, quiz, article, routine.
- All owned images from the article.
- Adjacent owned archive images only if article images are not enough.

## Carousel Angle Types

1. Trend hook carousel
   Start with what the audience already sees on TikTok/Instagram, then correct it with Sonagi expertise.

2. Mistake correction carousel
   Start with the wrong gesture or belief, then explain what it does to the skin.

3. Skin mechanism carousel
   Explain what the skin is doing in plain French, with one diagram insert if useful.

4. Routine sequencing carousel
   Show the right order, timing, frequency, or texture logic.

5. Product selection carousel
   Explain why one product/category fits the clarified need.

6. Audience filter carousel
   Clarify who should do it, who should avoid it, and how to adapt it.

7. Myth carousel
   Build around one strong counter-intuitive line that people will save.

## Quality Gate

Do not generate the carousel if:

- The angle is only a summary of the article.
- The hook sounds like a blog title.
- The slide sequence cannot create need before the CTA.
- The available visuals would force repeated photos or weak contextual matches.
- A person would need to guess what a slide means.

## Output Rule

For each article, save an angle bank before rendering slides:

```text
article-title/
  angle-bank.md
  angle-01-carousel/
  angle-02-carousel/
  angle-03-carousel/
```

The `angle-bank.md` should explain why each selected angle deserves its own carousel.
