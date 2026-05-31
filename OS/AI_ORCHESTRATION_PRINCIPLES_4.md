# AI Orchestration Architecture v4: Principles, Decisions, and the Lean Build

> Summary: This is v4 of the target architecture for Sonagi's human-plus-agent operating system. It keeps the strong thinking of v3 and bakes in six decisions taken in debate on 2026-05-30 (D1 to D6 below). It is written to be understood by a non-engineer: every technical term is defined in plain words the first time it appears. It is a PROPOSAL. Nothing here is implemented until Asma approves each step in chat.
>
> What changed from v3: (D1) we run ON Claude Code rather than building our own framework, with portable definitions so we are never locked in; (D2) two sources of truth confirmed, Notion earned its place; (D3) five folders, not eight; (D4) the Notion-to-Git sync problem is dissolved by descoping it; (D5) the autonomy slider is made concrete with three tiers and a graduation rule; (D6) two separate testing regimes, not one gate. Plus one new top principle (optimise the cold start), one correction (cache pricing), and one new rule (deprecate the dead).

## Index (read the header and the line you need, not the whole file)

- L34  Plain-words glossary (every technical term, defined once)
- L58  The one test above all others: optimise the cold start
- L66  The six decisions (D1 to D6), each with the reasoning
- L150 Operating principles (the spine)
- L170 Context engineering: what goes in the window each turn
- L186 Orchestration topologies: when each shape is right
- L200 The 12-factor agent rules, applied inside Claude Code
- L216 Agents and skills: roster, catalogue, register on creation, deprecate the dead
- L246 Maps and memory: focus, continuity, resilience
- L268 The founder approval queue (new, first-class)
- L278 File-writing protocol: summarise and index everything
- L290 Evals: two regimes, machine and content
- L304 Token-efficiency playbook (with the cache correction)
- L320 Security and safety
- L330 The lean target layout (five folders)
- L352 Session checklist (every run)
- L368 Sources

---

## Plain-words glossary

Defined once, in the order a newcomer meets them. The standing Sonagi rule is: never use a technical word without explaining it. This section is the backstop.

- **Agent.** A helper that holds context, looks around, decides, and acts in a loop. It exercises judgment. Robots think.
- **Skill.** An instruction card or recipe. No judgment, no loop. An agent picks it up and follows it. Cards do not think.
- **Runtime.** The workshop where the work actually happens: the room, benches, power. Claude Code is our runtime.
- **Framework.** A build-it-yourself workshop kit. We are choosing NOT to build one (see D1).
- **Claude Code.** The finished workshop we already have and use. The thing Asma types into.
- **Orchestration.** The conductor that decides which agent acts when, so they do not collide.
- **Event log / transcript.** A diary that records every step in order, so any run can be replayed and audited. Claude Code writes this for us.
- **Memory.** The notebook that survives between sessions. Without it, every new session wakes up remembering nothing.
- **Context window.** The agent's short-term attention, like the top of a desk. Only so much fits. What you put on it, and where, decides the quality of the work.
- **Cache.** Reusing thinking we already paid for instead of redoing it. Cheap. The single biggest cost lever.
- **Gateway.** A money-saving middle box that sends easy questions to a cheap brain and hard ones to an expensive brain. Deferred until spend justifies it.
- **Model.** One of the thinking-brains (for example Opus, Sonnet, Haiku).
- **Lock-in.** Being stuck with one provider, unable to leave. We avoid it through how we write definitions, not by building our own runtime.
- **Markdown.** Plain readable text with light formatting. Anyone can read it. Our agent and skill definitions live in it so they stay portable.
- **Tool scope.** The rule that each agent may only touch the tools its job needs. The painter gets brushes, never the bandsaw.
- **MCP (Model Context Protocol).** An open standard, like a universal plug, for letting agents reach tools and data in a consistent way. Open means no single vendor owns it.
- **Eval.** A test. For machines it is pass or fail. For content it is a checklist plus a human's eye.

---

## The one test above all others: optimise the cold start

