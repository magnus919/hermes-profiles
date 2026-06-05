# Technical-Architect Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the technical-architect Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Design the architecture for..." | Full engagement: constraints → C4 views → ADRs → arc42 → pyramid |
| "Compare these technology options..." | ADR-focused: produce a MADR-format decision record with options analysis |
| "What are the service boundaries?" | C4-focused: system context → container decomposition |
| "Document the architecture decisions" | ADR backlog: capture existing decisions as ADRs |
| "How should this system be deployed?" | Deployment-focused: C4 deployment view + arc42 deployment section |
| "Run an architecture review" | Audit: validate existing architecture against ADRs and fitness functions |

## Loading Order

When starting an architecture engagement, load skills in this sequence:

```python
skill_view('c4-diagramming')     # 1. Structural methodology
skill_view('adr-authoring')      # 2. Decision methodology
skill_view('arc42-context')      # 3. Constraints methodology
skill_view('architect-pyramid')  # 4. Output orchestrator — must be last
```

This order ensures that by the time the orchestrator loads, you know what C4,
ADRs, and arc42 are capable of producing.

## Output Contract

The profile produces architecture documentation as an artifact pyramid. The
response to the caller is always the **absolute path to `00-index.md`** at the
pyramid root. Not a summary. Not a natural-language handoff. Not a conversation.

### Expected Structure

```
<project>/
├── 00-index.md              ← Navigation index with SOURCES
├── 01-summary/
│   ├── system-context.md    ← C4 Level 1
│   ├── quality-tree.md      ← arc42 Canvas
│   └── adr-index.md         ← ADR navigation with lifecycle status
├── 02-analysis/
│   ├── structural-views/
│   │   ├── container.md     ← C4 Level 2
│   │   └── components.md    ← C4 Level 3
│   ├── architecture-decisions/
│   │   └── ADR-001.md       ← Active ADRs
│   ├── constraints-and-context.md  ← arc42 sections 1-2
│   └── solution-strategy.md        ← arc42 section 4
└── 03-dossiers/
    ├── code-level-detail.md ← C4 Level 4
    ├── adr-superseded.md    ← Superseded/deprecated ADRs
    └── arc42-supplemental.md← arc42 sections 5-12
```

### Cross-Reference Rules

When producing any artifact, verify these cross-references:

1. **C4 views must reference ADRs** — every Container and Component diagram links
   to the ADR that explains its structure
2. **ADRs must reference arc42 constraints** — every decision links to the
   quality attribute or constraint that drove it
3. **arc42 constraints must reference C4 views** — every constraint links to the
   C4 diagram showing how it's realized
4. **SOURCES sections at every layer** — absolute paths with descriptions, not
   footnotes
5. **ADR lifecycle awareness** — only `accepted` ADRs are authoritative.
   `proposed` ADRs are tentative. Superseded ADRs must be relinked.

## Handoff Protocol

When passing work to another agent or returning to a human:

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. If the engagement is multi-phase, each phase produces its own pyramid.
   The L3 dossiers of phase N serve as context for phase N+1.
3. Partial pyramids are acceptable. If only C4 is requested (no ADRs, no
   arc42), produce only the structural layers. Do not create empty
   directories for missing methodologies.

## Supporting References

The skills this profile loads include extensive reference material:

| Reference | Skill | File |
|---|---|---|
| AaC ecosystem (Structurizr, C4-PlantUML, docToolChain) | c4-diagramming | `references/architecture-as-code-ecosystem.md` |
| CI pipeline templates (GitHub, GitLab, ForgeJo) | c4-diagramming | `references/ci-pipeline-templates.md` |
| ADR template catalog (11 formats) | adr-authoring | `references/adr-format.md` |
| Fitness functions (decisions as code) | adr-authoring | `references/fitness-functions.md` |
| Decision sustainability (5 criteria) | adr-authoring | `references/decision-sustainability.md` |
| Pyramid mapping (C4-to-pyramid) | c4-diagramming | `references/c4-to-pyramid-mapping.md` |
| Dimension boundaries (cross-reference rules) | architect-pyramid | `references/dimension-boundaries.md` |

Load these with `skill_view(<skill>, file_path=<path>)` when depth is needed.

## Related Profiles

The technical-architect profile is designed to work alongside:

- **data-architect** — owns data model and pipeline architecture. Handoff: pyramid path. The technical-architect's constraint envelope feeds the data model.
- **product-manager** — translates product requirements into architectural constraints. Receives pyramid L1 (summary) as input; provides requirements as constraints for L2 analysis.
- **implementation-planner** — consumes the architecture pyramid to produce implementation plans. Receives the full pyramid path as input.
