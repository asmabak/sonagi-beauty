/* ══════════════════════════════════════════════════════
   SONAGI ANALYTICS LOADER (consent-gated)

   Loads Google Analytics 4 (statistics consent) and Meta Pixel (marketing consent)
   ONLY after the visitor has consented in the Sonagi cookie banner.

   To activate, set the IDs in window.SONAGI_ANALYTICS_CONFIG before this script runs:

     <script>
       window.SONAGI_ANALYTICS_CONFIG = {
         ga4:       'G-XXXXXXXXXX',  // Google Analytics 4 Measurement ID, or null
         metaPixel: '1234567890123', // Meta Pixel ID, or null
         googleAds: null              // optional Google Ads conversion ID
       };
     </script>
     <script src="js/sonagi-analytics.js" defer></script>

   While the IDs stay null, this file loads NOTHING. CNIL-safe by default.
   ══════════════════════════════════════════════════════ */
(function(){
  'use strict';

  /* ╔═══════════════════════════════════════════════════════╗
     ║  EDIT HERE to activate analytics. While both are null,
     ║  no third-party script ever loads. CNIL-safe by default.
     ║  Both will only fire AFTER user clicks "Accepter" in the
     ║  consent banner (statistics for GA4, marketing for Meta).
     ╚═══════════════════════════════════════════════════════╝ */
  var DEFAULT_CONFIG = {
    ga4:       null,  // e.g. 'G-XXXXXXXXXX'   : Google Analytics 4 Measurement ID
    metaPixel: null,  // e.g. '1234567890123'  : Meta Pixel ID
    googleAds: null   // e.g. 'AW-1234567890'  : Google Ads conversion ID (optional)
  };

  var cfg = window.SONAGI_ANALYTICS_CONFIG || DEFAULT_CONFIG;
  var loadedGA = false;
  var loadedMeta = false;
  var loadedAds = false;

  function consent(){
    return (window.SONAGI_CONSENT) || (function(){
      try { return JSON.parse(localStorage.getItem('sonagi_consent_v1') || 'null'); }
      catch(e){ return null; }
    })() || {};
  }

  function loadGA4(){
    if (loadedGA || !cfg.ga4) return;
    loadedGA = true;
    var id = cfg.ga4;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){ window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id, {
      anonymize_ip: true,
      cookie_flags: 'SameSite=None;Secure'
    });
  }

  function loadMetaPixel(){
    if (loadedMeta || !cfg.metaPixel) return;
    loadedMeta = true;
    var id = cfg.metaPixel;
    /* Meta Pixel base code (official, https://developers.facebook.com/docs/meta-pixel/get-started). */
    !function(f,b,e,v,n,t,s){
      if(f.fbq) return; n=f.fbq=function(){
        n.callMethod ? n.callMethod.apply(n,arguments) : n.queue.push(arguments);
      };
      if(!f._fbq) f._fbq=n; n.push=n; n.loaded=!0; n.version='2.0';
      n.queue=[]; t=b.createElement(e); t.async=!0;
      t.src=v; s=b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t,s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', id);
    window.fbq('track', 'PageView');
  }

  function loadGoogleAds(){
    if (loadedAds || !cfg.googleAds) return;
    loadedAds = true;
    var id = cfg.googleAds;
    if (!loadedGA) {
      // Google Ads piggybacks on gtag; load gtag.js if GA4 isn't already loaded
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function(){ window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
    }
    window.gtag('config', id);
  }

  function applyConsent(){
    var c = consent();
    if (c.statistics) loadGA4();
    if (c.marketing)  { loadMetaPixel(); loadGoogleAds(); }
  }

  /* Run once on page load if consent already granted from a previous visit. */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyConsent);
  } else {
    applyConsent();
  }

  /* Re-evaluate when the user changes their consent in the banner. */
  document.addEventListener('sonagi-consent-changed', function(){
    applyConsent();
  });

  /* Public hook so future code can fire custom events behind the same gate. */
  window.sonagiTrack = function(eventName, params){
    var c = consent();
    if (window.gtag && c.statistics) window.gtag('event', eventName, params || {});
    if (window.fbq && c.marketing)   window.fbq('track', eventName, params || {});
  };
})();
