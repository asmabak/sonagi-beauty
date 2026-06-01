#!/usr/bin/env python3
"""Swap the existing single-level La Boutique dropdown with the canonical 3-level mega-menu across all 19 HTML pages.

Anchor strategy:
  start = first occurrence of '<li class="nav-item has-drop">' on the line
  end   = closing '</div></li>' that follows the 'Coffrets &amp; Bundles' link

We preserve the `active` class on the La Boutique anchor if it was present on
the original (skincare/maquillage/haircare/marques/produit pages).
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/marou/sonagi-beauty/files")

PAGES = [
    "index.html", "skincare.html", "maquillage.html", "haircare.html",
    "marques.html", "masterclasses.html", "journal.html", "glossaire.html",
    "about.html", "faq.html", "compte.html", "panier.html", "produit.html",
    "rewards.html", "confirmation.html", "mentions-legales.html",
    "politique-confidentialite.html", "cookies.html", "cgv.html",
]

# Canonical block - {ACTIVE_ATTR} placeholder gets replaced with ' class="active"' or ''.
CANONICAL_TEMPLATE = '''<li class="nav-item has-drop"><a href="skincare.html"{ACTIVE_ATTR} data-fr="La Boutique" data-en="The Shop">La Boutique</a><div class="nav-dropdown">
        <a href="skincare.html" class="t" data-fr="Tout voir" data-en="Shop all">Tout voir</a>
        <div class="nd-sep"></div>
        <div class="nd-sub"><button class="nd-link t" data-fr="Skincare" data-en="Skincare">Skincare</button>
          <div class="nd-sub-panel">
            <a href="skincare.html" class="t" data-fr="Tout Skincare" data-en="All Skincare">Tout Skincare</a>
            <div class="nd-sep"></div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Type de produit" data-en="Product type">Type de produit</button>
              <div class="nd-sub-panel">
                <a href="skincare.html?cat=nettoyant" class="t" data-fr="Nettoyant" data-en="Cleanser">Nettoyant</a>
                <a href="skincare.html?cat=toner" class="t" data-fr="Toner" data-en="Toner">Toner</a>
                <a href="skincare.html?cat=exfoliant" class="t" data-fr="Exfoliant / Gommage" data-en="Exfoliant / Scrub">Exfoliant / Gommage</a>
                <a href="skincare.html?cat=essence" class="t" data-fr="Essence" data-en="Essence">Essence</a>
                <a href="skincare.html?cat=serum" class="t" data-fr="Ampoule / Sérum" data-en="Ampoule / Serum">Ampoule / Sérum</a>
                <a href="skincare.html?cat=contour-yeux" class="t" data-fr="Contour des Yeux" data-en="Eye care">Contour des Yeux</a>
                <a href="skincare.html?cat=creme" class="t" data-fr="Crème Hydratante" data-en="Moisturiser">Crème Hydratante</a>
                <a href="skincare.html?cat=spf" class="t" data-fr="Crème Solaire" data-en="Sun care">Crème Solaire</a>
                <a href="skincare.html?cat=masque" class="t" data-fr="Masque à Rincer" data-en="Rinse-off mask">Masque à Rincer</a>
                <a href="skincare.html?cat=masque-tissu" class="t" data-fr="Masque en Tissu" data-en="Sheet mask">Masque en Tissu</a>
              </div>
            </div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Type de peau" data-en="Skin type">Type de peau</button>
              <div class="nd-sub-panel">
                <a href="skincare.html?cat=peau-grasse" class="t" data-fr="Peau Grasse" data-en="Oily skin">Peau Grasse</a>
                <a href="skincare.html?cat=peau-seche" class="t" data-fr="Peau Sèche" data-en="Dry skin">Peau Sèche</a>
                <a href="skincare.html?cat=peau-mixte" class="t" data-fr="Peau Mixte" data-en="Combination skin">Peau Mixte</a>
                <a href="skincare.html?cat=peau-normale" class="t" data-fr="Peau Normale" data-en="Normal skin">Peau Normale</a>
                <a href="skincare.html?cat=peau-sensible" class="t" data-fr="Peau Sensible" data-en="Sensitive skin">Peau Sensible</a>
              </div>
            </div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Préoccupation" data-en="Concern">Préoccupation</button>
              <div class="nd-sub-panel">
                <a href="skincare.html?cat=acne" class="t" data-fr="Acné" data-en="Acne">Acné</a>
                <a href="skincare.html?cat=pores" class="t" data-fr="Pores dilatés &amp; Points noirs" data-en="Large pores &amp; blackheads">Pores dilatés &amp; Points noirs</a>
                <a href="skincare.html?cat=eclat" class="t" data-fr="Teint terne &amp; Hyperpigmentation" data-en="Dull skin &amp; hyperpigmentation">Teint terne &amp; Hyperpigmentation</a>
                <a href="skincare.html?cat=hydratation" class="t" data-fr="Déshydratation" data-en="Dehydration">Déshydratation</a>
                <a href="skincare.html?cat=anti-age" class="t" data-fr="Rides &amp; Élasticité" data-en="Wrinkles &amp; elasticity">Rides &amp; Élasticité</a>
                <a href="skincare.html?cat=anti-rougeurs" class="t" data-fr="Rougeurs &amp; Inflammations" data-en="Redness &amp; inflammation">Rougeurs &amp; Inflammations</a>
                <a href="skincare.html?cat=barriere" class="t" data-fr="Barrière endommagée" data-en="Damaged barrier">Barrière endommagée</a>
              </div>
            </div>
          </div>
        </div>
        <div class="nd-sub"><button class="nd-link t" data-fr="Maquillage" data-en="Makeup">Maquillage</button>
          <div class="nd-sub-panel">
            <a href="maquillage.html" class="t" data-fr="Tout Maquillage" data-en="All Makeup">Tout Maquillage</a>
            <a href="maquillage.html?cat=demaquillant" class="t" data-fr="Démaquillant" data-en="Makeup remover">Démaquillant</a>
            <div class="nd-sep"></div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Yeux" data-en="Eyes">Yeux</button>
              <div class="nd-sub-panel">
                <a href="maquillage.html?cat=fard" class="t" data-fr="Fard à paupières" data-en="Eye shadow">Fard à paupières</a>
                <a href="maquillage.html?cat=mascara" class="t" data-fr="Mascara" data-en="Mascara">Mascara</a>
                <a href="maquillage.html?cat=liner" class="t" data-fr="Liner &amp; Crayon" data-en="Liner &amp; Pencil">Liner &amp; Crayon</a>
              </div>
            </div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Lèvres" data-en="Lips">Lèvres</button>
              <div class="nd-sub-panel">
                <a href="maquillage.html?cat=rouge-a-levres" class="t" data-fr="Rouge à lèvres" data-en="Lipstick">Rouge à lèvres</a>
                <a href="maquillage.html?cat=baume-levres" class="t" data-fr="Baume à lèvres" data-en="Lip balm">Baume à lèvres</a>
                <a href="maquillage.html?cat=gloss" class="t" data-fr="Gloss &amp; Soins" data-en="Gloss &amp; Care">Gloss &amp; Soins</a>
                <a href="maquillage.html?cat=tint" class="t" data-fr="Tint lèvres" data-en="Lip tint">Tint lèvres</a>
              </div>
            </div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Teint" data-en="Foundation">Teint</button>
              <div class="nd-sub-panel">
                <a href="maquillage.html?cat=cushion" class="t" data-fr="Cushion / BB Crème" data-en="Cushion / BB Cream">Cushion / BB Crème</a>
                <a href="maquillage.html?cat=concealer" class="t" data-fr="Concealer" data-en="Concealer">Concealer</a>
                <a href="maquillage.html?cat=bronzer" class="t" data-fr="Bronzer / Highlighter" data-en="Bronzer / Highlighter">Bronzer / Highlighter</a>
                <a href="maquillage.html?cat=blush" class="t" data-fr="Blush" data-en="Blush">Blush</a>
                <a href="maquillage.html?cat=poudre" class="t" data-fr="Poudre / Fixateur" data-en="Powder / Setting">Poudre / Fixateur</a>
              </div>
            </div>
            <div class="nd-sep"></div>
            <a href="maquillage.html?cat=accessoires" class="t" data-fr="Accessoires" data-en="Accessories">Accessoires</a>
          </div>
        </div>
        <div class="nd-sub"><button class="nd-link t" data-fr="Cheveux &amp; Corps" data-en="Hair &amp; Body">Cheveux &amp; Corps</button>
          <div class="nd-sub-panel">
            <a href="haircare.html" class="t" data-fr="Tout Cheveux &amp; Corps" data-en="All Hair &amp; Body">Tout Cheveux &amp; Corps</a>
            <div class="nd-sep"></div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Cheveux" data-en="Hair">Cheveux</button>
              <div class="nd-sub-panel">
                <a href="haircare.html?cat=shampooing" class="t" data-fr="Shampooing" data-en="Shampoo">Shampooing</a>
                <a href="haircare.html?cat=apres-shampooing" class="t" data-fr="Après-shampooing" data-en="Conditioner">Après-shampooing</a>
                <a href="haircare.html?cat=masque" class="t" data-fr="Soins &amp; Traitements" data-en="Treatments">Soins &amp; Traitements</a>
                <a href="haircare.html?cat=serum" class="t" data-fr="Sérum capillaire" data-en="Hair serum">Sérum capillaire</a>
              </div>
            </div>
            <div class="nd-sub"><button class="nd-link t" data-fr="Corps" data-en="Body">Corps</button>
              <div class="nd-sub-panel">
                <a href="haircare.html?cat=corps" class="t" data-fr="Lotion pour le corps" data-en="Body lotion">Lotion pour le corps</a>
                <a href="haircare.html?cat=gommage" class="t" data-fr="Exfoliant corps" data-en="Body scrub">Exfoliant corps</a>
              </div>
            </div>
          </div>
        </div>
        <a href="marques.html" class="t" data-fr="Toutes les marques" data-en="All brands">Toutes les marques</a>
        <div class="nd-sep"></div>
        <a href="skincare.html?cat=coffret" class="t" data-fr="Coffrets &amp; Bundles" data-en="Sets &amp; Bundles">Coffrets &amp; Bundles</a>
      </div></li>'''

# Regex matches the original li (start anchor) up through the closing </div></li>
# right after the Coffrets & Bundles anchor.
PATTERN = re.compile(
    r'<li class="nav-item has-drop"><a href="skincare\.html"(?P<active>(?:\s+class="active")?)\s+data-fr="La Boutique"[\s\S]*?Coffrets &amp; Bundles</a>\s*</div></li>'
)


def process(path: Path) -> tuple[bool, str]:
    src = path.read_text(encoding="utf-8")
    matches = list(PATTERN.finditer(src))
    if len(matches) == 0:
        return False, "no match"
    if len(matches) > 1:
        return False, f"{len(matches)} matches (expected 1)"

    m = matches[0]
    active = m.group("active") or ""
    new_block = CANONICAL_TEMPLATE.replace("{ACTIVE_ATTR}", active)
    new_src = src[: m.start()] + new_block + src[m.end():]
    if new_src == src:
        return False, "no-op"
    path.write_text(new_src, encoding="utf-8")
    return True, "ok"


def main() -> int:
    failures: list[str] = []
    successes: list[str] = []
    for name in PAGES:
        p = ROOT / name
        if not p.exists():
            failures.append(f"{name}: missing file")
            continue
        ok, msg = process(p)
        (successes if ok else failures).append(f"{name}: {msg}")

    print("=== UPDATED ===")
    for s in successes:
        print(" ", s)
    if failures:
        print("=== FAILURES ===")
        for f in failures:
            print(" ", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
