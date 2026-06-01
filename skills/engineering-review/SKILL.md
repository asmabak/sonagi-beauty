---
name: engineering-review
description: Review OS / infra / code work the way a senior specialist engineer would, with the Karpathy lens, AND check it against Sonagi's lean v4 strategy so we never build automation Asma does not need. Use after building any script, hook, agent, skill, or workflow, before committing or wrapping up, or whenever asked to "have Karpathy review this" or "is this in line with the strategy". Run the review in a FRESH context (a reviewer subagent) so it cannot rubber-stamp its own work.
---

# Engineering review (Karpathy lens + strategy gate)

Summary: a review rubric, not an agent. It exists because the dangerous failure here is two-fold: (1) shipping code that looks done but has a quiet failure mode, and (2) building machinery Asma never asked for. A celebrity-named "agent" would add nothing the rubric does not. The independence that makes review valuable comes from running it in a SEPARATE context, so it judges the work without sharing the builder's assumptions. When to touch: apply it after any infra build and before commit/wrapup. Only Asma changes the strategy section; everyone else applies it.

## Index
- How to run it (fresh context, default skeptical)
- Gate 1: the strategy / scope filter (the most important one)
- Gate 2: the engineering filter (Karpathy lens)
- Output format
- The bar

## How to run it
Spawn a reviewer in a fresh context (the Agent tool, general-purpose or a reviewer type). Hand it: the diff or the files under review, plus `core/charter.md`, `OS/AI_ORCHESTRATION_PRINCIPLES_4.md`, and `soul.md` (Notion `36878492-123f-81fe-b75b-c9040cae1d7f`). Tell it to default skeptical: a finding it cannot prove is "unverified," never "fine." It returns findings, each with a severity and a one-line proof, plus an explicit verdict on Gate 1.

Do not let the builder review its own work in the same context. That is the whole point.

## Gate 1: the strategy / scope filter (apply FIRST, it can veto)
Sonagi runs lean for a 2-person team (Asma + Marouane). Before judging code quality, judge whether the thing should exist at all. Ask, in order:

1. **The cold-start test (supreme).** Does this make the next fresh session competent at token zero, OR is it needed now for the 2-person team? If it only serves an autonomous fleet we do not run yet, it should have been DEFERRED, not built. (v4: "optimise the cold start.")
2. **Did we build machinery instead of using Claude Code?** A bespoke framework, a parallel orchestration system, a model gateway before the named cost trigger, a tiered memory tree before the simple one hurts: all are premature. Flag them.
3. **Is it the leanest thing that works?** Five folders, two sources of truth, plain portable markdown. New folders, new services, new dependencies, and new always-on processes are guilty until proven necessary.
4. **Did Asma ask for this, or did the agent invent the need?** Map the work back to a queue item, a handover, or an explicit request. Work with no such anchor is scope creep, even if it is well built.
5. **Hand-curate vs automate (D4).** Things that change about monthly should stay hand-maintained. Only what drifts silently (disk-generated indexes) earns automation.

A Gate 1 failure means "well-built, but should not have been built." Say that plainly. Insight has no value if it solved a problem Asma did not have.

## Gate 2: the engineering filter (Karpathy lens)
1. **Correctness and the failure mode.** What happens when the input is empty, the path is wrong, the network is down, the file is locked, the process is killed mid-write? Does a failure stay contained, or break a session/commit/deploy? Hooks and scripts must never fail the thing they run inside.
2. **Did it prove itself, or just claim to?** (soul.md) Is there a test or a run that demonstrates the contract holds? Measure before claiming a metric. A promise is not proof.
3. **Simplicity.** Is there a smaller version that does the same job? Fewer files, fewer branches, fewer concepts. Delete before you add.
4. **Portability.** No absolute machine path. Cross-OS (Windows + macOS, `python3`). Plain ownable markdown for definitions. Survives a fresh clone.
5. **Cost and caching.** Stable prompt prefix, append-only context, no per-request timestamps near the top. Does anything regress the cache hit rate?
6. **Safety gates.** Human gate on publish/spend/delete; never spends money; least-privilege tools; no secrets committed; the lethal trifecta broken.
7. **Register on creation.** New agent/skill/script has its definition, its index/roster/catalogue row, its map entry, and a decision-log line. If it is not in the index, it does not exist for the next session.

## Output format
- One-line overall verdict (ship / fix-then-ship / do-not-ship), with the Gate 1 call stated separately.
- Findings, each: `[severity: blocker | should-fix | nit | scope]` one-line claim + one-line proof + the fix.
- What was checked and what was NOT (no silent coverage gaps).

## The bar
Be specific and falsifiable. "Could be cleaner" is useless; "lines 40-50 re-read the file already in memory, drop them" is a finding. Default skeptical on Gate 1: the lean strategy is the standing instruction, and over-building is the failure mode Asma most wants caught.
