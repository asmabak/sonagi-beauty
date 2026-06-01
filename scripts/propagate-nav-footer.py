#!/usr/bin/env python3
"""
One-shot script: propagate the new NAV + MOBILE MENU + FOOTER + bottom-of-body scripts
from index.html to 11 other pages of the Sonagi Beauty static site.

Reads exact blocks from index.html (the source of truth) and replaces equivalent
blocks in each target page. Idempotent: re-running produces the same output.
"""

import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\marou\sonagi-beauty\files")
INDEX = ROOT / "index.html"

PAGES = [
    "skincare.html",
    "maquillage.html",
    "haircare.html",
    "marques.html",
    "masterclasses.html",
    "journal.html",
    "compte.html",
    "panier.html",
    "produit.html",
    "rewards.html",
    "confirmation.html",
]


def slice_block(text, start_pat, end_pat, *, include_end=True, flags=re.DOTALL):
    """Return the substring from the first match of start_pat to the next end_pat."""
    sm = re.search(start_pat, text, flags)
    if not sm:
        raise ValueError(f"start pattern not found: {start_pat!r}")
    em = re.search(end_pat, text[sm.start():], flags)
    if not em:
        raise ValueError(f"end pattern not found after start: {end_pat!r}")
    end_abs = sm.start() + em.end() if include_end else sm.start() + em.start()
    return text[sm.start():end_abs]


def main():
    src = INDEX.read_text(encoding="utf-8")

    # Source-of-truth blocks from index.html
    new_nav = slice_block(src, r'<nav class="main-nav">', r'</nav>')
    # Mobile menu lives in a <div class="mobile-menu" ...>...</div>
    # We need its enclosing element including the mob-backdrop preceding sibling
    # but per spec we only replace the mobile-menu div itself. The mob-backdrop
    # already exists on every target page directly above mobile-menu (or sometimes
    # before nav). We will just replace the mobile-menu div block.
    new_mobile = slice_block(
        src,
        r'<div class="mobile-menu" id="mobile-menu">',
        r'</div>\s*\n',  # the closing </div> of the mobile-menu wrapper
        include_end=False,
    )
    # The above stops just before the closing </div>. Add it back, plus the closing.
    # Actually, the mobile-menu wrapper has nested divs, so we need a smarter parser.
    # Manually find the matching close by counting depth.
    new_mobile = extract_balanced_div(src, '<div class="mobile-menu" id="mobile-menu">')

    new_footer = extract_balanced_tag(src, "<footer>", "</footer>")

    # Bottom-of-body new scripts block (consent + geo-detect + currency)
    new_bottom_scripts = '''<script src="js/sonagi-consent.js" defer></script>
<script>
(function(){
  function applyLang(l){ if (typeof setLang==='function') setLang(l); }
  var saved = null;
  try { saved = localStorage.getItem('sonagi_lang'); } catch(e){}
  if (saved === 'fr' || saved === 'en') { applyLang(saved); return; }
  var langs = (navigator.languages || [navigator.language || 'fr']).map(function(s){return (s||'').toLowerCase()});
  var browserIsFr = langs.some(function(l){ return l.indexOf('fr') === 0; });
  var browserIsEn = langs.some(function(l){ return l.indexOf('en') === 0; });
  var FR_COUNTRIES = {FR:1,BE:1,CH:1,MC:1,LU:1,CA:1,TN:1,MA:1,DZ:1,SN:1,CI:1,CD:1,MG:1,RE:1,GP:1,MQ:1,GF:1,YT:1,PF:1,NC:1};
  var done = false;
  function decide(country){
    if (done) return; done = true;
    var lang = 'en';
    if (country && FR_COUNTRIES[country]) lang = 'fr';
    else if (browserIsFr && !browserIsEn) lang = 'fr';
    else if (!browserIsFr && browserIsEn) lang = 'en';
    else if (browserIsFr) lang = 'fr';
    applyLang(lang);
    try { localStorage.setItem('sonagi_lang', lang); } catch(e){}
  }
  var fallbackTimer = setTimeout(function(){ decide(null); }, 250);
  fetch('https://ipapi.co/country/', {cache:'force-cache'})
    .then(function(r){ return r.ok ? r.text() : null; })
    .then(function(c){ clearTimeout(fallbackTimer); decide(c ? c.trim().toUpperCase() : null); })
    .catch(function(){ clearTimeout(fallbackTimer); decide(null); });
})();
</script>
<script src="js/sonagi-currency.js" defer></script>
'''

    # New footer must use the spec footer (not index.html's exact one) because
    # we need: Informations col with Glossaire + À propos + FAQ; legal links anchored.
    # Build from scratch using index.html's footer-pay/footer-lang block as base.
    new_footer = build_spec_footer()

    print(f"== loaded blocks ==")
    print(f"  nav: {len(new_nav)} chars")
    print(f"  mobile menu: {len(new_mobile)} chars")
    print(f"  footer: {len(new_footer)} chars")
    print(f"  bottom scripts: {len(new_bottom_scripts)} chars")
    print()

    summary = []
    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            summary.append((name, "MISSING"))
            continue
        text = path.read_text(encoding="utf-8")
        original = text

        # 1) Replace <nav class="main-nav">...</nav>
        text, nav_ok = replace_balanced_tag(text, "<nav class=\"main-nav\">", "</nav>", new_nav)

        # 2) Replace <div class="mobile-menu" id="mobile-menu">...balanced</div>
        text, mob_ok = replace_balanced_div(text, '<div class="mobile-menu" id="mobile-menu">', new_mobile)

        # 3) Replace <footer>...</footer>
        text, foot_ok = replace_balanced_tag(text, "<footer>", "</footer>", new_footer)

        # 4) Insert bottom-of-body scripts just before </body>, idempotently
        if "js/sonagi-consent.js" in text:
            scripts_ok = "ALREADY"
        else:
            text, scripts_ok = insert_before_body_close(text, new_bottom_scripts)

        if text != original:
            path.write_text(text, encoding="utf-8")

        summary.append((name, f"nav={nav_ok} mob={mob_ok} foot={foot_ok} scripts={scripts_ok}"))

    print("== summary ==")
    for n, s in summary:
        print(f"  {n:25s} -> {s}")


