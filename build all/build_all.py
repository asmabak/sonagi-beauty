#!/usr/bin/env python3
"""
SONAGI BEAUTY — Site generator v5
Reads from template.pkl (shared CSS/JS) + extracted_imgs.pkl
Never edit HTML files directly — always edit source and regenerate.
"""
import pickle, os, re
from collections import defaultdict

# ── Load assets ─────────────────────────────────────────────────────────────
_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_dir)
_out = os.path.join(_root, 'files')
os.makedirs(_out, exist_ok=True)

with open(os.path.join(_dir, 'imgs_small.pkl'), 'rb') as f:
    imgs = pickle.load(f)
with open(os.path.join(_dir, 'template.pkl'), 'rb') as f:
    t = pickle.load(f)

P3='P3'; CX='CX'; GL='GL'; P1='P1'
P5='P5'; DR='DR'; P2='P2'; P8='P8'
HA='HA'; P6='P6'; P4='P4'; P7='P7'

# ── Visual image keys (file-path references for large visuals) ──────────────
HERO1       = 'HERO1'
HERO2       = 'HERO2'
CAT_SERUM   = 'CAT_SERUM'
CAT_CLEAN   = 'CAT_CLEAN'
CAT_MASK    = 'CAT_MASK'
CAT_EYE     = 'CAT_EYE'
CAT_LIP     = 'CAT_LIP'
CAT_MEN     = 'CAT_MEN'
CAT_SPF     = 'CAT_SPF'
BR_COSRX    = 'BR_COSRX'
BR_SBMI     = 'BR_SBMI'
BR_LAN      = 'BR_LAN'
BR_INN      = 'BR_INN'
BR_BOJ      = 'BR_BOJ'
BR_ANUA     = 'BR_ANUA'
BL_GLASS    = 'BL_GLASS'
BL_DOUBLE   = 'BL_DOUBLE'
BL_HANBANG  = 'BL_HANBANG'
BL_SPF      = 'BL_SPF'
BL_ACIDS    = 'BL_ACIDS'
BL_COLLAGEN = 'BL_COLLAGEN'
BL_ROUTINE  = 'BL_ROUTINE'
BL_MEN      = 'BL_MEN'
SOC1        = 'SOC1'
SOC2        = 'SOC2'
EMAIL_HDR   = 'EMAIL_HDR'
PROD_CLEAN  = 'PROD_CLEAN'
PROD_MARBLE = 'PROD_MARBLE'
SOC_STORY   = 'SOC_STORY'

# Map visual keys → file paths (relative to output HTML location)
_visuals = {
    HERO1:       '../images/visuals/sonagi-home_hero_1.png',
    HERO2:       '../images/visuals/sonagi-home_hero2.png.jpg',
    CAT_SERUM:   '../images/visuals/sonagi-cat_serum.png.jpg',
    CAT_CLEAN:   '../images/visuals/sonagi-cat_cleanser.png',
    CAT_MASK:    '../images/visuals/sonagi-cat_mask.png',
    CAT_EYE:     '../images/visuals/sonagi-cat_eyecare.png',
    CAT_LIP:     '../images/visuals/sonagi-cat_lip.png',
    CAT_MEN:     '../images/visuals/sonagi-cat_men.png',
    CAT_SPF:     '../images/visuals/sonagi-cat_spf.png.png',
    BR_COSRX:    '../images/visuals/sonagi-brand_cosrx.png',
    BR_SBMI:     '../images/visuals/sonagi-brand_somebymi.png',
    BR_LAN:      '../images/visuals/sonagi-brand_laneige.png',
    BR_INN:      '../images/visuals/sonagi-brand_innisfree.png',
    BR_BOJ:      '../images/visuals/sonagi-brand_boj.png.jpg',
    BR_ANUA:     '../images/visuals/sonagi-brand_anua.png',
    BL_GLASS:    '../images/visuals/sonagi-blog_glass.png',
    BL_DOUBLE:   '../images/visuals/sonagi-blog_double.png',
    BL_HANBANG:  '../images/visuals/sonagi-blog_hanbang.png',
    BL_SPF:      '../images/visuals/sonagi-blog_spf.png',
    BL_ACIDS:    '../images/visuals/sonagi-blog_acids.png',
    BL_COLLAGEN: '../images/visuals/sonagi-blog_collagen.png',
    BL_ROUTINE:  '../images/visuals/sonagi-blog_routine.jpg',
    BL_MEN:      '../images/visuals/sonagi-blog_men.jpg',
    SOC1:        '../images/visuals/sonagi-social_feed_1.png',
    SOC2:        '../images/visuals/sonagi-social_feed_2.png',
    EMAIL_HDR:   '../images/visuals/sonagi-email_header.png',
    PROD_CLEAN:  '../images/visuals/sonagi-prod_card_clean.png',
    PROD_MARBLE: '../images/visuals/sonagi-prod_card_marble.png',
    SOC_STORY:   '../images/visuals/sonagi-social_story_face.png',
}
imgs.update(_visuals)

# Build inline image JS - embeds all images directly in HTML
_img_pairs = ',\n  '.join(f'"{k}": "{v}"' for k, v in imgs.items())
IMGS_JS = f'window.QUIZ_IMGS = {{\n  {_img_pairs}\n}};'

SHARED_CSS  = t['SHARED_CSS']
SHARED_JS   = t['SHARED_JS']
QUIZ_JS     = t['QUIZ_JS']
ANNOUNCE    = t['ANNOUNCE']
FOOTER      = t['FOOTER']
CART        = t['CART_SIDEBAR']
QUIZ_MODAL  = t['QUIZ_MODAL']

# ── Image helper: uses data-imgkey, resolved by JS ───────────────────────────
def imgref(key, alt='', loading='lazy', cls=''):
    c = f' class="{cls}"' if cls else ''
    src = imgs.get(key, '')
    return f'<img src="{src}" alt="{alt}" loading="{loading}"{c}>'

# ── MEGA-NAV CSS ─────────────────────────────────────────────────────────────
MEGA_NAV_CSS = """
/* ── MEGA NAV ── */
.nav-item { position: relative; }
.nav-item > a { display: flex; align-items: center; gap: 4px; }
.nav-item.has-drop > a::after { content: ' ▾'; font-size: 9px; opacity: .6; }
.nav-dropdown { display: none; position: absolute; top: 100%; left: 0; background: #fff;
  border-radius: 12px; box-shadow: 0 8px 32px rgba(26,39,68,.12); min-width: 220px;
  padding: 10px 0; z-index: 300; }
@media(min-width:768px) {
  .nav-item:hover .nav-dropdown,
  .nav-item:focus-within .nav-dropdown { display: flex; flex-direction: column; }
  .nd-sub:hover .nd-sub-panel,
  .nd-sub:focus-within .nd-sub-panel { display: flex; flex-direction: column; }
}
.nav-dropdown a, .nav-dropdown button.nd-link {
  display: flex; align-items: center; justify-content: space-between;
  padding: 9px 18px; font-size: 13px; color: #2c2c2c; text-decoration: none;
  background: none; border: none; width: 100%; text-align: left; font-family: 'DM Sans',sans-serif;
  cursor: pointer; transition: background .15s; white-space: nowrap;
}
.nav-dropdown a:hover, .nav-dropdown button.nd-link:hover { background: #faf8f5; color: #1a2744; }
.nd-sep { height: 1px; background: #ede8e2; margin: 6px 12px; }
.nd-sub { position: relative; }
.nd-sub > button.nd-link::after { content: '›'; font-size: 14px; opacity: .5; }
.nd-sub-panel { display: none; position: absolute; left: 100%; top: 0;
  background: #fff; border-radius: 12px; box-shadow: 0 8px 32px rgba(26,39,68,.12);
  min-width: 200px; padding: 10px 0; z-index: 310; }
/* nd-sub hover handled above */
.nd-sub-panel a { padding: 9px 18px; font-size: 13px; color: #2c2c2c; text-decoration: none;
  transition: background .15s; white-space: nowrap; }
.nd-sub-panel a:hover { background: #faf8f5; color: #1a2744; }

/* mobile menu handled by shared.css */

/* ── INFLUENCER TIKTOK THUMBNAIL GRID ── */
.inf-video-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 28px; }
.inf-video-card { display: flex; flex-direction: column; border-radius: 12px; overflow: hidden;
  background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14);
  text-decoration: none; transition: transform .2s, background .2s; cursor: pointer; }
.inf-video-card:hover { transform: translateY(-4px); background: rgba(255,255,255,.12); }
.inf-video-thumb { position: relative; width: 100%; aspect-ratio: 9/16; overflow: hidden;
  background: rgba(255,255,255,.06); max-height: 320px; }
.inf-video-thumb img { width: 100%; height: 100%; object-fit: cover; }
.inf-play-btn { position: absolute; inset: 0; display: flex; align-items: center;
  justify-content: center; background: rgba(0,0,0,.25); transition: background .2s; }
.inf-video-card:hover .inf-play-btn { background: rgba(0,0,0,.4); }
.inf-play-btn svg { filter: drop-shadow(0 2px 6px rgba(0,0,0,.5)); }
.inf-tt-badge { position: absolute; bottom: 8px; left: 8px; background: rgba(0,0,0,.6);
  color: #fff; font-size: 10px; letter-spacing: 1px; padding: 3px 8px; border-radius: 20px;
  display: flex; align-items: center; gap: 4px; }
.inf-video-info { padding: 11px 14px; display: flex; flex-direction: column; gap: 3px; flex-shrink: 0; }
.inf-video-title { font-size: 12px; color: rgba(255,255,255,.9); line-height: 1.4; margin: 2px 0 3px; font-weight: 500; }
.inf-watch-cta { font-size: 10px; letter-spacing: 1px; color: #f5c4aa; color: var(--peach);
  text-transform: uppercase; margin-top: 2px; }

/* ── REVIEW CARD REDESIGN ── */
.rev-stars-top { font-size: 14px; color: #f5a623; color: var(--gold); margin-bottom: 10px; letter-spacing: 2px; }
.rev-footer { display: flex; align-items: center; gap: 10px; margin-top: 14px; padding-top: 12px;
  border-top: 1px solid #ede8e2; border-top: 1px solid var(--border); }
.rev-city { font-size: 10px; color: #8a8a8a; color: var(--muted); font-weight: 400; }

@media(min-width:768px) {
  .inf-video-grid { grid-template-columns: repeat(4, 1fr); gap: 18px; }
  .inf-video-thumb { max-height: 280px; }
}
"""

