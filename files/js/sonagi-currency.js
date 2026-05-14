/* ══════════════════════════════════════════════════════
   SONAGI CURRENCY · auto-convert EUR prices to the visitor's local currency.
   - Detects country via ipapi.co (cached by geo script in localStorage 'sonagi_country')
   - Falls back to navigator.language hint if API unavailable
   - Fetches FX rates daily from open.er-api.com (free, no key, ~1500 req/mo limit)
   - Caches rates in localStorage (24h)
   - Scans .prod-price / .evt-price / #cart-total / [data-price-eur]
   - Stores original EUR value in data-eur on first run so re-runs are idempotent
   - Always exposes the original EUR amount for cart math (window.sonagiCurrency.toEur)
   ══════════════════════════════════════════════════════ */
(function(){
  'use strict';

  // Country → currency mapping (only listing where conversion makes sense)
  var COUNTRY_CURRENCY = {
    GB:'GBP', US:'USD', CA:'CAD', CH:'CHF', AU:'AUD', NZ:'NZD',
    JP:'JPY', KR:'KRW', CN:'CNY', HK:'HKD', SG:'SGD', TW:'TWD',
    AE:'AED', SA:'SAR', IL:'ILS', TR:'TRY',
    NO:'NOK', SE:'SEK', DK:'DKK', PL:'PLN', CZ:'CZK', HU:'HUF', RO:'RON', BG:'BGN',
    RU:'RUB', UA:'UAH',
    BR:'BRL', MX:'MXN', AR:'ARS', CL:'CLP', CO:'COP', PE:'PEN',
    IN:'INR', TH:'THB', VN:'VND', ID:'IDR', PH:'PHP', MY:'MYR',
    ZA:'ZAR', EG:'EGP', NG:'NGN', KE:'KES',
    MA:'MAD', TN:'TND', DZ:'DZD'
  };

  // Currency symbols + decimals
  var CURRENCY_INFO = {
    EUR:{ sym:'€',  dec:2, post:true,  fr_post:true  }, // FR: 38,00 €  EN: €38.00
    GBP:{ sym:'£',  dec:2, post:false, fr_post:false },
    USD:{ sym:'$',  dec:2, post:false, fr_post:false },
    CAD:{ sym:'C$', dec:2, post:false, fr_post:false },
    CHF:{ sym:'CHF',dec:2, post:true,  fr_post:true  },
    AUD:{ sym:'A$', dec:2, post:false, fr_post:false },
    NZD:{ sym:'NZ$',dec:2, post:false, fr_post:false },
    JPY:{ sym:'¥',  dec:0, post:false, fr_post:false },
    KRW:{ sym:'₩',  dec:0, post:false, fr_post:false },
    CNY:{ sym:'¥',  dec:2, post:false, fr_post:false },
    HKD:{ sym:'HK$',dec:2, post:false, fr_post:false },
    SGD:{ sym:'S$', dec:2, post:false, fr_post:false },
    TWD:{ sym:'NT$',dec:0, post:false, fr_post:false },
    AED:{ sym:'AED',dec:2, post:true,  fr_post:true  },
    SAR:{ sym:'SAR',dec:2, post:true,  fr_post:true  },
    ILS:{ sym:'₪',  dec:2, post:false, fr_post:false },
    TRY:{ sym:'₺',  dec:2, post:false, fr_post:false },
    NOK:{ sym:'kr', dec:2, post:true,  fr_post:true  },
    SEK:{ sym:'kr', dec:2, post:true,  fr_post:true  },
    DKK:{ sym:'kr', dec:2, post:true,  fr_post:true  },
    PLN:{ sym:'zł', dec:2, post:true,  fr_post:true  },
    CZK:{ sym:'Kč', dec:0, post:true,  fr_post:true  },
    HUF:{ sym:'Ft', dec:0, post:true,  fr_post:true  },
    RON:{ sym:'lei',dec:2, post:true,  fr_post:true  },
    BGN:{ sym:'лв', dec:2, post:true,  fr_post:true  },
    RUB:{ sym:'₽',  dec:0, post:true,  fr_post:true  },
    UAH:{ sym:'₴',  dec:2, post:false, fr_post:false },
    BRL:{ sym:'R$', dec:2, post:false, fr_post:false },
    MXN:{ sym:'$',  dec:2, post:false, fr_post:false },
    ARS:{ sym:'$',  dec:2, post:false, fr_post:false },
    CLP:{ sym:'$',  dec:0, post:false, fr_post:false },
    COP:{ sym:'$',  dec:0, post:false, fr_post:false },
    PEN:{ sym:'S/', dec:2, post:false, fr_post:false },
    INR:{ sym:'₹',  dec:0, post:false, fr_post:false },
    THB:{ sym:'฿',  dec:2, post:false, fr_post:false },
    VND:{ sym:'₫',  dec:0, post:true,  fr_post:true  },
    IDR:{ sym:'Rp', dec:0, post:false, fr_post:false },
    PHP:{ sym:'₱',  dec:2, post:false, fr_post:false },
    MYR:{ sym:'RM', dec:2, post:false, fr_post:false },
    ZAR:{ sym:'R',  dec:2, post:false, fr_post:false },
    EGP:{ sym:'EGP',dec:2, post:true,  fr_post:true  },
    NGN:{ sym:'₦',  dec:0, post:false, fr_post:false },
    KES:{ sym:'KSh',dec:0, post:false, fr_post:false },
    MAD:{ sym:'MAD',dec:2, post:true,  fr_post:true  },
    TND:{ sym:'DT', dec:3, post:true,  fr_post:true  },
    DZD:{ sym:'DA', dec:2, post:true,  fr_post:true  }
  };

  var RATE_CACHE_KEY = 'sonagi_fx_rates_v1';
  var COUNTRY_KEY    = 'sonagi_country';
  var RATE_TTL_MS    = 24 * 60 * 60 * 1000;
  var RATES_URL      = 'https://open.er-api.com/v6/latest/EUR';

  function getCountry(){
    try { return localStorage.getItem(COUNTRY_KEY); } catch(e){ return null; }
  }
  function setCountry(c){
    try { localStorage.setItem(COUNTRY_KEY, c); } catch(e){}
  }

  // Currency override (user can pick from footer in future). For now: country-driven.
  function getUserCurrencyChoice(){
    try { return localStorage.getItem('sonagi_currency'); } catch(e){ return null; }
  }

  // Detect the visitor's currency (from country, or saved choice, default EUR).
  function detectCurrency(callback){
    var manual = getUserCurrencyChoice();
    if (manual && CURRENCY_INFO[manual]) { callback(manual); return; }

    var country = getCountry();
    if (country) { callback(currencyFor(country)); return; }

    // Fetch country once, cache it (the lang script also fetches; this is opportunistic)
    fetch('https://ipapi.co/country/', {cache:'force-cache'})
      .then(function(r){ return r.ok ? r.text() : null; })
      .then(function(c){
        if (c) { c = c.trim().toUpperCase(); setCountry(c); callback(currencyFor(c)); }
        else   { callback('EUR'); }
      })
      .catch(function(){ callback('EUR'); });
  }
  function currencyFor(country){
    if (!country) return 'EUR';
    if (COUNTRY_CURRENCY[country]) return COUNTRY_CURRENCY[country];
    return 'EUR'; // EU + unknown = EUR
  }

  // FX rate fetcher with 24h cache.
  function getRate(target, callback){
    if (target === 'EUR') { callback(1); return; }
    var cached = null;
    try { cached = JSON.parse(localStorage.getItem(RATE_CACHE_KEY) || 'null'); } catch(e){}
    var now = Date.now();
    if (cached && cached.ts && (now - cached.ts) < RATE_TTL_MS && cached.rates && cached.rates[target]) {
      callback(cached.rates[target]); return;
    }
    fetch(RATES_URL)
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(json){
        if (!json || !json.rates) { callback(null); return; }
        var payload = { ts: now, rates: json.rates };
        try { localStorage.setItem(RATE_CACHE_KEY, JSON.stringify(payload)); } catch(e){}
        callback(json.rates[target] || null);
      })
      .catch(function(){ callback(null); });
  }

  // Format a number per currency + lang (FR vs EN number formatting).
  function format(amount, currency, lang){
    var info = CURRENCY_INFO[currency] || CURRENCY_INFO.EUR;
    var dec = info.dec;
    var rounded;
    if (dec === 0) rounded = Math.round(amount);
    else rounded = Math.round(amount * Math.pow(10, dec)) / Math.pow(10, dec);

    var fixed = rounded.toFixed(dec);
    var parts = fixed.split('.');
    var intPart = parts[0];
    var decPart = parts[1] || '';

    // Thousands separator
    var thouSep = (lang === 'fr') ? ' ' : ',';
    var decSep  = (lang === 'fr') ? ',' : '.';
    intPart = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, thouSep);
    var num = decPart ? (intPart + decSep + decPart) : intPart;

    var post = (lang === 'fr') ? info.fr_post : info.post;
    var sym = info.sym;
    if (post) return num + ' ' + sym;
    return sym + num;
  }

  // Parse the EUR amount from an existing price string like "38,00 €" or "€38.00" or "1 250,00 €".
  function parseEur(text){
    if (!text) return null;
    // strip everything except digits, dot, comma, minus
    var clean = String(text).replace(/[^\d,.\-]/g, '').trim();
    if (!clean) return null;
    // detect comma vs dot decimal
    if (clean.indexOf(',') > -1 && clean.lastIndexOf(',') > clean.lastIndexOf('.')) {
      // FR format: "1 250,00" → "1250.00"
      clean = clean.replace(/\./g,'').replace(',', '.');
    } else {
      // EN format: "1,250.00" → "1250.00"
      clean = clean.replace(/,/g,'');
    }
    var n = parseFloat(clean);
    return isNaN(n) ? null : n;
  }

  // Find every priceable element on the page.
  function priceElements(){
    var sels = [
      '.prod-price', '.evt-price', '.cart-line-price', '#cart-total',
      '.cart-line-total', '.related-price', '[data-price-eur]'
    ];
    return document.querySelectorAll(sels.join(','));
  }

  function getLang(){
    try { return localStorage.getItem('sonagi_lang') || 'fr'; } catch(e){ return 'fr'; }
  }

  // Apply conversion to all price elements on the page.
  function applyPrices(currency, rate){
    var lang = getLang();
    var els = priceElements();
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var eur = el.getAttribute('data-eur');
      if (eur == null) {
        // First run: store the EUR amount.
        var parsed = parseEur(el.textContent);
        if (parsed == null) continue;
        eur = String(parsed);
        el.setAttribute('data-eur', eur);
      }
      var eurNum = parseFloat(eur);
      var converted = (currency === 'EUR') ? eurNum : (eurNum * rate);
      el.textContent = format(converted, currency, lang);
    }
  }

  // Add a small currency indicator to the footer, near the lang pills.
  function addCurrencyBadge(currency){
    if (!currency || currency === 'EUR') return;
    var langRow = document.querySelector('.footer-lang');
    if (!langRow || document.getElementById('footer-currency-badge')) return;
    var badge = document.createElement('span');
    badge.id = 'footer-currency-badge';
    badge.textContent = '· ' + currency;
    badge.style.cssText = 'font-size:10px;color:rgba(255,255,255,.6);letter-spacing:1.5px;align-self:center;margin-left:4px';
    badge.title = 'Conversion automatique depuis EUR (taux indicatif)';
    langRow.appendChild(badge);
  }

  function run(){
    detectCurrency(function(currency){
      window.sonagiCurrency = window.sonagiCurrency || {};
      window.sonagiCurrency.code = currency;
      window.sonagiCurrency.toEur = function(el){
        var v = el && el.getAttribute('data-eur');
        return v ? parseFloat(v) : null;
      };
      getRate(currency, function(rate){
        if (currency !== 'EUR' && (!rate || rate <= 0)) {
          // Fallback: leave prices in EUR if rate fetch failed
          applyPrices('EUR', 1);
          return;
        }
        applyPrices(currency, rate || 1);
        addCurrencyBadge(currency);
      });
    });
  }

  // Re-run when language toggles (number formatting differs FR vs EN)
  document.addEventListener('click', function(e){
    var t = e.target;
    if (t && t.id && (t.id === 'fbtn-fr' || t.id === 'fbtn-en' || t.id === 'btn-fr' || t.id === 'btn-en')) {
      // Wait a tick for setLang() to update LANG, then re-format prices
      setTimeout(run, 50);
    }
  }, true);

  // Re-run if catalogue/cart inserts new prices later
  window.sonagiRefreshCurrency = run;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
