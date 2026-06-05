# Artifact Pyramid Mapping — Product Management

Every engagement produces an artifact pyramid at an absolute filesystem path. This document maps each methodology and artifact type to its pyramid layer.

## Layer Structure

```
              ┌──────────────┐
              │   L1 (Summ)  │  ← Execs and stakeholders stop here
              ├──────────────┤
              │  L2 (Analysis)│  ← Engineers and designers work here
              ├──────────────┤
              │ L3 (Dossiers)│  ← Reference layer — pulled on demand
              └──────────────┘
```

## Complete Mapping

### L1 (Summary)

What lives here: the one-paragraph answer. Fit for an executive brief, a stakeholder update, or the first page of a spec.

| Artifact | What it contains | Audience |
|----------|-----------------|----------|
| Elevator pitch | One-paragraph product description: who, what, why, how it's different | Everyone |
| Vision statement | 1-2 paragraph North Star — what success looks like | Stakeholders, team |
| RICE summary table | Ranked priorities: feature name, RICE score, one-line rationale | Stakeholders, PM |
| Stakeholder brief | Concise recommendation-led update: what we're doing and why | Executives |
| OST root view | The core opportunity — the single customer need everything traces to | Whole team |
| Decision register (summary) | Active decisions, status, and one-line context | Stakeholders |
| MoSCoW overview | What's in/out for the current timebox — one line per item | Team, stakeholders |

**Format:** A single markdown file at `<pyramid-root>/01-summary.md`.

### L2 (Analysis)

What lives here: the reasoning, the requirements, the scope definitions. Engineers and designers read this layer to build from.

| Artifact | What it contains | Audience |
|----------|-----------------|----------|
| Problem statement | 2-4 paragraphs, concrete user language, no solutions | Engineers, designers |
| User stories | Organized by capability area, each with role/action/outcome | Engineers |
| Core concepts | Bounded domain nouns — each defined in one sentence | Whole team |
| Principles | 3-8 design coherence rules that constrain every decision | Engineers, designers |
| PRD sections 2-9 | Problem statement through Success Criteria — the structured spec | Whole team |
| Spec template | The full spec with scope, edge cases, constraints, risks | Engineers, designers |
| MoSCoW detailed | Each item categorized with brief rationale for its placement | Engineers, PM |
| Decision log | Decisions with context, options considered, rationale | Team, future PMs |
| OST opportunity level | Each opportunity with evidence, assumptions, and potential solutions | PM, designers |
| Edge case register | Known edge cases with handling status | Engineers, QA |
| Risk table | Risks, likelihood, impact, mitigations | Engineers, PM |

**Format:** Multiple markdown files at `<pyramid-root>/02-analysis/`. One file per capability area or artifact type. Each L2 file links down to relevant L3 dossiers.

### L3 (Dossiers)

What lives here: the raw material. Source data, transcripts, detailed analyses. No one reads this layer by default — it exists to verify claims and go deeper on demand.

| Artifact | What it contains | When consumed |
|----------|-----------------|---------------|
| Full PRD | All 13 sections including UX sketch, ecosystem map, full risk analysis | When formal sign-off is needed |
| Customer interview transcripts | Raw transcripts or detailed notes from discovery interviews | When challenging an assumption about what users need |
| Competitive deep-dives | Detailed analysis of each competitor's approach | When defending a strategic call |
| RICE scoring inputs | The reach/impact/confidence/effort numbers and their sources | When the prioritization is questioned |
| OST leaf nodes | Individual experiments, their hypotheses, and outcomes | When evaluating whether to continue or pivot |
| RTM (Requirements Traceability Matrix) | Formal mapping from requirements to test cases | In regulated environments |
| Survey raw data | Unprocessed survey responses | When verifying quantitative claims |
| Market sizing worksheets | The assumptions behind market size estimates | When defending TAM/SAM/SOM numbers |
| Stakeholder interview notes | Individual stakeholder needs and concerns | When navigating conflicting priorities |

**Format:** Files at `<pyramid-root>/03-dossiers/`. Organized by source or topic. Each dossier is self-contained and independently consumable.

## Directory Structure Convention

```
<pyramid-root>/
├── 01-summary.md                  # L1 — the one-paragraph answer
├── 02-analysis/
│   ├── 01-problem-statement.md
│   ├── 02-user-stories.md
│   ├── 03-core-concepts.md
│   ├── 04-principles.md
│   ├── 05-scope-moscow.md
│   ├── 06-spec.md
│   ├── 07-decision-log.md
│   ├── 08-opportunity-tree.md
│   └── 09-risks.md
└── 03-dossiers/
    ├── customer-interviews.md
    ├── competitive-analysis.md
    ├── rice-scoring-inputs.md
    ├── survey-data.md
    └── stakeholder-notes.md
```

## Design Principles

1. **Each layer is independently consumable.** An executive reads only L1 and has everything they need. An engineer reads L2 and has the requirements. No one reads L3 by default.

2. **L1 links to L2.** Every claim in the summary points to the analysis file that substantiates it — via the SOURCES section.

3. **L2 links to L3.** Every analysis file that depends on source data links to the relevant dossier — via the SOURCES section.

4. **The path is the contract.** The response to any caller is the absolute path to `00-index.md`. The caller navigates. No natural-language handoff.

## SOURCES Format

Every file at every layer carries this at the bottom:

```
SOURCES (LAYER {N} NAVIGATION)
path/to/file.md
 -> One-line description answering "what will I find if I go deeper?"

path/to/another-file.md
 -> Another dimension or supporting evidence
```

Paths are relative from the file's location. Descriptions answer the question every downstream agent asks before loading: *what will I find if I go deeper?*

## Production Checklist (Gate Audit)

Run this checklist before responding with the path:

- [ ] `00-index.md` exists with navigation table mapping every layer
- [ ] `01-summary/index.md` has SOURCES linking to every L2 file
- [ ] Every L2 analysis file has SOURCES linking to relevant L3 dossiers — **zero orphaned files**
- [ ] Every L3 dossier has source attribution metadata (URL, captured date, author, title)
- [ ] All SOURCES paths resolve correctly from their file's location
- [ ] Each layer is independently consumable (reader stops at any layer and has what they need)
- [ ] Response will be ONLY the absolute path to `00-index.md` — no prose, no summary, no conversation

If any checkbox is unchecked, go back and fix before responding. Missing SOURCES on an analysis file is a hard gate failure — the file is not ready to hand off.