# ── MEGA-NAV HTML ─────────────────────────────────────────────────────────────
def NAV(active=''):
    def li(href, fr, en, dropdown=''):
        cls = " class='active'" if fr == active else ""
        if dropdown:
            return f'<li class="nav-item has-drop"><a href="{href}"{cls} data-fr="{fr}" data-en="{en}">{fr}</a>{dropdown}</li>'
        return f'<li class="nav-item"><a href="{href}"{cls} data-fr="{fr}" data-en="{en}">{fr}</a></li>'

    sk_drop = """<div class="nav-dropdown">
      <a href="skincare.html">Best Sellers</a>
      <div class="nd-sep"></div>
      <div class="nd-sub"><button class="nd-link">Type de produit</button>
        <div class="nd-sub-panel">
          <a href="skincare.html?cat=nettoyant">Nettoyant</a>
          <a href="skincare.html?cat=toner">Toner</a>
          <a href="skincare.html?cat=exfoliant">Exfoliant / Gommage</a>
          <a href="skincare.html?cat=essence">Essence</a>
          <a href="skincare.html?cat=serum">Ampoule / Sérum</a>
          <a href="skincare.html?cat=contour-yeux">Contour des Yeux</a>
          <a href="skincare.html?cat=creme">Crème Hydratante</a>
          <a href="skincare.html?cat=spf">Crème Solaire</a>
          <a href="skincare.html?cat=masque">Masque à Rincer</a>
          <a href="skincare.html?cat=masque-tissu">Masque en Tissu</a>
        </div>
      </div>
      <div class="nd-sub"><button class="nd-link">Type de peau</button>
        <div class="nd-sub-panel">
          <a href="skincare.html?cat=peau-grasse">Peau Grasse</a>
          <a href="skincare.html?cat=peau-seche">Peau Sèche</a>
          <a href="skincare.html?cat=peau-mixte">Peau Mixte</a>
          <a href="skincare.html?cat=peau-normale">Peau Normale</a>
          <a href="skincare.html?cat=peau-sensible">Peau Sensible</a>
        </div>
      </div>
      <div class="nd-sub"><button class="nd-link">Préoccupation</button>
        <div class="nd-sub-panel">
          <a href="skincare.html?cat=acne">Acné</a>
          <a href="skincare.html?cat=pores">Pores dilatés &amp; Points noirs</a>
          <a href="skincare.html?cat=eclat">Teint terne &amp; Hyperpigmentation</a>
          <a href="skincare.html?cat=hydratation">Déshydratation</a>
          <a href="skincare.html?cat=anti-age">Rides &amp; Élasticité</a>
          <a href="skincare.html?cat=anti-rougeurs">Rougeurs &amp; Inflammations</a>
          <a href="skincare.html?cat=barriere">Barrière endommagée</a>
        </div>
      </div>
      <div class="nd-sep"></div>
      <a href="skincare.html?cat=coffret">Coffrets &amp; Bundles</a>
    </div>"""

    mq_drop = """<div class="nav-dropdown">
      <a href="maquillage.html">Tout le maquillage</a>
      <a href="maquillage.html?cat=demaquillant">Démaquillant</a>
      <div class="nd-sep"></div>
      <div class="nd-sub"><button class="nd-link">Yeux</button>
        <div class="nd-sub-panel">
          <a href="maquillage.html?cat=fard">Fard à paupières</a>
          <a href="maquillage.html?cat=mascara">Mascara</a>
          <a href="maquillage.html?cat=liner">Liner &amp; Crayon</a>
        </div>
      </div>
      <div class="nd-sub"><button class="nd-link">Lèvres</button>
        <div class="nd-sub-panel">
          <a href="maquillage.html?cat=rouge-a-levres">Rouge à lèvres</a>
          <a href="maquillage.html?cat=baume-levres">Baume à lèvres</a>
          <a href="maquillage.html?cat=gloss">Gloss &amp; Soins</a>
          <a href="maquillage.html?cat=tint">Tint lèvres</a>
        </div>
      </div>
      <div class="nd-sub"><button class="nd-link">Teint</button>
        <div class="nd-sub-panel">
          <a href="maquillage.html?cat=cushion">Cushion / BB Crème</a>
          <a href="maquillage.html?cat=concealer">Concealer</a>
          <a href="maquillage.html?cat=bronzer">Bronzer / Highlighter</a>
          <a href="maquillage.html?cat=blush">Blush</a>
          <a href="maquillage.html?cat=poudre">Poudre / Fixateur</a>
        </div>
      </div>
      <div class="nd-sep"></div>
      <a href="maquillage.html?cat=accessoires">Accessoires</a>
    </div>"""

    hc_drop = """<div class="nav-dropdown">
      <a href="haircare.html">Tout Cheveux &amp; Corps</a>
      <div class="nd-sep"></div>
      <div class="nd-sub"><button class="nd-link">Cheveux</button>
        <div class="nd-sub-panel">
          <a href="haircare.html?cat=shampooing">Shampooing</a>
          <a href="haircare.html?cat=apres-shampooing">Après-shampooing</a>
          <a href="haircare.html?cat=masque">Soins &amp; Traitements</a>
          <a href="haircare.html?cat=serum">Sérum capillaire</a>
        </div>
      </div>
      <div class="nd-sub"><button class="nd-link">Corps</button>
        <div class="nd-sub-panel">
          <a href="haircare.html?cat=corps">Lotion pour le corps</a>
          <a href="haircare.html?cat=gommage">Exfoliant corps</a>
        </div>
      </div>
    </div>"""

    nav_links = [
        li('skincare.html',      'Skincare',        'Skincare',       sk_drop),
        li('maquillage.html',    'Maquillage',      'Makeup',         mq_drop),
        li('haircare.html',      'Cheveux & Corps', 'Hair & Body',    hc_drop),
        li('marques.html',       'Marques',         'Brands'),
        li('masterclasses.html', 'Masterclasses',   'Masterclasses'),
        li('journal.html',       'Journal',         'Journal'),
    ]

    # Mobile menu with collapsible sections
    mob_nav = f"""
    <div class="mob-section">
      <button class="mob-section-title" onclick="toggleMobSection(this)">Skincare</button>
      <div class="mob-sub">
        <div class="mob-sub-group"><div class="mob-sub-group-title">Type de produit</div>
          <a href="skincare.html?cat=nettoyant">Nettoyant</a>
          <a href="skincare.html?cat=toner">Toner</a>
          <a href="skincare.html?cat=exfoliant">Exfoliant / Gommage</a>
          <a href="skincare.html?cat=essence">Essence</a>
          <a href="skincare.html?cat=serum">Ampoule / Sérum</a>
          <a href="skincare.html?cat=creme">Crème Hydratante</a>
          <a href="skincare.html?cat=spf">Crème Solaire</a>
          <a href="skincare.html?cat=masque">Masque</a>
        </div>
        <div class="mob-sub-group"><div class="mob-sub-group-title">Type de peau</div>
          <a href="skincare.html?cat=peau-grasse">Peau Grasse</a>
          <a href="skincare.html?cat=peau-seche">Peau Sèche</a>
          <a href="skincare.html?cat=peau-mixte">Peau Mixte</a>
          <a href="skincare.html?cat=peau-sensible">Peau Sensible</a>
        </div>
        <div class="mob-sub-group"><div class="mob-sub-group-title">Préoccupation</div>
          <a href="skincare.html?cat=acne">Acné</a>
          <a href="skincare.html?cat=pores">Pores &amp; Points noirs</a>
          <a href="skincare.html?cat=eclat">Teint terne &amp; Hyperpigmentation</a>
          <a href="skincare.html?cat=hydratation">Déshydratation</a>
          <a href="skincare.html?cat=anti-age">Rides &amp; Élasticité</a>
          <a href="skincare.html?cat=anti-rougeurs">Rougeurs &amp; Inflammations</a>
          <a href="skincare.html?cat=barriere">Barrière endommagée</a>
        </div>
        <a href="skincare.html?cat=coffret">Coffrets &amp; Bundles</a>
      </div>
    </div>
    <div class="mob-section">
      <button class="mob-section-title" onclick="toggleMobSection(this)">Maquillage</button>
      <div class="mob-sub">
        <div class="mob-sub-group"><div class="mob-sub-group-title">Yeux</div>
          <a href="maquillage.html?cat=fard">Fard à paupières</a>
          <a href="maquillage.html?cat=mascara">Mascara</a>
          <a href="maquillage.html?cat=liner">Liner &amp; Crayon</a>
        </div>
        <div class="mob-sub-group"><div class="mob-sub-group-title">Lèvres</div>
          <a href="maquillage.html?cat=rouge-a-levres">Rouge à lèvres</a>
          <a href="maquillage.html?cat=baume-levres">Baume à lèvres</a>
          <a href="maquillage.html?cat=gloss">Gloss &amp; Soins</a>
          <a href="maquillage.html?cat=tint">Tint lèvres</a>
        </div>
        <div class="mob-sub-group"><div class="mob-sub-group-title">Teint</div>
          <a href="maquillage.html?cat=cushion">Cushion / BB Crème</a>
          <a href="maquillage.html?cat=blush">Blush</a>
          <a href="maquillage.html?cat=poudre">Poudre / Fixateur</a>
        </div>
        <a href="maquillage.html?cat=demaquillant">Démaquillant</a>
        <a href="maquillage.html?cat=accessoires">Accessoires</a>
      </div>
    </div>
    <div class="mob-section">
      <button class="mob-section-title" onclick="toggleMobSection(this)">Cheveux &amp; Corps</button>
      <div class="mob-sub">
        <div class="mob-sub-group"><div class="mob-sub-group-title">Cheveux</div>
          <a href="haircare.html?cat=shampooing">Shampooing</a>
          <a href="haircare.html?cat=apres-shampooing">Après-shampooing</a>
          <a href="haircare.html?cat=masque">Soins &amp; Traitements</a>
          <a href="haircare.html?cat=serum">Sérum capillaire</a>
        </div>
        <div class="mob-sub-group"><div class="mob-sub-group-title">Corps</div>
          <a href="haircare.html?cat=corps">Lotion corps</a>
          <a href="haircare.html?cat=gommage">Exfoliant corps</a>
        </div>
      </div>
    </div>
    <a href="marques.html" onclick="closeMobileMenu()" style="display:block;font-family:'Cormorant Garamond',serif;font-size:18px;color:#1a2744;padding:10px 0;border-bottom:1px solid #ede8e2;text-decoration:none">Marques</a>
    <a href="masterclasses.html" onclick="closeMobileMenu()" style="display:block;font-family:'Cormorant Garamond',serif;font-size:18px;color:#1a2744;padding:10px 0;border-bottom:1px solid #ede8e2;text-decoration:none">Masterclasses</a>
    <a href="journal.html" onclick="closeMobileMenu()" style="display:block;font-family:'Cormorant Garamond',serif;font-size:18px;color:#1a2744;padding:10px 0;border-bottom:1px solid #ede8e2;text-decoration:none">Journal</a>
    """

    return f'''<nav class="main-nav">
  <div class="nav-inner">
    <a href="index.html" class="nav-logo">SONAGI<small>소나기 · K-Beauty</small></a>
    <ul class="nav-links">{''.join(nav_links)}</ul>
    <div class="nav-right">
      <button class="lang-btn active" id="btn-fr" onclick="setLang('fr')">FR</button>
      <button class="lang-btn" id="btn-en" onclick="setLang('en')">EN</button>
      <button class="quiz-nav-btn t" data-fr="Ma routine" data-en="My routine" onclick="openQuiz()">Ma routine</button>
      <button class="nav-icon" onclick="toggleCart()" aria-label="Panier">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        <span class="cart-badge" id="cart-badge" style="display:none">0</span>
      </button>
      <button class="hamburger" onclick="openMobileMenu()" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>
<div class="mob-backdrop" id="mob-backdrop" onclick="closeMobileMenu()"></div>
<div class="mobile-menu" id="mobile-menu">
  <div class="mobile-menu-head">
    <button class="mob-back" id="mob-back" onclick="mobBack()" style="display:none;background:none;border:none;font-size:20px;color:var(--navy);padding:0 8px 0 0">&#8249;</button>
    <span class="mobile-menu-logo" id="mob-title">SONAGI</span>
    <button class="mobile-menu-close" onclick="closeMobileMenu()">&#215;</button>
  </div>

  <!-- LEVEL 1: top categories -->
  <nav class="mob-panel active" id="mob-l1">
    <a class="mob-cat-link" onclick="mobDrill('mob-l2-skincare','Skincare')">Skincare <span>›</span></a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l2-maquillage','Maquillage')">Maquillage <span>›</span></a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l2-haircare','Cheveux &amp; Corps')">Cheveux &amp; Corps <span>›</span></a>
    <a href="marques.html" onclick="closeMobileMenu()" class="mob-cat-link">Marques</a>
    <a href="masterclasses.html" onclick="closeMobileMenu()" class="mob-cat-link">Masterclasses</a>
    <a href="journal.html" onclick="closeMobileMenu()" class="mob-cat-link">Journal</a>
  </nav>

  <!-- LEVEL 2: Skincare -->
  <nav class="mob-panel" id="mob-l2-skincare">
    <a href="skincare.html" onclick="closeMobileMenu()" class="mob-cat-link mob-all">Tout le Skincare</a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-sk-type','Type de produit')">Type de produit <span>›</span></a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-sk-peau','Type de peau')">Type de peau <span>›</span></a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-sk-concern','Préoccupation')">Préoccupation <span>›</span></a>
    <a href="skincare.html?cat=coffret" onclick="closeMobileMenu()" class="mob-cat-link">Coffrets &amp; Bundles</a>
  </nav>

  <!-- LEVEL 3: Skincare > Type de produit -->
  <nav class="mob-panel" id="mob-l3-sk-type">
    <a href="skincare.html?cat=nettoyant" onclick="closeMobileMenu()" class="mob-item-link">Nettoyant</a>
    <a href="skincare.html?cat=toner" onclick="closeMobileMenu()" class="mob-item-link">Toner</a>
    <a href="skincare.html?cat=exfoliant" onclick="closeMobileMenu()" class="mob-item-link">Exfoliant / Gommage</a>
    <a href="skincare.html?cat=essence" onclick="closeMobileMenu()" class="mob-item-link">Essence</a>
    <a href="skincare.html?cat=serum" onclick="closeMobileMenu()" class="mob-item-link">Ampoule / Sérum</a>
    <a href="skincare.html?cat=contour-yeux" onclick="closeMobileMenu()" class="mob-item-link">Contour des Yeux</a>
    <a href="skincare.html?cat=creme" onclick="closeMobileMenu()" class="mob-item-link">Crème Hydratante</a>
    <a href="skincare.html?cat=spf" onclick="closeMobileMenu()" class="mob-item-link">Crème Solaire</a>
    <a href="skincare.html?cat=masque" onclick="closeMobileMenu()" class="mob-item-link">Masque à Rincer</a>
    <a href="skincare.html?cat=masque-tissu" onclick="closeMobileMenu()" class="mob-item-link">Masque en Tissu</a>
  </nav>

  <!-- LEVEL 3: Skincare > Type de peau -->
  <nav class="mob-panel" id="mob-l3-sk-peau">
    <a href="skincare.html?cat=peau-grasse" onclick="closeMobileMenu()" class="mob-item-link">Peau Grasse</a>
    <a href="skincare.html?cat=peau-seche" onclick="closeMobileMenu()" class="mob-item-link">Peau Sèche</a>
    <a href="skincare.html?cat=peau-mixte" onclick="closeMobileMenu()" class="mob-item-link">Peau Mixte</a>
    <a href="skincare.html?cat=peau-normale" onclick="closeMobileMenu()" class="mob-item-link">Peau Normale</a>
    <a href="skincare.html?cat=peau-sensible" onclick="closeMobileMenu()" class="mob-item-link">Peau Sensible</a>
  </nav>

  <!-- LEVEL 3: Skincare > Préoccupation -->
  <nav class="mob-panel" id="mob-l3-sk-concern">
    <a href="skincare.html?cat=acne" onclick="closeMobileMenu()" class="mob-item-link">Acné</a>
    <a href="skincare.html?cat=pores" onclick="closeMobileMenu()" class="mob-item-link">Pores dilatés &amp; Points noirs</a>
    <a href="skincare.html?cat=eclat" onclick="closeMobileMenu()" class="mob-item-link">Teint terne &amp; Hyperpigmentation</a>
    <a href="skincare.html?cat=hydratation" onclick="closeMobileMenu()" class="mob-item-link">Déshydratation</a>
    <a href="skincare.html?cat=anti-age" onclick="closeMobileMenu()" class="mob-item-link">Rides &amp; Élasticité</a>
    <a href="skincare.html?cat=anti-rougeurs" onclick="closeMobileMenu()" class="mob-item-link">Rougeurs &amp; Inflammations</a>
    <a href="skincare.html?cat=barriere" onclick="closeMobileMenu()" class="mob-item-link">Barrière endommagée</a>
  </nav>

  <!-- LEVEL 2: Maquillage -->
  <nav class="mob-panel" id="mob-l2-maquillage">
    <a href="maquillage.html" onclick="closeMobileMenu()" class="mob-cat-link mob-all">Tout le Maquillage</a>
    <a href="maquillage.html?cat=demaquillant" onclick="closeMobileMenu()" class="mob-cat-link">Démaquillant</a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-mq-yeux','Yeux')">Yeux <span>›</span></a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-mq-levres','Lèvres')">Lèvres <span>›</span></a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-mq-teint','Teint')">Teint <span>›</span></a>
    <a href="maquillage.html?cat=accessoires" onclick="closeMobileMenu()" class="mob-cat-link">Accessoires</a>
  </nav>

  <!-- LEVEL 3: Maquillage > Yeux -->
  <nav class="mob-panel" id="mob-l3-mq-yeux">
    <a href="maquillage.html?cat=fard" onclick="closeMobileMenu()" class="mob-item-link">Fard à paupières</a>
    <a href="maquillage.html?cat=mascara" onclick="closeMobileMenu()" class="mob-item-link">Mascara</a>
    <a href="maquillage.html?cat=liner" onclick="closeMobileMenu()" class="mob-item-link">Liner &amp; Crayon</a>
  </nav>

  <!-- LEVEL 3: Maquillage > Lèvres -->
  <nav class="mob-panel" id="mob-l3-mq-levres">
    <a href="maquillage.html?cat=rouge-a-levres" onclick="closeMobileMenu()" class="mob-item-link">Rouge à lèvres</a>
    <a href="maquillage.html?cat=baume-levres" onclick="closeMobileMenu()" class="mob-item-link">Baume à lèvres</a>
    <a href="maquillage.html?cat=gloss" onclick="closeMobileMenu()" class="mob-item-link">Gloss &amp; Soins</a>
    <a href="maquillage.html?cat=tint" onclick="closeMobileMenu()" class="mob-item-link">Tint lèvres</a>
  </nav>

  <!-- LEVEL 3: Maquillage > Teint -->
  <nav class="mob-panel" id="mob-l3-mq-teint">
    <a href="maquillage.html?cat=cushion" onclick="closeMobileMenu()" class="mob-item-link">Cushion / BB Crème</a>
    <a href="maquillage.html?cat=concealer" onclick="closeMobileMenu()" class="mob-item-link">Concealer</a>
    <a href="maquillage.html?cat=bronzer" onclick="closeMobileMenu()" class="mob-item-link">Bronzer / Highlighter</a>
    <a href="maquillage.html?cat=blush" onclick="closeMobileMenu()" class="mob-item-link">Blush</a>
    <a href="maquillage.html?cat=poudre" onclick="closeMobileMenu()" class="mob-item-link">Poudre / Fixateur</a>
  </nav>

  <!-- LEVEL 2: Cheveux & Corps -->
  <nav class="mob-panel" id="mob-l2-haircare">
    <a href="haircare.html" onclick="closeMobileMenu()" class="mob-cat-link mob-all">Tout Cheveux &amp; Corps</a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-hc-cheveux','Cheveux')">Cheveux <span>›</span></a>
    <a class="mob-cat-link" onclick="mobDrill('mob-l3-hc-corps','Corps')">Corps <span>›</span></a>
  </nav>

  <!-- LEVEL 3: Cheveux -->
  <nav class="mob-panel" id="mob-l3-hc-cheveux">
    <a href="haircare.html?cat=shampooing" onclick="closeMobileMenu()" class="mob-item-link">Shampooing</a>
    <a href="haircare.html?cat=apres-shampooing" onclick="closeMobileMenu()" class="mob-item-link">Après-shampooing</a>
    <a href="haircare.html?cat=masque" onclick="closeMobileMenu()" class="mob-item-link">Soins &amp; Traitements</a>
    <a href="haircare.html?cat=serum" onclick="closeMobileMenu()" class="mob-item-link">Sérum capillaire</a>
  </nav>

  <!-- LEVEL 3: Corps -->
  <nav class="mob-panel" id="mob-l3-hc-corps">
    <a href="haircare.html?cat=corps" onclick="closeMobileMenu()" class="mob-item-link">Lotion pour le corps</a>
    <a href="haircare.html?cat=gommage" onclick="closeMobileMenu()" class="mob-item-link">Exfoliant corps</a>
  </nav>

  <div class="mobile-menu-foot">
    <div class="mob-lang">
      <button class="lang-btn active" id="mbtn-fr" onclick="setLang('fr')">FR</button>
      <button class="lang-btn" id="mbtn-en" onclick="setLang('en')">EN</button>
    </div>
    <button class="mob-quiz-btn t" data-fr="Ma routine personnalisée" data-en="My personalised routine" onclick="openQuiz();closeMobileMenu()">Ma routine personnalisée</button>
  </div>
</div>
'''


