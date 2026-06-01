#!/usr/bin/env python3
"""
Sonagi Beauty nav-restructure.
Applies the new nav, mobile L1 panel, and footer across all HTML files in files/.
Idempotent: running twice has no extra effect.
"""

import os
import re
import sys
from pathlib import Path

FILES_DIR = Path("C:/Users/marou/sonagi-beauty/files")

# ---- Replacement blocks ----------------------------------------------------

NEW_NAV_LINKS = '''<ul class="nav-links">
      <li class="nav-item has-drop"><a href="skincare.html"{ACTIVE_BOUTIQUE} data-fr="La Boutique" data-en="The Shop">La Boutique</a><div class="nav-dropdown">
        <a href="skincare.html" class="t" data-fr="Tout voir" data-en="Shop all">Tout voir</a>
        <div class="nd-sep"></div>
        <a href="skincare.html" class="t" data-fr="Skincare" data-en="Skincare">Skincare</a>
        <a href="maquillage.html" class="t" data-fr="Maquillage" data-en="Makeup">Maquillage</a>
        <a href="haircare.html" class="t" data-fr="Cheveux &amp; Corps" data-en="Hair &amp; Body">Cheveux &amp; Corps</a>
        <a href="marques.html" class="t" data-fr="Marques" data-en="Brands">Marques</a>
        <div class="nd-sep"></div>
        <a href="skincare.html?cat=coffret" class="t" data-fr="Coffrets &amp; Bundles" data-en="Sets &amp; Bundles">Coffrets &amp; Bundles</a>
      </div></li>
      <li class="nav-item"><a href="masterclasses.html"{ACTIVE_MASTER} data-fr="Masterclasses" data-en="Masterclasses">Masterclasses</a></li>
      <li class="nav-item"><a href="journal.html"{ACTIVE_JOURNAL} data-fr="Journal" data-en="Journal">Journal</a></li>
      <li class="nav-item"><a href="about.html"{ACTIVE_ABOUT} data-fr="À propos" data-en="About">À propos</a></li>
      <li class="nav-item glossary-2line"><a href="glossaire.html"{ACTIVE_GLOSS} data-fr="KBeauty<br>Glossary" data-en="KBeauty<br>Glossary">KBeauty<br>Glossary</a></li>
    </ul>'''

NEW_MOB_L1 = '''<nav class="mob-panel active" id="mob-l1">
    <a class="mob-cat-link t" data-fr="La Boutique <span>›</span>" data-en="The Shop <span>›</span>" onclick="mobDrill('mob-l2-skincare','La Boutique')">La Boutique <span>›</span></a>
    <a href="masterclasses.html" onclick="closeMobileMenu()" class="mob-cat-link t" data-fr="Masterclasses" data-en="Masterclasses">Masterclasses</a>
    <a href="journal.html" onclick="closeMobileMenu()" class="mob-cat-link t" data-fr="Journal" data-en="Journal">Journal</a>
    <a href="about.html" onclick="closeMobileMenu()" class="mob-cat-link t" data-fr="À propos" data-en="About">À propos</a>
    <a href="glossaire.html" onclick="closeMobileMenu()" class="mob-cat-link t" data-fr="KBeauty Glossary" data-en="KBeauty Glossary">KBeauty Glossary</a>
  </nav>'''

NEW_FOOTER_BOUTIQUE_INNER = '''<h4 class="t" data-fr="La Boutique" data-en="The Shop">La Boutique</h4>
        <ul>
          <li><a href="skincare.html" class="t" data-fr="Skincare" data-en="Skincare">Skincare</a></li>
          <li><a href="maquillage.html" class="t" data-fr="Maquillage" data-en="Makeup">Maquillage</a></li>
          <li><a href="haircare.html" class="t" data-fr="Cheveux &amp; Corps" data-en="Hair &amp; Body">Cheveux &amp; Corps</a></li>
          <li><a href="marques.html" class="t" data-fr="Toutes les marques" data-en="All brands">Toutes les marques</a></li>
        </ul>'''

