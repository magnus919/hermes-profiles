---
name: c4-diagramming
description: "C4 Model structural views — System Context, Container, Component, and Code diagrams. Maps C4 zoom levels to Artifact Pyramid layers (Context→L1, Container/Component→L2, Code→L3). Use when the technical-architect profile needs to produce structural architecture diagrams."
---

# C4 Diagramming

C4 Model for structural architecture visualization. Produces diagrams at four zoom levels, mapped into the artifact pyramid.

## C4-to-Pyramid Mapping

| C4 Level | Pyramid Layer | Path |
|----------|--------------|------|
| Level 1: System Context | L1 (Summary) | 01-summary/system-context.md |
| Level 2: Container | L2 (Analysis) | 02-analysis/structural-views/container.md |
| Level 3: Component | L2 (Analysis) | 02-analysis/structural-views/components.md |
| Level 4: Code | L3 (Dossiers) | 03-dossiers/code-level-detail.md |

C4 is the cleanest structural fit — its four-level hierarchy maps to the three pyramid layers with almost no translation, and Levels 2-3 both resolve to separate L2 analysis files.

## Authoring Formats

### Mermaid (Default for Quick Diagrams)

Use when you need a single diagram embedded in markdown. See the GitHub Rendering Constraint section below for C4-in-Mermaid compatibility notes.

### Structurizr DSL (Recommended for Long-Lived Projects)

Structurizr DSL is the C4 model's reference "models as code" implementation, created by Simon Brown. Define the entire architecture model in a single DSL file; all 4 C4 levels are generated from it. This ensures structural consistency across diagrams that hand-written Mermaid cannot guarantee.

```
workspace {
    model {
        user = person "Customer"
        system = softwareSystem "Your System" {
            webapp = container "Web Application" "TypeScript, React"
            api = container "API" "Go"
            db = container "Database" "PostgreSQL"
            user -> webapp "Uses"
            webapp -> api "Makes API calls"
            api -> db "Reads/writes"
        }
    }
    views {
        systemContext system { include * autolayout lr }
        container system { include * autolayout lr }
        component api { include * autolayout lr }
        theme default
    }
}
```

**Key capabilities:**
- `!adrs docs/adr` — imports Architecture Decision Records (adr-tools, MADR, log4brains) into the workspace, rendered alongside C4 diagrams
- `!docs docs/arc42` — imports arc42 documentation as Markdown/AsciiDoc
- Structurizr Lite (Docker) — local preview at http://localhost:8081
- CI commands: `validate`, `inspect`, `export` (PlantUML, Mermaid, static site)

Full reference in `references/architecture-as-code-ecosystem.md` — tool comparison, DSL cookbook, C4-PlantUML alternative, and the converged repo convention.

## Contents

- `references/c4-levels.md` — per-level detail: purpose, audience, what to model, pitfalls
- `references/c4-to-pyramid-mapping.md` — context→L1, container/component→L2, code→L3 (Mermaid + Structurizr DSL paths)
- `references/c4-to-flowchart.md` — (in `mermaid-diagrams` skill) C4 → standard flowchart conversion patterns for GitHub compatibility
- `references/architecture-as-code-ecosystem.md` — Structurizr DSL, C4-PlantUML, docToolChain, converged repo convention, tool comparison table
- `references/ci-pipeline-templates.md` — GitHub Actions, GitLab CI, ForgeJo (Gitea Actions, Woodpecker) pipeline templates for Structurizr validation, export, deploy

## GitHub Rendering Constraint

GitHub's built-in Mermaid renderer does **not** bundle the C4 plugin (`@mermaid-js/mermaid`). Any ````mermaid` block using `C4Context`, `C4Container`, or `C4Component` syntax renders as raw code rather than a diagram on GitHub. This affects issues, PR descriptions, discussion comments, and markdown files.

**Workaround:** Convert C4 diagrams to standard `flowchart` syntax before embedding in GitHub markdown:
- `Person()` → `[rect]` node with label
- `System()` / `System_Ext()` → `[rect]` inside or outside subgraphs
- `Container()` → `[rect` with tech stack label]`
- `Db()` → `[(cylinder shape)]`
- `System_Boundary{}` / `Container_Boundary{}` → `subgraph ... end`
- `Rel()` → `-- label -->` or `-.->`
- Drop `UpdateLayoutConfig()` — use `flowchart LR` or `TB` directive instead

For the full conversion table with worked examples of all three C4 levels, load `skill_view(name='mermaid-diagrams', file_path='references/c4-to-flowchart.md')`.

**.mmd files in a DIAGRAMS/ directory** must also use standard flowchart syntax if they need to render via `mmdc` or on GitHub. Files using C4-plugin syntax can only render in tools that bundle the plugin (e.g., Mermaid Live Editor, mmdc with C4 extension config). If you commit `.mmd` files with C4 syntax to a repo, GitHub's file preview will show them as raw text — convert them to standard syntax or render them to PNG first.

## Feature Request Filed

A GitHub Community feature request to bundle the C4 mermaid plugin was filed at https://github.com/orgs/community/discussions/197898 (closed — requires submission through the web UI with the Apps, API and Webhooks discussion template). If this gets implemented, the flowchart conversions below would no longer be necessary for GitHub rendering.

## Canonical Reference

- Simon Brown, "The C4 Model" — https://c4model.com/
- Magnus Hedemark, "Clanker Technical Architect: First on the Scene with Progressive Disclosure" — https://magnus919.com/2026/05/clanker-technical-architect-first-on-the-scene-with-progressive-disclosure/
- GroktoPlan C4 Diagrams (worked examples) — https://github.com/groktopus/groktoplan/blob/main/TECHNICAL_ARCHITECTURE.md
