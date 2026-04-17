/* ══════════════════════════════════════════════════════
   SONAGI CATALOG — product SKU → Stripe price ID
   ──────────────────────────────────────────────────────
   To wire a product for purchase:
   1. In Stripe Dashboard (Test mode), create the product + price.
   2. Copy the price ID (starts with "price_").
   3. Add an entry below.
   See STRIPE-SETUP.md for the full setup walk-through.
   ══════════════════════════════════════════════════════ */
window.SONAGI_CATALOG = {
  // sku                       priceId (test or live)        amount  currency  display name
  // EXAMPLE — replace with your real Stripe price IDs:
  // "cosrx-snail-mucin"     : { priceId: "price_REPLACE_ME", amount: 28.00, currency: "EUR", brand: "COSRX",            name: "Snail 96 Mucin Power Essence" },
  // "anua-heartleaf-toner"  : { priceId: "price_REPLACE_ME", amount: 24.00, currency: "EUR", brand: "Anua",             name: "Heartleaf 77% Toner" },
  // "boj-glow-serum"        : { priceId: "price_REPLACE_ME", amount: 17.00, currency: "EUR", brand: "Beauty of Joseon", name: "Glow Serum Propolis + Niacinamide" },
  // "boj-relief-sun-spf50"  : { priceId: "price_REPLACE_ME", amount: 18.00, currency: "EUR", brand: "Beauty of Joseon", name: "Relief Sun Rice + Probiotic SPF50+" },
  // "laneige-lip-mask"      : { priceId: "price_REPLACE_ME", amount: 22.00, currency: "EUR", brand: "Laneige",          name: "Lip Sleeping Mask Berry" },
};

/** Lookup helper — returns { priceId, amount, currency, brand, name } or null. */
window.SONAGI_CATALOG_GET = function (sku) {
  return (window.SONAGI_CATALOG && window.SONAGI_CATALOG[sku]) || null;
};
