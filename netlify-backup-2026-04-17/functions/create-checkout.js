/**
 * Sonagi Beauty — Stripe Checkout session creator
 *
 * Environment variables required:
 *   STRIPE_SECRET_KEY   — sk_test_... or sk_live_...
 *   SITE_URL            — https://sonagibeauty.com (or Netlify deploy URL)
 *   SHOP_OPEN           — "true" to enable live checkout, anything else = coming soon
 *
 * Usage: POST /.netlify/functions/create-checkout
 *   Body: { items: [{ price: "price_xxx", quantity: 1 }, ...] }
 */

const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };

  // Handle CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers, body: "" };
  }

  if (event.httpMethod !== "POST") {
    return { statusCode: 405, headers, body: JSON.stringify({ error: "Method not allowed" }) };
  }

  // ── SHOP_OPEN flag: if not "true", return coming-soon response ──
  if (process.env.SHOP_OPEN !== "true") {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        coming_soon: true,
        message: "La boutique ouvre prochainement. Inscris-toi à la newsletter pour être notifiée.",
      }),
    };
  }

  try {
    const { items } = JSON.parse(event.body || "{}");

    if (!items || !items.length) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: "No items provided" }) };
    }

    const siteUrl = process.env.SITE_URL || "https://sonagibeauty.com";

    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card"],
      // Apple Pay & Google Pay are auto-enabled when "card" is listed
      // and the Stripe Dashboard has them activated
      line_items: items.map((item) => ({
        price: item.price,       // Stripe Price ID (e.g. price_1Abc...)
        quantity: item.quantity || 1,
      })),
      shipping_address_collection: {
        allowed_countries: ["FR", "BE", "CH", "LU", "DE", "NL", "ES", "IT", "PT", "AT"],
      },
      success_url: `${siteUrl}/confirmation.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${siteUrl}/panier.html?cancelled=true`,
      locale: "fr",
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ sessionId: session.id, url: session.url }),
    };
  } catch (err) {
    console.error("Stripe error:", err.message);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: err.message }),
    };
  }
};
