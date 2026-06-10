from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import html
import math
import shutil

ROOT = Path(__file__).resolve().parent
REF = Path("/Users/marouanebakhtar/sonagi-reference")
W, H = 1080, 1350

FONT_TYPE = "/System/Library/Fonts/Supplemental/AmericanTypewriter.ttc"
FONT_SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

CREAM = (248, 241, 230)
INK = (28, 24, 21)
PEACH = (245, 196, 170)
YELLOW = (247, 216, 76)


def font(path, size, index=0):
    return ImageFont.truetype(path, size=size, index=index)


F = {
    "micro": font(FONT_TYPE, 17),
    "kicker": font(FONT_TYPE, 22),
    "title": font(FONT_SERIF_BOLD, 60),
    "title_sm": font(FONT_SERIF_BOLD, 51),
    "body": font(FONT_TYPE, 30),
    "body_sm": font(FONT_TYPE, 27),
    "cta": font(FONT_TYPE, 23),
    "cta_sm": font(FONT_TYPE, 18),
}


def assert_background_ok(path):
    bad_terms = [
        "diagram",
        "mechanism",
        "chart",
        "schema",
        "taille-routine",
        "how-toners",
        "timeline",
        "glp1",
        "routine-am-pm",
        "active-stack",
        "fat-compartments",
        "volume-loss-progression",
    ]
    text = str(path).lower()
    if any(term in text for term in bad_terms):
        raise ValueError(f"Diagram/chart cannot be used as slide background: {path}")
    if "/products/" in text:
        raise ValueError(f"Product packshot cannot be used as slide background; use it as a lower-half insert: {path}")


