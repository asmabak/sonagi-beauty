from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
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
    "micro": font(FONT_TYPE, 20),
    "kicker": font(FONT_TYPE, 25),
    "title": font(FONT_SERIF_BOLD, 68),
    "title_sm": font(FONT_SERIF_BOLD, 56),
    "body": font(FONT_TYPE, 32),
    "body_sm": font(FONT_TYPE, 28),
    "cta": font(FONT_TYPE, 26),
}


def cover(path, anchor="center"):
    img = Image.open(path).convert("RGB")
    scale = max(W / img.width, H / img.height)
    img = img.resize((math.ceil(img.width * scale), math.ceil(img.height * scale)), Image.LANCZOS)
    if anchor == "left":
        left = 0
    elif anchor == "right":
        left = img.width - W
    else:
        left = (img.width - W) // 2
    top = (img.height - H) // 2
    img = img.crop((left, top, left + W, top + H))
    img = ImageOps.autocontrast(img)
    return img


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
            a = int(alpha * max(0, (y - 720) / 520))
            for x in range(W):
                pix[x, y] = (0, 0, 0, a)
    return Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")


def paste_visual(canvas, path, mode):
    if not path:
        return
    src = Image.open(path).convert("RGBA")
    if mode == "diagram":
        bw, bh, x, y = 500, 374, 530, 700
        src.thumbnail((bw, bh), Image.LANCZOS)
        veil = Image.new("RGBA", (src.width + 34, src.height + 34), (248, 241, 230, 206))
        veil.alpha_composite(src, (17, 17))
        canvas.paste(veil, (x, y), veil)
    elif mode == "product":
        bw, bh, x, y = 360, 360, 650, 690
        src.thumbnail((bw, bh), Image.LANCZOS)
        glow = Image.new("RGBA", (src.width + 80, src.height + 80), (248, 241, 230, 66))
        glow = glow.filter(ImageFilter.GaussianBlur(22))
        canvas.paste(glow, (x - 40, y - 40), glow)
        canvas.paste(src, (x, y), src)


