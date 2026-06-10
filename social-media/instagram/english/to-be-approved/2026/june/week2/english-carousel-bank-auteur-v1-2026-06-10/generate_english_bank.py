from pathlib import Path
import importlib.util

FRENCH_GENERATOR = Path("/Users/marouanebakhtar/sonagi-beauty/social-media/instagram/french/to-be-approved/2026/june/week2/reference-carousel-bank-auteur-v5-2026-06-10/generate_v5_carousels.py")
spec = importlib.util.spec_from_file_location("fr_layout", FRENCH_GENERATOR)
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)

ROOT = Path(__file__).resolve().parent
IMG = layout.IMG
DIA = layout.DIA
IRIS = IMG / "_prompt-library/outputs"


def draw_cta_bar(draw, deck, i, s):
    if i == 6:
        draw.rectangle((52, 1184, 1028, 1294), fill=(28, 24, 21, 158))
        draw.text((74, 1198), "Shop: connect IG/TikTok Shop tag.", font=layout.F["cta"], fill=layout.CREAM)
        draw.text((74, 1228), f"Routine quiz: {deck['quiz_url']} / link in bio", font=layout.F["cta_sm"], fill=layout.CREAM)
        draw.text((74, 1252), f"Full article: {deck['article_url']} / Sonagi Reference", font=layout.F["cta_sm"], fill=layout.CREAM)
        draw.text((884, 1252), "sonagi", font=layout.F["cta"], fill=layout.PEACH)
        return
    draw.rectangle((52, 1222, 1028, 1270), fill=(28, 24, 21, 142))
    draw.text((74, 1234), "Save this guide · routine + references in the Sonagi profile", font=layout.F["cta_sm"], fill=layout.CREAM)
    draw.text((878, 1234), "sonagi", font=layout.F["cta"], fill=layout.PEACH)


layout.ROOT = ROOT
layout.draw_cta_bar = draw_cta_bar

