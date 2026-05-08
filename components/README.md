# Components — Atomic Design Naming Convention

This directory holds all UI components for sonagibeauty.com. Structure follows atomic design, enforced by the spec (`sonagiclaudecodespec.md` → "Component Naming Convention").

New components MUST follow this convention. Existing components in `/files/` are flagged for gradual refactor — see Migration policy below.

---

## Folder tree

```
components/
├── atoms/                    # smallest reusable units
│   ├── btn-primary
│   ├── btn-ghost
│   ├── btn-icon
│   ├── price-tag
│   ├── badge-flag           # variants: best-seller, new, trending
│   ├── trust-pill
│   ├── korean-script-accent
│   ├── star-rating
│   └── ...
├── molecules/                # composed of atoms
│   ├── product-card-default
│   ├── product-card-compact
│   ├── review-card
│   ├── concern-tile
│   ├── ingredient-pill
│   ├── brand-logo-link
│   ├── masterclass-card
│   └── ...
├── organisms/                # full sections
│   ├── hero-slider
│   ├── trust-band               # desktop
│   ├── trust-conveyor-mobile    # mobile (NEW)
│   ├── product-grid-desktop
│   ├── product-carousel-mobile  # 2x2 paginated (NEW)
│   ├── concern-grid-desktop
│   ├── concern-carousel-mobile  # 2x2 paginated (NEW)
│   ├── masterclass-carousel-mobile  # 1-card (NEW)
│   ├── reviews-section
│   ├── journal-grid
│   ├── social-wall
│   ├── footer
│   └── ...
├── templates/                # page-level layouts
│   ├── homepage
│   ├── product-detail
│   ├── brand-page
│   ├── encyclopedia-ingredient
│   ├── encyclopedia-clinical
│   ├── encyclopedia-concept
│   ├── encyclopedia-routine
│   ├── encyclopedia-concern
│   ├── rituel-detail
│   ├── article-detail
│   └── ...
└── pages/                    # route bindings
```

---

## Naming rules

- **Files:** `kebab-case` (e.g. `product-card-default.html`, `trust-conveyor-mobile.css`).
- **Modifiers:** `--modifier` for variants (e.g. `product-card--compact`, `btn-primary--ghost`).
- **States:** `.is-active`, `.is-loading`, `.is-disabled` — class-based, never inline style.
- **Viewport-specific suffix:** use `-mobile` or `-desktop` suffix only when the component genuinely differs (different DOM, different interaction model). Most components handle viewport variation via CSS breakpoints — do NOT split unless behaviour diverges.
- **Data props:** passed as JSON attributes on the component root (e.g. `data-props='{"sku":"...","persona":"strategique"}'`).
- **Per-component README:** each component folder ships a `README.md` documenting its props, modifiers, states, and a usage example. No undocumented components.

---

## Migration policy

Existing components living under `/files/` predate this convention. They are flagged for gradual refactor and will be moved into `components/{atoms,molecules,organisms,templates,pages}/` during the appropriate phase work — never as a wholesale rewrite. Until refactored, they remain in place and continue to ship; do not edit them to fit the new convention without a corresponding refactor task.

New components MUST be created under this directory using the convention above. No new files should be added to `/files/`.

---

## Proof of pattern

The encyclopedia page templates are the first builds compliant with this convention and serve as the reference implementation for everything that follows. See:

- `templates/encyclopedia-ingredient/` — first compliant template; props documented in its README; ships `MedicalSubstance` + `DefinedTerm` + `FAQPage` + `ScholarlyArticle` JSON-LD per the spec's Phase 6 schema requirements.
- `templates/encyclopedia-clinical/`
- `templates/encyclopedia-concept/`
- `templates/encyclopedia-concern/`
- `templates/encyclopedia-routine/`

When in doubt about file naming, prop shape, or README format, mirror `templates/encyclopedia-ingredient/`.