# ── Page wrapper — images load in <head> as blocking scripts ─────────────────
def page(title, body, active_nav='', extra_css=''):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,viewport-fit=cover">
<meta name="color-scheme" content="only light">
<meta name="theme-color" content="#faf8f5">
<title>{title} — Sonagi Beauty</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
{SHARED_CSS}
{MEGA_NAV_CSS}
{extra_css}
</style>
<script>
{IMGS_JS}
</script>
</head>
<body style="background:#faf8f5;color:#2c2c2c">
{ANNOUNCE}
{NAV(active_nav)}
{body}
{FOOTER}
{CART}
{QUIZ_MODAL}
<script>
{SHARED_JS}
{QUIZ_JS}
</script>
</body>
</html>'''

# ── Shared components ────────────────────────────────────────────────────────
def breadcrumb(items):
    parts = ''.join(
        f'<a href="{h}" data-fr="{f}" data-en="{e}">{f}</a><span>›</span>'
        if h else f'<span>{f}</span>'
        for f,e,h in items
    )
    return f'<div class="breadcrumb">{parts}</div>'

def prod_card(imgkey, brand, name, price, badge='', tags=None):
    bdg = f'<span class="prod-badge">{badge}</span>' if badge else ''
    tag_str = ' '.join(tags) if tags else ''
    dt = f' data-tags="{tag_str}"' if tag_str else ''
    return f'''<div class="prod-card"{dt}>
  <div class="prod-img-wrap">
    {bdg}
    {imgref(imgkey, name)}
    <button class="prod-add-btn t" data-fr="Ajouter au panier" data-en="Add to basket">Ajouter au panier</button>
  </div>
  <p class="prod-brand">{brand}</p>
  <p class="prod-name">{name}</p>
  <p class="prod-price">{price} €</p>
</div>'''

def cat_hero_card(imgkey, label_fr, label_en, sub_fr='Collection', sub_en='Collection', link='#'):
    return f'''<a href="{link}" class="cat-hero-card">
  {imgref(imgkey, label_fr)}
  <div class="cat-hero-label">
    <span class="cat-hero-sub t" data-fr="{sub_fr}" data-en="{sub_en}">{sub_fr}</span>
    <span class="cat-hero-name t" data-fr="{label_fr}" data-en="{label_en}">{label_fr}</span>
  </div>
</a>'''

def filter_strip(filters, target_sel):
    btns = ''.join(
        f'<button class="filt-btn{" active" if i==0 else ""} t" data-filter="{v}" data-fr="{f}" data-en="{e}">{f}</button>'
        for i,(v,f,e) in enumerate(filters)
    )
    return f'<div class="filter-strip" data-target="{target_sel}">{btns}</div>'

def listing_page_shell(breadcrumbs, title_fr, title_en, subtitle_fr, subtitle_en,
                        hero_cards, filter_btns, products_html):
    bc = breadcrumb(breadcrumbs)
    return f'''<div class="page-hero" style="text-align:left;background:#faf8f5">
  <div style="max-width:1360px;margin:0 auto;padding:0 16px">
    {bc}
    <h1 class="page-title t" data-fr="{title_fr}" data-en="{title_en}">{title_fr}</h1>
    <p class="page-subtitle t" data-fr="{subtitle_fr}" data-en="{subtitle_en}">{subtitle_fr}</p>
  </div>
</div>
<div style="max-width:1360px;margin:0 auto;padding:0 16px 64px;background:#faf8f5">
  <div class="cat-hero" id="cat-hero">{hero_cards}</div>
  {filter_btns}
  <div class="toolbar">
    <span class="toolbar-count" id="prod-count"></span>
    <span class="toolbar-sort t" data-fr="Trier : Popularité ▾" data-en="Sort: Popularity ▾">Trier : Popularité ▾</span>
  </div>
  <div class="prods-grid" id="prod-grid">{products_html}</div>
  <div class="pagination">
    <button class="page-btn active">1</button>
    <button class="page-btn">2</button>
    <button class="page-btn" style="width:auto;padding:0 12px">Suivant →</button>
  </div>
</div>'''

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1: INDEX
# ════════════════════════════════════════════════════════════════════════════
REVIEWS = [
    ('S','Sophie M.','Paris','★★★★★','Beauty of Joseon SPF50+', CX,
     'Honnêtement je cherchais un SPF léger depuis des années. Celui-là je le remets chaque été sans hésiter — aucun film blanc, ça sent rien et ma peau est protégée. Game changer.'),
    ('C','Camille D.','Lyon','★★★★★','COSRX Snail Mucin 96', CX,
     'Je sais ça sonne bizarre mais la bave d\'escargot a littéralement transformé ma peau. En trois semaines mon teint était plus lisse, les petites rougeurs avaient disparu. Je comprends enfin l\'obsession.'),
    ('I','Inès K.','Bordeaux','★★★★★','Glow Recipe Dew Drops', GL,
     'Je le mets le matin sous ma crème et parfois seul les jours où je veux juste avoir l\'air reposée. Mes collègues m\'ont demandé deux fois si j\'avais changé de fond de teint. Non, c\'est juste du niacinamide.'),
    ('A','Amandine T.','Nantes','★★★★☆','Mixsoon Bifida Essence', P1,
     'Peau sensible au point que j\'avais abandonné les actifs. Ce sérum c\'est la première fois que je ne réagis pas mal. Deux mois plus tard ma barrière cutanée s\'est vraiment reconstruite.'),
    ('L','Lucie F.','Strasbourg','★★★★★','SKIN1004 Centella Ampoule', P5,
     'J\'avais les joues rouges en permanence. Après dix jours avec le SKIN1004 c\'est presque plus visible. La formule est ultra clean, zéro parfum, et ça marche vraiment.'),
    ('M','Marie-Laure B.','Toulouse','★★★★★','Beauty of Joseon Relief Sun', P3,
     'J\'ai testé tellement de SPF coréens. Celui-là reste mon préféré depuis un an — texture eau, fini satiné, et il tient sous le maquillage. Je le recommande à tout le monde.'),
    ('J','Julie R.','Bordeaux','★★★★★','Anua Heartleaf 77% Toner', P5,
     'Je suis passée par une phase horrible avec de l\'acné adulte. L\'Anua Heartleaf a vraiment calmé les inflammations. Ma dermato était surprise des résultats, elle me l\'a maintenant recommandé à d\'autres.'),
    ('E','Emma V.','Paris','★★★★★','COSRX Snail Mucin 96', CX,
     'Mon mari l\'a utilisé par curiosité un matin. Maintenant il en commande lui-même. On est toute une famille convertie au snail mucin et on assume complètement.'),
]
rev_slides = ''.join(f'''<div class="rev-slide"><div class="rev-card">
  <div class="rev-stars-top">{stars}</div>
  <p class="rev-text">{quote}</p>
  <div class="rev-footer">
    <div class="rev-avatar">{init}</div>
    <div>
      <p class="rev-name">{name} <span class="rev-city">· {city}</span></p>
      <p class="rev-product">{prod}</p>
    </div>
  </div>
</div></div>''' for init,name,city,stars,prod,_,quote in REVIEWS)

EVENTS_DATA = [
    ('online','Gratuit','Webinaire','10 Mai','14h00','Masterclass : Lire une étiquette INCI','Décryptez les ingrédients derrière les noms scientifiques.', P6),
    ('inperson','45 €','Atelier physique','7 Juin','10h00','Workshop : Construire sa routine K-beauty','Diagnostic individuel + produits fournis. 12 places max.', P4),
    ('online','12 €','Live interactif','24 Mai','15h00','Atelier Glass Skin','Routine complète en direct. Q&A inclus.', P7),
    ('online','15 €','Expert session','21 Juin','16h00','Masterclass : Acides & Actifs','AHA, BHA, niacinamide — comment les associer.', GL),
]
evt_cards = ''.join(f'''<div class="evt-card">
  <div class="evt-img">{imgref(pimg, title)}</div>
  <div class="evt-body">
    <span class="evt-tag {dtype}">{"En ligne" if dtype=="online" else "En présentiel"}</span>
    <h3 class="evt-title">{title}</h3>
    <p class="evt-date">📅 {date} · 🕐 {time}</p>
    <p class="evt-desc">{desc}</p>
    <div class="evt-footer"><span class="evt-price">{price}</span><button class="evt-reserve">Réserver</button></div>
  </div>
</div>''' for dtype,price,tag,date,time,title,desc,pimg in EVENTS_DATA)

BLOG_DATA = [
    ('Tendance','Glass Skin : le secret de la peau coréenne parfaite','12 Avr 2026','Lumineux, velouté, presque translucide — bien plus qu\'une tendance.', P4),
    ('Routine','Double nettoyage : pourquoi c\'est non-négociable','5 Avr 2026','La base de toute routine K-beauty. Huile + mousse = peau nette en profondeur.', P6),
    ('Ingrédients','Centella Asiatica : l\'ingrédient star','28 Mar 2026','Anti-inflammatoire, cicatrisant, apaisant — le Cica expliqué en détail.', P7),
]
blog_cards = ''.join(f'''<div class="blog-card" onclick="window.location='journal.html'">
  <div class="blog-img">{imgref(pimg, title)}</div>
  <p class="blog-tag">{tag}</p>
  <h3 class="blog-title">{title}</h3>
  <p class="blog-excerpt">{excerpt}</p>
  <div class="blog-meta"><span>{date}</span></div>
</div>''' for tag,title,date,excerpt,pimg in BLOG_DATA)

# Viral TikTok videos — real video IDs from most-liked K-beauty content
# Sources: Mikayla Nogueira (258K+ likes), bambidoesbeauty (51K), bewareofpity (82K), BOJ official (39K)
INF_TIKTOKS = [
    {
        'id': '7490607555937422635',  # Mikayla Nogueira - Full face PDRN salmon DNA (258.7K likes)
        'handle': '@mikaylanogueira',
        'product': 'PDRN · ADN de saumon',
        'tag': 'Viral · 258K ♥',
    },
    {
        'id': '7302121489170468128',  # bambidoesbeauty - COSRX snail mucin range (51K likes)
        'handle': '@bambidoesbeauty',
        'product': 'COSRX Snail Mucin',
        'tag': 'Viral · 51K ♥',
    },
    {
        'id': '7393718267111607553',  # bewareofpity - viral Korean toners incl. Anua (82K likes)
        'handle': '@bewareofpity',
        'product': 'Anua Heartleaf Toner',
        'tag': 'Viral · 82K ♥',
    },
    {
        'id': '7556048499373133076',  # beautyofjoseon_official - BOJ starter pack (39.9K likes)
        'handle': '@beautyofjoseon_official',
        'product': 'Beauty of Joseon',
        'tag': 'Viral · 39.9K ♥',
    },
]

def inf_tiktok_card(v):
    # TikTok thumbnail + link card (works everywhere, no CSP issues)
    tt_url = f'https://www.tiktok.com/@{v["handle"].lstrip("@")}/video/{v["id"]}'
    # TikTok oEmbed thumbnail via their CDN pattern
    thumb_url = f'https://www.tiktok.com/api/img/?itemId={v["id"]}&location=0'
    return f'''<a class="inf-video-card" href="{tt_url}" target="_blank" rel="noopener">
  <div class="inf-video-thumb">
    <img src="{thumb_url}" alt="{v["product"]}" loading="lazy"
      onerror="this.parentElement.style.background='rgba(255,255,255,.1)';this.style.display='none'">
    <div class="inf-play-btn">
      <svg viewBox="0 0 24 24" fill="#fff" width="28" height="28"><path d="M8 5v14l11-7z"/></svg>
    </div>
    <div class="inf-tt-badge">
      <svg viewBox="0 0 24 24" fill="#fff" width="14" height="14"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1V9.01a6.34 6.34 0 0 0-.79-.05 6.34 6.34 0 0 0-6.34 6.34 6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.33-6.34V8.68a8.18 8.18 0 0 0 4.77 1.52V6.76a4.85 4.85 0 0 1-1-.07z"/></svg>
      TikTok
    </div>
  </div>
  <div class="inf-video-info">
    <span class="inf-handle">{v["handle"]}</span>
    <p class="inf-video-title">{v["product"]}</p>
    <span class="inf-tag">{v["tag"]}</span>
    <span class="inf-watch-cta">Voir sur TikTok →</span>
  </div>
