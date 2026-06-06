# CPO Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the CPO Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Define the product strategy for..." | Full strategic engagement: market thesis → competitive stance → bet portfolio → success criteria |
| "Evaluate product-market fit for..." | Fit analysis: cohort metrics → segment evaluation → gap assessment |
| "Where should we place our product bets?" | Bet portfolio: opportunity sizing → risk assessment → resource allocation |
| "How do we differentiate against X?" | Competitive positioning: landscape → positioning → moat analysis |
| "What should our product principles be?" | Product philosophy: strategic axioms → decision guardrails → culture |
| "Prioritize these strategic initiatives..." | Strategic prioritization: opportunity modeling → trade-off analysis → sequencing |
| "What's our competitive landscape for..." | Competitive analysis: market mapping → threat assessment → white space identification |
| "Should we build, buy, or partner for..." | Build-vs-buy-vs-partner: capability assessment → economic analysis → risk evaluation |

## Loading Order

When starting a CPO engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')     # 1. Output format specification
skill_view('executive-methodology') # 2. Executive decision frameworks
skill_view('product-strategy')       # 3. Product strategy frameworks
```

## Output Contract

The profile produces strategic artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root. Not a summary. Not a natural-language handoff.

### Expected Structure

```
<project>/
├── 00-index.md                         ← Navigation index with SOURCES
├── 01-summary/
│   ├── strategic-recommendation.md     ← The bet, the rationale, the expected outcome
│   └── decision-log.md                 ← Key choices and rejected alternatives
├── 02-analysis/
│   ├── market-analysis.md             ← Market sizing, segments, trends
│   ├── competitive-landscape.md       ← Competitor mapping, threat assessment
│   ├── fit-assessment.md              ← Retention cohorts, NPS, willingness-to-pay
│   └── opportunity-sizing.md          ← Bet portfolio, expected value, risk
└── 03-dossiers/
    ├── user-research.md               ← Interview data, behavioral observations
    ├── competitive-intelligence.md    ← Detailed competitor profiling
    └── market-data.md                 ← Third-party data, analyst reports
```

### Cross-Reference Rules

1. **Every recommendation in L1 must trace to L2** — strategic bets link to opportunity sizing analysis
2. **Every analysis in L2 must trace to L3** — market analysis references raw competitive intelligence
3. **SOURCES sections at every layer** — absolute paths with descriptions
4. **Uncertainty is quantified** — any recommendation without supporting L2 analysis is flagged as provisional
5. **Trade-offs are documented** — every recommendation includes what was rejected and why

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. Multi-phase engagements produce one pyramid per phase. Phase N's L3 dossiers serve as context for Phase N+1.
3. Partial pyramids are acceptable. If only a competitive landscape is requested, produce the landscape sections without empty directories for user research.

## Cross-Reference Rules with Related Profiles

1. **CPO → product-manager**: CPO provides strategic frame (L1-L2) as input. PM produces execution artifacts (specs, stories).
2. **CPO → CMO**: Market analysis from CPO feeds go-to-market positioning. CPO's product differentiation constrains CMO's messaging.
3. **CPO → technical-architect**: Roadmap bets inform architecture investment. High-risk product bets need more flexible architectures.
4. **CPO → CFO**: Opportunity sizing feeds financial modeling. Revenue projections depend on product bet sequencing.

## Related Profiles

- **product-manager** — consumes strategic direction as execution constraints. Handoff: pyramid path L1-L2 → PM's problem definition.
- **cmo** — receives product positioning and target segments for go-to-market strategy.
- **cto** — strategic roadmap informs architecture investment decisions and platform bets.
- **data-architect** — product analytics requirements shape data model and instrumentation decisions.
