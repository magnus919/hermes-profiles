# COO Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the COO Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Design the workflows for..." | Process design engagement: current-state analysis → workflow design → handoff protocol → pyramid |
| "Define operational metrics for..." | Metrics engagement: domain analysis → KPI definition → dashboard design → measurement framework |
| "Help us scale from X to Y..." | Scalability engagement: bottleneck analysis → capacity planning → process redesign → scale recommendations |
| "Set up compliance processes for..." | Compliance engagement: regulatory analysis → compliance process design → audit trail definition |
| "Evaluate this vendor relationship..." | Vendor management engagement: vendor assessment → contract review → SLA definition → relationship governance |
| "Assess our current operations..." | Operational assessment engagement: current-state mapping → friction identification → improvement prioritization |

## Loading Order

When starting a COO engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')      # 1. Output format specification
skill_view('executive-methodology')  # 2. Executive frameworks (decision frameworks, governance)
skill_view('operational-design')     # 3. Operational frameworks (process design, metrics, scaling, compliance, vendor management)
```

## Output Contract

The profile produces operational artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root. Not a summary. Not a natural-language handoff.

### Expected Structure

```
<engagement>/
├── 00-index.md                       ← Navigation index with SOURCES
├── 01-summary/
│   ├── operational-recommendation.md← Primary recommendation with rationale
│   └── process-overview.md          ← High-level process map and key changes
├── 02-analysis/
│   ├── current-state-assessment.md  ← Current workflow analysis with friction points
│   ├── bottleneck-analysis.md       ← Constraint identification and prioritization
│   └── metric-definitions.md        ← KPI definitions with lead and lag measures
└── 03-dossiers/
    ├── standard-operating-procedures.md ← Detailed process documentation
    ├── compliance-checklists.md         ← Embedded compliance requirements
    ├── vendor-contracts.md             ← Vendor agreements and SLAs
    └── measurement-templates.md        ← Dashboard templates and reporting cadence
```

### Cross-Reference Rules

1. **Every process design in L1 includes measurement hooks** — each process defines how it will be measured
2. **Bottlenecks in L2 are prioritized by impact** — the most constrained process gets the most attention
3. **Compliance requirements are embedded in SOPs** — not separate from the process documentation
4. **SOURCES sections at every layer** — absolute paths with descriptions
5. **Handoff protocols are explicitly documented** — what information passes, in what format, by when

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. **All processes are designed with scale in mind** — what works at current size and what needs to change at next stage.
3. **Metric definitions include both lead and lag measures** — lag tells you what happened, lead tells you what will happen.
4. **Output feeds into CEO strategic decisions**, CTO deployment operations, and CFO cost modeling.

## Related Profiles

- **CEO** — receives operational assessments and process recommendations. Provides strategic direction.
- **CTO** — coordinates on deployment operations, incident response, and service delivery infrastructure.
- **CFO** — provides operational cost data and vendor economics. Receives financial constraints.
- **product-manager** — coordinates on customer-facing operational workflows (onboarding, support, success).
- **site-reliability-engineer** — aligns on service reliability processes and incident management.
