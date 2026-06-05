# Template Schema Definitions

This document defines the YAML frontmatter schema for each of the 7 templates. Templates are authored as markdown files with YAML frontmatter. All templates follow these conventions:

- `type:` field identifies the template variant
- `brand:` field links across all templates for the same brand
- Array fields use block-list format (one `- ` per line)
- Booleans are bare (`true`/`false`, not quoted)
- Dates are `YYYY-MM-DD`
- Wikilinks are quoted `"[[Link]]"`

---

## brand-card.md

```yaml
---
type: brand-card
brand: Brand Name
tagline: "Short brand mission or positioning statement"
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
status: draft|active|archived
source:
  strategy: "[[Brand Name Strategy]]"
  visual-id: "[[Brand Name Visual Identity]]"
  voice: "[[Brand Name Voice]]"
layout: portrait|landscape
---
```

**Body sections:** Brand name + tagline → Logo (referenced) → Color swatches (condensed, 4-8 colors with names + HEX) → Type specimen (primary typeface name + weights) → Brand personality keywords → Tagline/positioning

---

## strategy.md

```yaml
---
type: brand-strategy
brand: Brand Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
status: draft|active|archived
positioning:
  audience: "Primary target audience description"
  differentiator: "What makes this brand unique"
  market: "Market category"
personality:
  - axis: sincere|exciting|competent|sophisticated|rugged
    value: 1-5
  - axis: sincere|exciting|competent|sophisticated|rugged
    value: 1-5
  - axis: sincere|exciting|competent|sophisticated|rugged
    value: 1-5
  - axis: sincere|exciting|competent|sophisticated|rugged
    value: 1-5
  - axis: sincere|exciting|competent|sophisticated|rugged
    value: 1-5
mission: "Core mission statement"
vision: "Long-term vision statement"
values:
  - name: Value Name
    description: "What this value means in practice"
  - name: Value Name
    description: "What this value means in practice"
competitors:
  - name: Competitor Name
    differentiator: "How we differ"
audiences:
  primary:
    name: "Persona name"
    description: "Description of primary audience"
  secondary:
    name: "Persona name"
    description: "Description of secondary audience"
---
```

**Body sections:** Positioning statement → Personality profile (with axis descriptions) → Mission & vision → Core values → Competitive landscape → Audience personas

---

## visual-id.md

