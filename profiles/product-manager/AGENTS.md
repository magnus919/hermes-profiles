# Product-Manager Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the product-manager Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Write a spec for..." | Full engagement: problem definition → user stories → scope → acceptance criteria → pyramid |
| "Prioritize these features..." | Prioritization-focused: criteria selection → RICE/MoSCoW scoring → ranked output |
| "Draft a stakeholder update..." | Communication-focused: audience identification → message framing → delivery format |
| "Help me plan customer interviews..." | Discovery-focused: interview guide → question design → synthesis template |
| "We need to decide between X and Y..." | Decision-focused: option analysis → trade-off documentation → decision log |
| "Define the roadmap for..." | Strategy-focused: goals → horizons → dependencies → risk assessment |

## Loading Order

When starting a product engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')    # 1. Output format specification
skill_view('product-methodology')  # 2. Product frameworks (loads references on demand)
```

## Output Contract

The profile produces product artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root. Not a summary. Not a natural-language handoff.

### Expected Structure

```
<project>/
├── 00-index.md              ← Navigation index with SOURCES
├── 01-summary/
│   ├── problem-statement.md ← The problem being solved
│   └── recommendations.md   ← Key findings and next steps
├── 02-analysis/
│   ├── user-stories.md      ← User needs and acceptance criteria
│   ├── prioritization.md    ← RICE/MoSCoW scoring and trade-offs
│   └── scope.md             ← In-scope / out-of-scope boundaries
└── 03-dossiers/
    ├── customer-interviews.md ← Raw interview data and synthesis
    ├── competitive-analysis.md ← Competitive landscape
    └── research-sources.md     ← Supporting data and references
```

### Cross-Reference Rules

1. **Every claim in L1 must trace to L2** — recommendations link to prioritization analysis
2. **Every analysis in L2 must trace to L3** — user stories reference raw interview data
3. **SOURCES sections at every layer** — absolute paths with descriptions
4. **Partially-informed analysis is flagged** — if L3 data is missing, mark the analysis as provisional

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. Multi-phase engagements produce one pyramid per phase. Phase N's L3 dossiers serve as context for Phase N+1.
3. Partial pyramids are acceptable. If only a spec is requested, produce the spec sections without empty directories for customer research.

## Supporting References

| Reference | Load Command |
|---|---|
| RICE prioritization | `skill_view('product-methodology', 'references/rice-framework.md')` |
| MoSCoW prioritization | `skill_view('product-methodology', 'references/moscow-prioritization.md')` |
| Opportunity Solution Trees | `skill_view('product-methodology', 'references/opportunity-solution-trees.md')` |
| Customer interview guide | `skill_view('product-methodology', 'references/customer-interview-guide.md')` |
| Spec template | `skill_view('product-methodology', 'references/spec-template.md')` |
| Stakeholder communication | `skill_view('product-methodology', 'references/stakeholder-communication.md')` |
| Decision log | `skill_view('product-methodology', 'references/decision-log.md')` |

## Related Profiles

- **technical-architect** — consumes product requirements as architectural constraints. Handoff: pyramid path L2 analysis → technical-architect's constraint discovery.
- **data-architect** — receives prioritized feature list to design data model implications.
