# Sonagi Beauty — Project Configuration

> RuFlo V3 (the claude-flow orchestration framework) was removed on 2026-05-31, executing the decision Asma took on 2026-05-12 ("strip RuFlo, use plain Claude Code"). This repo now runs on native Claude Code: subagents via the Agent tool, deterministic orchestration via Workflow, and ownable file-based agents and skills. The target architecture for the whole AI operating system lives in `OS/AI_ORCHESTRATION_PRINCIPLES_4.md`.

## Behavioral rules (always enforced)

- Do what has been asked; nothing more, nothing less.
- ALWAYS read a file before editing it.
- ALWAYS prefer editing an existing file to creating a new one.
- NEVER proactively create documentation or README files unless explicitly requested.
- NEVER save working files, notes, or tests to the repo root. Use the correct folder below.
- NEVER commit secrets, credentials, or `.env` files.
- Pause for human approval before anything that publishes, spends, or deletes.

## Where things live

- `OS/` — the AI operating-system architecture. Source of truth for how this agent system is meant to run.
- `images/YYYY-MM-DD/` — all generated assets, one dated folder per day (see the asset protocol in the global `~/.claude/CLAUDE.md`).
- `website/`, `netlify/` — the site and its deploy configuration.
- `brand-strategy/`, `content/`, `media/` — working docs. Largely untracked here; the backup mirror is `OneDrive/sonagi-beauty`.
- Most Sonagi context (brand voice, session state, the Minjun character, production pipelines) lives in the global `~/.claude/CLAUDE.md` and in Notion, not in this file.

## Agents and skills

- Bespoke Sonagi agents live as plain Markdown in `~/.claude/agents/` (global) so they stay ownable and portable. Today: chief-of-staff, medical-fact-checker, social-media-strategist. The remaining roster roles are defined in Notion and being written to files per the v4 architecture.
- Repo-local agents kept here: `.claude/agents/pdp-elite.md` and `.claude/agents/ads/` (the ads-audit set).
- Skills are surfaced via `.claude/skills/` (junctioned from `.agents/skills/` and the skill repos under `C:\Users\marou\`).

## Marketing skills

This project includes 36 marketing skills from [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), installed in `.agents/skills/` and surfaced through `.claude/skills/`.

**Conversion Optimization**: page-cro, signup-flow-cro, onboarding-cro, form-cro, popup-cro, paywall-upgrade-cro

**Content & Copy**: copywriting, copy-editing, cold-email, email-sequence, social-content

**SEO & Discovery**: seo-audit, ai-seo, programmatic-seo, site-architecture, competitor-alternatives, schema-markup

**Paid & Distribution**: paid-ads, ad-creative

**Measurement & Testing**: analytics-tracking, ab-test-setup

**Growth & Retention**: churn-prevention, free-tool-strategy, referral-program, community-marketing, aso-audit, lead-magnets

**Strategy**: marketing-ideas, marketing-psychology, launch-strategy, pricing-strategy, content-strategy, customer-research

**Sales & RevOps**: revops, sales-enablement

**Foundation**: product-marketing-context (read by the other skills first)

### Usage

Skills are discovered automatically. Ask naturally ("optimize this landing page" → page-cro, "write homepage copy" → copywriting) or invoke directly: `/page-cro`, `/copywriting`, `/seo-audit`.
