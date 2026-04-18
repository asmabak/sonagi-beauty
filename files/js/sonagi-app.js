/* ══════════════════════════════════════════════════════
   SONAGI APP — shared client JS (nav, cart sidebar, language, init)
   Single source of truth. Page-specific JS stays inline.
   ══════════════════════════════════════════════════════ */
/* ══════════════════════════════════════════════════════
   SONAGI BEAUTY — SHARED JS v4 (clean rebuild)
   All page interactions. No quiz here (quiz.js is separate).
   ══════════════════════════════════════════════════════ */

// ── LANGUAGE ──────────────────────────────────────────
var LANG = 'fr';
function setLang(l) {
  LANG = l;
  document.querySelectorAll('[id^="btn-"][id$="-fr"],[id^="btn-"][id$="-en"]').forEach(function(b){
    b.classList.toggle('active', b.id.endsWith('-'+l));
  });
  document.querySelectorAll('[data-fr]').forEach(function(el) {
    var v = el.getAttribute('data-'+l);
    if (v) el.innerHTML = v;
  });
  document.querySelectorAll('input[data-fr]').forEach(function(el) {
    var v = el.getAttribute('data-'+l);
    if (v) el.placeholder = v;
  });
}

// ── ANNOUNCE BAR ──────────────────────────────────────
var ANN_MSGS = [
  'Livraison offerte dès 50€ · Expédition sous 24h (lun–ven)',
  'Gagnez des points avec chaque achat — Sonagi Rewards',
  'Publiez votre routine #Sonagi et gagnez +50 points',
  'Masterclasses K-beauty en ligne et en présentiel → Réservez'
];
var annIdx = 0;
function rotateAnn(d) {
  annIdx = (annIdx + d + ANN_MSGS.length) % ANN_MSGS.length;
  var el = document.querySelector('.ann-msg');
  if (el) el.textContent = ANN_MSGS[annIdx];
}
setInterval(function(){ rotateAnn(1); }, 4500);

// ── MOBILE MENU (drill-down) ─────────────────────────
var mobStack = [];
function openMobileMenu() {
  var m = document.getElementById('mobile-menu');
  var bd = document.getElementById('mob-backdrop');
  if (!m) return;
  mobStack = [];
  document.querySelectorAll('.mob-panel').forEach(function(p){ p.classList.remove('active'); });
  var l1 = document.getElementById('mob-l1');
  if (l1) l1.classList.add('active');
  var back = document.getElementById('mob-back');
  if (back) back.style.display = 'none';
  var title = document.getElementById('mob-title');
  if (title) title.textContent = 'SONAGI';
  m.classList.add('open');
  if (bd) bd.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMobileMenu() {
  var m = document.getElementById('mobile-menu');
  var bd = document.getElementById('mob-backdrop');
  if (m) m.classList.remove('open');
  if (bd) bd.classList.remove('open');
  document.body.style.overflow = '';
  mobStack = [];
}
function mobDrill(panelId, label) {
  var current = document.querySelector('.mob-panel.active');
  if (current) {
    mobStack.push({ id: current.id, label: document.getElementById('mob-title').textContent });
    current.classList.remove('active');
  }
  var next = document.getElementById(panelId);
  if (next) next.classList.add('active');
  var title = document.getElementById('mob-title');
  if (title) title.textContent = label;
  var back = document.getElementById('mob-back');
  if (back) back.style.display = 'block';
}
function mobBack() {
  if (!mobStack.length) return;
  var prev = mobStack.pop();
  var current = document.querySelector('.mob-panel.active');
  if (current) current.classList.remove('active');
  var prevPanel = document.getElementById(prev.id);
  if (prevPanel) prevPanel.classList.add('active');
  var title = document.getElementById('mob-title');
  if (title) title.textContent = prev.label;
  var back = document.getElementById('mob-back');
  if (back) back.style.display = mobStack.length ? 'block' : 'none';
}

// ── HERO CAROUSEL ─────────────────────────────────────
var CS = 0, CT = 0;
function initCarousel() {
  var slides = document.querySelectorAll('.c-slide');
  CT = slides.length;
  if (!CT) return;
  buildDots();
  setInterval(function(){ moveSlide(1); }, 5500);
}
function moveSlide(d) { goSlide((CS + d + CT) % CT); }
function goSlide(n) {
  document.querySelectorAll('.c-slide').forEach(function(s,i){ s.classList.toggle('active', i===n); });
  document.querySelectorAll('.c-dot').forEach(function(d,i){ d.classList.toggle('active', i===n); });
  CS = n;
}
function buildDots() {
  var el = document.getElementById('c-dots');
  if (!el) return;
  el.innerHTML = '';
  for (var i=0; i<CT; i++) {
    var b = document.createElement('button');
    b.className = 'c-dot' + (i===0 ? ' active' : '');
    b.setAttribute('data-i', i);
    b.addEventListener('click', (function(idx){ return function(){ goSlide(idx); }; })(i));
    el.appendChild(b);
  }
}

// ── PRODUCT TABS ──────────────────────────────────────
function switchTab(el, id) {
  document.querySelectorAll('.tab').forEach(function(t){ t.classList.remove('active'); });
  el.classList.add('active');
  ['pn','pb'].forEach(function(tid){
    var g = document.getElementById(tid);
    if (g) g.style.display = (tid === id) ? 'grid' : 'none';
  });
}

// ── GENERIC FILTER ────────────────────────────────────
// Works for any filter strip + any card set.
// Usage: <button class="filt-btn active" data-filter="all" data-target=".article-card" data-attr="data-cat">
// Each card gets e.g. data-cat="tendance"
function initFilters() {
  document.querySelectorAll('.filt-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var parent = btn.parentElement;
      parent.querySelectorAll('.filt-btn').forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');

      var filterVal = btn.getAttribute('data-filter') || 'all';
      var targetSel = btn.getAttribute('data-target') || parent.getAttribute('data-target') || '.prod-card';

      document.querySelectorAll(targetSel).forEach(function(card) {
        if (filterVal === 'all') {
          card.style.display = '';
        } else {
          // Support both data-tags (space-separated) and legacy data-cat
          var tags = (card.getAttribute('data-tags') || card.getAttribute('data-cat') || '').split(' ');
          card.style.display = tags.indexOf(filterVal) > -1 ? '' : 'none';
        }
      });

      // Hide empty letter groups (brand page)
      document.querySelectorAll('.brand-letter-group').forEach(function(g) {
        var hasVisible = Array.from(g.querySelectorAll('.brand-name')).some(function(n){ return n.style.display !== 'none'; });
        g.style.display = hasVisible ? '' : 'none';
      });
    });
  });
}

