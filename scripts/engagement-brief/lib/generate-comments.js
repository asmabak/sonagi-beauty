/* Generate Sonagi-voice comments for a batch of posts using Google Gemini API.
   Free tier: 1M tokens/day, 15 req/min, no credit card.
   Get a key at https://aistudio.google.com/app/apikey  */

const https = require("https");

function callGemini({ apiKey, model, system, user, max_tokens, temperature }) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      contents: [{ role: "user", parts: [{ text: user }] }],
      systemInstruction: { parts: [{ text: system }] },
      generationConfig: {
        temperature: temperature || 0.85,
        maxOutputTokens: max_tokens || 800,
        responseMimeType: "application/json",
      },
    });
    const req = https.request(
      {
        hostname: "generativelanguage.googleapis.com",
        path: "/v1beta/models/" + encodeURIComponent(model) + ":generateContent?key=" + apiKey,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = "";
        res.on("data", (c) => (data += c));
        res.on("end", () => {
          try {
            const json = JSON.parse(data);
            if (json.error) return reject(new Error(json.error.message || JSON.stringify(json.error)));
            const cand = json.candidates && json.candidates[0];
            const text = cand && cand.content && cand.content.parts && cand.content.parts[0] && cand.content.parts[0].text;
            const usage = json.usageMetadata || {};
            resolve({ text: text || "", usage: { input_tokens: usage.promptTokenCount, output_tokens: usage.candidatesTokenCount } });
          } catch (e) { reject(new Error("Gemini parse error: " + e.message + " · raw: " + data.slice(0, 300))); }
        });
      },
    );
    req.on("error", reject);
    req.setTimeout(60000, () => req.destroy(new Error("Gemini API timeout")));
    req.write(body);
    req.end();
  });
}

function buildSystemPrompt(voice) {
  return [
    "You are the comment-drafting brain for " + voice.brand + ".",
    "Brand positioning: " + voice.positioning + ".",
    "Voice rules:",
    ...voice.rules.map((r) => "  - " + r),
    "",
    "You will receive a batch of social-media posts. For EACH post, generate exactly " + (voice.options_per_post || 4) + " comment options labelled A, B, C, D.",
    "Each option is a different angle. Mix: (A) thoughtful question, (B) expert add-on with niche knowledge, (C) intimate/personal reaction, (D) gentle counter-take or nuance.",
    "Output STRICTLY as JSON array. One element per post in the same order received. Each element: { id: <post id string>, comments: [<A>, <B>, <C>, <D>] }.",
    "Do NOT include any prose outside the JSON array.",
  ].join("\n");
}

function buildUserPrompt(posts) {
  const lines = ["Here are the posts to comment on. Output the JSON array now."];
  posts.forEach((p, i) => {
    lines.push("");
    lines.push("---");
    lines.push("Post " + (i + 1) + ":");
    lines.push("  id: " + p.id);
    lines.push("  platform: " + p.platform);
    lines.push("  author: " + (p.handle || p.author || "unknown"));
    lines.push("  posted: " + (p.pubDate ? new Date(p.pubDate).toISOString() : "unknown"));
    lines.push("  caption: \"" + (p.title || "").replace(/[\r\n]+/g, " ").slice(0, 200) + "\"");
    if (p.description && p.description.trim() && p.description.trim() !== p.title) {
      lines.push("  body: \"" + p.description.replace(/[\r\n]+/g, " ").slice(0, 600) + "\"");
    }
  });
  return lines.join("\n");
}

function tryParseJson(text) {
  let cleaned = (text || "").trim();
  if (cleaned.startsWith("```")) {
    cleaned = cleaned.replace(/^```(?:json)?/i, "").replace(/```$/, "").trim();
  }
  try { return JSON.parse(cleaned); }
  catch (e) {
    const m = cleaned.match(/\[\s*{[\s\S]+}\s*\]/);
    if (m) { try { return JSON.parse(m[0]); } catch (e2) { return null; } }
    return null;
  }
}

function delay(ms) { return new Promise((r) => setTimeout(r, ms)); }

/**
 * Generate comment options for an array of posts.
 * Batches in groups of 8 to stay under per-request token limits.
 * Returns Map<postId, string[]>.
 */
async function generateForPosts(posts, { apiKey, model, max_tokens, temperature, voice, batch_size = 8 }) {
  const result = new Map();
  if (!apiKey) {
    console.warn("[comments] No GEMINI_API_KEY set — skipping comment generation, returning empty.");
    return result;
  }
  const system = buildSystemPrompt(Object.assign({}, voice, { options_per_post: voice.options_per_post || 4 }));
  for (let i = 0; i < posts.length; i += batch_size) {
    const slice = posts.slice(i, i + batch_size);
    const user = buildUserPrompt(slice);
    try {
      const { text, usage } = await callGemini({ apiKey, model, system, user, max_tokens: max_tokens || 800, temperature: temperature || 0.85 });
      console.log("[gemini] batch " + (Math.floor(i / batch_size) + 1) + " · " + slice.length + " posts · in=" + (usage.input_tokens || "?") + " out=" + (usage.output_tokens || "?"));
      const parsed = tryParseJson(text);
      if (!Array.isArray(parsed)) {
        console.warn("[gemini] could not parse JSON for batch starting at index " + i + " — text head: " + (text || "").slice(0, 200));
        await delay(4000);  // stay under 15 req/min
        continue;
      }
      for (const entry of parsed) {
        if (entry && entry.id && Array.isArray(entry.comments)) result.set(String(entry.id), entry.comments);
      }
    } catch (e) {
      console.warn("[gemini] batch error at index " + i + ": " + e.message);
    }
    await delay(4000);  // 15 req/min ceiling = 4s between calls is safe
  }
  return result;
}

module.exports = { generateForPosts };
