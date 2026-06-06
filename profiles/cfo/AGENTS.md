# CFO Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the CFO Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Model the financials for..." | Financial modeling engagement: assumption definition → model construction → scenario analysis → pyramid |
| "Evaluate the unit economics of..." | Unit economics engagement: revenue decomposition → cost analysis → margin modeling → recommendation |
| "Should we raise money or bootstrap?" | Fundraising assessment: capital needs analysis → fundraising option evaluation → dilution modeling |
| "Set the pricing for..." | Pricing strategy engagement: value analysis → pricing model evaluation → revenue projection |
| "Stress-test this strategic proposal..." | Financial viability assessment: proposal analysis → financial modeling → risk identification → recommendation |
| "Allocate our budget for..." | Capital allocation engagement: strategic priorities → budget construction → trade-off documentation |

## Loading Order

When starting a CFO engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')      # 1. Output format specification
skill_view('executive-methodology')  # 2. Executive frameworks (decision frameworks, governance)
skill_view('financial-modeling')     # 3. Financial frameworks (modeling, unit economics, SaaS metrics, pricing, fundraising)
```

## Output Contract

The profile produces financial artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root. Not a summary. Not a natural-language handoff.

### Expected Structure

```
<engagement>/
├── 00-index.md                       ← Navigation index with SOURCES
├── 01-summary/
│   ├── financial-recommendation.md  ← Primary financial recommendation with rationale
│   └── model-overview.md           ← Key outputs and scenario comparison
├── 02-analysis/
│   ├── scenario-analysis.md        ← Base, downside, and upside scenario results
│   ├── unit-economics.md           ← Per-unit revenue and cost decomposition
│   └── sensitivity-tables.md       ← Key drivers and their impact on outcomes
└── 03-dossiers/
    ├── financial-model.md          ← Model workbook with all calculations
    ├── assumptions.md              ← Documented assumptions with sources and confidence levels
    └── data-sources.md            ← External data references and provenance
```

### Cross-Reference Rules

1. **Every assumption in the model is documented** in L3 with source and confidence level
2. **Scenarios in L2 reference the base model in L3** — all scenarios derive from the same model
3. **Sensitivity analysis in L2 identifies the top 3-5 value drivers** with their impact ranges
4. **SOURCES sections at every layer** — absolute paths with descriptions
5. **All financial data is traceable** to its source (model workbook, external reference, or documented estimate)

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. **Every model includes sensitivity analysis.** The model is not complete until key assumptions have been stress-tested.
3. **Assumptions are the most important output.** They are what the CEO and board will challenge. Document them clearly.
4. **Output feeds into CEO strategic decisions** and provides financial constraints for CTO and COO planning.

## Related Profiles

- **CEO** — provides financial analysis and capital allocation recommendations. Receives strategic direction and constraints.
- **CTO** — evaluates technology investment ROI and infrastructure cost models.
- **COO** — models operational costs, vendor economics, and unit cost of service delivery.
- **product-manager** — evaluates pricing strategy and feature-level unit economics.
