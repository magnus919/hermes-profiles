---
name: evaluate-gaps
description: >-
  Gap evaluation and recursion decision. Loaded after the gather phase.
  Applies the three-question model to decide whether to recurse deeper
  or proceed to pyramid assembly. Guides the researcher through
  structured gap assessment.
compatibility: Hermes Agent
metadata:
  tags: [research, gaps, recursion, evaluation]
  spec-version: "1.0"
---

# Evaluate Gaps

## When to Use

Load this skill after completing Phase 2 (Gather). The research log exists with documented findings, sources, and gaps. This phase determines whether you need another research pass or can proceed to building the pyramid.

## What to Do

### 1. Read Current State

Read the scope document and the latest research log to understand what you have and what's missing.

### 2. Apply the Three-Question Model

For each gap documented in the research log, ask:

**Q1: Is this gap in scope?**
Does the missing information fall within the scope boundaries defined in the mission brief? If it's outside scope, note it but do not pursue it. If it's inside scope, proceed to Q2.

**Q2: Would filling this gap change any conclusion?**
If you knew the answer to this gap, would it meaningfully alter the findings you plan to report? If not — if it would add color but not change the picture — this is low-priority. If it would change a conclusion, it's high-priority.

**Q3: Am I adding depth or just adding bulk?**
Does pursuing this gap add a new dimension of understanding (depth), or does it pile on more of the same kind of evidence (bulk)? Depth compounds. Bulk dilutes. Pursuing depth is worth another pass. Pursuing bulk is not.

### 3. Make the Recursion Decision

| Pattern | Decision |
|---------|----------|
| Gap is in-scope, changes a conclusion, adds depth | **Recurse** — full or targeted pass |
| Gap is in-scope, doesn't change conclusions, adds depth | **Recurse** — lightweight pass (search only) |
| Gap is in-scope, doesn't change conclusions, adds bulk | **Stop** — note the gap for transparency |
| Gap is out of scope | **Stop** — log as out-of-scope |

### 4. Determine Recursion Intensity

If you decide to recurse, choose the appropriate intensity:

- **Lightweight** (1-2 quick searches): `groktocrawl search "<specific query>" --limit 3`
- **Targeted** (need one article or source): `groktocrawl scrape <url>`
- **Full pass** (need significant new territory): `groktocrawl agent "<focused research prompt>"`
- **Browser-needed** (JS-rendered content suspected): groktocrawl browser suite

### 5. Execute or Advance

If recursing: return to Phase 2 (Gather) with a focused mission for the specific gap. Write a gap brief:

```markdown
# Gap Brief: <gap description>

## What We Need
<specific question the follow-up should answer>

## Why It Matters
<how it connects to Q2 — changes a conclusion>

## Suggested Approach
<lightweight / targeted / full pass / browser>
```

Save this as `/tmp/researcher-workflow/<mission-slug>/layer-3-detailed/gap-brief-<N>.md`.

After the recursion pass, evaluate gaps again. A second recursion cycle is acceptable. A third cycle requires strong justification — at that point, consider whether the scope itself was too broad.

If not recursing: proceed to Phase 4 (Build Pyramid).

## Transition Signals

- **If recursing:** Return to Phase 2 (Gather) with the gap brief
- **If stopping:** Proceed to Phase 4 (Build Pyramid) — all gathered material is in layer-3-detailed/

## What to Save

Each evaluation cycle produces a gap brief and the recursion decision. Save these so the pyramid can reference what was consciously set aside.
