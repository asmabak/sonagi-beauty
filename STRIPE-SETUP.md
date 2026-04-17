# Stripe Setup — Sonagi Beauty

End-to-end Stripe wiring for sonagibeauty.com. **No bank account required for steps 1–6** (test mode is free and full-feature). When you're ready to accept real money, jump to step 7.

---

## What's already wired in code

| Piece | Location | Status |
|---|---|---|
| Stripe Checkout function | `netlify/functions/create-checkout.js` | ✅ Live, gated by `SHOP_OPEN` env var |
| Cart persistence (localStorage) | `files/js/sonagi-cart.js` | ✅ Survives page navigation |
| Product catalog | `files/js/sonagi-catalog.js` | ⚠️ Fill in your Stripe price IDs |
| Checkout button handler | `window.SonagiCart.checkout()` | ✅ Reads cart, calls Stripe |
| Cart badge auto-sync | All pages with `.cart-badge` | ✅ |

---

## Step 1 — Create your Stripe account (free, no bank yet)

1. Go to **https://dashboard.stripe.com/register** and sign up with `contact@sonagibeauty.com`.
2. After signup you land in **Test mode** automatically (toggle is top-right of the dashboard).
3. **You can use test mode forever without entering a bank account.** Activation is only required to switch to live mode.

> 💳 *Reminder: I (Claude) won't sign up or enter any payment info on your behalf — that's always your call.*

---

## Step 2 — Get your Stripe test keys

1. Stripe Dashboard → top-right toggle **must read "Test mode"** (orange badge).
2. **Developers → API keys**.
3. Copy:
   - **Publishable key** → `pk_test_...` (used by the browser if you ever embed Stripe.js — currently not needed because we use Checkout redirect)
   - **Secret key** → `sk_test_...` (used by the Netlify function — keep this private, never commit it)

---

## Step 3 — Create your products in Stripe (Test mode)

For each Korean product Sonagi resells:

1. Stripe Dashboard → **Product catalog → + Add product**.
2. Fill: **Name** (e.g. "COSRX Snail 96 Mucin Power Essence"), **Description**, **Image**.
3. Pricing: **One-time**, **EUR**, set the price (e.g. 28.00).
4. Click **Save product** → on the product page, copy the **API ID for the price** (looks like `price_1OAbCdEfGh...`).

Repeat for every SKU you want to sell. Test-mode products don't charge anyone — perfect for full integration testing.

---

## Step 4 — Wire the catalog

Open `files/js/sonagi-catalog.js`. For each product, add an entry — the SKU is your own internal slug:

```js
window.SONAGI_CATALOG = {
  "cosrx-snail-mucin"     : { priceId: "price_1OAbCdEfGh...", amount: 28.00, currency: "EUR", brand: "COSRX",            name: "Snail 96 Mucin Power Essence" },
  "anua-heartleaf-toner"  : { priceId: "price_1OAbCdEfGh...", amount: 24.00, currency: "EUR", brand: "Anua",             name: "Heartleaf 77% Toner" },
  "boj-glow-serum"        : { priceId: "price_1OAbCdEfGh...", amount: 17.00, currency: "EUR", brand: "Beauty of Joseon", name: "Glow Serum Propolis + Niacinamide" },
  // ...
};
```

---

## Step 5 — Add three Netlify environment variables

Netlify Dashboard → **Site → Site configuration → Environment variables → Add a variable**:

| Key | Value | Notes |
|---|---|---|
| `STRIPE_SECRET_KEY` | `sk_test_...` (from step 2) | Use the **test** key first |
| `SITE_URL` | `https://sonagibeauty.com` | Or your Netlify URL while domain is pending |
| `SHOP_OPEN` | `true` | Without this the function returns "Bientôt disponible" |

After saving, **trigger a redeploy** (Deploys → Trigger deploy → Deploy site).

---

## Step 6 — Test the end-to-end flow

On the live site (or `netlify dev` locally):

1. Add a product to the cart (any product whose SKU is in `sonagi-catalog.js` with a real `price_xxx`).
2. Open `/panier.html` → click **Confirmer ma commande**.
3. You should be redirected to Stripe Checkout (URL starts with `checkout.stripe.com`).
4. Use Stripe's official test card:
   - Card: `4242 4242 4242 4242`
   - Expiry: any future date (e.g. `12/30`)
   - CVC: any 3 digits (e.g. `123`)
   - ZIP/postal: any (e.g. `75001`)
5. After payment success → you land on `/confirmation.html?session_id=...`.
6. In Stripe Dashboard → **Payments** you'll see the test charge appear.

**Other useful test cards:**

| Card number | What happens |
|---|---|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 9995` | Declined — insufficient funds |
| `4000 0025 0000 3155` | 3D Secure authentication required |
| `4000 0000 0000 0002` | Generic decline |

Full list: https://docs.stripe.com/testing

---

## Step 7 — Going live (when you have a bank account)

1. Open a French business bank account (Qonto, Shine, Revolut Business, BNP Pro all work for Stripe). You'll need your SIRET and ID.
2. Stripe Dashboard → **toggle to Live mode** (top-right) → **Activate account** wizard:
   - Business details (legal entity, SIRET, address)
   - Bank account IBAN
   - Owner ID verification
3. Once activated, **Developers → API keys** in *Live mode* → copy the **`sk_live_...`** secret key.
4. Re-create your products in **Live mode** (test-mode products don't carry over) — then copy each `price_live_...` ID.
5. Update `files/js/sonagi-catalog.js` with the live price IDs.
6. Update Netlify env var `STRIPE_SECRET_KEY` to the `sk_live_...` value → redeploy.
7. Verify with a real €1 test purchase you can refund yourself.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Button shows "Bientôt disponible" | `SHOP_OPEN` env var not set or not `true` | Set it on Netlify and redeploy |
| Button shows "Catalogue produits non configuré" | All cart SKUs are missing a `priceId` (or still `price_REPLACE_ME`) | Edit `files/js/sonagi-catalog.js` |
| `Erreur : No such price: price_xxx` | Price ID is from a different mode (test vs live mismatch) or doesn't exist | Re-copy from Stripe Dashboard, confirm mode |
| `Erreur : Invalid API Key` | Wrong key or test/live mismatch | Re-copy from Stripe → Developers → API keys |
| Cart empty after page navigation | localStorage disabled (private browsing) | This is browser policy; persist works in normal browsing |
| Checkout button does nothing | `js/sonagi-cart.js` not loaded on that page | Confirm `<script src="js/sonagi-cart.js">` is in `<head>` |

---

## Quick reference

- **Stripe test cards** → https://docs.stripe.com/testing
- **Stripe Dashboard** → https://dashboard.stripe.com
- **Netlify env vars** → Site → Site configuration → Environment variables
- **Toggle Test ↔ Live** → top-right of every Stripe page
