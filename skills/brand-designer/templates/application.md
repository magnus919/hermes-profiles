---
type: brand-application-template
name: Application Guidelines Template
description: >-
  Document how the brand is applied across channels and media. Covers digital,
  print, social, co-branding, and file format delivery. For brands appearing
  on 3+ channels.
---

# Application Guidelines: {{brand}}

> **Visual reference:** See [[{{Brand Name}} Visual Identity]] for the colors, typography, and logo assets used in these applications.

## Digital Applications

### Social Media

| Platform | Dimensions | Format | Template |
|----------|------------|--------|----------|
| Instagram (post) | 1080×1080 px | PNG/JPG | `{{path/template-insta.png}}` |
| Instagram (story) | 1080×1920 px | PNG/JPG | `{{path/template-story.png}}` |
| LinkedIn (post) | 1200×628 px | PNG/JPG | `{{path/template-linkedin.png}}` |
| Twitter/X | 1200×675 px | PNG/JPG | `{{path/template-x.png}}` |
| Facebook | 1200×630 px | PNG/JPG | `{{path/template-fb.png}}` |

### Email

| Element | Spec |
|---------|------|
| Max width | `{{600}}`px |
| Styling | {{Inline CSS}} |
| Header | {{path/email-header.png}} |
| Footer | {{path/email-footer.png}} |

### Website Elements

| Element | Specification |
|---------|---------------|
| Navigation bar | Primary color background, white text |
| Buttons (primary) | Accent color, 8px radius, 48px min height |
| Buttons (secondary) | Outlined, 2px stroke, transparent fill |
| Links | Primary color, underline on hover |
| Forms | Light gray border, 4px radius, 12px padding |

## Print Applications

| Item | Dimensions | Colors | Bleed | Template |
|------|------------|--------|-------|----------|
| Business card | 3.5×2 in / 85×55 mm | 4/4 CMYK | 3mm | `{{path/business-card.ai}}` |
| Letterhead | 8.5×11 in / A4 | 1-color logo | None | `{{path/letterhead.ai}}` |
| Presentation deck | 16:9 (1920×1080) | RGB | None | `{{path/deck.pptx}}` |

## Co-branding

### Rules

- Partner logo must be **equal or smaller** in visual weight
- Minimum clear space: **1×** the partner's logo height on all sides
- Partner logo should be in black, white, or their primary brand color
- Do not lock up partner logo with the {{brand}} logo in a fixed relationship unless approved

### Acceptable Examples

{{Include visual examples of correct co-branding}}

### Unacceptable Examples

{{Include visual examples of incorrect co-branding}}

## File Format Delivery

| Format | When to Use |
|--------|-------------|
| **SVG** | Web, digital interfaces, scalable vector graphics |
| **EPS** | Print production, professional design software |
| **PNG** | Office documents, social media, web (when SVG not supported) |
| **PDF** | Print-ready files, client delivery, documentation |
| **JPG** | Photography, social media, web imagery |
| **FIG** | Figma-based design and prototyping |
| **AI** | Adobe Illustrator source editing |
| **PSD** | Adobe Photoshop layered compositions |
| **TTF/WOFF2** | Font distribution for desktop/web |

## Motion Principles (optional)

| Element | Duration | Easing | Notes |
|---------|----------|--------|-------|
| Micro-interactions | `{{200-400ms}}` | `{{ease-in-out}}` | UI feedback |
| Logo animation | `{{1-2s}}` | `{{ease-out}}` | Video intros |
| Page transitions | `{{300ms}}` | `{{ease}}` | Web/app navigation |
