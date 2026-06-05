---
name: brand-designer
description: >-
  Create comprehensive brand identity documentation for any brand. Guides you
  through documenting strategy, visual identity (logo, color, typography, imagery),
  voice and tone, application guidelines, governance, and asset inventory.
  Produces markdown specs, compiled brand books, and brand-compliant images via
  reference-image-aware generation. Use when you need to capture a brand's identity
  in structured, durable form — for vault storage, agency handoff, or press kit
  distribution.
license: MIT
compatibility: >-
  CLI requires Python 3.8+; generate script requires an image generation backend.
  All templates are plain markdown. Works with any agent supporting Agent Skills.
metadata:
  source: "https://github.com/agentskills/agent-skills"
  spec-version: "1.0"
  category: creative
---

# Brand Designer

A systematic toolkit for documenting brand identity. Elicits brand information through structured templates, validates completeness, compiles into reference documents, and generates brand-compliant images.

## Quick Start

```bash
# 1. Scaffold a new brand
brand-book init ./my-brand --name "Acme Corp"

# 2. Fill in the templates (7 markdown files)
#    Start with strategy.md → visual-id.md → voice.md

# 3. Validate your work
brand-book validate ./my-brand/strategy.md --strict

# 4. Compile output
brand-book compile ./my-brand --artifact brand-card    # One-page summary
brand-book compile ./my-brand --artifact full           # Full brand book

# 5. Generate brand image (optional)
generate brand-card --brand-dir ./my-brand --layout landscape
```

## When to Use This Skill

| Trigger | Artifact | Audience |
|---------|----------|----------|
| "I need a brand card for press/stakeholders" | Brand card (image + one-pager) | Executives, press, partners |
| "I need to document my brand strategy" | Strategy memo | Leadership, marketing |
| "I need visual identity documentation" | Visual identity spec | Designers, developers |
| "I need brand voice guidelines" | Voice & messaging spec | Writers, content team |
| "I need a full brand book for agency handoff" | Compiled brand book | Agencies, partners |
| "I need to inventory all my brand assets" | Asset inventory | Everyone |

## Workflow

### 1. Choose artifact type

The decision tree in `references/canonical-components.md` maps brand maturity to artifact scope:

- **Startup** (<10 people) → Brand card + Strategy memo (condensed)
- **Growing** (10-50) → Full visual identity + voice specs
- **Scaling** (50-200) → All specs + governance framework
- **Enterprise** (200+) → Full system + asset inventory + compiled brand book

### 2. Fill templates

7 templates live in `templates/`. Start with strategy (it informs everything else), then visual-id, voice, and the rest:

| Template | What It Captures | Depends On |
|----------|-----------------|------------|
| `strategy.md` | Positioning, personality, mission, audience | — |
| `visual-id.md` | Logo system, color palette, typography, iconography, imagery | Strategy |
| `voice.md` | Voice attributes, tone matrix, vocabulary, copy examples | Strategy |
| `application.md` | Digital, print, social, co-branding rules | Visual identity |
| `governance.md` | Versioning, review cadence, exceptions | — |
| `asset-inventory.md` | Structured file index | All others |
| `brand-card.md` | Condensed visual summary (sources from others) | Strategy, visual-id, voice |

**Filling technique:** Replace `{{placeholders}}` in each template with your brand's information. Required fields are marked in frontmatter. Optional fields can be removed.

### 3. Validate

```bash
brand-book validate ./my-brand/visual-id.md              # Basic checks
brand-book validate ./my-brand/brand-card.md --strict     # Cross-reference checks
brand-book validate ./my-brand/*.md                       # Batch check all
```

Validation catches:
- Missing required fields
- Incomplete color values (missing RGB, CMYK, or Pantone)
- Cross-reference breaks (brand-card sourcing from nonexistent specs)

### 4. Compile

```bash
brand-book compile ./my-brand --artifact brand-card                        # One-pager
brand-book compile ./my-brand --artifact full                              # Full book
brand-book compile ./my-brand --artifact full --format html --output book.html  # HTML
```

The `--artifact` selector maps to individual templates or the compiled whole. See `references/artifact-hierarchy.md` for the complete taxonomy.

### 5. Generate images (optional)