// ── REVIEWS INFINITE LOOP ────────────────────────────────────────────
var RS = 0;
function initReviews() {
  var track = document.getElementById('rev-track');
  if (!track) return;
  // Duplicate cards for seamless infinite loop
  track.innerHTML += track.innerHTML;
}
function moveRev(d) {
  var slides = document.querySelectorAll('.rev-slide');
  var perView = window.innerWidth >= 768 ? 3 : 1;
  var half = slides.length / 2;
  RS = ((RS + d) % half + half) % half;
  var pct = 100 / perView;
  slides.forEach(function(s){ s.style.flexBasis = pct+'%'; s.style.minWidth = pct+'%'; });
  var track = document.getElementById('rev-track');
  if (track) track.style.transform = 'translateX(-'+(RS*pct)+'%)';
}
window.addEventListener('resize', function(){ RS=0; moveRev(0); });

// ── PRODUCT GALLERY (product detail page) ────────────
function setMainImg(thumb) {
  var main = document.getElementById('main-img');
  if (main) main.src = thumb.src;
  document.querySelectorAll('.prod-thumb').forEach(function(t){ t.classList.remove('active'); });
  thumb.classList.add('active');
}
function switchProdTab(btn, id) {
  document.querySelectorAll('.prod-tab').forEach(function(t){ t.classList.remove('active'); });
  document.querySelectorAll('.prod-tab-pane').forEach(function(t){ t.classList.remove('active'); });
  btn.classList.add('active');
  var pane = document.getElementById('ptab-'+id);
  if (pane) pane.classList.add('active');
}

// ── FILTER SIDEBAR TOGGLE ─────────────────────────────
function toggleFilter(el) {
  var opts = el.nextElementSibling;
  if (opts) opts.style.display = opts.style.display === 'flex' ? 'none' : 'flex';
}

