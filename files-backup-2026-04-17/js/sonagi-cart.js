/* ══════════════════════════════════════════════════════
   SONAGI CART + CHECKOUT — single source of truth
   ──────────────────────────────────────────────────────
   Persists cart in localStorage so it survives page navigation.
   Backwards compatible: if a page already has a `cartItems` global
   (the legacy in-memory array), this module mirrors it.
   ══════════════════════════════════════════════════════ */
(function () {
  var STORAGE_KEY = "sonagi_cart_v1";

  function read() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]") || []; }
    catch (e) { return []; }
  }
  function write(items) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(items || [])); } catch (e) {}
    if (typeof window.cartItems !== "undefined") window.cartItems = items;
    if (typeof window.renderCart === "function") { try { window.renderCart(); } catch (e) {} }
    syncBadge(items);
  }
  function syncBadge(items) {
    var badges = document.querySelectorAll(".cart-badge, #cart-badge");
    var count = (items || []).reduce(function (n, it) { return n + (it.qty || 1); }, 0);
    badges.forEach(function (b) { b.textContent = String(count); });
  }

  var SonagiCart = {
    items: function () { return read(); },

    add: function (item) {
      // item: { sku, brand, name, price (display string), qty }
      var items = read();
      var i = items.findIndex(function (x) { return x.sku && x.sku === item.sku; });
      if (i >= 0) { items[i].qty = (items[i].qty || 1) + (item.qty || 1); }
      else { items.push(Object.assign({ qty: 1 }, item)); }
      write(items);
      return items;
    },

    remove: function (skuOrIndex) {
      var items = read();
      if (typeof skuOrIndex === "number") items.splice(skuOrIndex, 1);
      else items = items.filter(function (it) { return it.sku !== skuOrIndex; });
      write(items);
      return items;
    },

    clear: function () { write([]); },

    setQty: function (sku, qty) {
      var items = read();
      var i = items.findIndex(function (x) { return x.sku === sku; });
      if (i >= 0) { if (qty <= 0) items.splice(i, 1); else items[i].qty = qty; }
      write(items);
      return items;
    },

    /** Hydrate from a legacy in-memory `cartItems` array if present. */
    hydrateLegacy: function () {
      if (typeof window.cartItems !== "undefined" && Array.isArray(window.cartItems) && window.cartItems.length) {
        var existing = read();
        if (!existing.length) write(window.cartItems);
      }
      window.cartItems = read();
    },

    /** Build Stripe line items by joining cart with SONAGI_CATALOG. */
    toStripeLineItems: function () {
      var items = read();
      var catalog = window.SONAGI_CATALOG || {};
      return items
        .map(function (it) {
          var entry = catalog[it.sku];
          if (!entry || !entry.priceId || /REPLACE/i.test(entry.priceId)) return null;
          return { price: entry.priceId, quantity: it.qty || 1 };
        })
        .filter(Boolean);
    },

    /** Trigger Stripe Checkout. Call from a button onclick. */
    checkout: function (opts) {
      opts = opts || {};
      var btn = document.getElementById(opts.btnId || "checkout-btn");
      var msg = document.getElementById(opts.msgId || "checkout-msg");

      function showMsg(html) {
        if (!msg) return;
        msg.style.display = "block";
        msg.innerHTML = html;
      }

      var lineItems = SonagiCart.toStripeLineItems();
      if (!lineItems.length) {
        if (btn) { btn.disabled = false; }
        showMsg(
          "⚠️ <strong>Catalogue produits non configuré</strong><br>" +
          "Ajoutez vos Stripe price IDs dans <code>js/sonagi-catalog.js</code>.<br>" +
          "Guide complet : <code>STRIPE-SETUP.md</code>."
        );
        return;
      }

      if (btn) { btn.disabled = true; btn.dataset.origText = btn.textContent; btn.textContent = "Chargement…"; }

      fetch("/.netlify/functions/create-checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items: lineItems })
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.coming_soon) {
            showMsg(
              "🌸 <strong>Bientôt disponible</strong><br>" +
              "La boutique Sonagi ouvre prochainement.<br>" +
              "Inscris-toi à la newsletter pour être notifiée."
            );
            if (btn) { btn.textContent = "Bientôt disponible"; }
          } else if (data.url) {
            window.location.href = data.url;
          } else {
            if (btn) { btn.disabled = false; btn.textContent = btn.dataset.origText || "Réessayer"; }
            showMsg("Erreur : " + (data.error || "Réessaye dans un instant."));
          }
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = btn.dataset.origText || "Réessayer"; }
          showMsg("Connexion impossible. Réessaye dans un instant.");
        });
    }
  };

  window.SonagiCart = SonagiCart;
  // Legacy compatibility — preserves any pre-existing handleCheckout call sites
  window.handleCheckout = function () { SonagiCart.checkout(); };

  document.addEventListener("DOMContentLoaded", function () {
    SonagiCart.hydrateLegacy();
    syncBadge(read());
  });
})();
