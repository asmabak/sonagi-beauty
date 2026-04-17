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
function addBasketToCart() {
  document.querySelectorAll('#quiz-basket .basket-item').forEach(function(it){
    cartItems.push({
      brand: it.getAttribute('data-brand') || '',
      name:  it.getAttribute('data-name')  || '',
      price: it.querySelector('.basket-price') ? it.querySelector('.basket-price').textContent : '0 €'
    });
  });
  renderCart();
  closeQuiz();
  setTimeout(function(){ toggleCart(); }, 250);
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
});