</a>'''

inf_cards = ''.join(inf_tiktok_card(v) for v in INF_TIKTOKS)

NEW_PROD = [
    (GL,'Glow Recipe','Watermelon Niacinamide Dew Drops','38,00','Nouveau',   ['eclat','serum','glow-recipe','nouveau','niacinamide','pores']),
    (P3,'Beauty of Joseon','Relief Sun Rice + Probiotics SPF50+','18,90','Coup de ♥',['spf','beauty-of-joseon','bestseller','spf50','peau-sensible']),
    (CX,'COSRX','Advanced Snail 96 Mucin Essence','22,50','',                 ['essence','cosrx','snail','hydratation','barriere']),
    (P1,'Mixsoon','Bifida Ferment Essence 100ml','29,00','',                  ['essence','mixsoon','bifida','peau-sensible','barriere']),
    (P5,'SKIN1004','Madagascar Centella Ampoule','21,50','',                  ['serum','skin1004','cica','centella','peau-sensible','anti-rougeurs','barriere']),
    (DR,'IUNIK','Rosehip Vitamin C Serum 15ml','15,90','Nouveau',             ['serum','iunik','vitaminc','eclat','nouveau','hyperpigmentation']),
    (P2,'Mixsoon','Galactomyces Ferment Essence','27,00','',                  ['essence','mixsoon','galactomyces','pores','eclat']),
    (P8,'Huxley','Secret of Sahara Hand Cream','14,90','',                   ['creme','huxley','mains','hydratation']),
    (HA,'Glow Recipe','Banana Soufflé Moisture Cream','35,00','Top noté',     ['creme','glow-recipe','hydratation','anti-age']),
    (P6,'Mixsoon','Bean Essence 100ml','25,00','',                            ['essence','mixsoon','bean','anti-age','rides']),
]
new_cards  = ''.join(prod_card(im,br,nm,pr,bdg,tags) for im,br,nm,pr,bdg,tags in NEW_PROD)
best_cards = ''.join(prod_card(im,br,nm,pr,'',tags)  for im,br,nm,pr,bdg,tags in NEW_PROD[:8])

INDEX_CSS = '.c-slide-bg-1{background:var(--cream)}.c-slide-bg-2{background:#fdf9f5}.c-slide-bg-3{background:#fdf8f2}'

index_body = f'''
<section class="carousel-wrap c-slide-bg-1">
  <button class="c-prev" onclick="moveSlide(-1)">&#8249;</button>
  <button class="c-next" onclick="moveSlide(1)">&#8250;</button>
  <div class="c-slide active c-slide-bg-1">
    <div class="c-slide-img">{imgref(HERO1,"Sonagi Beauty — K-beauty authentique","eager")}</div>
    <div class="c-slide-text">
      <span class="c-tag t" data-fr="Nouveauté · Glow Recipe" data-en="New arrival · Glow Recipe">Nouveauté · Glow Recipe</span>
      <h1 class="c-title t" data-fr="Watermelon<br><em>Glow</em>" data-en="Watermelon<br><em>Glow</em>">Watermelon<br><em>Glow</em></h1>
      <p class="c-sub t" data-fr="Niacinamide 5% · Éclat immédiat · Pores affinés." data-en="Niacinamide 5% · Instant glow · Refined pores.">Niacinamide 5% · Éclat immédiat · Pores affinés.</p>
      <div class="c-btns"><a href="produit.html" class="btn-primary t" data-fr="Découvrir" data-en="Shop now">Découvrir</a><button class="btn-outline t" data-fr="Ma routine" data-en="My routine" onclick="openQuiz()">Ma routine</button></div>
    </div>
  </div>
  <div class="c-slide c-slide-bg-2">
    <div class="c-slide-img">{imgref(HERO2,"Sonagi Beauty — K-beauty coréenne","lazy")}</div>
    <div class="c-slide-text">
      <span class="c-tag t" data-fr="Best-seller · Beauty of Joseon" data-en="Best-seller · Beauty of Joseon">Best-seller · Beauty of Joseon</span>
      <h1 class="c-title t" data-fr="Le SPF<br><em>coréen</em>" data-en="The Korean<br><em>SPF</em>">Le SPF<br><em>coréen</em></h1>
      <p class="c-sub t" data-fr="SPF50+ PA++++ · Texture eau · Riz + Probiotiques." data-en="SPF50+ PA++++ · Water texture · Rice + Probiotics.">SPF50+ PA++++ · Texture eau · Riz + Probiotiques.</p>
      <div class="c-btns"><a href="skincare.html" class="btn-primary t" data-fr="Voir les SPF" data-en="View SPFs">Voir les SPF</a><button class="btn-outline t" data-fr="Ma routine" data-en="My routine" onclick="openQuiz()">Ma routine</button></div>
    </div>
  </div>
  <div class="c-slide c-slide-bg-3">
    <div class="c-slide-img">{imgref(P5,"SKIN1004 Centella","lazy")}</div>
    <div class="c-slide-text">
      <span class="c-tag t" data-fr="Pour peaux sensibles · SKIN1004" data-en="For sensitive skin · SKIN1004">Pour peaux sensibles · SKIN1004</span>
      <h1 class="c-title t" data-fr="Centella<br><em>Apaisante</em>" data-en="Soothing<br><em>Centella</em>">Centella<br><em>Apaisante</em></h1>
      <p class="c-sub t" data-fr="Anti-rougeurs · Réparateur · Certifié vegan." data-en="Anti-redness · Repairing · Certified vegan.">Anti-rougeurs · Réparateur · Certifié vegan.</p>
      <div class="c-btns"><a href="skincare.html" class="btn-primary t" data-fr="Peaux sensibles" data-en="Sensitive skin">Peaux sensibles</a><button class="btn-outline t" data-fr="Ma routine" data-en="My routine" onclick="openQuiz()">Ma routine</button></div>
    </div>
  </div>
  <div class="carousel-dots" style="padding:14px 0"><div id="c-dots" style="display:flex;gap:8px;justify-content:center"></div></div>
</section>
<div class="marquee-wrap" aria-hidden="true"><div class="marquee-inner">
  <span>COSRX <span class="dot">✦</span></span><span>Beauty of Joseon <span class="dot">✦</span></span>
  <span>Mixsoon <span class="dot">✦</span></span><span>SKIN1004 <span class="dot">✦</span></span>
  <span>Glow Recipe <span class="dot">✦</span></span><span>Huxley <span class="dot">✦</span></span>
  <span>IUNIK <span class="dot">✦</span></span><span>Anua <span class="dot">✦</span></span>
  <span>Round Lab <span class="dot">✦</span></span><span>Laneige <span class="dot">✦</span></span>
  <span>COSRX <span class="dot">✦</span></span><span>Beauty of Joseon <span class="dot">✦</span></span>
  <span>Mixsoon <span class="dot">✦</span></span><span>SKIN1004 <span class="dot">✦</span></span>
  <span>Glow Recipe <span class="dot">✦</span></span><span>Huxley <span class="dot">✦</span></span>
  <span>IUNIK <span class="dot">✦</span></span><span>Anua <span class="dot">✦</span></span>
  <span>Round Lab <span class="dot">✦</span></span><span>Laneige <span class="dot">✦</span></span>
</div></div>
<div class="section-wrap" style="background:#faf8f5">
  <div class="section-head">
    <div class="prod-tabs">
      <button class="tab active t" onclick="switchTab(this,'pn')" data-fr="Nouveautés" data-en="New arrivals">Nouveautés</button>
      <button class="tab t" onclick="switchTab(this,'pb')" data-fr="Best-Sellers" data-en="Best-Sellers">Best-Sellers</button>
    </div>
    <a href="skincare.html" class="voir-tout t" data-fr="Voir tout" data-en="View all">Voir tout</a>
  </div>
  <div class="prods-grid" id="pn">{new_cards}</div>
  <div class="prods-grid" id="pb" style="display:none">{best_cards}</div>
</div>
<section class="quiz-banner">
  <h2 class="t" data-fr="Quelle routine pour votre peau ?" data-en="Which routine for your skin?">Quelle routine pour votre peau ?</h2>
  <p class="t" data-fr="4 questions · Protocole sur mesure · Panier prêt." data-en="4 questions · Bespoke protocol · Ready basket.">4 questions · Protocole sur mesure · Panier prêt.</p>
  <button class="btn-primary t" onclick="openQuiz()" data-fr="Commencer le quiz →" data-en="Start the quiz →">Commencer le quiz →</button>
</section>
<section class="brand-belt-section">
  <div class="brand-belt-inner"><span class="lbl t" data-fr="Nos marques" data-en="Our brands">Nos marques</span>
    <h2 style="font-size:32px;color:var(--navy)" class="t" data-fr="K-beauty authentique" data-en="Authentic K-beauty">K-beauty authentique</h2></div>
  <div class="belt-wrap"><div class="brand-belt">
    <span class="brand-logo serif">COSRX</span><span class="brand-logo spaced">BEAUTY OF JOSEON</span>
    <span class="brand-logo">Mixsoon</span><span class="brand-logo spaced">SKIN1004</span>
    <span class="brand-logo serif">Glow Recipe</span><span class="brand-logo spaced">HUXLEY</span>
    <span class="brand-logo">IUNIK</span><span class="brand-logo spaced">ANUA</span>
    <span class="brand-logo">Round Lab</span><span class="brand-logo serif">Laneige</span>
    <span class="brand-logo serif">COSRX</span><span class="brand-logo spaced">BEAUTY OF JOSEON</span>
    <span class="brand-logo">Mixsoon</span><span class="brand-logo spaced">SKIN1004</span>
    <span class="brand-logo serif">Glow Recipe</span><span class="brand-logo spaced">HUXLEY</span>
    <span class="brand-logo">IUNIK</span><span class="brand-logo spaced">ANUA</span>
    <span class="brand-logo">Round Lab</span><span class="brand-logo serif">Laneige</span>
  </div></div>
  <div class="belt-cta"><a href="marques.html" class="btn-marques t" data-fr="Toutes nos marques →" data-en="All our brands →">Toutes nos marques →</a></div>
</section>
<div class="reviews-section" style="background:#faf8f5">
  <div class="rating-row" style="margin-bottom:24px">
    <span class="rating-big">4.9</span>
    <div><div class="rating-stars">★★★★★</div><div class="rating-count t" data-fr="128 avis vérifiés" data-en="128 verified reviews">128 avis vérifiés</div></div>
  </div>
  <div class="rev-carousel"><div class="rev-track" id="rev-track">{rev_slides}</div></div>
</div>
<section class="blog-section"><div class="blog-inner">
  <div class="section-head">
    <span style="font-family:'Cormorant Garamond',serif;font-size:28px;color:var(--navy)" class="t" data-fr="Le journal Sonagi" data-en="The Sonagi Journal">Le journal Sonagi</span>
    <a href="journal.html" class="voir-tout t" data-fr="Tous les articles" data-en="All articles">Tous les articles</a>
  </div>
  <div class="blog-grid">{blog_cards}</div>
</div></section>
<section class="inf-section"><div class="inf-inner">
  <span class="lbl" style="color:var(--border)">Ils parlent de nous</span>
  <h2 style="font-size:30px;color:#fff;margin-bottom:6px" class="t" data-fr="La K-beauty expliquée par des experts" data-en="K-beauty explained by experts">La K-beauty expliquée par des experts</h2>
  <div class="inf-video-grid">{inf_cards}</div>
</div></section>
<section class="events-section"><div class="events-inner">
  <div class="section-head" style="border-bottom:1px solid #d4ccc4">
    <span style="font-family:'Cormorant Garamond',serif;font-size:28px;color:var(--navy)" class="t" data-fr="Masterclasses & Ateliers" data-en="Masterclasses & Workshops">Masterclasses & Ateliers</span>
    <a href="masterclasses.html" class="voir-tout t" data-fr="Toutes les sessions" data-en="All sessions">Toutes les sessions</a>
  </div>
  <div class="evt-grid">{evt_cards}</div>
</div></section>
<section class="insta-section">
  <span class="lbl">@sonagi.beauty</span>
  <h2 style="font-size:28px;color:var(--navy);margin-bottom:6px" class="t" data-fr="Notre communauté" data-en="Our community">Notre communauté</h2>
  <p style="font-size:13px;color:var(--muted);margin-bottom:22px">Partagez votre routine #Sonagi et gagnez 50 points Rewards</p>
  <div class="insta-grid">{''.join(f"<div class='insta-item'>{imgref(k,'Sonagi Beauty')}</div>" for k in [SOC1,SOC2,SOC_STORY,CX,P1,DR])}</div>
</section>
<section class="newsletter" style="background:linear-gradient(rgba(26,39,68,.55),rgba(26,39,68,.55)),url('{imgs[EMAIL_HDR]}') center/cover no-repeat;color:#fff">
  <h2 class="t" data-fr="Rejoignez la communauté" data-en="Join the community" style="color:#fff">Rejoignez la communauté</h2>
  <p class="t" data-fr="Nouveautés, tutoriels K-beauty et offres exclusives réservées à nos abonnés." data-en="New arrivals, K-beauty tutorials and exclusive subscriber offers.">Nouveautés, tutoriels K-beauty et offres exclusives réservées à nos abonnés.</p>
  <div class="email-form"><input type="email" placeholder="Votre email" data-fr="Votre email" data-en="Your email"><button class="t" data-fr="S'inscrire" data-en="Subscribe">S'inscrire</button></div>
</section>
<section class="points-section"><div class="points-inner">
  <div style="text-align:center;margin-bottom:8px">
    <span class="lbl" style="color:var(--border)">Sonagi Rewards</span>
    <h2 style="font-size:32px;color:#fff" class="t" data-fr="Chaque achat vous récompense" data-en="Every purchase rewards you">Chaque achat vous récompense</h2>
  </div>
  <div class="pts-grid">
    <div class="pt-card"><div class="pt-icon">🛒</div><div class="pt-title">1 pt / €</div><div class="pt-desc">Chaque euro dépensé en boutique</div><span class="pt-pts">automatique</span></div>
    <div class="pt-card"><div class="pt-icon">📱</div><div class="pt-title">+50 pts</div><div class="pt-desc">Post TikTok ou Instagram avec #Sonagi</div><span class="pt-pts">par post</span></div>
    <div class="pt-card"><div class="pt-icon">👥</div><div class="pt-title">+100 pts</div><div class="pt-desc">Par ami parrainé dès son premier achat</div><span class="pt-pts">par parrainage</span></div>
    <div class="pt-card"><div class="pt-icon">⭐</div><div class="pt-title">+25 pts</div><div class="pt-desc">Par avis produit publié avec photo</div><span class="pt-pts">par avis</span></div>
  </div>
  <div style="text-align:center;margin-top:32px">
    <a href="rewards.html" class="btn-primary" style="background:var(--peach);color:var(--navy)">Découvrir Sonagi Rewards →</a>
  </div>
