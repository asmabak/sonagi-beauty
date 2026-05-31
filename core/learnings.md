# learnings.md: distilled, auditable lessons

> Append-only. Each lesson is short, dated, and cites the evidence it came from (a session, a command output, a file). Distil raw experience into a durable rule here so the next session inherits it.

## 2026-05-31: Measure before claiming a metric is bad
**Lesson:** Do not assert a quantitative gap from architecture prose. Measure it. In the v4 review this session, I claimed cache hit rate was "effectively zero" and "unmeasured." When `scripts/session_cost.py` was built and run, the Anthropic prompt cache was at 92.2% across 31 sessions (95.6% this session). The real gap was the absence of *measurement* and of a *local Notion cache for cold start*, not a low hit rate. I had conflated two different caches (the automatic prompt cache vs the planned local index cache).
**Rule:** Before stating any number-shaped weakness ("X is slow / zero / expensive"), build or run the measurement first. An unmeasured metric is "unknown," never "bad."
**Evidence:** `python scripts/session_cost.py --all` output, 2026-05-31, TOTAL hit_rate 92.2% over 8,583 messages.

## 2026-05-31: A linter must pass its own gate
**Lesson:** The first `em_dash_lint.py` failed on its own source (the banned characters were typed as literals) and crashed printing them on a cp1252 console. Building the needles from `chr(0x2014)` and forcing UTF-8 output fixed both. The generator also emitted em dashes into the cache via mirrored third-party skill descriptions, fixed by sanitizing mirrored text.
**Rule:** A tool that forbids a token must contain none of it as a literal (construct from code points), and must sanitize any external text it republishes. Dogfood every gate against its own outputs.
**Evidence:** `evals/em_dash_lint.py --selftest` PASS; full gate over spine files exit 0, 2026-05-31.