// ── BRAND SEARCH ─────────────────────────────────────
function filterBrands(q) {
  q = (q||'').trim().toLowerCase();
  var names = document.querySelectorAll('.brand-name');
  var visible = 0;
  names.forEach(function(el){
    var matches = !q || el.textContent.toLowerCase().indexOf(q) !== -1;
    el.style.display = matches ? '' : 'none';
    if (matches) visible++;
  });
  document.querySelectorAll('.brand-letter-group').forEach(function(g){
    var has = Array.from(g.querySelectorAll('.brand-name')).some(function(n){ return n.style.display !== 'none'; });
    g.style.display = has ? '' : 'none';
  });
  var cnt = document.getElementById('brand-count');
  if (cnt) cnt.textContent = visible + ' marque' + (visible!==1?'s':'');
}

// ── CART ─────────────────────────────────────────────
var cartItems = [];
function toggleCart() {
  var c = document.getElementById('cart-sidebar');
  if (c) c.classList.toggle('open');
}
function renderCart() {
  var body = document.getElementById('cart-body');
  var foot = document.getElementById('cart-foot');
  var badge = document.getElementById('cart-badge');
  if (!body) return;
  if (!cartItems.length) {
    body.innerHTML = '<p class="cart-empty">Votre panier est vide</p>';
    if (foot) foot.style.display = 'none';
    if (badge) badge.textContent = '0';
    return;
  }
  var total = 0;
  body.innerHTML = cartItems.map(function(it){
    var p = parseFloat((it.price||'0').replace(/[^0-9,]/g,'').replace(',','.')) || 0;
    total += p;
    return '<div style="padding:12px 0;border-bottom:1px solid var(--border)">'
      +'<p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--muted)">'+it.brand+'</p>'
      +'<p style="font-size:12px;color:var(--text);margin:2px 0">'+it.name+'</p>'
      +'<p style="font-size:12px;color:var(--navy);font-weight:500">'+it.price+'</p>'
      +'</div>';
  }).join('');
  var tot = document.getElementById('cart-total');
  if (tot) tot.textContent = total.toFixed(2).replace('.',',') + ' €';
  if (foot) foot.style.display = 'block';
  if (badge) badge.textContent = cartItems.length;
}
// ── addBasketToCart() removed — moved into sonagi-quiz.js (basket logic
//    is now built from the AI advisor JSON, not from a #quiz-basket DOM
//    that the new quiz module no longer renders). Kept as a no-op shim
//    so any stray inline onclick="addBasketToCart()" doesn't throw.
function addBasketToCart() {
  if (window.SonagiQuiz && typeof window.SonagiQuiz.open === 'function') {
    // Old call sites probably want to re-open the quiz to use the new baskets
    window.SonagiQuiz.open();
  }
}

// ── TOUCH — show add button on mobile tap ─────────────
function initTouch() {
  document.querySelectorAll('.prod-card').forEach(function(card){
    card.addEventListener('touchstart', function(){
      document.querySelectorAll('.prod-card').forEach(function(c){ c.classList.remove('touched'); });
      card.classList.add('touched');
    }, {passive:true});
  });
}

// ── INIT ─────────────────────────────────────────────

// ── IMAGE RESOLVER ────────────────────────────────────
function resolveImages() {
  var imgs = window.QUIZ_IMGS || {};
  document.querySelectorAll('img[data-imgkey]').forEach(function(el) {
    var k = el.getAttribute('data-imgkey');
    if (imgs[k]) el.src = imgs[k];
  });
}
// QUIZ_IMGS is inline so call immediately — no waiting needed
resolveImages();
window.addEventListener('load', resolveImages);

document.addEventListener('DOMContentLoaded', function(){
  initCarousel();
  initFilters();
  initReviews();
  initTouch();
  resolveImages();
  initSearch();
  injectFooterLang();
});

// ── GLOBAL SEARCH ────────────────────────────────────
// Editorial overlay search across products, brands, concerns, journal, pages.
// Lightweight client-side fuzzy match. Pre-launch friendly — no backend needed.