</div></section>
'''

with open(f'{_out}/index.html','w',encoding='utf-8') as f:
    f.write(page('Sonagi Beauty — K-beauty authentique', index_body, extra_css=INDEX_CSS))
print(f"✓ index.html — {os.path.getsize(f'{_out}/index.html')/1024:.0f} KB")

# ════════════════════════════════════════════════════════════════════════════
# PAGES 2-4: LISTING PAGES with comprehensive tags
# ════════════════════════════════════════════════════════════════════════════

# ── SKINCARE ─────────────────────────────────────────────────────────────────
SK_PRODS = [
    (P3,'Beauty of Joseon','Relief Sun Rice + Probiotics SPF50+','18,90','Coup de ♥',
     ['spf','beauty-of-joseon','bestseller','spf50','peau-sensible','peau-normale','peau-mixte']),
    (CX,'COSRX','Advanced Snail 96 Mucin Essence','22,50','',
     ['essence','cosrx','snail','hydratation','barriere','peau-seche','peau-sensible']),
    (GL,'Glow Recipe','Watermelon Niacinamide Dew Drops','38,00','Nouveau',
     ['serum','glow-recipe','niacinamide','eclat','nouveau','pores','peau-grasse','peau-mixte']),
    (P1,'Mixsoon','Bifida Ferment Essence 100ml','29,00','',
     ['essence','mixsoon','bifida','peau-sensible','barriere','hydratation']),
    (P5,'SKIN1004','Madagascar Centella Ampoule','21,50','',
     ['serum','skin1004','cica','centella','peau-sensible','anti-rougeurs','barriere','acne']),
    (DR,'IUNIK','Rosehip Vitamin C Serum 15ml','15,90','Nouveau',
     ['serum','iunik','vitaminc','eclat','nouveau','hyperpigmentation','peau-terne']),
    (P2,'Mixsoon','Galactomyces Ferment Essence','27,00','',
     ['essence','mixsoon','galactomyces','pores','eclat','peau-grasse','peau-mixte']),
    (P8,'Huxley','Secret of Sahara Hand Cream','14,90','',
     ['creme','huxley','mains','hydratation','peau-seche']),
    (HA,'Glow Recipe','Banana Soufflé Moisture Cream 50ml','35,00','Top noté',
     ['creme','glow-recipe','hydratation','anti-age','rides','peau-seche','peau-normale']),
    (P6,'Mixsoon','Bean Essence 100ml','25,00','',
     ['essence','mixsoon','bean','anti-age','rides','elasticite']),
    (P4,'SKIN1004','Centella Water-Fit Sun SPF50+','19,90','',
     ['spf','skin1004','cica','centella','spf50','peau-sensible','peau-grasse']),
    (P7,'Mixsoon','Reishi Mushroom Essence 100ml','27,00','',
     ['essence','mixsoon','mushroom','anti-age','rides','elasticite','peau-seche']),
]
sk_hero = ''.join(cat_hero_card(img,fr,en,link=f'skincare.html?cat={tag}') for img,fr,en,tag in [
    (CAT_SPF,'Crème Solaire','Sun care','spf'),
    (CAT_SERUM,'Sérums & Essences','Serums','serum'),
    (CAT_CLEAN,'Nettoyants','Cleansers','creme'),
    (P5,'Peaux sensibles','Sensitive','peau-sensible'),
])
sk_filters = filter_strip([
    ('all','Tout','All'),
    ('spf','Crème solaire','Sun care'),
    ('serum','Sérums','Serums'),
    ('essence','Essences','Essences'),
    ('creme','Crèmes','Moisturisers'),
    ('peau-sensible','Peau sensible','Sensitive'),
    ('peau-grasse','Peau grasse','Oily'),
    ('peau-seche','Peau sèche','Dry'),
    ('hydratation','Hydratation','Hydration'),
    ('eclat','Éclat','Brightening'),
    ('anti-age','Anti-âge','Anti-age'),
    ('acne','Acné','Acne'),
    ('pores','Pores','Pores'),
    ('anti-rougeurs','Rougeurs','Redness'),
], '#prod-grid')
sk_prods_html = ''.join(prod_card(im,br,nm,pr,bdg,tags) for im,br,nm,pr,bdg,tags in SK_PRODS)
sk_body = listing_page_shell(
    [('Accueil','Home','index.html'),('Skincare','Skincare',None)],
    'Skincare','Skincare',
    'Produits authentiques importés de Corée du Sud',
    'Authentic products imported from South Korea',
    sk_hero, sk_filters, sk_prods_html
)
with open(f'{_out}/skincare.html','w',encoding='utf-8') as f:
    f.write(page('Skincare', sk_body, 'Skincare'))
print(f"✓ skincare.html — {os.path.getsize(f'{_out}/skincare.html')/1024:.0f} KB")

# ── MAQUILLAGE ───────────────────────────────────────────────────────────────
MQ_PRODS = [
    (P3,'Beauty of Joseon','Glaze Lip Balm — Rose Hip','12,90','Nouveau',
     ['levres','baume-levres','beauty-of-joseon','soin','nouveau','teinte-nude']),
    (GL,'Glow Recipe','Watermelon Glow Lip Pop','16,90','',
     ['levres','gloss','glow-recipe','brillant','teinte-nude','soin']),
    (P5,'Rom&nd','Blur Fudge Tint — Beet Red','14,50','Top noté',
     ['levres','tint','romand','teinte-rouge','longue-tenue']),
    (CX,'Peripera','Ink Velvet Tint 02','11,90','',
     ['levres','tint','peripera','velours','longue-tenue']),
    (DR,'CLIO','Waterproof Pen Liner — Black','13,90','',
     ['yeux','liner','clio','waterproof','longue-tenue']),
    (P1,'Etude House','Play Color Eyes Palette — Hanami','22,00','Coup de ♥',
     ['yeux','fard','etude-house','palette','coup-de-coeur']),
    (P2,'Innisfree','No-Sebum Mineral Powder 5g','9,90','',
     ['teint','poudre','innisfree','mat','pores']),
    (P4,'Heimish','Dailism Blush — Peach Fog','15,90','Nouveau',
     ['joues','blush','heimish','nouveau']),
    (P6,'Beauty of Joseon','Red Bean Refreshing Pore Mask','14,90','',
     ['teint','masque','beauty-of-joseon','pores','demaquillant']),
    (P7,'Laneige','Lip Sleeping Mask — Berry','22,90','Best-seller',
     ['levres','baume-levres','laneige','soin','nuit','bestseller']),
    (P8,'Romand','Han All Shadow — Dusty Rose','16,50','',
     ['yeux','fard','romand','palette']),
    (HA,'Missha','M Signature Real Complete BB Cream SPF25','18,90','',
     ['teint','cushion','missha','bb-creme','spf','couvrance']),
]
mq_hero = ''.join(cat_hero_card(img,fr,en,link=f'maquillage.html?cat={tag}') for img,fr,en,tag in [
    (CAT_LIP,'Lèvres','Lips','levres'),
    (GL,'Teint','Foundation','teint'),
    (CAT_EYE,'Yeux','Eyes','yeux'),
    (P5,'Joues','Cheeks','joues'),
])
mq_filters = filter_strip([
    ('all','Tout','All'),
    ('levres','Lèvres','Lips'),
    ('yeux','Yeux','Eyes'),
    ('teint','Teint','Foundation'),
    ('joues','Joues','Cheeks'),
    ('tint','Tints','Tints'),
    ('fard','Fards à paupières','Eye shadow'),
    ('longue-tenue','Longue tenue','Long-wear'),
    ('waterproof','Waterproof','Waterproof'),
    ('soin','Soin-maquillage','Skincare-makeup'),
    ('demaquillant','Démaquillant','Cleanser'),
], '#prod-grid')
mq_prods_html = ''.join(prod_card(im,br,nm,pr,bdg,tags) for im,br,nm,pr,bdg,tags in MQ_PRODS)
mq_body = listing_page_shell(
    [('Accueil','Home','index.html'),('Maquillage','Makeup',None)],
    'Maquillage','Makeup',
    'Teintes délicates, formules soin-maquillage, textures innovantes',
    'Delicate shades, skincare-makeup formulas, innovative textures',
    mq_hero, mq_filters, mq_prods_html
)
with open(f'{_out}/maquillage.html','w',encoding='utf-8') as f:
    f.write(page('Maquillage coréen', mq_body, 'Maquillage'))
print(f"✓ maquillage.html — {os.path.getsize(f'{_out}/maquillage.html')/1024:.0f} KB")

# ── HAIRCARE ─────────────────────────────────────────────────────────────────
HC_PRODS = [
    (P6,"La'dor","Argan Oil Shampoo 530ml",'19,90','Best-seller',
     ['shampooing','lador','argan','cheveux-secs','bestseller','nutrition']),
    (P7,'Mise En Scene','Perfect Serum Original 80ml','16,90','',
     ['serum','mise-en-scene','lissant','brillance','frisottis']),
    (CX,'Masil','8 Seconds Salon Hair Mask 200ml','22,50','Coup de ♥',
     ['masque','masil','nutrition','coup-de-coeur','cheveux-abimes','reparation']),
    (P1,'Derma Factory','Scalp Clinic Shampoo 300ml','24,90','Nouveau',
     ['shampooing','derma-factory','cuir-chevelu','nouveau','pellicules']),
    (GL,"La'dor","Tea Tree Scalp Hair Pack",'18,90','',
     ['masque','lador','cuir-chevelu','purifiant','pellicules']),
    (P3,'Masil','3 Salon CMC Shampoo 300ml','19,50','',
     ['shampooing','masil','reparation','cheveux-abimes','couleur']),
    (DR,'Mise En Scene','Perfect Repair Treatment 200ml','15,90','',
     ['masque','mise-en-scene','reparation','cheveux-abimes','pointes']),
    (P2,"La'dor","Hydro LPP Treatment 150ml",'20,90','Top noté',
     ['masque','lador','hydratation','nutrition','cheveux-secs']),
    (P4,'Masil','6 Lactobacillus Hair Perfume Ampoule','16,50','Nouveau',
     ['serum','masil','probiotiques','nouveau','brillance','parfum']),
    (P8,'Esthetic House','CP-1 Protein Treatment 250ml','28,90','',
     ['masque','esthetic-house','proteine','reparation','cheveux-abimes','pointes']),
    (HA,"La'dor","Keratin LPP Shampoo 530ml",'19,90','',
     ['shampooing','lador','keratine','lissant','frisottis']),
    (P5,'Masil','5 Probiotics Sealing Ampoule 15ml x8','21,90','',
     ['serum','masil','probiotiques','brillance','protection-thermique']),
]
hc_hero = ''.join(cat_hero_card(img,fr,en,link=f'haircare.html?cat={tag}') for img,fr,en,tag in [
    (P6,'Shampooings','Shampoos','shampooing'),
    (CAT_MASK,'Masques & Soins','Masks','masque'),
    (P7,'Sérums capillaires','Hair serums','serum'),
    (GL,'Cuir chevelu','Scalp','cuir-chevelu'),
])
hc_filters = filter_strip([
    ('all','Tout','All'),
    ('shampooing','Shampooings','Shampoos'),
    ('masque','Masques & Soins','Masks'),
    ('serum','Sérums','Serums'),
    ('cuir-chevelu','Cuir chevelu','Scalp'),
    ('cheveux-abimes','Cheveux abîmés','Damaged'),
    ('cheveux-secs','Cheveux secs','Dry hair'),
    ('lissant','Lissant','Smoothing'),
    ('nutrition','Nutrition','Nourishing'),
    ('reparation','Réparation','Repair'),
    ('brillance','Brillance','Shine'),
    ('pellicules','Pellicules','Dandruff'),
], '#prod-grid')
hc_prods_html = ''.join(prod_card(im,br,nm,pr,bdg,tags) for im,br,nm,pr,bdg,tags in HC_PRODS)
hc_body = listing_page_shell(
    [('Accueil','Home','index.html'),('Cheveux & Corps','Hair & Body',None)],
    'Cheveux & Corps','Hair & Body',
    'Soins capillaires coréens de salon — shampooings, masques, sérums',
    'Korean salon-quality hair care — shampoos, masks, serums',
    hc_hero, hc_filters, hc_prods_html
)
with open(f'{_out}/haircare.html','w',encoding='utf-8') as f:
    f.write(page('Cheveux & Corps', hc_body, 'Cheveux & Corps'))
print(f"✓ haircare.html — {os.path.getsize(f'{_out}/haircare.html')/1024:.0f} KB")

# ════════════════════════════════════════════════════════════════════════════
# PAGES 5-12: Produit, Panier, Marques, Journal, Masterclasses, Compte, Rewards, Confirmation
# ════════════════════════════════════════════════════════════════════════════

# ── PRODUIT ──────────────────────────────────────────────────────────────────
PROD_CSS = """
.prod-page{max-width:1360px;margin:0 auto;padding:24px 16px 64px}
.prod-layout{display:flex;flex-direction:column;gap:32px}
.prod-main-img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;border:1px solid var(--border);background:#fff;display:block}
.prod-thumbs{display:flex;gap:8px;margin-top:10px;overflow-x:auto;padding-bottom:4px}
.prod-thumb{width:68px;height:68px;flex-shrink:0;object-fit:cover;border-radius:6px;border:1.5px solid var(--border);cursor:pointer;transition:border-color .2s}
.prod-thumb.active{border-color:var(--navy)}
.prod-brand-tag{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.prod-name-full{font-size:28px;color:var(--navy);margin-bottom:12px;line-height:1.2}
.prod-stars{font-size:13px;color:var(--gold);margin-bottom:4px}
.prod-review-count{font-size:11px;color:var(--muted);margin-bottom:16px}
.prod-price-lg{font-size:30px;font-family:'Cormorant Garamond',serif;color:var(--navy);margin-bottom:16px}
.prod-pts-note{background:var(--peach-l);border:1px solid var(--peach);padding:9px 14px;font-size:11px;color:var(--navy);margin-bottom:18px;display:flex;align-items:center;gap:6px}
.prod-sizes{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
.size-btn{border:1px solid var(--border);padding:8px 18px;font-size:12px;background:#fff;transition:all .2s}
.size-btn.active,.size-btn:hover{border-color:var(--navy);color:var(--navy)}
.prod-add-main{width:100%;background:var(--navy);color:#fff;border:none;padding:16px;font-size:11px;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:10px}
.prod-quiz-cta{width:100%;background:var(--peach-l);color:var(--navy);border:1px solid var(--peach);padding:14px;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:24px}
.prod-tabs-bar{display:flex;gap:0;border-bottom:1px solid var(--border);margin-bottom:18px}
.prod-tab{padding:10px 0;margin-right:24px;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--muted);background:none;border:none;border-bottom:2px solid transparent;transition:all .2s}
.prod-tab.active{color:var(--navy);border-bottom-color:var(--navy)}
.prod-tab-pane{display:none;font-size:13px;line-height:1.8;color:var(--muted)}
.prod-tab-pane.active{display:block}
.ingr-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.ingr-tag{background:#f3eeea;padding:3px 9px;font-size:10px;letter-spacing:1px;color:var(--navy)}
.how-step{display:flex;gap:12px;align-items:flex-start;margin-bottom:12px}
.how-num{width:24px;height:24px;background:var(--navy);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:600;flex-shrink:0;margin-top:2px}
.related-section{padding:48px 16px;border-top:1px solid var(--border);max-width:1360px;margin:0 auto}
@media(min-width:768px){.prod-layout{flex-direction:row;gap:48px}.prod-gallery{width:50%;flex-shrink:0}.prod-main-img{aspect-ratio:4/5}.prod-name-full{font-size:36px}.prod-page{padding:40px 40px 80px}.related-section{padding:48px 40px}}
"""
def prod_card_s(imgkey,brand,name,price):
    return f'<div class="prod-card"><div class="prod-img-wrap">{imgref(imgkey,name)}<button class="prod-add-btn t" data-fr="Ajouter au panier" data-en="Add to basket">Ajouter au panier</button></div><p class="prod-brand">{brand}</p><p class="prod-name">{name}</p><p class="prod-price">{price} €</p></div>'

prod_body = f'''<div class="prod-page">
  {breadcrumb([('Accueil','Home','index.html'),('Skincare','Skincare','skincare.html'),('Sérums','Serums',None)])}
  <div class="prod-layout">
    <div class="prod-gallery">
      <img class="prod-main-img" id="main-img" src="" data-imgkey="GL" alt="Watermelon Glow Niacinamide Dew Drops" loading="eager">
      <div class="prod-thumbs">
        <img class="prod-thumb active" src="" data-imgkey="GL" onclick="setMainImg(this)" alt="">
        <img class="prod-thumb" src="" data-imgkey="P4" onclick="setMainImg(this)" alt="">
        <img class="prod-thumb" src="" data-imgkey="DR" onclick="setMainImg(this)" alt="">
        <img class="prod-thumb" src="" data-imgkey="P5" onclick="setMainImg(this)" alt="">
      </div>
    </div>
    <div>
      <p class="prod-brand-tag">Glow Recipe</p>
      <h1 class="prod-name-full">Watermelon Glow Niacinamide Dew Drops 30ml</h1>
      <div class="prod-stars">★★★★★</div>
      <p class="prod-review-count">4.9 · 128 avis</p>
      <p class="prod-price-lg">38,00 €</p>
      <div class="prod-pts-note">★ Gagnez 38 points Sonagi Rewards avec cet achat</div>
      <div class="prod-sizes"><button class="size-btn active">30ml</button><button class="size-btn">50ml</button></div>
      <button class="prod-add-main">Ajouter au panier</button>
      <button class="prod-quiz-cta" onclick="openQuiz()">✦ Ce produit est-il fait pour ma peau ? → Faire le quiz</button>
      <div class="prod-tabs-bar">
        <button class="prod-tab active" onclick="switchProdTab(this,'desc')">Description</button>
        <button class="prod-tab" onclick="switchProdTab(this,'ingr')">Ingrédients</button>
        <button class="prod-tab" onclick="switchProdTab(this,'how')">Comment utiliser</button>
      </div>
      <div class="prod-tab-pane active" id="ptab-desc"><p>Sérum multi-usage : niacinamide 5% unifie le teint, resserre les pores et illumine. Acide hyaluronique et extrait de pastèque hydratent en profondeur.</p></div>
      <div class="prod-tab-pane" id="ptab-ingr"><div class="ingr-tags"><span class="ingr-tag">Niacinamide 5%</span><span class="ingr-tag">Acide hyaluronique</span><span class="ingr-tag">Extrait de pastèque</span><span class="ingr-tag">Panthenol</span><span class="ingr-tag">Centella Asiatica</span></div></div>
      <div class="prod-tab-pane" id="ptab-how">
        <div class="how-step"><div class="how-num">1</div><p>Appliquer sur peau propre et sèche, matin et/ou soir.</p></div>
        <div class="how-step"><div class="how-num">2</div><p>Tapoter délicatement quelques gouttes sur l'ensemble du visage.</p></div>
        <div class="how-step"><div class="how-num">3</div><p>Laisser pénétrer, puis appliquer votre crème et SPF.</p></div>
      </div>
    </div>
  </div>
