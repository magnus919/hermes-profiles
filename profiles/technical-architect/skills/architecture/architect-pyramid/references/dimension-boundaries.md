# Dimension Boundaries

Defines which fact lives in which file and how files cross-reference each other.

## File Boundaries

| File | Contains | Does NOT contain |
|------|----------|-----------------|
| system-context.md | System boundary, external actors, key interactions | Internal component details, decision rationale, constraints |
| container.md | Service boundaries, data stores, tech choices | Component internals, ADRs, code details |
| components.md | Module responsibilities, interfaces | Container topology, code-level details, ADR rationale |
| architecture-decisions/ADR-NNN.md | Decision context, options, consequences | Structural descriptions, constraint details |
| constraints-and-context.md | Quality goals, constraints, stakeholder needs | Solution strategy, structural diagrams |
| code-level-detail.md | Class diagrams, interface definitions | Component responsibilities, container topology |

## ADR Lifecycle States in the Pyramid

ADRs flow through the pyramid as they progress through their lifecycle:

| Lifecycle Stage | Pyramid Layer | ADR Status | Allowed |
|---|---|---|---|
| Initiating → Researching → Evaluating | L2 (02-analysis/) | `proposed` | Being discussed, not yet final |
| Implementing → Maintaining | L2 (02-analysis/) | `accepted` | Final decision, actively used |
| Superseded / Deprecated / Rejected | L3 (03-dossiers/) | `superseded`, `deprecated`, `rejected` | Historical only |

**Rule:** All live ADRs (proposed + accepted) live in L2. Only historical ADRs move to L3. This prevents stale/rejected decisions from cluttering active analysis while preserving full history.

**Immutability vs living documents:** The physical movement model (L2→L3 on superseded) assumes the **immutable ADR** approach — once accepted, an ADR is never edited; a new ADR supersedes the old one. Some teams prefer a **living document** approach where ADRs are updated in-place with date-stamped additions. In that case, ADRs don't physically move between layers — the status field changes within the same file, and the L1 index reflects the current status. The pyramid structure supports both: the L3 `adr-superseded.md` file becomes a compilation of status-only entries (living document) rather than relocated files (immutable). Choose the model at project setup and document the choice in the ADR index README.

## Cross-Reference Rules

1. **structural-views/*.md → architecture-decisions/:** Every component links to the ADR that explains its structure
2. **architecture-decisions/*.md → constraints-and-context.md:** Every decision references the quality attribute or constraint that drove it
3. **constraints-and-context.md → structural-views/:** Every constraint links to the C4 diagram showing how it's realized
4. **No layer-crossing references within the same dimension:** C4 views don't reference C4 views across layers; ADRs don't reference ADRs across layers
5. **Lifecycle transitions must update pyramid location:** When an ADR moves from `accepted` to `superseded`, it physically moves from L2 to L3. The L1 adr-index.md is updated to reflect the new location. (Note: this applies to the immutable model. In the living document model, the file stays in place and only the status changes.)

## ADR Lifecycle Awareness

| Status | References Valid? | Consumer |
|--------|-------------------|----------|
| `proposed` | Yes — linked from C4 views as tentative | Engineers evaluating the decision |
| `accepted` | Yes — linked from C4 views as definitive | Implementers, reviewers |
| `deprecated` / `superseded` | No — moved to L3, C4 views relink to replacement | Historians, challengers |
| `rejected` | No — moved to L3 with rejection rationale | Auditors |

When a C4 component links to an ADR, verify the ADR's status before treating the link as authoritative. Superseded ADRs are evidence of the path not taken, not the current structure.
