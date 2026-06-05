---
name: receive-mission
description: >-
  Mission reception and scope interpolation. Use when an orchestrator or
  product-manager profile assigns a research brief. Reformulates the brief
  into explicit research questions, scope boundaries, and depth targets.
  This is the mandatory entry point for the researcher-workflow bundle.
compatibility: Hermes Agent
metadata:
  tags: [research, scope, mission, interpolation]
  spec-version: "1.0"
---

# Receive Mission

## When to Use

Load this skill when you are the researcher subagent and have been dispatched with a mission brief. Always start here — the mission brief as received from the orchestrator will not be researcher-native. Your first job is to interpolate it into a structured scope.

## What to Do

### 1. Read the Mission Brief

The orchestrator passes a brief. It may be vague, high-level, or missing key constraints. Do not take it at face value. Extract:

- **Core question:** What is the single most important thing they need to know?
- **Audience:** Who will consume each layer? (PM, data architect, data scientist, etc.)
- **Scope boundaries:** What is explicitly in and out of scope?
- **Depth signal:** Does the brief imply surface-level scanning or deep analysis?
- **Known context:** What does the researcher already know about this topic? (Check SOUL.md, loaded methodology skills, and any context passed in the dispatch.)

### 2. Interpolate into Research Scope

Reformulate the brief into a structured scope document. Write this to `/tmp/researcher-workflow/<mission-slug>/SCOPE.md`:

```markdown
# Research Scope: <Title>

## Mission (as received)
<Orchestrator's original brief>

## Reformulated Research Questions
- Q1: <primary question>
- Q2: <secondary question>
- Q3: <tertiary question>

## Scope Boundaries
- **In scope:** <what's covered>
- **Out of scope:** <what's explicitly excluded>

## Target Audiences & Depth
- **Layer 1 (Summary):** <who reads this — e.g., PM/exec>
- **Layer 2 (Analysis):** <who reads this — e.g., architect>
- **Layer 3 (Detailed):** <who reads this — e.g., data scientist>

## Known Unknowns
- <What you don't know yet that would meaningfully change the picture>

## Research Approach
- <Search strategy: what domains, what types of sources, what search queries>
- <Anticipated depth: light scan vs. deep systematic review>
```

### 3. Set Up Artifact Directory

```bash
mkdir -p /tmp/researcher-workflow/<mission-slug>/{layer-1-summary,layer-2-analysis,layer-3-detailed}
```

### 4. Load the Research Methodology Skill

Load the `research-methodology` skill to access the lifecycle, source evaluation, and synthesis references:

```
skill_view(name='research-methodology')
```

The shared references (`source-evaluation.md`, `structured-analytic-techniques.md`, `synthesis-patterns.md`) are likely needed in the next phase.

## Transition Signals

Move to Phase 2 (Gather) when:
- The SCOPE.md document is written
- The artifact directory is set up
- The research-methodology skill is loaded

## Tool Use

- Terminal for mkdir and filesystem operations
- No web research tools in this phase — that comes next
