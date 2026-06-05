---
name: product-methodology
description: >-
  Product management frameworks embedded in references/: RICE, MoSCoW,
  Opportunity Solution Trees, customer interviews, spec template, stakeholder
  communication, decision log. All output is organized as an artifact pyramid
  with full SOURCES navigation at every layer.
version: 1.1.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [product-management, prioritization, strategy, customer-discovery, roadmapping]
---

# Product Management Methodology

## Canonical Output

The canonical proof of work for every engagement is an **artifact pyramid** — a three-layer progressively-disclosable structure at an absolute filesystem path. Every methodology and framework in this skill feeds into one of the three layers.

Respond to any caller with the absolute path to `00-index.md` at the pyramid root. Not a summary. Not a handoff paragraph. A path.

The layer mapping is at `references/artifact-pyramid-mapping.md`.

## Production Flow

Build the pyramid in this order. Each phase gates the next.

### Phase 1: Scaffold

```
mkdir -p <pyramid-root>/{01-summary,02-analysis,03-dossiers}
```

Copy `assets/pyramid-template.md` to `<pyramid-root>/00-index.md` and fill in the overview.

### Phase 2: Build L3 Dossiers

For each source (interview, competitive analysis, market data):

1. Create a **flat file** directly in `03-dossiers/` — no subdirectories, no README files acting as folder indexes. A dossier is a single markdown file. If a topic has multiple sources, create multiple flat files (e.g., `customer-interviews.md`, `competitive-analysis.md`).
2. Include source attribution metadata at the top:
   ```
   **Source:** URL or transcript identifier
   **Captured:** YYYY-MM-DD
   **Author:** Person or organization
   **Title:** Original document title
   ```
3. Extract faithfully — no cherry-picking. Include counter-evidence.
4. Add a NOTES section with any methodology context (how the data was collected, processed, etc.)

**Gate C check:** Every dossier has source metadata. Extracts are faithful. Methodology is documented.

### Phase 3: Build L2 Analysis Files

From dossiers, compose one file per analysis dimension (problem, stories, scope, risk, etc.):

1. Each file is self-contained — makes sense read alone
2. Each file has a clear thesis, evidence, and conclusion
3. Each file ends with a `SOURCES` section:

   ```
   SOURCES (LAYER 3 NAVIGATION)
   ../03-dossiers/customer-interviews/transcript-001.md
    -> Primary user pain evidence supporting Section 2

   ../03-dossiers/competitive-analysis/feature-matrix.md
    -> Competitor feature comparison referenced in Scope section
   ```

   **Every file gets a SOURCES section.** No exceptions. Even if the only L3 source is a stub ("Interviews pending — placeholder"), link to it. An orphaned file with no L3 traceability will be rejected at the gate.

**Gate B check:** Every claim traces to L3. Conflict transparency. Narrative structure. Interpretive value.

### Phase 4: Build L1 Summary

From analysis files, compose the single L1 summary:

1. Restate the research question / mission brief
2. 3-5 key findings
3. Implications for the audience
4. End with a `SOURCES` section linking to every L2 analysis file:

   ```
   SOURCES (LAYER 2 NAVIGATION)
   ../02-analysis/01-problem-statement.md
    -> User pain this feature solves

   ../02-analysis/02-user-stories.md
    -> Canonical set of user needs
   ```

**Gate A check:** Every claim links to L2. Self-contained. Implications stated. No orphan claims.

### Phase 5: Quality Gate Audit

Run this checklist before responding:

- [ ] `00-index.md` exists with navigation table
- [ ] `01-summary/index.md` has SOURCES linking to all L2 files
- [ ] Every L2 file has SOURCES linking to L3 — no orphaned analysis files
- [ ] Every L3 dossier has source attribution metadata
- [ ] L3 dossiers are flat files in `03-dossiers/` — no subdirectories, no README placeholders
- [ ] All SOURCES paths resolve correctly (relative from file location)
- [ ] Each layer is independently consumable (a reader stops at any layer and has what they need)

### Phase 6: Respond

Respond with ONLY the absolute path to `00-index.md`. Example:

```
/tmp/pm-test-pyramid/00-index.md
```

No summary text, no analysis recap, no conversation. The caller reads the pyramid.

## References

| Reference | Load when | File |
|-----------|-----------|------|
| Artifact Pyramid mapping | You need to map a specific methodology or artifact to its pyramid layer | `references/artifact-pyramid-mapping.md` |
| RICE scoring | You need to compare unrelated feature proposals by Reach × Impact × Confidence / Effort | `references/rice-framework.md` |
| MoSCoW | Scope is tight for a time-boxed release and you need crisp boundaries | `references/moscow-prioritization.md` |
| Opportunity Solution Trees | The problem space is messy and you need to connect customer needs to build decisions without jumping to solutions | `references/opportunity-solution-trees.md` |
| Customer interview guide | You're planning discovery interviews — how to structure them, what to ask, what to avoid | `references/customer-interview-guide.md` |
| Spec template | You need a requirements document that engineers, designers, and stakeholders can all work from | `references/spec-template.md` |
| Stakeholder communication | You're preparing a message for execs, engineers, designers, or customers — each has a different format | `references/stakeholder-communication.md` |
| Decision log | You've made a decision with tradeoffs that will be questioned later — log the context and expected outcome | `references/decision-log.md` |

## Loading

Load a reference with:
```
skill_view(name="product-methodology", file_path="references/rice-framework.md")
```