</div>
<div class="related-section">
  <h2 style="font-size:26px;color:var(--navy);margin-bottom:22px">Vous pourriez aussi aimer</h2>
  <div class="prods-grid">
    {prod_card_s(P3,'Beauty of Joseon','Relief Sun Rice + Probiotics SPF50+','18,90')}
    {prod_card_s(CX,'COSRX','Advanced Snail 96 Mucin Essence','22,50')}
    {prod_card_s(P1,'Mixsoon','Bifida Ferment Essence 100ml','29,00')}
    {prod_card_s(P5,'SKIN1004','Madagascar Centella Ampoule','21,50')}
  </div>
</div>'''
with open(f'{_out}/produit.html','w',encoding='utf-8') as f:
    f.write(page('Watermelon Glow Niacinamide Dew Drops', prod_body, extra_css=PROD_CSS))
print(f"✓ produit.html — {os.path.getsize(f'{_out}/produit.html')/1024:.0f} KB")

# ── PANIER ───────────────────────────────────────────────────────────────────
PANIER_CSS = """
.checkout-wrap{max-width:1200px;margin:0 auto;padding:32px 16px 80px;display:flex;flex-direction:column;gap:24px}
.cart-item-row{display:flex;gap:14px;padding:16px 0;border-bottom:1px solid var(--border);align-items:flex-start}
.cart-item-img{width:80px;height:80px;object-fit:cover;border-radius:6px;border:1px solid var(--border);flex-shrink:0}
.cart-item-body{flex:1;min-width:0}
.ci-brand{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}
.ci-name{font-size:13px;color:var(--text);margin:3px 0;line-height:1.4}
.ci-price{font-size:14px;color:var(--navy);font-weight:500}
.qty-ctrl{display:flex;align-items:center;border:1px solid var(--border);width:fit-content;margin-top:8px}
.qty-btn{width:30px;height:30px;background:none;border:none;font-size:16px;color:var(--navy)}
.qty-val{width:36px;text-align:center;font-size:13px;border-left:1px solid var(--border);border-right:1px solid var(--border);height:30px;line-height:30px}
.order-summary{background:#fff;border:1px solid var(--border);padding:24px;position:sticky;top:80px}
.summary-row{display:flex;justify-content:space-between;padding:8px 0;font-size:13px;color:var(--muted)}
.summary-row.total{border-top:1px solid var(--border);padding-top:14px;margin-top:6px;font-size:16px;color:var(--navy);font-weight:500}
.promo-wrap{display:flex;border:1px solid var(--border);overflow:hidden;margin:16px 0}
.promo-wrap input{flex:1;border:none;padding:10px 14px;font-size:12px;font-family:'DM Sans',sans-serif;outline:none;background:var(--cream);min-width:0}
.promo-wrap button{background:var(--navy);color:#fff;border:none;padding:10px 14px;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;flex-shrink:0}
.checkout-btn{width:100%;background:var(--navy);color:#fff;border:none;padding:16px;font-size:11px;letter-spacing:2.5px;text-transform:uppercase;margin-top:12px}
.ship-option{display:flex;align-items:center;gap:10px;border:1px solid var(--border);padding:12px 14px;margin-bottom:8px;font-size:12px;cursor:pointer}
.ship-option.sel{border-color:var(--navy)}
.pay-section{background:var(--cream);border:1px solid var(--border);padding:18px;margin-top:20px}
.pay-btn{border:1.5px solid var(--border);padding:7px 14px;font-size:11px;display:flex;align-items:center;gap:6px;background:#fff;transition:all .2s}
.pay-btn.active{border-color:var(--navy);color:var(--navy)}
.pay-methods{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.card-field{border:1px solid var(--border);padding:11px 14px;background:#fff;margin-bottom:8px;font-size:13px;color:var(--muted);display:flex;align-items:center;gap:8px}
.card-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.form-row{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:10px}
.form-grp{display:flex;flex-direction:column;gap:4px;width:100%}
.form-lbl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}
.form-inp{border:1px solid var(--border);padding:10px 14px;font-size:13px;font-family:'DM Sans',sans-serif;outline:none;background:#fff;width:100%;box-sizing:border-box}
.form-inp:focus{border-color:var(--navy)}
@media(min-width:768px){.checkout-wrap{flex-direction:row;align-items:flex-start;padding:40px 40px 80px}.checkout-main{flex:1;min-width:0}.checkout-aside{width:340px;flex-shrink:0}.form-row{grid-template-columns:1fr 1fr}}
"""
panier_body = f'''<div class="checkout-wrap">
  <div class="checkout-main">
    <h1 class="page-title">Mon panier</h1>
    <h2 style="font-size:18px;color:var(--navy);margin-bottom:16px">Articles (3)</h2>
    {''.join(f"""<div class="cart-item-row">
      <img class="cart-item-img" src="" data-imgkey="{ik}" alt="{brand}">
      <div class="cart-item-body"><p class="ci-brand">{brand}</p><p class="ci-name">{name}</p>
        <div class="qty-ctrl"><button class="qty-btn">−</button><span class="qty-val">1</span><button class="qty-btn">+</button></div>
        <p class="ci-price" style="margin-top:6px">{price} €</p></div>
      <button style="background:none;border:none;color:var(--muted);font-size:20px;line-height:1">×</button>
    </div>""" for ik,brand,name,price in [('GL','Glow Recipe','Watermelon Glow Niacinamide Dew Drops 30ml','38,00'),('P3','Beauty of Joseon','Relief Sun Rice + Probiotics SPF50+','18,90'),('CX','COSRX','Advanced Snail 96 Mucin Power Essence 100ml','22,50')])}
    <div style="background:var(--peach-l);border:1px solid var(--peach);padding:12px 14px;margin-top:14px;font-size:11px;color:var(--navy)">★ Vous allez gagner 79 points Sonagi Rewards avec cette commande</div>
    <div style="margin-top:32px;padding-top:28px;border-top:1px solid var(--border)">
      <h3 style="font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--navy);margin-bottom:16px">Coordonnées</h3>
      <div class="form-row"><div class="form-grp"><label class="form-lbl">Prénom</label><input class="form-inp" type="text" placeholder="Marie"></div><div class="form-grp"><label class="form-lbl">Nom</label><input class="form-inp" type="text" placeholder="Dupont"></div></div>
      <div class="form-row"><div class="form-grp"><label class="form-lbl">Email</label><input class="form-inp" type="email" placeholder="marie@exemple.fr"></div></div>
      <h3 style="font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--navy);margin:20px 0 14px">Livraison</h3>
      <div class="form-row"><div class="form-grp"><label class="form-lbl">Adresse</label><input class="form-inp" type="text" placeholder="12 rue de la Paix"></div></div>
      <div class="form-row"><div class="form-grp"><label class="form-lbl">Code postal</label><input class="form-inp" type="text" placeholder="75001"></div><div class="form-grp"><label class="form-lbl">Ville</label><input class="form-inp" type="text" placeholder="Paris"></div></div>
      <label class="ship-option sel"><input type="radio" name="ship" checked> Colissimo 2–3 jours <span style="margin-left:auto">Offert dès 50€</span></label>
      <label class="ship-option"><input type="radio" name="ship"> Chronopost 24h <span style="margin-left:auto">7,90 €</span></label>
      <label class="ship-option"><input type="radio" name="ship"> Point Relais Mondial Relay <span style="margin-left:auto">4,90 €</span></label>
      <div class="pay-section">
        <h3 style="font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--navy);margin-bottom:14px">Paiement sécurisé</h3>
        <div class="pay-methods"><button class="pay-btn active">💳 Carte</button><button class="pay-btn">PayPal</button><button class="pay-btn">Apple Pay</button></div>
        <div class="card-field"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg> Numéro de carte</div>
        <div class="card-grid"><div class="card-field">MM / AA</div><div class="card-field">CVC</div></div>
        <div style="font-size:10px;color:var(--muted);display:flex;align-items:center;gap:6px;margin-top:6px">🔒 Paiement sécurisé via Stripe · Données chiffrées</div>
      </div>
      <button class="checkout-btn" onclick="window.location='confirmation.html'">Confirmer ma commande → 79,40 €</button>
    </div>
  </div>
  <div class="checkout-aside">
    <div class="order-summary">
      <h2 style="font-size:18px;color:var(--navy);margin-bottom:14px">Récapitulatif</h2>
      <div class="summary-row"><span>Sous-total (3 articles)</span><span>79,40 €</span></div>
      <div class="summary-row"><span>Livraison</span><span style="color:var(--navy)">Offerte</span></div>
      <div class="summary-row"><span>Points gagnés</span><span style="color:var(--peach)">+79 pts</span></div>
      <div class="promo-wrap"><input type="text" placeholder="Code promo"><button>Appliquer</button></div>
      <div class="summary-row total"><span>Total TTC</span><span style="font-family:'Cormorant Garamond',serif;font-size:22px">79,40 €</span></div>
    </div>
  </div>