Every fresh session begins half-amnesic: it knows nothing until we feed it. The entire value of this architecture is a cold-started session that is instantly competent at token zero.

So judge every proposed component by one question: **does this make the next fresh session smarter the moment it wakes up?** If yes, build it. If it only serves an autonomous fleet we do not run yet, defer it. This single filter separates the useful spine from the cathedral. It is why most of v3's heavier machinery is deferred below.

---

## The six decisions (D1 to D6)

These were taken in debate. Each states the choice, the reasoning, and what it changes.

### D1. Runtime posture: hybrid. Run on Claude Code, keep definitions portable.

We do not build our own framework. We use Claude Code as the runtime: agents are markdown files, orchestration is Workflow scripts (deterministic, code-defined runs), the event log is the transcript, memory is the memory directory. We apply the 12-factor and orchestration principles INSIDE Claude Code rather than building a parallel system.

Portability (avoiding lock-in) is bought cheaply, not by building a runtime but by writing every agent and skill as plain ownable markdown with its tool scope declared in the open. Such a definition would still make sense in another harness tomorrow. The robots are portable because their instructions are plain.

The gateway and model routing are deferred behind a NAMED trigger, so deferral is disciplined and not just procrastination. Add a gateway only when one of two things is true: monthly model spend crosses a figure on a real bill that we want to cut, OR a specific job genuinely needs a non-Anthropic model. Until then, a gateway is maintenance burden with no payoff. This trigger lives in the charter.

Why not build our own framework: a two-person team cannot maintain a bespoke runtime forever, it duplicates what we already pay Anthropic for, and ironically a custom runtime is its own lock-in (to our own unmaintained code), which is worse than the risk it tried to solve.

### D2. Storage: two sources of truth, plus a bucket, plus an optional viewer.

Confirmed in debate after watching the Notion layer actually work (the handover database and soul.md drive a clean cold start, which is exactly the payoff above).

- **Notion is the human brain.** Source of truth for what humans author and steer: brand charter, voice rules, strategy, the decisions log, ops state and handoffs, the readable agent roster and skills catalogue, research.
- **Git (the repo and `~/.claude/`) is the machine brain.** Source of truth for what agents read and write every run: agent and skill definitions, the maps, memory, evals, scripts, code. This is what needs version history (a record of every change), diff (seeing exactly what changed), and rollback (undo).
- **Drive or a CDN is heavy binaries only.** The validated image bank, video, large design files. Referenced by link, never duplicating canonical text. It is storage, not a brain, so it is not a third source of truth.
- **Obsidian is an optional read-only viewer** over the Git markdown, never a source of truth. Kept as a genuine fallback: if the human knowledge ever feels too heavy for Notion AND the only readers are Asma and Marouane, Obsidian-over-Git could collapse three systems to two. Anything collaborator- or customer-facing stays in Notion.

The trap to avoid forever: never let the same content have two sources of truth. That is the drift this whole document exists to stop.

### D3. Layout: five folders, not eight. Respect the global-versus-project split.

`/core`, `/agents`, `/skills`, `/evals`, `/scripts` earn their place now. Deferred until they actually hurt: `/knowledge` folds into `/skills` or `/core`; a tiered `/memory` tree is premature because Claude Code already gives a memory directory; `/orchestration` does not exist under D1.

Critical distinction v3 glossed: `~/.claude/` is GLOBAL across all of Asma's projects; the repo is PROJECT-specific. Global agents and skills belong in `~/.claude/`; only Sonagi-specific config belongs in the repo. The maps must respect this or they will lie about where things live.

### D4. Sync: dissolve the hardest problem by descoping it.

v3's hardest unsolved sentence was "automate Notion-to-Git sync." We do not build that pipeline. Split by rate of change instead:

- The human roster and catalogue in Notion change about monthly, so **hand-curate them.** Automation there rots faster than it helps.
- The Git-side indexes (`agent_chart.md`, `skills_index.md`, `PROJECT_MAP.md`) change with the code, so **generate them from the files on disk** via a script plus a hook (a hook is an automatic action that fires on an event, such as saving a file). Those are the ones that drift silently, so those are the ones we automate.

