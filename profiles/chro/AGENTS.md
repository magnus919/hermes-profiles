# CHRO Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the CHRO Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Design the org structure for..." | Org design engagement: team topology → decision rights → coordination → implementation |
| "Build a talent strategy..." | Talent strategy: workforce planning → skill gaps → hiring plan → development roadmap |
| "Design a compensation framework..." | Compensation design: philosophy → benchmarking → incentive structure → implementation |
| "Assess organizational health..." | Health assessment: engagement survey → culture audit → retention → burnout → recommendations |
| "Plan our hiring pipeline..." | Hiring plan: role definition → sourcing → interview process → offer strategy → timeline |
| "Design performance management..." | Performance system: framework → calibration → feedback → growth path |
| "Identify our leadership pipeline..." | Succession planning: bench assessment → development needs → readiness evaluation |
| "Assess our culture..." | Culture audit: values alignment → behavioral norms → feedback patterns → intervention design |

## Loading Order

When starting a CHRO engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')     # 1. Output format specification
skill_view('executive-methodology') # 2. Executive decision frameworks
skill_view('org-design')             # 3. Organizational design frameworks
```

## Output Contract

The profile produces organizational artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root.

### Expected Structure

```
<project>/
├── 00-index.md                           ← Navigation index with SOURCES
├── 01-summary/
│   ├── recommendation.md                 ← Key findings, design decisions, implementation priorities
│   └── decision-log.md                   ← Trade-offs, rejected alternatives, risks
├── 02-analysis/
│   ├── org-assessment.md                ← Current structure, capability inventory, skill gaps
│   ├── talent-analysis.md               ← Workforce gaps, succession readiness, bench strength
│   ├── compensation-design.md           ← Philosophy, benchmarking, incentive structure
│   ├── culture-assessment.md            ← Engagement, values alignment, behavioral patterns
│   └── performance-framework.md         ← System design, calibration process, feedback model
└── 03-dossiers/
    ├── role-definitions.md              ← Job architecture, role expectations, leveling guide
    ├── benchmark-data.md                ← Compensation benchmarks, market comparisons
    ├── survey-results.md                ← Engagement survey data, verbatim comments
    └── interview-frameworks.md          ← Structured interview guides, evaluation criteria
```

### Cross-Reference Rules

1. **Every recommendation in L1 must trace to L2** — org design recommendations link to assessment analysis
2. **Every analysis in L2 must trace to L3** — compensation analysis references benchmark data
3. **SOURCES sections at every layer** — absolute paths with descriptions
4. **Uncertainty is quantified** — talent projections and retention risk include confidence ranges
5. **Change management implications are documented** — every org design recommendation includes transition risk assessment

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. Multi-phase engagements produce one pyramid per phase.
3. Partial pyramids are acceptable. If only a compensation review is requested, produce the compensation sections without empty directories for culture assessment.

## Cross-Reference Rules with Related Profiles

1. **CHRO → CEO/board**: Org health and talent capability assessments inform strategic planning and investment decisions.
2. **CHRO → CLO**: Compensation designs must comply with employment law. Culture and performance systems must respect legal boundaries.
3. **CHRO → CFO**: Headcount plans, compensation budgets, and benefits costs from CHRO feed financial models.
4. **CHRO → CPO**: Product strategy determines required capabilities. CHRO's talent plan must align with product roadmap.

## Related Profiles

- **clo** — employment law, compliance training, and workplace policies guide talent practices
- **cfo** — headcount planning, compensation budgets, and benefits design inform financial models
- **cpo** — product strategy determines required organizational capabilities and skill needs
