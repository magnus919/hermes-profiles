# Worked Example: How an Artifact Pyramid Works (Synthetic Data)

This example traces a complete research cycle from mission brief to published summary using fabricated data. All names, numbers, and claims are synthetic.

**Mission Brief:** "Assess whether the company should enter the AI-powered code review market. We need competitive positioning, market size, and technical feasibility analysis."

---

## Layer 3: Detailed Dossiers

These are the source materials — raw data, transcripts, and notes that underpin the analysis.

### Dossier: Competitor Profiles

```
source-id: dossier-001
title: Competitor Market Scan — AI Code Review Tools
captured: 2026-05-20
sources:
  - https://example.edu/code-review-market-2026
  - https://example.com/competitor/comparison
```

**Extracted evidence:**

- Graphite: 200K+ developers, Series B, $50M ARR. Core feature: AI review summaries with inline fix suggestions. Enterprise tier $50/seat/mo.
- CodeRabbit: 150K developers, Series A, $20M ARR. Differentiator: fully automated review queue prioritization.
- Reviewpad: 30K developers, bootstrapped. Focus: custom review rules engine.
- Market projected at $800M by 2028, 28% CAGR (MarketResearch 2026).
- Developer survey (N=1500): 67% want AI code review but only 23% are satisfied with current tools (DevSurvey 2026).

### Dossier: Interview Transcript

```
source-id: dossier-002
title: Engineering Leader Interview — AI Review Needs
captured: 2026-05-21
methodology: 30-min semi-structured interview with VP Engineering, mid-size SaaS
```

**Key excerpts:**

- "We tried Graphite. The review summaries are great but the false positive rate is still too high — about 40% of suggestions are stylistic preferences, not bugs."
- "If someone could build a tool that learns our team's style conventions and only flags things that matter, that's worth $30/seat to us."
- "We're currently spending about 4 hours per week per senior dev on code review. Cutting that in half would save us roughly $200K/year."

### Dossier: Technical Notes

```
source-id: dossier-003
title: Architecture Feasibility — AI Review Engine
captured: 2026-05-22
```

- Fine-tuned LLM approach feasible with labeled training data (existing open datasets: CodeSearchNet, CodeReview-25K)
- Latency requirement: <5s per review to avoid blocking developer workflows
- Key technical risk: false positive rate management (survey data suggests >30% FP = tool abandonment)
- Integration surfaces: GitHub App API, GitLab Webhook API, Bitbucket Cloud API

---

## Layer 2: Analysis Collection

Each file covers one dimension of the research. Each links down to its dossiers.

### Analysis: Market Positioning

```
# Analysis: Competitive Landscape — AI Code Review Market

The code review market is projected at $800M by 2028 with strong
growth (28% CAGR). Current leaders have captured ~50% of known
developer users but satisfaction remains low at 23%.

## Key Findings

Graphite and CodeRabbit dominate mindshare but neither has solved
the false positive problem — the top unmet need (67% want it, 40%
FP rate on existing tools). This creates a wedge: a new entrant
with FP rates under 10% could capture the dissatisfied majority.

## Implications
- Entry is viable if we meet the FP rate threshold
- Pricing at $25-35/seat undercuts Graphite's enterprise tier
- Integration with existing workflows (VS Code, GitHub) is table stakes

SOURCES (LAYER 3 NAVIGATION)
research/dossiers/competitor-profiles.md
 -> Market data, ARR figures, developer counts

research/dossiers/interview-transcripts.md
 -> VP Engineering quote on false positive pain point
```

### Analysis: Technical Feasibility

```
# Analysis: Technical Feasibility — AI Review Engine

Building the core review engine is feasible with existing open
datasets and fine-tuning pipelines. The critical risk is not
model quality but false positive rate management.

## Key Findings
- Fine-tuning on CodeReview-25K + team-specific style data works
- Latency target of <5s is achievable with quantization (Q4)
- FP rate management requires reinforcement learning from
  developer corrections — a flywheel, not a one-shot fix

## Key Risk
If FP rate exceeds 30%, tool abandonment follows. The RL-based
approach requires an initial training period where FP rate is
above target. Mitigation: beta cohort with explicit expectations.

SOURCES (LAYER 3 NAVIGATION)
research/dossiers/technical-notes.md
 -> Architecture evaluation, latency targets, dataset references
```

### Analysis: Financial Projection

```
# Analysis: Financial Model — Market Entry

Conservative estimate: Year 1 revenue of $2.5M at 10,000 seats,
growing to $15M by Year 3 at 50,000 seats. Gross margin 75%
(cloud inference costs).

Breakeven at Month 14 with $4M seed round. Unit economics
improve with scale as inference costs drop faster than
customer acquisition costs.

Sensitivity: FP rate is the largest variable. If FP rate
remains above 30%, churn hits 40% and breakeven extends to
Month 24. If FP rate drops below 10%, organic growth from
referrals reduces CAC by 35%.

SOURCES (LAYER 3 NAVIGATION)
research/dossiers/competitor-profiles.md
 -> Market size and growth projections

research/dossiers/interview-transcripts.md
 -> Willingness-to-pay data from interviews
```

---

## Layer 1: Summary

```
# Summary: AI Code Review Market Entry — Assessment

Research question: Should we enter the AI-powered code review market?

## Key Findings
- The market is growing at 28% CAGR to $800M by 2028
- 67% of developers want better AI review tools; only 23% are
  satisfied with current options
- The critical unmet need is false positive rate management —
  existing tools hover at 40% FP, driving dissatisfaction
- Technical feasibility is established; the risk is operational
  (FP rate flywheel takes time to spin up)
- Conservative financial model shows Year 3 revenue of $15M
  with 75% gross margin

## Implications
- Entry is viable and timed well (market before saturation,
  incumbents haven't solved the core problem)
- The bet is on FP rate management as a competitive moat
- Recommended: proceed to pilot with $4M seed round, 5 beta
  customers, 12-month FP rate improvement target

SOURCES (LAYER 2 NAVIGATION)
research/analysis/market-positioning.md
 -> Competitive landscape and market sizing

research/analysis/technical-feasibility.md
 -> Architecture evaluation and risk assessment

research/analysis/financial-projection.md
 -> Revenue model, breakeven, sensitivity analysis
```

---

## Complete Traceability Chain

```
L1 Summary: "67% of developers want better AI review tools"
  ↓ reads SOURCES
L2 market-positioning.md
  ↓ reads SOURCES
L3 competitor-profiles.md
  → source: DevSurvey 2026 (N=1500, cited)
```

Every claim in the summary traces to a specific analysis file, which traces to a specific dossier, which traces to a specific source. A validator can verify any claim by following the chain downward.