Result: there is no Notion-to-Git pipeline at all. Disk generates its own indexes; Notion is the hand-maintained human view. The hardest problem was an artifact of trying to automate the half that should stay human.

### D5. Autonomy: three concrete tiers and a graduation rule.

The slider must be a mechanism, not a label, or it is just an org chart. (This is the section with the least published practice behind it, so it is the one most likely to need revision. Treat it as a first draft to test against reality.)

- **Tier 0, Draft only.** The agent produces drafts; a human runs and ships everything.
- **Tier 1, Assistant.** The agent acts within a session but a human approves every action that publishes, spends, or deletes.
- **Tier 2, Autonomous on rails.** The agent runs unattended for ONE named, narrow scope, with a kill switch (an instant stop) and a logged trace (the diary of what it did).

**Graduation:** an agent moves up one tier only after a set number of clean runs at its current tier with zero human-corrected errors on its core job, ratified at a wrapup. **Demotion is automatic** on any publish, spend, or delete error. The roster flag becomes a tier number plus a visible clean-run count, so trust is earned and seen, not assumed.

The current session's Claude is Tier 1 on this system and has not graduated.

### D6. Evals: two regimes, not one gate.

Binary pass-or-fail testing is perfect for the machine layer and wrong for content.

- **Machine layer, deterministic evals.** Is the map stale? Did the sync script run? Does the tool return valid structured output? Clean yes-or-no checks that block the ship on failure.
- **Content layer, lint plus human gate.** A lint is an automatic style checker. The em-dash ban, banned words, and missing-jargon-gloss are lintable. Quality judgments like "does this caption sound like a friend, not a price tag" are not, so they route to a human or a clearly-labelled judge model, never pretending to be binary.

Section 9 (Evals) states this split explicitly so no one expects content to pass a gate it cannot.

---

## Operating principles (the spine)

1. **Optimise the cold start.** The newest principle and the highest. See the test above. Every component is judged by whether it makes the next fresh session competent at token zero.
2. **Single-threaded by default.** One agent or one fixed chain holds continuous context. Fan out (split into several agents) only when the task genuinely needs it. Parallel agents on partial context make conflicting assumptions that do not reconcile.
3. **Right shape for the task.** Pick the orchestration topology (the team shape) per task, not one style for everything.
4. **Context is the product.** A model has a finite attention budget. Put the smallest set of high-signal tokens in the window for each step. Most failures are context failures, not model failures.
5. **Every session starts half-amnesic.** We engineer the knowledge a fresh session needs (memory, maps, roster, catalogue). We do not hope for it.
6. **One canonical definition per thing,** in the layer that owns its type (D2): executable definitions in Git, human-readable roster and catalogue in Notion.
7. **Governed, not ad-hoc.** Tools, skills, memory, and agents are declared, discoverable, and version-controlled, never improvised.
8. **Reliable over clever.** It must survive a crash, repeat exactly, and pause for a human on risky steps.
9. **Open, no lock-in.** Portability through plain ownable definitions and open standards (MCP). No bespoke runtime, no paid vendor SDK.
10. **Cost is a first-class metric.** Efficiency regressions are treated like quality regressions.
11. **Human in the loop on anything that publishes, spends, or deletes.**

---

## Context engineering: what goes in the window each turn

Memory is what persists across sessions. Context engineering is what we put in the window right now. Different jobs.

- **Finite attention budget.** Curate the smallest high-signal set of tokens for the step at hand. More context is not better; it dilutes attention.
- **Pin constraints at the top or bottom, never the middle.** Models reliably degrade on information buried in the middle of a long context (the "lost in the middle" effect, also called context rot). Put non-negotiable rules and the current goal at the very start or end.
- **Just-in-time retrieval.** Fetch the chunk you need when you need it. Do not preload everything. Prune aggressively.
- **Three strategies for long tasks:** compaction (summarise history when the window fills), structured note-taking (write durable notes to files and reload only what the next step needs), and sub-agents (delegate a self-contained sub-task to a fresh context that returns only its result).
- **Filesystem as external, unlimited context.** The window is small; the file system is not. Offload state and long outputs to files, keep only pointers in the window.
- **System prompt at the right altitude.** Specific enough to guide, general enough not to overfit.

