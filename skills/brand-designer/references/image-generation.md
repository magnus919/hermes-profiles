# Brand-Compliant Image Generation

How to generate on-brand images using the `generate` script and reference-image-aware prompts. Follows patterns proven in nous-branding and groktopus-branding.

## Core Principle

The built-in `image_generate` tool cannot use uploaded reference images. The `generate` script fills this gap by constructing brand-aware prompts and (optionally) routing through a reference-image-capable backend.

## Prompt Architecture

A brand-compliant prompt has four layers:

```
[SCENE]        — What's being shown (brand card, mockup, swatch, moodboard)
+ [COLORS]     — Exact palette constraints from brand data
+ [STYLE]      — Visual style (minimalist, photorealistic, illustrative, design-system)
+ [CONSTRAINTS]— What NOT to include (do/don't rules, banned elements)
```

### Good prompt structure

```
Professional brand card for "BrandName", horizontal 16:9 format.
Clean, minimalist design with:
- Large prominent brand name "BrandName" with tagline
- Color palette swatches: Brand Blue #0055FF, Accent Green #00CC66, Off Black #1A1A1A
- Clean sans-serif typography (Inter, SF Pro)
- Brand personality: competent, sincere
- Clean white background with subtle brand accent
- Elegant layout suitable for press kit
No photorealistic people. Design-system mockup style.
```

### Bad prompt structure

```
A cool-looking brand thing with some colors and maybe a logo. Make it look professional.
```

## Color in Prompts

**Always include HEX values** in prompts — models interpret `#0055FF` more precisely than "brand blue."

**Include color names** alongside hex values for models that don't parse hex well:
```
- Brand palette: Deep Navy #0A1628, Warm Gold #D4A843, Cream #F5F0E8
```

**Specify contrast relationships** for legibility:
```
- Dark text (#1A1A1A) on light background (#F8F8F8)
- White text (#FFFFFF) on brand-colored surfaces (#0055FF)
```

## Reference Image Patterns

When a reference-image-capable backend is available:

| Image Type | Best Reference Images | Effect |
|------------|----------------------|--------|
| Brand card | Logo + existing brand materials + palette card | Accurate logo rendering in context |
| Mockup | Logo + product photos | Realistic application examples |
| Swatch card | Palette reference image | Precise color matching |
| Logo bg | Logo file (transparent PNG) | Clean logo on various backgrounds |

## Subcommand Prompt Guide

### `generate brand-card`

Best output when the prompt includes:
- Brand name typographically (models render text inconsistently — accept this)
- HEX values for ALL primary and secondary colors
- The primary typeface name
- Layout: "flat lay" or "mockup on wall" for landscape; "social media card" for portrait

### `generate mockup --type signage`

For signage and environmental graphics, add context:
```
"architectural context, modern building exterior, subtle brand integration"
```
Avoid:
```
"huge logo on a building" — reads as billboard, not brand architecture
```

### `generate swatch`

Models tend to invent colors if not given exact values. Mitigations:
1. Provide hex values in the prompt
2. Reference an uploaded color palette card image
3. Expect some drift — swatch generation is a guide, not a Pantone proof

### `generate moodboard`

Moodboards benefit most from brand personality data. Include:
```
"Collage-style layout with textures, color fields, typography samples, 
and atmospheric imagery capturing [brand personality keywords] essence"
```

## Brand Card Layout Guide

| Layout | Dimensions | Use Case | Prompt Hint |
|--------|-----------|----------|-------------|
| Landscape | 16:9 (1920×1080) | Press kit, website hero, slide deck | "horizontal brand card, wide layout" |
| Portrait | 4:5 (1080×1350) | Social media, Instagram | "vertical brand card, social media format" |

## Do/Don't

| Do | Don't |
|----|-------|
| Include HEX values in prompts | Rely on color names alone ("brand blue" is ambiguous) |
| Specify what to exclude | Leave composition entirely to the model |
| Use reference images for logos | Expect text in generated images to be accurate |
| Match background to brand usage rules | Place colored logos on clashing backgrounds |
| Test prompts iteratively | Expect first-generation perfection |

## LLM Enhancement

When `BRAND_DESIGNER_LLM_URL` and `BRAND_DESIGNER_LLM_KEY` are set, the `generate` script can optionally:
- Refine prompts before sending to the imaging backend
- Suggest prompt improvements based on brand voice
- Classify whether a generated output is on-brand

This is optional — the script works without it; the LLM just improves quality.