</div>'''
with open(f'{_out}/panier.html','w',encoding='utf-8') as f:
    f.write(page('Mon panier', panier_body, extra_css=PANIER_CSS))
print(f"✓ panier.html — {os.path.getsize(f'{_out}/panier.html')/1024:.0f} KB")

# ── MARQUES ──────────────────────────────────────────────────────────────────
BRAND_LIST = sorted(["A'pieu","Abib","ACROPASS","Acwell","Aestura","Anua","APLB","Aprilskin","Aromatica","Axis-Y","B.Lab","Banila Co","Beauty of Joseon","Benton","Beplain","Biodance","Celimax","Centellian24","CLIO","CNP","COSRX","D'alba","Dasique","Derma:B","Dr. Ceuracle","Dr. Althea","Dr.G","Elizavecca","Etude House","Frudia","FWEE","Glow Recipe","Huxley","IUNIK","Isntree","Klairs","La'dor","Laneige","Masil","Medicube","Mise En Scene","Mixsoon","NACIFIC","Numbuzin","Peripera","Petitfée","Pyunkang Yul","Rom&nd","Round Lab","SKIN1004","Some By Mi","Tirtir","TonyMoly","VT Cosmetics"])
by_letter = defaultdict(list)
for b in BRAND_LIST: by_letter[b[0].upper()].append(b)
alpha_nav = ''.join(f'<a href="#L{l}" style="font-size:13px;color:#615050;padding:4px 6px;text-decoration:none">{l}</a>' if l in by_letter else f'<span style="font-size:13px;color:#c8cdd6;padding:4px 6px">{l}</span>' for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
def _brand_row(l):
    links = ''.join('<a href="skincare.html" class="brand-name" style="display:block;width:50%;padding:5px 0;font-family:Cormorant Garamond,serif;font-size:18px;color:#615050;text-decoration:none">' + b + '</a>' for b in sorted(by_letter[l]))
    return '<div style="display:flex;border-top:1px solid var(--border);padding:16px 0"><span id="L' + l + '" style="font-family:\'Cormorant Garamond\',serif;font-size:20px;color:#c8cdd6;width:44px;flex-shrink:0">' + l + '</span><div style="flex:1;display:flex;flex-wrap:wrap">' + links + '</div></div>'
brand_rows = ''.join(_brand_row(l) for l in sorted(by_letter.keys()))
MARQUES_CSS = '.brands-hero{text-align:center;padding:52px 20px 40px}.brands-hero h1{font-family:"Cormorant Garamond",serif;font-size:60px;font-weight:300;color:var(--navy);margin-bottom:28px}.brand-search-pill{display:flex;align-items:center;gap:10px;border:1.5px solid var(--border);border-radius:40px;padding:12px 20px;background:#fff;max-width:520px;margin:0 auto 16px}.brand-search-pill input{flex:1;border:none;outline:none;font-size:14px;background:transparent}.alpha-nav{display:flex;flex-wrap:wrap;justify-content:center;gap:2px;max-width:600px;margin:0 auto 8px}.brand-name:hover{color:var(--navy)!important}.feat-brands{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;max-width:800px;margin:0 auto 48px;padding:0 20px}.feat-brand{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid var(--border);border-radius:12px;padding:16px 20px;text-decoration:none;transition:transform .2s,box-shadow .2s}.feat-brand:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(26,39,68,.08)}.feat-brand img{width:48px;height:48px;object-fit:contain}.feat-brand span{font-family:"Cormorant Garamond",serif;font-size:20px;color:var(--navy)}@media(min-width:768px){.brands-hero h1{font-size:80px}.brand-name{width:25%!important;font-size:20px!important}.feat-brands{grid-template-columns:repeat(4,1fr)}}'
_feat_brands = ''.join(f'<a href="skincare.html" class="feat-brand">{imgref(img,name)}<span>{name}</span></a>' for img,name in [
    (BR_COSRX,'COSRX'),(BR_BOJ,'Beauty of Joseon'),(BR_SBMI,'Some By Mi'),(BR_ANUA,'Anua'),(BR_LAN,'Laneige'),(BR_INN,'Innisfree'),
])
marques_body = f'<div class="brands-hero"><h1>Marques</h1><div class="brand-search-pill"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--muted)" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg><input type="text" placeholder="Rechercher une marque…" oninput="filterBrands(this.value)"></div><p style="font-size:12px;color:var(--muted);margin-bottom:16px">{len(BRAND_LIST)} marques</p><nav class="alpha-nav">{alpha_nav}</nav></div><div class="feat-brands">{_feat_brands}</div><div style="max-width:1200px;margin:0 auto;padding:0 20px 80px">{brand_rows}</div>'
with open(f'{_out}/marques.html','w',encoding='utf-8') as f:
    f.write(page('Toutes nos marques', marques_body, 'Marques', MARQUES_CSS))
print(f"✓ marques.html — {os.path.getsize(f'{_out}/marques.html')/1024:.0f} KB")

# ── JOURNAL ───────────────────────────────────────────────────────────────────
ARTICLES = [
    ('tendance','Tendance','Glass Skin : le secret de la peau coréenne parfaite','12 Avr 2026','@hyram',BL_GLASS,'Lumineux, velouté, presque translucide — bien plus qu\'une tendance.'),
    ('routine','Routine','Double nettoyage : pourquoi c\'est non-négociable','5 Avr 2026','@gothamista',BL_DOUBLE,'La base de toute routine K-beauty. Huile + mousse = peau nette en profondeur.'),
    ('ingredients','Ingrédients','Hanbang : les ingrédients ancestraux coréens','28 Mar 2026','@jameswelshskin',BL_HANBANG,'Ginseng, centella, thé vert — les secrets de la pharmacopée coréenne.'),
    ('spf','SPF','SPF en K-beauty : guide complet','18 Mar 2026','@hyram',BL_SPF,'Pas de glass skin sans protection solaire. Les SPF coréens qui changent tout.'),
    ('actifs','Actifs','Acids en K-beauty : AHA, BHA, PHA décryptés','10 Mar 2026','@gothamista',BL_ACIDS,'Les exfoliants chimiques coréens. Comment les intégrer sans irriter.'),
    ('guides','Guide','Décoder les étiquettes INCI en 5 minutes','1 Mar 2026','@labmuffin',CX,'Vous voyez des noms scientifiques incompréhensibles ? Ce guide change tout.'),
    ('routine','Routine','La routine 10 étapes : mythe ou réalité ?','20 Fév 2026','@hyram',BL_ROUTINE,'Faut-il vraiment 10 étapes ? Décryptage et version simplifiée.'),
    ('ingredients','Ingrédients','Collagène en K-beauty : tout comprendre','10 Fév 2026','@jameswelshskin',BL_COLLAGEN,'Topique ou oral ? Les formules coréennes au collagène qui fonctionnent.'),
    ('guides','Guide','K-beauty pour hommes : par où commencer','1 Fév 2026','@gothamista',BL_MEN,'Routines minimalistes, textures légères — la K-beauty au masculin.'),
]
JOURNAL_CSS = '.journal-wrap{max-width:1360px;margin:0 auto;padding:32px 16px 80px}.journal-grid{display:grid;grid-template-columns:1fr;gap:20px}.article-card{cursor:pointer;transition:transform .2s;background:#fff;border:1px solid var(--border)}.article-card:hover{transform:translateY(-2px)}@media(min-width:768px){.journal-grid{grid-template-columns:repeat(2,1fr)}}@media(min-width:1024px){.journal-grid{grid-template-columns:repeat(3,1fr)}}'
j_filter = filter_strip([('all','Tout','All'),('tendance','Tendance','Trend'),('routine','Routine','Routine'),('ingredients','Ingrédients','Ingredients'),('spf','SPF','SPF'),('actifs','Actifs','Actives'),('guides','Guides','Guides')], '.article-card')
j_articles = ''.join(f'<div class="article-card" data-tags="{cat}" onclick="window.location=\'journal.html\'"><div class="blog-img">{imgref(img,title)}</div><div style="padding:18px"><p class="blog-tag">{tag}</p><h3 class="blog-title">{title}</h3><p class="blog-excerpt">{excerpt}</p><div class="blog-meta"><span>{date}</span><span>· {author}</span></div></div></div>' for cat,tag,title,date,author,img,excerpt in ARTICLES)
journal_body = f'<div class="journal-wrap"><h1 class="page-title">Le journal Sonagi</h1><p class="page-subtitle">Tendances, ingrédients, routines et coulisses de la K-beauty.</p>{j_filter}<div class="journal-grid">{j_articles}</div></div>'
with open(f'{_out}/journal.html','w',encoding='utf-8') as f:
    f.write(page('Le Journal', journal_body, 'Journal', JOURNAL_CSS))
print(f"✓ journal.html — {os.path.getsize(f'{_out}/journal.html')/1024:.0f} KB")

# ── MASTERCLASSES ─────────────────────────────────────────────────────────────
MC_CSS = """.mc-wrap{max-width:1360px;margin:0 auto;padding:32px 16px 80px}
.evt-full-card{background:#fff;border:1px solid var(--border);overflow:hidden;transition:transform .2s}
.evt-full-card:hover{transform:translateY(-2px)}
.evt-full-img{aspect-ratio:16/9;overflow:hidden}
.evt-full-img img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.evt-full-body{padding:20px;display:flex;flex-direction:column}
.evt-meta span{font-size:11px;color:var(--muted)}
.evt-full-title{font-family:"Cormorant Garamond",serif;font-size:20px;color:var(--navy);margin-bottom:8px;line-height:1.3}
.evt-full-desc{font-size:12px;color:var(--muted);line-height:1.75;margin-bottom:14px;flex:1}
.evt-full-footer{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border);padding-top:12px}
.evt-full-price{font-size:20px;font-family:"Cormorant Garamond",serif;color:var(--navy)}
.mc-grid{display:grid;grid-template-columns:1fr;gap:18px}
@media(min-width:768px){.mc-grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1024px){.mc-grid{grid-template-columns:repeat(3,1fr)}}"""
MC_EVENTS = [
    (P6,'online','gratuit','Webinaire','10 Mai 2026','14h00','1h30','Masterclass : Lire une étiquette INCI','Décryptez les ingrédients derrière les noms scientifiques.','Gratuit','89'),
    (GL,'online','payant','Live interactif','24 Mai 2026','15h00','1h30','Atelier Glass Skin','Routine complète en direct : double nettoyage, essence, sérum, SPF.','12 €','45'),
    (P7,'live','payant','Atelier physique','7 Juin 2026','10h00','3h','Workshop : Bâtir sa routine K-beauty','Atelier en petit groupe de 12. Diagnostic de peau individuel + produits fournis.','45 €','12'),
    (P3,'online','payant','Expert session','21 Juin 2026','16h00','1h30','Masterclass : Acides & Actifs','AHA, BHA, PHA, niacinamide — comment les associer sans agresser votre peau.','15 €','60'),
    (P4,'online','payant','Live interactif','12 Juil 2026','14h00','1h30','Routine matin vs soir','Découvrez comment adapter votre routine selon le moment de la journée.','12 €','60'),
    (CX,'live','payant','Atelier physique','26 Juil 2026','10h00','2h30','Diagnostic de peau : atelier expert','Diagnostic personnalisé. Construction de votre routine sur mesure.','65 €','8'),
]
mc_cards = ''.join(f'<div class="evt-full-card" data-tags="{dtype} {dfree}"><div class="evt-full-img">{imgref(img,title)}</div><div class="evt-full-body"><span class="evt-tag {"online" if dtype=="online" else "inperson"}">{tag}</span><h3 class="evt-full-title">{title}</h3><div class="evt-meta" style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px"><span>📅 {date}</span><span>🕐 {time}</span><span>⏱ {dur}</span></div><p class="evt-full-desc">{desc}</p><div class="evt-full-footer"><div><span class="evt-full-price">{price}</span><span style="font-size:11px;color:var(--muted);margin-left:6px">· {spots} places</span></div><button class="evt-reserve">Réserver</button></div></div></div>' for img,dtype,dfree,tag,date,time,dur,title,desc,price,spots in MC_EVENTS)
mc_filters = filter_strip([('all','Tous','All'),('online','En ligne','Online'),('live','En présentiel','In person'),('gratuit','Gratuits','Free')], '.evt-full-card')
mc_body = f'<div class="mc-wrap"><h1 class="page-title">Masterclasses & Ateliers</h1><p class="page-subtitle">En ligne et en présentiel — apprenez la K-beauty avec des expertes.</p>{mc_filters}<div class="mc-grid">{mc_cards}</div><section class="newsletter" style="margin-top:48px"><h2>Ne manquez aucun atelier</h2><p>Recevez les nouvelles sessions en avant-première.</p><div class="email-form"><input type="email" placeholder="Votre email"><button>S\'inscrire</button></div></section></div>'
with open(f'{_out}/masterclasses.html','w',encoding='utf-8') as f:
    f.write(page('Masterclasses & Ateliers', mc_body, 'Masterclasses', MC_CSS))
print(f"✓ masterclasses.html — {os.path.getsize(f'{_out}/masterclasses.html')/1024:.0f} KB")

# ── COMPTE ────────────────────────────────────────────────────────────────────
COMPTE_CSS = """
.auth-wrap{max-width:440px;margin:60px auto;padding:0 20px}
.auth-tabs-bar{display:flex;border-bottom:1px solid var(--border);margin-bottom:24px}
.auth-tab{flex:1;padding:12px 0;text-align:center;font-size:11px;letter-spacing:2px;text-transform:uppercase;cursor:pointer;border-bottom:2px solid transparent;background:none;border-top:none;border-left:none;border-right:none;color:var(--muted);transition:all .2s;font-family:'DM Sans',sans-serif}
.auth-tab.active{color:var(--navy);border-bottom-color:var(--navy)}
.auth-form{display:flex;flex-direction:column;gap:12px}
.auth-submit{width:100%;background:var(--navy);color:#fff;border:none;padding:14px;font-size:11px;letter-spacing:2px;text-transform:uppercase;font-family:'DM Sans',sans-serif;margin-top:4px}
.auth-or{text-align:center;font-size:11px;color:var(--muted);margin:14px 0;display:flex;align-items:center;gap:10px}
.auth-or::before,.auth-or::after{content:"";flex:1;height:1px;background:var(--border)}
.social-btn{width:100%;border:1px solid var(--border);padding:12px;font-size:12px;font-family:'DM Sans',sans-serif;background:#fff;display:flex;align-items:center;justify-content:center;gap:8px}
.rewards-teaser{margin-top:24px;background:var(--peach-l);border:1px solid var(--peach);padding:14px 16px;text-align:center;font-size:12px;color:var(--navy);line-height:1.7}
.acct-layout{max-width:1100px;margin:0 auto;padding:32px 16px 80px;display:grid;grid-template-columns:1fr;gap:20px}
.acct-panel{background:#fff;border:1px solid var(--border);padding:24px}
.acct-panel h2{font-size:22px;color:var(--navy);margin-bottom:16px}
.orders-tbl{width:100%;border-collapse:collapse;font-size:12px}
.orders-tbl th{text-align:left;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);padding-bottom:8px;border-bottom:1px solid var(--border)}
.orders-tbl td{padding:11px 0;border-bottom:1px solid var(--border);color:var(--text)}
.o-status{display:inline-block;padding:2px 8px;font-size:9px;letter-spacing:1px;text-transform:uppercase}
.o-status.delivered{background:#e8f5e9;color:#2e7d32}.o-status.shipped{background:#e3f2fd;color:#1565c0}
.pts-big{font-size:56px;font-family:'Cormorant Garamond',serif;color:var(--navy);text-align:center;line-height:1}
/* Form alignment fix */
.form-grp{display:flex;flex-direction:column;gap:4px;width:100%}
.form-lbl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}
.form-inp{border:1px solid var(--border);padding:10px 14px;font-size:13px;font-family:'DM Sans',sans-serif;outline:none;background:#fff;width:100%;box-sizing:border-box}
.form-inp:focus{border-color:var(--navy)}
@media(min-width:768px){.acct-layout{grid-template-columns:200px 1fr}}
"""
COMPTE_EXTRA_JS = """<script>
function switchAuthTab(btn,id){document.querySelectorAll('.auth-tab').forEach(function(t){t.classList.remove('active')});btn.classList.add('active');document.getElementById('auth-login').style.display=id==='login'?'block':'none';document.getElementById('auth-register').style.display=id==='register'?'block':'none';}
function showAccount(){document.getElementById('auth-panel').style.display='none';document.getElementById('account-panel').style.display='block';}
</script>"""
compte_body = '''<div id="auth-panel"><div class="auth-wrap">
  <h1 class="page-title" style="text-align:center">Mon compte</h1>
  <div class="auth-tabs-bar">
    <button class="auth-tab active" onclick="switchAuthTab(this,'login')">Se connecter</button>
    <button class="auth-tab" onclick="switchAuthTab(this,'register')">Créer un compte</button>
  </div>
  <div id="auth-login">
    <div class="auth-form">
      <div class="form-grp"><label class="form-lbl">Email</label><input class="form-inp" type="email" placeholder="marie@exemple.fr"></div>
      <div class="form-grp"><label class="form-lbl">Mot de passe</label><input class="form-inp" type="password" placeholder="••••••••"></div>
      <button class="auth-submit" onclick="showAccount()">Se connecter</button>
    </div>
    <div class="auth-or">ou</div>
    <button class="social-btn">
      <svg width="16" height="16" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
      Continuer avec Google
    </button>
  </div>
  <div id="auth-register" style="display:none">
    <div class="auth-form">
      <div class="form-grp"><label class="form-lbl">Prénom</label><input class="form-inp" type="text" placeholder="Marie"></div>
      <div class="form-grp"><label class="form-lbl">Email</label><input class="form-inp" type="email" placeholder="marie@exemple.fr"></div>
      <div class="form-grp"><label class="form-lbl">Mot de passe</label><input class="form-inp" type="password" placeholder="Minimum 8 caractères"></div>
      <button class="auth-submit" onclick="showAccount()">Créer mon compte</button>
    </div>
  </div>
  <div class="rewards-teaser">★ Rejoignez Sonagi Rewards — gagnez des points à chaque achat, post et parrainage.</div>
