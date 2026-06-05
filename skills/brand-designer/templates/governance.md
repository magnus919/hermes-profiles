---
type: brand-governance-template
name: Brand Governance Framework Template
description: >-
  Define how the brand is maintained, versioned, and evolved. Covers version
  numbering, stewardship, review cadence, exception process, changelog, and
  archive policy. Essential for scaling brands with multiple contributors.
---

# Brand Governance: {{brand}}

## Version Numbering

**Scheme:** `MAJOR.MINOR.PATCH`

| Bump | When | Example |
|------|------|---------|
| **MAJOR** | Complete brand redesign (logo change, new palette, new type) | `1.0.0` → `2.0.0` |
| **MINOR** | Palette expansion, typeface addition, new logo variant | `1.0.0` → `1.1.0` |
| **PATCH** | Documentation fix, example update, typo correction | `1.0.0` → `1.0.1` |

**Current version:** `{{1.0.0}}`

## Brand Steward

| Field | Value |
|-------|-------|
| **Owner** | {{Name}} |
| **Role** | {{Title}} |
| **Contact** | {{email@example.com}} |

The brand steward is the single point of accountability for brand consistency.
All exception requests route through this person.

## Review Cadence

| Cadence | Activity |
|---------|----------|
| **{{Quarterly}}** | {{Scheduled comprehensive review}} |
| **{{Annually}}** | {{Full brand audit across all channels}} |

### Trigger Events (off-cycle review)

- Logo refresh or evolution
- Merger, acquisition, or rebranding
- New product launch with distinct sub-brand
- Market expansion into new region/culture
- Consistent brand drift detected in audit

## Exception Process

When a team needs to deviate from brand guidelines:

1. **Submit** — Fill out the exception request form detailing the deviation, rationale, and duration
2. **Review** — Brand steward evaluates within {{5}} business days
3. **Approve/Deny** — Approved exceptions are logged with expiration date; denied requests get alternative guidance
4. **Log** — All exceptions recorded in changelog for quarterly review

**Approval chain:**
- Standard exceptions → Brand steward
- High-visibility exceptions (homepage, major campaign) → Brand steward + VP Marketing

## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {{YYYY-MM-DD}} | {{0.1.0}} | {{Initial brand identity documentation}} | {{Name}} |
| {{YYYY-MM-DD}} | {{1.0.0}} | {{First published version}} | {{Name}} |
| | | | |

## Archive Policy

- **Retention:** Current version + {{2}} previous major versions
- **Disposal:** Archived assets moved to `/archive/` directory
- **Access:** Archived versions still accessible via changelog but clearly marked as superseded

---

*This governance framework documents how [[{{Brand Name}}]] is maintained. See [[{{Brand Name}} Asset Inventory]] for the file index.*
