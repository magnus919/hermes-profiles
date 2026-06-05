---
name: deliver-findings
description: >-
  Delivery phase of the researcher-workflow. Reports findings back to the
  orchestrator with absolute path references and a description of what's
  at each layer of the pyramid. This is the final phase.
compatibility: Hermes Agent
metadata:
  tags: [research, delivery, handoff]
  spec-version: "1.0"
---

# Deliver Findings

## When to Use

Load this skill after Phase 4 (Build Pyramid) is complete. All three layers of the artifact pyramid exist and cross-reference links have been verified.

## What to Do

### 1. Verify the Pyramid is Complete

Check that all expected files exist:

```bash
ls -R /tmp/researcher-workflow/<mission-slug>/
```

### 2. Report Back to the Orchestrator

Return a structured delivery report with absolute paths. The output should enable the orchestrator to read the layer appropriate to their needs, and for downstream consuming agents to drill down as deep as they want.

```
## Research Complete: <Mission Title>

### Artifact Pyramid

**Layer 1 — Executive Summary**
Path: /tmp/researcher-workflow/<mission-slug>/layer-1-summary/README.md
Best for: Product managers, executives — the bottom line and key findings
Contains: Single-page summary with confidence assessments and links to deeper analysis

**Layer 2 — Analysis Collection**
Path: /tmp/researcher-workflow/<mission-slug>/layer-2-analysis/
Best for: Architects, domain experts — thematic analysis organized by finding
Contains: N individual analysis files, each covering a major theme with evidence and links to detailed dossiers
Available files: <list each analysis file with one-line description>

**Layer 3 — Detailed Dossiers**
Path: /tmp/researcher-workflow/<mission-slug>/layer-3-detailed/
Best for: Data scientists, deep investigators — raw findings, source evaluations, gap decisions
Contains: N research logs, source quality assessments, and gap briefs
Available files: <list each dossier with one-line description>

### Methodology Notes
- Sources evaluated using CRAAP framework (see layer-3-detailed/source-quality-assessment.md)
- Gaps evaluated as in-scope:
  - <gap that was filled> → resolved in gather pass 2
- Gaps evaluated as out-of-scope:
  - <gap set aside> → logged in layer-3-detailed/gap-brief-N.md

### Confidence Summary
- High: <list>
- Medium: <list>
- Low: <list>
```

### 3. Do NOT Clean Up

Leave the files in /tmp/ — the OS will clean them up when they're stale. The orchestrator and downstream consumer agents need the files to remain accessible for drill-down.

## Transition Signals

This is the terminal phase. No further transition.

## Tool Use

- Terminal for verifying file existence
- Standard output for the delivery report