var SONAGI_SEARCH_INDEX = [
  // ── Concerns (entry path to filtered category)
  { type:'concern', label:"Pores dilatés",         url:'skincare.html?concern=pores',       kw:'pores grands sébum mogong 모공 oily t-zone' },
  { type:'concern', label:"Déshydratation",        url:'skincare.html?concern=hydratation', kw:'déshydratation hydratation sec subun 수분 tiraillements' },
  { type:'concern', label:"Teint terne",           url:'skincare.html?concern=eclat',       kw:'éclat lumière glow gwangchae 광채 teint terne' },
  { type:'concern', label:"Taches & post-acné",    url:'skincare.html?concern=taches',      kw:'taches post-acné hyperpigmentation japti 잡티 mélasma' },
  { type:'concern', label:"Acné active",           url:'skincare.html?concern=acne',        kw:'acné boutons points noirs blanchâtres trouble 트러블 imperfections' },
  { type:'concern', label:"Sensibilité & rougeurs",url:'skincare.html?concern=sensibilite', kw:'sensible rougeurs barrière apaisant jinjeong 진정 réactif rosacée' },
  { type:'concern', label:"Premières rides",       url:'skincare.html?concern=rides',       kw:'rides anti-âge fermeté élasticité tallyeok 탄력 collagène' },
  { type:'concern', label:"Excès de sébum",        url:'skincare.html?concern=sebum',       kw:'sébum brillance peau grasse piji 피지 zone-t mat' },

  // ── Categories
  { type:'page', label:"Skincare",       url:'skincare.html',     kw:'skincare soins visage sérum toner crème' },
  { type:'page', label:"Maquillage",     url:'maquillage.html',   kw:'maquillage make-up tint cushion gloss baume teinté' },
  { type:'page', label:"Cheveux & Corps",url:'haircare.html',     kw:'cheveux corps haircare body masque shampoing' },
  { type:'page', label:"Toutes les marques", url:'marques.html',  kw:'marques brands 54 toutes' },
  { type:'page', label:"Diagnostic peau (5 questions)", url:'#', action:'openQuiz', kw:'quiz diagnostic peau routine personnalisée advisor' },
  { type:'page', label:"Le Journal",     url:'journal.html',      kw:'journal blog articles guides ingrédients' },
  { type:'page', label:"Masterclasses",  url:'masterclasses.html',kw:'masterclasses ateliers cours k-beauty' },
  { type:'page', label:"Sonagi Rewards", url:'rewards.html',      kw:'rewards points fidélité programme bonus' },

  // ── Featured products (homepage hero / Nouveautés / Best-Sellers)
  { type:'product', brand:'Glow Recipe',       label:"Watermelon Glow Niacinamide Dew Drops", url:'produit.html', kw:'watermelon glow niacinamide pores éclat sérum dew drops' },
  { type:'product', brand:'Beauty of Joseon',  label:"Relief Sun Rice + Probiotic SPF50+",    url:'produit.html', kw:'beauty of joseon relief sun spf50 protection solaire riz probiotique' },
  { type:'product', brand:'Anua',              label:"Heartleaf 77% Soothing Toner",          url:'produit.html', kw:'anua heartleaf toner houttuynia apaisant tonique' },
  { type:'product', brand:'Beauty of Joseon',  label:"Glow Serum Propolis + Niacinamide",     url:'produit.html', kw:'beauty of joseon glow serum propolis niacinamide éclat' },
  { type:'product', brand:'COSRX',             label:"Snail 96 Mucin Power Essence",          url:'produit.html', kw:'cosrx snail 96 mucin essence escargot réparateur' },
  { type:'product', brand:'SKIN1004',          label:"Centella Asiatica Ampoule",             url:'produit.html', kw:'skin1004 centella asiatica ampoule apaisant madagascar' },
  { type:'product', brand:'Mixsoon',           label:"Bifida Biome Essence",                  url:'produit.html', kw:'mixsoon bifida biome essence ferment microbiote' },
  { type:'product', brand:'Round Lab',         label:"1025 Dokdo Toner",                      url:'produit.html', kw:'round lab 1025 dokdo toner exfoliant doux pha' },
  { type:'product', brand:'Laneige',           label:"Lip Sleeping Mask Berry",               url:'produit.html', kw:'laneige lip sleeping mask berry baume lèvres nuit' },
  { type:'product', brand:'Huxley',            label:"Secret of Sahara Toner Extract It",     url:'produit.html', kw:'huxley secret sahara toner cactus prickly pear' },
  { type:'product', brand:'IUNIK',             label:"Centella Calming Daily Sun Cream",      url:'produit.html', kw:'iunik centella calming sun cream apaisant solaire' },

  // ── Brands (top 30 most-asked — pulled from marques.html catalog)
  { type:'brand', label:"COSRX",            url:'marques.html#LC', kw:'cosrx coréen snail mucin' },
  { type:'brand', label:"Beauty of Joseon", url:'marques.html#LB', kw:'beauty of joseon boj propolis riz spf' },
  { type:'brand', label:"Anua",             url:'marques.html#LA', kw:'anua heartleaf toner peeling' },
  { type:'brand', label:"Some By Mi",       url:'marques.html#LS', kw:'some by mi acné aha bha pha' },
  { type:'brand', label:"Laneige",          url:'marques.html#LL', kw:'laneige lèvres dormeuse cream skin' },
  { type:'brand', label:"Innisfree",        url:'marques.html#LI', kw:'innisfree thé vert volcanique mat' },
  { type:'brand', label:"Mixsoon",          url:'marques.html#LM', kw:'mixsoon ferment essence bifida' },
  { type:'brand', label:"SKIN1004",         url:'marques.html#LS', kw:'skin1004 centella ampoule madagascar' },
  { type:'brand', label:"Glow Recipe",      url:'marques.html#LG', kw:'glow recipe watermelon plum strawberry' },
  { type:'brand', label:"Round Lab",        url:'marques.html#LR', kw:'round lab dokdo birch juice tonique' },
  { type:'brand', label:"Numbuzin",         url:'marques.html#LN', kw:'numbuzin no.5 collagen serum' },
  { type:'brand', label:"Klairs",           url:'marques.html#LK', kw:'klairs vitamin c freshly juiced' },
  { type:'brand', label:"Pyunkang Yul",     url:'marques.html#LP', kw:'pyunkang yul essence toner ato' },
  { type:'brand', label:"Tirtir",           url:'marques.html#LT', kw:'tirtir mask fit cushion' },
  { type:'brand', label:"Axis-Y",           url:'marques.html#LA', kw:'axis-y dark spot mugwort' },
  { type:'brand', label:"Banila Co",        url:'marques.html#LB', kw:'banila clean it zero démaquillant balm' },
  { type:'brand', label:"Etude House",      url:'marques.html#LE', kw:'etude house play color tints' },
  { type:'brand', label:"Isntree",          url:'marques.html#LI', kw:'isntree hyaluronic toner spf' },
  { type:'brand', label:"Huxley",           url:'marques.html#LH', kw:'huxley sahara cactus hydratation' },
  { type:'brand', label:"IUNIK",            url:'marques.html#LI', kw:'iunik centella vitamin c sleeping mask' },
  { type:'brand', label:"Dr. Ceuracle",     url:'marques.html#LD', kw:'dr ceuracle royal vita propolis' },
  { type:'brand', label:"D'alba",           url:'marques.html#LD', kw:"d'alba truffe italienne mist" },
  { type:'brand', label:"Medicube",         url:'marques.html#LM', kw:'medicube zero pore pad triple collagen' },
  { type:'brand', label:"Aestura",          url:'marques.html#LA', kw:'aestura atobarrier ceramides barrière' },

  // ── Journal articles
  { type:'article', label:"Glass skin : la règle des 7 secondes",      url:'journal.html#glass',      kw:'glass skin coréenne hydratation peau mouillée 7 secondes' },
  { type:'article', label:"Le double cleansing expliqué",              url:'journal.html#double',     kw:'double cleansing nettoyage huile balm démaquillant' },
  { type:'article', label:"Centella : l'ingrédient apaisant n°1 en Corée", url:'journal.html#centella', kw:'centella asiatica madagascar apaisant ingrédient' },
  { type:'article', label:"Hanbang : la science derrière les cosmétiques coréens", url:'journal.html#hanbang', kw:'hanbang ginseng tradition coréenne herbes' },
  { type:'article', label:"Acides en K-beauty : AHA, BHA, PHA",        url:'journal.html#acides',    kw:'aha bha pha exfoliation acides peeling' },
  { type:'article', label:"SPF : pourquoi les coréens ne s'en passent pas",  url:'journal.html#spf',        kw:'spf protection solaire quotidien anti-âge' },

  // ── Ingredients (search by what it does)
  { type:'ingredient', label:"Niacinamide", url:'skincare.html?ingredient=niacinamide', kw:'niacinamide vitamine b3 pores éclat unifie teint' },
  { type:'ingredient', label:"Centella asiatique", url:'skincare.html?ingredient=centella', kw:'centella asiatique cica madagascar apaisant barrière' },
  { type:'ingredient', label:"Acide hyaluronique", url:'skincare.html?ingredient=hyaluronique', kw:'acide hyaluronique hydratation repulpant ha' },
  { type:'ingredient', label:"Vitamine C", url:'skincare.html?ingredient=vitamin-c', kw:'vitamine c éclat antioxydant taches l-ascorbic' },
  { type:'ingredient', label:"Snail mucin", url:'skincare.html?ingredient=snail', kw:'snail mucin escargot réparateur cosrx' },
  { type:'ingredient', label:"Propolis", url:'skincare.html?ingredient=propolis', kw:'propolis abeille réparateur antibactérien beauty of joseon' },
  { type:'ingredient', label:"Rétinol & rétinoïdes", url:'skincare.html?ingredient=retinol', kw:'rétinol rétinoïde anti-âge rides cell turnover' },
  { type:'ingredient', label:"Céramides", url:'skincare.html?ingredient=ceramides', kw:'céramides barrière lipides aestura ato' },
  { type:'ingredient', label:"PDRN (ADN de saumon)", url:'skincare.html?ingredient=pdrn', kw:'pdrn adn saumon salmon dna régénération' },
];