def extract_balanced_div(text, opening):
    """Extract a balanced <div ...>...</div> starting at the given opening tag."""
    i = text.find(opening)
    if i < 0:
        raise ValueError(f"opening tag not found: {opening!r}")
    return _balanced(text, i, "div")


def extract_balanced_tag(text, opening, closing):
    """Extract a balanced block starting at `opening` and ending at first `closing`
       at the same depth (only useful for non-nested same-tag contexts like <footer>)."""
    i = text.find(opening)
    if i < 0:
        raise ValueError(f"opening tag not found: {opening!r}")
    j = text.find(closing, i)
    if j < 0:
        raise ValueError(f"closing tag not found: {closing!r}")
    return text[i:j + len(closing)]


def _balanced(text, start_idx, tag_name):
    """Walk forward from start_idx of `<tag ...>`, count opens and closes of tag_name,
       return the slice through and including the matching close."""
    open_re = re.compile(rf'<{tag_name}\b[^>]*>', re.IGNORECASE)
    close_re = re.compile(rf'</{tag_name}\s*>', re.IGNORECASE)
    depth = 0
    pos = start_idx
    while pos < len(text):
        om = open_re.search(text, pos)
        cm = close_re.search(text, pos)
        if not cm:
            raise ValueError(f"unmatched <{tag_name}> from index {start_idx}")
        if om and om.start() < cm.start():
            depth += 1
            pos = om.end()
        else:
            depth -= 1
            pos = cm.end()
            if depth == 0:
                return text[start_idx:pos]
    raise ValueError(f"never balanced <{tag_name}> from index {start_idx}")


def replace_balanced_tag(text, opening, closing, replacement):
    try:
        block = extract_balanced_tag(text, opening, closing)
        return text.replace(block, replacement, 1), "OK"
    except ValueError as e:
        return text, f"FAIL({e})"


def replace_balanced_div(text, opening, replacement):
    try:
        block = extract_balanced_div(text, opening)
        return text.replace(block, replacement, 1), "OK"
    except ValueError as e:
        return text, f"FAIL({e})"


def insert_before_body_close(text, snippet):
    if "</body>" not in text:
        return text, "FAIL(no </body>)"
    # Insert snippet right before </body>, with a trailing newline
    return text.replace("</body>", snippet + "</body>", 1), "OK"