---

## Orchestration topologies: when each shape is right

A topology is just the shape of the team.

- **Sequential / single-threaded:** one chain, continuous context. The reliable default.
- **Supervisor (orchestrator-worker):** a lead splits the work, delegates, and combines results. Best for breadth-first research; roughly 90% better than a single agent at about 15x the token cost, a deliberate tradeoff.
- **Handoff:** agents pass control, with guardrails. Good for routing to specialists.
- **Group chat / debate:** several agents converse to refine an answer.
- **Magentic (dynamic manager):** a manager keeps shared context and picks who acts next, for open-ended tasks.

**Read versus write rule.** Parallelise read work (research, gathering) freely. Single-thread write work (code, content, any committed decision), because parallel writers diverge and cannot be merged cleanly. Start sequential, escalate to supervisor only when genuinely parallelisable, and cap the fan-out.

---

## The 12-factor agent rules, applied inside Claude Code

These are principles we honour in Claude Code, not a framework we build (D1).

- **Own your prompts.** No fully hidden, framework-generated prompts. We can read and edit every prompt.
- **Own your control flow.** The path through the steps is explicit (a Workflow script or a fixed chain), not emergent magic.
- **Small, focused agents.** Each agent does one job in roughly 3 to 20 steps, then hands off.
- **Replayable record.** Every input, tool call, and result is in one ordered log (the transcript). Any run is auditable and resumable.
- **Tools are structured outputs.** The model emits a structured call; deterministic code executes it.
- **Keep errors in the context.** When a tool fails, leave the error visible so the model self-heals within the run.
- **Contact humans with a tool call.** Asking for approval is just a tool. The agent can pause and resume.
- **Pre-fetch context.** Load what you know you will need up front.

---

## Agents and skills: roster, catalogue, register on creation, deprecate the dead

One canonical definition, one index, registered on creation, discovered from the index, never by scanning.

### The agent roster
- **Canonical executable definition:** `~/.claude/agents/<name>.md` (global) or the repo (project-specific), in plain markdown with declared tool scope.
- **Human-readable roster:** the AI Operations and Agent Architecture page in Notion, hand-maintained (D4).
- **Fast index in core:** `core/agent_chart.md` lists every agent with name, one-line job, tier and clean-run count (D5), runtime path, and Notion page ID. Generated from disk (D4).

### The skills catalogue
- **Canonical definition:** the skill's `SKILL.md`.
- **Human-readable catalogue:** a Skills Catalogue page in Notion, sibling of the roster, hand-maintained.
- **Fast index in core:** `core/skills_index.md` lists name, what it does, trigger, runtime location. Generated from disk.

### Management rules
- **Register on creation.** A new agent or skill is not done until it has its canonical definition, a row in the roster or catalogue, an entry in the relevant map, and a line in the decision log. If it is not in the index, it does not exist for the next session.
- **Deprecate the dead (new in v4).** The real state today is a hoard: many installed agents and skills, few used. Cataloguing everything is the wrong instinct; the audit must also archive or delete the unused. A registry of 100 dead entries hurts the cold start as much as having none. Every wrapup may retire what has not earned its keep.
- **Least privilege and stable tool sets.** Each agent gets only the tools its role needs. When a tool is temporarily unavailable, mask it (hide it) rather than remove it, so the cache stays stable.

### The agent-versus-skill litmus test
A skill is a capability: a how-to, no autonomy, no loop, invoked and applied. An agent is an actor: holds context, runs a look-decide-act loop, exercises judgment, calls skills and tools. If it decides or loops, it is an agent. If it is knowledge or a procedure an agent applies, it is a skill. Bias hard toward few agents and many shared skills: every extra agent adds routing, context fragmentation, and cost. Reclassify, do not delete: a demoted agent becomes a skill the remaining agents call.