def render_slide(deck, i, s):
    img = cover(s["bg"], s.get("anchor", "center"))
    img = gradient(img, "left", s.get("left_alpha", 170))
    img = gradient(img, "bottom", 125)
    d = ImageDraw.Draw(img, "RGBA")

    d.text((58, 52), "SONAGI", font=F["micro"], fill=(CREAM[0], CREAM[1], CREAM[2], 230))
    d.text((58, 82), deck["label"].upper(), font=F["micro"], fill=(CREAM[0], CREAM[1], CREAM[2], 205))
    d.text((958, 52), f"{i+1:02d}/07", font=F["micro"], fill=(CREAM[0], CREAM[1], CREAM[2], 220))

    d.text((58, 222), s["kicker"].upper(), font=F["kicker"], fill=YELLOW)
    title_font = F["title_sm"] if len(s["title"]) > 34 else F["title"]
    y = draw_text(d, (58, 280), s["title"], title_font, CREAM, s.get("title_w", 720), 7)
    draw_text(d, (60, y + 24), s["body"], F["body"], CREAM, s.get("body_w", 650), 8)

    paste_visual(img, s.get("visual"), s.get("visual_mode", "diagram"))

    d.rectangle((48, 1210, 1032, 1276), fill=(28, 24, 21, 176))
    cta = s["cta"]
    if len(cta) > 58 and " : " in cta:
        lead, slug = cta.split(" : ", 1)
        d.text((72, 1221), f"{lead} :", font=F["micro"], fill=CREAM)
        d.text((72, 1248), slug, font=F["micro"], fill=CREAM)
    else:
        d.text((72, 1230), cta, font=F["cta"], fill=CREAM)
    d.text((870, 1230), "sonagi", font=F["cta"], fill=PEACH)

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
        "slug": "01-skin-flooding-anua",
        "label": "hydratation virale",
        "title": "Skin flooding : TikTok l'a découvert, Séoul l'avait déjà codé",
        "note": "No-card Auteur-style version, one image per slide, direct Anua CTA.",
        "slides": [
            {"bg": IMG/"techniques/skin-flooding-hero.webp", "kicker": "Tendance", "title": "Tu appelles ça skin flooding. En Corée, c'était déjà une méthode.", "body": "Le buzz n'est pas nouveau. Ce qui compte, c'est pourquoi ta peau boit mieux quand elle reste humide.", "cta": "Sauvegarde avant d'empiler sept couches au hasard.", "anchor": "left"},
            {"bg": IMG/"techniques/skin-flooding-body-1.webp", "kicker": "Le besoin", "title": "Ta peau ne manque pas toujours de crème.", "body": "Souvent, elle manque d'eau retenue au bon moment. Une couche aqueuse sur peau humide limite l'évaporation.", "visual": DIA/"skin-flooding-mechanism.webp", "cta": "Slide suivante : le geste qui change tout.", "anchor": "center"},
            {"bg": IMG/"ingredients/acide-hyaluronique-hero.webp", "kicker": "La règle", "title": "Ne laisse pas sécher entre les couches.", "body": "Dix à vingt secondes. Pas plus. Si la peau sèche, tu perds l'effet d'occlusion humectante.", "cta": "Teste trois couches avant d'en faire sept.", "anchor": "right"},
            {"bg": IMG/"edito/top-picks-2026-06/top-picks-toners-stilllife.webp", "kicker": "Le piège", "title": "Le mauvais toner ruine la méthode.", "body": "Pas d'alcool, pas d'astringent agressif, pas de parfum qui pique. Le toner doit être aqueux, doux, empilable.", "visual": IMG/"products/anua/anua-heartleaf-77-soothing-toner.webp", "visual_mode": "product", "cta": "Cherche une texture qui disparaît, pas qui colle."},
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "Pour qui", "title": "Peau qui tire, avion, chauffage, stress.", "body": "Le skin flooding parle surtout aux peaux déshydratées. Une peau grasse peut aussi manquer d'eau.", "visual": DIA/"skin-flooding-mechanism.webp", "cta": "Si ta peau brille et tire, garde cette slide."},
            {"bg": IMG/"ingredients/heartleaf-hero.webp", "kicker": "Le choix", "title": "Prends un toner qui calme autant qu'il hydrate.", "body": "Heartleaf aide les peaux réactives à tolérer le geste. C'est pour ça que l'Anua 77 est devenu un standard.", "visual": IMG/"products/anua/anua-heartleaf-77-soothing-toner.webp", "visual_mode": "product", "cta": "Dernière slide : le lien direct.", "anchor": "right"},
            {"bg": IMG/"products/anua/anua-heartleaf-77-soothing-toner.webp", "kicker": "CTA", "title": "Le produit pivot : Anua Heartleaf 77 Toner.", "body": "À utiliser après le nettoyage, sur peau encore humide, avant sérum et crème.", "cta": "Va au produit : /produits/anua-heartleaf-77-toner", "anchor": "center"},
        ],
    },
    {
        "slug": "02-double-nettoyage-boj",
        "label": "nettoyage du soir",
        "title": "Le double nettoyage n'est pas une routine de plus",
        "note": "No-card Auteur-style version, SPF/maquillage logic, Beauty of Joseon CTA.",
        "slides": [
            {"bg": IMG/"techniques/double-cleansing-hero.webp", "kicker": "Contre-intuitif", "title": "Ta mousse seule ne retire pas vraiment ton SPF.", "body": "Pas parce qu'elle est mauvaise. Parce que l'eau ne dissout pas bien ce qui aime le gras.", "cta": "Sauvegarde si tu portes SPF ou maquillage.", "anchor": "left"},
            {"bg": IMG/"edito/ozempic-face-kbeauty/ozempic-skin-context.webp", "kicker": "La peau du soir", "title": "Ton visage porte deux familles de résidus.", "body": "Sébum oxydé, SPF, maquillage d'un côté. Sueur, poussières, pollution hydrosoluble de l'autre.", "visual": DIA/"double-cleansing-mechanism.webp", "cta": "Un seul nettoyant force souvent le frottement."},
            {"bg": IMG/"products/beauty-of-joseon/beauty-of-joseon-radiance-cleansing-balm.webp", "kicker": "Étape 1", "title": "Le baume dissout le gras sans décaper.", "body": "Sur peau sèche, il fond avec les paumes et soulève SPF, sébum et maquillage longue tenue.", "cta": "Le bon baume fait le travail mécanique."},
            {"bg": IMG/"techniques/double-cleansing-2.webp", "kicker": "Étape 2", "title": "La mousse douce retire l'émulsion.", "body": "Le second geste doit respecter le pH de la peau. L'eau brûlante et le savon classique cassent l'intérêt du rituel.", "visual": DIA/"double-cleansing-mechanism.webp", "cta": "Double nettoyage ne veut pas dire double agression.", "anchor": "right"},
            {"bg": IMG/"edito/top-picks-2026-06/top-picks-how-toners-work.webp", "kicker": "Pour qui", "title": "Pas tous les matins. Surtout les soirs de SPF.", "body": "Le matin, inutile. Le soir, essentiel si tu as porté protection solaire, pollution urbaine ou maquillage.", "cta": "Si ta peau tire après, le geste 2 est trop fort."},
            {"bg": IMG/"brands/beauty-of-joseon-body-1.webp", "kicker": "Le choix", "title": "Commence par un baume qui émulsionne proprement.", "body": "Le Beauty of Joseon Radiance Cleansing Balm est le geste 1 Sonagi : il fond, masse, puis se rince au lait.", "visual": IMG/"products/beauty-of-joseon/beauty-of-joseon-radiance-cleansing-balm.webp", "visual_mode": "product", "cta": "Dernière slide : le lien direct."},
            {"bg": IMG/"brands/beauty-of-joseon-hero.webp", "kicker": "CTA", "title": "Le geste 1 : Beauty of Joseon Radiance Balm.", "body": "À utiliser le soir, sur peau sèche, avant ton nettoyant à pH bas.", "visual": IMG/"products/beauty-of-joseon/beauty-of-joseon-radiance-cleansing-balm.webp", "visual_mode": "product", "cta": "Va au produit : /produits/beauty-of-joseon-radiance-cleansing-balm", "anchor": "right"},
        ],
    },
    {
        "slug": "03-barriere-centella",
        "label": "barrière cutanée",
        "title": "Ta barrière n'a pas besoin de courage, elle a besoin de silence",
        "note": "No-card Auteur-style version, barrier education, Skin1004 CTA.",
        "slides": [
            {"bg": IMG/"basics/la-barriere-cutanee-card-v3.webp", "kicker": "Signal faible", "title": "Si tout pique, ce n'est pas que ta peau est capricieuse.", "body": "C'est souvent la barrière qui fuit. Et sur un mur fissuré, plus d'actifs ne réparent rien.", "cta": "Sauvegarde avant d'ajouter un nouveau sérum."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Le besoin", "title": "Briques, ciment, eau retenue.", "body": "Les cellules sont les briques. Les lipides sont le ciment. Quand le ciment manque, l'eau sort et les irritants entrent.", "visual": DIA/"la-barriere-cutanee.webp", "cta": "La peau qui tire demande moins, pas plus.", "anchor": "right"},
            {"bg": IMG/"basics/reparer-barriere-hero.webp", "kicker": "Le piège", "title": "Acides + rétinol + gommage : le mur prend tout.", "body": "La barrière abîmée ne tolère plus ce qu'elle supportait avant. Ce n'est pas une faiblesse, c'est un signal.", "cta": "Deux semaines simples valent mieux qu'un placard plein."},
            {"bg": IMG/"ingredients/snail-mucin-body-1.webp", "kicker": "Ce qu'elle veut", "title": "Calmer d'abord. Sceller ensuite.", "body": "Toner doux, ampoule apaisante, crème. Le minimum assez longtemps pour que le ciment se refasse.", "visual": DIA/"reparer-la-barriere-cutanee-mechanism.webp", "cta": "Si ça chauffe, enlève une étape."},
            {"bg": IMG/"ingredients/centella-asiatica-hero.webp", "kicker": "Pourquoi centella", "title": "Parce que la peau rouge veut du calme.", "body": "La centella est le réflexe K-beauty quand la peau réagit vite : peu d'ingrédients, beaucoup de tolérance.", "visual": IMG/"products/skin1004/skin1004-madagascar-centella-ampoule.webp", "visual_mode": "product", "cta": "Garde la formule courte."},
            {"bg": IMG/"products/skin1004/skin1004-madagascar-centella-ampoule.webp", "kicker": "Le choix", "title": "Une ampoule, pas une punition.", "body": "Skin1004 Madagascar Centella Ampoule : un geste simple pour remettre la routine au calme.", "cta": "Dernière slide : le lien direct."},
            {"bg": IMG/"ingredients/centella-asiatica-1.webp", "kicker": "CTA", "title": "Le produit calme : Skin1004 Centella Ampoule.", "body": "À poser après nettoyage, avant crème, surtout quand la peau devient rouge ou inconfortable.", "visual": IMG/"products/skin1004/skin1004-madagascar-centella-ampoule.webp", "visual_mode": "product", "cta": "Va au produit : /produits/skin1004-madagascar-centella-ampoule"},
        ],
    },
    {
        "slug": "04-sebum-heartleaf",
        "label": "peau qui brille",
        "title": "La peau qui brille n'est pas sale",
        "note": "No-card Auteur-style version, sebum education, Anua CTA.",
        "slides": [
            {"bg": IMG/"basics/le-sebum-hero-v3.webp", "kicker": "Hot take", "title": "Plus tu assèches ta peau grasse, plus elle négocie.", "body": "Le sébum n'est pas une saleté. C'est une couche protectrice. Le but, c'est réguler, pas exterminer.", "cta": "Sauvegarde si tu matifies toute la journée.", "anchor": "left"},
            {"bg": IMG/"basics/le-sebum-card-v3.webp", "kicker": "Le besoin", "title": "Le sébum sort d'une usine sous le pore.", "body": "Il remonte le long du follicule, se mélange aux lipides et forme le film hydrolipidique.", "visual": DIA/"le-sebum.webp", "cta": "Briller un peu n'est pas échouer."},
            {"bg": IMG/"conditions/acne-hormonale-body-1.webp", "kicker": "Le cercle", "title": "Trop laver peut relancer la brillance.", "body": "Eau chaude, savon alcalin, exfoliation quotidienne : la surface sèche, la peau compense.", "cta": "Ne confonds pas propre et décapé."},
            {"bg": IMG/"ingredients/heartleaf-body-1.webp", "kicker": "Ce qu'elle veut", "title": "Un actif qui calme pendant qu'il régule.", "body": "Heartleaf vise rougeurs, inconfort et excès de sébum sans transformer la routine en traitement brutal.", "visual": DIA/"heartleaf-mechanism.webp", "cta": "La peau grasse aussi a besoin de douceur."},
            {"bg": IMG/"products/anua/anua-heartleaf-77-soothing-toner.webp", "kicker": "Le dosage", "title": "77 %, ce n'est pas une décoration d'étiquette.", "body": "Anua a fait de l'herbe-cœur le cœur de la formule. Texture aqueuse, facile à placer matin ou soir.", "cta": "Commence par réguler le premier geste après nettoyage."},
            {"bg": IMG/"ingredients/heartleaf-hero.webp", "kicker": "Le choix", "title": "Toner d'équilibre, pas lotion décapante.", "body": "Utilise-le quand la peau brille, rougit ou réagit. Si ça pique, ce n'est pas le bon produit pour toi.", "visual": IMG/"products/anua/anua-heartleaf-77-soothing-toner.webp", "visual_mode": "product", "cta": "Dernière slide : le lien direct.", "anchor": "right"},
            {"bg": IMG/"edito/top-picks-2026-06/top-picks-toners-stilllife.webp", "kicker": "CTA", "title": "Le toner équilibre : Anua Heartleaf 77.", "body": "À appliquer après nettoyage, avant sérum.", "visual": IMG/"products/anua/anua-heartleaf-77-soothing-toner.webp", "visual_mode": "product", "cta": "Va au produit : /produits/anua-heartleaf-77-toner"},
        ],
    },
    {
        "slug": "05-sephora-kids-spf",
        "label": "peau jeune",
        "title": "Une fille de douze ans n'a pas besoin d'anti-âge",
        "note": "No-card Auteur-style version, Sephora Kids education, BOJ SPF CTA.",
        "slides": [
            {"bg": IMG/"edito/sephora-kids/sephora-kids-hero-v2.webp", "kicker": "Sujet qui fâche", "title": "Le problème des Sephora Kids, ce n'est pas la crème.", "body": "C'est l'idée qu'une enfant devrait déjà surveiller son visage comme un défaut à corriger.", "cta": "Sauvegarde pour la prochaine liste d'anniversaire.", "anchor": "left"},
            {"bg": IMG/"routines/routine-pre-ado-hero.webp", "kicker": "La peau jeune", "title": "Elle n'a pas de ride à réparer.", "body": "Une peau d'enfant ou de pré-ado a surtout besoin de douceur, de nettoyage simple, et de protection solaire.", "visual": DIA/"routine-pre-ado-puberty-transition.webp", "cta": "Anti-âge à dix ans : mauvais besoin, mauvais message."},
            {"bg": IMG/"edito/sephora-kids/taille-routine-enfant.webp", "kicker": "Le vrai risque", "title": "Trop d'actifs, trop tôt.", "body": "Acides, rétinol, parfums, routines longues : plus de points de friction sur une barrière encore sensible.", "cta": "Une routine d'enfant doit être courte."},
            {"bg": IMG/"routines/routine-enfant-hero-v3.webp", "kicker": "Ce qu'elle veut", "title": "Un nettoyant doux. Une crème. Un SPF.", "body": "Pas une performance devant le miroir. Pas douze étapes. Pas une peur de vieillir.", "cta": "Le meilleur soin, c'est parfois d'en enlever."},
            {"bg": IMG/"products/beauty-of-joseon/beauty-of-joseon-relief-sun-rice-probiotics.webp", "kicker": "Le paradoxe", "title": "Le seul vrai anti-âge est souvent absent.", "body": "Dans les routines virales d'enfants, l'écran solaire manque trop souvent. C'est pourtant le geste le plus utile.", "cta": "On remplace la peur par la protection."},
            {"bg": IMG/"edito/top-picks-2026-06/top-picks-creams-stilllife.webp", "kicker": "Le choix", "title": "Un SPF confortable est celui qu'on remet.", "body": "Beauty of Joseon Relief Sun a cette texture crème légère qui rend la protection moins punitive.", "visual": IMG/"products/beauty-of-joseon/beauty-of-joseon-relief-sun-rice-probiotics.webp", "visual_mode": "product", "cta": "Dernière slide : le lien direct."},
            {"bg": IMG/"routines/routine-asma-spf.webp", "kicker": "CTA", "title": "Le vrai geste utile : Beauty of Joseon Relief Sun.", "body": "À utiliser le matin, dernière étape, et à renouveler selon exposition.", "visual": IMG/"products/beauty-of-joseon/beauty-of-joseon-relief-sun-rice-probiotics.webp", "visual_mode": "product", "cta": "Va au produit : /produits/beauty-of-joseon-relief-sun"},
        ],
    },
]