NEW_FOOTER_INFOS_INNER = '''<h4 class="t" data-fr="Informations" data-en="Information">Informations</h4>
        <ul>
          <li><a href="about.html" class="t" data-fr="À propos" data-en="About">À propos</a></li>
          <li><a href="journal.html" class="t" data-fr="Journal" data-en="Journal">Journal</a></li>
          <li><a href="masterclasses.html" class="t" data-fr="Masterclasses" data-en="Masterclasses">Masterclasses</a></li>
          <li><a href="glossaire.html" class="t" data-fr="KBeauty Glossary" data-en="KBeauty Glossary">KBeauty Glossary</a></li>
          <li><a href="rewards.html" class="t" data-fr="Sonagi Rewards" data-en="Sonagi Rewards">Sonagi Rewards</a></li>
          <li><a href="faq.html" class="t" data-fr="FAQ" data-en="FAQ">FAQ</a></li>
        </ul>'''


# ---- Active-class map (per page) ------------------------------------------

ACTIVE_MAP = {
    "skincare.html":      "BOUTIQUE",
    "maquillage.html":    "BOUTIQUE",
    "haircare.html":      "BOUTIQUE",
    "marques.html":       "BOUTIQUE",
    "produit.html":       "BOUTIQUE",
    "masterclasses.html": "MASTER",
    "journal.html":       "JOURNAL",
    "about.html":         "ABOUT",
    "glossaire.html":     "GLOSS",
}


def build_nav(active_key):
    repl = {"BOUTIQUE": "", "MASTER": "", "JOURNAL": "", "ABOUT": "", "GLOSS": ""}
    if active_key:
        repl[active_key] = ' class="active"'
    out = NEW_NAV_LINKS
    out = out.replace("{ACTIVE_BOUTIQUE}", repl["BOUTIQUE"])
    out = out.replace("{ACTIVE_MASTER}",   repl["MASTER"])
    out = out.replace("{ACTIVE_JOURNAL}",  repl["JOURNAL"])
    out = out.replace("{ACTIVE_ABOUT}",    repl["ABOUT"])
    out = out.replace("{ACTIVE_GLOSS}",    repl["GLOSS"])
    return out


# ---- Regex patterns -------------------------------------------------------

# Match the full <ul class="nav-links">... </ul> block (lazy, single or multi-line)
NAV_UL_RX = re.compile(r'<ul class="nav-links">.*?</ul>', re.DOTALL)

# Match the existing mob-l1 panel <nav class="mob-panel active" id="mob-l1"> ... </nav>
MOB_L1_RX = re.compile(
    r'<nav class="mob-panel active" id="mob-l1">.*?</nav>',
    re.DOTALL,
)

# Match the existing Boutique footer column block (h4 ... </ul>)
FOOTER_BOUTIQUE_RX = re.compile(
    r'<h4 class="t" data-fr="Boutique" data-en="Shop">Boutique</h4>\s*<ul>.*?</ul>',
    re.DOTALL,
)

# Match the existing Informations footer column block
FOOTER_INFOS_RX = re.compile(
    r'<h4 class="t" data-fr="Informations" data-en="Information">Informations</h4>\s*<ul>.*?</ul>',
    re.DOTALL,
)


def process_file(path: Path):
    name = path.name
    src = path.read_text(encoding="utf-8")
    orig = src

    # 1. Update nav-links
    active_key = ACTIVE_MAP.get(name, "")
    new_nav = build_nav(active_key)
    src, n_nav = NAV_UL_RX.subn(new_nav, src, count=1)

    # 2. Update mob-l1 (only if present)
    src, n_mob = MOB_L1_RX.subn(NEW_MOB_L1, src, count=1)

    # 3. Update footer Boutique column inner content
    src, n_b = FOOTER_BOUTIQUE_RX.subn(NEW_FOOTER_BOUTIQUE_INNER, src, count=1)

    # 4. Update footer Informations column inner content
    src, n_i = FOOTER_INFOS_RX.subn(NEW_FOOTER_INFOS_INNER, src, count=1)

    if src != orig:
        path.write_text(src, encoding="utf-8")
    return name, n_nav, n_mob, n_b, n_i


def main():
    files = sorted(FILES_DIR.glob("*.html"))
    print(f"Processing {len(files)} files")
    for p in files:
        name, n_nav, n_mob, n_b, n_i = process_file(p)
        print(f"  {name:36s}  nav={n_nav}  mob-l1={n_mob}  foot-boutique={n_b}  foot-infos={n_i}")


if __name__ == "__main__":
    main()
