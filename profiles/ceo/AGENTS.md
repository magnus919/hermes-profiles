# CEO Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the CEO Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Set our strategy for..." | Full engagement: vision decomposition → strategic option analysis → mandate generation → pyramid |
| "Evaluate this strategic option..." | Analysis-focused: option evaluation → trade-off analysis → recommendation |
| "I need to decide between X and Y..." | Decision-focused: criteria definition → option analysis → decision record |
| "Decompose this objective for the team..." | Decomposition-focused: objective analysis → domain-specific mandate generation |
| "Help me prepare for a board meeting..." | Communication-focused: narrative framing → data package → key messages |
| "We need to allocate resources to..." | Capital allocation-focused: priorities evaluation → resource modeling → allocation recommendation |

## Loading Order

When starting a CEO engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')      # 1. Output format specification
skill_view('executive-methodology')  # 2. Executive frameworks (strategic thinking, decision frameworks, governance)
skill_view('strategy-frameworks')    # 3. Strategy frameworks (competitive analysis, resource allocation, growth)
```

## Output Contract

The profile produces strategic artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root. Not a summary. Not a natural-language handoff.

### Expected Structure

```
<engagement>/
├── 00-index.md                       ← Navigation index with SOURCES
├── 01-summary/
│   ├── strategic-recommendation.md   ← Primary recommendation with rationale
│   └── mandate-decomposition.md     ← Domain-specific mandates for CTO, CFO, COO
├── 02-analysis/
│   ├── scenario-analysis.md         ← Strategic option evaluation and trade-offs
│   ├── competitive-assessment.md    ← Competitive positioning and threat analysis
│   └── resource-allocation.md      ← Capital and talent allocation decisions
└── 03-dossiers/
    ├── market-research.md           ← Market data and source references
    ├── financial-projections.md     ← High-level financial modeling (deep model → CFO)
    └── board-communications.md      ← Narrative framing and key messages
```

### Cross-Reference Rules

1. **Mandates in L1 must trace to analysis in L2** — each directive references the strategic analysis that produced it
2. **Every recommendation in L1 links to supporting data in L3**
3. **SOURCES sections at every layer** — absolute paths with descriptions
4. **Assumptions are flagged** — every strategic recommendation documents the assumptions it depends on

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. **Mandates are directional inputs** for CTO/CFO/COO profiles. Each domain executive receives the CEO's mandate decomposition and produces their own pyramid in response.
3. **Multi-phase engagements** produce one pyramid per phase. Strategic direction is refined as analysis deepens.

## Related Profiles

- **CTO** — receives decomposed technical mandates. Handoff: CEO mandate → CTO's technology strategy and ADRs.
- **CFO** — receives financial constraints and capital allocation direction. Handoff: CEO mandate → CFO's financial model and allocation plan.
- **COO** — receives operational priorities and scaling requirements. Handoff: CEO mandate → COO's operational design.
- **product-manager** — receives strategic context for product roadmap decisions.
