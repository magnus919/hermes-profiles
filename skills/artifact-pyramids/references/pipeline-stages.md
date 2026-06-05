# Pipeline Stages: The Three Layers in Detail

## Layer Numbering Convention

The Artifact Pyramid numbers layers **top-down**, matching the Agent Skills input model:

| | Agent Skills (Input) | Artifact Pyramid (Output) |
|---|---|---|
| Level 1 | Skill metadata (~100 tokens) | **Summary** — the entry point, most distilled |
| Level 2 | Skill instructions (<5000 tokens) | **Analysis Collection** — detail on demand |
| Level 3 | Reference files (loaded as needed) | **Detailed Dossiers** — the full evidentiary base |

---

## Layer 1: Summary

### Purpose
The entry point for every consuming agent. A single file that states the research question, key findings, and most important implications. No evidence, methodology, or supporting data — those live one layer down.

### Format
A single markdown file, typically a few paragraphs to a few pages.

### Contents
- Research question (restated from mission brief)
- Key findings (3-5 bullet points or short paragraphs)
- Implications (what this means for the audience)
- **SOURCES section** at the bottom linking to Layer 2 analysis files:

```
SOURCES (LAYER 2 NAVIGATION)
research/analysis/market-position.md
 -> Competitor mapping and market share analysis

research/analysis/technical-feasibility.md
 -> Architecture evaluation
```

### Who Consumes
- Product-manager agents (strategic orientation, no technical depth needed)
- Executives (headline-level decisions)
- Quick scanners deciding whether to go deeper

### Quality Gate (Gate A)

- [ ] Every claim in the summary links to a specific Layer 2 analysis file
- [ ] The summary contains no unsupported assertions — everything traces downward
- [ ] The summary is self-contained (makes sense without lower layers)
- [ ] Implications are stated explicitly, not buried in findings

---

## Layer 2: Analysis Collection

### Purpose
Self-contained analysis files, each covering a specific dimension of the research. A consumer who needs only one dimension loads that single file and nothing else.

### Format
Individual markdown files, one per research dimension. Each is independently consumable.

### Typical Dimensions
- Market analysis (size, trends, segmentation)
- Competitive landscape (positioning, strengths, gaps)
- Technical feasibility (architecture, constraints, trade-offs)
- Risk assessment (uncertainties, failure modes, mitigations)
- Regulatory analysis (compliance, jurisdictional issues)

### Contents
- Thesis or research question for this dimension
- Analysis narrative with supporting evidence
- Data visualizations or tables as needed
- **SOURCES section** at the bottom linking to Layer 3 dossiers:

```
SOURCES (LAYER 3 NAVIGATION)
research/dossiers/competitor-profiles.md
 -> Market-by-market competitive positioning data

research/dossiers/interview-transcripts.md
 -> Customer interview transcripts referenced in Section 2
```

### Who Consumes
- Domain-specialist agents (data scientist reads data analysis only)
- In-depth researchers (need one dimension, not the full picture)
- Downstream agents composing cross-domain syntheses

### Quality Gate (Gate B)

- [ ] Each analysis file is self-contained (makes sense without surrounding files)
- [ ] Every claim traces to specific Layer 3 sources
- [ ] Analysis adds interpretive value beyond raw data
- [ ] Conflicting evidence is surfaced, not buried
- [ ] Layer 3 navigation (SOURCES) is complete

---

## Layer 3: Detailed Dossiers

### Purpose
The broadest layer. Source excerpts, raw data tables, interview transcripts, methodology notes. A reference library that consuming agents pull from as needed — not intended for linear reading.

### Format
Multiple files of varying types: markdown notes, raw data exports, captured pages, transcript extracts.

### Typical Contents
- Source excerpts (annotated with source metadata)
- Raw data tables
- Interview or meeting transcripts
- Methodology documentation
- Literature review notes
- Dataset descriptions

### Who Consumes
- Validators (fact-checking claims from upper layers)
- Deep-dive researchers (need the full evidentiary base)
- Downstream analysis tools (embedding pipelines, graph databases)

### Quality Gate (Gate C)

- [ ] Every source has attribution (URL, timestamp, author, title)
- [ ] Extracts are faithful to the original (no misrepresentation)
- [ ] Methodology is documented (how was this data collected/processed?)
- [ ] Dossiers are organized for discoverability (not a raw dump)

---

## Production Flow: How the Pyramid Gets Built

The pyramid is not a formatting template applied after research is complete. It is the natural output of a recursive research methodology:

```
Mission Brief
  ↓
1. Mission Interpolation
   Reformulate the brief into explicit research questions,
   scope boundaries, and a register of known unknowns.
  ↓
2. Systematic Gathering
   Use groktocrawl for all source gathering — scrape for single URLs, search for discovery, agent for synthesis.
   Capture sources, extract evidence, organize into preliminary
   drafts of Layer 3 dossiers.
  ↓
3. Draft Layer 2 Analysis
   From dossiers, compose per-dimension analysis files.
   Add SOURCES sections linking back to dossiers.
  ↓
4. Draft Layer 1 Summary
   From analysis files, compose the summary. Add SOURCES
   section linking to analysis files.
  ↓
5. Gap Evaluation
   For each gap, evaluate: is it in-scope? Would filling it
   change any conclusion in layers above? Does it add depth
   or just bulk?
  ↓
6. Recurse (if needed)
   Go deeper on open gaps. Update layers as new evidence arrives.
  ↓
Publish
```

The key insight: **depth is a function of mission complexity, not a fixed template.** A simple technology explanation brief may produce only a summary and two analysis files. A competitive landscape analysis may require all three layers plus multiple files per layer.

---

## Cross-layer Navigation

### Explicit SOURCES Format

Every file carries this at the bottom:

```
SOURCES (LAYER {N} NAVIGATION)
path/to/file.md
 -> One-line description answering "what will I find if I go deeper?"

path/to/another-file.md
 -> Another dimension or supporting evidence
```

### Consumption Flow

```
L1 Summary
  ↓ reads SOURCES, loads only the analysis it needs
L2 market-position.md
  ↓ reads SOURCES, loads dossiers to verify claims
L3 competitor-profiles.md
```

### Production Flow

```
L3 Source capture
  ↓ compose analysis
L2 Analysis Collection
  ↓ synthesize findings
L1 Summary
```

### Auditing

1. **Forward audit**: Start from dossiers → every source is valid → analysis is sound → summary is trustworthy.
2. **Backward audit**: Start from summary → for each claim, find the L2 file → for each claim in L2, find the L3 dossier → for each source, verify.