</div></div>
<div id="account-panel" style="display:none"><div class="acct-layout">
  <nav style="display:flex;flex-direction:column">
    <a href="#" style="display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid var(--border);font-size:13px;color:var(--navy);text-decoration:none">📦 Mes commandes</a>
    <a href="rewards.html" style="display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid var(--border);font-size:13px;color:var(--text);text-decoration:none">★ Mes points Rewards</a>
    <a href="#" style="display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid var(--border);font-size:13px;color:var(--text);text-decoration:none">❤ Ma liste de souhaits</a>
    <a href="#" style="display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid var(--border);font-size:13px;color:var(--muted);text-decoration:none">Déconnexion</a>
  </nav>
  <div>
    <div class="acct-panel" style="margin-bottom:14px">
      <div class="pts-big">247</div>
      <p style="text-align:center;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-top:4px">Sonagi Rewards Points</p>
      <p style="text-align:center;font-size:11px;color:var(--muted);margin-top:6px">Prochain palier : 500 pts · <a href="rewards.html" style="color:var(--navy);border-bottom:1px solid var(--navy)">Voir mes avantages</a></p>
    </div>
    <div class="acct-panel">
      <h2>Mes dernières commandes</h2>
      <table class="orders-tbl"><thead><tr><th>Commande</th><th>Date</th><th>Total</th><th>Statut</th></tr></thead>
      <tbody>
        <tr><td>#SB-2026-041</td><td>8 Avr 2026</td><td>79,40 €</td><td><span class="o-status delivered">Livré</span></td></tr>
        <tr><td>#SB-2026-033</td><td>22 Mar 2026</td><td>45,80 €</td><td><span class="o-status shipped">Expédié</span></td></tr>
        <tr><td>#SB-2026-021</td><td>5 Mar 2026</td><td>38,90 €</td><td><span class="o-status delivered">Livré</span></td></tr>
      </tbody></table>
    </div>
  </div>
</div></div>'''
compte_page = page('Mon compte', compte_body, extra_css=COMPTE_CSS) + COMPTE_EXTRA_JS
with open(f'{_out}/compte.html','w',encoding='utf-8') as f:
    f.write(compte_page)
print(f"✓ compte.html — {os.path.getsize(f'{_out}/compte.html')/1024:.0f} KB")

# ── REWARDS ───────────────────────────────────────────────────────────────────
RWD_CSS = """.rwd-hero{background:var(--navy);color:#fff;padding:64px 20px;text-align:center}
.rwd-hero h1{font-size:44px;color:#fff;margin-bottom:12px}
.rwd-hero p{font-size:14px;color:var(--border);max-width:480px;margin:0 auto 24px;line-height:1.75}
.rwd-join-btn{background:var(--peach);color:var(--navy);border:none;padding:14px 32px;font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:500;border-radius:24px}
.rwd-wrap{max-width:1100px;margin:0 auto;padding:48px 20px 80px}
.rwd-section{margin-bottom:48px;padding-bottom:48px;border-bottom:1px solid var(--border)}
.rwd-section h2{font-size:28px;color:var(--navy);margin-bottom:20px}
.earn-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.earn-card{background:#fff;border:1px solid var(--border);padding:20px;text-align:center}
.earn-pts{font-size:22px;font-family:'Cormorant Garamond',serif;color:var(--navy);margin-bottom:4px}
.earn-lbl{font-size:11px;color:var(--muted);line-height:1.5}
.tier-grid{display:grid;grid-template-columns:1fr;gap:14px}
.tier-card{border:1px solid var(--border);padding:22px;background:#fff}
.tier-card.current{border-color:var(--navy);border-width:2px}
.tier-name{font-family:'Cormorant Garamond',serif;font-size:22px;color:var(--navy);margin-bottom:6px}
.tier-pts{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.tier-perks{list-style:none;display:flex;flex-direction:column;gap:8px}
.tier-perks li{font-size:12px;color:var(--text);display:flex;align-items:flex-start;gap:8px}
.tier-perks li::before{content:"✓";color:var(--navy);font-weight:700;flex-shrink:0}
.redeem-grid{display:grid;grid-template-columns:1fr;gap:12px}
.redeem-card{background:var(--cream);border:1px solid var(--border);padding:18px;display:flex;align-items:center;gap:14px}
.redeem-pts{font-size:28px;font-family:'Cormorant Garamond',serif;color:var(--navy);flex-shrink:0;min-width:72px}
.redeem-title{font-size:14px;color:var(--navy);margin-bottom:4px}
.redeem-desc{font-size:12px;color:var(--muted);line-height:1.5}
.redeem-btn{background:none;border:1px solid var(--navy);padding:7px 16px;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--navy);flex-shrink:0}
@media(min-width:768px){.rwd-hero h1{font-size:60px}.earn-grid{grid-template-columns:repeat(4,1fr)}.tier-grid{grid-template-columns:repeat(3,1fr)}.redeem-grid{grid-template-columns:repeat(2,1fr)}}"""
rewards_body = '''<div class="rwd-hero"><span class="lbl" style="color:var(--border)">Programme de fidélité</span>
  <h1>Sonagi Rewards</h1>
  <p>Gagnez des points à chaque achat, post et parrainage. Échangez-les contre des avantages exclusifs.</p>
  <button class="rwd-join-btn" onclick="window.location='compte.html'">Rejoindre Sonagi Rewards</button>
</div>
<div class="rwd-wrap">
  <div class="rwd-section"><h2>Comment gagner des points</h2><div class="earn-grid">
    <div class="earn-card"><div style="font-size:28px;margin-bottom:8px">🛒</div><div class="earn-pts">1 pt / €</div><div class="earn-lbl">Chaque euro dépensé</div></div>
    <div class="earn-card"><div style="font-size:28px;margin-bottom:8px">📱</div><div class="earn-pts">+50 pts</div><div class="earn-lbl">Post TikTok ou Instagram #Sonagi</div></div>
    <div class="earn-card"><div style="font-size:28px;margin-bottom:8px">👥</div><div class="earn-pts">+100 pts</div><div class="earn-lbl">Par ami parrainé dès son 1er achat</div></div>
    <div class="earn-card"><div style="font-size:28px;margin-bottom:8px">⭐</div><div class="earn-pts">+25 pts</div><div class="earn-lbl">Par avis produit publié avec photo</div></div>
  </div></div>
  <div class="rwd-section"><h2>Les paliers Rewards</h2><div class="tier-grid">
    <div class="tier-card current"><div style="font-size:30px;margin-bottom:10px">🌱</div><div class="tier-name">Sonagi</div><div class="tier-pts">0 – 499 points</div><ul class="tier-perks"><li>1 point par euro dépensé</li><li>-5€ dès 200 points</li><li>Livraison offerte dès 50€</li></ul></div>
    <div class="tier-card"><div style="font-size:30px;margin-bottom:10px">✨</div><div class="tier-name">Sonagi Glow</div><div class="tier-pts">500 – 1 499 points</div><ul class="tier-perks"><li>Produit offert à 500 pts</li><li>Accès prioritaire nouveautés</li><li>Birthday -15%</li></ul></div>
    <div class="tier-card"><div style="font-size:30px;margin-bottom:10px">💎</div><div class="tier-name">Sonagi Éclat</div><div class="tier-pts">1 500 points +</div><ul class="tier-perks"><li>Livraison offerte dès 0€</li><li>Accès VIP masterclasses</li><li>Invitations événements exclusifs</li></ul></div>
  </div></div>
  <div class="rwd-section" style="border-bottom:none"><h2>Échanger mes points</h2><div class="redeem-grid">
    <div class="redeem-card"><div class="redeem-pts">200</div><div><p class="redeem-title">-5€ sur ma prochaine commande</p><p class="redeem-desc">Valable sans minimum d\'achat.</p></div><button class="redeem-btn">Utiliser</button></div>
    <div class="redeem-card"><div class="redeem-pts">500</div><div><p class="redeem-title">Produit offert de mon choix</p><p class="redeem-desc">Parmi une sélection jusqu\'à 25€.</p></div><button class="redeem-btn">Utiliser</button></div>
    <div class="redeem-card"><div class="redeem-pts">300</div><div><p class="redeem-title">Accès masterclass premium</p><p class="redeem-desc">Réservez une masterclass avec vos points.</p></div><button class="redeem-btn">Utiliser</button></div>
    <div class="redeem-card"><div class="redeem-pts">150</div><div><p class="redeem-title">Livraison express offerte</p><p class="redeem-desc">Chronopost 24h sur votre prochaine commande.</p></div><button class="redeem-btn">Utiliser</button></div>
  </div></div>
</div>
<section style="background:var(--navy);padding:52px 20px;text-align:center"><h2 style="font-size:32px;color:#fff;margin-bottom:10px">Prête à commencer ?</h2><p style="font-size:13px;color:var(--border);max-width:380px;margin:0 auto 22px;line-height:1.75">Créez votre compte gratuitement et commencez dès votre premier achat.</p><button class="rwd-join-btn" onclick="window.location='compte.html'">Créer mon compte</button></section>'''
with open(f'{_out}/rewards.html','w',encoding='utf-8') as f:
    f.write(page('Sonagi Rewards', rewards_body, extra_css=RWD_CSS))
print(f"✓ rewards.html — {os.path.getsize(f'{_out}/rewards.html')/1024:.0f} KB")

# ── CONFIRMATION ─────────────────────────────────────────────────────────────
CONF_CSS = """.conf-wrap{max-width:580px;margin:52px auto;padding:0 20px;text-align:center}
.conf-icon{width:60px;height:60px;background:var(--peach-l);border:2px solid var(--peach);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:26px}
.order-box{background:#fff;border:1px solid var(--border);padding:22px;text-align:left;margin-bottom:20px}
.order-box h3{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--navy);margin-bottom:14px}
.order-row{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--border);font-size:13px}
.order-row:last-child{border-bottom:none;font-weight:500;color:var(--navy);font-size:15px}
.conf-cta{background:var(--navy);color:#fff;border:none;padding:14px;font-size:11px;letter-spacing:2px;text-transform:uppercase;width:100%;margin-bottom:10px}
.conf-sec{background:none;border:1px solid var(--border);padding:13px;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--navy);width:100%}
.next-steps{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:580px;margin:20px auto 0;text-align:left}
.next-step{background:#fff;border:1px solid var(--border);padding:16px;text-decoration:none;display:block;transition:transform .2s}
.next-step:hover{transform:translateY(-2px)}
@media(min-width:768px){.next-steps{grid-template-columns:repeat(4,1fr)}}"""
conf_body = '''<div style="padding:32px 16px 80px">
  <div class="conf-wrap">
    <div class="conf-icon">✓</div>
    <p style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--muted)">Commande confirmée</p>
    <h1 class="page-title">Merci pour votre commande !</h1>
    <p style="font-size:13px;color:var(--muted);margin-bottom:24px;line-height:1.7">Un email de confirmation a été envoyé à marie@exemple.fr. Vous recevrez un email de suivi dès l\'expédition.</p>
    <div class="order-box"><h3>Récapitulatif — #SB-2026-042</h3>
      <div class="order-row"><span>Watermelon Glow Niacinamide Dew Drops</span><span>38,00 €</span></div>
      <div class="order-row"><span>Relief Sun Rice + Probiotics SPF50+</span><span>18,90 €</span></div>
      <div class="order-row"><span>Advanced Snail 96 Mucin Power Essence</span><span>22,50 €</span></div>
      <div class="order-row"><span>Livraison</span><span style="color:var(--navy)">Offerte</span></div>
      <div class="order-row"><span>Total payé</span><span>79,40 €</span></div>
    </div>
    <div style="display:flex;flex-direction:column;gap:10px">
      <button class="conf-cta" onclick="window.location='compte.html'">Suivre ma commande</button>
      <button class="conf-sec" onclick="window.location='skincare.html'">Continuer mes achats</button>
    </div>
  </div>
  <div style="background:var(--peach-l);border:1px solid var(--peach);padding:14px;text-align:center;margin:0 auto;max-width:580px">
    <div style="font-size:48px;font-family:'Cormorant Garamond',serif;color:var(--navy)">+79 pts</div>
    <p style="font-size:11px;color:var(--muted);margin-top:4px">Vous venez de gagner 79 points · Solde : 326 points</p>
  </div>
  <p style="text-align:center;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin:20px 0 14px">Et maintenant ?</p>
  <div class="next-steps">
    <a href="journal.html" class="next-step"><div style="font-size:22px;margin-bottom:6px">📖</div><p style="font-size:13px;color:var(--navy);margin-bottom:3px">Lire le journal</p><p style="font-size:11px;color:var(--muted)">Conseils K-beauty</p></a>
    <a href="masterclasses.html" class="next-step"><div style="font-size:22px;margin-bottom:6px">🎓</div><p style="font-size:13px;color:var(--navy);margin-bottom:3px">Réserver un atelier</p><p style="font-size:11px;color:var(--muted)">En ligne & présentiel</p></a>
    <a href="rewards.html" class="next-step"><div style="font-size:22px;margin-bottom:6px">⭐</div><p style="font-size:13px;color:var(--navy);margin-bottom:3px">Mes points Rewards</p><p style="font-size:11px;color:var(--muted)">326 pts disponibles</p></a>
    <a href="skincare.html" class="next-step"><div style="font-size:22px;margin-bottom:6px">🛒</div><p style="font-size:13px;color:var(--navy);margin-bottom:3px">Découvrir la boutique</p><p style="font-size:11px;color:var(--muted)">Nouveautés K-beauty</p></a>
  </div>
</div>'''
with open(f'{_out}/confirmation.html','w',encoding='utf-8') as f:
    f.write(page('Commande confirmée', conf_body, extra_css=CONF_CSS))
print(f"✓ confirmation.html — {os.path.getsize(f'{_out}/confirmation.html')/1024:.0f} KB")

# ── Final report ──────────────────────────────────────────────────────────────
print("\n══ BUILD COMPLETE ══")
total = 0
for p in ['index','skincare','maquillage','haircare','produit','panier','marques','journal','masterclasses','compte','rewards','confirmation']:
    sz = os.path.getsize(f'{_out}/{p}.html')
    total += sz
    print(f"  {p+'.html':25} {sz/1024:5.0f} KB")
print(f"\n  Total: {total/1024:.0f} KB")
