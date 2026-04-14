/**
 * Sonagi Advisor — AI-powered K-beauty skin protocol
 *
 * Environment variables required:
 *   ANTHROPIC_API_KEY — Claude API key
 *
 * Usage: POST /.netlify/functions/quiz-advisor
 *   Body: { prompt: "..." }
 */

exports.handler = async (event) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };

  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers, body: "" };
  }

  if (event.httpMethod !== "POST") {
    return { statusCode: 405, headers, body: JSON.stringify({ error: "Method not allowed" }) };
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: "API key not configured" }) };
  }

  try {
    const { prompt } = JSON.parse(event.body || "{}");
    if (!prompt) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: "No prompt provided" }) };
    }

    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-6",
        max_tokens: 2000,
        messages: [{ role: "user", content: prompt }],
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Anthropic API error:", errText);
      return { statusCode: 502, headers, body: JSON.stringify({ error: "AI service error" }) };
    }

    const result = await response.json();
    const text = result.content?.[0]?.text || "";

    // Parse the JSON response from Claude
    const parsed = JSON.parse(text);

    return { statusCode: 200, headers, body: JSON.stringify(parsed) };
  } catch (err) {
    console.error("Quiz advisor error:", err.message);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: "Failed to generate protocol" }),
    };
  }
};
