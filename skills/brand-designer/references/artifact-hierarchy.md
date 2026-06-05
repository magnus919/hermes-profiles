# Artifact Hierarchy

Every artifact the `brand-designer` skill produces, organized by audience, format, depth, and relationship.

## Quick Reference

```
Tier 0: Brand Card         →   Stakeholders, Press, Partners       (image + one-pager)
Tier 1: Strategy Memo      →   Leadership, Marketing               (narrative)
Tier 2: Visual Identity    →   Designers, Developers               (structured spec)
Tier 3: Voice & Messaging  →   Writers, Content, Support           (guidelines)
Tier 4: Application        →   Producers, Agencies                 (rules + examples)
Tier 5: Governance         →   Brand Owners, Legal                 (framework)
Tier 6: Asset Inventory    →   Everyone                            (index)
       └── Compiled Brand Book (Tiers 1-6 combined)                (comprehensive reference)
```

## Artifact Descriptions

### Brand Card (Tier 0)

| Field | Value |
|-------|-------|
| **What it is** | A single-page visual and textual summary of the brand's identity. The "elevator pitch." |
| **Audience** | Stakeholders, executives, press, partners, new hires |
| **Format** | (a) Markdown one-pager via `templates/brand-card.md`, (b) Generated image via `scripts/generate brand-card` |
| **Depth** | Condensed — selects key elements from other tiers, does not exhaust |
| **Dependency** | Sources from Strategy, Visual Identity, and Voice. Requires those to exist first (or be filled alongside). |
| **When to produce** | Always — even pre-revenue startups benefit from a brand card |
| **Image variant** | `generate brand-card --layout portrait|landscape` — renders logo + palette swatches + type specimen + tagline |

### Strategy Memo (Tier 1)

| Field | Value |
|-------|-------|
| **What it is** | The "why" behind the brand. Positioning, personality, audience, competitive landscape. |
| **Audience** | Leadership, marketing team, agency briefs |
| **Format** | Markdown template via `templates/strategy.md` |
| **Depth** | Narrative — 3-5 pages of structured prose |
| **Dependency** | None (foundational) |
| **When to produce** | Growing brands (10+ people) or any brand working with agencies |

### Visual Identity Spec (Tier 2)

| Field | Value |
|-------|-------|
| **What it is** | The "how it looks." Complete documentation of logo system, color, typography, iconography, imagery. |
| **Audience** | Designers, developers, content creators, agencies |
| **Format** | Markdown template via `templates/visual-id.md` |
| **Depth** | Exhaustive — tables, values in multiple color spaces, type scale, do/don't examples |
| **Dependency** | Informed by Strategy Memo (positioning drives visual decisions) |
| **When to produce** | Growing brands producing external materials |
| **Image variants** | `generate swatch` (palette visualization), `generate logo-bg` (logo on different backgrounds), `generate mockup` (application examples) |

### Voice & Messaging Spec (Tier 3)

| Field | Value |
|-------|-------|
| **What it is** | The "how it sounds." Voice attributes, tone matrix, vocabulary, copy examples. |
| **Audience** | Writers, content marketers, customer support, product designers |
| **Format** | Markdown template via `templates/voice.md` |
| **Depth** | Moderate — enough rules to be practical, with plenty of examples |
| **Dependency** | Informed by Strategy Memo (personality drives voice) |
| **When to produce** | Growing brands with >1 person writing for the brand |
| **Image variants** | `generate moodboard [--theme <name>]` — visual mood board aligned to voice |

### Application Guidelines (Tier 4)

| Field | Value |
|-------|-------|
| **What it is** | The "where it goes." Rules for digital, print, social, signage, co-branding. |
| **Audience** | Producers, agencies, marketing operations |
| **Format** | Markdown template via `templates/application.md` |
| **Depth** | Moderate — channel-by-channel with file format matrix |
| **Dependency** | Depends on Visual Identity Spec (colors, type, logo are referenced) |
| **When to produce** | Brands appearing on 3+ channels |
| **Image variants** | `generate mockup --type stationery|social|signage|digital` |

### Governance Framework (Tier 5)

| Field | Value |
|-------|-------|
| **What it is** | The "how we keep it consistent." Versioning, ownership, review cadence, exception process. |
| **Audience** | Brand owners, stewards, legal, marketing ops |
| **Format** | Markdown template via `templates/governance.md` |
| **Depth** | Moderate — framework documents, content light |
| **Dependency** | None (parallel to other tiers) |
| **When to produce** | Scaling brands (50+ people) or any brand with multiple contributors |

### Asset Inventory (Tier 6)

| Field | Value |
|-------|-------|
| **What it is** | A structured index of every brand asset with format metadata, path, usage context. |
| **Audience** | Everyone who needs to find a brand file |
| **Format** | Markdown template via `templates/asset-inventory.md` |
| **Depth** | Tabular — rows of files with columns for format, path, usage, owner |
| **Dependency** | Depends on all other tiers being defined (assets are created from specs) |
| **When to produce** | Brands with >50 asset files |

### Compiled Brand Book (All Tiers)

| Field | Value |
|-------|-------|
| **What it is** | All spec documents assembled into a single unified reference, in canonical order. |
| **Audience** | Agencies, new hires, external partners — anyone who needs the complete picture |
| **Format** | (a) Compiled markdown via `brand-book compile --artifact full`, (b) HTML with optional CSS |
| **Depth** | Comprehensive — all sections, all detail |
| **Dependency** | Requires all other tiers to exist |
| **When to produce** | Agency handoff, enterprise distribution, press kit |

## Production Flow

```
User fills templates (Phase 2)
        │
        ▼
brand-book validate (Step 3.3)
    checks: required fields, color spaces, cross-references
        │
        ▼
brand-book compile --artifact brand-card
        │                            │
        ▼                            ▼
   Markdown one-pager          generate brand-card
                                    │
                                    ▼
                                Brand card image
                                
brand-book compile --artifact full
        │
        ▼
    Compiled brand book (markdown or HTML)
```

## Who Needs What

| Role | Artifacts They Use |
|------|-------------------|
| **CEO / Founder** | Brand card, strategy memo |
| **Designer** | Visual identity spec, asset inventory, brand card |
| **Developer** | Visual identity spec (colors, type), asset inventory |
| **Writer / Marketer** | Voice spec, brand card, application guidelines |
| **Agency Partner** | Compiled brand book, asset inventory |
| **Press / Media** | Brand card image, compiled brand book |
| **New Hire** | Brand card (first), compiled brand book (week one) |
| **Legal / Ops** | Governance framework, co-branding rules |