```yaml
---
type: brand-visual-identity
brand: Brand Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
status: draft|active|archived
logo:
  primary:
    description: "Full-color horizontal logo"
    file_svg: "path/logo.svg"
    file_png: "path/logo.png"
    min_width_px: 100
  secondary:
    description: "Stacked vertical variant"
    file_svg: "path/logo-stacked.svg"
  icon:
    description: "Standalone symbol"
    file_svg: "path/icon.svg"
    min_width_px: 24
  monochrome:
    - variant: black|white|grayscale
      file_svg: "path/logo-black.svg"
  clear_space: 0.25
  min_sizes:
    print_mm: 15
    screen_px: 32
    social_px: 48
  backgrounds:
    allowed:
      - light solid
      - dark solid
    prohibited:
      - busy imagery
      - similar color to mark
  incorrect_usage:
    - description: "Don't stretch the logo"
    - description: "Don't add drop shadows"
    - description: "Don't recolor"
colors:
  primary:
    - name: "Brand Blue"
      hex: "#0055FF"
      rgb: "0 85 255"
      cmyk: "100 67 0 0"
      pantone: "2736 C"
      usage: "Primary brand elements"
  secondary:
    - name: "Accent Green"
      hex: "#00CC66"
      rgb: "0 204 102"
      cmyk: "75 0 85 0"
      usage: "Call-to-action elements"
  functional:
    - name: "Success"
      hex: "#00AA55"
      role: success
    - name: "Error"
      hex: "#DD3333"
      role: error
  neutral:
    - name: "Off Black"
      hex: "#1A1A1A"
      usage: "Body text"
  dark_mode:
    enabled: true
    adaptation: invert
  wcag_pairs:
    - foreground: "#0055FF"
      background: "#FFFFFF"
      ratio: 8.6
      level: AAA
typography:
  primary:
    family: "Brand Sans"
    weights:
      - 300
      - 400
      - 600
      - 700
    license: "Google Fonts / OFL"
  secondary:
    family: "Brand Serif"
    weights:
      - 400
      - 700
    fallback: "Georgia, serif"
  scale:
    - level: h1
      font_size: 48
      line_height: 1.2
      tracking: -0.02
    - level: h2
      font_size: 36
      line_height: 1.3
      tracking: -0.01
    - level: h3
      font_size: 24
      line_height: 1.4
      tracking: 0
    - level: body
      font_size: 16
      line_height: 1.6
      tracking: 0
    - level: caption
      font_size: 12
      line_height: 1.4
      tracking: 0.01
  web_fallbacks: "'Brand Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
iconography:
  style: outlined
  stroke_weight: 1.5
  corner_radius: 2
  grid_size: 24
  padding: 2
  accessibility:
    min_touch_target: 44
    min_contrast: 3.0
photography:
  narrative: "Description of visual style, subject matter, and mood"
  color_grading: "Description of filter or color treatment"
  framing_rules:
    - "Rule description"
  diversity_guidelines: "Representation standards"
  prohibited:
    - "Generic stock photography"
    - "Overly posed corporate shots"
illustration:
  style: "Description of illustration style"
  allowed_colors: ["List of palette colors"]
  detail_level: 3
  tone: ["descriptive adjectives"]
---
```

**Body sections:** Logo system (variants table, clear space diagram, minimum sizes, backgrounds, misuse examples) → Color palette (primary, secondary, functional, neutral, dark mode, WCAG pairs) → Typography (typefaces table, scale, hierarchy, fallbacks, licensing) → Iconography (style, grid, accessibility) → Photography (narrative, framing, diversity, anti-patterns) → Illustration (style, palette constraints, detail level)

---

## voice.md

```yaml
---
type: brand-voice
brand: Brand Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
status: draft|active|archived
attributes:
  - name: "Confident"
    description: "Speaks with authority, not arrogance"
  - name: "Clear"
    description: "Prefer the direct word over the impressive one"
  - name: "Human"
    description: "Warm, conversational, never corporate"
tone_matrix:
  - context: "Product copy"
    audience: "New users"
    tone: "Helpful, encouraging"
  - context: "Error message"
    audience: "All users"
    tone: "Apologetic, solution-oriented"
  - context: "Social media"
    audience: "Followers"
    tone: "Playful, brief"
pillars:
  - name: "Innovation"
    description: "We push boundaries"
vocabulary:
  approved:
    - "we"
    - "you"
    - "let's"
  forbidden:
    - "leverage"
    - "synergize"
    - "utilize"
examples:
  - scenario: "404 error page"
    bad: "The requested resource was not found"
    good: "Hmm, that page wandered off. Let's get you back."
localization:
  notes:
    - "Maintain direct address in all markets"
---
```

**Body sections:** Voice attributes (3-5 with descriptions) → Tone matrix (context × audience → tone) → Messaging pillars → Vocabulary (approved words, words to avoid) → Copy examples (before/after pairs for common scenarios) → Localization notes

---

## application.md

