# Delegation Context Template: Artifact Pyramid Mandate

When delegating research to a subagent via `delegate_task`, the subagent does NOT load any skills. The folder structure, SOURCES requirement, and output format MUST be explicitly included in the `context` string. This template provides the exact text to include.

## Minimal Template

Copy this block verbatim into every research delegation context:

```
OUTPUT FORMAT: You MUST produce a compliant Artifact Pyramid, not flat files.

Create this directory structure at <your-output-path>/:
├── 00-index.md              ← entry point (mandatory)
├── 01-summary/findings.md   ← L1: one findings file
├── 02-analysis/             ← L2: one file per dimension/opportunity
└── 03-dossiers/             ← L3: raw scrape outputs, search results

Every file MUST end with a ## SOURCES section linking to deeper layers:
- L1 files link to L2 analysis files
- L2 files link to L3 dossiers
- Each SOURCES entry includes a description answering: "what will I find if I go deeper?"

When the output directory doesn't exist yet, create it with the full pyramid structure before writing any files.

Respond with ONLY the absolute path to the completed pyramid's 00-index.md.
Do NOT respond with natural language summaries or prose.
```

## Expanded Template (with rationale)

For first-time delegations or when the subagent needs more context:

```
OUTPUT FORMAT: You MUST produce a compliant Artifact Pyramid (https://www.groktop.us/artifact-pyramid-progressive-disclosure/).

The pyramid has three layers consumed top-down:
- L1 (01-summary/): Key findings, most important implications. One file only.
- L2 (02-analysis/): Per-dimension analysis files. One file per discovery. Self-contained.
- L3 (03-dossiers/): Raw source excerpts, scrape outputs, methodology notes.

Directory structure at <your-output-path>/:
├── 00-index.md              ← entry point (mandatory)
├── 01-summary/findings.md   ← L1: one findings file
├── 02-analysis/             ← L2: one file per promising result
└── 03-dossiers/             ← L3: raw outputs

Every file MUST end with a ## SOURCES section. SOURCES are navigation affordances
for downstream agents — each entry answers "what will I find if I go deeper?"
L1 SOURCES links to 02-analysis/ files. L2 SOURCES links to 03-dossiers/ files.

If the output directory doesn't exist, create it with mkdir -p before writing.

Respond with ONLY the absolute path to 00-index.md. No summary, no natural language.
```

## Why This Is Necessary

`delegate_task` subagents have no access to the parent's loaded skills, memory, or conversation history. They receive only the `context` string. If the artifact-pyramid folder structure isn't in that string, they will produce flat files at the root of their output directory. The flat files will contain good content but will lack navigation affordances, making them unusable by downstream agents in the pipeline.
