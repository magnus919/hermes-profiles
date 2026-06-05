---
type: brand-visual-identity-template
name: Visual Identity Spec Template
description: >-
  Complete documentation of your brand's visual system. Fill in logo variants,
  color values in all spaces, typography scale, iconography, photography,
  and illustration style. This is the primary reference for designers and
  developers.
---

# Visual Identity: {{brand}}

> **Strategy reference:** See [[{{Brand Name}} Strategy]] for the positioning and personality that drive these visual decisions.

## Logo System

### Logo Variants

| Variant | Preview | File (SVG) | File (PNG) | Min Width | Usage |
|---------|---------|------------|------------|-----------|-------|
| Primary (color) | | `logo.svg` | `logo.png` | `{{100px}}` | Light backgrounds |
| Secondary (stacked) | | `logo-stacked.svg` | `logo-stacked.png` | `{{80px}}` | Square spaces |
| Icon only | | `icon.svg` | `icon.png` | `{{24px}}` | Favicon, avatars |

### Monochrome Variants

- **Black:** `logo-black.svg` — for 1-color print, dark-on-light
- **White:** `logo-white.svg` — for dark backgrounds
- **Grayscale:** `logo-gray.svg` — for limited-color applications

### Clear Space

Minimum empty area around logo: **{{0.25}}×** the height of the logo on all sides.

*Any text or graphic within this zone weakens the logo's visual impact.*

### Minimum Reproduction Size

| Medium | Size |
|--------|------|
| Print | `{{15}}` mm |
| Screen | `{{32}}` px |
| Social avatar | `{{48}}` px |

### Approved Backgrounds

| Background Type | Logo Variant to Use |
|----------------|-------------------|
| Light solid (#FFFFFF - #CCCCCC) | Primary color |
| Dark solid (#333333 - #000000) | White reversed |
| Photography (even toned) | White reversed |
| Photography (busy) | Avoid — use solid |

### Incorrect Usage

> Do **not** stretch, recolor, add effects, rotate, or change the logo in any way. Use only provided files.

| Incorrect | Why |
|-----------|-----|
| {{Screenshot placeholder}} | Do not stretch the logo |
| {{Screenshot placeholder}} | Do not change logo colors |
| {{Screenshot placeholder}} | Do not add drop shadows or outlines |
| {{Screenshot placeholder}} | Do not place on busy backgrounds |

## Color Palette

### Primary Colors

| Name | Swatch | HEX | RGB | CMYK | Pantone | Usage |
|------|--------|-----|-----|------|---------|-------|
| {{Brand Blue}} | | `#{{hex}}` | `{{r g b}}` | `{{c m y k}}` | `{{code}}` | Primary brand elements |
| {{Brand Red}} | | `#{{hex}}` | `{{r g b}}` | `{{c m y k}}` | `{{code}}` | Accent highlights |

### Secondary Colors

| Name | Swatch | HEX | RGB | CMYK | Usage |
|------|--------|-----|-----|------|-------|-------|
| {{Accent Green}} | | `#{{hex}}` | `{{r g b}}` | `{{c m y k}}` | CTA buttons |
| {{Accent Yellow}} | | `#{{hex}}` | `{{r g b}}` | `{{c m y k}}` | Notifications |

### Functional Colors (UI)

| Role | Name | Swatch | HEX | Contrast on White |
|------|------|--------|-----|-------------------|
| Success | {{Green}} | | `#{{hex}}` | {{ratio}}:1 |
| Error | {{Red}} | | `#{{hex}}` | {{ratio}}:1 |
| Warning | {{Yellow}} | | `#{{hex}}` | {{ratio}}:1 |
| Info | {{Blue}} | | `#{{hex}}` | {{ratio}}:1 |

### Neutral Palette

| Name | Swatch | HEX | Usage |
|------|--------|-----|-------|
| Off Black | | `#{{hex}}` | Body text |
| Dark Gray | | `#{{hex}}` | Secondary text |
| Medium Gray | | `#{{hex}}` | Borders, dividers |
| Light Gray | | `#{{hex}}` | Backgrounds |
| Off White | | `#{{hex}}` | Page backgrounds |

### Dark Mode (optional)

| Token | Light Value | Dark Value |
|-------|-------------|------------|
| Background | `#FFFFFF` | `#{{hex}}` |
| Text Primary | `#{{hex}}` | `#FFFFFF` |
| {{Token}} | `#{{hex}}` | `#{{hex}}` |

## Typography

### Typefaces

| Role | Typeface | Weights | Fallback | License |
|------|----------|---------|----------|---------|
| Display/Headlines | {{Primary Typeface}} | {{300, 400, 600, 700}} | {{system stack}} | {{license}} |
| Body | {{Secondary Typeface}} | {{400, 600}} | {{system stack}} | {{license}} |
| Code (if applicable) | {{Mono Typeface}} | {{400}} | {{mono stack}} | {{license}} |

### Type Scale

| Level | Size | Line Height | Tracking | Usage |
|-------|------|-------------|----------|-------|
| **H1** | `{{48}}px` | `{{1.2}}` | `{{-0.02em}}` | Page titles |
| **H2** | `{{36}}px` | `{{1.3}}` | `{{-0.01em}}` | Section headers |
| **H3** | `{{24}}px` | `{{1.4}}` | `{{0}}` | Subsection headers |
| **Body** | `{{16}}px` | `{{1.6}}` | `{{0}}` | Paragraphs |
| **Caption** | `{{12}}px` | `{{1.4}}` | `{{0.01em}}` | Image captions, footnotes |

### Web Font Stack

```
{{Primary Typeface}}, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
```

## Iconography (optional)

| Property | Value |
|----------|-------|
| Style | {{outlined / filled}} |
| Stroke weight | `{{1.5}}`px |
| Corner radius | `{{2}}`px |
| Grid size | `{{24}}`×`{{24}}` |
| Min touch target | `{{44}}`px |

## Photography & Imagery (optional)

### Visual Narrative

{{Describe the photographic style: subject matter, mood, lighting, color treatment}}

### Framing Rules

- {{Rule 1: e.g., "Subjects should be in natural settings, not studios"}}
- {{Rule 2: e.g., "Use negative space for copy overlay"}}

### Diversity Standards

{{Representation guidelines for photography}}

### Avoid

- {{Anti-pattern 1: "Generic stock photography of people in business suits shaking hands"}}
- {{Anti-pattern 2: "Overly filtered or faux-vintage looks"}}

## Illustration Style (optional)

| Property | Value |
|----------|-------|
| Style | {{Description, e.g., "Flat vector, geometric, 2-color"}} |
| Detail level | {{1-5 scale}} |
| Tone | {{Whimsical, technical, serious, etc.}} |
| Allowed palette | {{Referenced from color palette above}} |
