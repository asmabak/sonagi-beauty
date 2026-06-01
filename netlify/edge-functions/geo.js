// Sonagi geo language autodetect, Netlify Edge Function (Deno).
// Injects <meta name="x-country" content="XX"> into every HTML response so
// the client-side language picker (sonagi-app.js _detectLang) can default to
// fr for francophone visitors.
//
// Netlify Edge gives us context.geo.country.code (ISO 3166-1 alpha-2) without
// needing Cloudflare. If the visitor sets the sonagi_lang cookie manually
// (FR/EN buttons), the client always honours that over geo.

export default async (request, context) => {
  const response = await context.next();
  const ct = response.headers.get('content-type') || '';
  if (!ct.includes('text/html')) return response;

  const country = (context.geo && context.geo.country && context.geo.country.code) || '';
  if (!country) return response;

  // Inject meta tag right after <head> (case-insensitive, first occurrence).
  const html = await response.text();
  const tag = `<meta name="x-country" content="${country}">`;
  const out = html.replace(/<head([^>]*)>/i, `<head$1>\n${tag}`);

  return new Response(out, {
    status: response.status,
    headers: response.headers,
  });
};

export const config = { path: '/*' };