def cover(path, anchor="center"):
    assert_background_ok(path)
    img = Image.open(path).convert("RGB")
    img = ImageOps.autocontrast(img)
    ratio = img.width / img.height
    if not (0.70 <= ratio <= 1.20):
        raise ValueError(f"Background aspect ratio is unsafe for full-bleed 4:5 slide ({ratio:.2f}): {path}")

    scale = max(W / img.width, H / img.height)
    bg = img.resize((math.ceil(img.width * scale), math.ceil(img.height * scale)), Image.LANCZOS)
    # Auteur-style slides need one centered photo, not improvised left/right crops.
    left = (bg.width - W) // 2
    top = max(0, (bg.height - H) // 2)
    return bg.crop((left, top, left + W, top + H))


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if not line or draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text(draw, xy, text, fnt, fill, width, gap=8, shadow=True):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        if shadow:
            draw.text((x + 2, y + 2), line, font=fnt, fill=(0, 0, 0, 118))
        draw.text((x, y), line, font=fnt, fill=fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + gap
    return y


def gradient(canvas, side="left", alpha=170):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = layer.load()
    if side == "left":
        for x in range(W):
            a = int(alpha * max(0, 1 - x / 820))
            for y in range(H):
                pix[x, y] = (0, 0, 0, a)
    elif side == "bottom":
        for y in range(H):
            a = int(alpha * max(0, (y - 820) / 430))
            for x in range(W):
                pix[x, y] = (0, 0, 0, a)
    elif side == "top":
        for y in range(H):
            a = int(alpha * max(0, 1 - y / 470))
            for x in range(W):
                pix[x, y] = (0, 0, 0, a)
    return Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")


def paste_diagram(canvas, path):
    if not path:
        return
    src_path = str(path).lower()
    if "/diagrams/" not in src_path:
        return
    src = Image.open(path).convert("RGBA")
    src.thumbnail((520, 330), Image.LANCZOS)
    box_w, box_h = src.width + 30, src.height + 30
    x = (W - box_w) // 2
    y = 790
    veil = Image.new("RGBA", (box_w, box_h), (248, 241, 230, 210))
    veil.alpha_composite(src, (15, 15))
    canvas.paste(veil, (x, y), veil)


def draw_cta_bar(draw, deck, i, s):
    if i == 6:
        draw.rectangle((52, 1184, 1028, 1294), fill=(28, 24, 21, 158))
        draw.text((74, 1198), deck["shop_cta"], font=F["cta"], fill=CREAM)
        draw.text((74, 1228), f"Quiz routine : {deck['quiz_url']}", font=F["cta_sm"], fill=CREAM)
        draw.text((74, 1252), f"Article complet : {deck['article_url']}", font=F["cta_sm"], fill=CREAM)
        draw.text((884, 1252), "sonagi", font=F["cta"], fill=PEACH)
        return

    draw.rectangle((52, 1222, 1028, 1270), fill=(28, 24, 21, 142))
    cta = s["cta"]
    if len(cta) > 58 and " : " in cta:
        lead, slug = cta.split(" : ", 1)
        draw.text((74, 1228), f"{lead} :", font=F["micro"], fill=CREAM)
        draw.text((74, 1249), slug, font=F["micro"], fill=CREAM)
    else:
        draw.text((74, 1234), cta, font=F["cta"], fill=CREAM)
    draw.text((878, 1234), "sonagi", font=F["cta"], fill=PEACH)


def render_slide(deck, i, s):
    img = cover(s["bg"])
    img = gradient(img, "top", 54)
    img = gradient(img, "left", s.get("left_alpha", 170))
    img = gradient(img, "bottom", 112)
    d = ImageDraw.Draw(img, "RGBA")

    d.text((62, 50), "SONAGI", font=F["micro"], fill=(CREAM[0], CREAM[1], CREAM[2], 230))
    d.text((62, 76), deck["label"].upper(), font=F["micro"], fill=(CREAM[0], CREAM[1], CREAM[2], 205))
    d.text((963, 50), f"{i+1:02d}/07", font=F["micro"], fill=(CREAM[0], CREAM[1], CREAM[2], 220))

    text_x = 62
    text_y = 154 if i == 0 else 186
    kicker = s["kicker"]
    if i == 6 and kicker.upper() == "CTA":
        kicker = "À faire"
    d.text((text_x, text_y), kicker.upper(), font=F["kicker"], fill=YELLOW)
    title_font = F["title_sm"] if len(s["title"]) > 34 else F["title"]
    y = draw_text(d, (text_x, text_y + 52), s["title"], title_font, CREAM, s.get("title_w", 700), 5)
    draw_text(d, (text_x + 2, y + 16), s["body"], F["body_sm"], CREAM, s.get("body_w", 610), 7)

    paste_diagram(img, s.get("visual"))
    draw_cta_bar(d, deck, i, s)

    out = ROOT / deck["slug"] / f"slide-{i+1:02d}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=96)
    return out


def contact(paths, out):
    sheet = Image.new("RGB", (216 * 7, 270), CREAM)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        im.thumbnail((216, 270), Image.LANCZOS)
        sheet.paste(im, (i * 216, 0))
    sheet.save(out, quality=92)


def preview(deck, paths):
    figs = "".join(f'<figure><img src="{p.name}"><figcaption>{i+1}</figcaption></figure>' for i, p in enumerate(paths))
    doc = f"""<!doctype html><html lang="fr"><meta charset="utf-8"><title>{html.escape(deck['title'])}</title>
<style>body{{margin:0;background:#f8f1e6;color:#1c1815;font-family:"American Typewriter",Courier,monospace}}header{{padding:34px 44px}}h1{{font-family:Georgia,serif;font-size:38px;margin:0 0 8px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;padding:0 44px 60px}}img{{width:100%;box-shadow:0 18px 40px rgba(0,0,0,.18)}}figure{{margin:0}}figcaption{{padding:8px 0}}</style>
<header><h1>{html.escape(deck['title'])}</h1><p>{html.escape(deck['note'])}</p></header><main class="grid">{figs}</main></html>"""
    (ROOT / deck["slug"] / "carousel-preview.html").write_text(doc)


IMG = REF / "assets/images"
DIA = REF / "assets/diagrams"

decks = [
    {
        "slug": "01-ph-savon-marseille",
        "label": "manteau acide",
        "title": "Le savon de Marseille n'est pas neutre pour ton visage",
        "note": "Article: Le pH de la peau. Angle: mistake correction.",
        "shop_cta": "Shoppe un nettoyant low pH via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/basics/fr/le-ph-de-la-peau/",
        "slides": [
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "Erreur française", "title": "Le savon de Marseille est trop haut pour ton visage.", "body": "Ta peau vit autour de pH 4,5 à 5,5. Le savon classique peut monter vers 9 ou 10.", "cta": "Sauvegarde avant de laver ton visage au savon."},
            {"bg": IMG/"basics/_originals/skin-ph-asma.png", "kicker": "Le terrain", "title": "Ta peau est acide. C'est voulu.", "body": "Ce manteau acide aide la barrière, les enzymes de réparation et l'équilibre microbien.", "visual": DIA/"le-ph-de-la-peau.webp", "cta": "Acide ne veut pas dire agressif."},
            {"bg": IMG/"techniques/double-cleansing-hero.webp", "kicker": "Le piège", "title": "Plus ça mousse, plus ça peut décaper.", "body": "La sensation de propre peut cacher une barrière déplacée vers le basique pendant plusieurs heures.", "cta": "Ne confonds pas propre et déstabilisé."},
            {"bg": IMG/"routines/routine-homme-body-3.webp", "kicker": "La règle", "title": "Cherche pH bas, pas peau qui crisse.", "body": "Les nettoyants K-beauty doux vivent souvent autour de pH 5 à 6. C'est la logique, pas le folklore.", "cta": "Le bon nettoyant laisse la peau souple."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Le signal", "title": "Si ça tire après le rinçage, ce n'est pas normal.", "body": "Tiraillement, rougeur, picotement: la peau te dit souvent que le nettoyage a été trop haut ou trop fort.", "cta": "Change le geste avant d'ajouter un sérum."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "Le choix", "title": "La routine commence par respecter le pH.", "body": "Baume ou huile le soir si SPF, puis nettoyant doux. Le reste marche mieux quand la barrière n'est pas contrariée.", "cta": "Dernière slide: les liens utiles."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "À faire", "title": "Commence par le nettoyant, pas par dix actifs.", "body": "Le bon pH rend la routine plus tolérable, surtout si ta peau rougit ou tire.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "02-ph-manteau-acide",
        "label": "barrière invisible",
        "title": "Le manteau acide est la sécurité invisible de ta peau",
        "note": "Article: Le pH de la peau. Angle: mechanism.",
        "shop_cta": "Shoppe un toner apaisant via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/basics/fr/le-ph-de-la-peau/",
        "slides": [
            {"bg": IMG/"sections/comprendre-hero.webp", "kicker": "Mécanisme", "title": "Ta peau se défend avec de l'acidité.", "body": "Pas une acidité qui brûle. Une acidité fine, biologique, qui garde la surface stable.", "cta": "Garde cette slide si ta peau réagit à tout."},
            {"bg": IMG/"basics/_originals/skin-ph-asma.png", "kicker": "La zone", "title": "4,5 à 5,5 : c'est la plage utile.", "body": "Dans cette zone, la couche cornée fonctionne mieux et la barrière se répare plus proprement.", "visual": DIA/"le-ph-de-la-peau.webp", "cta": "Un chiffre peut expliquer beaucoup de tiraillements."},
            {"bg": IMG/"ingredients/heartleaf-body-1.webp", "kicker": "Après nettoyage", "title": "Un toner doux aide à revenir au calme.", "body": "Il ne doit pas piquer. Il doit remettre de l'eau, du confort, et préparer la suite.", "cta": "Le toner n'est pas une punition alcoolisée."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Texture", "title": "Une peau équilibrée reflète mieux la lumière.", "body": "Le glow commence rarement par un highlighter. Il commence par une surface qui retient l'eau.", "cta": "Le pH est moins glamour, mais plus fondamental."},
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "Erreur", "title": "Le citron, le savon, l'eau chaude : trio faux ami.", "body": "Naturel ne veut pas dire compatible avec ton manteau acide.", "cta": "Simple ne veut pas dire brutal."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Le lien", "title": "pH et barrière travaillent ensemble.", "body": "Quand le pH grimpe, la barrière devient plus perméable. Quand la barrière fuit, tout pique plus vite.", "cta": "Lis l'article complet pour le mécanisme."},
            {"bg": IMG/"cta/cta-community.webp", "kicker": "À faire", "title": "Teste ta routine avant de la durcir.", "body": "Si ta peau tire, commence par le nettoyage et le toner, pas par un actif plus fort.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "03-niacinamide-lente",
        "label": "actif patient",
        "title": "La niacinamide ne fait pas du bruit. Elle travaille.",
        "note": "Article: Niacinamide. Angle: expectation reset.",
        "shop_cta": "Shoppe le rituel niacinamide via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/fr/niacinamide/",
        "slides": [
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Contre buzz", "title": "Si tu veux un effet en trois jours, ce n'est pas elle.", "body": "La niacinamide se mesure plutôt en semaines: barrière, taches, sébum, confort.", "cta": "Sauvegarde avant de jeter ton sérum trop tôt."},
            {"bg": IMG/"basics/ppm-hero.webp", "kicker": "La dose", "title": "2 à 5 % suffit souvent.", "body": "Plus n'est pas toujours mieux. L'intérêt est la régularité, pas la brûlure.", "cta": "Un actif intelligent n'a pas besoin de crier."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Barrière", "title": "Elle aide la peau à refaire ses lipides.", "body": "C'est pour ça qu'elle parle aux peaux ternes, grasses, tachées ou un peu irritables.", "visual": DIA/"niacinamide-mechanism.webp", "cta": "La barrière est souvent le vrai sujet."},
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Sébum", "title": "Elle ne supprime pas le sébum. Elle le module.", "body": "Le but n'est pas d'assécher. Le but est d'obtenir une brillance moins chaotique.", "cta": "La peau grasse aussi a besoin de douceur."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Taches", "title": "Elle agit aussi sur le transfert du pigment.", "body": "Pas comme un peeling brutal. Plutôt comme une correction lente et mieux tolérée.", "cta": "La patience fait partie de la formule."},
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "Routine", "title": "Après toner, avant crème et SPF.", "body": "Le matin, elle se place bien sous protection solaire. Le soir, elle soutient la barrière.", "cta": "Dernière slide: choisir sans forcer."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "À faire", "title": "Choisis la niacinamide si ta peau doit se stabiliser.", "body": "Pas si tu veux décaper. Oui si tu veux réguler, éclaircir doucement et renforcer.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "04-niacinamide-pores",
        "label": "pores visibles",
        "title": "Tes pores ne se ferment pas. Ils se négocient.",
        "note": "Article: Niacinamide. Angle: pores/sebum myth.",
        "shop_cta": "Shoppe le rituel niacinamide via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/fr/niacinamide/",
        "slides": [
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "Mythe", "title": "Un pore n'est pas une porte.", "body": "Il ne s'ouvre pas et ne se ferme pas à volonté. Il devient surtout plus ou moins visible.", "cta": "Garde cette phrase pour les promesses absurdes."},
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Pourquoi", "title": "Sébum + kératine + lumière = pore visible.", "body": "Quand la surface est encombrée ou déshydratée, le relief accroche plus la lumière.", "visual": DIA/"le-sebum.webp", "cta": "La visibilité n'est pas une fatalité."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Le levier", "title": "La niacinamide aide à réguler sans punir.", "body": "Elle vise le sébum, la barrière et l'inflammation légère. C'est plus fin qu'un produit qui décape.", "visual": DIA/"niacinamide-mechanism.webp", "cta": "Réguler bat assécher."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Hydratation", "title": "Une peau déshydratée montre plus de texture.", "body": "Avant de chercher plus fort, remets de l'eau et protège le film de surface.", "cta": "Le pore visible n'est pas toujours gras."},
            {"bg": IMG/"ingredients/heartleaf-body-1.webp", "kicker": "Tolérance", "title": "Si ça pique, tu perds le bénéfice.", "body": "Un actif utile devient inutile si la routine autour rend la peau nerveuse.", "cta": "Le calme est une stratégie."},
            {"bg": IMG/"sections/comprendre-hero.webp", "kicker": "Attente", "title": "On vise moins visible, pas invisible.", "body": "Le but réaliste: surface plus régulière, brillance mieux tenue, taches qui s'installent moins.", "cta": "Pas de filtre, juste une meilleure logique."},
            {"bg": IMG/"cta/cta-newsletter.webp", "kicker": "À faire", "title": "Construis autour du pore, pas contre lui.", "body": "Nettoyage doux, niacinamide, hydratation, SPF. C'est moins spectaculaire, plus durable.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "05-snail-mucin-tabou",
        "label": "actif bizarre",
        "title": "La mucine d'escargot est étrange. C'est aussi pour ça qu'elle marche.",
        "note": "Article: Snail mucin. Angle: taboo to education.",
        "shop_cta": "Shoppe la mucine COSRX via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/fr/snail-mucin/",
        "slides": [
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Tabou", "title": "Oui, c'est de la bave. Non, ce n'est pas sale.", "body": "La mucine cosmétique est filtrée, purifiée, formulée. Le mot dérange plus que la texture.", "cta": "Sauvegarde si le nom t'a toujours bloquée."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "Texture", "title": "Elle forme un film hydratant très fin.", "body": "Pas une colle. Un voile qui aide la surface à garder l'eau et à paraître plus lisse.", "visual": DIA/"snail-mucin-mechanism.webp", "cta": "Le glow vient souvent du film."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Pour qui", "title": "Peau déshydratée, post-boutons, barrière fatiguée.", "body": "Elle parle aux peaux qui veulent du confort sans gras lourd.", "cta": "Pas besoin d'en mettre trop."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Le piège", "title": "Ce n'est pas un traitement miracle de l'acné.", "body": "Elle peut aider le confort et l'aspect post-bouton, mais elle ne remplace pas un traitement médical.", "cta": "Ne demande pas à un hydratant d'être un médicament."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "Timing", "title": "Après toner, avant crème.", "body": "Une ou deux couches fines. Attends une minute si tu veux éviter l'effet collant.", "cta": "La couche fine gagne presque toujours."},
            {"bg": IMG/"sections/ingredient-hero.webp", "kicker": "Attention", "title": "Si tu es allergique aux escargots, évite.", "body": "Et si ta peau réagit facilement, teste sur une petite zone avant de l'installer.", "cta": "Bizarre ne veut pas dire universel."},
            {"bg": IMG/"cta/cta-community.webp", "kicker": "À faire", "title": "Utilise-la comme hydratant intelligent, pas comme miracle.", "body": "Elle brille quand la routine est simple: toner, mucine, crème, SPF le matin.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "06-snail-mucin-post-acne",
        "label": "après bouton",
        "title": "Après un bouton, ta peau ne veut pas forcément un acide.",
        "note": "Article: Snail mucin. Angle: post-acne repair.",
        "shop_cta": "Shoppe la mucine COSRX via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/fr/snail-mucin/",
        "slides": [
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Après-coup", "title": "Le bouton part. La peau reste vexée.", "body": "Rougeur, marque, texture: l'après-bouton est souvent une question de réparation de surface.", "cta": "Sauvegarde avant de ré-exfolier trop vite."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "Le besoin", "title": "Elle veut de l'eau, du calme, du temps.", "body": "La mucine aide surtout comme couche hydratante et confortable, pas comme attaque.", "visual": DIA/"snail-mucin-mechanism.webp", "cta": "Réparer n'est pas décaper."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Erreur", "title": "Acide sur acide peut prolonger l'irritation.", "body": "Quand la barrière est déjà stressée, ajouter de l'intensité peut garder la marque visible plus longtemps.", "cta": "Moins fort peut aller plus vite."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Duo", "title": "Niacinamide + mucine : duo patient.", "body": "L'une soutient la barrière et les taches. L'autre apporte le film hydratant.", "cta": "Pas glamour. Très utile."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Application", "title": "Deux fines couches valent mieux qu'une flaque.", "body": "Sur peau légèrement humide, puis crème. Le collant vient souvent de la dose.", "cta": "La texture doit disparaître, pas étouffer."},
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "SPF", "title": "Sans SPF, la marque s'accroche.", "body": "Le matin, la réparation post-bouton finit toujours par protection solaire.", "cta": "La lumière décide souvent de la tache."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "À faire", "title": "Pour les marques, commence par calmer.", "body": "Si l'acné est active ou douloureuse, ce n'est pas le rôle d'un cosmétique: demande un avis médical.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "07-slugging-pas-pour-tout-le-monde",
        "label": "scellage de nuit",
        "title": "Le slugging n'est pas pour toutes les peaux.",
        "note": "Article: Slugging. Angle: audience filter.",
        "shop_cta": "Shoppe le rituel barrière via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/techniques/fr/slugging/",
        "slides": [
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Filtre", "title": "Si ta peau est acnéique active, prudence.", "body": "Le slugging scelle. S'il scelle trop de sébum, de chaleur ou de bactéries, il peut empirer le confort.", "cta": "Sauvegarde avant de tester la vaseline partout."},
            {"bg": IMG/"techniques/slugging-body.webp", "kicker": "Le principe", "title": "Ce n'est pas hydrater. C'est bloquer l'évaporation.", "body": "Le film occlusif garde l'eau sous lui. Il ne remplace pas le toner, le sérum ou la crème.", "visual": DIA/"slugging-mechanism.webp", "cta": "On scelle ce qui est déjà bien posé."},
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "Pour qui", "title": "Peau sèche, hiver, barrière fatiguée.", "body": "Là, le geste peut être très utile. Surtout en fine couche, pas en masque gras.", "cta": "Le slugging est une couverture, pas un traitement."},
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "À éviter", "title": "Pas sur inflammation active.", "body": "Boutons douloureux, folliculite, zone T très grasse: on adapte ou on évite.", "cta": "La tendance ne connaît pas ta peau."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "Avant", "title": "Hydrate d'abord, scelle ensuite.", "body": "Une peau sèche sous vaseline reste sèche. Elle perd juste moins vite.", "cta": "La préparation fait le résultat."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "Fréquence", "title": "Une à deux nuits suffisent souvent.", "body": "Pas besoin d'en faire une identité. Observe la peau le matin.", "cta": "Rituel intelligent, pas automatisme."},
            {"bg": IMG/"cta/cta-newsletter.webp", "kicker": "À faire", "title": "Teste en zone sèche avant tout le visage.", "body": "Si ça chauffe, gratte ou crée des boutons, arrête. Le bon soin doit simplifier la peau.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "08-glass-skin-pas-huile",
        "label": "mool-gwang",
        "title": "Glass skin ne veut pas dire visage huileux.",
        "note": "Article: Glass skin. Angle: myth correction.",
        "shop_cta": "Shoppe le rituel glow via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/techniques/fr/glass-skin/",
        "slides": [
            {"bg": IMG/"techniques/skin-flooding-body-1.webp", "kicker": "Mythe", "title": "Le glow K-beauty n'est pas une couche de gras.", "body": "Mool-gwang parle d'eau et de lumière, pas d'une surface saturée.", "cta": "Sauvegarde si ta routine brille mais tire."},
            {"bg": IMG/"techniques/glass-skin-2.webp", "kicker": "Optique", "title": "Une peau hydratée reflète autrement.", "body": "Quand la couche cornée retient l'eau, la lumière se pose plus régulièrement.", "visual": DIA/"glass-skin-mechanism.webp", "cta": "Le glow est d'abord une surface."},
            {"bg": IMG/"techniques/double-cleansing-hero.webp", "kicker": "Base", "title": "Le soir commence par retirer SPF et résidus.", "body": "Sans nettoyage doux, tu empiles du soin sur du bruit.", "cta": "La glass skin commence au lavabo."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Actifs", "title": "Niacinamide, mucine, heartleaf : couches fines.", "body": "Le secret n'est pas le nombre de produits. C'est leur place, leur dose, leur tolérance.", "cta": "Une peau saturée n'est pas une peau hydratée."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Barrière", "title": "Sans barrière, le glow devient rougeur.", "body": "Si tout pique, arrête de poursuivre la brillance. Répare le confort.", "cta": "La lumière vient après le calme."},
            {"bg": IMG/"sections/routine-hero.webp", "kicker": "Règle", "title": "Trois gestes bien posés valent dix étapes.", "body": "Nettoyage doux, hydratation, crème ou SPF. Ajoute seulement ce que ta peau tolère.", "cta": "Le rituel doit tenir dans la vraie vie."},
            {"bg": IMG/"cta/cta-community.webp", "kicker": "À faire", "title": "Cherche l'eau-lumière, pas l'effet gras.", "body": "Si tu veux savoir quelle version du glow convient à ta peau, commence par le quiz.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "09-acne-cycle",
        "label": "acné adulte",
        "title": "Le bouton qui revient chaque mois n'est pas un hasard.",
        "note": "Article: Acné hormonale. Angle: cycle pattern.",
        "shop_cta": "Shoppe les soins apaisants via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/conditions/fr/acne-hormonale/",
        "slides": [
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "Pattern", "title": "Même zone, même semaine, même bouton.", "body": "Quand ça revient autour du cycle, la peau raconte souvent une histoire hormonale.", "cta": "Sauvegarde si ton menton a un calendrier."},
            {"bg": IMG/"sections/technique-hero.webp", "kicker": "Zone", "title": "Bas du visage, mâchoire, menton.", "body": "Ce sont des zones fréquentes dans l'acné adulte hormonale, surtout quand la poussée est inflammatoire.", "visual": DIA/"acne-hormonale-mechanism.webp", "cta": "Observer le pattern aide déjà."},
            {"bg": IMG/"basics/hormones-phase-6-real.webp", "kicker": "Mécanisme", "title": "Les androgènes stimulent le sébum.", "body": "Plus de sébum, plus de kératine, plus de risque de microcomédon. Ce n'est pas une question de saleté.", "visual": DIA/"le-sebum.webp", "cta": "Laver plus fort n'est pas la réponse."},
            {"bg": IMG/"ingredients/heartleaf-body-1.webp", "kicker": "Cosmétique", "title": "Les soins calment le terrain, ils ne traitent pas l'hormone.", "body": "Heartleaf, centella, niacinamide peuvent aider la tolérance et la barrière.", "cta": "Le rôle du soin doit rester honnête."},
            {"bg": IMG/"techniques/double-cleansing-2.webp", "kicker": "Rituel", "title": "Nettoyer doux, surtout les soirs de SPF.", "body": "Le nettoyage doit sortir les résidus sans transformer la barrière en zone rouge.", "cta": "La régularité compte plus que la force."},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Alerte", "title": "Douleur, nodules, cicatrices : avis médical.", "body": "L'acné modérée à sévère relève du dermatologue. Le cosmétique accompagne, il ne remplace pas.", "cta": "Sonagi ne vend pas de miracle médical."},
            {"bg": IMG/"cta/cta-diagnostic.webp", "kicker": "À faire", "title": "Repère le cycle avant de changer toute ta routine.", "body": "Note la semaine, la zone, la douleur, puis construis une routine qui respecte la barrière.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
    {
        "slug": "10-acne-ne-pas-decaper",
        "label": "peau inflammée",
        "title": "Une peau acnéique n'a pas besoin d'être punie.",
        "note": "Article: Acné hormonale. Angle: routine mistake.",
        "shop_cta": "Shoppe les soins apaisants via le tag boutique IG/TikTok Shop.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/conditions/fr/acne-hormonale/",
        "slides": [
            {"bg": IMG/"sections/basic-hero.webp", "kicker": "Hot take", "title": "Décaper l'acné peut nourrir l'inflammation.", "body": "Quand la peau est déjà en conflit, trop laver ou trop exfolier peut prolonger le stress.", "cta": "Sauvegarde avant ton prochain gommage."},
            {"bg": IMG/"ingredients/niacinamide-hero.webp", "kicker": "Objectif", "title": "On régule. On ne cherche pas le désert.", "body": "Le sébum protège aussi. Le but est de calmer l'excès, pas d'effacer la peau.", "visual": DIA/"niacinamide-mechanism.webp", "cta": "Une peau sèche peut être encore plus nerveuse."},
            {"bg": IMG/"ingredients/centella-asiatica-hero.webp", "kicker": "Calme", "title": "La centella parle aux peaux qui s'enflamment vite.", "body": "Peu d'ingrédients, texture simple, tolérance. C'est moins sexy qu'un peeling, souvent plus utile.", "cta": "Le calme est un actif."},
            {"bg": IMG/"ingredients/heartleaf-body-1.webp", "kicker": "Rougeurs", "title": "Heartleaf aide quand la peau brille et rougit.", "body": "Le geste intéressant: apaiser pendant qu'on régule.", "visual": DIA/"heartleaf-mechanism.webp", "cta": "Pas besoin de faire mal pour agir."},
            {"bg": IMG/"routines/routine-homme-body-1.webp", "kicker": "Nettoyage", "title": "Un nettoyant doux vaut mieux que deux agressifs.", "body": "Le soir, retire SPF et pollution. Mais la peau ne doit pas crisser ensuite.", "cta": "Propre n'est pas décapé."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Barrière", "title": "Si tout pique, pause sur les actifs.", "body": "Une barrière abîmée transforme même de bons produits en problème.", "visual": DIA/"la-barriere-cutanee.webp", "cta": "Le reset est parfois la stratégie."},
            {"bg": IMG/"cta/cta-newsletter.webp", "kicker": "À faire", "title": "Construis une routine qui calme avant de corriger.", "body": "Si l'acné est douloureuse ou persistante, avis médical. Pour le reste, commence par la tolérance.", "cta": "Placeholder shop + quiz + article."},
        ],
    },
]


def main():
    for deck in decks:
        seen = set()
        for s in deck["slides"]:
            bg = str(s["bg"])
            if bg in seen:
                raise ValueError(f"Repeated background inside carousel {deck['slug']}: {bg}")
            seen.add(bg)
        folder = ROOT / deck["slug"]
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
        paths = [render_slide(deck, i, s) for i, s in enumerate(deck["slides"])]
        contact(paths, folder / "contact-sheet.jpg")
        preview(deck, paths)
        (folder / "SPEC.md").write_text(
            f"# {deck['title']}\n\n"
            "- V5 correction: one centered full-bleed background photo only.\n"
            "- The only allowed overlay is a small centered lower-space diagram from Sonagi Reference.\n"
            "- No product packshot or second lifestyle photo is pasted on top of the background.\n"
            "- No diagram/chart backgrounds; only crop-safe photos or still lifes.\n"
            "- Each slide must have a different visual family within the carousel, not only a different filename.\n"
            "- Images selected first from the Sonagi Reference article, then from adjacent Sonagi archive material.\n"
            "- Final CTA includes shop tag route, quiz URL, and full article URL.\n"
        )

    cards = []
    for deck in decks:
        cards.append(f'<article><h2><a href="{deck["slug"]}/carousel-preview.html">{html.escape(deck["title"])}</a></h2><a href="{deck["slug"]}/carousel-preview.html"><img src="{deck["slug"]}/contact-sheet.jpg"></a><p>{html.escape(deck["note"])}</p></article>')
    bank = f"""<!doctype html><html lang="fr"><meta charset="utf-8"><title>Sonagi Launch Auteur carousel bank</title>
<style>body{{margin:0;background:#f8f1e6;color:#1c1815;font-family:"American Typewriter",Courier,monospace}}header{{padding:42px 52px 12px}}h1{{font-family:Georgia,serif;font-size:48px;margin:0 0 10px}}main{{padding:20px 52px 70px;display:grid;gap:34px}}article{{border-top:1px solid rgba(28,24,21,.22);padding-top:24px}}h2{{font-family:Georgia,serif;font-size:28px}}img{{width:100%;box-shadow:0 18px 40px rgba(0,0,0,.14)}}a{{color:#1c1815}}</style>
<header><h1>Sonagi Launch Auteur carousel bank</h1><p>Launch draft: full-bleed photo, optional centered diagram, shop placeholder, quiz link, full article link.</p></header><main>{''.join(cards)}</main></html>"""
    (ROOT / "bank-preview.html").write_text(bank)


if __name__ == "__main__":
    main()
