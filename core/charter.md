# charter.md: non-negotiable rules (local cache of the Notion Charter)

> Read-only cache. Canonical source: Notion Charter `37178492-123f-8101-b440-e2aeb2abc568`.
> This is the machine brain's copy of the rules so a session has them at token zero without a Notion call. If this and Notion disagree, Notion wins; refresh this file from it.

Summary: the floor every session works to. Doctrine, source of truth, the human gate, and the cost trigger, in the fewest words that still bind.

## Doctrine
Insight has no value without effort. Do the work, not the look of the work. Verify, do not guess. Exhaust the input before interpreting it. Full text: soul.md (`36878492-123f-81fe-b75b-c9040cae1d7f`).

## Source of truth (two brains)
- Notion is the human brain: brand, voice, strategy, decisions, ops state, handoffs, the readable agent and skill roster.
- Git is the machine brain: executable agent and skill definitions, maps, indexes, evals, scripts, code. A running agent loads from a file on disk, so executable definitions live in git, never only in Notion.
- One canonical home per item. Mirrors (laptop clone, cloud clone, generated core/ indexes) only follow their master; never hand-edit a second copy.

## Non-negotiables
- No em dashes. Use periods, commas, colons, parentheses. (Enforced: `evals/em_dash_lint.py`.)
- Define every technical, medical, or jargon term on first use.
- Code lives in git, never OneDrive (OneDrive corrupts git working trees). Always push after you commit; never leave unpushed commits (they are lost on a fresh clone or new laptop). A private-backup push is part of saving, not a publish.
- Human gate on anything that publishes to production, spends, deletes, or is customer-facing. A private git push (backup) is not this gate. Route gated items to Asma.
- Never spend money. The user decides every purchase.

## Autonomy
T0 draft-only, T1 assistant (human approves publish/spend/delete), T2 autonomous on one narrow scope with a kill switch. Up one tier after N clean runs; demotion is automatic on any publish/spend/delete error. (Tiers are currently a label; the clean-run counter is not built yet.)

## Cost trigger (the deferred gateway)
Add a model gateway only when monthly model spend on a real bill crosses a figure worth cutting, OR a specific job needs a non-Anthropic model. Until then a gateway is maintenance with no payoff. Measurement lives in `scripts/session_cost.py` (tokens + cache hit rate).
