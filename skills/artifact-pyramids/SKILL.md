---
name: artifact-pyramids
description: >-
  Progressive disclosure for what AI agents produce. Structure research outputs
  across three layers of increasing depth — Summary (key findings), Analysis
  Collection (per-dimension files), and Detailed Dossiers (source excerpts,
  raw data, transcripts) — so downstream agents and humans consume only as
  deeply as they need. Load this skill when organizing research outputs,
  building multi-agent research pipelines, or designing agent collaboration
  protocols.
license: MIT
compatibility: Agent-agnostic — concepts apply to any AI agent workflow. Scripts require Python 3.9+ and a POSIX shell.
metadata:
  spec-version: "0.0.3"
  source: https://github.com/groktopus/artifact-pyramids
  canonical-article: https://www.groktop.us/artifact-pyramid-progressive-disclosure/
---

# Artifact Pyramids for Agentic AI Research

Progressive disclosure governs how we feed agents context: metadata at startup, instructions on activation, resources on demand. **The Artifact Pyramid applies the same principle to what agents produce.** Three layers of increasing depth, each independently consumable, each linking down to the next.

## Loading Guidance

**When producing an artifact pyramid, load these references as a required set (not piecemeal):**

| Reference | File |
|-----------|------|
| Pipeline Stages — layer definitions, navigation format, production flow | `references/pipeline-stages.md` |
| Output Classification Framework — role-agnostic content contracts, 00-index/L1 boundary | `references/output-classification-framework.md` |
| Quality Gates — verification checklists per layer | `references/quality-gates.md` |
| Delegation Context Template — exact text for subagent output mandates | `references/delegation-context-template.md` |

These four define complementary aspects of the spec that the others assume. Loading only a subset risks violating content contracts (e.g., putting findings in 00-index) or skipping required navigation affordances. Load the full set before writing any pyramid files.

The reference table below describes *when* to load each file; the four above are **always required** for pyramid production. The remaining references (framework, worked example, canonical article, intellectual lineage, provenance, composite synthesis) are supplementary — load when the task calls for conceptual depth or a worked pattern.

## The Pyramid

```
      ┌──────────────┐
      │  L1 SUMMARY  │  One file: research question, key findings,
      │    🎯        │  most important implications. Links to L2 files.
      └──────┬───────┘
      ┌──────┴───────┐
      │  L2 ANALYSIS │  Per-dimension files: market, competitive,
      │  COLLECTION  │  technical feasibility, risk. Self-contained,
      │   🧩        │  each links to L3 dossiers.
      └──────┬───────┘
      ┌──────┴───────┐
      │  L3 DOSSIERS │  Source excerpts, raw data tables, interview
      │    📦        │  transcripts, methodology notes. Reference
      └──────────────┘  library, pulled on demand.
```

The pyramid is consumed top-down but produced via recursive gap analysis: start with the summary, embed links to analysis files, write analysis files that link to dossiers, and evaluate after each round whether gaps remain.

**Layer numbering is top-down** — L1 is the most distilled layer (the entry point), L3 is the most detailed (pulled on demand). This mirrors the Agent Skills input model: metadata (L1) → instructions (L2) → resources (L3).

## The Navigation Mechanism

Every file at every layer carries, at the bottom, an explicit `SOURCES` section with absolute path references and descriptions:

```
SOURCES (LAYER 2 NAVIGATION)
research/analysis/market-position.md
 -> Competitor mapping and market share analysis supporting Section 2
research/analysis/technical-feasibility.md
 -> Architecture evaluation supporting Section 3
research/dossiers/competitor-profiles.md
 -> Raw competitor data dossiers
```

