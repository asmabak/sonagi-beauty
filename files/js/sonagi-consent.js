/* ══════════════════════════════════════════════════════
   SONAGI CONSENT · GDPR/CNIL cookie consent banner
   - Auto-injects on every page until user makes a choice
   - Persists in localStorage['sonagi_consent_v1'] for 6 months
   - Reject must be as easy as accept (CNIL guidelines)
   - No tracking script loads before consent
   - Bilingual (fr/en) based on sonagi_lang or browser
   ══════════════════════════════════════════════════════ */
(function(){
  'use strict';

  var STORAGE_KEY = 'sonagi_consent_v1';
  var SIX_MONTHS_MS = 1000 * 60 * 60 * 24 * 30 * 6;
  var CONSENT_VERSION = 1;

  // ── DEFAULT STATE ─────────────────────────────────────
  function defaultState() {
    return {
      necessary: true,      // always: strictly necessary
      preferences: false,   // lang, currency
      statistics: false,    // analytics
      marketing: false,     // ads pixel
      setAt: null,
      version: CONSENT_VERSION
    };
  }

  // ── PUBLIC STATE ──────────────────────────────────────
  window.SONAGI_CONSENT = defaultState();

  // ── LANGUAGE DETECTION (independent of sonagi-app.js) ──
  function detectLang() {
    var saved = null;
    try { saved = localStorage.getItem('sonagi_lang'); } catch(e) {}
    if (saved === 'fr' || saved === 'en') return saved;
    var langs = (navigator.languages || [navigator.language || 'fr']);
    for (var i = 0; i < langs.length; i++) {
      var l = (langs[i] || '').toLowerCase();
      if (l.indexOf('fr') === 0) return 'fr';
      if (l.indexOf('en') === 0) return 'en';
    }
    return 'fr';
  }

  // ── COPY ──────────────────────────────────────────────
  var COPY = {
    fr: {
      title: 'Cookies',
      body: 'On utilise des cookies pour améliorer ton expérience. Tu peux tout accepter, tout refuser, ou choisir quoi activer.',
      reject: 'Tout refuser',
      accept: 'Tout accepter',
      customize: 'Personnaliser',
      save: 'Enregistrer mes choix',
      back: 'Retour',
      modalTitle: 'Tes préférences cookies',
      modalIntro: 'Choisis les catégories que tu souhaites activer. Les cookies strictement nécessaires sont toujours actifs car ils font fonctionner le site.',
      catNecessary: 'Strictement nécessaires',
      catNecessaryDesc: 'Indispensables au fonctionnement du site (panier, sécurité, mémorisation de tes choix de cookies). Toujours actifs.',
      catPreferences: 'Préférences',
      catPreferencesDesc: 'Mémorisent ta langue et ta devise pour t\'éviter de les re-sélectionner.',
      catStatistics: 'Statistiques',
      catStatisticsDesc: 'Nous aident à comprendre comment le site est utilisé pour l\'améliorer (Google Analytics, anonymisé).',
      catMarketing: 'Marketing',
      catMarketingDesc: 'Permettent de te proposer des publicités plus pertinentes (Meta Pixel, Google Ads).',
      always: 'Toujours actif',
      learnMore: 'En savoir plus dans notre',
      cookiePolicy: 'politique cookies'
    },
    en: {
      title: 'Cookies',
      body: 'We use cookies to improve your experience. You can accept all, reject all, or pick what you turn on.',
      reject: 'Reject all',
      accept: 'Accept all',
      customize: 'Customize',
      save: 'Save my choices',
      back: 'Back',
      modalTitle: 'Your cookie preferences',
      modalIntro: 'Pick which categories you want to enable. Strictly necessary cookies are always on because the site needs them to work.',
      catNecessary: 'Strictly necessary',
      catNecessaryDesc: 'Required for the site to work (cart, security, remembering your cookie choice). Always on.',
      catPreferences: 'Preferences',
      catPreferencesDesc: 'Remember your language and currency so you don\'t have to pick them again.',
      catStatistics: 'Statistics',
      catStatisticsDesc: 'Help us understand how the site is used so we can improve it (Google Analytics, anonymized).',
      catMarketing: 'Marketing',
      catMarketingDesc: 'Allow us to show you more relevant ads (Meta Pixel, Google Ads).',
      always: 'Always on',
      learnMore: 'Learn more in our',
      cookiePolicy: 'cookie policy'
    }
  };

  // ── STORAGE ───────────────────────────────────────────
  function loadState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || parsed.version !== CONSENT_VERSION) return null;
      // Expire after 6 months
      if (parsed.setAt && (Date.now() - parsed.setAt) > SIX_MONTHS_MS) return null;
      return parsed;
    } catch(e) { return null; }
  }

  function saveState(state) {
    state.setAt = Date.now();
    state.version = CONSENT_VERSION;
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
    window.SONAGI_CONSENT = state;
    document.dispatchEvent(new CustomEvent('sonagi-consent-changed', { detail: state }));
  }

  // ── STYLES (injected once) ────────────────────────────
  function injectStyles() {
    if (document.getElementById('sonagi-consent-styles')) return;
    var css = '' +
      '#sonagi-consent-banner,#sonagi-consent-modal,#sonagi-consent-backdrop{font-family:"DM Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#2c2c2c;box-sizing:border-box}' +
      '#sonagi-consent-banner *,#sonagi-consent-modal *{box-sizing:border-box}' +
      '#sonagi-consent-banner{position:fixed;left:0;right:0;bottom:0;z-index:9998;background:#fff;box-shadow:0 -8px 32px rgba(0,0,0,.12);border-top:3px solid #FF3E9D;padding:20px 16px calc(20px + env(safe-area-inset-bottom,0px));animation:sonagi-consent-slide-up .35s ease-out}' +
      '@keyframes sonagi-consent-slide-up{from{transform:translateY(100%)}to{transform:translateY(0)}}' +
      '.sonagi-consent-inner{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:14px}' +
      '.sonagi-consent-text h3{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:20px;margin:0 0 6px;color:#2c2c2c;letter-spacing:-.01em}' +
      '.sonagi-consent-text p{margin:0;font-size:14px;line-height:1.55;color:#4a4036}' +
      '.sonagi-consent-actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center}' +
      '.sonagi-consent-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:12px 22px;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:500;font-family:inherit;border-radius:0;cursor:pointer;transition:opacity .15s,background .15s,color .15s;border:1.5px solid transparent;text-decoration:none;line-height:1}' +
      '.sonagi-consent-btn:focus-visible{outline:2px solid #FF3E9D;outline-offset:2px}' +
      '.sonagi-consent-btn-accept{background:#FF3E9D;color:#fff;border-color:#FF3E9D;flex:1;min-width:140px}' +
      '.sonagi-consent-btn-accept:hover{background:#e23588;border-color:#e23588}' +
      '.sonagi-consent-btn-reject{background:transparent;color:#FF3E9D;border-color:#FF3E9D;flex:1;min-width:140px}' +
      '.sonagi-consent-btn-reject:hover{background:#FF3E9D;color:#fff}' +
      '.sonagi-consent-link{background:none;border:0;color:#4a4036;text-decoration:underline;font-size:12px;letter-spacing:.5px;text-transform:none;padding:8px 12px;cursor:pointer;font-family:inherit;min-height:44px}' +
      '.sonagi-consent-link:hover{color:#FF3E9D}' +
      '@media(min-width:640px){.sonagi-consent-inner{flex-direction:row;align-items:center;gap:24px}.sonagi-consent-text{flex:1}.sonagi-consent-actions{flex-shrink:0;flex-wrap:nowrap}.sonagi-consent-btn-accept,.sonagi-consent-btn-reject{flex:0 0 auto}}' +
      /* Modal */
      '#sonagi-consent-backdrop{position:fixed;inset:0;background:rgba(28,28,28,.55);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px;animation:sonagi-consent-fade .25s ease-out}' +
      '@keyframes sonagi-consent-fade{from{opacity:0}to{opacity:1}}' +
      '#sonagi-consent-modal{background:#fff;max-width:560px;width:100%;max-height:90vh;overflow-y:auto;border-radius:8px;box-shadow:0 24px 64px rgba(0,0,0,.25);padding:0}' +
      '.sonagi-consent-modal-head{padding:24px 24px 12px;border-bottom:1px solid #ede8e2}' +
      '.sonagi-consent-modal-head h3{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:24px;margin:0 0 8px;color:#2c2c2c;letter-spacing:-.01em}' +
      '.sonagi-consent-modal-head p{margin:0;font-size:13px;line-height:1.55;color:#4a4036}' +
      '.sonagi-consent-modal-body{padding:8px 24px}' +
      '.sonagi-consent-cat{padding:18px 0;border-bottom:1px solid #ede8e2}' +
      '.sonagi-consent-cat:last-child{border-bottom:0}' +
      '.sonagi-consent-cat-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:6px}' +
      '.sonagi-consent-cat-name{font-size:14px;font-weight:500;color:#2c2c2c;margin:0}' +
      '.sonagi-consent-cat-desc{font-size:12px;line-height:1.55;color:#4a4036;margin:0}' +
      '.sonagi-consent-always{font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:#6b5e4a;font-weight:500}' +
      /* Toggle switch */
      '.sonagi-consent-toggle{position:relative;display:inline-block;width:44px;height:24px;flex-shrink:0}' +
      '.sonagi-consent-toggle input{opacity:0;width:0;height:0}' +
      '.sonagi-consent-slider{position:absolute;cursor:pointer;inset:0;background:#cfc8be;transition:.2s;border-radius:24px}' +
      '.sonagi-consent-slider:before{position:absolute;content:"";height:18px;width:18px;left:3px;top:3px;background:#fff;transition:.2s;border-radius:50%}' +
      '.sonagi-consent-toggle input:checked+.sonagi-consent-slider{background:#FF3E9D}' +
      '.sonagi-consent-toggle input:checked+.sonagi-consent-slider:before{transform:translateX(20px)}' +
      '.sonagi-consent-toggle input:focus-visible+.sonagi-consent-slider{outline:2px solid #FF3E9D;outline-offset:2px}' +
      '.sonagi-consent-modal-foot{padding:16px 24px 24px;display:flex;flex-wrap:wrap;gap:10px;border-top:1px solid #ede8e2;background:#FAF8F5;border-radius:0 0 8px 8px}' +
      '.sonagi-consent-modal-foot .sonagi-consent-btn{flex:1;min-width:120px}' +
      '.sonagi-consent-policy-link{font-size:12px;color:#4a4036;text-align:center;padding:6px 24px 0;margin:0}' +
      '.sonagi-consent-policy-link a{color:#FF3E9D;text-decoration:underline}' +
      /* Body lock */
      'body.sonagi-consent-modal-open{overflow:hidden}' +
      '';
    var s = document.createElement('style');
    s.id = 'sonagi-consent-styles';
    s.textContent = css;
    document.head.appendChild(s);
  }

  // ── DOM HELPERS ───────────────────────────────────────
  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) {
      for (var k in attrs) {
        if (k === 'class') n.className = attrs[k];
        else if (k === 'html') n.innerHTML = attrs[k];
        else if (k === 'onclick') n.addEventListener('click', attrs[k]);
        else n.setAttribute(k, attrs[k]);
      }
    }
    if (children) {
      for (var i = 0; i < children.length; i++) {
        var c = children[i];
        if (typeof c === 'string') n.appendChild(document.createTextNode(c));
        else if (c) n.appendChild(c);
      }
    }
    return n;
  }

  // ── BANNER ────────────────────────────────────────────
  var bannerEl = null;
  function showBanner() {
    if (bannerEl) return;
    var t = COPY[detectLang()];
    var inner = el('div', { class: 'sonagi-consent-inner' }, [
      el('div', { class: 'sonagi-consent-text' }, [
        el('h3', null, [t.title]),
        el('p', null, [t.body])
      ]),
      el('div', { class: 'sonagi-consent-actions' }, [
        el('button', { class: 'sonagi-consent-btn sonagi-consent-btn-reject', type: 'button', onclick: function(){ acceptAll(false); } }, [t.reject]),
        el('button', { class: 'sonagi-consent-link', type: 'button', onclick: openModal }, [t.customize]),
        el('button', { class: 'sonagi-consent-btn sonagi-consent-btn-accept', type: 'button', onclick: function(){ acceptAll(true); } }, [t.accept])
      ])
    ]);
    bannerEl = el('div', { id: 'sonagi-consent-banner', role: 'dialog', 'aria-modal': 'false', 'aria-labelledby': 'sonagi-consent-banner-title' }, [inner]);
    document.body.appendChild(bannerEl);
  }
  function hideBanner() {
    if (bannerEl && bannerEl.parentNode) {
      bannerEl.parentNode.removeChild(bannerEl);
    }
    bannerEl = null;
  }

  // ── MODAL ─────────────────────────────────────────────
  var modalEl = null, backdropEl = null;
  function openModal() {
    if (modalEl) return;
    var t = COPY[detectLang()];
    var current = window.SONAGI_CONSENT || defaultState();

    function makeCat(key, name, desc, locked) {
      var checkbox;
      if (locked) {
        checkbox = el('span', { class: 'sonagi-consent-always' }, [t.always]);
      } else {
        var input = el('input', { type: 'checkbox', 'data-key': key });
        if (current[key]) input.checked = true;
        var slider = el('span', { class: 'sonagi-consent-slider' });
        checkbox = el('label', { class: 'sonagi-consent-toggle' }, [input, slider]);
      }
      return el('div', { class: 'sonagi-consent-cat' }, [
        el('div', { class: 'sonagi-consent-cat-head' }, [
          el('h4', { class: 'sonagi-consent-cat-name' }, [name]),
          checkbox
        ]),
        el('p', { class: 'sonagi-consent-cat-desc' }, [desc])
      ]);
    }

    var body = el('div', { class: 'sonagi-consent-modal-body' }, [
      makeCat('necessary', t.catNecessary, t.catNecessaryDesc, true),
      makeCat('preferences', t.catPreferences, t.catPreferencesDesc, false),
      makeCat('statistics', t.catStatistics, t.catStatisticsDesc, false),
      makeCat('marketing', t.catMarketing, t.catMarketingDesc, false)
    ]);

    var foot = el('div', { class: 'sonagi-consent-modal-foot' }, [
      el('button', { class: 'sonagi-consent-btn sonagi-consent-btn-reject', type: 'button', onclick: function(){ acceptAll(false); } }, [t.reject]),
      el('button', { class: 'sonagi-consent-btn sonagi-consent-btn-accept', type: 'button', onclick: saveCustom }, [t.save])
    ]);

    var policyLink = el('p', { class: 'sonagi-consent-policy-link', html:
      t.learnMore + ' <a href="cookies.html">' + t.cookiePolicy + '</a>.'
    });

    modalEl = el('div', { id: 'sonagi-consent-modal', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'sonagi-consent-modal-title' }, [
      el('div', { class: 'sonagi-consent-modal-head' }, [
        el('h3', { id: 'sonagi-consent-modal-title' }, [t.modalTitle]),
        el('p', null, [t.modalIntro])
      ]),
      body,
      policyLink,
      foot
    ]);

    backdropEl = el('div', { id: 'sonagi-consent-backdrop' }, [modalEl]);
    // Block backdrop click from closing: explicit choice required
    backdropEl.addEventListener('click', function(e){
      if (e.target === backdropEl) {
        // Do nothing: user must pick reject, accept, or save
        e.preventDefault();
        e.stopPropagation();
      }
    });
    document.body.appendChild(backdropEl);
    document.body.classList.add('sonagi-consent-modal-open');

    // Block escape from closing: explicit choice required
    document.addEventListener('keydown', blockEscape, true);
  }
  function blockEscape(e) {
    if (e.key === 'Escape' || e.keyCode === 27) {
      e.preventDefault();
      e.stopPropagation();
    }
  }
  function closeModal() {
    if (backdropEl && backdropEl.parentNode) backdropEl.parentNode.removeChild(backdropEl);
    backdropEl = null;
    modalEl = null;
    document.body.classList.remove('sonagi-consent-modal-open');
    document.removeEventListener('keydown', blockEscape, true);
  }

  // ── ACTIONS ───────────────────────────────────────────
  function acceptAll(value) {
    var s = defaultState();
    s.preferences = !!value;
    s.statistics = !!value;
    s.marketing = !!value;
    saveState(s);
    closeModal();
    hideBanner();
  }
  function saveCustom() {
    var s = defaultState();
    if (modalEl) {
      var inputs = modalEl.querySelectorAll('input[type=checkbox][data-key]');
      for (var i = 0; i < inputs.length; i++) {
        var k = inputs[i].getAttribute('data-key');
        s[k] = !!inputs[i].checked;
      }
    }
    saveState(s);
    closeModal();
    hideBanner();
  }

  // ── PUBLIC API ────────────────────────────────────────
  window.sonagiOpenCookieSettings = function() {
    injectStyles();
    openModal();
  };
  window.sonagiGetConsent = function() {
    return Object.assign({}, window.SONAGI_CONSENT);
  };
  window.sonagiResetConsent = function() {
    try { localStorage.removeItem(STORAGE_KEY); } catch(e) {}
    window.SONAGI_CONSENT = defaultState();
    closeModal();
    hideBanner();
    showBanner();
  };

  // ── INIT ──────────────────────────────────────────────
  function init() {
    injectStyles();
    var existing = loadState();
    if (existing) {
      window.SONAGI_CONSENT = existing;
      // Fire event so any analytics listeners can lazy-load
      document.dispatchEvent(new CustomEvent('sonagi-consent-changed', { detail: existing }));
      return;
    }
    showBanner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
