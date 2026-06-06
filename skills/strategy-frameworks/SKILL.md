---
name: strategy-frameworks
description: >-
  CEO methodology for strategic planning, competitive analysis, growth
  strategy, and resource allocation. Covers OKRs, mission/vision/values
  definition, competitive moat analysis (Porter's Five Forces, Blue Ocean),
  strategic narrative construction, growth frameworks (Ansoff Matrix, Three
  Horizons), capital allocation strategy, and M&A evaluation.
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags:
      [
        ceo,
        strategy,
        competitive-analysis,
        growth,
        capital-allocation,
        okrs,
      ]
---

# Strategy Frameworks

CEO methodology for setting direction, analyzing competitive position, identifying growth opportunities, and allocating resources. These frameworks operate at the organizational level — defining where to play, how to win, and what to stop doing.

## Domain Model

| Domain | Covers | Artifact |
|--------|--------|----------|
| **Strategic Planning** | OKRs, mission/vision/values, strategic narrative | Strategy doc, annual plan |
| **Competitive Analysis** | Five Forces, Blue Ocean, moat analysis, competitive positioning | Competitive assessment, positioning map |
| **Growth Strategy** | Ansoff Matrix, Three Horizons, market entry, adjacencies | Growth roadmap, market entry plan |
| **Resource Allocation** | Capital allocation, M&A evaluation, portfolio management | Capital plan, M&A thesis |

## When to Load

Load this skill when the task involves:

- Defining or refining company mission, vision, and values
- Setting OKRs at the organizational level
- Analyzing competitive threats and defensibility
- Evaluating market entry or new product adjacencies
- Building a strategic narrative for investors or employees
- Assessing an M&A target or acquisition thesis
- Allocating capital across business units or initiatives
- Running a horizon planning exercise (Three Horizons)
- Developing a growth strategy using the Ansoff Matrix

## Loading Order

```
skill_view('strategy-frameworks')                   # This — methodology index
skill_view('executive-methodology')                  # Shared decision frameworks
skill_view('artifact-pyramids')                      # Output contract
skill_view('strategy-frameworks', file_path='references/strategic-planning.md')
skill_view('strategy-frameworks', file_path='references/competitive-analysis.md')
skill_view('strategy-frameworks', file_path='references/growth-strategy.md')
skill_view('strategy-frameworks', file_path='references/resource-allocation.md')
```

## Reference Files

| Reference | Load When | File |
|-----------|-----------|------|
| Strategic Planning | You need to set OKRs, define M/V/V, or construct a strategic narrative | `references/strategic-planning.md` |
| Competitive Analysis | You're assessing competitive position, moat durability, or market forces | `references/competitive-analysis.md` |
| Growth Strategy | You're evaluating market entry, adjacencies, or horizon planning | `references/growth-strategy.md` |
| Resource Allocation | You're building a capital allocation plan or evaluating an M&A target | `references/resource-allocation.md` |

## Design Principles

1. **Strategy is choice.** A strategy that does not explicitly say what the organization will stop doing is not a strategy — it's a wish list.
2. **Competitive moats are earned, not declared.** A moat exists when a competitor would find it irrational to invest in competing. Everything else is a feature.
3. **Horizons must be balanced.** Neglect Horizon 1 (core) and cash flow dies. Neglect Horizon 3 (emerging) and the company has no future. The allocation across horizons is the CEO's primary control.
4. **OKRs are a communication tool, not a measurement system.** Their value is in forcing clarity about what matters most, not in the precision of the scores.
5. **Capital allocation is strategy made concrete.** How a company spends its money reveals its actual priorities regardless of what the strategy document says.

## Related Skills

- `executive-methodology` — shared decision frameworks and governance
- `financial-modeling` — CFO-side unit economics, SaaS metrics, fundraising
- `operational-design` — COO-side process design and scaling execution
- `artifact-pyramids` — output contract specification
