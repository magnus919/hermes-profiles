---
type: brand-card-template
name: Brand Card Template
description: >-
  Single-page brand card template. Fill this to produce a condensed visual and
  textual summary of your brand. Sources from your other brand templates via
  the `source` frontmatter field. When complete, run `generate brand-card`
  to produce the image version.
---

# Brand Card: {{brand}}

Replace the sections below with your brand's information.

## Brand Name & Tagline

**Brand Name:** `{{your brand name}}`
**Tagline:** `{{your tagline}}`

## Logo

*Reference your primary logo file. See [[{{Brand Name}} Visual Identity]] for all variants.*

| Variant | File | Usage |
|---------|------|-------|
| Primary (color) | {{path/logo.svg}} | Light backgrounds |
| Primary (reversed) | {{path/logo-white.svg}} | Dark backgrounds |
| Icon | {{path/icon.svg}} | Social avatars, favicon |

## Color Palette

| Swatch | Name | HEX |
|--------|------|-----|
| {{color box placeholder}} | {{Primary Color Name}} | `#{{hex}}` |
| {{color box placeholder}} | {{Secondary Color Name}} | `#{{hex}}` |
| {{color box placeholder}} | {{Accent Color Name}} | `#{{hex}}` |
| {{color box placeholder}} | {{Neutral Color Name}} | `#{{hex}}` |

*Full palette with RGB, CMYK, Pantone values in [[{{Brand Name}} Visual Identity]].*

## Typography

| Role | Typeface | Weights | Fallback |
|------|----------|---------|----------|
| Display / Headlines | {{Primary Typeface}} | {{weights}} | {{fallback}} |
| Body | {{Secondary Typeface}} | {{weights}} | {{fallback}} |

## Brand Personality

{{keyword}}, {{keyword}}, {{keyword}}, {{keyword}}

*Full personality profile in [[{{Brand Name}} Strategy]].*

## Voice

{{Short description of brand voice — e.g., "Confident, clear, and human."}}

*Full voice guidelines in [[{{Brand Name}} Voice]].*

---

*Generated from [[{{Brand Name}} Strategy]], [[{{Brand Name}} Visual Identity]], [[{{Brand Name}} Voice]].*
