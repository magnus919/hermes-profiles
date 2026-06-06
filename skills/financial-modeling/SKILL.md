---
name: financial-modeling
description: >-
  CFO methodology for unit economics, financial modeling, pricing strategy,
  fundraising, budget frameworks, and SaaS metrics. Covers CAC/LTV/payback
  analysis, revenue projections, cost structures, runway analysis, scenario
  planning, value-based pricing, cap tables, term sheets, zero-based
  budgeting, rolling forecasts, ARR/MRR, churn, NDR, Rule of 40, and
  Magic Number.
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags:
      [
        cfo,
        financial-modeling,
        unit-economics,
        pricing,
        fundraising,
        saas-metrics,
      ]
---

# Financial Modeling

CFO methodology for building financial models, analyzing unit economics, setting pricing strategy, managing fundraising, allocating budgets, and tracking SaaS operating metrics. These frameworks provide the quantitative backbone for strategic decisions across the organization.

## Domain Model

| Domain | Covers | Artifact |
|--------|--------|----------|
| **Unit Economics** | CAC, LTV, payback period, contribution margin, gross margin analysis | Unit economics model |
| **Financial Modeling** | Revenue projections, cost structures, runway analysis, scenario planning, sensitivity | Financial model (3-statement) |
| **Pricing Strategy** | Value-based, competitive, freemium, tiered, usage-based, packaging | Pricing recommendation deck |
| **Fundraising** | Valuation, cap table, dilution, term sheets, investor materials | Data room, pitch deck, cap table |
| **Budget Frameworks** | Zero-based, driver-based, rolling forecasts, variance analysis | Budget model, forecast |
| **SaaS Metrics** | ARR/MRR, churn, NDR, Rule of 40, Magic Number, CAC ratio | Metrics dashboard |

## When to Load

Load this skill when the task involves:

- Building or reviewing a financial model (P&L, balance sheet, cash flow)
- Calculating unit economics (CAC, LTV, payback, contribution margin)
- Designing a pricing strategy or packaging model
- Preparing for a fundraising round (valuation, cap table, term sheets)
- Creating a budget (zero-based, driver-based, rolling forecast)
- Analyzing SaaS operating metrics (ARR, churn, NDR, Rule of 40)
- Running scenario or sensitivity analysis
- Evaluating a pricing change or monetization strategy

## Loading Order

```
skill_view('financial-modeling')                    # This — methodology index
skill_view('executive-methodology')                  # Shared decision frameworks
skill_view('artifact-pyramids')                      # Output contract
skill_view('financial-modeling', file_path='references/unit-economics.md')
skill_view('financial-modeling', file_path='references/financial-modeling.md')
skill_view('financial-modeling', file_path='references/pricing-strategy.md')
skill_view('financial-modeling', file_path='references/fundraising.md')
skill_view('financial-modeling', file_path='references/saas-metrics.md')
```

## Reference Files

| Reference | Load When | File |
|-----------|-----------|------|
| Unit Economics | You need to calculate CAC, LTV, payback period, or contribution margin | `references/unit-economics.md` |
| Financial Modeling | You're building or auditing a financial model with revenue projections and cost structures | `references/financial-modeling.md` |
| Pricing Strategy | You're evaluating pricing models, packaging, or monetization strategy | `references/pricing-strategy.md` |
| Fundraising | You're preparing cap tables, term sheets, valuation, or fundraising materials | `references/fundraising.md` |
| SaaS Metrics | You're analyzing ARR/MRR, churn, NDR, Rule of 40, or Magic Number | `references/saas-metrics.md` |

## Design Principles

1. **Models are tools for thinking, not predictions.** A financial model's value is in forcing explicit assumptions and exposing their implications. The output is never "right" — it's internally consistent with stated assumptions.
2. **Unit economics come before growth.** If you don't know whether each customer is profitable, scaling unprofitable growth will destroy the company. Understand unit economics before raising growth capital.
3. **Pricing is a product feature.** It signals value, segments the market, and drives adoption patterns. Treat pricing decisions with the same rigor as product decisions.
4. **The cap table is a governance document.** Every financing round reshapes incentives. Understand who controls what, and how future rounds will dilute existing holders.
5. **SaaS metrics are management by proxy.** A Rule of 40 score is a summary, not a strategy. The underlying drivers (retention, efficiency, growth) are what matter. Lead with levers, not scores.
6. **Scenarios, not single points.** Every forecast should have a base, upside, and downside case. A single-number forecast implies a level of certainty that never exists.

## Related Skills

- `executive-methodology` — shared decision frameworks and governance
- `strategy-frameworks` — CEO-side strategic planning and capital allocation
- `operational-design` — COO-side operational metrics and process design
- `artifact-pyramids` — output contract specification
