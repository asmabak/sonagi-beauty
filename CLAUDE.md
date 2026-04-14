# Sonagi Beauty

## Marketing Skills

This project includes 36 marketing skills from [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), installed in `.agents/skills/` (symlinked to `.claude/skills/`).

### Available Skills

**Conversion Optimization**: page-cro, signup-flow-cro, onboarding-cro, form-cro, popup-cro, paywall-upgrade-cro

**Content & Copy**: copywriting, copy-editing, cold-email, email-sequence, social-content

**SEO & Discovery**: seo-audit, ai-seo, programmatic-seo, site-architecture, competitor-alternatives, schema-markup

**Paid & Distribution**: paid-ads, ad-creative

**Measurement & Testing**: analytics-tracking, ab-test-setup

**Growth & Retention**: churn-prevention, free-tool-strategy, referral-program, community-marketing, aso-audit, lead-magnets

**Strategy**: marketing-ideas, marketing-psychology, launch-strategy, pricing-strategy, content-strategy, customer-research

**Sales & RevOps**: revops, sales-enablement

**Foundation**: product-marketing-context (read by all other skills first)

### Usage

Skills are automatically discovered. Ask for marketing help naturally:

- "Help me optimize this landing page for conversions" -> page-cro
- "Write homepage copy for my SaaS" -> copywriting
- "Set up GA4 tracking for signups" -> analytics-tracking
- "Create a 5-email welcome sequence" -> email-sequence

Or invoke directly: `/page-cro`, `/copywriting`, `/seo-audit`, etc.

### Product Marketing Context

Create `.agents/product-marketing-context.md` to provide your product, audience, and positioning details. All skills reference this file first.
