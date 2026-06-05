---
name: architect-pyramid
description: "Output orchestrator for the technical-architect profile — maps C4 structural views, ADR decision records, and arc42 constraints into a unified artifact pyramid. Manages the pyramid structure, cross-referencing rules, and handoff convention. Load after c4-diagramming, adr-authoring, and arc42-context."
---

# Architect Pyramid

Output orchestrator for the technical-architect profile. Takes structural views (C4), decision records (ADRs), and context/constraint documentation (arc42) and assembles them into a single artifact pyramid.

## Pyramid Output Structure

```
<project>/
├── 00-index.md
├── 01-summary/
│   ├── system-context.md          ← C4 Level 1 (System Context diagram)
│   └── quality-tree.md            ← arc42 Canvas / quality attributes
├── 02-analysis/
│   ├── structural-views/
│   │   ├── container.md           ← C4 Level 2 (Container diagram)
│   │   └── components.md          ← C4 Level 3 (Component diagram)
│   ├── architecture-decisions/
│   │   └── ADR-001.md             ← Active ADRs (one per decision)
│   ├── constraints-and-context.md ← arc42 sections 1-2 (goals, constraints)
│   └── solution-strategy.md       ← arc42 section 4
└── 03-dossiers/
    ├── code-level-detail.md       ← C4 Level 4 (Code diagram)
    ├── adr-superseded.md          ← Superseded ADRs
    └── arc42-supplemental.md      ← arc42 sections 5-12 (risks, deployment, glossary)
```

## Cross-Referencing Rules

1. **C4 views reference ADRs** — every Container and Component diagram links to the ADRs that explain why they're structured that way
2. **ADRs reference arc42 constraints** — every decision log links to the arc42 quality attribute or constraint that drove the decision
3. **arc42 constraints reference C4 views** — every constraint entry links to the C4 diagram that shows how the constraint is realized
4. **SOURCES sections at every layer** — absolute paths with descriptions, not footnotes
5. **ADR lifecycle awareness** — C4 views should only reference `accepted` ADRs as authoritative. Links to `proposed` ADRs should be marked tentative. When an ADR is superseded, C4 views must relink to the replacement — see `references/dimension-boundaries.md` for the full lifecycle table.

## Related Approach: Architecture as Code (AaC) Repo Convention

The artifact pyramid is the right output format for **agent-driven architecture work** — the consumer is another agent or the pyramid serves as a one-time analysis deliverable at `/tmp/architect-workflow/`.

For teams that need **long-lived, tool-rendered architecture documentation** in a git repo, the AaC community has converged on a Structurizr-based convention that combines C4 + ADRs + arc42 in a single repository with Docker preview.

### Mapping: Pyramid → AaC Convention

| Pyramid Layer | Pyramid File | AaC Convention |
|---|---|---|
| L1 (Summary) | 01-summary/system-context.md | `model/system.dsl` (C4 Level 1 via Structurizr) |
| L1 (Summary) | 01-summary/quality-tree.md | `src/10_quality_requirements.adoc` (arc42) |
| L2 (Analysis) | 02-analysis/structural-views/container.md | `model/system.dsl` (C4 Level 2 via Structurizr) |
| L2 (Analysis) | 02-analysis/architecture-decisions/ADR-NNN.md | `adr/NNNN-title.md` (adr-tools format) |
| L2 (Analysis) | 02-analysis/constraints-and-context.md | `src/01_introduction.adoc` + `02_constraints.adoc` |
| L3 (Dossiers) | 03-dossiers/code-level-detail.md | `model/system.dsl` (C4 Level 4 via Structurizr) |
| L3 (Dossiers) | 03-dossiers/arc42-supplemental.md | `src/05`-`12` (remaining arc42 sections) |

### When to Use Each

| Situation | Recommendation |
|---|---|
| Agent-driven analysis, single engagement, no Docker | **Artifact pyramid** — no tooling dependencies, portable, agent-native |
| Team maintaining docs in a repo, wants local preview | **AaC convention** — Structurizr Lite for `docker compose up`, CI for publishing |
| Mixed: agent produces initial docs, team maintains long-term | Produce pyramid first → if team adopts it, migrate to AaC structure |

Full reference in `references/architecture-as-code-ecosystem.md` (c4-diagramming skill).

## Handoff Convention

The response to any caller is the absolute path to `00-index.md`. Not a summary. Not a natural-language handoff. A path.

```
metadata={"artifact": "/tmp/architect-workflow/<slug>/00-index.md"}
```

## Contents

- `references/pyramid-handoff-convention.md` — kanban API, delegate_task, quality gate checklist
- `references/dimension-boundaries.md` — which fact lives in which file, cross-reference rules, ADR lifecycle states and awareness table, immutable vs living document model note

## Canonical Reference

- Magnus Hedemark, "Clanker Technical Architect: First on the Scene with Progressive Disclosure" — https://magnus919.com/2026/05/clanker-technical-architect-first-on-the-scene-with-progressive-disclosure/
