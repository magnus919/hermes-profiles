# Architecture as Code (AaC) Ecosystem

Tools, conventions, and patterns for managing C4 model diagrams, arc42 documentation, and Architecture Decision Records (ADRs) together in a git repository.

## 1. Structurizr — C4 Reference Implementation

Structurizr is the official "models as code" tool for the C4 model, created by Simon Brown (the C4 model's author). You write a text-based DSL that defines your entire software architecture model; all diagrams are generated from that single model.

**Key website:** https://structurizr.com/ — **Docs:** https://docs.structurizr.com/

### Core Concepts

- **Workspace** — the top-level container. Holds a model + views + documentation + decisions.
- **Model** — defines elements (persons, software systems, containers, components) and their relationships.
- **Views** — selects subsets of the model for diagram rendering (system context, container, component, dynamic, deployment).
- **DSL** — text-based domain-specific language. Single source of truth. Git-friendly.

### Minimal Example (All Four C4 Levels)

```
workspace {

    model {
        user = person "Customer"
        system = softwareSystem "Internet Banking System" {
            webapp = container "Web Application" "TypeScript, React" {
                user -> this "Uses"
            }
            api = container "API" "Go" {
                webapp -> this "Makes API calls"
            }
            db = container "Database" "PostgreSQL" {
                api -> this "Reads/writes"
            }
        }
    }

    views {
        systemContext system {
            include *
            autolayout lr
        }
        container system {
            include *
            autolayout lr
        }
        component api {
            include *
            autolayout lr
        }
        theme default
    }

}
```

### The `!adrs` Keyword — Native ADR Integration

Structurizr can import Architecture Decision Records directly into the workspace:

```
workspace {

    !adrs docs/adr

    model { ... }
    views { ... }

}
```

This imports all Markdown files from `docs/adr/` using the adr-tools format by default. Supported formats:
- `adrtools` (default) — expects files matching adr-tools naming convention
- `madr` — for MADR-format ADRs
- `log4brains` — for log4brains-format ADRs

The ADRs are rendered in the Structurizr UI alongside the C4 diagrams. This is the tightest integration available between C4 and ADRs.

### The `!docs` Keyword — arc42 Documentation Import

```
workspace {

    !docs docs/arc42

    model { ... }
    views { ... }

}
```

Imports Markdown or AsciiDoc documentation (structured as arc42 sections) and renders them in the UI alongside diagrams and ADRs. Supports section-based navigation.

### Structurizr Lite — Local Preview

Docker container for rendering the full workspace in a browser:

```yaml
# docker-compose.yml
services:
  structurizr-lite:
    image: structurizr/lite
    ports:
      - "8081:8080"
    volumes:
      - ./docs/arch:/usr/local/structurizr
```

Access at `http://localhost:8081`. Shows C4 diagrams, arc42 documentation, and ADRs in a unified web UI with navigation.

### CI/CD Commands

```bash
# Validate DSL syntax and model consistency
structurizr-cli validate -w docs/arch/model/system.dsl

# Inspect for architectural drift
structurizr-cli inspect -w docs/arch/model/system.dsl

# Export diagrams to PlantUML
structurizr-cli export -w docs/arch/model/system.dsl -format plantuml

# Export diagrams to Mermaid
structurizr-cli export -w docs/arch/model/system.dsl -format mermaid

# Export to static HTML site
structurizr-cli export -w docs/arch/model/system.dsl -format site
```

### DSL Cookbook

Full tutorial guide: https://docs.structurizr.com/dsl/cookbook/

Topics covered: workspace structure, model elements, relationships, views, styling, themes, animations, deployment nodes, dynamic diagrams, filtering, properties, perspectives.

---

## 2. C4-PlantUML — Lighter Alternative

**Repo:** https://github.com/plantuml-stdlib/C4-PlantUML

PlantUML include files that add C4 semantics to standard PlantUML. No single-model consistency (each diagram is a separate file), but much lower learning curve than Structurizr.

### Function Reference

| Function | C4 Level | Purpose |
|---|---|---|
| `Person(alias, label, description)` | Any | External user or actor |
| `Person_Ext(alias, label, description)` | Context | External user (outside system boundary) |
| `System(alias, label, description)` | Context | Software system |
| `System_Ext(alias, label, description)` | Context | External software system |
| `Container(alias, label, tech, description)` | Container | Application container (web app, API, DB) |
| `Container_Boundary(alias, label)` | Container | Groups related containers |
| `Component(alias, label, tech, description)` | Component | Module within a container |
| `System_Boundary(alias, label)` | Context | Groups related systems |
| `Rel(from, to, label, tech)` | Any | Relationship between elements |
| `Rel_D(from, to, label, tech)` | Any | Relationship (dashed) |
| `Rel_Neighbor(from, to, label, tech)` | Any | Relationship rendering optimization |
| `UpdateLayoutConfig(c4ShapeInRow, c4BoundaryInRow)` | Any | Layout tuning |
| `LAYOUT_WITH_LEGEND()` | Any | Renders with automatic legend |

### Example

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(customer, "Customer")
System(system, "Your System", "Core platform")
System_Ext(external, "External Service", "Payment processor")

Rel(customer, system, "Uses")
Rel(system, external, "Charges via")
@enduml
```

### When to Choose Over Structurizr

| Situation | Choice |
|---|---|
| Team already uses PlantUML for other diagrams | C4-PlantUML (consistent toolchain) |
| Need a quick C4 diagram for an ad-hoc document | C4-PlantUML (no DSL learning curve) |
| Need consistent multi-diagram model across 4 C4 levels | Structurizr (single source of truth) |
| Want ADR integration in the diagram viewer | Structurizr (native `!adrs` support) |
| CI pipeline already has PlantUML | Either — Structurizr exports to PlantUML |

---

## 3. docToolChain — arc42 Build Pipeline

**Repo:** https://github.com/docToolchain/docToolchain

A Gradle-based docs-as-code toolchain purpose-built for arc42 documentation. Handles the full pipeline: AsciiDoc compilation, PlantUML diagram generation, PDF/HTML export, Confluence publishing.

### Key Capabilities

- **arc42 template management** — generates skeleton arc42 documentation with all 12 sections
- **AsciiDoc compilation** — converts `.adoc` source files to HTML, PDF, DocBook
- **PlantUML integration** — renders C4 diagrams (via C4-PlantUML includes) as part of the build
- **Confluence export** — publishes rendered docs to Confluence spaces via asciidoc2confluence
- **Gradle task hierarchy** — `generateHTML`, `generatePDF`, `exportConfluence` as standard tasks

### Directory Structure Convention

```
docs/
├── src/
│   ├── arc42/
│   │   ├── 01_introduction_and_goals.adoc
│   │   ├── ...
│   │   └── 12_glossary.adoc
│   └── images/
├── build/              ← Generated output
├── build.gradle        ← docToolChain configuration
└── gradle.properties
```

### When to Use

docToolChain is for organizations that want a **standardized, build-pipeline-driven** approach to arc42 documentation. It adds ceremony (Gradle build, strict directory structure) in exchange for consistent output formats and Confluence integration. For teams that just want C4 diagrams with ADRs, Structurizr is lighter.

---

## 4. Converged Repo Convention

The AaC community has converged on a standard directory structure for combining C4, arc42, and ADRs in a single git repository. Multiple reference implementations use the same pattern:

### Directory Structure

```
docs/arch/
├── model/
│   ├── system.dsl                ← Structurizr DSL (the architecture model)
│   └── deployment/               ← Deployment-specific views (dev, staging, prod)
│       ├── dev.dsl
│       └── live.dsl
├── src/                          ← arc42 12-section template
│   ├── 01_introduction_and_goals.adoc
│   ├── 02_constraints.adoc
│   ├── 03_system_scope_and_context.adoc
│   ├── 04_solution_strategy.adoc
│   ├── 05_building_block_view.adoc
│   ├── 06_runtime_view.adoc
│   ├── 07_deployment_view.adoc
│   ├── 08_crosscutting_concepts.adoc
│   ├── 09_architecture_decisions.adoc
│   ├── 10_quality_requirements.adoc
│   ├── 11_technical_risks.adoc
│   └── 12_glossary.adoc
├── adr/                          ← Architecture Decision Records
│   ├── 0001-record-architecture-decisions.md
│   ├── 0002-use-postgresql.md
│   ├── 0003-adopt-event-sourcing.md
│   └── README.md                 ← ADR index with status table
├── images/                       ← Embedded screenshots, diagrams
├── README.md                     ← Project overview
└── docker-compose.yml            ← Structurizr Lite
```

### How the Three Methodologies Relate

| Component | Purpose | Created By | Consumed By |
|---|---|---|---|
| `model/system.dsl` | C4 model (all levels) | Technical architect | Structurizr renders 4 diagrams |
| `src/09_architecture_decisions.adoc` | arc42 decision section | Technical architect | Humans reading arc42 docs |
| `adr/0002-use-postgresql.md` | Full ADR content | Technical architect | Structurizr imports via `!adrs` |
| `docker-compose.yml` | Local preview | Team | `docker compose up` → browser |

### Reference Implementations

- **dzimchuk/architecture-as-code** — Structurizr DSL + arc42 AsciiDoc + ADRs + Docker Compose. The cleanest minimal example. https://github.com/dzimchuk/architecture-as-code
- **milanm/architecture-docs** — Same approach but with PlantUML diagram export and GitHub Pages CI. https://github.com/milanm/architecture-docs
- **bitsmuggler/arc42-c4-example** — arc42 template filled out for an Internet Banking System. https://bitsmuggler.github.io/arc42-c4-software-architecture-documentation-example/

---

## 5. Tool Comparison

| Criteria | Structurizr | C4-PlantUML | Mermaid |
|---|---|---|---|
| **Model consistency** | Single model → all 4 diagrams | Per-file includes | Per-file manual |
| **Learning curve** | Medium (DSL syntax) | Low (PlantUML) | Low |
| **ADR integration** | Native (`!adrs` keyword) | None | None |
| **arc42 integration** | Native (`!docs` keyword) | None | None |
| **CI readiness** | CLI + Docker image | PlantUML CLI | `mmdc` CLI |
| **GitHub rendering** | No (needs Structurizr viewer) | Via PlantUML GitHub Action | Native (if flowchart syntax) |
| **Local preview** | Structurizr Lite (Docker) | PlantUML server | VS Code plugins |
| **Layout** | Auto + manual (drag to arrange) | Auto only | Auto via `---` direction |

## 6. Further Reading

- Structurizr DSL cookbook: https://docs.structurizr.com/dsl/cookbook/
- Structurizr DSL language reference: https://docs.structurizr.com/dsl/language
- Structurizr ADR integration: https://docs.structurizr.com/dsl/adrs
- Structurizr "as code" philosophy: https://docs.structurizr.com/as-code
- C4-PlantUML: https://github.com/plantuml-stdlib/C4-PlantUML
- docToolChain: https://github.com/docToolchain/docToolchain
- dzimchuk AaC example: https://github.com/dzimchuk/architecture-as-code
- milanm AaC example: https://github.com/milanm/architecture-docs
- CI pipeline templates (GitHub Actions, GitLab CI, ForgeJo): `references/ci-pipeline-templates.md`