These aren't footnotes. They are **navigation affordances** for agent consumers. Each description answers the question the consuming agent asks before loading: *what will I find if I go deeper?*

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| Framework & Symmetry | You need the full conceptual foundation — the asymmetry problem, multi-agent routing, DIKW relationship | `references/artifact-pyramid-framework.md` |
| Pipeline Stages | You're building or auditing a pyramid — detailed definitions per layer, navigation format, production flow | `references/pipeline-stages.md` |
| Quality Gates | You need to verify an artifact meets the standard for its layer | `references/quality-gates.md` |
| Worked Example | You want to see a complete synthetic walkthrough of all three layers | `references/synthetic-example.md` |
| Canonical Article | Read the published groktop.us piece — the Layer 3 artifact that defines the concept | `references/canonical-article.md` |
| Intellectual Lineage | How software architecture documentation (4+1 Views, C4, arc42, ADRs) independently discovered progressive disclosure under different names — and what the Artifact Pyramid generalizes beyond them | `references/intellectual-lineage.md` |
| Methodology-to-Pyramid Mapping | How specialist profiles map domain-specific methodologies into the universal pyramid structure, with dimension boundary rules | `references/methodology-to-pyramid-mapping.md` |
| Output Classification Framework | **Role-agnostic** — three questions any specialist can ask to map their outputs into the correct layer: who consumes it, how often, what question it answers. Includes per-layer content contracts to eliminate duplication between 00-index and L1 files. | `references/output-classification-framework.md` |
| Composite Pyramid Synthesis | How to merge multiple subagent pyramids into a root-level composite pyramid — orchestrator flow, SOURCES convention, worked example from jobs-finder pipeline | `references/composite-pyramid-synthesis.md` |
| Delegation Context Template | You're delegating research to subagents and need the exact text to include in context strings to ensure artifact-pyramid output | `references/delegation-context-template.md` |
| Flat-to-Pyramid Migration | You're converting existing flat JSON outputs to artifact-pyramid format — the pattern for L1/L2/L3 structure, 00-index rules, and downstream consumer fallback reads | `references/flat-to-pyramid-migration.md` |
| Nested Pyramid Pattern | You're designing a single system that produces multiple artifact streams over time (multi-phase, multi-epoch) — avoid scatter, nest epochs under a single root pyramid | `references/nested-pyramid-pattern.md` |

## Scripts

| Script | Load when | File |
|--------|-----------|------|
| pyramid-status | You want to audit an existing research directory for structural coverage | `scripts/pyramid-status.sh` |
| extract-atoms | You have raw source text and need candidate atomic claims | `scripts/extract-atoms.py` |

## Templates

| Template | Load when | File |
|----------|-----------|------|
| Project Scaffold | You're starting a new research project and need the index skeleton | `assets/pyramid-template.md` |
| Artifact Inventory | You need to track what exists at each layer across a project | `assets/artifact-inventory.md` |

## Quick Start

```bash
# Scaffold a new research project with all three layer directories
mkdir -p my-project/{01-summary,02-analysis,03-dossiers}
cp assets/pyramid-template.md ./my-project/00-index.md

# Check structural coverage of an existing project
scripts/pyramid-status.sh ./my-project

# Extract candidate atoms from source text
scripts/extract-atoms.py ./my-project/03-dossiers/source-1.txt
```

## Project Structure

```
my-project/
├── 00-index.md              # Project scaffold (from template)
├── 01-summary/              # L1: one file — key findings, implications, links to L2
├── 02-analysis/             # L2: per-dimension files (market, competitive, technical)
├── 03-dossiers/             # L3: source excerpts, transcripts, raw data, methodology
└── artifact-inventory.md    # Cross-layer tracking (from template)
```

The numbered prefixes mirror the pyramid's top-to-bottom orientation: 01 is most consumed, 03 is pulled on demand.

## Key Principles

1. **Progressive disclosure is symmetric.** The same three-tier model governs what agents consume (metadata → instructions → resources) and what they produce (summary → analysis → dossiers).
2. **Each layer is independently consumable.** A product-manager agent reads only the L1 summary. A data-scientist agent reads a single L2 analysis file. A verifier reads L3 dossiers.
3. **Navigation is explicit.** Every file carries a `SOURCES` section with absolute paths and descriptions — not footnotes, but agent navigation affordances answering *what will I find if I go deeper?*
4. **Depth varies by mission complexity.** A simple brief may produce only L1 + 2 analysis files. A competitive landscape may need all three layers with multiple files per layer.
5. **Quality gates are directional.** Material moves from L3 (sources) toward L1 (summary) only when it meets the gate for the target layer.
6. **03-dossiers/ is flat — no subdirectories.** The dossier layer is a flat reference library. Organize with epoch-prefixed or category-prefixed filenames (`epoch-1-validation-edit-3.json`), not nested directories. Subdirectories inside 03-dossiers/ violate the flat-file contract and break the SOURCES navigation path.
7. **Root-level files are amended; lower-level files are fixed.** In multi-epoch or multi-phase systems, `00-index.md`, `01-summary/findings.md`, and `02-analysis/` trajectory files grow as new data arrives. They are rewritten to reflect the current state. Files in `03-dossiers/` and per-category analysis files below `02-analysis/` are created once and never modified — they represent a fixed point in time.

## When NOT to use

- Single-turn Q&A with no research artifacts to preserve
- Tasks producing only ephemeral output (one-off calculations, quick lookups)
- Workflows where the source material IS the final output (no synthesis needed)
