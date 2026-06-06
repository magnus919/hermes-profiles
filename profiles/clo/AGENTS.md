# CLO Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the CLO Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Review this contract..." | Contract risk analysis: liability, indemnification, termination, dispute resolution |
| "What's the regulatory exposure for..." | Regulatory assessment: framework mapping → exposure analysis → compliance plan |
| "Assess our IP position..." | IP analysis: portfolio review → defensibility → gap analysis → filing recommendations |
| "Check license compatibility..." | Open-source audit: dependency tree → license compatibility → risk mitigation |
| "Design a compliance framework..." | Compliance design: regulatory mapping → policies → audit protocol |
| "Evaluate the legal risk of..." | Risk assessment: scenario analysis → probability → exposure → mitigation |
| "Negotiate these contract terms..." | Negotiation guidance: fallback positions → leverage points → deal-breakers |
| "Review this for M&A due diligence..." | Due diligence: target assessment → data room → risk flagging → purchase agreement review |

## Loading Order

When starting a CLO engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')     # 1. Output format specification
skill_view('executive-methodology') # 2. Executive decision frameworks
skill_view('legal-strategy')         # 3. Legal strategy frameworks
```

## Output Contract

The profile produces legal artifacts as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root.

### Expected Structure

```
<project>/
├── 00-index.md                            ← Navigation index with SOURCES
├── 01-summary/
│   ├── risk-assessment.md                 ← Key risks, probabilities, exposures, recommendations
│   └── decision-log.md                    ← Trade-offs, rejected approaches, mitigation costs
├── 02-analysis/
│   ├── regulatory-analysis.md            ← Applicable frameworks, exposure mapping, compliance gaps
│   ├── ip-analysis.md                    ← Portfolio assessment, defensibility, enforcement options
│   ├── contract-review.md                ← Key clauses, risk allocation, negotiation positions
│   └── compliance-assessment.md          ← Framework alignment, audit readiness, remediation plan
└── 03-dossiers/
    ├── relevant-statutes.md              ← Applicable laws, regulations, and guidelines
    ├── case-precedent.md                 ← Relevant case law and regulatory decisions
    ├── contract-excerpts.md              ← Key contract provisions under review
    └── license-texts.md                  ← Open-source licenses and compatibility notes
```

### Cross-Reference Rules

1. **Every risk flag in L1 must trace to L2** — risk assessments link to detailed regulatory or contract analysis
2. **Every legal conclusion in L2 must trace to L3** — regulatory analysis references specific statutes and precedent
3. **SOURCES sections at every layer** — absolute paths with descriptions
4. **Uncertainty is quantified** — legal risks include probability ranges (likely/probable/unlikely) and financial exposure estimates
5. **Alternatives are documented** — every recommendation includes the rejected alternatives and their trade-offs

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. Multi-phase engagements produce one pyramid per phase.
3. Partial pyramids are acceptable. If only a contract review is requested, produce the contract review sections without empty directories for regulatory analysis.

## Cross-Reference Rules with Related Profiles

1. **CLO → CPO**: Regulatory constraints from CLO inform product roadmap decisions and feature viability.
2. **CLO → CTO/engineering**: Open-source license audits and IP risks from CLO constrain technology choices.
3. **CLO → CFO**: Litigation reserves, regulatory fines, and compliance costs from CLO feed financial planning.
4. **CLO → CHRO**: Employment law, non-compete/enforceability, and compliance training requirements from CLO inform talent strategy.

## Related Profiles

- **cpo** — provides regulatory constraints that affect product strategy and feature prioritization
- **cto** — technology and open-source license guidance shapes architecture and dependency decisions
- **cfo** — legal exposures, litigation reserves, and compliance costs inform financial planning
- **chro** — employment law, compliance training, and workplace policies affect people operations