---

## Maps and memory: focus, continuity, resilience

### The two maps (both in core memory, both loaded turn one)
- **`core/PROJECT_MAP.md`,** the code map: for every folder and key file, its path, one-line purpose, and entry points. Generated on change (D4).
- **`core/WORKSPACE_MAP.md`,** the Notion map: for every canonical page, its page ID, one-line purpose, and what lives under it. Hand-maintained on page add (D4).

### Core memory contents (always loaded)
The two maps, the roster and catalogue indexes, the charter and non-negotiable rules, and pointers (not full contents) to deeper memory.

### The three memory layers
- **Short-term session:** working memory for the current run.
- **Long-term memory bank:** carries facts across sessions, tiered into core, recall, archival, self-edited by the agent via tool calls. (Use the simple Claude Code memory directory first; build tiers only when it hurts, per D3.)
- **Durable workflow state:** persists for days so a paused or crashed run resumes exactly.

### How memory is retrieved (not recency alone)
Score every memory on recency, importance, and relevance; retrieve the top blend. Periodically distil raw entries into durable lessons (reflection), and have every distilled lesson cite the raw entries it came from (auditable).

---

## The founder approval queue (new in v4, first-class)

Every "human in the loop" gate routes to one person, Asma. Scattered across whoever happens to ask, that becomes noise and a bottleneck. Make it a single, first-class component: the Chief of Staff agent batches everything waiting on Asma into one surfaced queue, shown once, each item with its context and the reversible-or-not flag. The architecture is agent-centric on the surface but the real scarce resource is one human's attention, so it gets a named home.

---

## File-writing protocol: summarise and index everything

So a session jumps to the exact right place and never re-reads a whole file. This very document follows the pattern.

1. **Summary header at the top:** 1 to 3 sentences on what the file does and when to touch it.
2. **An index:** the file's sections with line numbers and a few words each.
3. **One job per file.** Split anything that does more than one thing.
4. **The index is regenerated on save** by a hook, so it never drifts.

Reading rule for agents: read the header and index first, decide the exact location, then read only that span.

---

## Evals: two regimes, machine and content (D6)

- **Folder:** `evals/`, one file per capability or agent.
- **Machine layer, deterministic.** Binary checks: input plus an expected result. Many small unambiguous checks. A regression blocks the ship. Cost evals included: assert a token or cost budget per run so an efficiency regression fails the build.
- **Content layer, lint plus human gate.** Lintable rules (banned words, em-dash ban, jargon-gloss) run automatically; quality judgments route to a human or a labelled judge model. Never a fake binary.
- **Error-analysis loop.** Every real failure becomes a permanent regression test in `evals/`, with the root cause logged in `core/learnings.md`.

---

## Token-efficiency playbook (ranked by ROI)

1. **Cache hit rate is the single most important production metric.** Reused (cached) thinking is far cheaper than fresh. On Anthropic specifically: a cache WRITE costs about 1.25x a normal input token, and a cache READ costs about 0.1x, so the saving comes from reading the same cached prefix many times. (v3 said a flat "10x"; this is the corrected model.) Keep a stable prompt prefix (no per-request timestamps near the top), make context append-only, and serialise deterministically (stable key order). Watch the hit rate like a core dashboard number.
2. **Model routing / cascade.** Cheapest model that can answer; frontier model only for hard steps. Savings are workload-dependent (often large), not a guaranteed constant. Enabled by the gateway, which is deferred behind the D1 trigger.
3. **Caching tiers.** Exact-match for identical queries, semantic for similar, session for state.
4. **Compress and retrieve just in time.** Fetch the chunk you need, prune the rest; auto-compact at the limit.
5. **Cap the multi-agent fan-out.** Forbid sub-agents from spawning their own; enforce a per-run budget in the orchestrator.
6. **Put a gateway in front** only once the D1 trigger fires.
7. **Make cost a first-class metric.** Track cost per run; watch for silent creep.

