# C4-to-Pyramid Mapping

## Mapping Table

| C4 Level | Pyramid Layer | Mermaid Path | Structurizr DSL Path | Consumer |
|----------|--------------|--------------|----------------------|----------|
| Level 1: System Context | **L1** (01-summary/) | 01-summary/system-context.md | `docs/arch/model/system.dsl` (systemContext view) | Any stakeholder needing the big picture |
| Level 2: Container | **L2** (02-analysis/) | 02-analysis/structural-views/container.md | `docs/arch/model/system.dsl` (container view) | Developers, integrators |
| Level 3: Component | **L2** (02-analysis/) | 02-analysis/structural-views/components.md | `docs/arch/model/system.dsl` (component view) | Component developers |
| Level 4: Code | **L3** (03-dossiers/) | 03-dossiers/code-level-detail.md | `docs/arch/model/system.dsl` (code view) | Implementers, code reviewers |

**Note on Structurizr DSL paths:** All four C4 levels are defined in a single `system.dsl` file. The `system.dsl` path is the same for all levels because Structurizr generates all diagrams from one model. The difference is which **view** is rendered: `systemContext` for L1, `container` for L2, `component` for L3, `code` for L4. See `references/architecture-as-code-ecosystem.md` for the full Structurizr reference.

## Why C4 Maps Cleanly

C4 is the only architecture methodology with a built-in depth hierarchy. Its four zoom levels correspond naturally to the three pyramid layers (with Levels 2-3 both resolved as separate L2 analysis files). No other methodology maps this cleanly.

## Key Principle

C4 is fundamentally a visual notation. It communicates structure to someone who already understands the domain. It does NOT communicate rationale (that's ADRs) or constraints (that's arc42). The three methodologies are complementary, not competitive.
