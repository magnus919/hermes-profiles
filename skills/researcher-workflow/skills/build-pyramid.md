---
name: build-pyramid
description: >-
  Progressive disclosure artifact pyramid assembly. Loaded after gap evaluation
  determines saturation is reached. Reads gathered material from layer-3-detailed/
  and produces layered output: summary (layer 1), analysis collection (layer 2),
  detailed dossiers (layer 3). Each layer links downward with descriptions.
compatibility: Hermes Agent
metadata:
  tags: [research, pyramid, artifacts, writing, synthesis]
  spec-version: "1.0"
---

# Build Pyramid

## When to Use

Load this skill after Phase 3 (Evaluate Gaps) indicates saturation. All gathered material is in `/tmp/researcher-workflow/<mission-slug>/layer-3-detailed/`. This phase transforms material into the progressive disclosure pyramid.

## Pyramid Structure

```
layer-1-summary/
└── README.md              ← Executive summary (single file, high-level)

layer-2-analysis/
├── 01-market-analysis.md   ← Thematic analysis files
├── 02-risk-assessment.md   ← One per major theme
├── 03-competitive-landscape.md
└── ...

layer-3-detailed/
├── 01-gather-pass-1.md     ← Raw research logs
├── 02-gather-pass-2.md     ← One per research pass
├── gap-brief-1.md          ← Gap evaluation records
├── source-quality-assessment.md
└── ...
```

The pyramid shape: narrow at the top (summary, dense), wide at the bottom (detailed, comprehensive).

## What to Do

### 1. Read All Gathered Material

Read all files in `layer-3-detailed/` to understand the full body of findings.

### 2. Build Layer 3 — Detailed Dossiers (already populated)

The research logs from Phase 2 already live here. Review and organize them into a logical order. Prefix filenames with numbers to indicate reading order. Add a `_index.md` that lists all dossiers with one-line descriptions:

```markdown
# Detailed Dossiers: <Mission Title>

## Available Files

- `01-gather-pass-1.md` — Initial research pass covering <breadth>
- `02-gather-pass-2.md` — Follow-up on <specific gap>
- `source-quality-assessment.md` — CRAAP evaluation of all sources
- `gap-brief-1.md` — Gap that was evaluated as out-of-scope
```

### 3. Build Layer 2 — Analysis Collection

For each major theme from the research, write a focused analysis file. Each analysis file should:

- State the claim or finding
- Summarize the supporting evidence
- Note conflicting evidence or uncertainty
- Link to specific dossiers in layer 3 for detail

Link format (absolute path + description):

```
See [/tmp/researcher-workflow/<mission-slug>/layer-3-detailed/01-gather-pass-1.md]
for the initial discovery that led to this finding.
```

### 4. Build Layer 1 — Executive Summary

Write a single README.md in `layer-1-summary/`. This is the most constrained file — densest, most distilled. Structure:

```markdown
# Research Summary: <Title>

## One-Paragraph Bottom Line
<The single most important thing the PM needs to know>

## Key Findings
- <Finding 1> → [See analysis](</analysis/01-market-analysis.md>)
- <Finding 2> → [See analysis](</analysis/02-risk-assessment.md>)

Each finding links to the relevant analysis file with a brief description of what's there.

## Confidence Assessment
- **High confidence:** <claims with strong, triangulated evidence>
- **Medium confidence:** <claims with reasonable but incomplete evidence>
- **Low confidence:** <claims with thin or conflicting evidence>

## Out of Scope
- <Items evaluated and set aside during gap evaluation>

## How to Dive Deeper
- For market context and competitive landscape → load layer-2-analysis/
- For full source logs and gap evaluations → load layer-3-detailed/
```

### 5. Ensure Links Work

After writing all layers, verify that each cross-reference in layers 1 and 2 actually resolves to a file on disk. A broken link defeats progressive disclosure.

## Transition Signals

Proceed to Phase 5 (Deliver) when:
- All three layers are written
- Cross-reference links are verified
- Files are organized with numbered prefixes and _index.md guides

## Tool Use

- Terminal for reading/synthesizing files
- write_file for creating artifact files
- No web research tools — you're building, not gathering