def build_spec_footer():
    """Build the new footer per spec, based on index.html's footer but with:
       - Informations col: Journal / Masterclasses / Glossaire / Sonagi Rewards / À propos / FAQ
       - footer-bottom legal text replaced with 4 anchored links
       - keeps the language pill row + payment strip
    """
    return '''<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div>
        <a href="index.html" class="footer-logo">SONAGI<small>소나기 · K-Beauty</small></a>
        <p class="footer-desc t" data-fr="K-beauty curatée, sélection coréenne pensée pour les peaux françaises." data-en="Curated K-beauty, a Korean selection made for French skin.">K-beauty curatée, sélection coréenne pensée pour les peaux françaises.</p>
      </div>
      <div class="footer-col">
        <h4 class="t" data-fr="Boutique" data-en="Shop">Boutique</h4>
        <ul>
          <li><a href="skincare.html" class="t" data-fr="Skincare" data-en="Skincare">Skincare</a></li>
          <li><a href="maquillage.html" class="t" data-fr="Maquillage" data-en="Makeup">Maquillage</a></li>
          <li><a href="haircare.html" class="t" data-fr="Cheveux & Corps" data-en="Hair & Body">Cheveux & Corps</a></li>
          <li><a href="marques.html" class="t" data-fr="Toutes les marques" data-en="All brands">Toutes les marques</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="t" data-fr="Informations" data-en="Information">Informations</h4>
        <ul>
          <li><a href="journal.html" class="t" data-fr="Journal" data-en="Journal">Journal</a></li>
          <li><a href="masterclasses.html" class="t" data-fr="Masterclasses" data-en="Masterclasses">Masterclasses</a></li>
          <li><a href="glossaire.html" class="t" data-fr="Glossaire" data-en="Glossary">Glossaire</a></li>
          <li><a href="rewards.html" class="t" data-fr="Sonagi Rewards" data-en="Sonagi Rewards">Sonagi Rewards</a></li>
          <li><a href="about.html" class="t" data-fr="À propos" data-en="About">À propos</a></li>
          <li><a href="#" class="t" data-fr="FAQ" data-en="FAQ">FAQ</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="t" data-fr="Contact" data-en="Contact">Contact</h4>
        <ul>
          <li><a href="mailto:contact@sonagibeauty.com">contact@sonagibeauty.com</a></li>
          <li><a href="https://instagram.com/sonagi.beauty" target="_blank">Instagram</a></li>
          <li><a href="https://tiktok.com/@sonagi.beauty" target="_blank">TikTok</a></li>
          <li><a href="compte.html" class="t" data-fr="Mon compte" data-en="My account">Mon compte</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="t" data-fr="© 2026 Sonagi Beauty · Tous droits réservés" data-en="© 2026 Sonagi Beauty · All rights reserved">© 2026 Sonagi Beauty · Tous droits réservés</p>
      <p>
        <a href="mentions-legales.html" class="t" data-fr="Mentions légales" data-en="Legal notice">Mentions légales</a> ·
        <a href="cgv.html" class="t" data-fr="CGV" data-en="T&amp;Cs">CGV</a> ·
        <a href="politique-confidentialite.html" class="t" data-fr="Confidentialité" data-en="Privacy">Confidentialité</a> ·
        <a href="cookies.html" class="t" data-fr="Cookies" data-en="Cookies">Cookies</a>
      </p>
    </div>
    <style>
    .footer-lang{display:flex;justify-content:center;gap:8px;padding:18px 0 4px;border-top:1px solid rgba(255,255,255,.12);margin-top:18px}
    .footer-lang .lang-btn{background:transparent;color:rgba(255,255,255,.65);border:1px solid rgba(255,255,255,.2);padding:6px 14px;font-size:11px;font-weight:500;letter-spacing:1.5px;text-transform:uppercase;border-radius:20px;cursor:pointer;transition:all .2s}
    .footer-lang .lang-btn:hover{color:#fff;border-color:rgba(255,255,255,.5)}
    .footer-lang .lang-btn.active{background:var(--pink);border-color:var(--pink);color:#fff}
    .footer-lang-label{font-size:10px;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:2px;margin-right:6px;align-self:center}
    .footer-pay{display:flex;justify-content:center;gap:14px;padding:14px 0 8px;flex-wrap:wrap}
    .footer-pay span{font-size:10px;color:rgba(255,255,255,.45);letter-spacing:2px;text-transform:uppercase;font-weight:500}
    </style>
    <div class="footer-lang" role="group" aria-label="Choix de langue">
      <span class="footer-lang-label t" data-fr="Langue" data-en="Language">Langue</span>
      <button class="lang-btn active" id="fbtn-fr" onclick="setLang('fr');try{localStorage.setItem('sonagi_lang','fr')}catch(e){}">FR</button>
      <button class="lang-btn" id="fbtn-en" onclick="setLang('en');try{localStorage.setItem('sonagi_lang','en')}catch(e){}">EN</button>
    </div>
    <div class="footer-pay" aria-label="Moyens de paiement">
      <span>VISA</span><span>·</span><span>MASTERCARD</span><span>·</span><span>APPLE PAY</span><span>·</span><span>GOOGLE PAY</span><span>·</span><span>SEPA</span>
    </div>
  </div>
</footer>'''


if __name__ == "__main__":
    main()