```yaml
---
type: brand-application
brand: Brand Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
status: draft|active|archived
digital:
  channels:
    - name: "Social media"
      templates:
        - "path/template-instagram.png"
        - "path/template-linkedin.png"
      specs: "1080x1080 square, 1200x628 landscape"
    - name: "Email"
      templates:
        - "path/email-template.html"
      specs: "600px max width, inline CSS"
print:
  items:
    - name: "Business card"
      templates:
        - "path/business-card.ai"
      specs: "3.5x2in, 4/4 CMYK + spot gloss"
    - name: "Letterhead"
      templates:
        - "path/letterhead.ai"
      specs: "8.5x11in, 1-color logo"
cobranding:
  rules:
    - "Partner logo must be same size or smaller"
    - "Minimum clear space: 1x partner logo height"
  examples:
    - "path/cobrand-example.png"
file_formats:
  - format: SVG
    usage: "Web, digital, scalable"
  - format: EPS
    usage: "Print production"
  - format: PNG
    usage: "Office documents, social"
  - format: PDF
    usage: "Print-ready, client delivery"
motion:
  principles:
    - "Duration: 200-400ms for micro-interactions"
    - "Easing: ease-in-out for UI elements"
---
```

**Body sections:** Digital applications (per-channel templates and specs) → Print applications (per-medium templates and specs) → Co-branding rules → File format delivery matrix → Motion principles

---

## governance.md

```yaml
---
type: brand-governance
brand: Brand Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
status: draft|active|archived
versioning:
  scheme: "MAJOR.MINOR.PATCH"
  current_version: "1.0.0"
  notes: "MAJOR = redesign, MINOR = palette/type change, PATCH = documentation fix"
steward:
  name: "Brand Owner Name"
  role: "Title"
  contact: "email@example.com"
review:
  cadence: "Quarterly"
  last_review: YYYY-MM-DD
  next_review: YYYY-MM-DD
  trigger_events:
    - "Logo refresh"
    - "Merger or acquisition"
    - "New product launch with distinct identity"
exceptions:
  process:
    - "Submit exception request to brand steward"
    - "Steward reviews within 5 business days"
    - "Approved exceptions logged with expiration date"
  approval_chain: "Brand Steward → VP Marketing (if high-visibility)"
changelog:
  - date: YYYY-MM-DD
    change: "Initial brand identity documentation"
    author: "Author Name"
archive:
  retention: "Current + 2 previous versions"
  disposal: "Deprecated assets moved to /archive/ directory"
---
```

**Body sections:** Version numbering convention → Brand steward contact → Review cadence + trigger events → Exception request process → Changelog → Archive policy

---

## asset-inventory.md

```yaml
---
type: brand-asset-inventory
brand: Brand Name
updated: YYYY-MM-DD
owner: "Brand Steward Name"
---
```

**Body sections:** Table of all brand assets. The body is primarily a markdown table with these columns:

| Asset Name | Formats | Path | Usage Context | Updated | Owner |
|---|---|---|---|---|---|
| Primary Logo Color | SVG, PNG, EPS | `/assets/logos/primary/` | Web, print, social | 2026-01-15 | Design Team |
| Primary Logo B/W | SVG, EPS | `/assets/logos/primary/bw/` | Print, monotone | 2026-01-15 | Design Team |
| Brand Colors (ASE) | ASE, PDF | `/assets/color/` | Design tools reference | 2026-01-15 | Design Team |
| Brand Sans Regular | WOFF2, TTF | `/assets/fonts/` | Web, desktop | 2026-01-15 | Design Team |
| Icon Set | SVG | `/assets/icons/` | Web, app UI | 2026-01-15 | Design Team |
| Social Templates | PSD, AI, FIG | `/assets/templates/social/` | Social media production | 2026-01-15 | Design Team |
| Brand Guidelines | Markdown | `/docs/brand/` | Internal reference | 2026-01-15 | Brand Steward |

### Asset categories (in canonical order)
- **Logo files:** All variants, all formats
- **Color reference files:** ASE swatches, palette reference cards
- **Font files:** All licensed typefaces with format variants
- **Icon sets:** Style-specific icon libraries
- **Illustration assets:** Style-specific illustration libraries
- **Photography:** Stock libraries, commissioned shoots, usage rights
- **Templates:** Social, email, slide deck, document templates
- **Video/Motion:** Brand videos, logo animations, lower thirds
- **Documentation:** Brand guidelines, spec documents, usage guides
