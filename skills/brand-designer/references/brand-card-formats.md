# Brand Documentation Formats: Comparison & Selection Guide

Brand identity documentation comes in multiple formats. The right choice depends on team size, update frequency, technical sophistication, and audience.

## Format Options

### 1. Online Brand Guidelines (Web/Frontify/Zeroheight)

**Best for:** Growing to enterprise teams that update frequently (>2x/year)

| Factor | Assessment |
|--------|-----------|
| Update speed | Instant — single source of truth updates for everyone |
| Asset delivery | Embedded downloads — no separate file hosting needed |
| Searchability | Full-text search + deep-linkable sections |
| Interactivity | Video, interactive examples, click-to-copy color codes |
| Governance | Roles, permissions, analytics, version history |
| Cost | Platform subscription ($500-$5K/yr) or custom development |
| Technical skill | Medium — content management, no coding required |
| Offline access | No |

**Examples:** Bang & Olufsen (Frontify), Trustpilot (Frontify), Sinch (Frontify), IBM, Cash App

### 2. PDF Brand Book

**Best for:** Small teams, agency deliverables, static identities that rarely change

| Factor | Assessment |
|--------|-----------|
| Update speed | Slow — re-export from InDesign/Figma, re-upload, renotify |
| Asset delivery | Static — files must be downloaded separately |
| Searchability | Limited — reader search only, no cross-linking |
| Interactivity | None — static pages |
| Governance | Manual version control (filename conventions) |
| Cost | Design tool subscription only |
| Technical skill | Medium — InDesign/Figma/Illustrator |
| Offline access | Yes — downloadable, printable |

**Examples:** Most agency client deliverables, some small-company brand books

### 3. Notion / Google Docs / Wiki

**Best for:** Early-stage startups, internal-only documentation

| Factor | Assessment |
|--------|-----------|
| Update speed | Fast — anyone can edit |
| Asset delivery | Embedded previews + download links |
| Searchability | Native platform search |
| Interactivity | Comments, embeds, checklists |
| Governance | Page-level permissions |
| Cost | Free to low (<$50/user/mo) |
| Technical skill | Low |
| Offline access | Limited |

**Examples:** Early-stage startups before they invest in a formal brand portal

### 4. Figma / Design Tool Libraries

**Best for:** Design-team-internal documentation tightly coupled to design tools

| Factor | Assessment |
|--------|-----------|
| Update speed | Fast — design tokens in component libraries |
| Asset delivery | Direct — designers consume in tool |
| Searchability | Figma search |
| Interactivity | Interactive components, prototyping |
| Governance | Figma permissions, library publishing |
| Cost | Figma subscription |
| Technical skill | High — requires design tool proficiency |
| Offline access | Limited |

**Examples:** Design system teams that keep brand documentation inside their tooling

### 5. CLI-Generated / Markdown + Compiler

**Best for:** Developer-friendly teams, vault-based knowledge management, open-source projects

| Factor | Assessment |
|--------|-----------|
| Update speed | Fast — edit markdown, recompile |
| Asset delivery | Referenced by path, compiled in |
| Searchability | grep/full-text search on markdown |
| Interactivity | None in markdown; HTML output can include CSS |
| Governance | Git-based — PRs, version tags, changelogs |
| Cost | Free |
| Technical skill | Medium — markdown + CLI |
| Offline access | Yes — plain text files |

**Examples:** This skill's output format, designlang's generated brand books

### 6. Brand Card Image (Single Visual)

**Best for:** Press kits, social media, stakeholder presentations, quick reference

| Factor | Assessment |
|--------|-----------|
| Update speed | Slow — regenerate when identity changes |
| Asset delivery | Single image file |
| Searchability | None — it's an image |
| Interactivity | None |
| Governance | Manual |
| Cost | Free |
| Technical skill | Low — use the `generate` script |
| Offline access | Yes |

**Examples:** Nous-branding card, groktopus-branding card, most press kit brand sheets

## Decision Matrix

| Your situation | Recommended format | Why |
|----------------|-------------------|-----|
| Solo founder, pre-revenue | Brand card image + Notion | Fast, free, covers 80% of needs |
| Small team (<10), one brand | Brand card + PDF | Simple to produce, easy to share |
| Growing team (10-50), multiple channels | Online guidelines + spec docs | Single source of truth, instant updates |
| Agency delivering to client | PDF brand book + design source files | Client expects a deliverable, source files enable future edits |
| Developer-facing product brand | CLI-generated markdown + design tokens | Devs prefer markdown; tokens integrate with code |
| Enterprise, global, many partners | Online guidelines (Frontify/Zeroheight) + compiled brand book PDF | Access control, analytics, partner self-service |
| Open source project | Markdown + generated brand card | Git-based, low barrier, low cost |

## Hybrid Approach

Most mature brands use **multiple formats** for different audiences:

| Audience | Format | Depth |
|----------|--------|-------|
| Executive / board | Brand card image + strategy memo | One-pager |
| Design team | Figma library + online guidelines | Full spec |
| Engineering team | Design tokens + markdown spec | Structured data |
| Marketing / content | Online guidelines + voice spec | Practical rules |
| External agencies | Compiled brand book PDF | All-in-one reference |
| Press / partners | Brand card image + press kit | Visual summary |

## Format Transition Path

```
Startup              Growing                  Scaling               Enterprise
──────               ───────                  ───────                ─────────
Brand card     →     Brand card          →   Online guidelines  →   Online guidelines
Notion/Google Docs   + spec docs (markdown)    + compiled PDF        + design system tokens
                     + Figma (design team)     + asset inventory     + global localization
```