def main():
    for deck in decks:
        folder = ROOT / deck["slug"]
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
        paths = [render_slide(deck, i, s) for i, s in enumerate(deck["slides"])]
        contact(paths, folder / "contact-sheet.jpg")
        preview(deck, paths)
        (folder / "SPEC.md").write_text(
            f"# {deck['title']}\n\n"
            "- V4 correction: no card behind text; full-bleed photo with contrast veil only.\n"
            "- Each slide has a different background image within the carousel.\n"
            "- Images selected first from the Sonagi Reference article, then from adjacent Sonagi archive material.\n"
            "- Diagrams/product visuals appear in the lower half only when they clarify the text.\n"
        )

    cards = []
    for deck in decks:
        cards.append(f'<article><h2><a href="{deck["slug"]}/carousel-preview.html">{html.escape(deck["title"])}</a></h2><a href="{deck["slug"]}/carousel-preview.html"><img src="{deck["slug"]}/contact-sheet.jpg"></a><p>{html.escape(deck["note"])}</p></article>')
    bank = f"""<!doctype html><html lang="fr"><meta charset="utf-8"><title>Sonagi V4 Auteur carousel bank</title>
<style>body{{margin:0;background:#f8f1e6;color:#1c1815;font-family:"American Typewriter",Courier,monospace}}header{{padding:42px 52px 12px}}h1{{font-family:Georgia,serif;font-size:48px;margin:0 0 10px}}main{{padding:20px 52px 70px;display:grid;gap:34px}}article{{border-top:1px solid rgba(28,24,21,.22);padding-top:24px}}h2{{font-family:Georgia,serif;font-size:28px}}img{{width:100%;box-shadow:0 18px 40px rgba(0,0,0,.14)}}a{{color:#1c1815}}</style>
<header><h1>Sonagi V4 Auteur carousel bank</h1><p>No-card editorial system: full-bleed image, readable text, unique contextual image per slide, Kbeauty Gems structure.</p></header><main>{''.join(cards)}</main></html>"""
    (ROOT / "bank-preview.html").write_text(bank)


if __name__ == "__main__":
    main()
