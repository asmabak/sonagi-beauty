/**
 * Sonagi — send-protocol
 *
 * POST /.netlify/functions/send-protocol
 *
 * Receives the diagnostic payload returned by `quiz-advisor`, plus the
 * user's name + email + answers, and sends a designed transactional email
 * via Resend.
 *
 * Environment variables:
 *   RESEND_API_KEY  — Resend API key (Dashboard → API Keys)
 *
 * Optional environment variables:
 *   FROM_EMAIL      — defaults to "Sonagi <protocole@sonagibeauty.com>"
 *   REPLY_TO_EMAIL  — defaults to "contact@sonagibeauty.com"
 *
 * Behaviour when RESEND_API_KEY is NOT configured:
 *   Returns 200 with { skipped: true, reason: "..." } so the front-end
 *   does not block on a missing dev configuration.
 *
 * Expected request body shape:
 *   {
 *     name:       "Marie",
 *     email:      "marie@example.fr",
 *     diagnostic: { ... },          // shape returned by quiz-advisor.js
 *     answers:    { ... },          // raw quiz answers
 *     locale:     "fr"
 *   }
 */

"use strict";

const { renderProtocolEmail } = require("../../files/email/protocol-template");

const FROM_EMAIL = process.env.FROM_EMAIL || "Sonagi <protocole@sonagibeauty.com>";
const REPLY_TO_EMAIL = process.env.REPLY_TO_EMAIL || "contact@sonagibeauty.com";

// RFC 5322-lite — good enough for client-side validation, server is generous.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function jsonResponse(statusCode, body, extraHeaders = {}) {
  return {
    statusCode,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Content-Type": "application/json; charset=utf-8",
      ...extraHeaders,
    },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  // CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return jsonResponse(200, { ok: true });
  }
  if (event.httpMethod !== "POST") {
    return jsonResponse(405, { ok: false, error: "Method not allowed" });
  }

  // Parse body
  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch (err) {
    return jsonResponse(400, { ok: false, error: "Invalid JSON body" });
  }

  // Validate
  const { name, email, diagnostic } = payload;
  if (!name || typeof name !== "string") {
    return jsonResponse(400, { ok: false, error: "Missing 'name'" });
  }
  if (!email || typeof email !== "string" || !EMAIL_RE.test(email)) {
    return jsonResponse(400, { ok: false, error: "Missing or invalid 'email'" });
  }
  if (!diagnostic || typeof diagnostic !== "object") {
    return jsonResponse(400, { ok: false, error: "Missing 'diagnostic'" });
  }

  // Soft-fail when Resend isn't wired up yet
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.warn("[send-protocol] RESEND_API_KEY not set — skipping send.");
    return jsonResponse(200, {
      ok: true,
      skipped: true,
      reason: "RESEND_API_KEY not configured",
    });
  }

  // Render the email
  let rendered;
  try {
    rendered = renderProtocolEmail(payload);
  } catch (err) {
    console.error("[send-protocol] render error:", err && err.message);
    return jsonResponse(500, { ok: false, error: "Failed to render email" });
  }
  const { subject, html, text } = rendered;

  // Send via Resend SDK
  let Resend;
  try {
    ({ Resend } = require("resend"));
  } catch (err) {
    console.error(
      "[send-protocol] 'resend' package not installed. Run `npm install resend` then redeploy."
    );
    return jsonResponse(500, {
      ok: false,
      error: "Resend SDK not installed (npm install resend)",
    });
  }

  const resend = new Resend(apiKey);

  try {
    const { data, error } = await resend.emails.send({
      from: FROM_EMAIL,
      to: [email],
      reply_to: REPLY_TO_EMAIL,
      subject,
      html,
      text,
      tags: [
        { name: "type", value: "protocol" },
        { name: "locale", value: String(payload.locale || "fr") },
      ],
    });

    if (error) {
      console.error("[send-protocol] Resend error:", error);
      return jsonResponse(502, {
        ok: false,
        error: error.message || "Resend rejected the message",
      });
    }

    return jsonResponse(200, { ok: true, id: data && data.id });
  } catch (err) {
    console.error("[send-protocol] unexpected error:", err && err.message);
    return jsonResponse(500, {
      ok: false,
      error: "Unexpected error sending the email",
    });
  }
};