function fuzzy(haystack, needle) {
  haystack = (haystack || '').toLowerCase();
  needle = (needle || '').toLowerCase().trim();
  if (!needle) return 0;
  if (haystack.indexOf(needle) > -1) return 10;
  // multi-word: every word matches
  var words = needle.split(/\s+/).filter(Boolean);
  if (words.length > 1 && words.every(function(w){ return haystack.indexOf(w) > -1; })) return 7;
  // partial: any word matches
  for (var i = 0; i < words.length; i++) { if (haystack.indexOf(words[i]) > -1) return 4; }
  return 0;
}

function searchSonagi(q) {
  q = (q || '').trim();
  if (q.length < 2) return [];
  return SONAGI_SEARCH_INDEX
    .map(function(item){
      var hay = (item.label || '') + ' ' + (item.brand || '') + ' ' + (item.kw || '');
      return { item: item, score: fuzzy(hay, q) };
    })
    .filter(function(x){ return x.score > 0; })
    .sort(function(a,b){ return b.score - a.score; })
    .slice(0, 24)
    .map(function(x){ return x.item; });
}

function renderSearchResults(items, query) {
  var box = document.getElementById('search-results');
  if (!box) return;
  if (!query || query.length < 2) {
    box.innerHTML = '' +
      '<div class="search-section">' +
        '<p class="search-section-label">Recherches populaires</p>' +
        '<div class="search-chips">' +
          '<a class="search-chip" href="#" onclick="closeSearch();openQuiz();return false;">✦ Diagnostic peau</a>' +
          '<a class="search-chip" href="skincare.html?concern=pores">Pores</a>' +
          '<a class="search-chip" href="skincare.html?concern=hydratation">Hydratation</a>' +
          '<a class="search-chip" href="skincare.html?concern=acne">Acné</a>' +
          '<a class="search-chip" href="skincare.html?concern=sensibilite">Peau sensible</a>' +
          '<a class="search-chip" href="marques.html#LB">Beauty of Joseon</a>' +
          '<a class="search-chip" href="marques.html#LC">COSRX</a>' +
          '<a class="search-chip" href="skincare.html?ingredient=niacinamide">Niacinamide</a>' +
          '<a class="search-chip" href="skincare.html?ingredient=centella">Centella</a>' +
        '</div>' +
      '</div>';
    return;
  }
  if (!items.length) {
    box.innerHTML = '<p class="search-empty">Aucun résultat pour <strong>"' + query.replace(/[<>]/g,'') + '"</strong>. Essaie une marque, un ingrédient, ou un concern.</p>';
    return;
  }
  // Group by type
  var groups = { product: [], brand: [], concern: [], ingredient: [], article: [], page: [] };
  items.forEach(function(it){ (groups[it.type] || (groups[it.type] = [])).push(it); });
  var labels = { product:'Produits', brand:'Marques', concern:'Préoccupations', ingredient:'Ingrédients', article:'Journal', page:'Pages' };
  var html = '';
  ['product','brand','concern','ingredient','article','page'].forEach(function(type){
    var list = groups[type];
    if (!list || !list.length) return;
    html += '<div class="search-section">';
    html += '<p class="search-section-label">' + labels[type] + '</p>';
    html += '<ul class="search-list">';
    list.forEach(function(it){
      var sub = it.brand ? '<span class="search-sub">' + it.brand + '</span>' : '';
      var attr = it.action === 'openQuiz' ? 'href="#" onclick="closeSearch();openQuiz();return false;"' : 'href="' + it.url + '"';
      html += '<li><a class="search-result" ' + attr + '>' + sub + '<span class="search-label">' + it.label + '</span></a></li>';
    });
    html += '</ul>';
    html += '</div>';
  });
  box.innerHTML = html;
}

