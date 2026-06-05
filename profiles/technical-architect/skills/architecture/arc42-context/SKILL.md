---
name: arc42-context
description: "arc42 template — constraints and context documentation covering sections 1-4 (stakeholders, quality goals, constraints, solution strategy) and supplemental sections (architecture, risks, deployment, glossary). Maps arc42 sections to Artifact Pyramid layers (Canvas→L1, sections 1-4→L2, sections 5-12→L3). Use when the technical-architect profile needs to document system context and constraints."
---

# arc42 Context

arc42 template for documenting system constraints, context, and quality attributes. arc42 supplies the contextual dimension — constraints and quality attributes — that structure views (C4) and decision records (ADRs) alone don't capture.

## arc42-to-Pyramid Mapping

| arc42 Section | Pyramid Layer | Path |
|--------------|--------------|------|
| Canvas / Quality tree | L1 (Summary) | 01-summary/quality-tree.md |
| Sections 1-2: Goals, Constraints | L2 (Analysis) | 02-analysis/constraints-and-context.md |
| Section 4: Solution Strategy | L2 (Analysis) | 02-analysis/solution-strategy.md |
| Sections 5-8: Architecture | L3 (Dossiers) | 03-dossiers/arc42-supplemental.md |
| Sections 9-12: Risks, Deployment, Glossary | L3 (Dossiers) | 03-dossiers/arc42-supplemental.md |

Without arc42, an agent sees the solution but not the boundaries that define what constitutes a valid solution. Sections 1-4 in L2 provide the constraint envelope. Sections 5-12 in L3 provide the detailed implementation context.

## Contents

- `references/arc42-sections-1-4.md` — detailed guidance per section with example tables
- `references/arc42-to-pyramid-mapping.md` — constraints→L2, Canvas→L1, lean/essential/thorough modes

## Canonical Reference

- arc42 — https://arc42.org/
- Magnus Hedemark, "Clanker Technical Architect: First on the Scene with Progressive Disclosure" — https://magnus919.com/2026/05/clanker-technical-architect-first-on-the-scene-with-progressive-disclosure/
