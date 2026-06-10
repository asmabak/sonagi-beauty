from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import html
import math
import shutil

ROOT = Path(__file__).resolve().parent
REF = Path("/Users/marouanebakhtar/sonagi-reference")
W, H = 1080, 1350

FONT_REG = "/System/Library/Fonts/Supplemental/AmericanTypewriter.ttc"
FONT_SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

CREAM = (246, 238, 224)
INK = (31, 28, 24)
MUTED = (92, 77, 62)
PEACH = (245, 196, 170)
PINK = (255, 62, 157)
BANANA = (247, 216, 76)
MINT = (168, 217, 185)


def font(path, size, index=0):
    return ImageFont.truetype(path, size=size, index=index)


F = {
    "kicker": font(FONT_REG, 27),
    "h1": font(FONT_SERIF_BOLD, 72),
    "h1_small": font(FONT_SERIF_BOLD, 58),
    "body": font(FONT_REG, 39),
    "body_sm": font(FONT_REG, 33),
    "caption": font(FONT_REG, 25),
    "cta": font(FONT_REG, 29),
    "tiny": font(FONT_REG, 20),
}


def load_cover(path):
    img = Image.open(path).convert("RGB")
    scale = max(W / img.width, H / img.height)
    img = img.resize((math.ceil(img.width * scale), math.ceil(img.height * scale)), Image.LANCZOS)
    left = (img.width - W) // 2
    top = (img.height - H) // 2
    img = img.crop((left, top, left + W, top + H))
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.GaussianBlur(0.25))
    overlay = Image.new("RGB", (W, H), (58, 41, 31))
    img = Image.blend(img, overlay, 0.16)
    wash = Image.new("RGBA", (W, H), (246, 238, 224, 30))
    img = Image.alpha_composite(img.convert("RGBA"), wash)
    return img