```bash
generate brand-card --brand-dir ./my-brand --layout landscape    # Press kit card
generate mockup --brand-dir ./my-brand --type social             # Social media mockup
generate swatch --brand-dir ./my-brand                           # Color palette card
generate moodboard --brand-dir ./my-brand --theme "innovation"  # Mood board
generate logo-bg primary --brand-dir ./my-brand --background dark  # Logo on dark
```

The `generate` script is prompt-engineering-first: it reads your brand data and constructs optimized prompts for image generation backends. For best results with accurate logo rendering, provide reference images alongside the prompt.

## Scripts Reference

### `scripts/brand-book`
The main CLI. Subcommands:

| Command | Action |
|---------|--------|
| `init <dir> [--name]` | Scaffold brand directory with 7 templates |
| `compile <dir> [--artifact] [--format] [--output]` | Assemble brand artifact |
| `validate <file...> [--strict] [--json]` | Check frontmatter completeness |
| `preview <file> [--json]` | Terminal preview of a brand component |

All subcommands support `--json` for machine output and `--dry-run` for preview.

### `scripts/generate`
Image prompt construction for brand-compliant generation. Subcommands:

| Command | Action |
|---------|--------|
| `brand-card [--layout portrait|landscape]` | Brand card image prompt |
| `mockup --type stationery|social|signage|digital` | Application mockup prompt |
| `swatch` | Palette visualization prompt |
| `moodboard [--theme]` | Mood board prompt |
| `logo-bg <variant> [--background]` | Logo presentation prompt |

## Reference Files

| File | What It Contains |
|------|-----------------|
| `references/canonical-components.md` | Definitive component hierarchy + maturity decision tree |
| `references/artifact-hierarchy.md` | Every artifact: who consumes it, format, depth, relationships |
| `references/gold-standard-analysis.md` | Structural analysis of Cash App, IBM, Netflix, Bang & Olufsen, Klarna |
| `references/brand-card-formats.md` | Format comparison: PDF vs online vs CLI vs Figma vs image |
| `references/template-schemas.md` | Complete YAML frontmatter schemas for all 7 templates |
| `references/image-generation.md` | Brand-compliant image prompt patterns and reference-image usage |

## Artifact Tiers Summary

```
Tier 0: Brand Card          → image + one-pager        → stakeholders, press
Tier 1: Strategy Memo       → narrative document       → leadership, marketing
Tier 2: Visual Identity     → structured spec          → designers, developers
Tier 3: Voice & Messaging   → guidelines with examples → writers, content
Tier 4: Application         → channel-by-channel rules → producers, agencies
Tier 5: Governance          → framework document       → brand owners, legal
Tier 6: Asset Inventory     → indexed table            → everyone
       └── Compiled Brand Book (Tiers 0-6 combined)    → agencies, partners
```

## Gotchas

### Templates are elicitation tools, not final designs
The templates produce markdown documentation, not designed PDFs. The content is structured and correct; visual polish is a post-processing step. If you need a beautifully designed PDF, export the markdown and lay it out in InDesign/Figma.

### Color accuracy in generated images
Generated images will *approximate* brand colors, not match them precisely. The `generate swatch` command provides hex values in the prompt, but image models interpret color imprecisely. For Pantone-accurate color reference, use the documented values in the spec, not generated images.

### Reference-image-aware generation is setup-dependent
The `generate` script constructs prompts regardless of backend. To use reference images (logos, existing materials) for better results, you need a generation setup that supports image inputs — e.g., ComfyUI, local Stable Diffusion with img2img, or an API that accepts image references. The prompts work without this; they just improve with it.

### Brand card sources from other templates
The brand-card template uses `source:` frontmatter links to strategy, visual-id, and voice templates. This means: compile may show placeholder text if those source templates aren't filled yet. Fill strategy + visual-id before expecting a complete brand card.

### The skill produces documents, not art
The image generation capability exists, but the primary output is **structured documentation** — markdown that can live in a vault, be versioned in git, and be compiled into various formats. The images are the garnish, not the meal.

## See Also

- `nous-branding` — Reference-image generation for Nous Research brand
- `cli-builder` — Patterns used by the brand-book CLI
- `references/image-generation.md` — Detailed prompt craft guide
