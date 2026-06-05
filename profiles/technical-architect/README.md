# Technical Architect — Hermes Profile

Systems architecture specialization for Hermes Agent. Designs service boundaries, API contracts, deployment topologies, and produces architecture documentation using the **artifact pyramid** output format.

## What This Profile Provides

- **C4 Model** — structural views at 4 zoom levels (System Context, Container, Component, Code)
- **ADRs** — architecture decision records with lifecycle management and 11 template formats
- **arc42** — system constraints, quality attributes, and deployment context
- **Artifact pyramid** — all three methodologies composed into a single progressively-disclosable output

## Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com/) installed and configured
- The following skills installed (see Installation below)

## Installation

```bash
# Clone the profiles repo
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles

# Copy the profile
cp -r ~/hermes-profiles/profiles/technical-architect ~/.hermes/profiles/

# Install required skills
hermes skills install artifact-pyramids
hermes skills install c4-diagramming
hermes skills install adr-authoring
hermes skills install arc42-context
hermes skills install architect-pyramid
hermes skills install mermaid-diagrams

# Recommended (but optional)
hermes skills install groktocrawl
hermes skills install searxng-cli
hermes skills install github-issues
hermes skills install github-pr-workflow

# Switch to the profile
hermes --profile technical-architect
```

## Quick Start

Once the profile is loaded, give it an architecture prompt:

> "Design the service boundaries for a payment processing system handling 10K transactions per minute with PCI-DSS compliance requirements."

The profile will:
1. Discover constraints (latency, compliance, team structure)
2. Produce C4 structural views (Context → Container → Component)
3. Document key decisions as ADRs with alternatives considered
4. Layer in arc42 context (quality attributes, risks, deployment)
5. Output an artifact pyramid at `/tmp/architect-workflow/<project>/00-index.md`

## Skill Dependencies

Each required skill provides a specific capability. Load them in order when starting an engagement:

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure specification | `skill_view('artifact-pyramids')` |
| `c4-diagramming` | C4 structural views (Mermaid or Structurizr DSL) | `skill_view('c4-diagramming')` |
| `adr-authoring` | ADR lifecycle, 11 templates, fitness functions | `skill_view('adr-authoring')` |
| `arc42-context` | Constraints, quality attributes, risk/deployment docs | `skill_view('arc42-context')` |
| `architect-pyramid` | Output orchestrator, cross-referencing rules | `skill_view('architect-pyramid')` |
| `mermaid-diagrams` | Diagram rendering (used by c4-diagramming) | `skill_view('mermaid-diagrams')` |

### Supporting References (included in skills)

The skills bundle extensive reference material accessible via `skill_view()`:

- **AaC ecosystem** — Structurizr DSL, C4-PlantUML, docToolChain, converged repo convention, tool comparison (`c4-diagramming` skill, `references/architecture-as-code-ecosystem.md`)
- **CI pipeline templates** — GitHub Actions, GitLab CI, ForgeJo templates for automating architecture documentation generation (`c4-diagramming` skill, `references/ci-pipeline-templates.md`)
- **ADR format catalog** — 11 template formats with selection decision tree (`adr-authoring` skill, `references/adr-format.md`)
- **Fitness functions** — ArchUnit, AI-assisted, Structurizr CI as decisions-as-code (`adr-authoring` skill, `references/fitness-functions.md`)
- **Decision sustainability** — 5 criteria + 8 guidelines for ADR quality (`adr-authoring` skill, `references/decision-sustainability.md`)

## Output Format

All output follows the artifact pyramid convention:

```
<project>/
├── 00-index.md              ← Navigation + SOURCES
├── 01-summary/              ← C4 Context diagram, arc42 quality tree, ADR index
├── 02-analysis/             ← C4 Container/Component, active ADRs, arc42 sections 1-4
└── 03-dossiers/             ← C4 Code, superseded ADRs, arc42 sections 5-12
```

The response to any caller is the absolute path to `00-index.md`. Not a summary. Not a conversation. A path.

## Verification

A deployed technical-architect agent should pass these checks:

- [ ] Accepts an architecture prompt and produces an artifact pyramid
- [ ] Pyramid contains artifacts from all three methodologies (C4, ADRs, arc42)
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Each methodology is independently consumable
