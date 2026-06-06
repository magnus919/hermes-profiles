# CMO Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the CMO Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Define the GTM strategy for..." | Full engagement: positioning → segmentation → channels → budget → measurement |
| "How should we position X against Y?" | Positioning-focused: differentiation → value prop → messaging hierarchy |
| "What's our brand architecture?" | Brand-focused: hierarchy → coherence → governance → equity measurement |
| "Model our acquisition channels..." | Channel analysis: portfolio → efficiency → CAC → rebalancing recommendation |
| "Plan the market entry for..." | Entry strategy: timing → sequencing → resource allocation → risk |
| "What's the messaging strategy for..." | Messaging engagement: audience → message hierarchy → channel adaptation |
| "Analyze our competitive positioning..." | Competitive positioning: landscape → differentiation → positioning statement |
| "Build a growth model for..." | Growth modeling: CAC → LTV → channel mix → scaling scenarios |

## Loading Order

When starting a CMO engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')     # 1. Output format specification
skill_view('executive-methodology') # 2. Executive decision frameworks
skill_view('go-to-market')           # 3. GTM frameworks and growth modeling
```

## Output Contract

The profile produces GTM artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root.

### Expected Structure

```
<project>/
├── 00-index.md                          ← Navigation index with SOURCES
├── 01-summary/
│   ├── gtm-recommendation.md            ← Strategic recommendation, launch timing, budget
│   └── decision-log.md                  ← Trade-offs, rejected alternatives
├── 02-analysis/
│   ├── positioning.md                   ← Segmentation, differentiation, positioning statement
│   ├── channel-strategy.md              ← Channel portfolio, CAC, efficiency analysis
│   ├── messaging-architecture.md        ← Message hierarchy, audience adaptation
│   └── measurement-framework.md         ← KPIs, attribution, decision gates
└── 03-dossiers/
    ├── competitive-research.md          ← Competitor messaging, ad spend, positioning
    ├── audience-insights.md             ← Segmentation data, persona research
    └── channel-benchmarks.md            ← Industry CAC benchmarks, channel unit economics
```

### Cross-Reference Rules

1. **Every recommendation in L1 must trace to L2** — channel strategy links to efficiency analysis
2. **Every analysis in L2 must trace to L3** — positioning references competitive research dossiers
3. **SOURCES sections at every layer** — absolute paths with descriptions
4. **Uncertainty is quantified** — channel performance projections include confidence ranges
5. **Trade-offs are documented** — every recommendation includes what was rejected and why

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. Multi-phase engagements produce one pyramid per phase.
3. Partial pyramids are acceptable. If only a channel analysis is requested, produce the relevant sections.

## Cross-Reference Rules with Related Profiles

1. **CMO → CPO**: Product positioning and differentiation from CPO constrains CMO's messaging. CMO provides market feedback to CPO.
2. **CMO → branding-designer**: Positioning brief and messaging architecture from CMO feeds creative brief for brand designer.
3. **CMO → CFO**: CAC and LTV projections from CMO feed financial modeling and budget planning.
4. **CMO → sales**: Positioning documents, battle cards, and case studies from CMO equip the sales team.

## Related Profiles

- **cpo** — receives go-to-market positioning from CMO; provides product differentiation and target segments
- **brand-designer** — consumes positioning and messaging for visual identity and brand asset creation
- **cfo** — marketing budget, CAC projections, and LTV modeling feed financial planning
