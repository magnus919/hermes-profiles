# Intellectual Lineage: Progressive Disclosure in Software Architecture Documentation

The Artifact Pyramid applies progressive disclosure to what AI agents produce. But the principle was independently discovered (under different names) by software architecture documentation methodology over 30 years. This reference traces that lineage and clarifies what the Artifact Pyramid generalizes beyond what architecture already found.

## The Six Discoveries (Chronological)

| Year | Methodology | Their Word for Progressive Disclosure | What They Built |
|------|-------------|--------------------------------------|-----------------|
| 1995 | Kruchten's 4+1 Views | "concurrent views," "partial expression" | Role-based information partitioning by stakeholder |
| 2000 | IEEE 1471 / ISO 42010 | "viewpoints," "stakeholder concerns" | Formal standard: views are "partial expressions" of architecture |
| 2002 | Views and Beyond (SEI/Clements) | "view selection," "scoping" | Systematic process for choosing which views to produce |
| 2005 | Rozanski & Woods | "viewpoints framework" | Audience-targeted viewpoint selection |
| 2008 | arc42 | "tailoring," "lean/essential/thorough" | Three built-in depth modes + a Canvas "zip-version" |
| 2011 | ADRs (Nygard) | "small, modular documents" | Atomic decisions — read one at a time, chain as needed |
| ~2011 | C4 Model (Brown) | "zoom levels," "hierarchical abstractions" | Context → Container → Component → Code drill-down |

## The Key Distinctions

### Architecture's version: role-based, synchronous
Architecture view models partition information **by stakeholder role**. Different views exist simultaneously for different people. An executive sees the Context view; a developer sees the Component view. This is progressive disclosure as a *social coordination mechanism* — telling different stories to different audiences at the same time.

### Artifact Pyramid: role-based AND temporal
The Artifact Pyramid adds **temporal unfolding** — the same consumer (whether human or agent) gets more detail as they go deeper. This is progressive disclosure as a *consumption mechanism* — the same person or agent starts at the summary and drills in on demand.

Architecture discovered the first axis. The Artifact Pyramid adds the second.

### Domain scope
Architecture documentation covers structural visualization and decisions. The Artifact Pyramid covers the full delivery lifecycle: strategy → architecture → implementation → operations → learning. No architecture methodology has a broader scope.

### Consumer type
Architecture documentation assumes a *human* reader who can flip pages, open files, and decide what to read next. The Artifact Pyramid assumes an *agent* consumer — which changes the constraints entirely:
- Context windows and token budgets make progressive disclosure a **hard requirement**, not a convenience
- Agents are stateless between calls — each layer must be independently consumable
- Navigation must be explicit (SOURCES blocks with absolute paths), not implicit ("see chapter 4")

## What This Means

The architecture community validates that the mechanism works — 30 years of practice, thousands of teams, documented in IEEE standards. The Artifact Pyramid did not rediscover progressive disclosure. It:

1. **Named** a principle that architecture docs had stumbled toward without naming
2. **Generalized** it across the full lifecycle (not just structural views)
3. **Extended** it to temporal unfolding (not just role-based)
4. **Applied** it to a new domain (AI agent output) where it's a hard requirement, not an optimization

## Sources

### Vault (permanent knowledge base)

The full research with source excerpts, 9 supporting atoms, and methodology-by-methodology analysis lives in the Magnus v2 vault:

```
2 - Molecules/Intellectual Lineage of the Artifact Pyramid — Progressive Disclosure in Architecture Documentation.md
 -> Full synthesis: 9 atoms covering Kruchten (1995), IEEE 1471, C4 Model, arc42, ADRs, Views and Beyond, Rozanski & Woods. Source excerpts from each canonical source.
```

### Canonical URLs

### Vault (permanent knowledge base)

The full research with source excerpts, 9 supporting atoms, and methodology-by-methodology analysis lives in the Magnus v2 vault:

```
2 - Molecules/Intellectual Lineage of the Artifact Pyramid — Progressive Disclosure in Architecture Documentation.md
 -> Full synthesis with 9 atoms covering each methodology, source excerpts, and cross-cutting analysis
```

### Canonical URLs

- Kruchten (1995): https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf
- IEEE 1471: https://ieeexplore.ieee.org/document/875998
- ISO 42010: https://www.iso.org/obp/ui/en/#!iso:std:74393:en
- Views and Beyond (Clements et al.): https://www.pearson.com/en-us/subject-catalog/p/documenting-software-architectures-views-and-beyond/P200000000186/9780132488594
- arc42 template: https://docs.arc42.org/
- ADRs (Nygard, 2011): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- C4 Model: https://c4model.com
- Rozanski & Woods: https://www.viewpoints-and-perspectives.info/