def fit_image(path, box, radius=0, opacity=255):
    x, y, bw, bh = box
    src = Image.open(path).convert("RGBA")
    scale = max(bw / src.width, bh / src.height)
    src = src.resize((math.ceil(src.width * scale), math.ceil(src.height * scale)), Image.LANCZOS)
    src = src.crop(((src.width - bw) // 2, (src.height - bh) // 2, (src.width + bw) // 2, (src.height + bh) // 2))
    if opacity < 255:
        src.putalpha(opacity)
    if radius:
        mask = Image.new("L", (bw, bh), 0)
        d = ImageDraw.Draw(mask)
        d.rounded_rectangle((0, 0, bw, bh), radius=radius, fill=255)
        src.putalpha(Image.composite(src.getchannel("A"), mask, mask))
    return src


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width or not line:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, width, line_gap=8):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap
    return y


def round_rect(draw, xy, fill, outline=None, width=1, radius=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def slide(deck, i, data, slide):
    bg = load_cover(slide.get("image", deck["images"][i % len(deck["images"])]))
    canvas = bg.convert("RGB")
    d = ImageDraw.Draw(canvas, "RGBA")

    d.rectangle((0, 0, W, H), fill=(0, 0, 0, 88 if slide["kind"] == "hook" else 54))
    d.text((64, 54), "SONAGI", font=F["tiny"], fill=(CREAM[0], CREAM[1], CREAM[2], 220))
    d.text((64, 88), deck["label"].upper(), font=F["tiny"], fill=(CREAM[0], CREAM[1], CREAM[2], 195))
    d.text((958, 54), f"{i+1:02d}/07", font=F["tiny"], fill=(CREAM[0], CREAM[1], CREAM[2], 205))

    if slide["kind"] == "hook":
        d.text((64, 214), slide["kicker"].upper(), font=F["kicker"], fill=(BANANA[0], BANANA[1], BANANA[2], 245))
        y = draw_wrapped(d, (64, 282), slide["title"], F["h1"], CREAM, 850, 8)
        draw_wrapped(d, (66, y + 28), slide["body"], F["body_sm"], CREAM, 740, 9)
    else:
        panel_y = 660
        round_rect(d, (48, panel_y, 1032, 1192), fill=(246, 238, 224, 232), outline=(255, 255, 255, 112), width=2, radius=28)
        d.rectangle((82, panel_y + 44, 998, panel_y + 47), fill=(31, 28, 24, 74))
        d.text((82, panel_y + 72), slide["kicker"].upper(), font=F["tiny"], fill=MUTED)
        title_font = F["h1_small"] if len(slide["title"]) > 30 else F["h1"]
        y = draw_wrapped(d, (82, panel_y + 116), slide["title"], title_font, INK, 575, 5)
        y = draw_wrapped(d, (82, y + 20), slide["body"], F["body_sm"], INK, 575, 8)
        asset = slide.get("asset")
        if asset:
            img = fit_image(asset, (708, panel_y + 118, 270, 270), radius=22)
            canvas.paste(img, (708, panel_y + 118), img)
            d.text((708, panel_y + 410), slide.get("asset_caption", ""), font=F["caption"], fill=MUTED)
        if slide.get("mini"):
            mx, my = 700, panel_y + 420
            round_rect(d, (mx, my, 978, my + 118), fill=(255, 255, 255, 118), outline=(31, 28, 24, 50), radius=18)
            draw_wrapped(d, (mx + 22, my + 20), slide["mini"], F["caption"], INK, 230, 4)

    d.rectangle((48, 1214, 1032, 1274), fill=(31, 28, 24, 212))
    if d.textbbox((0, 0), slide["cta"], font=F["cta"])[2] <= 740:
        d.text((72, 1230), slide["cta"], font=F["cta"], fill=CREAM)
    elif " : " in slide["cta"]:
        lead, slug = slide["cta"].split(" : ", 1)
        d.text((72, 1223), f"{lead} :", font=F["tiny"], fill=CREAM)
        d.text((72, 1248), slug, font=F["tiny"], fill=CREAM)
    else:
        d.text((72, 1232), slide["cta"], font=F["tiny"], fill=CREAM)
    d.text((860, 1232), "sonagi", font=F["cta"], fill=PEACH)
    out = ROOT / deck["slug"] / f"slide-{i+1:02d}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=96)
    return out


def make_contact_sheet(paths, out):
    thumbs = []
    for p in paths:
        img = Image.open(p).convert("RGB")
        img.thumbnail((216, 270), Image.LANCZOS)
        thumbs.append(img.copy())
    sheet = Image.new("RGB", (216 * 7, 270), CREAM)
    for i, img in enumerate(thumbs):
        sheet.paste(img, (i * 216, 0))
    sheet.save(out, quality=92)


def write_preview(deck, paths):
    items = "\n".join(
        f'<figure><img src="{p.name}" alt="slide {i+1}"><figcaption>{i+1}</figcaption></figure>'
        for i, p in enumerate(paths)
    )
    html_doc = f"""<!doctype html>
<html lang="fr"><meta charset="utf-8"><title>{html.escape(deck['title'])}</title>
<style>
body{{margin:0;background:#f6eee0;color:#1f1c18;font-family:"American Typewriter",Courier,monospace}}
header{{padding:36px 44px 10px}} h1{{font-family:Georgia,serif;font-size:38px;margin:0}} p{{max-width:760px;line-height:1.45}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;padding:26px 44px 60px}}
figure{{margin:0}} img{{width:100%;height:auto;display:block;box-shadow:0 18px 40px rgba(31,28,24,.16)}} figcaption{{font-size:13px;padding:8px 0}}
a{{color:#1f1c18}}
</style><header><h1>{html.escape(deck['title'])}</h1><p>{html.escape(deck['note'])}</p></header><main class="grid">{items}</main></html>"""
    (ROOT / deck["slug"] / "carousel-preview.html").write_text(html_doc)


def write_spec(deck):
    lines = [
        f"# {deck['title']}",
        "",
        f"- Source Sonagi Reference: `{deck['source']}`",
        f"- Product CTA: `{deck['product']}`",
        "- Format: 1080x1350, background photo with editorial filter, lower copy/diagram panel.",
        "- Structure: trend hook -> skin mechanism -> what it needs -> choice logic -> direct product CTA.",
        "- Style: Auteur-like photo background, Kbeauty Gems educational arc, typewriter/MoMA restraint.",
    ]
    (ROOT / deck["slug"] / "SPEC.md").write_text("\n".join(lines) + "\n")


IMG = REF / "assets/images"
DIA = REF / "assets/diagrams"

decks = [
    {
        "slug": "01-skin-flooding-anua",
        "label": "hydratation virale",
        "title": "Skin flooding : TikTok l'a découvert, Séoul l'avait déjà codé",
        "source": "content/techniques/fr/skin-flooding.md",
        "product": "https://sonagibeauty.com/produits/anua-heartleaf-77-toner",
        "note": "Trend hook, mécanisme d'hydratation, puis CTA direct vers Anua Heartleaf 77.",
        "images": [IMG / "techniques/skin-flooding-hero.webp", IMG / "techniques/skin-flooding-body-1.webp", IMG / "ingredients/heartleaf-hero.webp"],
        "slides": [
            {"kind": "hook", "kicker": "Tendance", "title": "Tu appelles ça skin flooding. En Corée, c'était déjà une méthode.", "body": "Le buzz n'est pas nouveau. Ce qui compte, c'est pourquoi ta peau boit mieux quand elle reste humide.", "cta": "Sauvegarde avant d'empiler sept couches au hasard."},
            {"kind": "body", "kicker": "Le besoin", "title": "Ta peau ne manque pas toujours de crème.", "body": "Souvent, elle manque d'eau retenue au bon moment. Une couche aqueuse sur peau humide limite l'évaporation de la précédente.", "asset": DIA / "skin-flooding-mechanism.webp", "asset_caption": "Mécanisme Sonagi", "mini": "eau + humectants + scellement", "cta": "Slide suivante : le geste qui change tout."},
            {"kind": "body", "kicker": "La règle", "title": "Ne laisse pas sécher entre les couches.", "body": "Dix à vingt secondes. Pas plus. Si la peau sèche, tu perds l'effet d'occlusion humectante.", "asset": IMG / "techniques/skin-flooding-body-1.webp", "asset_caption": "Peau encore humide", "mini": "3 couches = entretien\n5-7 = déshydratation", "cta": "Teste trois couches avant d'en faire sept."},
            {"kind": "body", "kicker": "Le piège", "title": "Le mauvais toner ruine la méthode.", "body": "Pas d'alcool, pas d'astringent agressif, pas de parfum qui pique. Le toner doit être aqueux, doux, empilable.", "asset": IMG / "products/anua/anua-heartleaf-77-soothing-toner.webp", "asset_caption": "Toner aqueux", "mini": "texture eau\nzéro décapage", "cta": "Cherche une texture qui disparaît, pas qui colle."},
            {"kind": "body", "kicker": "Pour qui", "title": "Peau qui tire, avion, chauffage, stress.", "body": "Le skin flooding parle surtout aux peaux déshydratées. Une peau grasse peut aussi manquer d'eau.", "asset": DIA / "skin-flooding-mechanism.webp", "asset_caption": "Couche cornée", "mini": "gras ≠ hydraté", "cta": "Si ta peau brille et tire, garde cette slide."},
            {"kind": "body", "kicker": "Le choix", "title": "Prends un toner qui calme autant qu'il hydrate.", "body": "Heartleaf aide les peaux réactives à tolérer le geste. C'est pour ça que l'Anua 77 est devenu un standard.", "asset": IMG / "products/anua/anua-heartleaf-77-soothing-toner.webp", "asset_caption": "Anua Heartleaf 77", "mini": "matin ou soir\npaumes ou coton", "cta": "Dernière slide : le lien direct."},
            {"kind": "body", "kicker": "CTA", "title": "Le produit pivot : Anua Heartleaf 77 Toner.", "body": "À utiliser après le nettoyage, sur peau encore humide, avant sérum et crème. Le lien direct est en bas de la slide.", "asset": IMG / "products/anua/anua-heartleaf-77-soothing-toner.webp", "asset_caption": "Sélection Sonagi", "mini": "Découvrir", "cta": "Va au produit : /produits/anua-heartleaf-77-toner"},
        ],
    },
    {
        "slug": "02-double-nettoyage-boj",
        "label": "nettoyage du soir",
        "title": "Le double nettoyage n'est pas une routine de plus",
        "source": "content/techniques/fr/double-cleansing.md",
        "product": "https://sonagibeauty.com/produits/beauty-of-joseon-radiance-cleansing-balm",
        "note": "SPF/maquillage/pollution -> deux solvants -> Beauty of Joseon Radiance Balm.",
        "images": [IMG / "techniques/double-cleansing-hero.webp", IMG / "techniques/double-cleansing-2.webp", IMG / "products/beauty-of-joseon/beauty-of-joseon-radiance-cleansing-balm.webp"],
        "slides": [
            {"kind": "hook", "kicker": "Contre-intuitif", "title": "Ta mousse seule ne retire pas vraiment ton SPF.", "body": "Pas parce qu'elle est mauvaise. Parce que l'eau ne dissout pas bien ce qui aime le gras.", "cta": "Sauvegarde si tu portes SPF ou maquillage."},
            {"kind": "body", "kicker": "La peau du soir", "title": "Le soir, ton visage porte deux familles de résidus.", "body": "Sébum oxydé, SPF, maquillage d'un côté. Sueur, poussières, pollution hydrosoluble de l'autre.", "asset": DIA / "double-cleansing-mechanism.webp", "asset_caption": "Deux familles", "mini": "lipophile\nhydrophile", "cta": "Un seul nettoyant force souvent le frottement."},
            {"kind": "body", "kicker": "Étape 1", "title": "Le baume dissout le gras sans décaper.", "body": "Sur peau sèche, il fond avec les paumes et soulève SPF, sébum et maquillage longue tenue.", "asset": IMG / "products/beauty-of-joseon/beauty-of-joseon-radiance-cleansing-balm.webp", "asset_caption": "Geste 1", "mini": "60 à 90 secondes\nsans frotter", "cta": "Le bon baume fait le travail mécanique."},
            {"kind": "body", "kicker": "Étape 2", "title": "La mousse douce retire l'émulsion.", "body": "Le second geste doit respecter le pH de la peau. L'eau brûlante et le savon classique cassent l'intérêt du rituel.", "asset": DIA / "double-cleansing-mechanism.webp", "asset_caption": "pH bas", "mini": "4,5 à 5,5\njamais savon", "cta": "Double nettoyage ne veut pas dire double agression."},
            {"kind": "body", "kicker": "Pour qui", "title": "Pas tous les matins. Surtout les soirs de SPF.", "body": "Le matin, inutile. Le soir, essentiel si tu as porté protection solaire, pollution urbaine ou maquillage.", "asset": IMG / "techniques/double-cleansing-2.webp", "asset_caption": "Routine du soir", "mini": "soir seulement\nselon journée", "cta": "Si ta peau tire après, le geste 2 est trop fort."},
            {"kind": "body", "kicker": "Le choix", "title": "Commence par un baume qui émulsionne proprement.", "body": "Le Beauty of Joseon Radiance Cleansing Balm est le geste 1 Sonagi : il fond, masse, puis se rince au lait.", "asset": IMG / "products/beauty-of-joseon/beauty-of-joseon-radiance-cleansing-balm.webp", "asset_caption": "BOJ Radiance Balm", "mini": "SPF\nmaquillage\nsébum", "cta": "Dernière slide : le lien direct."},
            {"kind": "body", "kicker": "CTA", "title": "Le geste 1 : Beauty of Joseon Radiance Balm.", "body": "À utiliser le soir, sur peau sèche, avant ton nettoyant à pH bas. Le lien direct est en bas de la slide.", "asset": IMG / "products/beauty-of-joseon/beauty-of-joseon-radiance-cleansing-balm.webp", "asset_caption": "Sélection Sonagi", "mini": "Découvrir", "cta": "Va au produit : /produits/beauty-of-joseon-radiance-cleansing-balm"},
        ],
    },
    {
        "slug": "03-barriere-centella",
        "label": "barrière cutanée",
        "title": "Ta barrière n'a pas besoin de courage, elle a besoin de silence",
        "source": "content/basics/fr/la-barriere-cutanee.md",
        "product": "https://sonagibeauty.com/produits/skin1004-madagascar-centella-ampoule",
        "note": "Peau qui pique -> mur de briques -> deux semaines de simplification -> Skin1004 Centella.",
        "images": [IMG / "basics/la-barriere-cutanee-hero-v3.webp", IMG / "basics/la-barriere-cutanee-body-1.webp", IMG / "products/skin1004/skin1004-madagascar-centella-ampoule.webp"],
        "slides": [
            {"kind": "hook", "kicker": "Signal faible", "title": "Si tout pique, ce n'est pas que ta peau est capricieuse.", "body": "C'est souvent la barrière qui fuit. Et sur un mur fissuré, plus d'actifs ne réparent rien.", "cta": "Sauvegarde avant d'ajouter un nouveau sérum."},
            {"kind": "body", "kicker": "Le besoin", "title": "Briques, ciment, eau retenue.", "body": "Les cellules sont les briques. Les lipides sont le ciment. Quand le ciment manque, l'eau sort et les irritants entrent.", "asset": DIA / "la-barriere-cutanee.webp", "asset_caption": "Schéma Sonagi", "mini": "TEWL = eau qui fuit", "cta": "La peau qui tire demande moins, pas plus."},
            {"kind": "body", "kicker": "Le piège", "title": "Acides + rétinol + gommage : le mur prend tout.", "body": "La barrière abîmée ne tolère plus ce qu'elle supportait avant. Ce n'est pas une faiblesse, c'est un signal.", "asset": IMG / "basics/la-barriere-cutanee-body-1.webp", "asset_caption": "Texture + barrière", "mini": "pause actifs\n14 jours", "cta": "Deux semaines simples valent mieux qu'un placard plein."},
            {"kind": "body", "kicker": "Ce qu'elle veut", "title": "Calmer d'abord. Sceller ensuite.", "body": "Toner doux, ampoule apaisante, crème. Le minimum assez longtemps pour que le ciment se refasse.", "asset": DIA / "reparer-la-barriere-cutanee-mechanism.webp", "asset_caption": "Réparation", "mini": "apaiser\nhydrater\nsceller", "cta": "Si ça chauffe, enlève une étape."},
            {"kind": "body", "kicker": "Pourquoi centella", "title": "Parce que la peau rouge veut du calme.", "body": "La centella est le réflexe K-beauty quand la peau réagit vite : peu d'ingrédients, beaucoup de tolérance.", "asset": IMG / "products/skin1004/skin1004-madagascar-centella-ampoule.webp", "asset_caption": "Skin1004", "mini": "ampoule légère\nsans surcharge", "cta": "Garde la formule courte."},
            {"kind": "body", "kicker": "Le choix", "title": "Une ampoule, pas une punition.", "body": "Skin1004 Madagascar Centella Ampoule : un geste simple pour remettre la routine au calme.", "asset": IMG / "products/skin1004/skin1004-madagascar-centella-ampoule.webp", "asset_caption": "Madagascar Centella", "mini": "matin/soir\navant crème", "cta": "Dernière slide : le lien direct."},
            {"kind": "body", "kicker": "CTA", "title": "Le produit calme : Skin1004 Centella Ampoule.", "body": "À poser après nettoyage, avant crème, surtout quand la peau devient rouge ou inconfortable. Le lien direct est en bas de la slide.", "asset": IMG / "products/skin1004/skin1004-madagascar-centella-ampoule.webp", "asset_caption": "Sélection Sonagi", "mini": "Découvrir", "cta": "Va au produit : /produits/skin1004-madagascar-centella-ampoule"},
        ],
    },
    {
        "slug": "04-sebum-heartleaf",
        "label": "peau qui brille",
        "title": "La peau qui brille n'est pas sale",
        "source": "content/basics/fr/le-sebum.md + content/ingredients/fr/heartleaf.md",
        "product": "https://sonagibeauty.com/produits/anua-heartleaf-77-toner",
        "note": "Peau brillante -> sébum protecteur -> réguler sans décaper -> Anua Heartleaf.",
        "images": [IMG / "basics/le-sebum-hero-v3.webp", IMG / "ingredients/heartleaf-hero.webp", IMG / "products/anua/anua-heartleaf-77-soothing-toner.webp"],
        "slides": [
            {"kind": "hook", "kicker": "Hot take", "title": "Plus tu assèches ta peau grasse, plus elle négocie.", "body": "Le sébum n'est pas une saleté. C'est une couche protectrice. Le but, c'est réguler, pas exterminer.", "cta": "Sauvegarde si tu matifies toute la journée."},
            {"kind": "body", "kicker": "Le besoin", "title": "Le sébum sort d'une usine sous le pore.", "body": "Il remonte le long du follicule, se mélange aux lipides et forme le film hydrolipidique.", "asset": DIA / "le-sebum.webp", "asset_caption": "Usine sébacée", "mini": "protéger\nretenir l'eau", "cta": "Briller un peu n'est pas échouer."},
            {"kind": "body", "kicker": "Le cercle", "title": "Trop laver peut relancer la brillance.", "body": "Eau chaude, savon alcalin, exfoliation quotidienne : la surface sèche, la peau compense.", "asset": IMG / "basics/le-sebum-card-v3.webp", "asset_caption": "Équilibre", "mini": "décaper → tirer\n tirer → produire", "cta": "Ne confonds pas propre et décapé."},
            {"kind": "body", "kicker": "Ce qu'elle veut", "title": "Un actif qui calme pendant qu'il régule.", "body": "Heartleaf est intéressant parce qu'il vise rougeurs, inconfort et excès de sébum sans transformer la routine en traitement brutal.", "asset": DIA / "heartleaf-mechanism.webp", "asset_caption": "Herbe-cœur", "mini": "sébum\nrougeurs\npores", "cta": "La peau grasse aussi a besoin de douceur."},
            {"kind": "body", "kicker": "Le dosage", "title": "77 %, ce n'est pas une décoration d'étiquette.", "body": "Anua a fait de l'herbe-cœur le cœur de la formule. Texture aqueuse, facile à placer matin ou soir.", "asset": IMG / "products/anua/anua-heartleaf-77-soothing-toner.webp", "asset_caption": "Anua 77", "mini": "paumes\nou coton", "cta": "Commence par réguler le premier geste après nettoyage."},
            {"kind": "body", "kicker": "Le choix", "title": "Toner d'équilibre, pas lotion décapante.", "body": "Utilise-le quand la peau brille, rougit ou réagit. Si ça pique, ce n'est pas le bon produit pour toi.", "asset": IMG / "products/anua/anua-heartleaf-77-soothing-toner.webp", "asset_caption": "Texture eau", "mini": "sans alcool\nsans violence", "cta": "Dernière slide : le lien direct."},
            {"kind": "body", "kicker": "CTA", "title": "Le toner équilibre : Anua Heartleaf 77.", "body": "À appliquer après nettoyage, avant sérum. Le lien direct est en bas de la slide.", "asset": IMG / "products/anua/anua-heartleaf-77-soothing-toner.webp", "asset_caption": "Sélection Sonagi", "mini": "Découvrir", "cta": "Va au produit : /produits/anua-heartleaf-77-toner"},
        ],
    },
    {
        "slug": "05-sephora-kids-spf",
        "label": "peau jeune",
        "title": "Une fille de douze ans n'a pas besoin d'anti-âge",
        "source": "content/edito/fr/sephora-kids.md",
        "product": "https://sonagibeauty.com/produits/beauty-of-joseon-relief-sun",
        "note": "Trend Sephora Kids -> peau jeune -> moins de produits -> SPF comme vrai geste utile.",
        "images": [IMG / "edito/sephora-kids/sephora-kids-hero-v2.webp", IMG / "routines/routine-pre-ado-hero.webp", IMG / "products/beauty-of-joseon/beauty-of-joseon-relief-sun-rice-probiotics.webp"],
        "slides": [
            {"kind": "hook", "kicker": "Sujet qui fâche", "title": "Le problème des Sephora Kids, ce n'est pas la crème.", "body": "C'est l'idée qu'une enfant devrait déjà surveiller son visage comme un défaut à corriger.", "cta": "Sauvegarde pour la prochaine liste d'anniversaire."},
            {"kind": "body", "kicker": "La peau jeune", "title": "Elle n'a pas de ride à réparer.", "body": "Une peau d'enfant ou de pré-ado a surtout besoin de douceur, de nettoyage simple, et de protection solaire.", "asset": DIA / "routine-pre-ado-puberty-transition.webp", "asset_caption": "Transition pré-ado", "mini": "doux\nsimple\nSPF", "cta": "Anti-âge à dix ans : mauvais besoin, mauvais message."},
            {"kind": "body", "kicker": "Le vrai risque", "title": "Trop d'actifs, trop tôt.", "body": "Acides, rétinol, parfums, routines longues : plus de points de friction sur une barrière encore sensible.", "asset": IMG / "edito/sephora-kids/taille-routine-enfant.webp", "asset_caption": "Données édito", "mini": "6 produits\n11 actifs irritants", "cta": "Une routine d'enfant doit être courte."},
            {"kind": "body", "kicker": "Ce qu'elle veut", "title": "Un nettoyant doux. Une crème. Un SPF.", "body": "Pas une performance devant le miroir. Pas douze étapes. Pas une peur de vieillir.", "asset": IMG / "routines/routine-pre-ado-hero.webp", "asset_caption": "Routine courte", "mini": "matin : SPF\nsoir : doux", "cta": "Le meilleur soin, c'est parfois d'en enlever."},
            {"kind": "body", "kicker": "Le paradoxe", "title": "Le seul vrai anti-âge est souvent absent.", "body": "Dans les routines virales d'enfants, l'écran solaire manque trop souvent. C'est pourtant le geste le plus utile.", "asset": IMG / "products/beauty-of-joseon/beauty-of-joseon-relief-sun-rice-probiotics.webp", "asset_caption": "SPF quotidien", "mini": "protéger\npas corriger", "cta": "On remplace la peur par la protection."},
            {"kind": "body", "kicker": "Le choix", "title": "Un SPF confortable est celui qu'on remet.", "body": "Beauty of Joseon Relief Sun a cette texture crème légère qui rend la protection moins punitive.", "asset": IMG / "products/beauty-of-joseon/beauty-of-joseon-relief-sun-rice-probiotics.webp", "asset_caption": "Relief Sun", "mini": "SPF 50+\nriz + probiotiques", "cta": "Dernière slide : le lien direct."},
            {"kind": "body", "kicker": "CTA", "title": "Le vrai geste utile : Beauty of Joseon Relief Sun.", "body": "À utiliser le matin, dernière étape, et à renouveler selon exposition. Le lien direct est en bas de la slide.", "asset": IMG / "products/beauty-of-joseon/beauty-of-joseon-relief-sun-rice-probiotics.webp", "asset_caption": "Sélection Sonagi", "mini": "Découvrir", "cta": "Va au produit : /produits/beauty-of-joseon-relief-sun"},
        ],
    },
]


def main():
    for deck in decks:
        folder = ROOT / deck["slug"]
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
        paths = [slide(deck, i, deck, s) for i, s in enumerate(deck["slides"])]
        make_contact_sheet(paths, folder / "contact-sheet.jpg")
        write_preview(deck, paths)
        write_spec(deck)

    cards = []
    for deck in decks:
        rel = f"{deck['slug']}/carousel-preview.html"
        img = f"{deck['slug']}/contact-sheet.jpg"
        cards.append(f'<article><h2><a href="{rel}">{html.escape(deck["title"])}</a></h2><a href="{rel}"><img src="{img}" alt=""></a><p>{html.escape(deck["note"])}</p></article>')
    bank = f"""<!doctype html>
<html lang="fr"><meta charset="utf-8"><title>Sonagi carousel bank V3</title>
<style>
body{{margin:0;background:#f6eee0;color:#1f1c18;font-family:"American Typewriter",Courier,monospace}}
header{{padding:42px 52px 8px}} h1{{font-family:Georgia,serif;font-size:48px;margin:0 0 12px}} p{{max-width:850px;line-height:1.45}}
main{{display:grid;grid-template-columns:1fr;gap:34px;padding:28px 52px 70px}} article{{border-top:1px solid rgba(31,28,24,.22);padding-top:24px}}
h2{{font-family:Georgia,serif;font-size:28px}} img{{width:100%;max-width:1512px;display:block;box-shadow:0 18px 40px rgba(31,28,24,.14)}} a{{color:#1f1c18}}
</style><header><h1>Sonagi carousel bank V3</h1><p>Kbeauty Gems structure: trend hook, skin-need education, product choice, direct product CTA. Auteur-style background: photo + editorial filter + typewriter/MoMA slide system.</p></header><main>{''.join(cards)}</main></html>"""
    (ROOT / "bank-preview.html").write_text(bank)


if __name__ == "__main__":
    main()