decks = [
    {
        "slug": "01-skin-flooding-anua",
        "label": "hydration trend",
        "title": "Skin flooding: TikTok found it. Seoul had already coded it.",
        "note": "English version. No French diagrams inserted where no English equivalent exists.",
        "shop_cta": "Connect the Anua Heartleaf IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/techniques/en/skin-flooding/",
        "slides": [
            {"bg": IRIS/"022-skin-flooding-body-v1.webp", "kicker": "Trend", "title": "You call it skin flooding. In Korea, it was already a method.", "body": "The trend is not the point. The point is why damp skin holds hydration better.", "cta": "Save before layering seven products at random."},
            {"bg": IMG/"techniques/slugging-body.webp", "kicker": "The need", "title": "Your skin is not always asking for more cream.", "body": "Often it is asking for water, placed at the right moment, before it evaporates.", "cta": "Hydration needs timing."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "The rule", "title": "Do not let skin dry between layers.", "body": "Ten to twenty seconds. If the surface dries, the humectant effect drops.", "cta": "Try three layers before seven."},
            {"bg": IMG/"basics/ppm-hero.webp", "kicker": "The trap", "title": "The wrong toner ruins the method.", "body": "No harsh alcohol, no sting, no astringent burn. It should be watery, gentle, layerable.", "cta": "Look for a texture that disappears."},
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "For whom", "title": "Tight skin, flights, heating, stress.", "body": "Skin flooding speaks to dehydrated skin. Oily skin can be dehydrated too.", "cta": "Shiny and tight is a signal."},
            {"bg": IMG/"ingredients/heartleaf-body-1.webp", "kicker": "The choice", "title": "Pick a toner that calms while it hydrates.", "body": "Heartleaf helps reactive skin tolerate the gesture. That is why Anua 77 became a standard.", "cta": "Routine + references in profile."},
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "To do", "title": "The pivot product: Anua Heartleaf 77 Toner.", "body": "Use after cleansing, while skin is still slightly damp, before serum and cream.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "02-double-cleansing-boj",
        "label": "evening cleanse",
        "title": "Double cleansing is not one more routine step.",
        "note": "English version.",
        "shop_cta": "Connect the Beauty of Joseon cleansing balm IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/techniques/en/double-cleansing/",
        "slides": [
            {"bg": IMG/"techniques/double-cleansing-hero.webp", "kicker": "Counter-intuitive", "title": "Foam alone does not really remove your SPF.", "body": "Not because it is bad. Because water does not dissolve oil-loving residue well.", "cta": "Save if you wear SPF or makeup.", "anchor": "left"},
            {"bg": IMG/"techniques/_originals/double-cleansing-2-raw.png", "kicker": "Evening skin", "title": "Your face carries two families of residue.", "body": "Sebum, SPF and makeup on one side. Sweat, dust and water-soluble pollution on the other.", "cta": "One cleanser often means more rubbing."},
            {"bg": IMG/"routines/routine-homme-body-4.webp", "kicker": "Step 1", "title": "The balm dissolves oil without stripping.", "body": "On dry skin, it melts with the palms and lifts SPF, sebum and long-wear makeup.", "cta": "The right balm does the mechanical work.", "anchor": "left"},
            {"bg": IMG/"routines/routine-homme-body-3.webp", "kicker": "Step 2", "title": "The gentle cleanser removes the emulsion.", "body": "The second cleanse should respect skin pH. Hot water and classic soap break the point.", "cta": "Double cleansing is not double aggression.", "anchor": "right"},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "For whom", "title": "Not every morning. Mostly SPF evenings.", "body": "In the morning, often unnecessary. At night, useful after sunscreen, city pollution or makeup.", "cta": "If skin feels tight, step 2 is too strong."},
            {"bg": IMG/"_prompt-library/outputs/020-beauty-of-joseon-body-v1.webp", "kicker": "The choice", "title": "Start with a balm that emulsifies cleanly.", "body": "Beauty of Joseon Radiance Cleansing Balm melts, massages, then rinses to milk.", "cta": "Routine + references in profile."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "To do", "title": "Gesture 1: Beauty of Joseon Radiance Balm.", "body": "Use at night on dry skin, before your low-pH cleanser.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "03-barrier-centella",
        "label": "skin barrier",
        "title": "Your barrier does not need courage. It needs silence.",
        "note": "English diagrams used where available.",
        "shop_cta": "Connect the Skin1004 Centella IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/basics/en/reparer-la-barriere-cutanee/",
        "slides": [
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Quiet signal", "title": "If everything stings, your skin is not being dramatic.", "body": "Often the barrier is leaking. On a cracked wall, more actives repair nothing.", "cta": "Save before adding another serum.", "anchor": "right"},
            {"bg": IMG/"basics/_originals/skin-barrier-asma.png", "kicker": "The need", "title": "Bricks, mortar, water held in.", "body": "Cells are the bricks. Lipids are the mortar. When the mortar is missing, water leaves and irritants enter.", "visual": DIA/"la-barriere-cutanee-en.webp", "cta": "Tight skin often needs less."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "The trap", "title": "Acids + retinol + scrubs: the wall takes the hit.", "body": "A damaged barrier stops tolerating products it used to accept.", "cta": "Two simple weeks beat a full shelf."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "What it wants", "title": "Calm first. Seal later.", "body": "Gentle toner, calming ampoule, cream. The minimum, long enough for the mortar to rebuild.", "visual": DIA/"reparer-la-barriere-cutanee-mechanism-en.webp", "cta": "If it heats up, remove a step."},
            {"bg": IMG/"ingredients/centella-asiatica-hero.webp", "kicker": "Why centella", "title": "Red skin wants quiet.", "body": "Centella is a K-beauty reflex for reactive skin: few ingredients, high tolerance.", "cta": "Keep the formula short."},
            {"bg": IMG/"ingredients/centella-asiatica-1.webp", "kicker": "The choice", "title": "An ampoule, not a punishment.", "body": "Skin1004 Madagascar Centella Ampoule is a simple gesture to bring the routine back down.", "cta": "Routine + references in profile."},
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "To do", "title": "The calm product: Skin1004 Centella Ampoule.", "body": "Apply after cleansing, before cream, when skin turns red or uncomfortable.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "04-sebum-heartleaf",
        "label": "oily skin",
        "title": "Skin that shines is not dirty.",
        "note": "English sebum diagram used.",
        "shop_cta": "Connect the Anua Heartleaf IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/basics/en/le-sebum/",
        "slides": [
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Hot take", "title": "The more you dry oily skin, the more it negotiates.", "body": "Sebum is not dirt. It is a protective layer. The goal is regulation, not extermination.", "cta": "Save if you mattify all day.", "anchor": "left"},
            {"bg": IMG/"basics/_originals/skin-ph-asma.png", "kicker": "The need", "title": "Sebum comes from a factory under the pore.", "body": "It moves up the follicle, mixes with lipids and forms the hydrolipidic film.", "visual": DIA/"le-sebum-en.webp", "cta": "A little shine is not failure."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "The loop", "title": "Over-cleansing can bring shine back.", "body": "Hot water, alkaline soap, daily exfoliation: the surface dries and skin compensates.", "cta": "Clean is not stripped."},
            {"bg": IMG/"ingredients/heartleaf-body-1.webp", "kicker": "What it wants", "title": "An active that calms while it regulates.", "body": "Heartleaf targets redness, discomfort and excess shine without turning the routine harsh.", "cta": "Oily skin still needs softness."},
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "The dose", "title": "77% is not label decoration.", "body": "Anua made heartleaf the centre of the formula. Watery texture, easy morning or night.", "cta": "Regulate the first step after cleansing.", "anchor": "right"},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "The choice", "title": "Balancing toner, not stripping lotion.", "body": "Use when skin shines, reddens or reacts. If it stings, it is not the right product for you.", "cta": "Routine + references in profile.", "anchor": "right"},
            {"bg": IMG/"basics/ppm-hero.webp", "kicker": "To do", "title": "The balancing toner: Anua Heartleaf 77.", "body": "Apply after cleansing, before serum.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "05-sephora-kids-spf",
        "label": "young skin",
        "title": "A twelve-year-old girl does not need anti-ageing.",
        "note": "Uses the exact Sephora Kids article hero first and English article diagram.",
        "shop_cta": "Connect the Beauty of Joseon SPF IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/editos/en/sephora-kids/",
        "slides": [
            {"bg": IMG/"edito/sephora-kids/sephora-kids-hero-v2.webp", "kicker": "Hot topic", "title": "The problem with Sephora Kids is not the cream.", "body": "It is the idea that a child should already monitor her face as a flaw to correct.", "cta": "Save for the next birthday list.", "anchor": "center", "wide_ok": True},
            {"bg": IMG/"routines/routine-enfant-hero-v3.webp", "kicker": "Young skin", "title": "She has no wrinkle to repair.", "body": "A child or pre-teen skin mostly needs softness, simple cleansing and sun protection.", "visual": IMG/"edito/sephora-kids/taille-routine-enfant-en.webp", "cta": "Anti-ageing at ten is the wrong need."},
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "The risk", "title": "Too many actives, too early.", "body": "Acids, retinol, fragrance, long routines: more friction points on a young barrier.", "cta": "A child routine should be short."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "What she needs", "title": "A gentle cleanser. A cream. SPF.", "body": "Not mirror performance. Not twelve steps. Not fear of ageing.", "cta": "The best care is sometimes removal."},
            {"bg": IMG/"cta/cta-newsletter.webp", "kicker": "The paradox", "title": "The only real anti-ageing step is often missing.", "body": "In viral child routines, sunscreen is too often absent. It is the most useful gesture.", "cta": "Replace fear with protection."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "The choice", "title": "A comfortable SPF is the one she reapplies.", "body": "Beauty of Joseon Relief Sun has a light cream texture that makes protection less punitive.", "cta": "Routine + references in profile."},
            {"bg": IMG/"cta/cta-community.webp", "kicker": "To do", "title": "The useful gesture: Beauty of Joseon Relief Sun.", "body": "Use in the morning as the last step, and reapply with exposure.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "06-ph-marseille-soap",
        "label": "acid mantle",
        "title": "Marseille soap is not neutral for your face.",
        "note": "English pH diagram used.",
        "shop_cta": "Connect a low-pH cleanser IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/basics/en/le-ph-de-la-peau/",
        "slides": [
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "French mistake", "title": "Marseille soap sits too high for your face.", "body": "Skin lives around pH 4.5 to 5.5. Classic soap can climb near 9 or 10.", "cta": "Save before washing your face with soap."},
            {"bg": IMG/"basics/_originals/skin-ph-asma.png", "kicker": "The terrain", "title": "Your skin is acidic. On purpose.", "body": "That acid mantle helps the barrier, repair enzymes and microbial balance.", "visual": DIA/"le-ph-de-la-peau-en.webp", "cta": "Acidic does not mean aggressive."},
            {"bg": IMG/"techniques/double-cleansing-hero.webp", "kicker": "The trap", "title": "More foam can mean more stripping.", "body": "The clean feeling can hide a barrier pushed alkaline for hours.", "cta": "Clean is not destabilised."},
            {"bg": IMG/"routines/routine-homme-body-3.webp", "kicker": "The rule", "title": "Look for low pH, not squeaky skin.", "body": "Many gentle K-beauty cleansers live around pH 5 to 6. That is logic, not folklore.", "cta": "Good cleansing leaves skin supple."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "The signal", "title": "If it feels tight after rinsing, it is not normal.", "body": "Tightness, redness, stinging: skin is often telling you the cleanse was too high or too strong.", "cta": "Change the gesture before adding serum."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "The choice", "title": "The routine begins by respecting pH.", "body": "Balm or oil at night if SPF, then gentle cleanser. Everything works better when the barrier is not annoyed.", "cta": "Routine + references in profile."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "To do", "title": "Start with cleanser, not ten actives.", "body": "The right pH makes the whole routine more tolerable, especially if skin reddens or feels tight.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "07-acid-mantle",
        "label": "invisible barrier",
        "title": "The acid mantle is your skin's invisible security.",
        "note": "English pH diagram used.",
        "shop_cta": "Connect a calming toner IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/basics/en/le-ph-de-la-peau/",
        "slides": [
            {"bg": IMG/"sections/comprendre-hero.webp", "kicker": "Mechanism", "title": "Your skin defends itself with acidity.", "body": "Not a burning acidity. A fine biological acidity that keeps the surface stable.", "cta": "Save if your skin reacts to everything."},
            {"bg": IMG/"basics/_originals/skin-ph-asma.png", "kicker": "The zone", "title": "4.5 to 5.5 is the useful range.", "body": "In that zone, the stratum corneum works better and the barrier repairs more cleanly.", "visual": DIA/"le-ph-de-la-peau-en.webp", "cta": "One number can explain a lot of tightness."},
            {"bg": IRIS/"018-heartleaf-body-v1.webp", "kicker": "After cleansing", "title": "A gentle toner helps skin return to calm.", "body": "It should not sting. It should add water, comfort and prepare the next step.", "cta": "Toner is not an alcoholic punishment."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Texture", "title": "Balanced skin reflects light better.", "body": "Glow rarely starts with highlighter. It starts with a surface that holds water.", "cta": "pH is less glamorous, more fundamental."},
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "Mistake", "title": "Lemon, soap, hot water: false friends.", "body": "Natural does not mean compatible with the acid mantle.", "cta": "Simple does not mean brutal."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "The link", "title": "pH and barrier work together.", "body": "When pH rises, the barrier becomes more permeable. When the barrier leaks, everything stings faster.", "cta": "Read the full mechanism."},
            {"bg": IMG/"cta/cta-community.webp", "kicker": "To do", "title": "Test your routine before making it stronger.", "body": "If skin feels tight, start with cleanser and toner, not a stronger active.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "08-niacinamide-slow",
        "label": "patient active",
        "title": "Niacinamide does not make noise. It works.",
        "note": "No French diagram inserted because English mechanism file is missing.",
        "shop_cta": "Connect the niacinamide routine IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/en/niacinamide/",
        "slides": [
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Anti-buzz", "title": "If you want an effect in three days, this is not her.", "body": "Niacinamide is measured in weeks: barrier, marks, sebum, comfort.", "cta": "Save before throwing your serum away."},
            {"bg": IMG/"basics/ppm-hero.webp", "kicker": "The dose", "title": "2 to 5% is often enough.", "body": "More is not always better. The value is consistency, not burn.", "cta": "A smart active does not need to shout."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Barrier", "title": "It helps skin rebuild its lipids.", "body": "That is why it speaks to dull, oily, marked or slightly reactive skin.", "cta": "The barrier is often the real topic."},
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Sebum", "title": "It does not erase sebum. It modulates it.", "body": "The goal is not drying out. The goal is a less chaotic shine.", "cta": "Oily skin needs softness too."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Marks", "title": "It also acts on pigment transfer.", "body": "Not like a harsh peel. More like a slow, better tolerated correction.", "cta": "Patience is part of the formula."},
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "Routine", "title": "After toner, before cream and SPF.", "body": "In the morning, it sits well under sunscreen. At night, it supports the barrier.", "cta": "Routine + references in profile."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "To do", "title": "Choose niacinamide if your skin needs stability.", "body": "Not if you want to strip. Yes if you want to regulate, soften marks and strengthen.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "09-niacinamide-pores",
        "label": "visible pores",
        "title": "Your pores do not close. They negotiate.",
        "note": "English sebum diagram used.",
        "shop_cta": "Connect the niacinamide routine IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/en/niacinamide/",
        "slides": [
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "Myth", "title": "A pore is not a door.", "body": "It does not open and close on command. It becomes more or less visible.", "cta": "Keep this for absurd promises."},
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Why", "title": "Sebum + keratin + light = visible pore.", "body": "When the surface is clogged or dehydrated, texture catches more light.", "visual": DIA/"le-sebum-en.webp", "cta": "Visibility is not destiny."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "The lever", "title": "Niacinamide helps regulate without punishing.", "body": "It targets sebum, barrier and mild inflammation. Finer than stripping.", "cta": "Regulation beats drying out."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Hydration", "title": "Dehydrated skin shows more texture.", "body": "Before stronger, add water back and protect the surface film.", "cta": "A visible pore is not always oily."},
            {"bg": IRIS/"018-heartleaf-body-v1.webp", "kicker": "Tolerance", "title": "If it stings, you lose the benefit.", "body": "A useful active becomes useless if the routine around it makes skin nervous.", "cta": "Calm is a strategy."},
            {"bg": IMG/"sections/comprendre-hero.webp", "kicker": "Expectation", "title": "Aim for less visible, not invisible.", "body": "Realistic goal: smoother surface, better shine control, fewer marks settling in.", "cta": "No filter. Better logic."},
            {"bg": IMG/"cta/cta-newsletter.webp", "kicker": "To do", "title": "Build around the pore, not against it.", "body": "Gentle cleanse, niacinamide, hydration, SPF. Less spectacular, more durable.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "10-snail-mucin-taboo",
        "label": "strange active",
        "title": "Snail mucin is strange. That is partly why it works.",
        "note": "No French diagram inserted because English mechanism file is missing.",
        "shop_cta": "Connect the COSRX mucin IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/en/snail-mucin/",
        "slides": [
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Taboo", "title": "Yes, it is slime. No, it is not dirty.", "body": "Cosmetic mucin is filtered, purified and formulated. The word bothers people more than the texture.", "cta": "Save if the name always blocked you."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "Texture", "title": "It forms a very fine hydrating film.", "body": "Not glue. A veil that helps the surface hold water and look smoother.", "cta": "Glow often comes from the film."},
            {"bg": IRIS/"022-skin-flooding-body-v1.webp", "kicker": "For whom", "title": "Dehydrated skin, post-breakout, tired barrier.", "body": "It speaks to skin that wants comfort without heavy grease.", "cta": "You do not need much."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "The trap", "title": "It is not an acne miracle treatment.", "body": "It can help comfort and post-spot appearance, but it does not replace medical care.", "cta": "Do not ask a hydrator to be medicine."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "Timing", "title": "After toner, before cream.", "body": "One or two thin layers. Wait a minute if you dislike stickiness.", "cta": "The thin layer usually wins."},
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "Caution", "title": "If you are allergic to snails, avoid it.", "body": "And if your skin reacts easily, patch-test before installing it.", "cta": "Strange does not mean universal."},
            {"bg": IMG/"cta/cta-community.webp", "kicker": "To do", "title": "Use it as intelligent hydration, not a miracle.", "body": "It shines when the routine is simple: toner, mucin, cream, SPF in the morning.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "11-snail-mucin-post-acne",
        "label": "after a spot",
        "title": "After a spot, your skin may not want an acid.",
        "note": "No French diagram inserted because English mechanism file is missing.",
        "shop_cta": "Connect the COSRX mucin IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/en/snail-mucin/",
        "slides": [
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Aftermath", "title": "The spot leaves. The skin stays offended.", "body": "Redness, mark, texture: post-spot skin is often a surface repair question.", "cta": "Save before exfoliating again."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "The need", "title": "It wants water, calm and time.", "body": "Mucin helps most as a hydrating comfort layer, not an attack.", "cta": "Repair is not stripping."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Mistake", "title": "Acid on acid can prolong irritation.", "body": "When the barrier is already stressed, intensity can keep the mark visible longer.", "cta": "Less strong can be faster."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Duo", "title": "Niacinamide + mucin: patient duo.", "body": "One supports barrier and marks. The other brings the hydrating film.", "cta": "Not glamorous. Very useful."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Application", "title": "Two thin layers beat one puddle.", "body": "On slightly damp skin, then cream. Stickiness often comes from dose.", "cta": "The texture should disappear."},
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "SPF", "title": "Without SPF, the mark hangs on.", "body": "In the morning, post-spot repair always ends with sunscreen.", "cta": "Light often decides the mark."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "To do", "title": "For marks, begin by calming.", "body": "If acne is active or painful, cosmetics are not enough: seek medical advice.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "12-slugging-not-for-everyone",
        "label": "night sealing",
        "title": "Slugging is not for every skin.",
        "note": "No French diagram inserted because English mechanism file is missing.",
        "shop_cta": "Connect the barrier ritual IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/techniques/en/slugging/",
        "slides": [
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Filter", "title": "If your acne is active, be careful.", "body": "Slugging seals. If it seals too much sebum, heat or bacteria, comfort can worsen.", "cta": "Save before trying petrolatum everywhere."},
            {"bg": IMG/"techniques/slugging-body.webp", "kicker": "Principle", "title": "It is not hydration. It blocks evaporation.", "body": "The occlusive film keeps water underneath. It does not replace toner, serum or cream.", "cta": "You seal what was placed well."},
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "For whom", "title": "Dry skin, winter, tired barrier.", "body": "There, the gesture can be useful. Especially in a thin layer, not a greasy mask.", "cta": "Slugging is a blanket, not treatment."},
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "Avoid", "title": "Not over active inflammation.", "body": "Painful spots, folliculitis, very oily T-zone: adapt or avoid.", "cta": "The trend does not know your skin."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "Before", "title": "Hydrate first, seal second.", "body": "Dry skin under petrolatum stays dry. It just loses water more slowly.", "cta": "Preparation makes the result."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "Frequency", "title": "One or two nights are often enough.", "body": "No need to make it an identity. Observe the skin in the morning.", "cta": "Smart ritual, not reflex."},
            {"bg": IMG/"cta/cta-newsletter.webp", "kicker": "To do", "title": "Patch-test on a dry zone before the whole face.", "body": "If it heats, itches or creates spots, stop. Good care simplifies skin.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "13-glass-skin-not-oil",
        "label": "mool-gwang",
        "title": "Glass skin does not mean an oily face.",
        "note": "No French diagram inserted because English mechanism file is missing.",
        "shop_cta": "Connect the glow ritual IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/techniques/en/glass-skin/",
        "slides": [
            {"bg": IRIS/"022-skin-flooding-body-v1.webp", "kicker": "Myth", "title": "K-beauty glow is not a layer of grease.", "body": "Mool-gwang is about water and light, not a saturated surface.", "cta": "Save if your routine shines but feels tight."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Optics", "title": "Hydrated skin reflects differently.", "body": "When the stratum corneum holds water, light lands more evenly.", "cta": "Glow is first a surface."},
            {"bg": IMG/"techniques/double-cleansing-hero.webp", "kicker": "Base", "title": "Night starts by removing SPF and residue.", "body": "Without gentle cleansing, you layer care over noise.", "cta": "Glass skin begins at the sink."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Actives", "title": "Niacinamide, mucin, heartleaf: thin layers.", "body": "The secret is not product count. It is place, dose and tolerance.", "cta": "Saturated skin is not hydrated skin."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Barrier", "title": "Without barrier, glow becomes redness.", "body": "If everything stings, stop chasing shine. Repair comfort.", "cta": "Light comes after calm."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "Rule", "title": "Three well-placed gestures beat ten steps.", "body": "Gentle cleanse, hydration, cream or SPF. Add only what your skin tolerates.", "cta": "The ritual must live in real life."},
            {"bg": IMG/"cta/cta-community.webp", "kicker": "To do", "title": "Look for water-light, not grease.", "body": "If you want to know which glow version suits your skin, start with the quiz.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "14-acne-cycle",
        "label": "adult acne",
        "title": "The spot that returns every month is not random.",
        "note": "English sebum diagram used where available.",
        "shop_cta": "Connect the calming care IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/conditions/en/acne-hormonale/",
        "slides": [
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "Pattern", "title": "Same zone, same week, same spot.", "body": "When it returns around the cycle, skin is often telling a hormonal story.", "cta": "Save if your chin has a calendar."},
            {"bg": IMG/"sections/technique-hero.webp", "kicker": "Zone", "title": "Lower face, jawline, chin.", "body": "Frequent zones in adult hormonal acne, especially when the flare is inflammatory.", "cta": "Observing the pattern already helps."},
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Mechanism", "title": "Androgens stimulate sebum.", "body": "More sebum, more keratin, more microcomedone risk. It is not a question of dirt.", "visual": DIA/"le-sebum-en.webp", "cta": "Washing harder is not the answer."},
            {"bg": IRIS/"018-heartleaf-body-v1.webp", "kicker": "Cosmetic", "title": "Skincare calms the terrain. It does not treat the hormone.", "body": "Heartleaf, centella and niacinamide can help tolerance and the barrier.", "cta": "The role of care must stay honest."},
            {"bg": IMG/"techniques/double-cleansing-2.webp", "kicker": "Ritual", "title": "Cleanse gently, especially on SPF nights.", "body": "Cleansing should remove residue without turning the barrier red.", "cta": "Regularity beats force."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Alert", "title": "Pain, nodules, scars: medical advice.", "body": "Moderate to severe acne belongs with a dermatologist. Cosmetics can accompany, not replace.", "cta": "Sonagi does not sell medical miracles."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "To do", "title": "Track the cycle before changing everything.", "body": "Note the week, zone and pain, then build a barrier-respecting routine.", "cta": "Product, quiz, article."},
        ],
    },
    {
        "slug": "15-acne-do-not-strip",
        "label": "inflamed skin",
        "title": "Acne-prone skin does not need punishment.",
        "note": "English sebum and barrier diagrams used where available.",
        "shop_cta": "Connect the calming care IG/TikTok Shop tag.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/conditions/en/acne-hormonale/",
        "slides": [
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "Hot take", "title": "Stripping acne can feed inflammation.", "body": "When skin is already in conflict, over-cleansing or over-exfoliating can prolong stress.", "cta": "Save before your next scrub."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Goal", "title": "Regulate. Do not aim for desert.", "body": "Sebum also protects. The goal is calming excess, not erasing skin.", "visual": DIA/"le-sebum-en.webp", "cta": "Dry skin can be more nervous."},
            {"bg": IMG/"ingredients/centella-asiatica-hero.webp", "kicker": "Calm", "title": "Centella speaks to skin that inflames fast.", "body": "Few ingredients, simple texture, tolerance. Less sexy than a peel, often more useful.", "cta": "Calm is an active."},
            {"bg": IRIS/"018-heartleaf-body-v1.webp", "kicker": "Redness", "title": "Heartleaf helps when skin shines and reddens.", "body": "The interesting gesture: soothing while regulating.", "cta": "It does not need to hurt to work."},
            {"bg": IMG/"routines/routine-homme-body-1.webp", "kicker": "Cleansing", "title": "One gentle cleanser beats two aggressive ones.", "body": "At night, remove SPF and pollution. But skin should not squeak after.", "cta": "Clean is not stripped."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Barrier", "title": "If everything stings, pause actives.", "body": "A damaged barrier turns even good products into a problem.", "visual": DIA/"la-barriere-cutanee-en.webp", "cta": "Reset is sometimes the strategy."},
            {"bg": IMG/"cta/cta-newsletter.webp", "kicker": "To do", "title": "Build a routine that calms before correcting.", "body": "If acne is painful or persistent, seek medical advice. For the rest, begin with tolerance.", "cta": "Product, quiz, article."},
        ],
    },
]


def main():
    layout.decks = decks
    layout.main()


if __name__ == "__main__":
    main()