function openSearch() {
  var ov = document.getElementById('search-overlay');
  if (!ov) return;
  ov.classList.add('open');
  document.body.style.overflow = 'hidden';
  setTimeout(function(){ var i = document.getElementById('search-input'); if (i) i.focus(); }, 50);
  renderSearchResults([], '');
}
function closeSearch() {
  var ov = document.getElementById('search-overlay');
  if (!ov) return;
  ov.classList.remove('open');
  document.body.style.overflow = '';
  var i = document.getElementById('search-input');
  if (i) i.value = '';
}
window.openSearch = openSearch;
window.closeSearch = closeSearch;

function initSearch() {
  // 1. Inject the search trigger button into nav-right (left of cart)
  var navRight = document.querySelector('.nav-right');
  if (navRight && !document.querySelector('.search-trigger')) {
    var cart = navRight.querySelector('[onclick*="toggleCart"]');
    var btn = document.createElement('button');
    btn.className = 'nav-icon search-trigger';
    btn.setAttribute('aria-label', 'Rechercher');
    btn.setAttribute('onclick', 'openSearch()');
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/></svg>';
    navRight.insertBefore(btn, cart || navRight.lastChild);
  }

  // 2. Inject the search overlay into <body>
  if (!document.getElementById('search-overlay')) {
    var ov = document.createElement('div');
    ov.id = 'search-overlay';
    ov.className = 'search-overlay';
    ov.innerHTML = '' +
      '<div class="search-backdrop" onclick="closeSearch()"></div>' +
      '<div class="search-panel">' +
        '<div class="search-bar">' +
          '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/></svg>' +
          '<input type="search" id="search-input" placeholder="Cherche un produit, une marque, un ingrédient…" autocomplete="off" spellcheck="false">' +
          '<button class="search-close" onclick="closeSearch()" aria-label="Fermer">×</button>' +
        '</div>' +
        '<div class="search-results" id="search-results"></div>' +
        '<p class="search-hint"><kbd>Esc</kbd> pour fermer · <kbd>Entrée</kbd> pour aller au premier résultat</p>' +
      '</div>';
    document.body.appendChild(ov);

    var input = document.getElementById('search-input');
    if (input) {
      input.addEventListener('input', function(e){
        var q = e.target.value;
        renderSearchResults(searchSonagi(q), q);
      });
      input.addEventListener('keydown', function(e){
        if (e.key === 'Escape') closeSearch();
        if (e.key === 'Enter') {
          var first = document.querySelector('.search-result');
          if (first) first.click();
        }
      });
    }
  }

  // 3. Keyboard shortcuts: "/" or "Ctrl/Cmd+K" opens search
  document.addEventListener('keydown', function(e){
    var ov = document.getElementById('search-overlay');
    if (!ov) return;
    var isInput = ['INPUT','TEXTAREA'].indexOf((e.target.tagName || '').toUpperCase()) > -1;
    if ((e.key === '/' && !isInput) || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) {
      e.preventDefault();
      ov.classList.contains('open') ? closeSearch() : openSearch();
    }
    if (e.key === 'Escape' && ov.classList.contains('open')) closeSearch();
  });
}

// ── FOOTER LANGUAGE SWITCHER ────────────────────────
// Inject a subtle FR/EN toggle into the footer (luxury convention).
function injectFooterLang() {
  if (document.querySelector('.footer-lang')) return;
  var footer = document.querySelector('footer') || document.querySelector('.footer-wrap') || document.querySelector('.site-footer');
  if (!footer) return;
  var fl = document.createElement('div');
  fl.className = 'footer-lang';
  fl.innerHTML =
    '<span class="footer-lang-label">Langue · Language</span>' +
    '<button class="footer-lang-btn ' + (LANG === 'fr' ? 'active' : '') + '" id="fbtn-fr" onclick="setLang(\'fr\')">Français</button>' +
    '<span class="footer-lang-sep">·</span>' +
    '<button class="footer-lang-btn ' + (LANG === 'en' ? 'active' : '') + '" id="fbtn-en" onclick="setLang(\'en\')">English</button>';
  footer.appendChild(fl);
}