---

## Security and safety

- **The lethal trifecta.** Danger appears when an agent at once has (a) access to private data, (b) exposure to untrusted content, and (c) a way to send data out. Any flow with all three is high risk; break at least one leg.
- **OWASP LLM Top 10 as the checklist.** Screen for prompt injection (hostile instructions hidden in content the agent reads), insecure output handling, sensitive-data leakage, and excessive agency before production.
- **Defence in depth:** least privilege on tools, per-agent identity and audit trail, guardrails on inputs and outputs, human approval on anything that publishes, spends, or deletes.

---

## The lean target layout (five folders)

```
/core
    PROJECT_MAP.md          # code map, generated on change
    WORKSPACE_MAP.md        # Notion map, hand-maintained on page add
    agent_chart.md          # roster index (name, job, tier, clean-run count), generated
    skills_index.md         # catalogue index, generated
    charter.md              # non-negotiable rules, the gateway trigger, brand/ops
    learnings.md            # distilled, auditable lessons
/agents                     # plain markdown definitions, declared tool scope (or in ~/.claude/agents for global)
/skills                     # each skill a SKILL.md with trigger + tool scope
/evals                      # machine (binary + cost) and content (lint + human gate)
/scripts
    update_project_map.py   # regenerates the maps and indexes from disk
CLAUDE.md / AGENTS.md       # loads core/, states the session rules
```

Deferred until they hurt: `/knowledge`, a tiered `/memory`, `/orchestration`, a gateway. The Notion side mirrors this in spirit: the AI Operations page holds the roster, a Skills Catalogue page holds the skills, the workspace map points to both plus the Strategy Dashboard, soul.md, and The Asma File.

---

## Session checklist (every run)

1. Load `core/PROJECT_MAP.md`, `WORKSPACE_MAP.md`, `agent_chart.md`, `skills_index.md`, `charter.md`.
2. Pin the goal and the non-negotiable rules at the top of context.
3. Use the maps to locate work; pick agents and skills from the indexes, not by scanning.
4. Read file headers and indexes, then jump to the exact span.
5. Pick the smallest topology that fits; parallelise reads, single-thread writes.
6. Stay within budget; keep the prefix stable and context append-only for cache hits.
7. Pause for human approval before anything that publishes, spends, or deletes; route it to the founder approval queue.
8. On finish: update both maps if structure changed, update the roster or catalogue if an agent or skill changed (register new ones, retire dead ones), regenerate file indexes, add or adjust evals, append a distilled lesson to `core/learnings.md` citing its evidence, log the decision, and update any agent's clean-run count and tier.

---

## Sources

- Andrej Karpathy, Software 3.0 (context window as memory, the autonomy slider, half-amnesic sessions).
- Anthropic, Building Effective Agents (2024) and Effective Context Engineering for AI Agents (2025).
- Cognition (Walden Yan), Don't Build Multi-Agents: single-threaded default, context-sharing failure modes.
- Manus (Yichao Ji): cache hit rate as primary metric, mask-don't-remove tools, filesystem as context, keep errors in context.
- Liu et al. (Stanford, 2023), Lost in the Middle (arXiv 2307.03172); Chroma, Context Rot.
- HumanLayer (Dex Horthy), 12-Factor Agents.
- Packer et al., MemGPT / Letta (arXiv 2310.08560): tiered core/recall/archival memory, self-editing.
- Park et al. (Stanford), Generative Agents (arXiv 2304.03442): recency, importance, relevance scoring; reflection.
- Phil Schmid: parallelise reads, single-thread writes.
- OWASP, Top 10 for LLM Applications; Simon Willison, the lethal trifecta.
- Husain and Shankar: evals as the release gate; error-analysis loop.

---

*v4, drafted 2026-05-30 in debate with Asma. Next step: Asma reviews this draft, then we audit both layers against it and implement one reversible step at a time, updating the maps, roster, catalogue, and evals after each, pausing for review.*
