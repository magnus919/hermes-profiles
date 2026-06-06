# CFO — Hermes Profile

CFO specialization for Hermes Agent. Owns financial strategy and capital discipline, stress-tests proposals for financial viability, models costs of strategic paths, and evaluates pricing and fundraising strategy.

## What This Profile Provides

- **Financial modeling** — revenue models, cost projections, unit economics, scenario analysis
- **Capital allocation** — investment prioritization, budget constraint analysis, opportunity cost evaluation
- **Fundraising support** — financial model construction, data room preparation, investor narrative
- **Pricing strategy** — pricing model evaluation, revenue model design, monetization analysis
- **Risk assessment** — financial risk identification, sensitivity analysis, downside scenario planning
- **Strategic finance** — make-vs-buy financial analysis, total cost of ownership, cost of capital

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/cfo ~/.hermes/profiles/
hermes --profile cfo
```

## Quick Start

Once the profile is loaded, give it a financial strategy prompt:

> "We're a Series A SaaS company with $3M ARR, 80% gross margin, and 18 months of runway. Model the financial impact of moving upmarket vs. expanding horizontally, and recommend an allocation strategy."

The profile will:
1. Analyze current financial position and unit economics
2. Model alternative strategic scenarios with sensitivities
3. Compute unit economics, payback periods, and capital requirements
4. Produce a financial recommendation backed by documented assumptions
5. Output an artifact pyramid at the engagement path

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking, decision frameworks, governance, stakeholder communication | `skill_view('executive-methodology')` |
| `financial-modeling` | Financial modeling, unit economics, SAAS metrics, pricing strategy, fundraising | `skill_view('financial-modeling')` |

### Supporting References

| Reference | File |
|---|---|
| Financial modeling | `skill_view('financial-modeling', 'references/financial-modeling.md')` |
| Unit economics | `skill_view('financial-modeling', 'references/unit-economics.md')` |
| SaaS metrics | `skill_view('financial-modeling', 'references/saas-metrics.md')` |
| Pricing strategy | `skill_view('financial-modeling', 'references/pricing-strategy.md')` |
| Fundraising | `skill_view('financial-modeling', 'references/fundraising.md')` |
| Decision frameworks | `skill_view('executive-methodology', 'references/decision-frameworks.md')` |

## Output Format

All output follows the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts a financial strategy prompt and produces an artifact pyramid
- [ ] Pyramid contains financial model with documented assumptions and sensitivities
- [ ] Unit economics are decomposed with clear cost and revenue drivers
- [ ] Scenario analysis includes base, downside, and upside cases
- [ ] Response is the absolute path to `00-index.md`, not a summary
